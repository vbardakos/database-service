import sqlparse
from sqlparse import tokens as tkn
from sqlparse import tokens, sql
from sqlparse.sql import Token, Identifier, Statement, Where, IdentifierList
from typing import Any

SELECT = Token(tkn.DML, 'select')
DOT = Token(tkn.Punctuation, '.')
SEP = Token(tkn.Punctuation, ',')
AS = Token(tkn.Keyword, 'as')
LIMIT = Token(tkn.Keyword, 'limit')
SPACE = Token(tkn.Whitespace, ' ')
FROM = Token(tkn.Keyword, 'from')
WHERE = Token(tkn.Keyword, 'where')
ORDER = Token(tkn.Keyword, 'order by')
END = Token(tkn.Punctuation, ';')


class SQLBuilder:
    def construct_columns(self, *names: str, **as_names: str):
        columns = list(map(self._identifier, map(self._column, names)))
        columns += map(self._identifier, map(self._column_as, as_names.items()))
        return self._identifiers(columns) if len(columns) > 1 else columns[0]

    def _column_as(self, name: tuple[str, str]):
        name, new_name = name
        return self._column(name) + [AS] + [self._identifier(self._column(new_name))]

    def _column(self, string: str) -> list[Token]:
        names = string.strip().split(DOT.value)
        return self._composer([Token(tkn.Name, name) for name in names], [DOT])

    def _identifier(self, components: list[Token]):
        return Identifier(tokens=self._composer(components, [SPACE]))

    def _identifiers(self, components: list[Identifier]):
        return IdentifierList(tokens=self._composer(components, [SEP, SPACE]))

    def _statement(self, components: list[Token | Identifier | IdentifierList]):
        return Statement(tokens=self._composer(components + [END], [SPACE]))

    def _lit(self, value: Any):
        match value:
            case int():
                ttype = tkn.Number.Integer
            case float():
                ttype = tkn.Number.Float
            case str() as v:
                ttype = tkn.String.Single
            case _:
                raise NotImplementedError('Not Implemented')
        return Token(ttype, repr(value))

    def _composer(self, components: list[sqlparse.sql], separators: list[tkn]) -> list:
        component = components.pop(0)
        if not components:
            return [component]
        elif DOT in {component, components[0]}:
            return [component] + self._composer(components, separators)
        else:
            return [component] + separators + self._composer(components, separators)


stmt1 = """select p.columnA as cA, columnB from sales.item where 1 = 2 order by column1, column2 desc limit 1;"""

if __name__ == '__main__':
    build = SQLBuilder()
    parsed = sqlparse.parse(stmt1)
    select_stmt = []
    select_stmt.append(sql.Token(tokens.DML, 'SELECT'))
    select_stmt.append(sql.Token(tokens.Whitespace, ' '))
    select_stmt.append(sql.Token(tokens.Wildcard, '*'))
    # select_stmt.append(sql.Token(sq))
    select_stmt.append(sql.Token(tokens.Newline, '\n'))
    select_stmt.append(sql.Token(tokens.Keyword, 'FROM'))
    select_stmt.append(sql.Token(tokens.Whitespace, ' '))
    select_stmt.append(sql.Identifier(tokens=[sql.Token(tokens.Name, 'sales'), sql.Token(tokens.Punctuation, '.'), sql.Token(tokens.Name, 'item')]))
    select_stmt.append(sql.Token(tokens.Punctuation, ';'))
    new_stmt = sql.Statement(tokens=select_stmt)
    # print(parsed[0].tokens[-2].value == repr(1))
    # print(new_stmt, sqlparse.format(stmt1, reindent=True, use_space_around_operators=True, keyword_case='upper'), sep='\n\n')
