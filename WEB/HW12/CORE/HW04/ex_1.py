# У нас є строка: "lsj94ksd231 9". Потрібно вибрати тільки цифри
s = 'lsj94ksd231 9'
result = []
for i in s:
    if i.isdigit():
        result.append(i)

print(result)