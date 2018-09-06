from bs4 import BeautifulSoup
import requests

def get_music_chart(self, update):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    addr = 'https://www.melon.com/chart/index.htm'
    self.addr = addr
    melon = requests.get(self.addr, headers = header)
    soup = BeautifulSoup(melon.text, 'html.parser')

    titles = soup.select('#lst50 > td > div > div > div.ellipsis.rank01 > span > a')
    artist = soup.select('#lst50 > td > div > div > div.ellipsis.rank02 > span')
    update.message.reply_text('실시간 멜론 차트\n'
                              + '1위: ' + titles[1].text + " - " + artist[1].text + '\n'
                              + '2위: ' + titles[2].text + " - " + artist[2].text + '\n'
                              + '3위: ' + titles[3].text + " - " + artist[3].text + '\n'
                              + '4위: ' + titles[4].text + " - " + artist[4].text + '\n'
                              + '5위: ' + titles[5].text + " - " + artist[5].text + '\n'
                              + '6위: ' + titles[6].text + " - " + artist[6].text + '\n'
                              + '7위: ' + titles[7].text + " - " + artist[7].text + '\n'
                              + '8위: ' + titles[8].text + " - " + artist[8].text + '\n'
                              + '9위: ' + titles[9].text + " - " + artist[9].text + '\n'
                              + '10위: ' + titles[10].text + " - " + artist[10].text + '\n'
                              )
