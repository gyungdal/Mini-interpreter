from sys import argv
from re import match, compile
from enum import Enum, auto

#enum 들 정의
class Flag(Enum):
    YES = auto()
    NO = auto()
    NOP = auto() 

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
    
#전역 변수
SYMBOL_TABLE = {}
flag : Flag = Flag.YES


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
    
# == Statements
def start(tokenList):
    global flag
    flag = Flag.YES
    statements(tokenList)
    if flag == Flag.YES:
        print("<YES>")
    elif flag == Flag.NO:
        print("<NO>")
    
def statements(tokenList):
    index = -1
    for idx, token in enumerate(tokenList):
        #print(token)
        if token['next_token'] == Type.SEMI_COLON:
            index = idx
            break
    
    # 내부에 semi colon이 있으면 다른거
    if index is not -1:
        # 들어있는 경우
        statement(tokenList[:index])
        statements(tokenList[index + 1:])
    else:
        statement(tokenList)
        
def statement(tokenList):
    global SYMBOL_TABLE
    global flag
    if len(tokenList) > 2:
        if tokenList[0]['next_token'] == Type.IDENT and tokenList[1]['next_token'] == Type.ASSIGNMENT_OPERATOR:
            val = expression(tokenList[2:])
            if type(val) is str :
                SYMBOL_TABLE[tokenList[0]['token_string']] = "Unknown"
            else:
                SYMBOL_TABLE[tokenList[0]['token_string']] = int(val)
        else:
            flag = Flag.NO

def expression(tokenList):
    global flag
    index = -1
    for idx, token in enumerate(tokenList):
        #print(token)
        if token['next_token'] == Type.PLUS_OPERATOR or token['next_token'] == Type.MINUS_OPERATOR:
            index = idx
            break
    
    # 내부에 semi colon이 있으면 다른거
    if index is not -1:
        if tokenList[index]['next_token'] == tokenList[index + 1]['next_token']: 
            t = '-'
            if tokenList[index]['next_token'] == Type.PLUS_OPERATOR:
                t = '+'
            print("<Warning: 중복 연산자({}) 제거>".format(t))
            temp = tokenList[:index]
            temp2 = tokenList[index + 1:] 
            tokenList = temp + temp2
            flag = Flag.NOP
        val1 = term(tokenList[:index]) 
        val2 = expression(tokenList[index + 1:])
        if tokenList[index]['next_token'] == Type.PLUS_OPERATOR:
            if type(val1) is str or type(val2) is str:
                return "Unknown"
            else:
                return int(val1) + int(val2)
        else:
            if type(val1) is str or type(val2) is str:
                return "Unknown"
            else:
                return int(val1) - int(val2)
    else:
        return term(tokenList)

def term(tokenList):
    index = -1
    for idx, token in enumerate(tokenList):
        #print(token)
        if token['next_token'] == Type.STAR_OPERATOR or token['next_token'] == Type.SLASH_OPERATOR:
            index = idx
            break
    
    # 내부에 semi colon이 있으면 다른거
    if index is not -1:
        val1 = factor(tokenList[:index])
        val2 = term(tokenList[index + 1:])
        if tokenList[index]['next_token'] == Type.STAR_OPERATOR:
            if type(val1) is str or type(val2) is str:
                return "Unknown"
            else:
                return int(val1) * int(val2)
        else:
            return 
            if type(val1) is str or type(val2) is str:
                return "Unknown"
            else:
                return int(val1) / int(val2)
    else:
        return factor(tokenList)

def factor(tokenList):
    global SYMBOL_TABLE
    global flag
    if len(tokenList) < 1:
        return 1
    type = tokenList[0]['next_token']
    if type == Type.LEFT_PARENTHESIS:
        return expression(tokenList[1:len(tokenList) - 1])
    elif type == Type.IDENT:
        if tokenList[0]['token_string'] not in SYMBOL_TABLE.keys():
            print("<Error: 정의 되지 않은 변수({})가 참조됨>".format(tokenList[0]['token_string']))
            flag = Flag.NOP
            SYMBOL_TABLE[tokenList[0]['token_string']] = "Unknown"
        return SYMBOL_TABLE[tokenList[0]['token_string']]
    elif type == Type.CONSTANT:
        return int(tokenList[0]['token_string'])


def condition(tokenList):
    global flag
    if tokenList[0]['next_token'] == Type.LESS_KEYWORD or tokenList[0]['next_token'] == Type.GREATER_KEYWORD or tokenList[0]['next_token'] == Type.EQUAL_KEYWORD:
        pass
    else:
        if flag is not Flag.NOP:
            flag = Flag.NO
            
def compare_value(tokenList):
    global flag
    if tokenList[0]['next_token'] == Type.IDENT and tokenList[1]['next_token'] == Type.COLON and tokenList[2]['next_token'] == Type.IDENT:
        pass
    else:
        if flag is not Flag.NOP:
            flag = Flag.NO
        
def lexical(line):
    # ascii 값으로 32 이하면 전부 white-space 로 치환
    for index in range(len(line)):
        if ord(line[index]) <= ord(' '):
            line = line[:index] + ' ' + line[index + 1:]
    tokens = line.split(' ')
    # 빈 문자 제거
    tokens = list(filter(lambda a: a != '', tokens))
    tempTokens = []
    for token in tokens:
        if "(" in token:
            spl = token.split('(')
            tempTokens.append(spl[1])
        elif ")" in token:
            spl = token.split(')')
            tempTokens.append(spl[0])
        else:
            tempTokens.append(token)
    tokens = tempTokens
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
    print('==> ID: {}; CONST: {}; OP: {}; '.format(tokenTypeList.count(Type.IDENT), 
                                                    tokenTypeList.count(Type.CONSTANT), 
                                                    len([x for x in tokenTypeList if x.value >= Type.OPERATOR.value])), end=' ')
    start(lexicalList)
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
    print("Result ==> ", end='')
    for key, values in SYMBOL_TABLE.items():
        print("{} : {}; ".format(key, values), end='')
    print()

