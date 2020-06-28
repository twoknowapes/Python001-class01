import requests

REFERER = 'https://shimo.im/login?from=home'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
LOGIN_URL = 'https://shimo.im/login?from=home'

HEADERS = {
    'Referer': REFERER,
    'User-Agent': USER_AGENT
}

form_data = {
    'mobile': '+8618456071819',
    'password': 'shimo@2020'
}

s = requests.Session()
response = s.post(LOGIN_URL, data=form_data, headers=HEADERS)
print(response.text)
