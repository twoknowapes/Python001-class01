import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

BASE_URl = 'https://maoyan.com/films?showType=3'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
COOKIE = '''__mta=20796935.1593135622503.1593135733440.1593136644843.5; uuid_n_v=v1; uuid=FF228A80B74D11EAA2F937AFDFBC83F6F76F18CC1D274F578B50AD0775755615; _csrf=5ab0f18bc28652e2acc47491b537eb4c9094431b62743d23f21b24e86fcaa718; _lxsdk_cuid=172ee4868fec8-0ec1ff0cf77216-31627404-13c680-172ee4868ffc8; _lxsdk=FF228A80B74D11EAA2F937AFDFBC83F6F76F18CC1D274F578B50AD0775755615; mojo-uuid=af2fa3e5038aabf3e62743370c5191bd; mojo-session-id={"id":"fd843c9538fd03e1ff632d91984a6a06","time":1593153611316}; mojo-trace-id=1; __mta=20796935.1593135622503.1593136644843.1593153611754.6; _lxsdk_s=172ef58406d-ed7-3cf-7ac%7C%7C5'''
HEADERS = {'User-Agent': USER_AGENT,
           'Cookie': COOKIE}

response = requests.get(BASE_URl, headers=HEADERS)
bs_info = bs(response.text, 'html.parser')

movie_list = []
count = 0

for tags in bs_info.find_all('div', attrs={'class': 'movie-item film-channel'}):
    count += 1
    if count >= 10:
        break

    movie_title = tags.find('span', attrs={'class': 'name'}).text
    movie_tags = tags.find('span', attes={'class': 'hover-tag'})
    movie_type = movie_tags[0].next_sibling.strip()
    movie_time = movie_tags[2].next_sibling.strip()
    movie_list.append((movie_title, movie_type, movie_time))

if movie_list:
    movie_data = pd.DataFrame(data=movie_list)
    movie_data.to_csv('movie_data.to_csv', encoding='utf-8')
