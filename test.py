import json

jsonDictionory = []


with open('File_to_DataBase/async_scrapper_news10000TEXT.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    for item in data:

        jsonDictionory.append(

            {
                "Текст Новости": item
            }
        )


with open("File_to_DataBase/news10000TextEdit.json", "a", encoding="utf-8") as file:
    json.dump(jsonDictionory, file, indent=4, ensure_ascii=False)



