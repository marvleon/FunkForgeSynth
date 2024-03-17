import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))
from main import Menu
from unittest.mock import Mock, patch

class MenuTest(unittest.TestCase):
    def setUp(self):
        self.synth_mock = Mock()
        self.menu = Menu(self.synth_mock)

    def test_select_waveform(self):
        with patch('builtins.input', side_effect=['1']):
            self.menu.select_waveform()
            self.synth_mock.set_waveform.assert_called_with('sine')

    def test_select_filter(self):
        with patch('builtins.input', side_effect=['2']):
            self.menu.select_filter()
            self.synth_mock.set_filter.assert_called_with('lowpass')

    def test_change_volume(self):
        with patch('builtins.input', side_effect=['0.5']):
            self.menu.change_volume()
            self.synth_mock.set_volume.assert_called_with(0.5)

    def test_play_tone(self):
        self.menu.play_tone()
        self.synth_mock.play_tone.assert_called_once()

    def test_start_midi(self):
        with patch('MidiConnection') as midi_mock:
            self.menu.start_midi()
            midi_mock.assert_called_once_with(self.synth_mock)
            midi_mock.return_value.run.assert_called_once()


if __name__ == '__main__':
    unittest.main()
