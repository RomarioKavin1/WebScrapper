import csv

from bs4 import BeautifulSoup
from selenium import webdriver
driver=webdriver.Chrome()
def urlpage(pg):
    pg=str(pg)
    url='https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    if(pg==1):
        return url
    else:
        url='https://www.amazon.in/s?k=bags&page='+pg+'&crid=2M096C61O4MLT&qid=1675266421&sprefix=ba%2Caps%2C283&ref=sr_pg_'+pg
        return url
def extract_record(item):
    taga=item.h2.a
    name=taga.text.strip()
    try:
        produrl='https://www.amazon.in'+taga.get('href')
        price=item.find('span','a-price-whole').text
    except AttributeError:
        return
    try:
        rating=item.i.text
        no_rating=item.find('span','a-size-base s-underline-text').text
    except AttributeError:
        rating=''
        no_rating=''
    result=(name,price,rating,no_rating,produrl)
    return result
records=[]
for page in range(1,21):
    url=urlpage(page)
    driver.get(url)
    soup =BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all('div',{'data-component-type':'s-search-result'})
    for i in results:
        record=extract_record(i)
        if record:
            records.append(record)
with open('results.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name','Price','Rating','No. of Rating','Link'])
    writer.writerows(records)