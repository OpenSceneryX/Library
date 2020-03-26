# -*- coding: utf-8 -*-
# Script to walk through objects and calculate their dimensions, saving these into the associated info.txt file
# Copyright (c) 2019 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.

import getopt
import os
import subprocess
import re
import shutil
import sys
import traceback
import urllib

import classes
import functions

widthPattern = re.compile(r"^Width:\s+(.*)$", re.MULTILINE)
heightPattern = re.compile(r"^Height:\s+(.*)$", re.MULTILINE)
depthPattern = re.compile(r"^Depth:\s+(.*)$", re.MULTILINE)
descPattern = re.compile(r"^=+\n(Description|Note):", re.MULTILINE)

def main(argv):
    startPath = ''

    try:
        opts, args = getopt.getopt(argv,"hp:",["path="])
    except getopt.GetoptError:
        print ('process_objest_dimensions.py -p <path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('process_objest_dimensions.py -p <path>')
            sys.exit()
        elif opt in ("-p", "--path"):
            startPath = arg

    functions.displayMessage("============================\n")
    functions.displayMessage("Processing Object Dimensions\n")
    functions.displayMessage("============================\n")

    if startPath == '':
        print ('process_objest_dimensions.py -p <path>')
        sys.exit()

    for root, dirs, files in os.walk(startPath):
        for file in files:
            if file == "object.obj":
                # CLITool is a specially-written command-line tool, using Laminars xptools: https://github.com/aussig/xptools/tree/feature/clitool
                output = subprocess.run(["./CLITool", "--measure", os.path.join(root, file)], capture_output=True)
                x, y, z = tuple(output.stdout.decode(encoding='UTF-8').split(","))
                x = round(float(x), 1)
                y = round(float(y), 1)
                z = round(float(z), 1)

                infoFile = open(os.path.join(root, "info.txt"), "r+")
                infoFileContents = infoFile.read()

                infoX = infoY = infoZ = -1

                result = widthPattern.search(infoFileContents)
                if result:
                    try:
                        infoX = float(result.group(1))
                    except ValueError:
                        infoX = -2

                result = heightPattern.search(infoFileContents)
                if result:
                    try:
                        infoY = float(result.group(1))
                    except ValueError:
                        infoY = -2

                result = depthPattern.search(infoFileContents)
                if result:
                    try:
                        infoZ = float(result.group(1))
                    except ValueError:
                        infoZ = -2

                if x != infoX or y != infoY or z != infoZ:
                    print(os.path.join(root, file))
                    print("Mismatch:\n")
                    print(f"  From file: x: {x} y: {y} z: {z}")
                    print(f"  From info: x: {infoX} y: {infoY} z: {infoZ}")

                    if infoX != -1:
                        # Width already in info.txt, modify it
                        print("  Replacing x")
                        infoFileContents = widthPattern.sub(f"Width: {x}", infoFileContents)
                    else:
                        # Width missing from info.txt, insert it
                        infoFileContents = descPattern.sub(fr"Width: {x}\n=====================\n\1:", infoFileContents, 1)

                    if infoY != -1:
                        # Height already in info.txt, modify it
                        print("  Replacing y")
                        infoFileContents = heightPattern.sub(f"Height: {y}", infoFileContents)
                    else:
                        # Height missing from info.txt, insert it
                        infoFileContents = descPattern.sub(fr"Height: {y}\n=====================\n\1:", infoFileContents, 1)

                    if infoZ != -1:
                        # Depth already in info.txt, modify it
                        print("  Replacing z")
                        infoFileContents = depthPattern.sub(f"Depth: {z}", infoFileContents)
                    else:
                        # Depth missing from info.txt, insert it
                        infoFileContents = descPattern.sub(fr"Depth: {z}\n=====================\n\1:", infoFileContents, 1)

                    infoFile.seek(0)
                    infoFile.write(infoFileContents)
                    infoFile.truncate()

                else:
                    # Everything matches, no need to make changes
                    print("Match")

                infoFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])
