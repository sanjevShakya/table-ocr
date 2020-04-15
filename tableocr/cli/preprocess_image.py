#!/usr/bin/env python3
""" CLI Tool for the OCR """

import os
import sys
import cv2
from pytesseract import image_to_string

sys.path.insert(0, os.path.abspath(".."))

from clint.arguments import Args
from clint.textui import puts, colored, indent
from util.image_preprocessing import preprocess, binarize, flip_image

args = Args()


def preprocess_image(src, dst, flip=0):
    with indent(4, quote=" > "):
        puts(colored.blue("Processing image: ", str(src)))

    img = cv2.imread(src)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = binarize(img)
    img = preprocess(img)

    if flip:
        img = flip_image(img)

    cv2.imwrite(dst, img)

    with indent(4, quote=" > "):
        puts(colored.green("Output: " + dst))


if __name__ == "__main__":
    if not args:
        with indent(4, quote=" > "):
            puts(colored.red("No argument passed. Use --help for help."))
    else:
        puts(colored.green(str(args)))

        if args.flags[0] == "--help":
            with indent(4, quote=" > "):
                puts(colored.blue("Welcome to OCR CLI tool"))
                puts(colored.blue("Usage:"))
                puts(colored.blue("--preprocess <URL of image>"))
                puts(colored.blue("--preprocess <URL of image> --flip"))
                puts(colored.blue("--preprocess <URL of image> -o <Output path>"))
                puts(colored.blue("--binarize <URL of image>"))
                puts(colored.blue("--binarize <URL of image> -o <Output path>"))
                puts(colored.blue("--extract <URL of image> "))
                puts(
                    colored.blue(
                        "--extract <URL of image> -l <lang: eng | nep> [Install language pack like: yum install tesseract-langpack-nep]"
                    )
                )
                puts(colored.blue("--extract <URL of image> --preprocess"))
                puts(colored.blue("--extract <URL of image> --flip"))
                puts(colored.blue("--extract <URL of image> --preprocess --flip"))

        elif args.flags[0] == "--preprocess" and args.files:
            img_src = args.files[0]
            with indent(4, quote=" > "):
                puts(colored.blue("Preprocessing image " + str(img_src)))
            img = cv2.imread(img_src)
            img = preprocess(img, rotate=-90)

            if "--flip" in str(args.flags):
                img = flip_image(img)

            if dict(args.grouped).get("-o"):
                cv2.imwrite(str(dict(args.grouped).get("-o")[0]), img)
            else:
                cv2.imshow("Processed", img)
                cv2.waitKey()

        elif args.flags[0] == "--binarize" and args.files:
            img_src = args.files[0]
            with indent(4, quote=" > "):
                puts(colored.blue("Binarizing image " + str(img_src)))
            img = cv2.imread(img_src)
            img = binarize(img)

            if dict(args.grouped).get("-o"):
                cv2.imwrite(str(dict(args.grouped).get("-o")[0]), img)
            else:
                cv2.imshow("Binarized", img)
                cv2.waitKey()

        elif args.flags[0] == "--extract" and args.files:
            img_src = args.files[0]
            with indent(4, quote=" > "):
                puts(colored.blue("Extracting image " + str(img_src)))
            img = cv2.imread(img_src)

            if "--preprocess" in str(args.flags):
                img = preprocess(img)
                img = preprocess(img, rotate=-90)

            if "--flip" in str(args.flags):
                img = flip_image(img)

            if dict(args.grouped).get("-l"):
                txt = image_to_string(img, lang=str(dict(args.grouped).get("-l")[0]))
            else:
                txt = image_to_string(img, lang="eng")
            with indent(4, quote=" > "):
                puts(colored.green(str(txt)))

        elif args.files:
            if len(args.all) < 2:
                with indent(4, quote=" > "):
                    puts(
                        colored.red(
                            "Output location is required as second argument. Use --help for help."
                        )
                    )
            elif "--flip" in str(args.flags):
                preprocess_image(args.files[0], args.all[1], flip=1)
            else:
                preprocess_image(args.files[0], args.all[1])

        else:
            with indent(4, quote=" > "):
                puts(colored.red("Invalid arguments. Use --help for help."))
