# Marvin Leon
# Midi connection

# pip install mido
# pip install rt midi
import mido

class MidiConnection:
    
    def __init__(self, synthesizer):
        self.keyboard = self.get_midi()
        self.synth = synthesizer
    def get_midi(self):
        input_names = mido.get_input_names()
        if input_names:
            keyboard = mido.open_input(input_names[0])
            print(f"Connected to {input_names[0]}")
        else:
            print("No MIDI input devices found.")
        return keyboard
    
    def run(self):
        global out_freq, out_note
        keyboard = self.keyboard
        #start synthesis stream
        self.synth.start_stream()
        print('Waiting for MIDI messages. Press CTRL+C to exit.')
        try:
            for msg in keyboard:
                message_t = msg.type
                if (message_t == 'note_on') and (msg.velocity == 0): 
                    message_t = 'note_off'
                    pass
                if message_t == 'note_on':
                # Extract the note and velocity from the MIDI message
                    note = msg.note
                    velocity = msg.velocity / 127
                    print(f'Note pressed: {note}, v: {velocity}')
                    self.synth.play_note(note)
                
                # Handle 'note_off' messages to stop notes
                elif message_t == 'note_off':
                    note = msg.note
                    self.synth.stop_note(note)
        except KeyboardInterrupt:
            print('Exiting...')