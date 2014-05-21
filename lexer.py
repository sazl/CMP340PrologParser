import re

def re_name(name, regex):
    return '(?P<{}>{})'.format(name, regex)
def re_union(*regexes):
    return '|'.join('({})'.format(r) for r in regexes)
def re_modify(regex, modify):
    return '({}){}'.format(regex, modify)
def re_wrap(regex, left, right):
    return '{}{}{}'.format(left, regex, right)

special       = r'[+\-*/\\^~:.?\s#$&]'
digit         = r'\d'
lowercase     = r'[a-z]'
uppercase     = r'[A-Z_]'
alphanumeric  = re_union(lowercase, uppercase, digit)
character     = re_union(alphanumeric, special)
string        = re_modify(character, '+')
characterlist = re_modify(alphanumeric, '+')
smallatom     = re_modify(lowercase, '+')
    
lparen        = re_name('lparen', r'\(')
rparen        = re_name('rparen', r'\)')
dot           = re_name('dot', r'\.')
comma         = re_name('comma', r'\,')
rule          = re_name('rule', r'\:-')
query         = re_name('query', r'\?-')
numeral       = re_name('numeral', re_modify(digit, '+'))
variable      = re_name('variable', re_modify(uppercase, '+'))
atom          = re_name('atom', re_union(smallatom, re_wrap(string, "'", "'")))
lexer         = re.compile(re_union(lparen, rparen, dot, comma, rule, query,
                                    numeral, variable, atom))

class LexicalError(Exception):

    def __init__(self, text, line, span):
        super().__init__("unknown lexeme: {} line: {} span: {}".format(text, line, span))

class Token(object):

    def __init__(self, token='', value='', line=0, span=0):
        self.__token = token
        self.__value = value
        self.__line  = line
        self.__position = position

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

class Lexer(object):

    def __init__(self):
        self.__index = 0
        self.__tokens = []

    def lexical_error(self, line, text):
        match = re.search('[^\s]+', text)
        if match:
            raise LexicalError(match.group(), line, match.span())

    def lex_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                unmatched = lexer.sub('', line)
                if unmatched.strip():
                    return self.lexical_error(i+1, unmatched)
            
                for m in lexer.finditer(line):
                    for k, v in m.groupdict().items():
                        if v:
                            self.tokens.append(Token(token=k, value=v, line=i+1, span=m.span()))
            return self.tokens

    def next(self):
        self.index += 1
        return self.tokens[self.index]

    def previous(self):
        self.index -= 1
        return self.tokens[self.index]

    def current(self):
        return self.tokens[self.index]

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
