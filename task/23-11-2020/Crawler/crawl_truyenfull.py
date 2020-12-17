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


def getListUrl(path = "url.txt"):
    listString = []
    with open(path, encoding="UTF-8", mode="r") as f:
        listString = f.readlines()
        listString = [x.strip() for x in listString]
    return listString
# getListChapter("https://truyenfull.vn/toi-thay-hoa-vang-tren-co-xanh/")

def getChapter(text):
    pos = text.find(':')
    if (pos== -1): pos = len(text)
    chap = text[0:pos]
    return [int(s) for s in chap.split() if s.isdigit()][0]
def getListChapter(url):
    global wd
    wd.get(url)
    soup = BeautifulSoup(wd.page_source, features="lxml")
    isPanigation = soup.find_all('ul', {'class','pagination pagination-sm'})
    if len(isPanigation) != 0:
        lastAPageElement = isPanigation[len(isPanigation)- 1].find_all('a')[0]
        newUrl = lastAPageElement.attrs['href']
        wd.get(newUrl)
        soup = BeautifulSoup(wd.page_source, features="lxml")
    ColumsChapters = soup.find_all('ul', {'class','list-chapter' })
    listEndChapters = ColumsChapters[len(ColumsChapters)-1].contents
    lastChapter = listEndChapters[len(listEndChapters) - 1]
    a_element = lastChapter.find_all('a')[0]
    totalChapter = getChapter(a_element.text)
    return totalChapter

def getTextOfPage(url, storyName, chapter): #url, laohac,15
    global wd
    print("Crawl : "+ url)
    storyName = storyName +"_chuong"+ str(chapter)+".txt"
    if os.path.isfile(storyName) == True:
        return
    wd.get(url)
    soup = BeautifulSoup(wd.page_source, features="lxml")
    items = soup.find_all('div', {'id','chapter-c' })[0]
    # print(items.text)
    writeFile(storyName, items.text)

def writeFile(filename, content):
    with open(filename, 'w', encoding="UTF-8") as writer:
        writer.write(content)
def crawStoryUrl(url, dirout = "textdir"):
    if os.path.isdir(dirout) == False:
        os.mkdir(dirout)
    if (url[len(url)-1] != "/"):
        url += "/"
    temp = url.split("/")
    storyName = dirout + "/" + temp[len(temp)-2].replace("-","")
    totalPage = getListChapter(url)
    # exp : 81
    for chapter in range(1,totalPage+1):
        try:
            getTextOfPage(url+'chuong-'+str(chapter),storyName,chapter)
        except Exception as err:
            print("Error : " + str(err))
dirname = "textdir"
urlPath = 'url.txt'
# main(url)
import normalize
if __name__ == "__main__":
    listUrl = getListUrl(urlPath)
    for url in listUrl:
        print("Story path : "+url)
        try:
            crawStoryUrl(url)
        except Exception as err:
            print("Error : " + str(err))
    normalize.startNormalize()
    # main(url)
    