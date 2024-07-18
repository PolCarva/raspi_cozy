import pygame
import sys
import serial
import os

# Set the SDL video driver to dummy to avoid the need for a display
os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.mixer.init()

audio_files = {
    '1': "/tibetan.ogg",
    '2': "/forest.ogg",
    '3': "/ocean.ogg",
    '4': "/rain.ogg",
    '5': "/jungle.ogg"
}

volume = 0.5
pygame.mixer.music.set_volume(volume)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def handle_serial_input(command):
    global volume
    command = command.strip()
    if command in audio_files:
        pygame.mixer.music.load(audio_files[command])
        pygame.mixer.music.play(-1)
    elif command == '6':
        pygame.mixer.music.stop()
    elif command == '9':
        volume = min(volume + 0.1, 1.0)
        pygame.mixer.music.set_volume(volume)
        print(f"Volume increased to: {volume}")
    elif command == '0':
        volume = max(volume - 0.1, 0.0)
        pygame.mixer.music.set_volume(volume)
        print(f"Volume decreased to: {volume}")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8')
            if line:
                handle_serial_input(line)
            else:
                print("No data read from the device.")
    except serial.SerialException as e:
        print("Error reading from serial port:", e)
    except UnicodeDecodeError as e:
        print("Error decoding data from serial port:", e)

    # Without pygame event handling since we are not using display
    # Just a simple loop to keep the script running
    os.system('clear')  # Clear the terminal to reduce clutter if desired
    print("Listening for serial input... (Press Ctrl+C to exit)")
    sys.stdout.flush()
