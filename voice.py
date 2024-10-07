import pyaudio
import numpy as np
import matplotlib.pyplot as plt

def measure_microphone_sensitivity(seconds=5, rate=44100, chunk_size=1024):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")
    frames = []
    for i in range(0, int(rate / chunk_size * seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_data = audio_data.astype(np.float32) / 32767.0  # normalize to range [-1, 1]
    return audio_data

def plot_audio_waveform(audio_data, rate):
    time = np.linspace(0, len(audio_data) / rate, num=len(audio_data))
    plt.plot(time, audio_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Microphone Sensitivity Measurement')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    audio_data = measure_microphone_sensitivity()
    plot_audio_waveform(audio_data, rate=44100)
