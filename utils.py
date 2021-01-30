import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

CHAR_LIST = '@%#*+=-:. ' # short
CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " # long

BG_CODE = 255 # white
BG_CODE = 0 # black

FACE_CASCADE = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_focus(img):
    # detect faces
    faces = FACE_CASCADE.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)

    # focus on the face
    x, y, w, h = faces[0]
    img = img[y:y+h, x:x+w]

    '''
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    '''

    return img

def aschier(img):
    num_cols = 100
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=10 * (int(num_cols / 100) + 1))
    num_chars = len(CHAR_LIST)

    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("too many rows or columns")
        # default width and height
        cell_width = 6
        cell_height = 12

        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    char_width, char_height = font.getsize("A")

    out_width = char_width * num_cols
    out_height = 2 * char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), BG_CODE)
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):
        line = "".join([
            CHAR_LIST[
                min(int(np.mean(
                    image[
                        int(i * cell_height):min(int((i + 1) * cell_height), height),
                        int(j * cell_width):min(int((j + 1) * cell_width), width)]
                    ) * num_chars / 255), num_chars - 1)]
            for j in
                range(num_cols)]) + "\n"
        draw.text((0, i * char_height), line, fill=255 - BG_CODE, font=font)

    return np.asarray(out_image.crop(out_image.getbbox()))
