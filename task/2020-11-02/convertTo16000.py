#Tool convert file wav to 16000Hz
mport wave
import audioop
import sys
import os
pathWav = "mydata"
outPath = "outwav"
ok = 0
failed = 0
from scipy.io import wavfile
import scipy.io
def downsampleWav(src, dst, inrate=44100, outrate=16000, inchannels=1, outchannels=1):
    global ok, failed
    if not os.path.exists(src):
        print('Source not found!')
        failed += 1
        return False
    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except:
        print('Failed to open files!')
        failed += 1
        return False

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1 & inchannels != 1:
            converted[0] = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print('Failed to downsample wav')
        failed += 1
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted[0])
    except:
        print('Failed to write wav')
        failed += 1
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print('Failed to close wav files')
        failed += 1
        return False
    ok += 1
    return True

if __name__ == "__main__":
    if os.path.isdir(pathWav) == False:
              os.mkdir(pathWav)
        print('Create '+pathWav)
    if os.path.isdir(outPath) == False:
        os.mkdir(outPath)
        print('Create '+outPath)
    for file in os.listdir(pathWav):
        if file.endswith(".wav"):
            src = os.path.join(pathWav, file)
            downsampleWav(src, os.path.join(outPath, file)) 
    print("Success : ", str(ok))
    print("Failed : ", str(failed))