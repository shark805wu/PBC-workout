import requests
from bs4 import BeautifulSoup 
import re
import urllib3
import time
import random
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


'''
url = 'https://foodtracer.taipei.gov.tw/Front/Breakfast'
a = requests.get(url, verify=False)
print(a.text)
# print('======', BeautifulSoup(requests.get(url, verify=False).text, 'html.pareser'), '======')


'''
# 進到摩斯
url = 'https://foodtracer.taipei.gov.tw/Front/Breakfast/Product?id=23928945'
# 先爬目前類別


# 速食
# '''
calories_dic = {}
with open('brand.csv', newline='') as csvfile:
    csv = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in csv:
        print(count)
        time.sleep(3)
        if count == 12:
            break
        store_name = row[0]
        store_url = row[1]
        calories_dic[store_name] = {}
        product_url_list = []
        store_r = requests.get(store_url, verify=False)
        store_soup = BeautifulSoup(store_r.text, 'html.parser')
        sub_url_list = []
        for product_tag in store_soup.find('div', id='mygallery').find_all('div', class_='panel'):
            sub_url_list.append(product_tag.a['href']) # sub_url_list: 某個子類別
        for sub_url in sub_url_list: # 開始找產品
            sub_url = 'https://foodtracer.taipei.gov.tw' + sub_url
            sub_r = requests.get(sub_url, verify=False)
            sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
            for product_tag in sub_soup.find_all('div', class_='product'):
                product_url_list.append(product_tag.a['href'])

        # 以下大類別不同（速食/冰...）要改
        for product_url in product_url_list:
            product_url = 'https://foodtracer.taipei.gov.tw' + product_url
            product_r = requests.get(product_url, verify=False)
            product_soup = BeautifulSoup(product_r.text, 'html.parser')
            product_name = product_soup.find('div', class_='crack').a.next_sibling.strip('\n \r /') # 品名
            product_calories = product_soup.find('th', string='熱量(卡)').parent.next_sibling.next_sibling.contents[3].text
            calories_dic[store_name][product_name] = float(product_calories)

        count += 1
print(calories_dic)
# '''

'''
速食熱量數字：soup.find('th', string='熱量(卡)').parent.next_sibling.next_sibling.contents[1]
'''




