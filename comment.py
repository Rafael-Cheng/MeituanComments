import sys
import time
import json
import random
import requests
import telnetlib
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def getStore(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    response = requests.get(url, headers=headers)
    cookies = response.cookies
    page = response.text
    json_obj = json.loads(page)
    for i in range(30):
        bname = json_obj['data'][i]['brandname']
        bid = json_obj['data'][i]['id']
        getComment(bname, bid, headers, cookies)
        print 'bid: ' + str(bid)

def getComment(bname, bid, headers, cookies):
    offset = 0
    url = 'http://www.meituan.com/deal/feedbacklist/' + str(bid) + '/all/all/0/default/50?limit=10&showpoititle=1&offset=0' 
    total = json.loads(requests.get(url, headers=headers,\
            cookies=cookies).text)['data']['total']
    print 'total: ' + str(total)
    if total == 0:
        return
    with open(str(bid), 'a') as f:
        f.write(bname)
        f.write('\n\n')
    while offset <= total:
        url = 'http://www.meituan.com/deal/feedbacklist/' + str(bid) \
                + '/all/all/0/default/50?limit=10&showpoititle=1&offset=' + str(offset)
        page = requests.get(url, headers=headers, cookies=cookies)
        json_obj = json.loads(page.text)
        comments = json_obj['data']['ratelistHtml']
        soup = BeautifulSoup(comments, 'lxml')
        lists = soup.find_all(class_='J-ratelist-item rate-list__item cf')
        for li in lists:
            name = li.find(class_='name').text
            comment = li.find(class_='content').text.strip()
            with open(str(bid), 'a') as f:
                f.write(name)
                f.write('\n')
                f.write(comment)
                f.write('\n\n')
        offset += 10
        stime = random.randint(10, 15)
        time.sleep(stime)

if __name__ == '__main__':
    count = 0
    preurl = 'http://lvyou.meituan.com/volga/api/v1/trip/deal/select/city/50?cateId=226&utm_medium=pc&client=pc&uuid=1d4d560d0a5bf0f14268.1488681429.0.0.0&fromCityId=50&fromCityName=%E6%9D%AD%E5%B7%9E&sort=defaults&offset='
    posturl = '&limit=30'
    while count < 420:
        curl = preurl + str(count) + posturl
        getStore(curl)
        count += 30
