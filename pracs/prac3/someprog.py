import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF_TASK3 = '''
E = bytes
bytes = byte | byte bytes
byte = 0 | 1
'''

BNF_TASK4 = '''
E = brackets
brackets = curly_brackets | parentheses
curly_brackets = { brackets } | {}
parentheses = ( brackets ) | ()
'''

BNF_TASK5 = '''
E = expr
var = x | y
val = var | ( expr )
expr = ~ val | val & val | val + val
'''

BNF = BNF_TASK5

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
