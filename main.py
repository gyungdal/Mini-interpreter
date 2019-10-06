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
    # 숫자 분리
    numberCheck = compile("^[0-9]*$")
    if numberCheck.match(token) != None:
        return Type.CONSTANT
    # 숫자도 아니면 변수
    return Type.IDENT
    
def lexical(line):
    # ascii 값으로 32 이하면 전부 white-space 로 치환
    for index in range(len(line)):
        if ord(line[index]) <= ord(' '):
            line = line[:index] + ' ' + line[index + 1:]
    tokens = line.split(' ')
    # 빈 문자 제거
    tokens = list(filter(lambda a: a != '', tokens))
    #print(tokens)
    #토큰들을 분리해서 toekn_string에 저장
    for token_string in tokens:
        # 토큰 타입은 next_token에 저장됨
        # enum이니까 정수 형태임
        next_token = token_type(token_string)
        print(next_token, end=', ')
    print('')
    next_token = None

if __name__ == "__main__":
    if(len(argv) != 2):
        print("NOT FOUND FILE")
    else:
        with open(argv[1], "r") as file:
            lines = file.readlines()
            file.close()
            for line in lines:
                lexical(line)

