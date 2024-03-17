import unittest

class Synth:
    def __init__(self):
        self.filter = None
        self.volume = None
        self.output_stream = None

    def set_filter(self, filter):
        self.filter = filter
        print(f"Filter set to {self.filter}.")

    def set_volume(self, volume):
        self.volume = volume
        print(f"Volume set to {self.volume}.")

    def start_stream(self):
        if self.output_stream is None:
            self.initialize_stream()
        self.output_stream.start()

    def stop_stream(self):
        if self.output_stream is not None:
            self.output_stream.stop()
            self.output_stream.close()
            self.output_stream = None
        print('stopping stream')
        print('closing stream')

    def note_to_freq(self, note):
        return 440.0 * (2.0 ** ((note - 69) / 12.0))

    def initialize_stream(self):
        self.output_stream = MockStream()

class MockStream:
    def start(self):
        print("Stream started")

    def stop(self):
        print("Stream stopped")

    def close(self):
        print("Stream closed")


class TestSynth(unittest.TestCase):
    def setUp(self):
        self.synth = Synth()

    def test_set_filter(self):
        self.synth.set_filter("low-pass")
        self.assertEqual(self.synth.filter, "low-pass")

    def test_set_volume(self):
        self.synth.set_volume(70)
        self.assertEqual(self.synth.volume, 70)

    def test_start_stream(self):
        self.synth.start_stream()
        self.assertIsNotNone(self.synth.output_stream)

    def test_stop_stream(self):
        self.synth.start_stream()
        self.synth.stop_stream()
        self.assertIsNone(self.synth.output_stream)

    def test_note_to_freq(self):
        freq = self.synth.note_to_freq(69)
        self.assertEqual(freq, 440.0)

if __name__ == '__main__':
    unittest.main()
