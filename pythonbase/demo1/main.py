# 抓取百度贴吧图片

import requests
from bs4 import BeautifulSoup

url = "http://www.jjmeinv.com/s.asp?act=topic&keyword=%B8%A3%C0%FB%BC%A7"
headers = {
}

response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
imageList = soup.find_all("img")

offset = 0
for image in imageList:
    print(image.get("src"))
    image_content = requests.get(image.get("src")).content
    with open('./image/{}.jpg'.format(offset), 'wb') as file:
        file.write(image_content)
        offset = offset + 1
