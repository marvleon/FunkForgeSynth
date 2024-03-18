# Marvin Leon

# CS 410 Sound

# Funk Forge Synth

[License](LICENSE)

# Vision

The vision of this project is to make sound synthesis accessible to users who have never used a synthesizer. By providing a tool that combines simple design with sound manipulation features, the Funk Forge Synth will encourage creativity and experimentation. I want this application to help the user with sound creation without the need for deep technical knowledge. I’m inspired by the synth sounds of Parliament - Mothership Connection and Ohio Players - Funky Worm.

# Application Overview

This project aims to create a usable sound synthesizer application using Python. The Funk Forge Synth enables users to create and manipulate sounds through a command prompt main menu and play back using a midi keyboard. Testing was completing using python unit tests to verify correct method return values and operation. The synthesizer is a class object with a supporting note class object that stores individual note data. The midi connection class manages midi connection and requires a synthesizer object to send its note data to. The main class contains the menu object which calls upon the synthesizer and midi connection classes.

Heres an examples

```
synth = Synthesizer() # create a synthesizer object able to synthesize and playback sound
menu = Menu(synth) # create a menu object to manipulate synthesizer parameters and pass in your synth object
menu.main_menu() # call the menu operations to be prompted in the command line
# within the main menu, playing a note looks like:
syth.play_tone()
```

# Project Summary

This project was both challenging and rewarding. This is my first course where I studied any bit of sound. I think sound on its own is daunting, and computers are challenging in their own right. Mixing the two makes for a very fun and challenging experience.

I think my project works well with producing sound and it has an interactive way to do that. This project allows you to bring your own midi keyboard or just mess around with sounds in the main menu. I feel satisified with the effort I put into the project and what it has produced.

I think what didn't work was the external .wav functionality. I think at that point I started to get more lost in my code and the math functions involved. I spent a lot of time debating/thinking about how to organize the code and pairing that with the heavy mathemetics and logic involved with sound synthesis made it all the more challenging. I think in the future, I will try to implement things in a more encapsulated way so that if I want to make changes I can make them to separate classes and methods.

Overall, this is a project I feel proud of and I like to show my roommates what I accomplished. This is a project I want to continue to improve and expand upon.

# How To Build and Run

1. **Environment Setup**: Ensure Python 3 is installed on your system. You will also need `pip` for installing Python packages.

2. **Install Dependencies**: Run the following command to install the necessary Python libraries:
   ```sh
   pip install numpy scipy sounddevice mido rtmidi
   ```
3. **Run**: To start the synth, plug in a midi device, then run the following command inside the FunkForgeSynth directory: `python source`

4. **Main Menu**: Check the command line for menu prompts. Use number keys to enter in desired menu options.

# Core Components

## Menu Interface

**Role:** Acts as user control for synthesizer and midi connection.

**Functionality:** Allows the user to select different waveforms, filters, volume, test notes, and enable midi connection. Instatiates a synthesizer and midi connection object.

## Synthesizer Logic

**Role:** The core engine that also uses a note class to store sound data for individual notes.

**Functionality:**

- Reads stored settings from Menu Interface and from the Midi connection
- Applies digital signal processing to synthesize sound based on user-defined parameters
- Outputs the sound when the user clicks play or when utilizing midi connection, all based on the adjustments made through the Menu interface
- Sine, Square, Sawtooth, and custom waveform samples

## Midi Connection

**Role:** Manages the connection of midi devices and how their input is translated through to the synthesizer for sound synthesis and playback.
**Functionality:**

- Self contained class called from the Menu class
- Searches for active midi devices and retrieves their name for Mido connection.
- Method run() actively waits for midi messages and sends the key/note value through to an instance of the synthesizer class for audio playback

# Issues of Concern

## Sound Complexity

Right now, there is limited waveform variety. The synthesizer has basic waveforms (sine, square, sawtooth) but that can limit the range of sounds that it can produce. There are limited modulation and shaping options. This is something I’m not super familiar with but I want to explore wave table synthesis more. There is the option to use an external .wav file.

## Performance

I don’t have an expectation for optimizing my application for performance. I’m more concerned with functionality and making sure that sounds can be made and manipulated. I want this synthesizer to eventually work in real-time to encourage sound experimentation so performance should be prioritized. I am also deprioritizing visual feedback (representing waveforms, envelopes, etc.) for the time being but this would be useful for sound creation.

## Flexibility

There is no support for plugins. The only external support allows the user to upload their own .wav file so they can use it. At the current moment, the attack and release time can only be adjusted through accessing the code which makes things a little difficult for those who do not want to tinker with the source files.
