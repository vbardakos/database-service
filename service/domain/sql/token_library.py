from sqlparse.sql import Token, Identifier, TokenList, Parenthesis
from sqlparse import tokens as tkn
from typing import TypeVar


TknType = TypeVar('TknType', bound=Token)


class SQLTokens(list):

    @staticmethod
    def _compose(token: TknType, value: str):
        return Token(token, value)


if __name__ == '__main__':
    tkns = SQLTokens()
    print(tkns)
    tkns.append(10)
    print(tkns)
    print(type(Token))

token = Token(tkn.Name, 'name')
