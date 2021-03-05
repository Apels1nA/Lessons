date_info = {'day': '05', 'mounth': '03', 'year': '2021'}
data = {'group': 'B&W', 'id': '76235601492'}

filename = "{year}-{mounth}-{day} {group}-{id}.png".format(**date_info, **data)

print(filename)

number = [1, 2, 3]
fruits = ['apple', 'banana']

print(*number, *fruits)


def inf(*cort):
    print(*cort)

inf(1,2,3,4,5,6,7, 'dgfhjk')