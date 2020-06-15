from urllib import request
import os
import sys
from urllib.parse import unquote, quote
from bs4 import BeautifulSoup

file_list = []
base_url = None


class Attachment(object):
    protocol = "http"
    base_url = None
    name = None
    display_name = None
    type = None

    def __init__(self, url: str, display_name: str = None):
        self.protocol = url.split("://")[0]
        self.base_url = '/'.join(url.replace(self.protocol + "://", "").split("/")[:-1]) + '/'

        f = url.split("/")[-1].split('.')
        self.name = '.'.join(f[:-1])
        self.type = f[-1]

        if display_name is not None:
            self.display_name = display_name

    def __repr__(self):
        return self.protocol + "://" + unquote(self.base_url + self.name + '.' + self.type)

    def show_name(self, depth, decode=True) -> str:
        name = "/".join(self.base_url.split("/")[-depth:]) + self.name + '.' + self.type

        return unquote(name) if decode is True else name

    @property
    def url(self) -> str:
        return self.protocol + "://" + quote(self.base_url + self.name + '.' + self.type)


def is_file(url: str) -> bool:
    return "." in url.split("/")[-1]


def check_protocol(url: str) -> bool:
    return "http://" in url or "https://" in url


def require_base_url() -> None:
    global base_url

    print("A 태그에 http(s) 가 포함된 URL이 설정되지 않은 것 같습니다. \nBASE URL을 입력하십시오: ")

    while True:

        input_base_url = input()
        if not check_protocol(input_base_url):
            print("http:// 또는 https:// 를 포함하여 입력 하십시오.: ")
            continue

        print("다운로드할 최종 URL은 {} 와 같이 설정될 것입니다. 해당 URL로 설정하시겠습니까? (y/n): ".format(input_base_url + "/aaa.txt"))
        if "y" in input():
            base_url = input_base_url
            break
        else:
            print("BASE URL을 입력하십시오: ")


if len(sys.argv) > 1 and check_protocol(sys.argv[1]):
    base_url = sys.argv[1]

print("HTML 텍스트를 입력하십시오. 다 입력하셨다면 <e> 를 입력하십시오.")
input_str = ""

while True:
    input_str += input()

    if "<e>" in input_str:
        input_str.replace("<e>", "")
        break

html_soup = BeautifulSoup(input_str, "html.parser")

for a in html_soup.find_all("a", href=True):

    if not is_file(a["href"]):
        print(a["href"] + " 는 파일이 아닌 것 같습니다.")
        continue

    if not check_protocol(a["href"]) and base_url is None:
        require_base_url()

    if not check_protocol(a["href"]):
        a["href"] = base_url + "/" + a["href"]

    current_file = Attachment(a["href"])
    file_list.append(current_file)

    print(current_file.show_name(1) + " 추가됨")

if not os.path.isdir("./downloads"):
    os.mkdir("./downloads")

for file in file_list:
    request.urlretrieve(file.url, "./downloads/" + file.show_name(1))
    print(file.show_name(1) + "를 다운로드 받았습니다.")
