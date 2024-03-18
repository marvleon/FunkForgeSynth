from main import Menu, Synthesizer

def main():
    pianoSynth = Synthesizer()
    synthMenu = Menu(pianoSynth)
    synthMenu.main_menu()

if __name__ == "__main__":
    main()
