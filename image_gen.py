import os
import sys

from PIL import Image, ImageEnhance


def img_out(img_ext=".jpg") -> str:
    global img_count
    path_name = os.path.join(dest_folder, str(img_count) + img_ext)
    img_count += 1
    return path_name


plant = sys.argv[1]
disease_folder = os.path.join("tests", "data", plant, sys.argv[2])
try:
    img_folders = os.listdir(disease_folder)
except Exception as e:
    print(e)

dest_folder = os.path.join("data", "train", sys.argv[2])
if not os.path.exists(dest_folder):
    os.mkdir(dest_folder)

# Output images count
img_count = 1

# get all the folder in current disease imgaes - yellowish, bluish
for img_type in img_folders:
    img_folder = os.path.join(disease_folder, img_type)
    print(img_folder)

    # get all images in img_folder
    images = os.listdir(img_folder)

    # process all the images
    for image in images:
        img_path = os.path.join(img_folder, image)
        img = Image.open(img_path)
        img_ext = os.path.splitext(image)[1]

        # # Imgae filters:
        # img = img.filter(ImageFilter.SMOOTH)
        # img = img.filter(ImageFilter.DETAIL)

        # Resizing images close to 225 x 225
        img_x, img_y = img.size
        min_dim = min(img_x, img_y)
        r_factor = 225 / min_dim
        img_x = round(img_x * r_factor)
        img_y = round(img_y * r_factor)
        img = img.resize((img_x, img_y))

        # Rotating original images
        for rot in range(0, 360, 90):
            temp_img = img.rotate(rot, expand=True)
            temp_img.save(img_out())
            temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(img_out())

        # processing bright images (yellowish type)
        if img_type.lower() == "bright":
            # setting rgb color for morning/evening images (yellowish)
            for y in range(img_y):
                for x in range(img_x):
                    r, g, b = img.getpixel((x, y))
                    r -= 20
                    g -= 20
                    b += 20
                    img.putpixel((x, y), (r, g, b))

            # fixed brightness and varying contrast
            imgB = ImageEnhance.Brightness(img).enhance(0.8)
            imgC = ImageEnhance.Contrast(imgB)

            # Rotating images
            for r in range(100, 150, 10):
                factor = r / 100

                for rot in range(0, 360, 90):
                    temp_img = imgC.enhance(factor).rotate(rot, expand=True)
                    temp_img.save(img_out())
                    temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(img_out())

        # processing dim images (having shadow)
        elif img_type.lower() == "dim":
            # fixed brightness and varying contrast
            imgB = ImageEnhance.Brightness(img).enhance(1.25)
            imgC = ImageEnhance.Contrast(imgB)

            # Rotating images
            for r in range(100, 130, 5):
                factor = r / 100

                for rot in range(0, 360, 90):
                    temp_img = imgC.enhance(factor).rotate(rot, expand=True)
                    temp_img.save(img_out())
                    temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(img_out())

        # processing normal images (blusih type)
        else:
            # setting rgb color for normal image
            for y in range(img_y):
                for x in range(img_x):
                    r, g, b = img.getpixel((x, y))
                    r += 5
                    g -= 5
                    b -= 10
                    img.putpixel((x, y), (r, g, b))

            # fixed brightness and varying contrast
            imgC = ImageEnhance.Contrast(img).enhance(0.9)
            imgB = ImageEnhance.Brightness(imgC)
            for r in range(90, 120, 5):
                factor = r / 100

                for rot in range(0, 360, 90):
                    temp_img = imgB.enhance(factor).rotate(rot, expand=True)
                    temp_img.save(img_out())
                    temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(img_out())

        img.close()
