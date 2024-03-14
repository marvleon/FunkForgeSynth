class Synthesizer:
    def __init__(self):
        self.volume = 1.0 # default
        self.waveform = 'sine' # default
    def play_key(self, key):
        pass
    def set_waveform(self, waveform):
        self.waveform = waveform
    def set_volume(self, volume):
        self.volume = volume