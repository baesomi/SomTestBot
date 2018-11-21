from bs4 import BeautifulSoup
import requests
import re


def get_music_chart(self, update):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    addr = 'https://www.melon.com/chart/index.htm'
    self.addr = addr
    melon = requests.get(self.addr, headers = header)
    soup = BeautifulSoup(melon.text, 'html.parser')

    song_list_title = soup.select('#tb_list tr .wrap_song_info a[href*=playSong]')
    melon_top_ten = '';
    top_ten = song_list_title[0:10]
    for idx,song in enumerate(top_ten,1):
        title = song.text
        link = song['href']
        # link에서 정규표현식으로 song_id를 검색
        matched = re.search(r'(\d+)\);' ,link)
        if matched:
            song_id = matched.group(1)
            song_url = 'https://www.melon.com/song/detail.htm?songId=' + song_id
            melon_top_ten += str(idx) + '위 ' + title + '\n' +song_url + '\n'

    update.message.reply_text(melon_top_ten)