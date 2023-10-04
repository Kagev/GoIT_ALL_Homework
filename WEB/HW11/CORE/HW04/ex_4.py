# Реалізувати функція, яка буде приймати оператор і дві цифри і буде виконувати операцію.
# Реалізувати це через dict

def if_elif_vs_dict(operator, operand_1, operand_2):
    return {
        'add': lambda: operand_1 + operand_2,
        'sub': lambda: operand_1 - operand_2,
        'mul': lambda: operand_1 * operand_2,
        'div': lambda: operand_1 / operand_2,
    }.get(operator, lambda: 'Not valid operation')()

print(if_elif_vs_dict('add', 5, 4))
print(if_elif_vs_dict('sub', 5, 4))
print(if_elif_vs_dict('mul', 5, 4))
print(if_elif_vs_dict('div', 5, 4))
print(if_elif_vs_dict('/', 5, 3))