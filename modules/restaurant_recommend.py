import requests
from bs4 import BeautifulSoup
from uuid import uuid4


def set_where(self, update):
    return update.message.text + " "


def set_when(self, update):
    return update.message.text+" "


def set_howmany(self, update):
    return update.message.text


#다이닝 코드 크롤링
def get_restaurant(self, update, keyword):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
              'Content-Type': 'text/html; charset=UTF-8'}
    params = {'query': keyword}

    print("params" + str(keyword))

    # 응답 get 요청
    addr = 'http://www.diningcode.com/list.php'
    restaurants = requests.get(addr, headers=header, params=params).text
    soup = BeautifulSoup(restaurants, 'html.parser')

    restaurants_list = soup.select('ul#div_list li a span.btxt')
    menu_list = soup.select('ul#div_list li a span.stxt')
    rest_top_ten = '';
    title = restaurants_list[1:11]
    menu = menu_list[1:11]

    rest_top_ten += keyword + '결과입니다. \n'
    for i in range(10):
        rest_top_ten += title[i].text + ' (' + menu[i].text + ')' + '\n'

    update.message.reply_text(rest_top_ten)