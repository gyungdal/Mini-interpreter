from sys import argv
from re import match, compile
from enum import Enum, auto

SYMBOL_TABLE = {}

class Type(Enum):
    IDENT = auto()
    CONSTANT = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    LESS_KEYWORD = auto()
    GREATER_KEYWORD = auto()
    EQUAL_KEYWORD = auto()
    COLON = auto()
    SEMI_COLON = auto()
    ASSIGNMENT_OPERATOR = auto()
    PLUS_OPERATOR = auto()
    MINUS_OPERATOR = auto()
    STAR_OPERATOR = auto()
    SLASH_OPERATOR = auto()
    QUESTION_OPERATOR = auto()
    OPERATOR = PLUS_OPERATOR

def token_type(token):
    tokenType = {
        "<" : Type.LESS_KEYWORD,
        ">" : Type.GREATER_KEYWORD,
        "==" : Type.EQUAL_KEYWORD,
        "(" : Type.LEFT_PARENTHESIS,
        ")" : Type.RIGHT_PARENTHESIS,
        ":" : Type.COLON,
        ";" : Type.SEMI_COLON,
        "?" : Type.QUESTION_OPERATOR,
        "=" : Type.ASSIGNMENT_OPERATOR,
        "+" : Type.PLUS_OPERATOR,
        "-" : Type.MINUS_OPERATOR,
        "*" : Type.STAR_OPERATOR,
        "/" : Type.SLASH_OPERATOR
    }
    # 일치하는 키워드 토큰 분리
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
    #토큰들을 분리해서 token_string에 저장
    lexicalList = []
    tokenTypeList = list()
    for token_string in tokens:
        # 토큰 타입은 next_token에 저장
        # enum이니까 정수 형태
        next_token = token_type(token_string)
        tokenTypeList.append(next_token)
        lexicalList.append({
            'next_token' : next_token,
            'token_string' : token_string
        })
        print(token_string, end=' ')
    flag = False
    print('==> ID: {}; CONST: {}; OP: {}; '.format(tokenTypeList.count(Type.IDENT), 
                                                    tokenTypeList.count(Type.CONSTANT), 
                                                    len([x for x in tokenTypeList if x.value >= Type.OPERATOR.value])), end=' ')
    print()
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

