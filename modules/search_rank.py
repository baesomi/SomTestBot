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

    keywords = soup.select('div.keyword_rank.select_date span.title')
    keyword_top_ten = ''

    for idx, keyword in enumerate(keywords[:10],1):
        title = keyword.text
        keyword_top_ten += str(idx) + '위 ' + title + '\n'


    update.message.reply_text(keyword_top_ten)