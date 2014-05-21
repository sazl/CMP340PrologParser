import lexer as lexical

class ParseError(Exception):

    def __init__(self, expected_tokens, token):
        super().__init__("expected: {} got: {} line: {} span: {}".format(
            expected_tokens, token.token, token.line, token.span))

def none_on_error(f):
    def func(self):
        try:
            return f(self)
        except ParseError as p:
            print(p)
            return None
    return func

class Parser(object):

    def __init__(self, lexer):
        self.__lexer = lexer

    @property
    def lexer(self):
        return self.__lexer

    @property
    def current_token(self):
        return self.lexer.current

    def next_token(self):
        return self.lexer.next()

    def accept(self, token):
        if self.current_token().token != token:
            return False
        return self.next_token()
    
    def expect(self, token):
        if not self.accept(token):
            return False
        return self.current_token()

    def accept_repeated(self, func):
        items = []
        while True:
            item = func()
            if not item:
                break
            items.append(item)
        return items

    @none_on_error
    def program(self):
        print('program')
        clist = self.clause_list()
        query = self.query()
        return ('program', clist, query)
    
    @none_on_error
    def clause_list(self):
        print('clause_list')
        clauses = self.accept_repeated(self.clause)
        return ('clause_list', clauses)

    @none_on_error
    def clause(self):
        print('clause')
        pred = self.predicate()
        preds = None
        if self.accept('rule'):
            preds = self.predicate_list()
        self.accept('dot')
        return ('clause', pred, preds)

    @none_on_error
    def query(self):
        print('query')
        self.accept('query')
        preds = self.predicate_list()
        self.accept('dot')
        return ('query', preds)

    @none_on_error
    def predicate_list(self):
        print('predicate_list')
        preds = [self.predicate()]
        while self.accept('comma'):
            preds.append(self.predicate())
        return ('predicate_list', preds)

    @none_on_error
    def predicate(self):
        print('predicate')
        atom = self.accept('atom')
        term_list = None
        if self.accept('lparen'):
            term_list = self.term_list()
            self.accept('rparen')
        return ('term_list', atom, term_list)

    @none_on_error
    def term_list(self):
        print('term_list')
        terms = [self.term()]
        while self.accept('comma'):
            terms.append(self.term())
        return ('term_list', terms)

    @none_on_error
    def term(self):
        print('term')
        if self.accept('atom'):
            pass
        elif self.accept('variable'):
            pass
        elif self.accept('numeral'):
            pass
        else:
            self.structure()

    @none_on_error
    def structure(self):
        print('structure')
        self.accept('atom')
        self.accept('lparen')
        terms = self.term_list()
        self.accept('rparen')
        return ('structure', terms)
        
if __name__ == "__main__":
    lex = lexical.Lexer()
    lex.lex_file('test.pl')
    parser = Parser(lex)
    print(parser.program())
