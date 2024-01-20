# Импорт библиотек
import json

import requests
from bs4 import BeautifulSoup
from function import *
import time
import asyncio
import aiohttp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Глобальные переменные
URL = 'https://v102.ru/center_line_dorabotka_ajax.php?page=1&category=0'
URL_MAIN = 'https://v102.ru'
wholeNewsDictionary = []  # Итоговый список для создания json
allLinksOfNews = []
finalListOfNewsText = []


# ----------------------------------------------------------------------
# ------------------------------ Код парсера ---------------------------
# ----------------------------------------------------------------------

start_time = time.time()
async def get_page_data(session, page):

    URL = f'https://v102.ru/center_line_dorabotka_ajax.php?page={page}&category=0'
    # Берем агента текущего пользователя, чтобы не блокнули по причине (Бот)
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }



    async with session.get(url=URL, headers=headers) as responce:
        responce_text = await responce.text()

        # html объект в дерево объектов Python
        soup = BeautifulSoup(responce_text, "lxml")
        mainNews = soup.find_all('div', class_='new-article')

        for item in mainNews:

            #Берет ссылку
            try:
                newsURL = (URL_MAIN + item.find('a', class_='detail-link').get('href'))
                allLinksOfNews.append(newsURL)
            except:
                newsURL = 'Нет данных'


            # # Берет весь текст новости
            # try:
            #     newsFullText = get_full_text(newsURL)
            # except:
            #     newsFullText = 'Что-то не так с тэгами'

            #Берет Название
            try:
                newsTitle = item.find('a', class_='detail-link').next_element.text
            except:
                newsTitle = 'Нет данных'

            #Берет дату
            try:
                newsDate = item.find('span', class_='mobile-date').text
            except:
                newsDate = 'Нет данных'

            # Берет описание
            try:
                newsDescription = item.find('div', class_='short-text').find('a').text
            except:
                newsDescription = 'Нет данных'

            # Итоговый список для json
            wholeNewsDictionary.append(

                {
                    "URL": newsURL,
                    "Название Новости": newsTitle,
                    "Дата": newsDate,
                    "Описание": cleanListSymbol(newsDescription)
                    #"Тест Новости": cleanListSymbol(newsFullText)
                }
            )

# 
async def gather_data():

    URL = 'https://v102.ru/center_line_dorabotka_ajax.php?page=1&category=0'
    # Берем агента текущего пользователя, чтобы не блокнули по причине (Бот)
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    async with aiohttp.ClientSession() as session:
        responce = await session.get(url=URL, headers=headers)
        soup = BeautifulSoup(await responce.text(), "lxml")

        tasks = []

        for page in range(1, 671):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


# --------------------------------------------------------------------------------------------
async def get_data_page_new(session, link):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    async with session.get(url=link, headers=headers) as responce:
        responce_text = await responce.text()
        # html объект в дерево объектов Python
        soup = BeautifulSoup(responce_text, "lxml")

        mainNews = soup.find_all('div', class_='n-text')
        finalListOfNewsText.append(
            {

                "Тескт Новости": cleanListSymbol(mainNews[0].text)

            }
        )



async def gather_data_page():
    async with aiohttp.ClientSession() as session:

        tasks = []

        for link in allLinksOfNews:
            task = asyncio.create_task(get_data_page_new(session, link))
            tasks.append(task)

        await asyncio.gather(*tasks)

# --------------------------------------------------------------------------------------------

def main():

    asyncio.run(gather_data())
    print('pages')
    # asyncio.run(gather_data_page())
    get_full_text(finalListOfNewsText, allLinksOfNews)
    # print(finalListOfNewsText)
    # addTextToNews(wholeNewsDictionary, finalListOfNewsText)


if __name__ == "__main__":
    print('main start:\n')
    main()
    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")

    with open("File_to_DataBase/async_scrapper_news10000.json", "a", encoding="utf-8") as file:
        json.dump(wholeNewsDictionary, file, indent=4, ensure_ascii=False)

    with open("File_to_DataBase/async_scrapper_news10000TEXT.json", "a", encoding="utf-8") as file:
        json.dump(finalListOfNewsText, file, indent=4, ensure_ascii=False)



