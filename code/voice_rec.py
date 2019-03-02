import gpiozero as gpio
import time
from threading import Thread
from I2C_LCD_DRIVER import lcd
from Queue import Queue
def main():

    # GPIO set up
    button = gpio.Button(6)

    queue = Queue(1)

    # Set up of display
    addr = 0x27
    port = 1
    screen = lcd(addr, port)
    screen_thread = Thread(target=print_to_screen,args=(screen,queue))
    screen_thread.start()
    queue.put(['Welcome!'])
    time.sleep(1)
    queue.put(['Press the button'])

    # FSM for voice recording
    wait_for_button = 0
    listen_for_voice = 1
    show_text = 2
    state = wait_for_button
    try:
        while True:
            if state == wait_for_button:
                if button.wait_for_press(timeout=1):
                    button.wait_for_release()
                    queue.put(['Listening.', 'Listening..', 'Listening...'])
                    state = listen_for_voice
            elif state == listen_for_voice:
                if button.wait_for_press(timeout=1):
                    button.wait_for_release()
                    queue.put(['You said:', 'TEST WORD'])
                    state = show_text
            elif state == show_text:
                if button.wait_for_press(timeout=1):
                    button.wait_for_release()
                    queue.put(['Press the button'])
                    state = wait_for_button
    except KeyboardInterrupt:
        queue.put(['end'])
        screen_thread.join()
        print('')

def print_to_screen(screen, queue):
    while True:
        input = queue.get()
        # if input is 'end', break from look
        if input[0] == 'end':
            break

        # If only one string, display then pass
        if len(input) == 1:
            screen.lcd_display_string(input[0].ljust(16))
            pass

        # If multiple strings, loop them until queue is not empty
        i = 0
        while queue.empty():
            screen.lcd_display_string(input[i].ljust(16))
            i = (i + 1) % len(input)
            time.sleep(1)

    # Clear screen before retunring
    screen.lcd_clear()

if __name__ == "__main__":
    main()
