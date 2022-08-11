#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import time
import selenium
from selenium import webdriver



driver=webdriver.Chrome(r'C:\Users\User\Desktop\chromedriver.exe')




driver.get("https://www.instagram.com/")




from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By



WebDriverWait(driver,30).until(EC.presence_of_element_located((By.NAME,'username')))




username_input = driver.find_elements_by_name('username')[0]
password_input = driver.find_elements_by_name('password')[0]
print("inputing username and password...")




username_input.send_keys("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
password_input.send_keys("XXXXXXXXXXXXXXXXXXX")



WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')))




login_click = driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button')[0]



login_click.click()


WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/div/div/section/div/button')))



store_click = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button')[0]
store_click.click()



WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div/div/div/div[3]/button[2]')))



open_click = driver.find_elements_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')[0]
open_click.click()


search_input = driver.find_elements_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')[0]
search_input.send_keys("蝦皮美食")



search_input.click()



url = "https://www.instagram.com/explore/tags/%E8%9D%A6%E7%9A%AE%E7%BE%8E%E9%A3%9F/"
driver.get(url)
all_html = driver.page_source
all_soup = Soup(all_html,'lxml')


num = str(all_soup)
num = num.split('則')[0]
num = num.replace(" ","")
num = num.split('"')[-1]
num = int(num)
print(num)


n_scroll=1
url_list = []

while True:
    scroll = 'window.scrollTo(0,document.body.scrollHeight);'
    driver.execute_script(scroll)
    html = driver.page_source
    soup = Soup(html,'lxml')
    
    for elem in soup.select('article div div div div a'):
        
        bottom = elem['href']
        bottom = "https://www.instagram.com/"+bottom
        if bottom not in url_list:
            print(bottom)
            url_list.append(bottom)
        time.sleep(1)
    if len(url_list) == num:
        break
print("total:"+str(len(url_list)))


print(len(url_list))


from lxml import etree
img_list = []
author_list = []
content_list = []
good_list = []
comment_list = []




for url in url_list:
    time.sleep(2)
    print(url)
    driver.get(url)
    html = driver.page_source
    soup = Soup(html,'lxml')
    
     #圖片、影片
    try:
        img = soup.find_all(class_="KL4Bh")[0].img.get('src')
        print(img)
        img_list.append(img)
    except:
        video = soup.find_all(class_="_5wCQW")[0].video.get('src')
        img_list.append(video)

    content = soup.find("div", class_="C4VMK")
    
    #作者
    author = str(content)
    author = author.split("</a>")[0]
    author = author.split(">")[-1]
    author_list.append(author)
    
    #文章內容
    text = []
    for word in content.text:
        if word == " ":
            word = "\n"
            text.append(word)
        else:
            text.append(word)
    text = "".join(text)
    if str(author) in text:
        text = text.split(author)[1]
    content_list.append(text)
    
    #評論
    scrape_xpath = etree.HTML(html)
    i = 0
    comment_text = []
    while True:
        i = i+1
        comment = scrape_xpath.xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div/div[2]/span/text()')
        if len(comment) == 0:
            break
        else:
            comment = str(comment)
            comment = comment.replace(" ","")
            comment = comment.replace("['","")
            comment = comment.replace("']","")

            comment_text.append(comment)
            
    text = ""
    text = str(text)
    for j in range(len(comment_text)):
        text = text+','+comment_text[j]

    text = text[1:]
    comment_list.append(text)
    
    
    #讚數
    try:
        good = soup.find("div", class_="Nm9Fw")
        good_list.append(good.text)
    except:
        good_list.append(" ")

print(img_list)
print(author_list)
print(content_list)
print(good_list)
print(comment_list)



df = pd.DataFrame()
df['img/video'] = pd.DataFrame(img_list)
df['author'] = pd.DataFrame(author_list)
df['content'] = pd.DataFrame(content_list)
df['good'] = pd.DataFrame(good_list)
df['comment'] = pd.DataFrame(comment_list)




df.to_excel(r"蝦皮美食.xlsx",index=False)


data_list = []
row_list = []
nRows = len(df)
nCols = len(df.columns)
for i in range(0, nRows):
    row_list = []
    for j in range(nCols):
        data_value = df.iloc[i][j]
        row_list.append(data_value)
    data_list.append(row_list)

print(data_list[509])


import pyodbc
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=蝦皮美食.accdb')
cursor = conn.cursor()


for i in range(len(data_list)):
    data_list[i][0] = data_list[i][0].replace("'","")
    data_list[i][1] = data_list[i][1].replace("'","")
    data_list[i][2] = data_list[i][2].replace("'","")
    data_list[i][3] = data_list[i][3].replace("'","")
    data_list[i][4] = data_list[i][4].replace("'","")
    try:
        cursor.execute("INSERT INTO 蝦皮美食 (img , author, content, good, comment)VALUES('%s','%s','%s','%s','%s')"%(data_list[i][0],data_list[i][1],data_list[i][2],data_list[i][3],data_list[i][4]))
    except:
        print(i)
cursor.commit()
cursor.close()
conn.close()



#載入json套件
import json 
jsonList = []

#利用迴圈將4個list寫入jsonList
for i in range(0,len(img_list)):
    jsonList.append({"img" : img_list[i], "author" : author_list[i],"content" : content_list[i],"good": good_list[i],"comment" : comment_list[i]})
#print(json.dumps(jsonList, indent = 1))

#利用json.dumps寫入json格式
x = json.dumps(jsonList,ensure_ascii=False)
print(x)


file = "shopee.json"
with open(file,"w",encoding='UTF-8') as f:
    json.dump(jsonList,f,ensure_ascii=False, indent = 1)
