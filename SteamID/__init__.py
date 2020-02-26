# l = list(range(235))
# x=[l[i:i+100] for i in range(0, 235, 100)]
# print(x)

a = [[{'t': "t"}, {'t': "s"}],[{'t': "q"}, {'t': "z"}]]
z = {'a': {'b': [{'q': 1}, {'q': 2}, {'q': 3}, {'q': 4}]}}
b = [y for x in a for y in x]
for v, q in enumerate(b):
    z['a']['b'][v]['z'] = q
print(z)