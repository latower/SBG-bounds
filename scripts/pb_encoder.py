# -*- coding: utf-8 -*-
"""
This code is adapted from the original file https://github.com/latower/identifying-codes/blob/main/scripts/encoding/ilp_encoding.py,
retrieved in July 2024.

Original author:     Anna L.D. Latour
Author of changes:   Anna L.D. Latour
Creation date:       11 October 2022
Modification date:   18 July 2024
Maintainer:          Anna L.D. Latour
Contact:             a.l.d.latour@tudelft.nl
File:                pb_encoder.py
Description:         Class for encoding an Identifying Codes instance as a
                     pseudo-Boolean formula.
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


import networkx as nx

# Own modules/libraries
from identifying_codes import IdentifyingCodesInstance


class PBEncoder(IdentifyingCodesInstance):

    def __init__(self):
        IdentifyingCodesInstance.__init__(self)
        self._node2var = dict()
        self._var2node = dict()

    def _rename_variables(self):
        self._node2var = {node: idx + 1 for idx, node in enumerate(self._G.nodes())}
        self._var2node = {idx: node for node, idx in self._node2var.items()}

    def _get_renaming_info(self):
        assert len(self._node2var) == len(self._var2node) == self._G.number_of_nodes(), \
            'Something wrong with renaming info.'

        node_name_width = max(len(max(self._node2var.keys())), 10) + 1
        idx_width = len(str(self._G.number_of_nodes())) + 1
        info = [
            f"{'node':<{node_name_width}}{'idx':>{idx_width}}",
            "-" * (node_name_width + idx_width)
        ]
        for node, var in self._node2var.items():
            info.append(f"{node:<{node_name_width}}{var:>{idx_width}}")
        info.append('')
        return info

    def _alo_constraints(self) -> set:
        """
        For each node in the network, at least one node in the closed 1-neigh-
        bourhood of that node must have a sensor. Hence, the sum of the x
        variables corresponding to the nodes in that neighbourhood, must be at
        least k + 1 (fault tolerance).
        :return: set of sets
        """
        alo_csts = set()
        for node in self._G.nodes():
            lhs = frozenset(nx.ego_graph(self._G, node, radius=1, center=True, undirected=True).nodes())
            alo_csts.add((lhs, self._fault_tolerance + 1))
        return alo_csts

    def _unique_constraints(self):
        """
        We must encode that all signatures are unique. This means that for
        every two nodes v and u, at least one x variable corresponding to a node
        in the distinguishing set of v and u must be 1. Hence, the sum of the
        x variables corresponding to the nodes of the distinguishing set of v
        and u must be larger or equal than 1.

        Note that we only have to check the v's and u's that are in each other's
        closed 2-neighbourhoods.
        :return:
        """

        # Do some preprocessing for faster performance
        closed_1_neighbourhoods = {
            node: set(nx.ego_graph(self._G, node, radius=1, center=True, undirected=True).nodes())
            for node in self._G
        }
        closed_2_neighbourhoods = {
            node: set(nx.ego_graph(self._G, node, radius=2, center=True, undirected=True).nodes())
            for node in self._G
        }

        pair2constraint = dict()
        for v in self._G.nodes():
            N2_v = set(closed_2_neighbourhoods[v])
            N1_v = set(closed_1_neighbourhoods[v])
            for u in N2_v:
                pair = tuple(sorted([v, u]))
                if u is not v and pair not in pair2constraint.keys():
                    N1_u = set(closed_1_neighbourhoods[u])
                    distinguishing_set = frozenset(N1_v.symmetric_difference(N1_u))
                    pair2constraint[pair] = distinguishing_set
        left_hand_sides = set(pair2constraint.values())
        return set([(lhs, self._fault_tolerance + 1) for lhs in left_hand_sides])

    def _write_pb_to_opb(self, pb_file, n_vars, n_csts, constraints, header):
        """
        :param n_vars:
        :param n_csts:
        :param constraints:
        :param pb_file:
        :return:
        """

        info = f'* #variable= {n_vars} #constraint= {n_csts}'
        opb = [info] + \
            ['* ' + line for line in header] + \
            constraints
        with open(pb_file, 'w') as ofile:
            ofile.write('\n'.join(opb))

    def encode(self, pb_file):
        # RoundingSAT does not accept arbitrary variable names, so we must do some renaming:
        self._rename_variables()
        assert len(self._node2var) == len(self._var2node), \
            f'Something went wrong while renaming: len(self._node2var) = {len(self._node2var)} and ' \
            f'len(self._var2node) = {len(self._var2node)}'
        assert len(self._node2var) == self._G.number_of_nodes(), \
            f'Something went wrong while renaming: len(self._node2var) = {len(self._node2var)} and ' \
            f'self._G.number_of_nodes() = {self._G.number_of_nodes()}'

        # Get the left-hand-sides of the various constraints
        alo_csts = self._alo_constraints()
        unique_csts = self._unique_constraints()
        csts = alo_csts.union(unique_csts)
        renamed_csts = [([self._node2var[n] for n in lhs], degree) for lhs, degree in csts]

        # Create the PB constraints in the correct format
        pb_csts = [
            ' '.join([f'+1 x{var}' for var in vars]) +
            f' >= {degree} ;' for (vars, degree) in renamed_csts
        ]
        # For the cardinality constraint, we must multiply the LHS and the RHS with -1,
        # so we can turn the '<=' into a '>=', since RoundingSAT only supports
        # '>=' and '=' comparators.
        cardinality_lhs = (self._node2var[n] for n in self._G.nodes())
        pb_csts += [
            ' '.join([f'-1 x{var}' for var in cardinality_lhs]) +
            f' >= {-self._budget} ;'
        ]

        n_vars = self._G.number_of_nodes()
        n_csts = len(pb_csts)
        header = self._get_header()
        header.extend(self._get_renaming_info())

        self._write_pb_to_opb(pb_file, n_vars, n_csts, pb_csts, header)