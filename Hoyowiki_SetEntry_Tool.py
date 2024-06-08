import json
import requests
import os
import webbrowser

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

tags_to_remove = ["</unbreak>", "<unbreak>", "</color>","<color=#8790abff>","<u>","</u>","</i>","<i>"]
download_results = { }
query_results = { }
contents = ""
outputtext = "const inputElements = document.querySelectorAll('.ed-text-input-inner');const contents = ["
output_file = 'output.txt'
count = 1
print('Downloading textmap...\n')
for file_name, file_url in file_urls.items():
    response = requests.get(file_url)
    if response.status_code == 200:
        download_results[file_name] = json.loads(response.content.decode('utf-8'))
        print(f"textmap{file_name} download complete({count}/13)......\n")
        count += 1
        continue
    print(f"textmap{file_name}download failed\n")
print('All textmap download complete\n')

while True:
    Language = input('Please select language(CHS,CHT,DE,EN,ES,FR,ID,JP,KR,PT,RU,TH,VI) or press Enter to skip:')
    if not Language:
        break
    if Language and Language.upper() in file_urls:
        Language = Language.upper()
        url = file_urls[Language]
        url_hoyolab = "https://wiki.hoyolab.com/pc/hsr/editor/guide"
        webbrowser.open(url_hoyolab)
        webbrowser.open(url)
    else:
        print('Invalid input\n')
    break


while True:
    query = input('\nPlease enter the text number you want to query(please use find function(Ctrl + F) to confirm the text you need and the corresponding text number), or enter "exit" to finish the program.: ')
    
    if query == 'exit':
        break

    contents = ""
    outputtext = "const inputElements = document.querySelectorAll('.ed-text-input-inner');const contents = ["
    results = {}
    chrome_results = {}
    
    for file_name, data in download_results.items():
        if query in data:
            results[file_name] = data[query]

    if results:
        with open(output_file, 'w', encoding='utf-8') as output:
            for file_name, result in results.items():
                for tag in tags_to_remove:
                    result = result.replace(tag, "")
                output.write(f'{file_name}: {result}\n')
                result = result.replace('"', '\\"')
                contents = contents + f"\"{result}\",\"\","
            contents = contents[:-4]
            outputtext += contents
            outputtext += "];inputElements.forEach((inputElement, index) => {if (inputElement) {inputElement.value = contents[index];}});inputElements.forEach((inputElement) => {if (inputElement) {inputElement.dispatchEvent(new Event('input', { bubbles: true }));}});"
            output.write(f'\n***Please copy the following text to the browser console workspace(Each browsers are different) of the set entry webpage***\n\n')
            output.write(outputtext)
        os.startfile(output_file)

    else:
        print(f'\nCan\'t find {query}')
    
