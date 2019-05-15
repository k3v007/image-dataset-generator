import argparse
import os
import random
import shutil
import sys

from PIL import Image, ImageEnhance


# Argparse
parser = argparse.ArgumentParser(
    description="This is a image-dataset generator program")
parser.add_argument("source", type=str,
                    help='Specify the source folder of images (Required)')
parser.add_argument("-r", "--ratio",  action="store", dest="ratio",
                    type=float, help="Specify validation ratio between [0, 1]. If not specified then ratio = 0.2 is used.")   # noqa
args = parser.parse_args()


# Get full path of the subfolder/subdirectory of a given folder/directory
# (not recursive)
def get_subfolders(folder):
    if os.path.isdir(folder):
        return [os.path.join(folder, dir) for dir in os.listdir(folder)
                if os.path.isdir(os.path.join(folder, dir))]


# add the allowed formats of image
def get_all_images(folder):
    allowed_formats = [".jpg", ".jpeg", ".png"]

    if os.path.isdir(folder):
        return [os.path.join(folder, img) for img in os.listdir(folder)
                if os.path.splitext(img)[1] in allowed_formats]


# returns new image name in destination folder
def img_out(dest_dir, img_count, img_ext=".jpg") -> str:
    path_name = os.path.join(dest_dir, str(img_count) + img_ext)

    return path_name


# source folder location in first argument
src_folder = args.source

# set ratio
if not args.ratio and args.ratio != 0:
    ratio = 0.2
elif not (0 <= args.ratio <= 1):
    sys.exit("[Error]: Not a valid ratio (float). It should be between [0, 1]")    # noqa
else:
    ratio = args.ratio

# check if folder exits to get all subfolders
sub_folders = get_subfolders(src_folder)   # get all subfolder
if not sub_folders:
    sys.exit(print("[ERROR]: Folder doesn't exist or it's empty!"))   # noqa

# create destination folder in same src_folder location
dest_folder = os.path.join(src_folder, "data", "train")
os.makedirs(dest_folder, exist_ok=True)

for sub_folder in sub_folders:
    if os.path.basename(sub_folder).lower() != "data":
        # for Output_images count
        img_count = 1

        # creat same sub-folder in dest_src folder
        dest_dir = os.path.join(dest_folder, os.path.basename(sub_folder))
        os.makedirs(dest_dir, exist_ok=True)

        # get all the image type folders in current sub-folder - bright, dim and normal  # noqa
        itype_folders = get_subfolders(sub_folder)
        for itype_folder in itype_folders:

            # get all images in img_folder
            images = get_all_images(itype_folder)
            for img_path in images:
                img = Image.open(img_path)
                img_ext = os.path.splitext(img_path)[1]

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
                    temp_img.save(img_out(dest_dir, img_count, img_ext))
                    img_count += 1
                    temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(
                        img_out(dest_dir, img_count, img_ext))
                    img_count += 1

                # processing bright images (yellowish type)
                if itype_folder.lower() == "bright":
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
                            temp_img = imgC.enhance(factor).rotate(rot,
                                                                   expand=True)
                            temp_img.save(img_out(dest_dir, img_count, img_ext))  # noqa
                            img_count += 1
                            temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(
                                img_out(dest_dir, img_count, img_ext))
                            img_count += 1

                # processing dim images (having shadow)
                elif itype_folder.lower() == "dim":
                    # fixed brightness and varying contrast
                    imgB = ImageEnhance.Brightness(img).enhance(1.25)
                    imgC = ImageEnhance.Contrast(imgB)

                    # Rotating images
                    for r in range(100, 130, 5):
                        factor = r / 100
                        for rot in range(0, 360, 90):
                            temp_img = imgC.enhance(factor).rotate(rot,
                                                                   expand=True)
                            temp_img.save(img_out(dest_dir, img_count,
                                                  img_ext))
                            img_count += 1
                            temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(
                                img_out(dest_dir, img_count, img_ext))
                            img_count += 1

                # processing normal images (bluish type)
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
                            temp_img = imgB.enhance(factor).rotate(rot,
                                                                   expand=True)
                            temp_img.save(img_out(dest_dir, img_count,
                                                  img_ext))
                            img_count += 1
                            temp_img.transpose(Image.FLIP_LEFT_RIGHT).save(
                                img_out(dest_dir, img_count, img_ext))
                            img_count += 1
                img.close()


# Transfer images from train to validation folder (specify percentage, max set to 20%)  # noqa
src_folder = os.path.join(sys.argv[1], "data", "train")
dest_folder = os.path.join(sys.argv[1], "data", "validation")

os.makedirs(dest_folder, exist_ok=True)
sub_folders = get_subfolders(src_folder)

for sub_folder in sub_folders:
    # set same sub-folder in validation folder
    dest_dir = os.path.join(dest_folder, os.path.basename(sub_folder))
    os.makedirs(dest_dir, exist_ok=True)

    # Get and Move images to validation folder
    images = get_all_images(sub_folder)
    random_images = random.sample(images, k=round(ratio * len(images)))
    for img in random_images:
        shutil.move(img, dest_dir)
