import requests
from bs4 import BeautifulSoup
import re

def get_movie_chart(self, update):
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
              'Referer': 'https://movie.naver.com/movie/sdb/rank/rreserve.nhn'}
    addr = 'https://movie.naver.com/movie/sdb/rank/rreserve.nhn'
    self.addr = addr
    movies = requests.get(self.addr, headers=header).text
    soup = BeautifulSoup(movies, 'html.parser')

    movie_title = soup.select('.list_ranking tr .title a[href*=code]')
    movie_top_ten = ''

    for idx, movie in enumerate(movie_title, 1):
        title = movie.text
        link = movie['href']
        # link에서 정규표현식으로 song_id를 검색
        matched = re.search('(\d+)', link)
        if matched:
            movie_id = matched.group(1)
            movie_url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=' + movie_id
            movie_top_ten += str(idx) + '위 ' + title + '\n' + movie_url + '\n'

    update.message.reply_text(movie_top_ten)