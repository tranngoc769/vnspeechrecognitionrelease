#Tool tao thu muc chua data /wav , /txt thu file json
import csv
import os
import codecs
import os.path 
import numpy
import soundfile as sf
from shutil import copyfile
import numpy as np
from log import Logger
import json
# Return true if not NaN
def checkAudioIsNaN(path):
    sound, sample_rate = sf.read(path, dtype='int16')
    sound = sound.astype('float32') / 32767  # normalize audio
    if len(sound.shape) > 1:
        if sound.shape[1] == 1:
            sound = sound.squeeze()
        else:
            sound = sound.mean(axis=1)  # multiple channels, average
    if (np.count_nonzero(sound))==0:
            return False
    return True
pathWav = "/datasetIR/wav/"   #"PATH_WAV_DATA/" directory
pathTxt = "/datasetIR/txt/"   #"PATH_TXT_DATA" directory
pathCSVout = "/datasetIR/40train.csv"  #"PATH_CSV_IN"
pathCSVErrout = "/datasetIR/error_train.csv"  #"PATH_CSV_IN"
okLog = Logger("csv_info")
errLog = Logger("csv_erro")
pathNan = "/datasetIR/nantest/"
countName = 0
# Get file name without full path
def getFileName(wav):
      x = wav.split('/')
      return x[len(x)-1]
def createTranscriptFile(filename,data):
      file = codecs.open(filename, "w", "utf-8")
      file.write(data)
      file.close()

def Solve(path, data):  # Copy wav, create txt
      global countName
      fullPath = path #Name with path
      wavName = pathWav+"IR_{0:06d}.wav".format(countName)  #wav name
      filename = pathTxt+"IR_{0:06d}.txt".format(countName)  #txt name
      if os.path.isfile(fullPath) == False:
            okLog.error('Not found : ' + fullPath)
            errLog.error('Not found : ' + fullPath)
            return False, filename,wavName
      else:
            try:
                  copyfile(fullPath,wavName)
                  # return True  #Split filename without extension
                  createTranscriptFile(filename, data)
                  countName += 1
            except Exception as err:
                  errLog.error(err+":"+wavName)
                  okLog.error(err+":"+wavName)
                  return False, filename,wavName
            return True, filename,wavName
      return True, filename,wavName
def run():
      if os.path.isdir(pathWav) == False:
            os.mkdir(pathWav)
            okLog.info('Create '+pathWav)
      if os.path.isdir(pathTxt) == False:
            os.mkdir(pathTxt)
            okLog.info('Create '+pathTxt)
      if os.path.isdir(pathNan) == False:
            os.mkdir(pathNan)
            okLog.info('Create '+pathTxt)            
      okCSV = []   # Data list
      erCSV = []   # Erro list
      with open("transcript.json", "r") as read_file:
            transcript = json.load(read_file)
      #     print("Decoded JSON Data From File")
            listTranscript = transcript['list']
            line_count = 0
            line_success = 0
            line_erro = 0
            for item in  listTranscript:
                  try:
                        # Copy wav, create txt
                        notNaN = checkAudioIsNaN(item["key"])
                        if (notNaN):
                              # Bool, trans.txt , pathwav+/name.wav
                              check,filename,wavName = Solve(item["key"], item["text"])
                              if (check == True):
                                    okCSV.append([wavName,filename])
                                    line_success += 1
                              else:
                                    erCSV.append([wavName])
                                    line_erro += 1
                        else:
                              errLog.error("NAN : " + item["key"])
                              copyfile(item["key"], pathNan + getFileName(item["key"]))
                              erCSV.append([wavName])
                              line_erro += 1
                  except Exception as identifier:
                        okLog.error(identifier)
                        line_erro += 1
                  line_count += 1
            okLog.info('Processed success : ' + str(line_success))
            okLog.info('Processed error : '+ str(line_erro))
            okLog.info('Processed totals : '+ str(line_count))
      
      with open(pathCSVout, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(okCSV)
      if (line_erro == 0):
            return
      with open(pathCSVErrout, 'w', newline='', encoding='utf-8') as fileerr:
            writer = csv.writer(fileerr)
            writer.writerows(erCSV)
      
if __name__ == "__main__":
      run()