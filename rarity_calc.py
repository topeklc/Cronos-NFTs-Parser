import csv
import ast


def read_file():
    with open("NFTs_data.csv", mode="r") as wac:
        reader = csv.reader(wac, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        my_lst = []
        for x in reader:
            for y in x:
                my_lst.append(ast.literal_eval(y))
    return my_lst


my_lst = read_file()
counter_dict = {}
dict_trait_points = {}
banned = ["ID", "image"]


for dic in my_lst:
    for trait in dic:
        if trait not in banned:
            counter_dict[trait] = []

print(counter_dict)

for dct in my_lst:
    for x in dct:
        if x not in banned:
            if {dct[x]: 0} not in counter_dict[x]:
                counter_dict[x].append({dct[x]: 0})

for dct in my_lst:
    for i in dct:
        if i not in banned:
            for x in counter_dict[i]:
                a = next(iter(x))
                if a in list(dct.values()):
                    x[a] += 1


print(counter_dict)