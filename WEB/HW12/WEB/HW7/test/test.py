from cfonts import render, say

# Пример с использованием render
header = render("Меню", colors=["red", "yellow"], align="center", font="block")
print(header)

# Пример с использованием say
say("Меню", align="center", font="block", colors=["red", "yellow"])