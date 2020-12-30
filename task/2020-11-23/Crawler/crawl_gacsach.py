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
categoryUrl = "https://gacsach.com/van-hoc-viet-nam.html"

import normalize
def getTotalPageOfCategory():
    global categoryUrl
    global wd
    wd.get(categoryUrl)
    soup = BeautifulSoup(wd.page_source, features="lxml")
    lastPageUl = soup.find_all('li', {'class','pager-last last' }) # get ul
    lastPageHref = lastPageUl[0].find_all('a')[0]  #get child : <a> --> href

    pass
    # listEndChapters = .contents
    # lastChapter = listEndChapters[len(listEndChapters) - 1]
    # a_element = lastChapter.find_all('a')[0]
    # totalChapter = getTotalChapter(a_element.text)
    return 1

if __name__ == "__main__":
    getTotalPageOfCategory()
    pass
    # listUrl = getListUrl(urlPath)
    # for url in listUrl:
    #     print("Story path : "+url)
    #     try:
    #         crawStoryUrl(url)
    #     except Exception as err:
    #         print("Error : " + str(err))
    # normalize.startNormalize()
    # # main(url)
    