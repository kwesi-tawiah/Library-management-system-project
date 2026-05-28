import re

text = "(show) I want to borrow (book)"
pattern = r"\(([^)]+)\)"

request = list(re.finditer(pattern, text, re.I))

one = request[0].group(1)

print(one)

text = "(name,sex,email,phone_number)"

pattern = r"(\d*[A-Za-z][A-Za-z_%&$?+]*\d*[@gmail.com]*)"
search = list(re.finditer(pattern, text, re.I))

for match in search:
    print(match.group(1))


tup = [(19)]



print(tup[0])

print(tup)