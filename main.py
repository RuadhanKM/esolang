#
#   Each token is seperated by a space
#   Call a function with func *( param-a , param-b )*
#

import sys
import built_in_func as bif

if (len(sys.argv) == 1):
    print('Unknown command!')
    print('Do "main.py help" to get help')
    exit()
if (sys.argv[1].lower() == 'help'):
    print('Run script:  main.py [file-name.es]')
    print('Help:        main.py help')
    exit()
    
memory = {}
split_key = "^"

memory['cmdl_args'] = {'type': 'str', 'value': " ".join(sys.argv[2:])}

in_func_define = False
cur_func_define = None

func_depth = 0

debugging = False

with open('scripts/' + sys.argv[1], 'r') as f:
    script = "".join(['' if i[:2] == "//" else i for i in f.readlines()]).replace('\n', '').replace(' ', '').replace('\s', ' ').replace('\t', '').strip()
    # ik its a long line but all it does it strip the script of newlines, spaces, and comments

commands = script.split(";")[:-1]

def get_var(name):
    global memory
    
    v = name
    
    if (name in memory.keys()):
        v = memory[name]['value']
    
    return v

def run_command(command, parsed_command):
    global memory, in_func_define, cur_func_define, split_key, debugging, func_depth

    command_prefix = parsed_command[0]
    
    if debugging:
        if type(command) == str:
            print('  ' * func_depth + command)
        if type(command) == list:
            print('  ' * func_depth + "^".join(command))
    
    if command_prefix == "end":
        func_depth -= 1
    
        in_func_define = False
        cur_func = None
        return
    if in_func_define:
        memory[cur_func_define]['value']['commands'].append(parsed_command)
        return
    
    if command_prefix == "pm":
        print("\n-- MEMORY --\n")
        print("Memory Size:")
        print("\t" + str(sys.getsizeof(memory)) + " b")
        print("\t" + str(len(memory.keys())) + " vars")
        print("\nRaw Memory:")
        for i in memory.keys():
            print('\t{:>20}  {:>10}  {:>10}'.format(i, ':', (memory[i]["value"] if memory[i]["type"] != "func" else 'func')))
        print("\n-- MEMORY --\n")
        
        return
    elif command_prefix == "sk":
        split_key = parsed_command[1]
        return
    elif command_prefix == "debug":
        debugging = not debugging
    elif command_prefix == "estr":
        var_name = parsed_command[1]

        memory[var_name] = {'type': 'str', 'value': ''}
        return
    elif command_prefix == "eint":
        var_name = parsed_command[1]

        memory[var_name] = {'type': 'int', 'value': 0}
        return
    elif command_prefix == "earr":
        var_name = parsed_command[1]

        memory[var_name] = {'type': 'int', 'value': []}
        return
    elif command_prefix == "ebool":
        var_name = parsed_command[1]

        memory[var_name] = {'type': 'int', 'value': False}
        return
    elif command_prefix == "var":
        value = get_var(parsed_command[3])
        var_type = parsed_command[2]
        var_name = parsed_command[1]
        
        if var_type == 'int':
            memory[var_name] = {'type': var_type, 'value': int(value)}
            return
        if var_type == 'str':
            memory[var_name] = {'type': var_type, 'value': value}
            return
        if var_type == 'arr':
            memory[var_name] = {'type': var_type, 'value': [get_var(i) for i in parsed_command[3:]]}
            return
        if var_type == 'bool':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            else:
                print(f'Invalid value for type bool "{value}"')
                exit()
        
            memory[var_name] = {'type': var_type, 'value': value}
            return
    elif command_prefix == "+":
        a = memory[parsed_command[1]]
        b = get_var(parsed_command[2])
        
        if a['type'] == 'int':
            a['value'] = a['value'] + int(b)
        if a['type'] == 'str' or a['type'] == 'arr':
            a['value'] = a['value'] + b
        
        return
    elif command_prefix == "-":
        memory[parsed_command[1]]['value'] = memory[parsed_command[1]]['value'] - int(get_var(parsed_command[2]))
        return
    elif command_prefix == "*":
        memory[parsed_command[1]]['value'] = memory[parsed_command[1]]['value'] * int(get_var(parsed_command[2]))
        return
    elif command_prefix == "/":
        memory[parsed_command[1]]['value'] = memory[parsed_command[1]]['value'] / int(get_var(parsed_command[2]))
        return
    elif command_prefix == "%":
        memory[parsed_command[1]]['value'] = memory[parsed_command[1]]['value'] % int(get_var(parsed_command[2]))
        return
    elif command_prefix == "match":
        a = get_var(parsed_command[2])
        b = get_var(parsed_command[3])
        
        if a == b:
            match_command = parsed_command[1] + '^' + str(a)
            match_parsed_command = match_command.split(split_key)
            
            func_depth += 1
            run_command(match_command, match_parsed_command)
            func_depth -= 1
    elif command_prefix == "==":
        a = get_var(parsed_command[2])
        b = get_var(parsed_command[3])
        
        memory[parsed_command[1]]['value'] = a == b
    elif command_prefix == "<":
        a = int(get_var(parsed_command[2]))
        b = int(get_var(parsed_command[3]))
        
        memory[parsed_command[1]]['value'] = a < b
    elif command_prefix == ">":
        a = int(get_var(parsed_command[2]))
        b = int(get_var(parsed_command[3]))
        
        memory[parsed_command[1]]['value'] = a > b
    elif command_prefix == "<=":
        a = int(get_var(parsed_command[2]))
        b = int(get_var(parsed_command[3]))
        
        memory[parsed_command[1]]['value'] = a <= b
    elif command_prefix == ">=":
        a = int(get_var(parsed_command[2]))
        b = int(get_var(parsed_command[3]))
        
        memory[parsed_command[1]]['value'] = a >= b
    elif command_prefix == "if":
        if get_var(parsed_command[2]):
            if_command = parsed_command[1]
            if_parsed_command = if_command.split(split_key)
            
            func_depth += 1
            run_command(if_command, if_parsed_command)
            func_depth -= 1
    elif command_prefix == "while":
        while get_var(parsed_command[2]):
            while_command = parsed_command[1]
            while_parsed_command = while_command.split(split_key)
            
            func_depth += 1
            run_command(while_command, while_parsed_command)
            func_depth -= 1
    elif command_prefix == "func":
        func_depth += 1
    
        func = {
            'type': 'func',
            'value': {
                'params': parsed_command[2:],
                'commands': []
            }
        }
        
        in_func_define = True
        cur_func_define = parsed_command[1]
        
        memory[parsed_command[1]] = func
        
        return
    elif command_prefix == "for":
        iters = get_var(parsed_command[1])
        
        func_depth += 1
        
        for i in range(int(iters)):
            for_command = parsed_command[2] + '^' + str(i)
            for_parsed_command = for_command.split(split_key)
            
            run_command(for_command, for_parsed_command)
        
        func_depth -= 1
    elif command_prefix == "foreach":
        string = get_var(parsed_command[1])
        
        func_depth += 1
        
        for i in string:
            for_command = parsed_command[2] + '^' + str(i)
            for_parsed_command = for_command.split(split_key)
            
            run_command(for_command, for_parsed_command)
        
        func_depth -= 1
    elif command_prefix in bif.funcs.keys():
        meta = {}
        meta['memory'] = memory
        meta['args'] = parsed_command[1:]
        meta['run_command'] = run_command
        meta['split_key'] = split_key
        meta['func_depth'] = func_depth
    
        bif.funcs[command_prefix](meta)
    elif command_prefix in memory:
        if memory[command_prefix]['type'] == 'func':
            func_depth += 1
            
            func = memory[command_prefix]
            
            func_commands = func['value']['commands']
            func_params = func['value']['params']
            parsed_func_commands = []
            
            for func_command in func_commands:
                parsed_func_commands.append([])
                
                for token in func_command:
                    fin_token = token
                    
                    for param_index, func_param in enumerate(func_params):
                        if token == func_param:
                            if parsed_command[param_index+1] in memory.keys():
                                fin_token = str(memory[parsed_command[param_index+1]]['value'])
                            else:
                                fin_token = parsed_command[param_index+1]
                    parsed_func_commands[-1].append(fin_token)
            
            for i in range(len(func_commands)):
                run_command(func_commands[i], parsed_func_commands[i])
            
            func_depth -= 1

for command_index, command in enumerate(commands):
    parsed_command = command.split(split_key)
    run_command(command, parsed_command)