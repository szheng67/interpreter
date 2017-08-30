#TOKEN types
#EOF == no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER','PLUS','MINUS', 'EOF'

class Token(object):
    def __init__(self,type,value):
        self.type=type #INTEGER, PLUS OR EOF
        self.value=value # 0-9, '+', or None
    
    def __str__(self):
        '''
        String representation of the class instance
        #Examples:
        Token(INTEGER,3)
        Token(PLUS, '+')
        '''
        return 'Token({type},{value})'.format(
        type=self.type,
        value=repr(self.value)
    )   

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self,text):
        #input string, e.g. "1+1"
        self.text=text
        #index into self.text
        self.pos=0
        #current token instance
        self.current_token=None
    def error(self):
        raise Exception('Error parsing input')
    def get_next_token(self):
        while(self.pos<len(self.text)-1 and self.text[self.pos]==" "):
            self.pos+=1
        if self.pos>len(self.text)-1:
            return Token(EOF,None)
        current_char=self.text[self.pos]
        end_pos=self.pos
        if current_char.isdigit():
            while (end_pos+1<len(self.text) and self.text[end_pos+1].isdigit()):
                end_pos+=1
            token=Token(INTEGER,int(self.text[self.pos:end_pos+1]))
            self.pos+=end_pos+1
            return token
        if current_char=='+':
            token=Token(PLUS,current_char)
            self.pos+=1
            return token
        if current_char=='-':
            token=Token(MINUS,current_char)
            self.pos+=1
            return token
        self.error()

    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.get_next_token()
        else:
            self.error()
    def ops(self,plus,minus):
        if self.current_token.type==plus or self.current_token.type==minus:
            self.current_token=self.get_next_token()
        else:
            self.error()

    def expr(self):
        # expr -> INTEGER PLUS INTEGER
        # set current token to the first token from the input
        self.current_token=self.get_next_token()
        #validate current token
        left=self.current_token
        self.eat(INTEGER)
        op = self.current_token
        self.ops(PLUS,MINUS)
        right = self.current_token
        self.eat(INTEGER)

        if op.value=="+":
            res=left.value+right.value
        elif op.value=="-":
             res=left.value-right.value
        return res


def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter=Interpreter(text)
        result=interpreter.expr()
        print(result)

if __name__=='__main__':
    main()
