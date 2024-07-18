#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code is adapted from the original file https://github.com/latower/identifying-codes/blob/main/scripts/encoding/encode_network.py,
retrieved in July 2024.

Original author:     Anna L.D. Latour
Author of changes:   Anna L.D. Latour
Creation date:       15 October 2022
Modification date:   18 July 2024
Maintainer:          Anna L.D. Latour
Contact:             a.l.d.latour@tudelft.nl
File:                encode_network.py
Description:         Script that converts an undirected network into a
                     Pseudo-Boolean formula that encodes an Identifying Code Set
                     problem on that network.
                     Precondition: Input network is undirected and has no twins*.
                     [*] Twins are two distinct nodes v and w, such that their
                     closed neighbourhoods are equal: N+(v) = N+(w).
Version:             0.0.1
Copyright:           (C) 2022 & 2024, Anna L.D. Latour
License:             MIT

Copyright (C) 2022 & 2024 Anna L.D. Latour

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# Generic/Built-in
import argparse
from datetime import datetime
import os
import pathlib
import sys

# Own modules/libraries
from pb_encoder import PBEncoder

parser = argparse.ArgumentParser()
required_args = parser.add_argument_group("Required arguments")
optional_args = parser.add_argument_group("Optional arguments")
required_args.add_argument("--network", "-n", type=str, required=True,
                           help="Path to network file.")
required_args.add_argument("--out_dir", type=str, required=True,
                           help="Path to output directory above k sub directory.")
required_args.add_argument("--out_file", type=str, required=True,
                           help="Basename of output file.")
optional_args.add_argument("-b", type=int, required=False, default=-1,
                           help="Budget.")
optional_args.add_argument("-k", type=int, required=False, default=0,
                           help="Fault tolerance.")
args = parser.parse_args()

SCRIPT_NAME = os.path.basename(__file__)


def log_message(message):
    print(f'[{SCRIPT_NAME}], {datetime.now().strftime("%Y-%m-%d, %Hh%Mm%Ss")}: {message}')


# Build and encode problem
log_message("Initialising PB instance.")

instance = PBEncoder()
build_successful = True

log_message(f"Parsing network {args.network}.")
sys.stdout.flush()

try:
    instance.build_from_file(args.network, budget=args.b, fault_tolerance=args.k)
    log_message("Building completed.")
except Exception as exc:
    build_successful = False
    log_message("Building FAILED.")
    log_message(exc)
sys.stdout.flush()

if build_successful:
    log_message(f"Encoding {args.network} with budget {args.b} into a set of PB constraints.")
    pathlib.Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    try:
        instance.encode(f"{args.out_dir}/{args.out_file}")
        log_message(f"Encoding completed! Written to {args.out_dir}/{args.out_file}.")
    except Exception as exc:
        log_message("Encoding FAILED.")
        log_message(exc)
else:
    log_message("Building failed. Aborting rest of the process.")

sys.stdout.flush()

log_message("Done!")
