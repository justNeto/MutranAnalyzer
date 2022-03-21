'''
|----------------------------------|
Program created by github/justNeto
|----------------------------------|
'''
import sys, os, re
import itertools
import musicalbeeps as mb


def translate_note(note):
    match note:
        case '-2':
            return 0
        case '-1':
            return 1
        case '0':
            return 2
        case '1':
            return 3
        case '2':
            return 4
        case '3':
            return 5
        case '4':
            return 6
        case '5':
            return 7
        case '6':
            return 8
        case '7':
            print("Error: musicalbeeps cannot reproduce the sound")
            os._exit(1)
        case '8':
            print("Error: musicalbeeps cannot reproduce the sound")
            os._exit(1)


def sound_duration(time_interval):
    t = 2
    match time_interval:
        case 'w':
            return t
        case 'h':
            return t/2
        case 'q':
            return t/4
        case 'e':
            return t/8
        case 's':
            return t/16
        case 't':
            return t/32
        case 'f':
            return t/64


def play_audio(word):
    player = mb.Player(volume=0.3, mute_output=True)

    notes = ['Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#']

    nf = 0 # number of flat after main note
    ns = 0 # number of sharps after main note

    note = re.compile(r'([A-GR][#b]*)')
    note_re = note.findall(word)[0] # Finds note: A
    if DEBUG == True:
        print("Note detected:", note_re)

    octave = re.compile(r'(-2|-1|0|1|2|3|4|5|6|7|8)')
    try:
        octave_re = octave.findall(word)[0] # Finds Octave
    except:
        octave_re = "None"

    time = re.compile(r'(w|h|q|e|s|t|f)')
    time_re = time.findall(word)[-1] # Finds time interval

    if (octave_re == "None" and note_re == "R"):
        if DEBUG == True:
            print("Not an octave detected")
        player.play_note("pause", sound_duration(time_re))
        return 0

    # Logic to correctly detect what note to play taking into account flats and sharps

    ns_octave_modifier = 1
    nf_octave_modifier = 0
    octave_modifier = 0

    if len(note_re) != 1:
        for i in range(len(note_re)):
            if note_re[i] == "#":
                ns += 1
            elif note_re[i] == "b":
                nf += 1

            if ns % 21 == 0 and ns != 0:
                ns_octave_modifier += 1
                octave_modifier += 1

            elif nf % 21 == 0 and nf != 0:
                nf_octave_modifier += 1
                octave_modifier -= 1
        note_re = note_re[0]
        if DEBUG == True:
            print("Base note", note_re)
            print("Number of sharps:", ns)
            print("Number of flats:", nf)

    if DEBUG == True:
         print("Base note")

    note_index = notes.index(note_re)
    if DEBUG == True:
        print("Index of the note before adding sharps and flats:", note_index)

    note_index = note_index + ns - nf
    if DEBUG == True:
        print("Index of the note after adding sharps and flats:", note_index)
        print("NS bigger than 21 by:", ns_octave_modifier, "times")
        print("NF bigger than 21 by:", nf_octave_modifier, "times")

    # start relative indexing
    if (note_index >= 21):
        note_sound = notes[note_index-21*ns_octave_modifier]
        if DEBUG == True:
            print("Actual note to play:", note_sound)
    elif (note_index <= -1):
        note_sound = notes[note_index+21*nf_octave_modifier]
        if DEBUG == True:
            print("Actual note to play:", note_sound)
    else:
        note_sound = notes[note_index]
        if DEBUG == True:
            print("Actual note to play:", note_sound)

    # Logic to translate mut note to musical beeps note
    octave_re = translate_note(octave_re)
    octave_re = int(octave_re) + octave_modifier
    if DEBUG == True:
        print("Octave to play:", octave_re)

    note_tmp = note_sound[0]
    if DEBUG == True:
        print("Save base note:", note_tmp)

    note_sound = note_tmp + str(octave_re)
    if DEBUG == True:
        print("Composed note:", note_tmp)

    player.play_note(note_sound, sound_duration(time_re))


def input_options():
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_options()
            os._exit(1)

        elif sys.argv[1] == "-f" or sys.argv[1] == "--file":
            MUTRAN_FILE = open(sys.argv[2])
            return MUTRAN_FILE

        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            print("Version 4.0. Same for MA.py but validating | and right and left.")
            os._exit(1)

    except:
        print("Missing arguments. Try python", sys.argv[0], "-h or python", sys.argv[0], "--help for more information.\n")
        os._exit(1)

    else:
        print("Invalid option. Try python", sys.argv[0], "-h or python", sys.argv[0], "--help for more information.\n")
        os._exit(1)


def regex_validation(word):
    if re.fullmatch(r'(([A-G]|[A-G]([#b]*))(-2|-1|0|1|2|3|4|5|6|7|8)|(R))((w|h|q|e|s|t|f)|(w|h|q|e|s|t|f)(([.]+)|(t|3|5|7|9)))', word):
        return 0
    elif word == "|":
        return 1
    elif word == "right":
        return 2
    elif word == "left":
        return 3


def print_options():
    print("Usage: python MA.py [OPTIONS] ... [FILE] ...\n")
    print("Analyzes a MUTRAN music file writing and produces the song accordingly.\n")
    print("Options for the analyzer.\n")
    print("-f, --file       file in MUTRAN to be analyzed.\n")
    print("-h, --help       shows this help menu and exits.\n")
    print("-v, --version    current version of project.\n")


''' Main python loop'''
def main():

    global DEBUG

    DEBUG_ENABLE = input("Do you want to debug the code? Y(yes) | N(no)\n")
    if DEBUG_ENABLE == "Y" or DEBUG_ENABLE == "Yes":
        DEBUG = True
    else:
        DEBUG = False

    MUTRAN_FILE = input_options()
    MUTRAN_LIST = list()

    for line in MUTRAN_FILE:
        MUTRAN_LIST = line.split()
        if line[0] == '#': # Drops everyline starting with #
            continue
        else:
            for i in range(len(MUTRAN_LIST)):
                if (regex_validation(MUTRAN_LIST[i]) == 0): # Checks if expression is valid
                    print(f"Expression read: {MUTRAN_LIST[i]} - Expression validated")
                    play_audio(MUTRAN_LIST[i])

                elif (regex_validation(MUTRAN_LIST[i]) == 1): # Checks if expression is valid
                    print(f"New bar detected: {MUTRAN_LIST[i]} - Expression validated")

                elif (regex_validation(MUTRAN_LIST[i]) == 2): # Checks if right hand will play
                    print(f"Expression read: {MUTRAN_LIST[i]} - Expression validated")

                elif (regex_validation(MUTRAN_LIST[i]) == 3): # Checks if left hand detected
                    print(f"Expression read: {MUTRAN_LIST[i]} - Expression validated")

                else:
                    print(f"Expression read: {MUTRAN_LIST[i]} - Expression is not validated - STOPPING THE PROGRAM")
                    os._exit(1)

    print("\nCode analyzed")

# Main Code
main()
