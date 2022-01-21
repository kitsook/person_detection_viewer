import re
import serial
import tkinter
from PIL import Image, ImageTk

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

IMAGE_WIDTH = 96
IMAGE_HEIGHT = 96

RE_START_LINE = re.compile(r"\+\+\+ frame \+\+\+")
RE_END_LINE = re.compile(r"\-\-\- frame \-\-\-")
RE_PERSON_SCORE_LINE = re.compile(r"Person score\: \-?([0-9]+) No person score\: \-?([0-9]+)")

IS_PERSON_THRESHOLD = 110

buffer = bytearray()
buffer_started = False
buffer_filled = False

tk_image_label = None
is_person = False

def is_start_line(str):
    if RE_START_LINE.search(str):
        return True
    return False

def is_end_line(str):
    if RE_END_LINE.search(str):
        return True
    return False

def is_score_line(str):
    scores = RE_PERSON_SCORE_LINE.match(str)
    if scores is None or scores.group(1) is None or scores.group(2) is None:
        return None
    return (scores.group(1), scores.group(2))

def convert_line_to_byte_array(str):
    try:
        str = str.replace(' ', '').replace('\r', '').replace('\n', '')
        return bytearray.fromhex(str)
    except ValueError:
        return None

def add_to_buffer(str):
    global buffer
    converted = convert_line_to_byte_array(str)
    if converted:
        buffer.extend(converted)
    else:
        # problem reading data
        buffer_started = False
        print("Problem reading image. Resetting buffer")

def new_buffer():
    global buffer, buffer_started, buffer_filled

    buffer_started = True
    buffer_filled = False
    buffer = bytearray()

def end_of_buffer():
    global buffer_filled, buffer_started

    if buffer_started:
        buffer_filled = True
    buffer_started = False

def display_image():
    global tk_image_label

    image = Image.frombytes('L', (IMAGE_WIDTH, IMAGE_HEIGHT), bytes(buffer))

    tk_image = ImageTk.PhotoImage(image)
    if tk_image_label:
        tk_image_label.destroy()

    tk_image_label = tkinter.Label(image=tk_image, bd=0, highlightthickness=4)
    if is_person:
        tk_image_label.config(highlightbackground='green')
    else:
        tk_image_label.config(highlightbackground='red')

    tk_image_label.image = tk_image
    tk_image_label.place(x=0, y=0)

def process_line(line):
    global buffer_filled, is_person

    str = line.decode('utf-8')

    if is_start_line(str):
        new_buffer()
    elif is_end_line(str):
        end_of_buffer()
    elif buffer_started:
        add_to_buffer(str)
    else:
        scores = is_score_line(str)
        is_person = scores and int(scores[0]) > IS_PERSON_THRESHOLD

        if buffer_filled:
            display_image()

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry(str(IMAGE_WIDTH+8) + 'x' + str(IMAGE_HEIGHT+8))

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            line = ser.readline()
            if line:
                process_line(line)
            root.update()
