import csv
import ast


def read_file() -> list:
    """
    Reads csv file created by main.py.
    Returns:
        List of dictionaries with NFTs data.

    """
    with open("NFTs_data.csv", mode="r") as wac:
        reader = csv.reader(
            wac, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        lst = []
        for x in reader:
            for y in x:
                lst.append(ast.literal_eval(y))
    return lst


my_lst = read_file()
counter_dict = {}
dict_trait_points = {}
sum_traits_dict = {}
percent_traits_dict = {}
id_points_dict = {}
banned = ["ID", "image"]


def calculate_percent_of_occurrence():
    """Calculates the percentage of occurrence of a specific trait"""
    # make empty list in counter_dict value
    for dic in my_lst:
        for trait in dic:
            if trait not in banned:
                counter_dict[trait] = []
    # append list in counter_dict values by specific trait dictionary and set value to 0
    for dct in my_lst:
        for x in dct:
            if x not in banned:
                if {dct[x]: 0} not in counter_dict[x]:
                    counter_dict[x].append({dct[x]: 0})
    # increment specific trait dictionary in counter_dict if occurs
    for dct in my_lst:
        for i in counter_dict:
            if i not in banned:
                for x in counter_dict[i]:
                    a = next(iter(x))
                    if a in list(dct.values()):
                        x[a] += 1
    # set values percent_traits_dict
    for i in counter_dict:
        sum_traits_dict[i] = 0
        for x in counter_dict[i]:
            sum_traits_dict[i] += next(iter(x.values()))
        for y in counter_dict[i]:
            sum_traits_dict[next(iter(y.keys()))] = 0
            percent_traits_dict[next(iter(y.keys()))] = 100 / (
                sum_traits_dict[i] / next(iter(y.values()))
            )


def calculate_points():
    """Calculates total points for each NFT"""
    # calculate sum of points (100 - occurrence percent)
    for i in my_lst:
        id_points_dict[i["ID"]] = 0
        for x in i:
            if x not in banned:
                id_points_dict[i["ID"]] += 100 - percent_traits_dict[i[x]]


def main() -> dict:
    """
    Runs all functions and sorts results.
    Returns:
        Sorted dictionary with results
    """
    read_file()
    calculate_percent_of_occurrence()
    calculate_points()
    sorted_points_dict = {
        k: v for k, v in sorted(id_points_dict.items(), key=lambda item: item[1])
    }
    return sorted_points_dict


print(main())
