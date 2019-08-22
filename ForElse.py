items = [2, 25, 9]
divisor = 21

for item in items:
    if item % divisor == 0:
        found = item
        break
else:
    items.append(divisor)
    found = divisor

print(locals())
print("{items} contains {found} which is a multiple of {divisor}"
      .format(**locals()))

'''
def ensure_has_divisible(items, divisor):
    for item in items:
        if item % divisor == 0:
            return item
    items.append(divisor)
    return divisor
'''

