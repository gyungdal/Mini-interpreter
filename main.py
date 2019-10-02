from sys import argv
from pyparsing import Word, Literal, alphas, nums
from enum import Enum

CONSTANT = Word(nums)
IDENT = Literal("if") | Literal("while")

class Type(Enum):
    QUESTION_OPERATOR = Literal("?")
    LESS_KEYWORD = Literal("<")
    GREATER_KEYWORD = Literal(">")
    EQUAL_KEYWORD = Literal("==")
    COLON = Literal(":")
    ASSIGNMENT_OPERATOR = Literal("=")
    SEMI_COLON = Literal(";")
    PLUS_OPERATOR = Literal("+")
    MINUS_OPERATOR = Literal("-")
    STAR_OPERATOR = Literal("*")
    SLASH_OPERATOR = Literal("/")
    LEFT_PARENTHESIS = Literal("(")
    RIGHT_PARENTHESIS = Literal(")")


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
                tokens = list(filter(lambda a: a != '', tokens))
                print(tokens)

def token_type(token):
    pass 

def lexical(next_token, token_string):
    if len(token_string) > 1:
        pass
    else:
        pass
    
def lexical():
    next_token = None