# Заповнити список числами які кратні 30 або 31

# 30 ... 255
res = []
for item in range(30, 256):
    if item % 30 == 0 or item % 31 == 0:
        res.append(item)

print(res)