import numpy as np
import scipy.signal as signal
import sounddevice as sd

class Note:
    def __init__(self, note, start_time, attack_time, release_time):
        self.note = note
        self.frequency = self.note_to_freq(note)
        self.start_time = start_time
        self.attack_time = attack_time
        self.release_time = release_time
        self.release_start = None
        self.is_releasing = False


    @staticmethod
    def note_to_freq(note):
        return 440.0 * (2.0 ** ((note - 69) / 12.0))

    def start_release(self, release_time):
        self.release_start = release_time
        self.is_releasing = True

    def get_amplitude(self, current_time):
        if self.is_releasing and self.release_start is not None:
            release_phase = (current_time - self.release_start) / self.release_time
            return max(0, 1 - release_phase)  # Ensure amplitude doesn't go below 0
        else:
            attack_phase = (current_time - self.start_time) / self.attack_time
            return min(1, attack_phase)  # Ensure amplitude doesn't go above 1

class Synthesizer:
    def __init__(self):
        self.samplerate = 48000
        self.blocksize = 512
        self.sample_clock = 0
        self.out_freq = None
        self.out_note = None
        self.active_notes = []
        self.volume = 1.0 # default
        self.waveform = 'sine' # default
        self.attack_time = 0.05
        self.release_time = 0.1
        self.filter = None
        self.frequency = 440
        self.output_stream = sd.OutputStream(samplerate=self.samplerate, channels=1, blocksize=self.blocksize, callback=self.output_callback)
    def output_callback(self, out_data, frame_count, time_info, status):
        if status:
            print("Status", status)
        current_time = self.sample_clock / self.samplerate
        samples = np.zeros(frame_count, dtype=np.float32)
        for note in list(self.active_notes):  # Use a copy of the list to allow modification during iteration
            t = np.linspace(current_time, current_time + frame_count / self.samplerate, frame_count)
            amplitude = note.get_amplitude(current_time)
            if note.is_releasing and current_time - note.release_start >= note.release_time:
                self.active_notes.remove(note)
            else:
                samples += amplitude * np.sin(2 * np.pi * note.frequency * t)
        samples *= self.volume / max(len(self.active_notes), 1)
        out_data[:] = np.reshape(samples, (frame_count, 1))
        self.sample_clock += frame_count
    def start_stream(self):
        self.output_stream.start()
    def note_to_freq(self, note):
        return 440.0 * (2.0 ** ((note - 69) / 12.0))
    def stop_note(self, note):
        current_time = self.sample_clock / self.samplerate
        for n in self.active_notes:
            if n.note == note and not n.is_releasing:
                n.start_release(current_time)
            
    def play_note(self, midi_key):
        new_note = Note(midi_key, self.sample_clock / self.samplerate, self.attack_time, self.release_time)
        self.active_notes.append(new_note)

    def generate_waveform(self, frequency, waveform, t):
        if waveform == 'sine':
            return np.sin(2 * np.pi * frequency * t, dtype=np.float32)
        elif waveform == 'square':
            return signal.square(2 * np.pi * frequency * t)
        elif waveform == 'sawtooth':
            return signal.sawtooth(2 * np.pi * frequency * t)
        return np.zeros_like(t, dtype=np.float32)
    
    def set_waveform(self, waveform):
        self.waveform = waveform
        print(f"Waveform set to {self.waveform}")
    def set_filter(self, filter):
        self.filter = filter
        print(f"Filter set to {self.filter}.")
    def set_volume(self, volume):
        self.volume = volume
        print(f"Volume set to {self.volume}.")
    def play_tone(self):
        tone = self.generate_tone(self.frequency, self.samplerate, self.waveform, self.volume)
        if self.filter:
            tone = self.apply_filter(tone, self.filter, self.samplerate)
        sd.play(tone, self.samplerate)
        sd.wait()
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