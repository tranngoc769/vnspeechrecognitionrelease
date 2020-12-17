# Không ghi các dòng lỗi ra file output
# Dictionary filter
import time
start = time.time()
pathIn  = "success.txt"
pathDict  = "/work/Tool4Thesis/ToolLanguageModel/OUTPUTS/final_dictionary.txt"
# For output
erwords_output_txt = "erro_words_truyenfull.txt"
ok_output_txt = "success_sentenses_truyenfull.txt"
er_output_txt = "erro_sentenses_truyenfull.txt"
import normalize 
# for normalize 
beginNormalize = True 
inputTextFolder = "/work/languagemodel/temp/"
outputFile = "chuanhoa_truyenfull.txt"
def writeFile(text,path = "NoMeaningTexts.txt"):
      with open(path, encoding="UTF-8", mode="a") as fOut:
            fOut.write(text.strip() + "\n")
import time
if __name__ == "__main__":
      start = time.time()
      print("Normalize file....")
      if (beginNormalize):
            normalize.startNormalize(inputTextFolder, outputFile)
            pathIn = outputFile
      listDictionary = []
      print("Read dictionary file....")
      with open(pathDict, encoding="UTF-8", mode="r") as f:
            listDictionary = f.readlines()
            listDictionary = [x.strip() for x in listDictionary]
      lineCount = 0
      successCount = 0
      erroCount = 0
      erroCountWord = 0
      with open(pathIn, encoding="UTF-8", mode="r") as f:
            end = time.time()
            listLines = f.readlines()
            lenFile = len(listLines)
            print("Loading "+str(lenFile)  +" lines cost : " +str(end - start))
            filterTime = time.time()
            listLines = [x.strip() for x in listLines]
            for line in listLines:
                  if (line.strip() == ''):
                        continue
                  noErroWord = True
                  lineCount+=1
                  listWord = [y.strip() for y in line.split(" ")]
                  for item in listWord:
                        if item.lower() not in listDictionary:
                              noErroWord = False
                              writeFile(item,erwords_output_txt)
                              erroCountWord += 1
                  outString = " ".join(listWord)
                  if (noErroWord):
                        successCount += 1
                        writeFile(outString,ok_output_txt)
                  else:
                        erroCount += 1
                        writeFile(outString,er_output_txt)
                  if (lineCount % 10000 ==0):
                        print(lineCount)
            
            filterEndTime = time.time()
      print("Summary")
      print("Success: " + str(successCount))
      print("No meaning : " + str(erroCount))
      print("Erro words : " + str(erroCountWord))
      print("Filter time "+str(lenFile) +" cost : " +str(filterEndTime - filterTime))