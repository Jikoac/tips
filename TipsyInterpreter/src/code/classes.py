import random
import typing as tp
import sys

sys.dont_write_bytecode=True

def conv(__base__:dict={},**items):
    __base__={} or __base__
    __base__.update(items)
    return __base__

class tclass:
    type=None
    default=None
    def __init__(self,value=None):
        if value==None:
            value=self.default
        self.value=value
    def __call__(self,index:int|None=None):
        if self.value==None:
            return 'void'
        if index!=None:
            return str(self.value[index])
        return str(self.value)
    def raw(self):
        if self.value==None:
            return 'void'
        return str(self.value)
    def __str__(self):
        return self.raw()
    
void=tclass()
    
class trandom(tclass):
    type='generator'
    default=[void]
    def __call__(self,index:int|None=None):
        if index!=None:
            return self.value[index]
        return random.choice(self.value)
    def raw(self,seperator:str=', '):
        return seperator.join(self.value)
    
class tstring(tclass):
    def __init__(self,value=[]):
        self.value=', '.join(value)
    type='string'
    default=''

class tnumber(tclass):
    def __init__(self,value=None):
        operator='+'
        if value==None:
            self.value=self.default
        else:
            for op in ['+','-','*','/']:
                if op in value:
                    operator=op
            self.value=eval(operator.join(value))
    type='number'
    default=0

class tset(tclass):
    type='set'
    def __call__(self,sep:str=', '):
        return sep.join(self.value)
    def raw(self,sep:str=', '):
        return sep.join(self.value)

class tbool(tclass):
    type='bool'
    def __init__(self,value=[]):
        value=''.join([str(values) for values in value])
        if value.lower()=='no' or value=='0' or value.lower()=='false' or value.lower()=='null' or value.lower()=='void' or value.lower()=='none':
            self.value=False
        else:
            self.value=bool(value)
    def raw(self,format:tp.Literal['string','number']=''):
        if format=='string':
            return str(bool(self.value))
        elif format=='number':
            return int(bool(self.value))
        else:
            return 'yes' if self.value else 'no'
    def __call__(self):
        return self.raw()

class tkeyset(tclass):
    type='keyset'
    default=[]
    def __init__(self,value:list[str]=[]):
        if all(['=' in bit for bit in value]):
            sep='='
        else:
            sep=':'
        self.value={}
        for item in value:
            key=item.split(sep)[0]
            val=item.split(sep)[1]
            self.value.update({key:val})
    def __call__(self,index=None):
        if index==None:
            output=[]
            for key,val in self.value.items():
                output.append(f'{key}={val}')
            return ', '.join(output)
        return self.value[index]
    def raw(self,index=None):
        return self(index)
class twrs(tclass):
    type='wrs',
    default=[]
    def __init__(self,value:list[str]=[]):
        self.value=tkeyset(value).value
    def __call__(self):
        pool=[]
        for item,chance in self.value.items():
            pool+=[item]*int(chance)
        return random.choice(pool)
    def raw(self,index=None):
        if index==None:
            output=[]
            for key,val in self.value.items():
                output.append(f'{key}={val}')
            return ', '.join(output)
        return self.value[index]
class tfunction(tclass):
    type='function'
    def __init__(self,name='',args=[]):
        self.lines=[]
        self.args=dict.fromkeys(args)
        self.name=name
    def add_line(self,line:str):
        self.lines.append(line[1:])
    def __call__(self,*args):
        from processor import run
        self.args=dict.fromkeys(list(self.args))
        args=dict(zip(self.args,args))
        self.args.update(args)
        prev=run.current_function
        run.current_function=self.name
        value=run('\n'.join(self.lines),silent=True)
        run.current_function=prev
        return value

class t__no_function__(tfunction):
    def add_line(self, line: str):
        raise NameError('No function defined!')

def tinput(text:str=''):
    return input(text)