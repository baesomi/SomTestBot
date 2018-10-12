import requests
from bs4 import BeautifulSoup


def get_search_rank(self, update):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://datalab.naver.com/keyword/realtimeList.naver'}
    addr = 'https://datalab.naver.com/keyword/realtimeList.naver'
    self.addr = addr
    result = requests.get(self.addr, headers=header).text
    soup = BeautifulSoup(result, 'html.parser')

    keywords_list = soup.select_one('div.keyword_rank')
    keywords = keywords_list.select('li.list span.title')
    keyword_top_ten = ''

    for idx, keyword in enumerate(keywords[:10],1):
        title = keyword.text
        search_url = "https://search.naver.com/search.naver?where=nexearch&query=" + title + "&sm=top_lve&ie=utf8"
        keyword_top_ten += str(idx) + '위 ' + title + '\n' + search_url + '\n'

    update.message.reply_text(keyword_top_ten)