# 飲冰品
'''
strip = 'kcal大卡約'
calories_dic = {}
with open('brand.csv', newline='') as csvfile:
    csv = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in csv:
        count += 1
        if count < 14:
            continue
        print(count)
        time.sleep(3)
        # if count == 90:
        #     break
        store_name = row[0]
        store_url = row[1]
        product_url_list = []
        store_r = requests.get(store_url, verify=False)
        store_soup = BeautifulSoup(store_r.text, 'html.parser')
        sub_url_list = []
        for product_tag in store_soup.find('div', id='mygallery').find_all('div', class_='panel'):
            sub_url_list.append(product_tag.a['href']) # sub_url_list: 某個子類別
        for sub_url in sub_url_list: # 開始找產品
            sub_url = 'https://foodtracer.taipei.gov.tw' + sub_url
            sub_r = requests.get(sub_url, verify=False)
            sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
            for product_tag in sub_soup.find_all('div', class_='product'):
                product_url_list.append(product_tag.a['href'])

        # 以下大類別不同（速食/冰...）要改
    product_count = 0
    for product_url in product_url_list:
        product_url = 'https://foodtracer.taipei.gov.tw' + product_url
        product_r = requests.get(product_url, verify=False)
        product_soup = BeautifulSoup(product_r.text, 'html.parser')
        store_name = product_soup.find('div', class_='storeName').text
        if store_name not in calories_dic:
            calories_dic[store_name] = {}
        product_name = product_soup.find('div', class_='crack').a.next_sibling.strip('\n \r /') # 品名
        try:
            parenttag = product_soup.find(string=re.compile('熱量')).parent.parent
            try:
                if len(parenttag) == 7:
                    product_calories = product_soup.find(string=re.compile('熱量')).parent.parent.contents[4].text.strip()
                    calories_dic[store_name][product_name] = float(product_calories.strip('蔗度熱量正常冰全糖熱量(大卡) kcal'))
                if len(parenttag) == 13:
                    product_name_one = product_name + product_soup.find(string=re.compile('熱量')).parent.parent.contents[2].text
                    product_calories_one = product_soup.find(string=re.compile('熱量')).parent.parent.contents[4].text
                    calories_dic[store_name][product_name_one] = float(product_calories_one.strip('蔗度熱量正常冰全糖熱量約(大卡) kcal'))
                    product_name_two = product_name + product_soup.find(string=re.compile('熱量')).parent.parent.contents[8].text
                    product_calories_two = product_soup.find(string=re.compile('熱量')).parent.parent.contents[10].text
                    calories_dic[store_name][product_name_two] = float(product_calories_two.strip('蔗度熱量正常冰全糖熱量(大卡) kcal'))
            except:
                if len(parenttag) == 7 and "/" in product_calories:
                    calories_list = product_calories.split("/")
                    capacity_list = product_soup.find(string=re.compile('熱量')).parent.parent.contents[2].text.split("/")
                    product_name_one = product_name + capacity_list[0]
                    product_name_two = product_name + capacity_list[1]
                    calories_dic[store_name][product_name_one] = float(calories_list[0].strip('蔗度熱量正常冰全糖熱量約(大卡) kcal中'))
                    calories_dic[store_name][product_name_two] = float(calories_list[1].strip('蔗度熱量正常冰全糖熱量約(大卡) kcal中'))
                    print(calories_dic[store_name][product_name_two], calories_dic[store_name][product_name_one])
                if len(parenttag) == 7 and ", " in product_calories:
                    calories_list = product_calories.split(", ")
                    capacity_list = product_soup.find(string=re.compile('熱量')).parent.parent.contents[2].text.split(", ")
                    product_name_one = product_name + capacity_list[0]
                    product_name_two = product_name + capacity_list[1]
                    calories_dic[store_name][product_name_one] = float(calories_list[0].strip('蔗度熱量正常冰全糖熱量約(大卡) kcal中'))
                    calories_dic[store_name][product_name_two] = float(calories_list[1].strip('蔗度熱量正常冰全糖熱量約(大卡) kcal中'))
                    print(calories_dic[store_name][product_name_two], calories_dic[store_name][product_name_one])
        except:
            pass
print(calories_dic)
        # count += 1
# '''



'''
# 測試區
print('test')
url = 'https://foodtracer.taipei.gov.tw/Front/Ice/ProductDetail?id=14565&pt=%e5%92%96%e5%95%a1'
r = requests.get(url, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.find('div', class_='crack').a.next_sibling.strip('\n \r /'))
# for i in range(10):
print(soup.find(string=re.compile('熱量')).parent.parent.contents[2].text.split("/"))
print('test')
# 測試區
'''

'''
sub_url = []
for product_tag in soup.find('div', id='mygallery').find_all('div', class_='panel'):
    sub_url.append(product_tag.a['href']) # sub_url: 某個子類別
    print(product_tag.text + '*')


# print(sub_url)
product_url = []
for url in sub_url: # 開始找產品
    url = 'https://foodtracer.taipei.gov.tw' + url
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for product_tag in soup.find_all('div', class_='product'):
        product_url.append(product_tag.a['href'])


print(product_url)
# 現在product_url有這家店全部產品的網址


# 開始爬熱量
calories_dic = {}
for url in product_url[:1]:
    time.sleep(0.5)
    url = 'https://foodtracer.taipei.gov.tw' + url
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    product_name = soup.find('div', class_='crack').a.next_sibling.strip('\n \r /') # 品名
    product_calories = soup.find('th', string='熱量(大卡)').next_sibling.next_sibling.text
    calories_dic[product_name] = float(product_calories)

print(calories_dic)
'''



# 大分類
    # 商店
        # 商店中分類（panel）
            # 商品
