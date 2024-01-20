import json
import re

def get_place():
    jsonDictionary = []

    # Открываем файл JSON для чтения
    with open('tomita/place.json', 'r', encoding='utf8') as file:
        # Загружаем данные из файла
        data = json.load(file)

    for json_object in data:
        value = json_object['Id'] # айди
        varId = value

        valueFact = json_object['FactGroup'][0]['Fact'][0]['Field'][0]['Value']# факт
        varValue = valueFact

        jsonDictionary.append(
            {
                "Id": varId,
                "Place": varValue
            }
        )

    with open("output_json/placeDB.json", "a", encoding="utf-8") as file:
        json.dump(jsonDictionary, file, indent=4, ensure_ascii=False)


def get_people():

    jsonDictionaryPeople = []

    # Открываем файл JSON для чтения
    with open('tomita/people.json', 'r', encoding='utf8') as file:
        # Загружаем данные из файла
        data = json.load(file)


    for json_object in data:
        value = json_object['Id'] # айди
        varId = value

        valueFact = json_object['FactGroup'][0]['Fact'][0]['Field'][0]['Value']# факт
        varValue = valueFact

        jsonDictionaryPeople.append(
            {
                "Id": varId,
                "VIP": varValue
            }
        )

    with open("output_json/peopleDB.json", "a", encoding="utf-8") as file:
        json.dump(jsonDictionaryPeople, file, indent=4, ensure_ascii=False)


def main():
    get_place()
    # get_people()


if __name__ == "__main__":
    print('main start:\n')
    main()




