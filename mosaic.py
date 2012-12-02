import os
import random
import itertools
import numpy
import argparse
import shutil

from PIL import Image, ImageOps
from clint.textui import progress, colored


def nearest_neighbour(color, color_data):
    color = color[:3]

    indexes = color_data.keys()
    other_colors = color_data.values()
    colors_array = numpy.array(other_colors)
    distances = numpy.sqrt(((colors_array - color)**2).sum(axis=1))

    images_names = [indexes[idx] for idx in numpy.argsort(distances)]

    color_data.pop(images_names[0])

    return Image.open(images_names[0])


def image_average_color(img):
    array = numpy.asarray(img.getdata())
    return numpy.average(array, axis=0)


def prepare_tiles(size, in_directory, out_directory):
    tiles = {}
    for f in progress.bar(os.listdir(in_directory)):
        try:
            image = Image.open(os.path.join(in_directory, f))
            image = ImageOps.fit(image, (args.size, args.size))
            image.save(os.path.join(out_directory, f), "JPEG")

            tiles[os.path.join(out_directory, f)] = image_average_color(image)
        except IOError:
            print "File '%s' not an image or corrupted, skipping. " % f

    return tiles


def create(args):
    size = args.size
    out_directory = os.path.join(args.in_directory, '.%s_tiles' % size)

    print colored.green("Preparing tiles: re-sizing, cropping and stuff ...")
    out_directory = os.path.join(args.in_directory, '.%s_tiles' % size)

    if not os.path.exists(out_directory):
        os.mkdir(out_directory)

    color_data = prepare_tiles(size, args.in_directory, out_directory)

    print colored.green("Generating mosaic for you ...")

    image = Image.open(open(args.image, "rb"))

    x_range = image.size[0] / size
    y_range = image.size[1] / size

    full_range = [e for e in itertools.product(range(x_range), range(y_range))] #to list
    full_range = random.sample(full_range, len(full_range)) #shuffle

    image_mosaic = Image.new('RGBA', image.size, (0, 0, 0, 0))

    try:
        for x, y in progress.bar(full_range):
            box = (
                x*size,           y*size,
                x*size+size, y*size+size
            )

            color = image_average_color(image.crop(box))
            tile = nearest_neighbour(color, color_data)

            image_mosaic.paste(tile, box)
    finally:
        shutil.rmtree(out_directory)
        image_mosaic.save(args.o, "JPEG")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate some mosaic')
    parser.add_argument('image', type=str)
    parser.add_argument('in_directory', type=str)
    parser.add_argument('size', type=int)
    parser.add_argument('-o', default='mosaic.jpg')

    args = parser.parse_args()

    create(args)
