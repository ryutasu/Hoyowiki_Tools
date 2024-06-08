import json
import os
import requests

file_urls = {
    'CHS': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapCHS.json',
    'CHT': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapCHT.json',
    'DE': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapDE.json',
    'EN': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapEN.json',
    'ES': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapES.json',
    'FR': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapFR.json',
    'ID': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapID.json',
    'JP': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapJP.json',
    'KR': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapKR.json',
    'PT': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapPT.json',
    'RU': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapRU.json',
    'TH': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapTH.json',
    'VI': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapVI.json'
}
Book_urls = {
    'LocalbookConfig': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/LocalbookConfig.json',
    'BookSeriesConfig': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/BookSeriesConfig.json',
    'ItemConfigBook': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigBook.json',
    'ItemConfig': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfig.json'
}
tags_to_remove = ["</unbreak>", "<unbreak>", "</color>","<color=#8790abff>","<u>","</u>","</i>","<i>"]
text_to_remove = ["</unbreak>", "<unbreak>", "</color","</align>","</b","</size>","</i"]

def FindTextMap(name, text_map):
    for text, data in text_map.items():
        if str(name) in str(text):
            return data
    return False

TextMap = { }
BookIDConfig = { }
BookTextConfig = { }
ItemConfigBook = { }
ItemConfig = { }
outicon = ""
IDlist = { }
Configlist = { }
outputlist = { }
output_file = 'output.txt'
Name_file = 'Book_Title_List.txt'

print(f'Downloading data...')
for file_name, file_url in Book_urls.items():
    response = requests.get(file_url)
    if response.status_code == 200:
        try:
            data = json.loads(response.content.decode('utf-8'))
            if file_name == 'LocalbookConfig':
                BookTextConfig = data
            elif file_name == 'BookSeriesConfig':
                BookIDConfig = data
            elif file_name == 'ItemConfigBook':
                ItemConfigBook = data
            elif file_name == 'ItemConfig':
                ItemConfig = data
            print(f'{file_name} Download complete')
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for {file_name}: {e}\n")
    else:
        print(f"{file_name} download failed\n")
print('All data download complete\n')
ItemConfigBook.update(ItemConfig)

while True:
    Language = input('Please select language(CHS,CHT,DE,EN,ES,FR,ID,JP,KR,PT,RU,TH,VI): ')
    if Language and Language.upper() in file_urls:
        Language = Language.upper()
        url = file_urls[Language]
        print(f'Downloading {Language}textmap...')
        response = requests.get(url)
        if response.status_code == 200:
            TextMap = json.loads(response.content.decode('utf-8'))
            print('TextMap download complete\n')
            break
        else:
            print('Textmap download failed,please retry the progrem.\n')
    else:
        print('Invalid input\n')

for ID_key,ID_data in BookIDConfig.items():
    if "BookSeries" in ID_data:
        book_name = FindTextMap(ID_data["BookSeries"]["Hash"], TextMap)
        for tag in tags_to_remove:
            book_name = book_name.replace(tag, "")
    if "BookSeriesComments" in ID_data:
        book_comments = FindTextMap(ID_data["BookSeriesComments"]["Hash"], TextMap)
        for tag in tags_to_remove:
            book_comments = book_comments.replace(tag, "")
        IDlist[book_name] = {"ID":ID_key,"Comments":book_comments}
        Configlist[ID_key] = { }
print("IDlist reading completed")

for Config_key,Config_data in BookTextConfig.items():
    if "BookInsideName" in Config_data:
        Configname = FindTextMap(Config_data["BookInsideName"]["Hash"], TextMap)
        for tag in tags_to_remove:
            Configname = Configname.replace(tag, "")
    if "BookSeriesID" in Config_data:
        BookSeriesID = Config_data["BookSeriesID"]
    if "BookContent" in Config_data:
        BookContent = FindTextMap(Config_data["BookContent"]["Hash"], TextMap)
        BookContent = BookContent.replace("\\n\\n", "\n \n")
        BookContent = BookContent.replace("\\n", "\n")
        BookContent = BookContent.replace("{NICKNAME}", "開拓者")
        BookContent = BookContent.replace("\u00A0", " ")
        for tag in text_to_remove:
            BookContent = BookContent.replace(tag, "")
    if BookSeriesID not in Configlist:
        Configlist[BookSeriesID] = {}
    if Configname not in Configlist[BookSeriesID]:
        Configlist[BookSeriesID][Configname] = {}
    Configlist[BookSeriesID][Configname]["Booktext"] = BookContent
print("Configlist reading completed")

with open(Name_file, 'w', encoding='utf-8') as Name_fileoutput:
    for Name_fileoutputname,Name_fileoutputdata in IDlist.items():
        Name_fileoutput.write(f'{Name_fileoutputname}\n')
    os.startfile(Name_file)

while True:
    query = input('\nPlease enter the title of the book you are searching for, or enter "exit" to finish the program.: ')
    outicon = ""
    output_bookID = ""
    if query == 'exit':
        break
    if query:
        for bookname,bookdata in IDlist.items():
            if query in bookname:
                output_name = query
                bookID = bookdata["ID"]
                for output_ID,output_data in BookTextConfig.items():
                    if int(bookID) == int(output_data["BookSeriesID"]):
                        output_bookID = output_data["BookID"]
                        break
                for outputItemConfig_ID,outputItemConfig_data in ItemConfigBook.items():
                    if int(output_bookID) == int(outputItemConfig_ID):
                        outicon = outputItemConfig_data["ItemIconPath"]
                        outicon = outicon.replace("SpriteOutput/ItemIcon/", "")
                        outicon = outicon.replace("SpriteOutput/ItemFigures/", "")
                        break
                if outicon == "":
                    outicon = "No record"
                comment = bookdata["Comments"]
                outputlist.clear()
                for Config_ID,Config_data in Configlist.items():
                    if int(bookID) == int(Config_ID):
                        for Config_name,Config_Booktext in Config_data.items():
                            outputlist[Config_name] = Config_Booktext["Booktext"]
                if outputlist:
                    with open(output_file, 'w', encoding='utf-8') as output:
                        output.write(f'{output_name}\n')
                        output.write(f'{comment}\n')
                        output.write(f'Icon:{outicon}')
                        for Book_name, Book_text in outputlist.items():
                            output.write('\n********************************************\n')
                            output.write(f'{Book_name}\n——————————————\n')
                            output.write(f'{Book_text}')
                    os.startfile(output_file)
                break
    
    