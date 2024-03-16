import numpy as np
import scipy.signal as signal
import sounddevice as sd

class Note:
    # initialize a note object with given parameters
    def __init__(self, note, start_time, attack_time, release_time):
        self.note = note # MIDI key number
        self.frequency = self.note_to_freq(note) # note frequency given a MIDI key
        self.start_time = start_time # time when the note starts playing
        self.attack_time = attack_time # time it takes for note to reach full volume
        self.release_time = release_time # time it takes for note to fade after release
        self.release_start = None # time when the note starts to release 
        self.is_releasing = False # boolean flag to indicate if note is in the release phase


    @staticmethod
    def note_to_freq(note):
        # convert keyboard number to its frequency in Hz
        return 440.0 * (2.0 ** ((note - 69) / 12.0))

    # method marks note as releasing and record the start time
    def start_release(self, release_time):
        self.release_start = release_time # set the time when the note begins to release
        self.is_releasing = True # set the flag to indicate releasing

    # method calculates amplitude of the note based on current time and attack/release state
    def get_amplitude(self, current_time):
        # if note is releasing, calculate release phase amplitude
        if self.is_releasing and self.release_start is not None:
            release_phase = (current_time - self.release_start) / self.release_time
            return max(0, 1 - release_phase)  # Ensure amplitude doesn't go below 0
        else:
        # note is not releasing yet, calculate the attack phase amplitude
            attack_phase = (current_time - self.start_time) / self.attack_time
            return min(1, attack_phase)  # Ensure amplitude doesn't go above 1

class Synthesizer:
    def __init__(self):
        # initialize the synth with default settings
        self.samplerate = 48000 # number of samples audio per second
        self.blocksize = 512 # data size 
        self.sample_clock = 0 # keeps track of total number of samples processed
        self.active_notes = [] # list to keep track of ntoes that are currently being played
        self.volume = 1.0 
        self.waveform = 'sine' # waveform type
        self.attack_time = 0.05 # time for note to reach max volume
        self.release_time = 0.1 # time for note to fade out after being released
        self.filter = None # filter type
        self.frequency = 440 # default A4 note
        # setup output stream to play synthesized sound
        self.output_stream = sd.OutputStream(samplerate=self.samplerate, channels=1, blocksize=self.blocksize, callback=self.output_callback)
    
    # Method fetches new samples to play
    def output_callback(self, out_data, frame_count, time_info, status):
        if status:
            print("Status", status)

        current_time = self.sample_clock / self.samplerate 
        samples = np.zeros(frame_count, dtype=np.float32) # initialize array of zeros for the audio samples
        
        for note in list(self.active_notes):  # copy to allow modification during iteration
            t = np.linspace(current_time, current_time + frame_count / self.samplerate, frame_count) # time values for each sample
            amplitude = note.get_amplitude(current_time) # get the current amplitude for the note
            # remove the note from the active list if it has finished releasing
            if note.is_releasing and current_time - note.release_start >= note.release_time:
                self.active_notes.remove(note)
            else:
                # otherwise add the note's samples to the output buffer
                samples = samples + self.generate_samples(note.frequency, t, amplitude)
                # samples += amplitude * np.sin(2 * np.pi * note.frequency * t)

        # scale the samples by the volume and average them if there are multiple notes 
        samples *= self.volume / max(len(self.active_notes), 1)
        out_data[:] = np.reshape(samples, (frame_count, 1)) # write the samples to the output buffer
        
        self.sample_clock += frame_count # increment sample clock

   # method to start the output stream 
    def start_stream(self):
        self.output_stream.start()

   #helper method to convert midi key to frequency 
    def note_to_freq(self, note):
        return 440.0 * (2.0 ** ((note - 69) / 12.0))
    
    # method to stop given note and check release
    def stop_note(self, note):
        current_time = self.sample_clock / self.samplerate
        for n in self.active_notes:
            if n.note == note and not n.is_releasing:
                n.start_release(current_time)

    # method to play notes given a midi key           
    def play_note(self, midi_key):
        new_note = Note(midi_key, self.sample_clock / self.samplerate, self.attack_time, self.release_time)
        self.active_notes.append(new_note)
    
    def generate_samples(self, frequency, t, amplitude):
        if self.waveform == 'sine':
            samples = np.sin(2 * np.pi * frequency * t)
        elif self.waveform == 'square':
            return signal.square(2 * np.pi * frequency * t)
        elif self.waveform == 'sawtooth':
            return signal.sawtooth(2 * np.pi * frequency * t)
        return amplitude * samples
    
    # method to generate respective waveform parameter
    def generate_waveform(self, frequency, waveform, t):
        if waveform == 'sine':
            return np.sin(2 * np.pi * frequency * t, dtype=np.float32)
        elif waveform == 'square':
            return signal.square(2 * np.pi * frequency * t)
        elif waveform == 'sawtooth':
            return signal.sawtooth(2 * np.pi * frequency * t)
        return np.zeros_like(t, dtype=np.float32)
    
    # setter method to set waveform
    def set_waveform(self, waveform):
        self.waveform = waveform
        print(f"Waveform set to {self.waveform}")

    # setter method to set filter
    def set_filter(self, filter):
        self.filter = filter
        print(f"Filter set to {self.filter}.")

    # setter method to set volume 
    def set_volume(self, volume):
        self.volume = volume
        print(f"Volume set to {self.volume}.")

    # setter method to play test tone in main menu 
    def play_tone(self):
        tone = self.generate_tone(self.frequency, self.samplerate, self.waveform, self.volume)
        if self.filter:
            tone = self.apply_filter(tone, self.filter, self.samplerate)
        sd.play(tone, self.samplerate)
        sd.wait()

    # method to generate tone in main menu
    def generate_tone(self, frequency, fs, waveform, volume):
        t = np.linspace(0, 1, int(fs * 1), endpoint=False)
        if waveform == 'sine':
            tone = np.sin(2 * np.pi * frequency * t)
        elif waveform == 'square':
            tone = signal.square(2 * np.pi * frequency * t)
        elif waveform == 'sawtooth':
            tone = signal.sawtooth(2 * np.pi * frequency * t)
        else:
            raise ValueError("Unsupported waveform: {}".format(waveform))
        return tone * volume
    
    # method to apply filter to ton  
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