# USERS

- Make sure your midi keyboard is turned ON and pluggin IN
- Turn your speaker volume DOWN
- **HEARING SAFETY IS IMPORTANT**

# DEVELOPERS

- The program is separated into classes for the Menu, Synthesizer, Midi Connection, and Notes.
- The Synthesizer object does not require the Menu to run.
- The Note class depends on the Synthesizer class, there is little functionality but storing data on its own

## Synthesizer

- To use the Synthesizer object on its own, instatiate a synth

```
synth = Synthesizer()
```

- To play a midi key in the synth

```
synth.play_note(67)
```

- The synth class has dedicated functions to start and stop streams:

```
synth.stop_stream()
synth.start_stream()
```

these are required for when you utilize the midi connection object.

### Adjusting attack and release time can only be done within the source code via synthesis.py

- Attack and release are stored as:

```
self.attack_time
self.release_time
```
