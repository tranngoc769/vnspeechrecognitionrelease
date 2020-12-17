# Tool kiểm tra các từ trong từ điển có ý nghĩa không
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import re
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
options.add_argument('-disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver.exe',options=options)


def readFile(path = "dictionay.txt"):
    listString = []
    with open(path, encoding="UTF-8", mode="r") as f:
        listString = f.readlines()
        listString = [x.strip() for x in listString]
    return listString

def checkSuggest(element, word):
    haveMean = False
    listSG = []
    list_text = element.find_all('div', {'class', 'ctuloai'})
    for text_div in list_text:
        text = text_div.text
        if word in text:
            haveMean = True
        listSG.append(text)
    return haveMean, listSG
import re
def getMeaning_Example(element):
    listMean = []
    list_text = element.find_all('span')
    for i in range(1,len(list_text)):
        text = checkWord(list_text[i].text)
        splitText = re.split(';|\?|!|\.',text)
        for x in splitText:
            if x =='' or '(' in x or ')' in x:
                continue
            listMean.append(x.strip())
    return listMean
def getWordPage(word):
    global wd
    wd.get("http://tratu.coviet.vn/hoc-tieng-anh/tu-dien/lac-viet/V-V/"+word+".html")
    # wd.get("http://tratu.coviet.vn/hoc-tieng-anh/tu-dien/lac-viet/V-V/ăn.html")
    soup = BeautifulSoup(wd.page_source, features="lxml")
    checkIsOk = soup.find_all('div', {'class','cTi p10 b'})
    if len(checkIsOk) == 0:
        listSugget = soup.find_all('div', {'class','ovf p10lr'})
        if len(listSugget) ==0:
            writeFile("unknow_wordlist.txt",word)
            print("No meaning : "+ word)
            return
        isMean, listSg = checkSuggest(listSugget[0], word)
        for text in listSg:
            writeFile("mean_wordlist.txt",text)
        if (isMean):
            print("Success : "+ word)
        else:
            writeFile("unknow_wordlist.txt",word)
            print("No meaning : "+ word)
        return

    print("Success : "+ word)
    writeFile("known_wordlist.txt",word)
    meaning_block = soup.select("#partofspeech_0")[0]
    litsMeans = getMeaning_Example(meaning_block)
    for text in litsMeans:
        writeFile("mean_wordlist.txt",text)
def checkWord(strings):
      pos = strings.find("(")
      pose = strings.find(")")
      if (pose >pos):
            res = strings[pos:pose+1]
            print(res)
            strings = strings.replace(res,"")
      return strings

def writeFile(filename, content):
    with open(filename, 'a', encoding="UTF-8") as writer:
        writer.write(content +"\n")
if __name__ == "__main__":
    dictionaries = readFile("dictionary.txt");
    for word in dictionaries:
        try:
            getWordPage(word)
        except Exception as err:
            print("Error : " + str(err))
    # main(url)
    