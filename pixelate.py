import cv2
from PIL import Image
import numpy as np
from tkinter import messagebox
import argparse

drawing = False
mouseX, mouseY = -1, -1
ix, iy = -1, -1


def pixelate_image(image, pixel_size):
    width, height = image.size
    image = image.resize(
        (max(width // pixel_size, 1), max(height // pixel_size, 1)), Image.NEAREST
    )
    image = image.resize((max(width, 1), max(height, 1)), Image.NEAREST)
    return image


def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, mouseX, mouseY

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            mouseX, mouseY = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        mouseX, mouseY = x, y


def main(filename, pixel_size):
    image = Image.open(filename)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_callback)

    while True:
        img_temp = cv_image.copy()
        if drawing:
            cv2.rectangle(
                img_temp,
                (ix, iy),
                (mouseX, mouseY),
                (0, 255, 0),
                1,
                cv2.LINE_AA,
                shift=0,
            )
        cv2.imshow("image", img_temp)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            top_left_x = min(ix, mouseX)
            top_left_y = min(iy, mouseY)
            bottom_right_x = max(ix, mouseX)
            bottom_right_y = max(iy, mouseY)

            selected_area = image.crop(
                (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
            )
            pixelated_area = pixelate_image(selected_area, pixel_size)
            image.paste(pixelated_area, (top_left_x, top_left_y))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            image.save("pixelated_image.jpg")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    default_image_file = "example.jpg"
    default_pixel_size = 16

    parser = argparse.ArgumentParser(description="Pixelate an image.")
    parser.add_argument("image_file", nargs="?", default=default_image_file, help="Input image file name")
    parser.add_argument("-p", "--pixelsize", type=int, default=default_pixel_size, help="Pixel size for pixelation")

    args = parser.parse_args()
    image_file = args.image_file
    pixel_size = args.pixelsize

    main(image_file, pixel_size)
