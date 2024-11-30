import re
import random
from data import *

# def process(text:str,extra_generators:dict={},return_type:type=str):
#     # Define regex patterns for brackets and curly braces
#     bracket_pattern = r'''\[(.*?)\]'''
#     curly_brace_pattern = r'\{(.*?)\}'

    
#     generators = extra_generators

#     # Split text into lines
#     lines = text.split('\n')
    
#     # Process each line
#     processed_lines = []
#     for line in lines:
#         if line.startswith('#'):
#             match = re.match(r'#(.+?)=(.+)', line)
#             if match:
#                 key = match.group(1).strip()
#                 value = [process(value.strip(),generators) for value in match.group(2).split(',')]
#                 generators[key] = trandom(value)
#         else:
#             processed_lines.append(line)

#     text = '\n'.join(processed_lines)

#     brackets=re.findall(bracket_pattern,text)

#     for item in brackets:
#         try:
#             text=text.replace(f'[{item}]',random.choice(generators[item]))
#         except KeyError:
#             text=text.replace(f'[{item}]',eval(item)())
#         except:
#             None

#     # Find all curly braces content
#     curly_braces = re.findall(curly_brace_pattern, text)
    
#     for item in curly_braces:
#         options = item.split(',')
#         if options:
#             replacement = random.choice(options).strip()
#             text = text.replace(f'{{{item}}}', replacement, 1)

#     class gen:
#         def __init__(self,text,gen):
#             self.text=text
#             self.gen=gen
#         def __str__(self):
#             return self.text
#         def __gen__(self):
#             return self.gen
    
#     value=gen(text,generators)

#     return return_type(value)

# def gen(value):
#     return value.__gen__()


bracket_pattern = r'''\[(.*?)\]'''
curly_brace_pattern = r'\{(.*?)\}'

class run:
    silent=False
    def __init__(self,text:str=''):
        self.text=text
        self.variables=variables
        self.constants=constants
        self.globals=globals
        self.text_og=text
        self.text=self.process(text)
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
            if line.startswith('#'):
                tips.assign(line)
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
    def assign(tips,line:str):
                match_type = re.match(r'#\s*\[(.*?)\](.+?)=(.+)', line)
                match = re.match(r'#(.+?)=(.+)', line)
                type=None
                if match:
                    if match_type:
                        type=types[match_type.group(1).strip()]
                        key=match_type.group(2).strip()
                    else:
                        key = match.group(1).strip()
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