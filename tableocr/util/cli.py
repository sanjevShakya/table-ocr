#!/usr/bin/env python3
""" CLI Tool for the OCR """

import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(".."))

from clint.arguments import Args
from clint.textui import puts, colored, indent
from preprocessing import preprocess

args = Args()

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
                puts(colored.blue("--preprocess <URL of image> -o <Output path>"))

        elif args.flags[0] == "--preprocess" and args.files:
            img_src = args.files[0]
            with indent(4, quote=" > "):
                puts(colored.blue("Preprocessing image " + str(img_src)))
            img = cv2.imread(img_src)
            img = preprocess(img)

            if dict(args.grouped).get("-o"):
                cv2.imwrite(str(dict(args.grouped).get("-o")[0]), img)
            else:
                cv2.imshow("Processed", img)
                cv2.waitKey()

        else:
            with indent(4, quote=" > "):
                puts(colored.red("Invalid arguments. Use --help for help."))
