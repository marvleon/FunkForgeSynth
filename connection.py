# Marvin Leon
# Midi connection

# pip install mido
# pip install rt midi
import mido
import numpy as np
import scipy.signal as signal
import sounddevice as sd

keyboard = mido.open_input('Digital Piano-1 0')

samplerate = 48000
blocksize = 1024
keyboard = mido.open_input('Digital Piano-1 0')
sample_clock = 0
out_freq = None
out_note = None

def output_callback(out_data, frame_count):
	global sample_clock
	# output wav adjusted by midi or nothing
	if out_freq:
		t = np.linspace(sample_clock / samplerate, (sample_clock + frame_count) / samplerate, frame_count)
		out_data = np.sin(2 * np.pi * out_freq * t)
	else:
		out_data = np.zeros(frame_count)
	sample_clock += frame_count


output_stream = sounddevice.OutputStream(samplerate=samplerate, channels=1, blocksize=blocksize, callback=output_callback,)
output_stream.start()

def note_to_freq(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))

def connection():
    global out_freq, out_note
    try:
        print('Waiting for MIDI messages from Piano. Press CTRL+C to exit.')
        for msg in keyboard:
            message_t = msg.type
            if msg.type == 'note_on':
            # Extract the note and velocity from the MIDI message
                note = msg.note
                velocity = msg.velocity / 127
                print(f'Note pressed: {note}, v: {velocity}')
                out_note = note
                out_freq = note_to_freq(note)
            
            # Play the sound using the synthesizer logic
                play_sound(note, velocity)
            if msg.type == 'note_on' and msg.velocity == 0:
                message_t = 'note_off'

            # Handle 'note_off' messages to stop notes
            elif msg.type == 'note_off':
                note = msg.note
                velocity = msg.velocity / 127
                print(f'depressed: {note}, v: {velocity}')
                if note == out_note:
                    out_note = None
                    out_freq = None 


                pass
    except KeyboardInterrupt:
        print('Exiting...')

connection()