# Marvin Leon
# CS 410 Final

import numpy as np
import scipy.signal as signal
import sounddevice as sd

# Oscillator tone generator
def generate_tone(frequency, duration, fs, waveform, volume):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    if waveform == 'sine':
        tone = np.sin(2 * np.pi * frequency * t)
    elif waveform == 'square':
        tone = signal.square(2 * np.pi * frequency * t)
    elif waveform == 'sawtooth':
        tone = signal.sawtooth(2 * np.pi * frequency * t)
    else:
        raise ValueError("Unsupported waveform: {}".format(waveform))
    return tone * volume

    
def main():
    fs = 44100 # Sample rate in Hz
    duration = 2.0 # Seconds
    frequency = 440
    volume = 1.0

    # Menu items
    while True:
        print("\nSelect a waveform:")
        print("1. Sine")
        print("2. Square")
        print("3. Sawtooth")
        print("4. Change Volume")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice in ['1', '2', '3']:
            if choice == '1':
                waveform = 'sine'
            elif choice == '2':
                waveform = 'square'
            elif choice == '3':
                waveform = 'sawtooth'
            print(f"Playing a {duration} second {waveform} wave at {frequency} Hz with volume {volume}.")
            tone = generate_tone(frequency, duration, fs, waveform, volume)
            sd.play(tone, fs)
            sd.wait()
        elif choice == '4':
            volume = float(input("Enter volume level (0.0 to 1.0): "))
            volume = max(0.0, min(volume, 1.0)) 
            print(f"Volume set to {volume}.")
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()