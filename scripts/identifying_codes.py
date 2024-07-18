# -*- coding: utf-8 -*-
"""
This code is adapted from the original file https://github.com/latower/identifying-codes/blob/main/scripts/encoding/identifying_codes.py,
retrieved in July 2024.

Original author:     Anna L.D. Latour
Author of changes:   Anna L.D. Latour
Creation date:       22 April 2022
Modification date:   18 July 2024
Maintainer:          Anna L.D. Latour
Contact:             a.l.d.latour@tudelft.nl
File:                identifying_codes.py
Description:         Class for creating and manipulating Identifying Codes
                     problem instances.
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
import sys
from datetime import datetime
import os
import socket
import subprocess

# Other libs
import networkx as nx


THIS_DIR = os.getcwd()
REPO_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
SCRIPT_NAME = os.path.basename(__file__)


def log_message(message):
    print(f'[{SCRIPT_NAME}], {datetime.now().strftime("%Y-%m-%d, %Hh%Mm%Ss")}: {message}')
    sys.stdout.flush()


def _get_repo_info(repo_dir: str) -> dict:
    try:
        res = subprocess.check_output(
            f'git --git-dir {repo_dir}/.git config --get remote.origin.url',
            stderr=subprocess.STDOUT, shell=True)
        repo = res.decode()[:-1]
    except subprocess.CalledProcessError as grepexc:
        log_message(f"Error while retrieving remote url: {grepexc.returncode} {grepexc.output}")
        repo = 'None'
    try:
        res = subprocess.check_output(
            f"git --git-dir {repo_dir}/.git branch | grep '*'",
            stderr=subprocess.STDOUT, shell=True)
        branch = res.decode()[2:-1]
    except subprocess.CalledProcessError as grepexc:
        log_message(f"Error while retrieving branch: {grepexc.returncode} {grepexc.output}")
        branch = 'None'
    try:
        res = subprocess.check_output(
            f'git --git-dir {repo_dir}/.git log --format="%H" -n 1',
            stderr=subprocess.STDOUT, shell=True)
        commit = res.decode()[:-1]
    except subprocess.CalledProcessError as grepexc:
        log_message(f"Error while retrieving commit: {grepexc.returncode} {grepexc.output}")
        commit = 'None'
    return {'repo': repo, 'branch': branch, 'commit': commit}


class IdentifyingCodesInstance:
    def __init__(self):

        self._network_file = None
        self._budget = None
        self._fault_tolerance = None

        self._G = None
        self._record_renaming = True
        self._node_2_label = dict()
        self._label_2_node = dict()

        self._n_vars = None

    def build_from_file(self,
                        network_file: str,
                        budget=-1,
                        fault_tolerance=0):
        """
        :param network_file:  edge list or mtx file describing a network
        :param budget:        maximum number of sensors to place
        :return:              None
        """

        self._network_file = network_file
        self._create_from_edge_list()
        self._n_vars = self._G.number_of_nodes()
        self._budget = budget
        self._fault_tolerance = fault_tolerance

    def _create_from_edge_list(self):
        with open(self._network_file, 'r') as infile:
            edges = [tuple(line.split()[:2])
                     for line in infile.readlines()
                     if not (line.startswith('#') or line.startswith('%'))]
            self._G = nx.Graph()
            self._G.add_edges_from(edges)

    def _get_header(self):
        """
        :return:         List of strings, each string a line in the header
        """
        repo_dict = _get_repo_info(REPO_DIR)
        repo = repo_dict['repo']
        branch = repo_dict['branch']
        commit = repo_dict['commit']
        python_version = sys.version.replace("\n"," ")
        networkx_version = nx.__version__
        header = [
            '',
            'PROBLEM DATA',
            '------------',
            f'Network file:      {self._network_file}',
            f'Number of nodes:   {self._G.number_of_nodes()}',
            f'Number of edges:   {self._G.number_of_edges()}',
            f'Budget:            {self._budget}',
            '', '',
            'REPRODUCIBILITY INFO',
            '--------------------',
            f'Python version:    {python_version}',
            f'Networkx version:  {networkx_version}',
            f'Date (YYYY-MM-DD): {datetime.now().strftime("%Y-%m-%d")}',
            f'Repository:        {repo}',
            f'Branch:            {branch}',
            f'Commit:            {commit}',
            f'Machine:           {socket.gethostname()}',
            ''
        ]
        return header





