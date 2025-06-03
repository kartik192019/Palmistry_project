import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # For non-interactive backends (server rendering)
import matplotlib.pyplot as plt
import cv2
from pillow_heif import register_heif_opener


def heic_to_jpeg(heic_dir, jpeg_dir):
    register_heif_opener()
    image = Image.open(heic_dir)
    image.save(jpeg_dir, "JPEG")


def remove_background(jpeg_dir, path_to_clean_image):
    if jpeg_dir.lower().endswith('heic'):
        jpeg_dir = jpeg_dir[:-4] + 'jpg'
        heic_to_jpeg(jpeg_dir + 'c', jpeg_dir)

    img = cv2.imread(jpeg_dir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 20, 80], dtype="uint8")
    upper = np.array([50, 255, 255], dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    _, g, _ = cv2.split(result)
    ret, mask = cv2.threshold(g.copy(), 10, 255, 1)

    img[mask == 255] = 255
    cv2.imwrite(path_to_clean_image, img)


def resize(path_to_warped_image, path_to_warped_image_clean, path_to_warped_image_mini, path_to_warped_image_clean_mini, resize_value):
    pil_img = Image.open(path_to_warped_image)
    pil_img_clean = Image.open(path_to_warped_image_clean)

    pil_img.resize((resize_value, resize_value), resample=Image.NEAREST).save(path_to_warped_image_mini)
    pil_img_clean.resize((resize_value, resize_value), resample=Image.NEAREST).save(path_to_warped_image_clean_mini)


import textwrap

def save_result(im, contents, resize_value, path_to_result):
    if im is None:
        print_error()
        return

    heart_content_1, heart_content_2, head_content_1, head_content_2, life_content_1, life_content_2 = contents
    image_height, image_width = im.size
    fontsize = 44  # slightly reduced for better wrapping
    wrap_width = 70  # how many characters per line before wrapping

    # Wrap content
    def wrap(text): return "\n".join(textwrap.wrap(text, wrap_width))

    plt.figure(figsize=(35, 40))  # increased size to handle more text
    plt.imshow(im)
    plt.tick_params(
        axis='both',
        which='both',
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False
    )

    y_offset = 15
    spacing = 30  # vertical spacing between blocks

    # Heart Line
    plt.text(image_width + 15, y_offset,
             f"Heart line ({wrap(heart_content_1)})", color='r', fontsize=fontsize)
    plt.text(image_width + 15, y_offset + 55,
             wrap(heart_content_2), fontsize=fontsize)
    y_offset += spacing + 60

    # Head Line
    plt.text(image_width + 15, y_offset,
             f"Head line ({wrap(head_content_1)})", color='g', fontsize=fontsize)
    plt.text(image_width + 15, y_offset + 55,
             wrap(head_content_2), fontsize=fontsize)
    y_offset += spacing + 60

    # Life Line
    plt.text(image_width + 15, y_offset,
             f"Life line ({wrap(life_content_1)})", color='b', fontsize=fontsize)
    plt.text(image_width + 15, y_offset + 55,
             wrap(life_content_2), fontsize=fontsize)
    y_offset += spacing + 60

    # Notes
    plt.text(image_width + 15, y_offset,
             '* Note: This program is not yet accurately built! Please take the result with a light heart.',
             fontsize=fontsize - 4, color='gray')
    plt.text(image_width + 15, y_offset + 6,
             '   If you want to check out more about palmistry, we recommend reading the below books',
             fontsize=fontsize - 4, color='gray')

    plt.savefig(path_to_result, bbox_inches="tight")
    plt.close()


def print_error():
    print("Palm lines not properly detected! Please use another palm image.")