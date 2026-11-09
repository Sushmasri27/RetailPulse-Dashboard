import sounddevice as sd
import soundfile as sf

samplerate = 16000
duration = 5

print("Speak now...")

recording = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype="float32"
)

sd.wait()

sf.write("test.wav", recording, samplerate)

print("Recording saved as test.wav")