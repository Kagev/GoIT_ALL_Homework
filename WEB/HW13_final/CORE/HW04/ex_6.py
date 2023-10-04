# Валідація дужок
# ({)}
# (((}}}
def is_balanced(input_string):
    opens = '([{'
    closes = ')]}'
    stack = []

    for symbol_position, symbol in enumerate(input_string):
        if symbol in opens:
            stack.append((symbol_position, symbol))
        elif symbol in closes:
            position = closes.index(symbol)
            if stack and opens[position] == stack[-1][1]:
                stack.pop()
            else:
                return False
    if stack:
        return False
    else:
        return True


print(is_balanced('(){[(())]}'))
