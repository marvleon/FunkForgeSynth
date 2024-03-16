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
        self.active_notes = {}
        self.volume = 1.0 # default
        self.waveform = 'sine' # default
        self.filter = None
        self.frequency = 440
        self.output_stream = sd.OutputStream(samplerate=self.samplerate, channels=1, blocksize=self.blocksize, callback=self.output_callback)
    def output_callback(self, out_data, frame_count, time_info, status):
        if status:
            print("Status", status)
        t = np.linspace(self.sample_clock / self.samplerate, (self.sample_clock + frame_count) / self.samplerate, frame_count)
        samples = np.zeros(frame_count, dtype=np.float32)

        # Attempting thread safety
        active_notes_snapshot = self.active_notes.copy()

        for note, info in active_notes_snapshot.items():
            samples += self.generate_waveform(info['frequency'], info['waveform'], t)
            # Check if there are active notes
            if active_notes_snapshot:
                # if there are active notes, normalize samples by the number of active notes and clip the values
                samples = samples / len(active_notes_snapshot)
                samples = np.clip(samples, -1, 1)
            else:
                # no active notes, leave samples unchanged
                samples = samples 
        out_data[:] = np.reshape(samples, (frame_count, 1))
        self.sample_clock += frame_count
    def start_stream(self):
        self.output_stream.start()
    def note_to_freq(self, note):
        return 440.0 * (2.0 ** ((note - 69) / 12.0))
    def stop_note(self, note_to_compare):
        if note_to_compare == self.out_note:
            self.out_freq = None
            self.out_note = None
        if note_to_compare in self.active_notes:
            del self.active_notes[note_to_compare] 
            
    def play_note(self, note):
        self.out_freq = self.note_to_freq(note)
        self.out_note = note
        self.active_notes[note] = {'frequency': self.out_freq, 'waveform': self.waveform}

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