import lexer as lexical

#-------------------------------------------------------------------------------

class ParseError(Exception):

    def __init__(self, errors):
        super().__init__("Parse Error:")
        self.__errors = errors

    @property
    def errors(self):
        return self.__errors

#-------------------------------------------------------------------------------

class Parser(object):

    def __init__(self, lexer):
        self.__lexer = lexer
        self.__error = False
        self.__errors = []

    @property
    def lexer(self):
        return self.__lexer

    def current_token(self):
        return self.lexer.current_token
        
    def token(self):
        return self.lexer.current_token.token

    def next_token(self):
        return self.lexer.next_token()
        
    def not_token_end(self):
        return self.lexer.not_token_end()

    @property
    def error(self):
        return self.__error
    @error.setter
    def error(self, error):
        self.__error = error

    @property
    def errors(self):
        return self.__errors
    @errors.setter
    def errors(self, errors):
        self.__errors = errors

    def raise_error(self, expected):
        self.error = True
        token = self.current_token()
        self.errors.append("expected: {} got: {} line: {} span: {}".format(
            expected, token.token, token.line, token.span))

    def parse(self):
        self.program()
        if self.error:            
            raise ParseError(self.errors)
    
    def program(self):
        if self.token() == 'query':
            self.next_token()
            query = self.query()
            return ('program', query)
        elif self.token() == 'atom':
            while self.token() == 'atom':
                clist = self.clause_list()
                self.next_token()
                query = self.query()
                return ('program', clist, query)
        else:
            self.raise_error('?- or clause')
             
    def clause_list(self):
        clauses = []
        while self.token()=='atom':
            cl = self.clause()
            clauses.append(cl)
        return ('clause_list', clauses)

    def clause(self):
        pred = self.predicate()
        predicates = None
        if self.token()=='rule':
            self.next_token()
            predicates=self.predicate_list()
        
        if self.token()!='dot':
            self.raise_error('.')
             
        self.next_token()
        return ('clause', pred, predicates)

    def query(self):
        predicates = self.predicate_list()
        if self.token()!='dot':
            self.raise_error('.')
        return ('query', predicates)

    def predicate_list(self):
        predicates = []
        while self.token()=='atom':
            pred = self.predicate()
            predicates.append(pred)
            if self.token()=='atom':
                self.raise_error(',')
                 
            elif self.token()=='comma':
                self.next_token()
        return ('predicate_list', predicates)

    def predicate(self):
        atom=True
        tlist=None
        self.next_token()
        if self.token()=='lparen':
            self.next_token()
            tlist=self.term_list()
            if self.token()!='rparen':
                self.raise_error(')')
                 
            self.next_token()
        return ('predicate', atom, tlist)

    def term_list(self):
        tlist = []
        while self.token()=='atom' or self.token()=='variable' or self.token()=='numeral':
            t = self.term()
            tlist.append(t)
            if self.token()=='atom' or self.token()=='variable' or self.token()=='numeral':
                self.raise_error(',')
            elif self.token()=='comma':
                self.next_token()
                if self.token()!='atom' and self.token()!='variable' and self.token()!='numeral':
                    self.raise_error('atom or variable or numeral')
        return ('term_list', tlist)

    def term(self):
        if self.token()=='atom':
            self.next_token()
            if self.token() == 'lparen':
                self.structure()
            else:
                pass
        elif self.token()=='variable':
            self.next_token()
        elif self.token()=='numeral':
            self.next_token()
        else:
            self.structure()

    def structure(self):
        self.next_token()
        tlist=self.term_list()
        if self.token() != 'rparen':
            self.raise_error(')')
             
        self.next_token()
        return ('structure', tlist)

#-------------------------------------------------------------------------------

import os, re
if __name__ == "__main__":
    for file in sorted(os.listdir('.')):
        if re.match(r'\d+.txt', file):

            try:
                lex = lexical.Lexer()
                lex.lex_file(file)
                print(file, "lexically correct")
            except lexical.LexicalError as l:
                print(file, end=' ')
                for e in l.errors:
                    print(e)
            try:
                parser = Parser(lex)
                parser.parse()
                print(file, "syntactically correct")
            except ParseError as e:
                print(file, end=' ')
                for e in e.errors:
                    print(e)
            print("\n")
