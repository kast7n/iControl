

import speech_recognition as sr
import pyautogui as pag
from typing import Dict, List


def read_mic_input(r: sr.Recognizer, mic: sr.Microphone) -> Dict:

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source)

    response = {"success": True, "error": None, "transcription": None}

    try:
        response["transcription"] = r.recognize_google(audio).lower()


        response["transcription"] = response["transcription"].replace("-", " ")
        response["transcription"] = response["transcription"].replace("/", " ")
        response["transcription"] = response["transcription"].replace("\\", " ")
        response["transcription"] = response["transcription"].replace(" 00",
                                                                      " 0 0")


    except sr.RequestError:
        response["success"] = False
        response["error"] = "Error occurred with the API request."
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech."

    return response


def move_mouse_relative(direction: str, distance: int) -> None:
    if direction == "up":
        pag.moveRel(0, -distance, duration=1)
    elif direction == "down":
        pag.moveRel(0, distance, duration=1)
    elif direction == "left":
        pag.moveRel(-distance, 0, duration=1)
    elif direction == "right":
        pag.moveRel(distance, 0, duration=1)


def scroll(direction: str, amount: int) -> None:

    if direction == "up":
        pag.scroll(amount)
    elif direction == "down":
        pag.scroll(-amount)


def perform_hotkey(keys: List[str]) -> None:

    for k in keys:
        pag.keyDown(k)
    keys.reverse()
    for k in keys:
        pag.keyUp(k)


def correct_key_names(keys: List[str]) -> List[str]:

    joined = " ".join(keys)
    joined.replace("control", "ctrl")
    joined.replace("page down", "pagedown")
    joined.replace("page up", "pageup")
    joined.replace("volume down", "volumedown")
    joined.replace("volume up", "volumeup")
    joined.replace("page down", "pagedown")
    joined.replace("print screen", "printscreen")
    return joined.split()


def execute_command(parsed: List[str]) -> None:

    parsed = correct_key_names(parsed)
    x, y = pag.position()
    if parsed[0] == "move" and parsed[1] == "to":
        COMMANDS["move to"][0](int(parsed[2]), int(parsed[3]), duration=1)
    elif parsed[0] == "move":
        move_mouse_relative(parsed[1], int(parsed[2]))
    elif parsed[0] == "double" and parsed[1] == "click":
        COMMANDS["double click"][0](x, y)
    elif parsed[1] == "click":
        COMMANDS["left click"][0](x, y, button=parsed[0])
    elif parsed[0] == "hold" and parsed[1] in ["left", "middle", "right"]:
        COMMANDS["hold right"][0](x, y, button=parsed[1])
    elif parsed[0] == "release" and parsed[1] in ["left", "middle", "right"]:
        COMMANDS["release right"][0](x, y, button=parsed[1])
    elif parsed[0] == "scroll":
        COMMANDS["scroll up"][0](parsed[1], int(parsed[2]))
    elif parsed[0] == "type" and parsed[1] == "this":
        COMMANDS["type this"][0](" ".join(parsed[2:]), interval=0.05)
    elif parsed[1] == "key":
        COMMANDS[parsed[0] + " " + parsed[1]][0](parsed[2])
    elif parsed[0] == "use" and parsed[1] == "shortcut":
        perform_hotkey(parsed[2:])
    elif parsed[0] == "quit" and parsed[1] == "program":
        print("You said: quit program. Now quitting...")
        COMMANDS["quit program"][0]()


if __name__ == '__main__':
    pag.FAILSAFE = False
    COMMANDS = {"move to": (pag.moveTo, 4), "move up": (pag.moveRel, 3),
                "move down": (pag.moveRel, 3), "move left": (pag.moveRel, 3),
                "move right": (pag.moveRel, 3), "left click": (pag.click, 2),
                "double click": (pag.doubleClick, 2), "right click": (pag.click, 2),
                "middle click": (pag.click, 2), "hold left": (pag.mouseDown, 2),
                "hold right": (pag.mouseDown, 2), "hold middle": (pag.mouseDown, 2),
                "release left": (pag.mouseUp, 2), "release right": (pag.mouseUp, 2),
                "release middle": (pag.mouseUp, 2), "scroll up": (pag.scroll, 3),
                "scroll down": (pag.scroll, 3), "hold key": (pag.keyDown, 3),
                "release key": (pag.keyUp, 3), "press key": (pag.press, 3),
                "use shortcut": (pag.hotkey, 0), "type this": (pag.typewrite, 0),
                "quit program": (quit, 2)}

    KEYBOARD_KEYS = {'\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                     'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                     'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                     'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                     'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                     'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                     'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                     'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                     'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                     'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                     'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                     'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                     'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                     'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                     'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                     'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                     'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                     'command', 'option', 'optionleft', 'optionright'}

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    exiting = False
    while not exiting:
        print("Please say a voice command!")
        command = read_mic_input(recognizer, microphone)
        if not command["success"]:
            print(command["error"])

        elif command["error"]:
            print("{} Please try saying that again.".format(command["error"]))

        if command["transcription"]:
            parsed = command["transcription"].split()
            if len(parsed) < 2:
                print("{} is an invalid command. Please try another one!"
                      .format(command["transcription"]))
            else:
                base_command = parsed[0] + " " + parsed[1]

                if base_command == "type this" and len(parsed) > 2:
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command == "use shortcut" and len(parsed) > 2 and all(
                        [key in KEYBOARD_KEYS for key in parsed[2:]]):
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command in COMMANDS and "key" in base_command and len(
                        parsed) == COMMANDS[base_command][1] and parsed[2] in KEYBOARD_KEYS:
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command in COMMANDS and len(parsed) == COMMANDS[base_command][1] \
                        and all([x.isnumeric() for x in parsed[2:]]):
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))

                else:
                    print("{} is an invalid command. Please try another one!"
                          .format(command["transcription"]))
                    
