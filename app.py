import pyaudio
import wave
import sys
import getopt


CHUNK = 1024
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hr:p:",["rfile=","pfile="])
    except getopt.GetoptError:
        print("Usage -r <outname> -p <inputname")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage -r <output> -p <input>")
            sys.exit()
        elif opt in ("-r","--rfile"):
            WAVE_OUTPUT_FILENAME= arg
            p = pyaudio.PyAudio()
            FORMAT = pyaudio.paInt16
            stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

            print("* recording")

            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            print("* done recording")
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        elif opt in("-p","--pfile"):
            p = pyaudio.PyAudio()
            wf = wave.open(arg, 'rb')
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            data = wf.readframes(CHUNK)
            while data != '':
                stream.write(data)
                data = wf.readframes(CHUNK)
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
   main(sys.argv[1:])