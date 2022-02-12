from bs4 import BeautifulSoup
import requests
import html
import csv
from time import sleep

CONTRACT_ADDRESS = "0x89dBC8Bd9a6037Cbd6EC66C4bF4189c9747B1C56"
PAGES = 5


def get_trait_lst(lst: list) -> list:
    """
    Shortens the list to one that only contains traits.
    Args:
        lst: List of all metadata.

    Returns:
        List that contains only traits.
    """
    pointer = 0
    for i, item in enumerate(lst):
        if item[0].startswith("attributes"):
            pointer = i
            break
    trait_lst = lst[pointer:]
    return trait_lst


def get_data(page: int) -> dict:
    """
    Parse data for given contract address and page.
    Args:
        page: Page number passed as integer.

    Returns:
        Dictionary ready to save to a file.

    """
    html_code = requests.get(
        f"https://cronos.crypto.org/explorer/token/{CONTRACT_ADDRESS}/instance/{page}/metadata"
    )
    html_code = html.unescape(html_code.text)
    soup = BeautifulSoup(html_code, "html.parser")
    res = (
        soup.find("code")
        .text.replace("\n", "")
        .replace("{", "")
        .replace("}", "")
        .replace('"', "")
        .split(",")
    )
    ls = [x.lstrip().split(":") for x in res]
    dic = {}
    for i, x in enumerate(ls):
        if i == 0:
            dic["ID"] = int(x[-1].split("#")[-1].replace("#", "").replace(" ", ""))
        elif i == 1:
            dic[x[0]] = "ipfs:" + x[2]
    trait_lst = get_trait_lst(ls)
    for i, attr in enumerate(trait_lst):
        if i == 0:
            dic[trait_lst[i + 1][1].strip()] = attr[2].strip()
        elif i % 2 == 0:
            dic[trait_lst[i + 1][1].replace("]", "").strip()] = trait_lst[i][1].strip()
    return dic


def main():
    """Runs above functions and write result to a file."""
    nfts_data = []
    for page in range(1, PAGES):
        try:
            print(f"working on page {page}...")
            nfts_data.append(get_data(page))
        except Exception as e:
            print(e)
            print("Something went wrong...")
        sleep(0.3)
    print(nfts_data)
    with open("NFTs_data.csv", mode="w") as data:
        writer = csv.writer(
            data, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(nfts_data)


main()
