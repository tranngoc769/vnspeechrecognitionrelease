# Tool convert danh sách các file text trong thư mục thành 1 file duy nhất đã qua chuẩn hóa : dòng, kí tự,... --> làm language model
# Hướng dẫn sử dụng : python main.py -i|--textdir [TEXTDIR] -o|--output [FILEOUT]
import  re
import sys
import  os
import argparse
parser = argparse.ArgumentParser(description='Huong dan su dung')
parser.add_argument('-i','--textdir', help='Folder of text files', required=True)
parser.add_argument('-o','--output', help='Path of output text file', required=True)
# args = vars(parser.parse_args())
# textDir =  args['textdir']
# fileOut = args['output']
textDir = "test/"
fileOut = "success.txt"
logDeleteFile = "logDelete.txt"
def replaceNumber(dateString):
      number = re.findall('(\d+.\d+)', dateString)
      for d in number:
            orNumber = d
            d = d.replace('-','')
            d = d.replace(',','')
            d = d.replace('.','')
            d = d.replace('h', ' giờ ')
            d = d.replace('m', ' mét ')
            temp = re.findall('(\d+.\d{4})', d)
            if len(temp) > 0:
                  d = d.replace('-',' năm ')
                  d = d.replace('/',' năm ')
            else:
                  d = d.replace('-',' tháng ')
                  d = d.replace('/',' tháng ')
            dateString = dateString.replace(orNumber, d)
      return dateString+" "
def replaceDate(dateString):
      dates = re.findall('(\d+.\d+.\d+)', dateString)
      for d in dates:
            originalDate = d
            d = d.replace('/',' tháng ',1)
            d = d.replace('/',' năm ',1)
            d = d.replace('.','')
            d = d.replace(',','')
            if "tháng" in d:
                  d = "ngày " + d
            dateString = "ngày "+ dateString.replace(originalDate, d)
            # newDate = datetime.strptime(d, "%d-%m-%y") 
            # newDate = datetime.strftime(newDate, "%d-%m-%y")   
            # dateString = dateString.replace(originalDate, newDate)
      return dateString
def replaceDivice(dateString):
      number = re.findall('(.\D/.\D)', dateString)
      for d in number:
            orNumber = d
            newNumber = orNumber.replace("/", " trên ")
            dateString = dateString.replace(orNumber, newNumber)
      return dateString
def replace2Number(dateString):
      number = re.findall('\d.[đdmgs]\d.', dateString)
      for d in number:
            orNumber = d
            d = d.replace('m',' mét ')
            d = d.replace('g',' giờ')
            d = d.replace('s',' giây')
            d = d.replace('đ',' đồng')
            d = d.replace('d',' đồng')
            dateString = dateString.replace(orNumber, d+" ")
      return dateString
def normalize_text(text):
      text = text.strip()
      text = text.replace("'","")
      text = text.replace(".","")
      text = replaceDivice(text)
      text = replaceNumber(text)
      text = replace2Number(text)
      text = replaceDate(text)
      text = re.sub(r'[/\\~—@^&*()_\/*{}<>,“”‘’"]',' ', text)
      text = re.sub("Chương \d", "", text)
      text = re.sub("C\d", "", text)
      text = re.sub(r"\bt\b", "tôi", text)
      # 
      text = text.replace("VND"," Việt Nam Đồng")
      text = text.replace("USD"," đồng")
      text = text.replace("xhcn"," Xã Hội Chủ Nghĩa")
      text = text.replace("Sarah","Tôi")
      text = text.replace("được"," được ")
      text = text.replace("$"," đồng")
      text = text.replace("bar","ba")
      text = text.replace("taxi","tắc xi")
      text = text.replace("radio"," ra đi ô")
      text = text.replace("ok","ô kê")
      text = text.replace("guitar","ghi ta")
      text = text.replace("piano","pi a nô")
      text = text.replace("Lusia","mực")
      text = text.replace("chocolate","sô cô la")
      text = text.replace("café","cà phê")
      text = text.replace("sofa","sô pha")
      text = text.replace("%"," phần trăm")
      text = text.replace('Washington',"Hà Nội")
      text = text.replace('Potamac',"Hồng")
      text = text.replace('Rachel',"Quang")
      text = text.replace('Rodney',"Quang")
      text = text.replace('Malaysia',"Ma lay si a")
      text = text.replace('tivi',"ti vi")
      # 
      text = text.replace("="," ")
      text = text.replace("−"," ")
      text = text.replace("USD"," đồng")
      text = text.replace("+"," ")
      text = text.replace("-"," ")
      text = text.replace("–"," ")
      text = text.replace("]"," ")
      text = text.replace("["," ")
      text = text.replace("gacsach"," ")
      text = text.replace("Hix"," ")
      text = text.replace("Alo"," ")
      text = text.replace("  "," ")
      text = text.replace("1h","1 giờ")
      text = text.replace("12h","12 giờ")
      text = text.replace("13h","13 giờ")
      text = text.replace("14h","15 giờ")
      text = text.replace("16h","16 giờ")
      text = text.replace("15h","15 giờ")
      text = text.replace("17h","17 giờ")
      text = text.replace("18h","18 giờ")
      text = text.replace("19h","19 giờ")
      text = text.replace("20h","20 giờ")
      text = text.replace("21h","21 giờ")
      text = text.replace("22h","22 giờ")
      text = text.replace("23h","23 giờ")
      text = text.replace("24h","24 giờ")
      text = text.replace("1h","1 giờ")
      text = text.replace("2h","2 giờ")
      text = text.replace("3h","3 giờ")
      text = text.replace("4h","4 giờ")
      text = text.replace("5h","5 giờ")
      text = text.replace("6h","6 giờ")
      text = text.replace("7h","7 giờ")
      text = text.replace("8h","8 giờ")
      text = text.replace("9h","9 giờ")
      text = text.replace("10h","10 giờ")
      text = text.replace("11h","11 giờ")
      text = text.replace("Haizzz"," ")
      text = text.replace("-"," ")
      text = text.replace("zai","trai")
      text = text.replace(";","#")
      text = re.sub('i+', 'i',text)
      text = re.sub('a+', 'a',text)
      text = re.sub('u+', 'u',text)
      text = re.sub(' +', ' ',text)
      text = re.sub('\?+', '#',text)
      text = re.sub(':+', '#',text)
      text = re.sub('!+', '#',text)
      text = re.sub(';+', '#',text)
      text = re.sub('\.+', '#',text)
      text = text.replace("…","#")
      return text
