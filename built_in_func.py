import sys

def get_var(memory, name):
    v = name
    
    if (name in memory.keys()):
        v = memory[name]['value']
    
    return v

def eso_print(meta):
    memory = meta['memory']
    args = meta['args']

    print(get_var(memory, args[0]))


def eso_putconsole(meta):
    memory = meta['memory']
    args = meta['args']

    sys.stdout.write(get_var(memory, args[0]))
    sys.stdout.flush()


def eso_file(meta):
    memory = meta['memory']
    args = meta['args']

    with open('scripts/'+get_var(memory, args[0]), 'r') as f:
        text = ''.join(f.readlines())
        memory[args[1]]['value'] = text


def eso_input(meta):
    memory = meta['memory']
    args = meta['args']
    
    i = input(get_var(memory, args[0]))
    memory[args[1]]['value'] = i


def eso_parseint(meta):
    memory = meta['memory']
    args = meta['args']

    memory[args[0]]['value'] = int(memory[args[0]]['value'])
    memory[args[0]]['type'] = 'int'


def eso_slice(meta):
    memory = meta['memory']
    args = meta['args']

    if (len(args)) == 3:
        memory[args[0]]['value'] = get_var(memory, args[1])[int(get_var(memory, args[2]))]
    if (len(args)) == 4:
        memory[args[0]]['value'] = get_var(memory, args[1])[int(get_var(memory, args[2])) : int(get_var(memory, args[3]))]

def eso_setslice(meta):
    memory = meta['memory']
    args = meta['args']
    
    ls = memory[args[0]]['value']
    otype = type(ls)
    ls = list(ls)
    
    ls[int(get_var(memory, args[1]))] = get_var(memory, args[2])
    
    if otype == str:
        memory[args[0]]['value'] = "".join(ls)
    if otype == list:
        memory[args[0]]['value'] = ls


def eso_sliceleft(meta):
    memory = meta['memory']
    args = meta['args']

    memory[args[0]]['value'] = get_var(memory, args[1])[int(get_var(memory, args[2])):]


def eso_sliceright(meta):
    memory = meta['memory']
    args = meta['args']

    memory[args[0]]['value'] = get_var(memory, args[1])[:int(get_var(memory, args[2]))]

def eso_append(meta):
    memory = meta['memory']
    args = meta['args']
    
    memory[args[0]]['value'].append(get_var(memory, args[1]))
    
def eso_pop(meta):
    memory = meta['memory']
    args = meta['args']
    
    if len(args) == 2:
        memory[args[1]]['value'] = memory[args[0]]['value'].pop()
    if len(args) == 3:
        memory[args[1]]['value'] = memory[args[0]]['value'].pop(get_var(memory, args[2]))


def eso_len(meta):
    memory = meta['memory']
    args = meta['args']

    memory[args[0]]['value'] = len(get_var(memory, args[1]))
    

def eso_char(meta):
    memory = meta['memory']
    args = meta['args']
    
    memory[args[0]]['value'] = chr(int(get_var(memory, args[1])))


def eso_ord(meta):
    memory = meta['memory']
    args = meta['args']
    
    memory[args[0]]['value'] = ord(str(get_var(memory, args[1])))

funcs = {
    'print': eso_print,
    'putconsole': eso_putconsole,
    'file': eso_file,
    'input': eso_input,
    'parseint': eso_parseint,
    'slice': eso_slice,
    'sliceleft': eso_sliceleft,
    'sliceright': eso_sliceright,
    'setslice': eso_setslice,
    'append': eso_append,
    'pop': eso_pop,
    'len': eso_len,
    'char': eso_char,
    'ord': eso_ord,
}