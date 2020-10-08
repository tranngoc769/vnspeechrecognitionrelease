import os
count = 1
import argparse
import os
parser = argparse.ArgumentParser(description='Huong dan su dung')
parser.add_argument('-p','--path', help='Input Path', required=True)
parser.add_argument('-f','--format', help='Format of file name', required=True)
args = vars(parser.parse_args())

if __name__ == "__main__":
    try :
        for filename in os.listdir(args['path']):
            if filename.endswith(".wav") :
                try:
                    oldname = filename
                    newname = args['format']+"_{0:06d}.wav".format(count)
                    os.rename(oldname,newname)
                    count = count + 1
                except: 
                    pass
    except Exception as ex :
        print("Failed :" +str(ex))




