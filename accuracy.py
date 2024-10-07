import pyaudio
import numpy as np
import matplotlib.pyplot as plt

def generate_sine_wave(duration, frequency, rate):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def measure_microphone_accuracy(duration, rate, chunk_size):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")
    frames = []
    for i in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_data = audio_data.astype(np.float32) / 32767.0  # normalize to range [-1, 1]
    return audio_data

def plot_signals(reference_signal, recorded_signal, rate):
    time_ref = np.linspace(0, len(reference_signal) / rate, num=len(reference_signal))
    time_rec = np.linspace(0, len(recorded_signal) / rate, num=len(recorded_signal))
    
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_ref, reference_signal, label='Reference Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Reference Signal (Sine Wave)')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(time_rec, recorded_signal, label='Recorded Signal', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Recorded Signal (Microphone Input)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_frequency_spectra(reference_signal, recorded_signal, rate):
    fft_ref = np.fft.fft(reference_signal)
    fft_rec = np.fft.fft(recorded_signal)

    freq_ref = np.fft.fftfreq(len(fft_ref), 1 / rate)
    freq_rec = np.fft.fftfreq(len(fft_rec), 1 / rate)

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(freq_ref[:len(freq_ref)//2], np.abs(fft_ref)[:len(freq_ref)//2], label='Reference Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum - Reference Signal')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(freq_rec[:len(freq_rec)//2], np.abs(fft_rec)[:len(freq_rec)//2], label='Recorded Signal', color='orange')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum - Recorded Signal')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    duration = 3  # seconds
    frequency = 440  # Hz
    rate = 44100  # Hz
    chunk_size = 1024

    reference_signal = generate_sine_wave(duration, frequency, rate)
    recorded_signal = measure_microphone_accuracy(duration, rate, chunk_size)
    
    plot_signals(reference_signal, recorded_signal, rate)
    plot_frequency_spectra(reference_signal, recorded_signal, rate)
