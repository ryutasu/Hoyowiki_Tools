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
Item_urls = {
    'ItemConfig': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfig.json',
    'ItemConfigAvatar': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigAvatar.json',
    'ItemPlayerCard': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemPlayerCard.json',
    'ItemConfigRelic': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigRelic.json',
    'ItemConfigEquipment': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigEquipment.json',
    'ItemConfigDisk': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigDisk.json',
    'ItemConfigBook': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigBook.json',
    'ItemConfigAvatarRank': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigAvatarRank.json',
    'ItemConfigAvatarPlayerIcon': 'https://raw.githubusercontent.com/Dimbreath/StarRailData/master/ExcelOutput/ItemConfigAvatarPlayerIcon.json'
}
Raritylist = {
    "1":"Normal",
    "2":"NotNormal",
    "3":"Rare",
    "4":"VeryRare",
    "5":"SuperRare"
}
tags_to_remove = ["</unbreak>", "<unbreak>", "</color>","<color=#8790abff>","<u>","</u>","</i>","<i>"]
text_to_remove = ["</unbreak>", "<unbreak>", "</color","</align>","</b","</size>","</i"]

def FindTextMap(name, text_map):
    for text, data in text_map.items():
        if str(name) in str(text):
            return data
    return ""

def checkRarity(Rarity):
    return next((Rarity_id for Rarity_id, Rarity_name in Raritylist.items() if Rarity_name == Rarity), None)

TextMap = { }
ItemConfig = { }
Itemlist = { }
output_file = 'output.txt'
outputcount = 1

print(f'Downloading data...')
for file_name, file_url in Item_urls.items():
    response = requests.get(file_url)
    if response.status_code == 200:
        try:
            data = json.loads(response.content.decode('utf-8'))
            ItemConfig.update(data)
            print(f'{file_name} Download complete')
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for {file_name}: {e}\n")
    else:
        print(f"{file_name} download failed\n")
print('All data download complete\n')

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

for Item_key,Item_data in ItemConfig.items():
    if "ItemName" in Item_data:
        Item_name = FindTextMap(Item_data["ItemName"]["Hash"], TextMap)
        for tag in tags_to_remove:
            Item_name = Item_name.replace(tag, "")
        Item_name = Item_name.replace("{NICKNAME}", "開拓者")
    if "ItemDesc" in Item_data:
        Item_desc = FindTextMap(Item_data["ItemDesc"]["Hash"], TextMap)
        for tag in text_to_remove:
            Item_desc = Item_desc.replace(tag, "")
        Item_desc = Item_desc.replace("\\n\\n", "\n \n")
        Item_desc = Item_desc.replace("\\n", "\n")
        Item_desc = Item_desc.replace("{NICKNAME}", "開拓者")
        Item_desc = Item_desc.replace("\u00A0", " ")
    if "ItemBGDesc" in Item_data:
        Item_BGDesc = FindTextMap(Item_data["ItemBGDesc"]["Hash"], TextMap)
        for tag in text_to_remove:
            Item_BGDesc = Item_BGDesc.replace(tag, "")
        Item_BGDesc = Item_BGDesc.replace("\\n\\n", "\n \n")
        Item_BGDesc = Item_BGDesc.replace("\\n", "\n")
        Item_BGDesc = Item_BGDesc.replace("{NICKNAME}", "開拓者")
        Item_BGDesc = Item_BGDesc.replace("\u00A0", " ")

    Rarity = checkRarity(Item_data["Rarity"])
    ItemIconPath = Item_data["ItemIconPath"]
    ItemIconPath = ItemIconPath.replace("SpriteOutput/", "")
    Itemlist[Item_name] = {"Item_desc":Item_desc,"Item_BGDesc":Item_BGDesc,"Rarity":Rarity,"Path":ItemIconPath}
    outputword = "Reading " + str(outputcount) + " Item...."
    print(f'{outputword}', end="\r")
    outputcount += 1
    #print(f"{Item_name}：{Itemlist[Item_name]}")
    #print("\n")
print("Itemlist reading completed")

while True:
    query = input('\nPlease enter the title of the item you are searching for, or enter "exit" to quit the program.: ')
    if query == 'exit':
        break
    if query:
        with open(output_file, 'w', encoding='utf-8') as output:
            for Itemname,Itemdata in Itemlist.items():
                if query in Itemname:
                    output.write(f'{Itemname}\n')
                    output.write(f'{Itemdata["Item_desc"]}\n\n{Itemdata["Item_BGDesc"]}\n')
                    output.write('———————————————————————————————————\n')
                    output.write(f'Rarity：{Itemdata["Rarity"]}\n')
                    output.write(f'{Itemdata["Path"]}')
                    output.write('\n********************************************\n')
        os.startfile(output_file)
    
    