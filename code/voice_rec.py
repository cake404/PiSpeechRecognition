import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from I2C_LCD_DRIVER import lcd

def main():

    button = Event()
    flags = [False]
    # Thread to check the button
    button_thread = Thread(target=check_button_press, args=(button, flags))
    button_thread.start()

    # Set up of display
    addr = 0x27
    port = 1
    screen = lcd(addr, port)

    # FSM for voice recording
    wait_for_button = 0
    listen_for_voice = 1
    show_text = 2
    state = wait_for_button
    try:
        while True:
            if state == wait_for_button:
                print('waiting')
                button.wait()
                print('done waiting')
                time.sleep(1)
                button.clear()
                pass
            elif state == listen_for_voice:
                pass
            elif state == show_text:
                pass
    except KeyboardInterrupt:
        flags[0] = True
        button_thread.join()
        GPIO.cleanup()
        print('\n')

def check_button_press(button, flags):
    # Set up of button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN)
    # check button
    input = GPIO.input(6)
    while True and not flags[0]:
        input = GPIO.input(6)
        print(input)
        if not input:
            button.set()
            time.sleep(0.1)

if __name__ == "__main__":
    main()
