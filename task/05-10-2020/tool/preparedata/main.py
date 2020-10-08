import os
import soundfile as sf
countTime = 0
countFR = 0
import wave
import audioop
import sys
import os
import soundfile as sf
def downsampleWav(src, dst, outrate=16000, inchannels=1, outchannels=1):
    if not os.path.exists(src):
        print('Source not found!')
        return False
    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except:
        print('Failed to open files!')
        return False

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    f = sf.SoundFile(src)
    inrate = f.samplerate
    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1 & inchannels != 1:
            converted[0] = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print('Failed to downsample wav')
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted[0])
    except:
        print('Failed to write wav')
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print('Failed to close wav files')
        return False
    return True
count = 0
countTime = 0
countFR = 0
downfail = 0
import glob
wavCo = len(glob.glob1("./","*.wav"))
print(wavCo)
exit
def writelog(filename):
    with open("log.txt", "a") as myfile:
        myfile.write(filename)
        myfile.write("\n")

for filename in os.listdir("./"):
    if filename.endswith(".wav") :
        try:
            count = count+1
            print(count)
            f = sf.SoundFile(filename)
            lent = len(f)
            fr = f.samplerate
            time = lent / f.samplerate
            f.close()
            if (time > 10):
                os.remove(filename)
                print(filename + " has been delete because over 10seconds: " + str(time))
                countTime = countTime + 1
                writelog(filename + "| over time")
                continue
            if (fr > 16000):
                writelog(filename + "| over Hz "+ str(fr))
                oldname = filename
                newname = "QQ_"+filename
                if (downsampleWav(oldname,newname) == False):
                    print("Downsampling falied")
                    writelog(filename + "| down failed")
                    downfail = downfail + 1
                else:
                    countFR = countFR + 1
                    os.remove(oldname)
                    os.rename(newname,oldname)
        except:
            pass

print("Total "+ str(countTime) + " over 10s")
print("Total "+ str(countFR + downfail) + " over HZ")

print("Down HZ "+ str(countFR) + " over 16Hz success")
print("Down HZ "+ str(downfail) + " over 16Hz failed")
             
