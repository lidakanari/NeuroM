#!/usr/bin/env python

# Copyright (c) 2015, Ecole Polytechnique Federale de Lausanne, Blue Brain Project
# All rights reserved.
#
# This file is part of NeuroM <https://github.com/BlueBrain/NeuroM>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from neurom.io import utils
from neurom import stats
import os
import glob
import comparison
import argparse
import numpy as np

def parse_args():
    '''Parse command line arguments'''
    parser = argparse.ArgumentParser(
        description='Summary of morphometrical comparison between neurons')

    parser.add_argument('datapath',
                        help='Path to morphology data directory')

    parser.add_argument('output',
                        help='Path to figures output directory')

    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()

    data_directory = args.datapath
    output_directory = args.output

    # Definition of Data according to BigNeuron distribution

    gs = glob.glob(data_directory + '00*')[0] # Manual reconstruction
    autorec = glob.glob(data_directory + '*.swc')   # All data
    autorec.remove(gs) # Automatic reconstructions

    ngs = utils.load_trees(gs)
    scores = np.zeros(len(autorec))

    for ear, ar in enumerate(autorec):
        try:
            nar = utils.load_trees(ar)
            if len(nar) > 0:
                try:
                    all_f = comparison.get_features(ngs, nar)
                    score = np.abs(1 - stats.total_score(all_f)/len(all_f))
                    print ar, score
                    comparison.boxplots(all_f, output_path=output_directory,
                                        name='('+ar.split('/')[-1][:2]+')'+ar.split('/')[-1].split('.')[1],
                                        output_name=str("{0:.3f}".format(score)), show_plot=False)
                except:
                    print 'Failed on ', ar
        except:
            print 'Failed to load: ' + ar
