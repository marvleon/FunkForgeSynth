# Marvin Leon
# CS 410 Final

import numpy as np
import scipy.signal as signal
import sounddevice as sd

class Menu:
    def __init__(self, synthesizer, midi_connection):
        self.syntheizer = synthesizer
        self.midi_connection = midi_connection
    def select_waveform(self):
        print("\nSelect a waveform:")
        print("1. Sine")
        print("2. Square")
        print("3. Sawtooth")
        waveform_choice = input("Enter your choice (1-3): ")
        self.waveform = ['sine', 'square', 'sawtooth'][int(waveform_choice) - 1]
    def select_filter(self):
        print("\nSelect a filter (or none):")
        print("1. None")
        print("2. Lowpass")
        print("3. Highpass")
        filter_choice = input("Enter your choice (1-3): ")
        self.filter_type = [None, 'lowpass', 'highpass'][int(filter_choice) - 1]
    def change_volume(self):
        self.volume = float(input("Enter volume level (0.0 to 1.0): "))
        self.volume = max(0.0, min(self.volume, 1.0))
        print(f"Volume set to {self.volume}.")
    def play_tone(self):
        print("playing")
        tone = generate_tone(frequency, duration, fs, waveform, volume)
        tone = apply_filter(tone, filter_type, fs)
        sd.play(tone, fs)
        sd.wait()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Select Waveform")
            print("2. Select Filter")
            print("3. Change Volume")
            print("4. Play Tone")
            print("5. Exit")
            main_choice = input("Enter your choice (1-5): ")

            if main_choice == '1':
                self.select_waveform()
            elif main_choice == '2':
                self.select_filter()
            elif main_choice == '3':
                self.change_volume()
            elif main_choice == '4':
                self.play_tone()
            elif main_choice == '5':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please try again.")
        
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

def apply_filter(tone, filter_type, fs):
    if filter_type == 'lowpass':
        # Create a low-pass filter (Butterworth)
        sos = signal.butter(4, 1000, 'lp', fs=fs, output='sos')
    elif filter_type == 'highpass':
        # Create a high-pass filter (Butterworth)
        sos = signal.butter(4, 1000, 'hp', fs=fs, output='sos')
    else:
        return tone  # No filter applied
    filtered_tone = signal.sosfiltfilt(sos, tone)  # Apply filter
    return filtered_tone

def play_tone(frequency, duration, fs, waveform='sine', volume=1.0, filter_type=None):
    tone = generate_tone(frequency, duration, fs, waveform, volume)
    if filter_type:
        tone = apply_filter(tone, filter_type, fs)
    sd.play(tone, fs)
    sd.wait()

def main():
    fs = 44100  # Sample rate in Hz
    duration = 2.0  # Seconds
    frequency = 440
    volume = 1.0
    waveform = 'sine'  # Default waveform
    filter_type = None  # Default filter

    while True:
        print("\nMain Menu:")
        print("1. Select Waveform")
        print("2. Select Filter")
        print("3. Change Volume")
        print("4. Play Tone")
        print("5. Exit")
        main_choice = input("Enter your choice (1-5): ")

        if main_choice == '1':
            print("\nSelect a waveform:")
            print("1. Sine")
            print("2. Square")
            print("3. Sawtooth")
            waveform_choice = input("Enter your choice (1-3): ")
            waveform = ['sine', 'square', 'sawtooth'][int(waveform_choice) - 1]

        elif main_choice == '2':
            print("\nSelect a filter (or none):")
            print("1. None")
            print("2. Lowpass")
            print("3. Highpass")
            filter_choice = input("Enter your choice (1-3): ")
            filter_type = [None, 'lowpass', 'highpass'][int(filter_choice) - 1]

        elif main_choice == '3':
            volume = float(input("Enter volume level (0.0 to 1.0): "))
            volume = max(0.0, min(volume, 1.0))
            print(f"Volume set to {volume}.")

        elif main_choice == '4':
            print(f"Playing a {duration} second {waveform} wave at {frequency} Hz with volume {volume} and {filter_type or 'no'} filter.")
            play_tone(frequency, duration, fs, waveform, volume, filter_type)

        elif main_choice == '5':
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

synthMenu = Menu()
synthMenu.main_menu()