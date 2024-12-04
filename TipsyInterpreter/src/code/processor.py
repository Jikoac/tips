import re
import random
from data import *

bracket_pattern = r'''\[(.*?)\]'''
curly_brace_pattern = r'\{(.*?)\}'

class run:
    silent=False
    last_code_block='__no_function__'
    current_function=None
    def __init__(self,text:str='',silent:bool|None=None,debug:bool=False):
        self.debug=debug
        silent=silent if silent!=None else self.silent
        self.text=text
        self.variables=variables
        self.variables.update({'__no_function__':tfunction()})
        self.constants=constants
        self.globals=globals
        self.text_og=text
        self.text=self.process(text,silent=silent)
    def process(tips,text:str,extra_variables:dict={},silent:bool|None=None):
        silent=silent if silent!=None else tips.silent
        bracket_pattern = r'''\[(.*?)\]'''
        curly_brace_pattern = r'\{(.*?)\}'

        
        tips.variables.update(extra_variables)

        # Split text into lines
        lines = text.split('\n')
        
        # Process each line
        processed_lines = []
        for line in lines:
            if line.startswith('#*'):
                tips.create_function(line)
            elif line.startswith('#'):
                tips.assign(line)
            elif line.startswith('?'):
                tips
            elif line.startswith('>'):
                tips.sort_line(line)
            else:
                processed_lines.append(line)
                if not silent:
                    print(tips.process_line(line))

        text = '\n'.join(processed_lines)

        brackets=re.findall(bracket_pattern,text)

        for item in brackets:
            text=text.replace(f'[{item}]',str(tips.from_brackets(item)))

        # Find all curly braces content
        curly_braces = re.findall(curly_brace_pattern, text)
        
        for item in curly_braces:
            text = text.replace(f'{{{item}}}', str(tips.from_braces(item)), 1)
        
        value=text

        return value
    def from_braces(tips,item):
            options = item.split(',')
            if options:
                replacement = random.choice(options).strip()
                return replacement
            return item
    def from_brackets(tips,item:str):
            args=item.split(',')
            item=args.pop(0)
            if item.startswith('*'):
                item=item[1:]
                raw=True
            else:
                raw=False
            if tips.current_function:
                if item in tips.variables[tips.current_function].args:
                    return tips.variables[tips.current_function].args[item]
            if not tips.debug:
                try:
                    if raw:
                        return tips.constants[item].raw(*args)
                    return tips.constants[item](*args)
                except:
                    try:
                        if raw:
                            return tips.variables[item].raw(*args)
                        return tips.variables[item](*args)
                    except:
                        try:
                            if raw:
                                return eval(item)
                            return eval(item)(*args)
                        except:
                            try:
                                return eval(item)
                            except:
                                return item
            else:
                if raw:
                    return tips.variables[item].raw(*args)
                return tips.variables[item](*args)
    def assign(tips,line:str):
                match_type = re.match(r'#\s*\[(.*?)\](.+?)=(.+)', line)
                match_in=re.match(r'#(.+?)<(.+)', line)
                match_func=re.match(r'#!(.+?)=(.+)', line)
                match = re.match(r'#(.+?)=(.+)', line)
                type=None
                is_arg=False
                if match:
                    if match_type:
                        type=types[match_type.group(1).strip()]
                        key=match_type.group(2).strip()
                    elif match_in:
                        key=match_in.group(2).strip()
                    elif match_func and tips.current_function:
                        key=match_func.group(1).strip()
                        is_arg=True
                    else:
                        key = match.group(1).strip()
                    if match_in:
                        value=input(tips.process(match_in.group(2)))
                    else:
                        value = [tips.process(value.strip(),tips.variables,silent=True) for value in match.group(2).split(',')]
                    if type==None:
                        if len(value)==1:
                            try:
                                float(value[0])
                                type=tnumber
                            except:
                                type=tstring
                        else:
                            type=trandom
                    if is_arg:
                        if tips.variables[tips.current_function].args[key]==None:
                            tips.variables[tips.current_function].args[key] = type([tips.process(val,silent=True) for val in value])
                    else:
                        tips.variables[key] = type([tips.process(val,silent=True) for val in value])
                else:
                    match=re.match(r'#(.+)',line)
                    match_type = re.match(r'#\s*\[(.*?)\](.+)', line)
                    if match_type:
                        type=types[match_type.group(1).strip()]
                        key=match_type.group(2)
                    else:
                        key=match.group(1)
                        type=tclass
                    tips.variables[key] = type()
    def __str__(self):
        return self.text
    def process_line(tips,text):
        
        brackets=re.findall(bracket_pattern,text)

        for item in brackets:
            text=text.replace(f'[{item}]',str(tips.from_brackets(item)))

        # Find all curly braces content
        curly_braces = re.findall(curly_brace_pattern, text)
        
        for item in curly_braces:
            text = text.replace(f'{{{item}}}', str(tips.from_braces(item)), 1)
        
        return text
    def create_function(tips,line):
        match_args = re.match(r'#\*(.+?)=(.+)', line)
        match = re.match(r'#\*(.+)', line)
        if match_args:
            name=match_args.group(1).strip()
            args=[arg.strip() for arg in match_args.group(2).split(',')]
            function=tfunction(name,args)
        else:
            name=match.group(1).strip()
            function=tfunction(name)
        tips.variables[name]=function
        tips.last_code_block=name
    def sort_line(tips,line):
        code=tips.last_code_block
        tips.variables[code].add_line(line)