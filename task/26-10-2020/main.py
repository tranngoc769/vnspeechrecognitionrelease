import csv
import os
import codecs
import os.path 
import numpy

parser = argparse.ArgumentParser(description='Huong dan su dung')
parser.add_argument('-i','--in', help='input data file', required=True)
parser.add_argument('-o','--out', help='output excel file', required=True)
parser.add_argument('-pw','--pathwav', help='folder wav file', required=True)
parser.add_argument('-pt','--pathtxt', help='folder txt file', required=True)
args = vars(parser.parse_args())

pathWav = args['pathwav']
pathTxt = args['pathtxt']

def getFileName(wav):
      x = wav.split('/')
      return x[len(x)-1]
def createTranscriptFile(filename,data):
      file = codecs.open(pathTxt+filename, "w", "utf-8")
      file.write(data)
      file.close()
def moveWavData(path):
      if os.path.isfile(path) == False:
            print('Not found ' + path)
      else:
            os.rename(path,pathWav+getFileName(path))
            print('Move ' +path)
def getTxtFromPath(path):
      x = path.split('/')
      return x[len(x)-1][0:len(fn)-4]+".txt"
def Solve(path, data):
      moveWavData(path)
      fn = getFileName(path)
      txtName = fn[0:len(fn)-4]+".txt"
      createTranscriptFile(txtName, data)
      return txtName
def run():
      if os.path.isdir(pathWav) == False:
            os.mkdir(pathWav)
            print('Create '+pathWav)
      if os.path.isdir(pathTxt) == False:
            os.mkdir(pathTxt)
            print('Create '+pathTxt)
      data = []
      with open(args['in'], mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = -1
            line_success = 0
            for row in csv_reader:
                  if line_count == -1:
                        print(f'Column names are {", ".join(row)}')
                        line_count = 0
                  try:
                        txtName = Solve(row["wav_filename"], row["transcript"])
                        print(f'\t{row["wav_filename"]} , {row["wav_filesize"]} , {row["transcript"]}.')
                        data.append([row["wav_filename"],txtName])
                        line_count += 1
                  except expression as identifier:
                        print(identifier)
                        line_success += 1
            print(f'Processed success {line_count} lines.')
            print(f'Processed error {line_success} lines.')
      with open(args['out'], 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            
if __name__ == "__main__":
      run()