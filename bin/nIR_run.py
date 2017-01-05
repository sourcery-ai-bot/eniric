#!/usr/bin/python
# Script to perform a convolution on a spectrum.
# Can take a number of parameters if needed
from __future__ import division, print_function
from eniric.nIRanalysis import convolution, resample_allfiles

import argparse


def _parser():
    """Take care of all the argparse stuff.

    :returns: the args
    """
    parser = argparse.ArgumentParser(description='Helpful discription')
    parser.add_argument('spectrum', help='Spectrum name', dtype=str)
    parser.add_argument("-v", "--vsini",  help="Rotational velocity of source", dtype(float))
    parser.add_argument("-R", "--resolution",  help="Observational resolution", dtype(float))
    parser.add_argument("-b", "--band", dtype=str, default="ALL",
                        choices=["ALL", "VIS", "GAP", "Z", "Y", "J", "H", "K"],
                        help="Wavelength band to select")
    parser.add_argument('-d', '--data_dir', help='Data directory', dtype=str)
    parser.add_argument('--sample_rate', default=3.0, dtype=float,
                        help="Resample rate, pixels per FWHM. Default=3.0")
    parser.add_argument('--results', default=None, dtype=str,
                        help='Result directory Default=data_dir+"/../"')
    parser.add_argument('--resamples', default=None, dtype=str
                        help='Resample directory. Default=data_dir+"/../"')
    parser.add_argument('--noresample', help='Resample output', default=True,
                        action="store_false")

    args = parser.parse_args()
    return args

def main(spectrum, vsini, resolution, band, data_dir=None, results=None,
         resamples=None, sample_rate=3.0, noresample=False):

        # vsini, resolution, band and sample_rate can all be a series of values
    pass



if __name__ == '__main__':
    args = vars(_parser())
    spectrum_name = args.pop('spectrum')  # positional arguments

    opts = {k: args[k] for k in args}

    main(spectrum_name, **opts)