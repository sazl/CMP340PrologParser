

class Token(object):

    def __init__(self, token='', value='', line=0, span=()):
        self.__token = token
        self.__value = value
        self.__line  = line
        self.__span  = span

    def __str__(self):
        return "{:<10} {:<10} {:^5} {:^5}".format(
            self.token, self.value, self.line, self.span)

    @property
    def token(self):
        return self.__token

    @property
    def value(self):
        return self.__value

    @property
    def line(self):
        return self.__line
    
    @property
    def span(self):
        return self.__span

#-------------------------------------------------------------------------------

class LexicalError(Exception):

    def __init__(self, text, line, span):
        super().__init__("unknown lexeme: {} line: {} span: {}".format(text, line, span))

#-------------------------------------------------------------------------------

class Lexer(object):

    def __init__(self):
        self.__index = 0
        self.__tokens = []
        self.__line = 1
        self.__position = 0
        self.__stream_index = 0
        self.__stream = ""

    @property
    def index(self):
        return self.__index
    @index.setter
    def index(self, index):
        self.__index = index

    @property
    def tokens(self):
        return self.__tokens
    @tokens.setter
    def tokens(self, tokens):
        self.__tokens = tokens

    @property
    def line(self):
        return self.__line
    @line.setter
    def line(self, line):
        self.__line = line

    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, position):
        self.__position = position

    @property
    def stream(self):
        return self.__stream
    @stream.setter
    def stream(self, stream):
        self.__stream = stream

    @property
    def stream_index(self):
        return self.__stream_index
    @stream_index.setter
    def stream_index(self, stream_index):
        self.__stream_index = stream_index
    
    @property
    def current(self):
        return self.stream[self.stream_index]

    def next(self):
        if self.current == '\n':
            self.position = 0
            self.line += 1
        else:
            self.position += 1
        self.stream_index += 1

    def not_end(self):
        return self.stream_index < len(self.stream)

    @property
    def current_token(self):
        return self.tokens[self.index]

    def next_token(self):
        self.index += 1
        if self.not_token_end():
            return self.current_token

    def not_token_end(self):
        return self.index < len(self.tokens)

    def tokenize(self, token, value=''):
        return Token(token, value, self.line, span=self.position)

    def raise_error(self):
        raise LexicalError(self.current, self.line, self.stream_index)

    def lex_file(self, filename):
        with open(filename) as f:
            self.stream = f.read()
            self.lex()

    def lex_next_token(self):
        if not self.skip_space():
            return
        if self.is_uppercase():
            return self.variable()
        elif self.is_lowercase() or self.current == "'":
            return self.atom()
        elif self.is_digit():
            return self.numeral()
        elif self.current == '?':
            return self.query()
        elif self.current == ':':
            return self.rule()
        elif self.current == ',':
            self.next()
            return self.tokenize('comma')
        elif self.current == '.':
            self.next()
            return self.tokenize('dot')
        elif self.current == '(':
            self.next()
            return self.tokenize('lparen')
        elif self.current == ')':
            self.next()
            return self.tokenize('rparen')
        else:
            self.raise_error()
    
    def lex(self):
        while self.not_end():
            self.tokens.append(self.lex_next_token())
        self.tokens = self.tokens[:-1]
        return self.tokens

    def skip_space(self):
        while self.not_end() and self.current.isspace():
            self.next()
        return self.not_end()

    def is_special(self):
        return self.current in "+-*/\\^~:.? #$&"

    def is_digit(self):
        return self.current.isdigit()

    def is_lowercase(self):
        return self.current.islower()

    def is_uppercase(self):
        return (self.current.isupper() or self.current == '_')

    def is_alphanumeric(self):
        return (self.is_lowercase() or self.is_uppercase() or self.is_digit())

    def is_character(self):
        return self.is_alphanumeric() or self.is_special()

    def string(self):
        self.next()
        result = ''
        while self.is_character() and self.current != "'":
            result += self.current
            self.next()
        return result

    def characterlist(self):
        charlist = ''
        while self.is_alphanumeric():
            charlist += self.current
            self.next()
        return charlist

    def smallatom(self):
        satom = self.current
        self.next()
        satom += self.characterlist()
        return satom

    def rule(self):
        self.next()
        if self.current == '-':
            self.next()
            return self.tokenize('rule')
        else:
            self.raise_error()

    def query(self):
        self.next()
        if self.current == '-':
            self.next()
            return self.tokenize('query')
        else:
            self.raise_error()

    def numeral(self):
        num = ''
        while self.is_digit():
            num += self.current
            self.next()
        return self.tokenize('numeral', int(num))

    def variable(self):
        var = self.current
        self.next()
        var += self.characterlist()
        return self.tokenize('variable', var)

    def atom(self):
        result = ''
        if self.current == "'":
            result = self.string()
        else:
            result = self.smallatom()
        return self.tokenize('atom', result)

#-------------------------------------------------------------------------------

import sys
if __name__ == "__main__":
    lex = Lexer()
    lex.lex_file(sys.argv[1])
    while lex.not_token_end():
        print(lex.next_token())

#-------------------------------------------------------------------------------
