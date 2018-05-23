#!/usr/bin/env python3
#
# savegame-goggles
#

import os
import argparse

# Read our arguments.
parser = argparse.ArgumentParser(description='utility for managing save files in savegame archives by @dreadpiratepj')
parser.add_argument('-outpath', metavar='outpath', type=str, default=os.getcwd(), help='the path where to write the save files')
parser.add_argument('savegame', metavar='savegame', type=str, help='the savegame archive to process')
parser.add_argument('operation', metavar='operation', type=str, help='the operation to perform on the save files')
parser.add_argument('wildcard', metavar='wildcard', nargs='?', type=str, default='*', help='the wildcard to match the save files on which to operate')
arguments = parser.parse_args()
