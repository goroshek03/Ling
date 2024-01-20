# Импорт библиотек
import requests
from bs4 import BeautifulSoup

# Глобальные переменные
URL = 'https://v102.ru/center_line_dorabotka_ajax.php?page=2&category=0'
URL_MAIN = 'https://v102.ru'


def cleanListSymbol(str):
    str = str.replace('\xa0', '')
    str = str.replace('\r\n', '')
    str = str.replace('\xa0 \r\n', '')
    str = str.replace('\n', ' ')
    str.strip()

    return str



def get_full_text(final_list, links_list):



    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }
    try:
        for link in links_list:

            #Отправим GET()-запрос на сайт и сохраним полученное
            page = requests.get(link, headers=headers)

            # html объект в дерево объектов Python
            soup = BeautifulSoup(page.text, "lxml")
            # print(soup)

            mainNews = soup.find_all('div', class_='n-text')
            final_list.append(cleanListSymbol(mainNews[0].text))
    except:
        print('Exeption')

def addTextToNews(listOfdictionary, paresedTextList):

    # for i in range(len(listOfdictionary)):
    #     listOfdictionary[i].update(listOfdictionary(Текст_Новости=paresedTextList[i]))

    i = 0
    for item in listOfdictionary:
        item['Текст Новости'] = paresedTextList[i]
        i += 1


