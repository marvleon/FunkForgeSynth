# Marvin Leon
# CS 410 Final
import numpy as np
import scipy.signal as signal
import sounddevice as sd
from synthesis import Synthesizer

class Menu:
    def __init__(self, synthesizer):
        self.synth = synthesizer

    def select_waveform(self):
        print("\nSelect a waveform:")
        print("1. Sine")
        print("2. Square")
        print("3. Sawtooth")
        waveform_choice = input("Enter your choice (1-3): ")
        wave = ['sine', 'square', 'sawtooth'][int(waveform_choice) - 1]
        self.synth.set_waveform(wave)
    
    def select_filter(self):
        print("\nSelect a filter (or none):")
        print("1. None")
        print("2. Lowpass")
        print("3. Highpass")
        filter_choice = input("Enter your choice (1-3): ")
        filter = [None, 'lowpass', 'highpass'][int(filter_choice) - 1]
        self.synth.set_filter(filter)
   
    def change_volume(self):
        volume_choice = float(input("Enter volume level (0.0 to 1.0): "))
        volume = max(0.0, min(volume_choice, 1.0))
        self.synth.set_volume(volume)
    
    def play_tone(self):
        print("playing")
        self.synth.play_tone()
 
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
        

pianoSynth = Synthesizer()
synthMenu = Menu(pianoSynth)
synthMenu.main_menu()