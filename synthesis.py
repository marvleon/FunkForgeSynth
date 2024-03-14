class Synthesizer:
    def __init__(self):
        self.volume = 1.0 # default
        self.waveform = 'sine' # default
        self.filter = None
    def play_key(self, key):
        pass
    def set_waveform(self, waveform):
        self.waveform = waveform
        print(f"Waveform set to {self.waveform}")
    def set_filter(self, filter):
        self.filter = filter
        print(f"Filter set to {self.filter}.")
    def set_volume(self, volume):
        self.volume = volume
        print(f"Volume set to {self.volume}.")
