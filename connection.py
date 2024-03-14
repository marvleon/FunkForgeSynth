# Marvin Leon
# Midi connection

# pip install mido
# pip install rt midi
import mido
import numpy as np
import scipy.signal as signal
import sounddevice as sd

#print(mido.get_input_names())

keyboard = mido.open_input('Digital Piano-1 0')

def play_sound(note, velocity):
    print(f'Note: {note}, Velocity: {velocity}')
    samplerate = 48000
    frequency = 440.0 * (2.0 ** ((note - 69) / 12.0))
    wave = generate_sine_wave(frequency, velocity)
    sd.play(wave, samplerate)
    sd.wait()


def generate_sine_wave(frequency, velocity):
    amplitude = velocity / 127
    t = np.linspace(0, 1, int(48000), False)
    wave = amplitude * np.sin(2*np.pi * frequency * t)
    return wave


def main():
    try:
        print('Waiting for MIDI messages from Piano. Press CTRL+C to exit.')
        for msg in keyboard:
            if msg.type == 'note_on':
            # Extract the note and velocity from the MIDI message
                note = msg.note
                velocity = msg.velocity
            
            # Play the sound using the synthesizer logic
                play_sound(note, velocity)
            
            # Handle 'note_off' messages to stop notes
            elif msg.type == 'note_off':
                pass
    except KeyboardInterrupt:
        print('Exiting...')

main()