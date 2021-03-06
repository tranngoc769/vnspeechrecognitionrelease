# Tool crawl audio netnews
# Cách sử dụng : truyền homepage, run 
# Output : 
# + Mỗi thể loại là một folder
# + Trong mỗi folder thể loại, mỗi page là 1 folder
# + Audio được lưu dưới dạng mp3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import threading
import re
import os
import time
homepage = "http://netnews.vn/"
INFO = '\033[94m'
DEBUG = '\033[93m'
NORM = '\033[0m'
def getCategory(url="http://netnews.vn/bao-noi.html"):
      with urlopen(url) as homepage:
            soup = BeautifulSoup(homepage.read(), features="lxml")
            breadcum = soup.find('div', {'class': 'breadcrumd-tn'})
            child_a_element = breadcum.find_all('a')
            listCates = [x.attrs['href'].strip() for x in child_a_element]
            return listCates
# Get list songs
def getListSongOfPage(soup):
      scripts = soup.find_all('script',{'type':'text/javascript'});
      if (len(scripts) < 1):
            print("No script found")
            return listSong_str
      listSongs = []
      listSong_str = ""
      for item in reversed(scripts):
            if (len(item.contents) > 0):
                  if "songs" in item.contents[0]:
                        listSong_str = item.contents[0]
                        break
      if (listSong_str==""):
            print("No list songs found")
            return listSongs
      listSongs = re.findall("(/?http.+?mp3)",listSong_str)
      return listSongs
# Get next page
def getNextPage(soup):
      nextpage = soup.find('p',{'class':'more-tn-cate'})
      if nextpage == None:
            return None
      return nextpage.find('a').attrs['href'].strip()
# Make dir
def makedir(cateDir):
      if os.path.isdir(cateDir) == False:
            os.makedirs(cateDir)
# get folder name
def getCategoryName(string):
      string = string.replace("-","_")
      index = string.rfind(".")
      if (index <0):
            return string
      return string[0:index]
# get mp3 name
def getMP3Name(url):
      pos = url.rfind("/")
      return url[pos+1:]
# crawl page
def crawl_page(cateFolder,child_link):
      print(DEBUG+"Page : "+child_link+NORM)
      url = homepage + child_link
      with urlopen(url) as link:
            soup = BeautifulSoup(link.read(), features="lxml")
            try:
                  listSongs = getListSongOfPage(soup)
                  pageName = getCategoryName(child_link)
                  if (len(listSongs)> 0):
                        pageDir = cateFolder+"/"+pageName
                        makedir(pageDir)
                        for mp3 in listSongs:
                              mp3Name = getMP3Name(mp3)
                              mp3Path = pageDir+"/"+mp3Name
                              if (os.path.isfile(mp3Path)):
                                    print("Already existed")
                                    continue
                              urllib.request.urlretrieve(mp3, mp3Path)
                        print(INFO+"FINISH : "+mp3Name+NORM)
            except Exception as err:
                  print(DEBUG+"ERROR : "+str(err)+NORM)
                  # Craw every song here
            nextpage = getNextPage(soup)
            if (nextpage!=None):
                  crawl_page(cateFolder,nextpage)
            else:
                  print(DEBUG+"Finish : "+ cateFolder+NORM)
# Per thread 
def crawl_category(cate):
      try:
            print(DEBUG+"CRAWL : "+cate+NORM)
            cateName = getCategoryName(cate)
            makedir(cateName)
            crawl_page(cateName,cate)
      except Exception as err :
            print("Crawl category erro : " + str(err))
# Multi thread 
def crawl_thread(cate):
      cmdThr = threading.Thread(target=crawl_category, args = (cate,))
      cmdThr.setDaemon(True)
      cmdThr.start()
# Test 
def test(cate):
      while True:
            print("Test : " + cate)
            time.sleep(2)
import urllib
if __name__ == '__main__':
      homepage = "http://netnews.vn/"
      listCates = getCategory()
      for cate in listCates:
            crawl_thread(cate)
      while (True):
            pass
      print("Finish")
