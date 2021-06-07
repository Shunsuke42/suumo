from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint

url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=050&bs=040&ta=23&sc=23105&cb=0.0&ct=9999999&et=9999999&md=01&md=02&md=03&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1?page=%7B%7D?page=1&page={}'
d_list = []

for i in range(1,62):
    target_url = url.format(i)
    print(target_url)

    r = requests.get(target_url)

    sleep(1)

    soup = BeautifulSoup(r.text,'html.parser')

    contents = soup.find_all('div',class_='cassetteitem')

    for content in contents:
        detail = content.find('div',class_='cassetteitem-detail')
        table = content.find('table',class_='cassetteitem_other')
        title = detail.find('div',class_='cassetteitem_content-title')
        address = detail.find('li',class_='cassetteitem_detail-col1')
        age = detail.find('li',class_='cassetteitem_detail-col3')
        age1 = age.find_all('div')[0]

        tr_tags = table.find_all('tr',class_='js-cassette_link')
        tr_tag = tr_tags[0]

        floor,price,first_fee,capasity = tr_tag.find_all('td')[2:6]
        fee,management_fee = price.find_all('li')
        deposit,gratuity = first_fee.find_all('li')
        madori,menseki = capasity.find_all('li')

        #title:物件名
        #address:住所
        #age:築年数
        #floor:階数
        #fee:賃料
        #management_fee:管理費
        #deposit:敷金
        #gratuity:礼金
        #madori:間取り
        #menseki:面積

        d = {
            'title':title.text,
            'address':address.text,
            'age':age1.text,
            'floor':floor.text,
            'fee':fee.text,
            'management_fee':management_fee.text,
            'deposit':deposit.text,
            'gratuity':gratuity.text,
            'madori':madori.text,
            'menseki':menseki.text
        }

        d_list.append(d)

df = pd.DataFrame(d_list)
df.head()

#print(df.shape)

#print(len(df.title.unique()))

df.to_csv('test.csv',index=None,encoding='utf=8=sig')
#pprint(df.head)
