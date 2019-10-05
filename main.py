from sys import argv
from re import match, compile
from enum import Enum, auto

SYMBOL_TABLE = {}

class Type(Enum):
    IDENT = auto()
    CONSTANT = auto()
    QUESTION_OPERATOR = auto()
    LESS_KEYWORD = auto()
    GREATER_KEYWORD = auto()
    EQUAL_KEYWORD = auto()
    COLON = auto()
    ASSIGNMENT_OPERATOR = auto()
    SEMI_COLON = auto()
    PLUS_OPERATOR = auto()
    MINUS_OPERATOR = auto()
    STAR_OPERATOR = auto()
    SLASH_OPERATOR = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()


if __name__ == "__main__":
    if(len(argv) != 2):
        print("NOT FOUND FILE")
    else:
        with open(argv[1], "r") as file:
            lines = file.readlines()
            file.close()
            for line in lines:
                # ascii 값으로 32 이하면 전부 white-space 로 치환
                for index in range(len(line)):
                    if ord(line[index]) <= ord(' '):
                        line = line[:index] + ' ' + line[index + 1:]
                tokens = line.split(' ')
                # 빈 문자 제거
                tokens = list(filter(lambda a: a != '', tokens))
                print(tokens)

def token_type(token):
    tokenType = {
        "?" : Type.QUESTION_OPERATOR,
        "<" : Type.LESS_KEYWORD,
        ">" : Type.GREATER_KEYWORD,
        "==" : Type.EQUAL_KEYWORD,
        ":" : Type.COLON,
        "=" : Type.ASSIGNMENT_OPERATOR,
        ";" : Type.SEMI_COLON,
        "+" : Type.PLUS_OPERATOR,
        "-" : Type.MINUS_OPERATOR,
        "*" : Type.STAR_OPERATOR,
        "/" : Type.SLASH_OPERATOR,
        "(" : Type.LEFT_PARENTHESIS,
        ")" : Type.RIGHT_PARENTHESIS
    }
    if token in tokenType.keys():
        return tokenType[token]
    identCheck = compile("/([a-zA-Z])[a-zA-Z0-0]\w+/g")
    if identCheck(token) != None:
        return Type.IDENT
    numberCheck = compile("\d")
    if numberCheck(token) != None:
        return Type.CONSTANT
    
def lexical(next_token, token_string):
    if len(token_string) > 1:
        pass
    else:
        pass
    
def lexical():
    next_token = None