import sys
import os
import unittest 
import mido
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))
from connection import MidiConnection
from unittest.mock import patch, MagicMock

class TestMidiConnection(unittest.TestCase):

    @patch('mido.open_input')
    @patch('mido.get_input_names')
    def test_init(self, mock_get_input_names, mock_open_input):
        mock_get_input_names.return_value = ['MockMidi']
        mock_open_input.return_value = 'MockKeyboard'

        synth_mock = MagicMock()
        midi_conn = MidiConnection(synth_mock)

        mock_get_input_names.assert_called_once()
        mock_open_input.assert_called_once_with('MockMidi')
        self.assertEqual(midi_conn.synth, synth_mock)
        self.assertEqual(midi_conn.keyboard, 'MockKeyboard')

if __name__ == '__main__':
    unittest.main()
