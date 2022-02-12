import csv
import ast

with open("NFTs_data.csv", mode="r") as wac:
    reader = csv.reader(wac, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    my_lst = []

    for x in reader:
        print(x)
        for y in x:
            print(y)
            my_lst.append(ast.literal_eval(y))

counter_dict = {}
dict_trait_points = {}
banned = ["ID", "image"]
for dct in my_lst:
    for x in dct:
        if x not in banned:
            counter_dict[dct[x]] = 0

for dct in my_lst:
    for y in dct:
        if y not in banned:
            dict_trait_points[dct[y]] = 0


for dct in my_lst:
    for i in dct:
        if i not in banned:
            counter_dict[dct[i]] += 1

print(counter_dict)

sorted_dct = {k: v for k, v in sorted(counter_dict.items(), key=lambda item: item[1])}

print(sorted_dct)


total = len(sorted_dct)


def occurrences_to_points(occurrences):
    points = total - occurrences
    return points


for k in sorted_dct:
    dict_trait_points[k] = occurrences_to_points(sorted_dct[k])

# print(dict_trait_points)
traits = dict_trait_points.keys()

id_points_dict = {}


for item in my_lst:
    id_points_dict[item["ID"]] = 0
    ape_traits = [i for i in item.values()]
    for trait in traits:
        # print(trait)
        if trait in ape_traits:
            id_points_dict[item["ID"]] += dict_trait_points[trait]

sorted_points_dict = {
    k: v for k, v in sorted(id_points_dict.items(), key=lambda item: item[1])
}

print(sorted_points_dict)