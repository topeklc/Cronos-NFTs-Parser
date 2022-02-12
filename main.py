from bs4 import BeautifulSoup
import requests
import html
import csv
from time import sleep
# 0xf518f16f6611f0b7a51496cfcba2ed954ec81112
# 0x7D5f8F9560103E1ad958A6Ca43d49F954055340a
CONTRACT_ADDRESS = '0xf518f16f6611f0b7a51496cfcba2ed954ec81112'
pages = 1112


def get_data(page):
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
    print(ls)
    dic = {}
    correcter = len(ls) - 23
    for i, x in enumerate(ls):
        if i == 0:
            dic["ID"] = int(x[-1].split('#')[-1].replace("#", "").replace(" ", ""))
        elif i == 1:
            dic[x[0]] = "ipfs:" + x[2]
        elif i - correcter == 7:
            dic[ls[i + 1][1].strip()] = x[2].strip()
        elif i - correcter > 8:
            try:
                if i % 2 != 0:
                    dic[ls[i - correcter + 1][1].replace("]", "").strip()] = ls[i - correcter][1].strip()
            except IndexError as error:
                print(error)
                continue
    return dic


nfts_data = []


def main(pages):
    for page in range(pages):
        try:
            print(f"working on page {page}...")
            nfts_data.append(get_data(page))
        except Exception as e:
            print(e)
            print("Something goes wrong...")
        sleep(0.3)
    print(nfts_data)
    with open("NFTs_data.csv", mode="w") as data:
        writer = csv.writer(
            data, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(nfts_data)

main(pages)