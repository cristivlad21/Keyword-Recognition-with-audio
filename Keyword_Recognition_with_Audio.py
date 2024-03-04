import speech_recognition as sr
import pyautogui
import re

# Initialize the speech recognition
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech_from_mic(recognizer, microphone):
    # Check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # Adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # Try recognizing the speech in the recording
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# Function to perform actions based on voice commands
def perform_action(command):
    # Check if the command is to quit the program
    if command == "quit program":
        return "QUIT"

    # Handling movement commands
    move_command = re.match(r'move (up|down|left|right) (\d+)', command)
    if move_command:
        direction, pixels = move_command.groups()
        pixels = int(pixels)
        current_x, current_y = pyautogui.position()
        if direction == 'up':
            pyautogui.moveTo(current_x, current_y - pixels)
        elif direction == 'down':
            pyautogui.moveTo(current_x, current_y + pixels)
        elif direction == 'left':
            pyautogui.moveTo(current_x - pixels, current_y)
        elif direction == 'right':
            pyautogui.moveTo(current_x + pixels, current_y)
        return "CONTINUE"

    # Handling key press commands
    press_command = re.match(r'press (\w+)', command)
    if press_command:
        key = press_command.group(1)
        pyautogui.press(key)
        return "CONTINUE"


    # For opening apps: Expect commands like "open WhatsApp" or "open notepad"
    open_command = re.match(r'open (\w+)', command)
    if open_command:
        app_name = open_command.group(1)
        open_app(app_name)
        return

    print(f"Command '{command}' is not recognized.")

    print(f"Command '{command}' is not recognized.")
    return "CONTINUE"

def open_app(app_name: str) -> None:
    """
    Open an app with a search bar by typing the app name and pressing Enter.
    """
    pyautogui.keyDown('winleft')  # Hold down the Windows key
    pyautogui.keyUp('winleft')    # Release the Windows key
    pyautogui.write(app_name)  # Type the app name
    pyautogui.press('enter')  # Press Enter to open the app


# Main loop to listen and respond to voice commands
def main():
    # Set up the microphone
    mic = sr.Microphone()

    print("Listening for voice commands. Say something like 'move up 100' or 'press enter'.")
    while True:
        print("Say your command:")
        command_response = recognize_speech_from_mic(recognizer, mic)
        if command_response["error"]:
            print("ERROR: {}".format(command_response["error"]))
            continue  # Skip to the next loop iteration
        print(f"You said: {command_response['transcription']}")
        if command_response['transcription']:
            action = perform_action(command_response['transcription'].lower())
            if action == "QUIT":
                print("Quitting program...")    
                break  # Exit the loop to end the program

# Uncomment the following line to run the script
main()