def numberToText(number, prefix =""):
      range1 = [
        [0, "không", "", ""],
        [1, "một", "mốt"],
        [2, "hai"],
        [3, "ba"],
        [4, "bốn"],
        [5, "năm", "lăm", "lăm"],
        [6, "sáu"],
        [7, "bảy"],
        [8, "tám"],
        [9, "chín"],
        [10, "mười"]
    ]
      range2 = [
            [1000000000, "tỷ"],
            [1000000, "triệu"],
            [1000, "ngàn"],
            [100, "trăm"]
      ]
      if (number < 0):
            number *= -1;
            return numberToText(number, "âm ")
      decTxt = ""
      intPart = number
      if (intPart >= 0 and intPart <= 10):
            r = range1[intPart]
            return prefix + r[1]+decTxt
      # mười -> mười chín
      if (intPart > 10 and intPart < 20):
            r = range1[intPart - 10]
            n = r[1]
            try:
                  n = r[3]
            except:
                  n = r[1]
            return prefix +"mười " + n + decTxt
      if (intPart >= 20 and intPart < 100):
            f = intPart // 10
            l = intPart % 10
            r = range1[f][1] #Bốn
            k = range1[l][1]
            try:
                  k = range1[l][2]
            except:
                  k = range1[l][1]
            return prefix +r +" mươi " + k 
      result = ''
      for i in range(0, len(range2)):
            r = range2[i]
            rVal = int(r[0])
            roundedDiv = intPart // rVal
            if roundedDiv >= 1:
                  remainder = intPart % rVal
                  result += numberToText(roundedDiv)
                  result += " " + r[1]
                  if remainder:
                        if remainder < 10:
                              result+= " lẻ"
                        result+= " " +numberToText(remainder)
                  break
      return prefix + result + decTxt
def checkNumberInSentense(text):
      temp = []
      check = True
      for s in text.split():
            if s.isdigit():
                  try:
                        s = numberToText(int(s))
                        check = False
                  except:
                        s = "4"
                        check = False
            temp.append(s)
      totalWord = len(temp)
      if (totalWord < 3 and check == False):
            totalWord = 0
      return totalWord, " ".join(temp)
def Normalize_File(textDir,fileOut):
      if os.path.isdir(textDir) == False:
            print("Not found folder")
            return False
      listFile = getTextFileInFolder(textDir)
      with open(fileOut, encoding="UTF-8", mode="w") as fOut:
            for filename in listFile:
                  with open(filename, encoding="UTF-8", mode="r") as f:
                        listString = f.readlines()
                        listString = [x.strip() for x in listString] 
                        # content = ("#".join(listString)).split("#")
                        content = listString
                        totalLine = len(content)
                        start = 0
                        for text in content:
                              # if "..." in text or "…" in text:
                              #       writeDelete(text)
                              #       continue
                              out = normalize_text(text)
                              subTextArr = out.split("#")
                              for subText in subTextArr:
                                    subText = subText.strip()
                                    totalWord, solveString = checkNumberInSentense(subText)
                                    if (totalWord != 0):
                                          fOut.write(solveString.strip() + "\n")
                        start+= 1
                              # print(str(start)+"/"+str(totalLine))
      return True
def writeDelete(text,path = "outDeelte.txt"):
      with open(path, encoding="UTF-8", mode="a") as fOut:
            fOut.write(text.strip() + "\n")
# import re
# text = "   Bắt~!@#$%^&*()_\\-=+/*<>đầu từ-gà gáy một tiếng, trâu bò lục-tục kéo thợ cầy đến đoạn đường phía trong điếm tuần.... - Mọi ngày, giờ ấy, những con-vật này cũng như những người cổ cầy, vai bừa kia, đã lần-lượt đi mò ra ruộng làm việc cho chủ."
# print(out)
def getTextFileInFolder(folder):
      listFile = []
      for file in os.listdir(folder):
          if file.endswith(".txt"):
            listFile.append(os.path.join(folder, file))
      return listFile
def startNormalize(textDir = 'test', fileOut = 'output.txt'):
      stt = Normalize_File(textDir, fileOut)
      if (stt):
            return True
      else:
            return False
if __name__ == "__main__":
      startNormalize()
