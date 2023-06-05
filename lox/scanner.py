"""
Module for the scanner.
"""

from typing import List
from enum import Enum, auto
import logging

LOGGER = logging.getLogger(__name__)

class TokenType(Enum):
    # single char tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # one or two char tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # KEYWORDS.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    
    EOF = auto()


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return self.type.name + " " + self.lexeme + " " + str(self.line)

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        # LOGGER.info(f"start: {self.start}, current: {self.current}, line: {self.line}, source: {self.source}")

    def is_at_end(self) -> bool:
        LOGGER.info(f"current {self.current}, len(source): {len(self.source)}")
        return self.current >= len(self.source)

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            # we are at the beginning of the next lexeme
            self.start = self.current
            self.scan_token()
            # break
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        
        c = self.advance()
        LOGGER.info(f"in scan_token(), c = {c}")

        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
            case "<":
                self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">":
                self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.handle_string()
            # case '0'| '1'| '2'| '3'| '4'| '5'| '6'| '7'| '8'| '9':
            #     self.handle_number()
            
            case _:
                if self.is_digit(c):
                    self.handle_number()
                else:
                    # TODO - call error() from lox.py, need to move it out to a separate module
                    LOGGER.error("default case")


    def advance(self):
        LOGGER.info(f"len(source) {len(self.source)}, current {self.current}")
        consume = self.source[self.current]
        self.current += 1
        return consume

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def add_token(self, token_type: TokenType, **kwargs) -> None:
        LOGGER.info(f"start: {self.start}, current: {self.current}")
        # import pdb;pdb.set_trace()
        text = self.source[self.start: self.current]

        if 'literal' in kwargs:
            literal = kwargs.get('literal')    
            self.tokens.append(Token(token_type, text, literal, self.line))
            return
        
        self.tokens.append(Token(token_type, text, None, self.line))
    
    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            LOGGER.error(f"{self.line} Unterminated string")
            return
        
        # the closing ".
        self.advance()
        # trim the surrounding quotes
        value = self.source[self.start+1 : self.current]
        LOGGER.info(f"trimmed string {value}")
        self.add_token(TokenType.STRING, value)

    def handle_number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        # if dot
            # read next char
            # if num continue
                # else throw error
        if self.source[self.current] == ".":
            while self.is_digit(self.peek()):
                self.advance()
        
        value = self.source[self.start : self.current]
        LOGGER.info(f"number = {value}")
        self.add_token(TokenType.NUMBER, value)

    def is_digit(self, character: str) -> bool:
        return character in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
