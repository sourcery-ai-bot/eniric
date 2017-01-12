#!/usr/bin/python
# Script to perform a convolution on a spectrum.
# Can take a number of parameters if needed
from __future__ import division, print_function
from eniric.nIRanalysis import convolve_spectra
from eniric.resample import resampler

import argparse


def _parser():
    """Take care of all the argparse stuff.

    :returns: the args
    """
    parser = argparse.ArgumentParser(description='Helpful discription')
    parser.add_argument('startype', help='Spectral Type e.g "MO"', type=str, nargs="+")
    parser.add_argument("-v", "--vsini", help="Rotational velocity of source",
                        type=float, nargs="+")
    parser.add_argument("-R", "--resolution", help="Observational resolution",
                        type=float, nargs="+")
    parser.add_argument("-b", "--band", type=str, default="ALL",
                        choices=["ALL", "VIS", "GAP", "Z", "Y", "J", "H", "K"],
                        help="Wavelength band to select", nargs="+")
    parser.add_argument('-d', '--data_dir', help='Data directory', type=str, default=None)
    parser.add_argument('--sample_rate', default=[3.0], type=float, nargs="+",
                        help="Resample rate, pixels per FWHM. Default=3.0")
    parser.add_argument('--results', default=None, type=str,
                        help='Result directory Default=data_dir+"/../"')
    parser.add_argument('--resamples', default=None, type=str,
                        help='Resample directory. Default=data_dir+"/../"')
    parser.add_argument('--noresample', help='Resample output', default=False,
                        action="store_true")
    parser.add_argument('--normalize', help='Normalize for wavelength step', default=False,
                        action="store_true")

    args = parser.parse_args()
    return args

def get_spectrum_name(startype, logg="4.50", feh="0.0"):
    """ Return correct spectrum filename for a given spectral type.

    Ability to add logg and metalicity (feh) later on
    """

    temps = {"M0": "03900", "M3": "03500", "M6": "02800", "M9": "02600"}
    base = "PHOENIX-ACES-AGSS-COND-2011-HiRes_wave.dat"
    if startype in temps.keys():
        spectrum_name = "PHOENIX-ACES_spectra/lte{0}-{1}-{2}.{3}".format(temps[startype], logg, feh, base)
        # spectrum_name = "PHOENIX-ACES_spectra/Z-{2}/lte{0}-{1}-{2}.{3}".format(temps[startype], logg, feh, base)
    else:
        raise NotImplemented("This spectral type is not implemented yet")

    return spectrum_name

def main(startype, vsini, resolution, band, data_dir=None, results=None,
         resamples=None, sample_rate=3.0, noresample=False, normalize=False):
    """ Run convolutions of NIR spectra for the range of given parameters.

    Multiple values of startype, vsini, resolution, band, and sample_rate can
    be provided.

    Read files from data_dir + "PHOENIX_ACES_spectra/"
    Saves results to data_dir + "results/"
    Resamples results to data_dir + "resamples/"

    Parameters
    ----------
    startype: list of strings
    vsini: list of floats
    resolution: list of floats
    band: list of strings
    data_dir: str, default=None
    results: str, default=None
    resample: str, default=None
    sample_rate: list of floats default=[3.0]
    noresample: bool default=False
    normalize: bool default=False

    """
        # vsini, resolution, band and sample_rate can all be a series of values

    if data_dir is None:
        data_dir = "../data/"

    if results is None:
        results_dir = data_dir + "results/"
    else:
        results_dir = results

    if resamples is None:
        resampled_dir = data_dir + "resampled/"
    else:
        resampled_dir = resamples

    for star in startype:
        spectrum_name = get_spectrum_name(star)

        for b in band:
            for vel in vsini:
                for R in resolution:
                    for sample in sample_rate:
                        if normalize:
                            # when normalize ation is confirmed then can
                            result_name = "Spectrum_{}-PHOENIX-ACES_{}band_vsini{}_R{}k_conv_normalized.txt".format(star, b, vel, int(R/1000))
                        else:
                            result_name = "Spectrum_{}-PHOENIX-ACES_{}band_vsini{}_R{}k.txt".format(star, b, vel, int(R/1000))
                        print("Name to be result file", result_name)
                        convolve_spectra(data_dir + spectrum_name, b, vel, R, epsilon=0.6, plot=False,
                                         FWHM_lim=5.0, numProcs=None, data_rep=data_dir,
                                         results_dir=results_dir, normalize=normalize, output_name=result_name)

                    # Resample only the file just made
                    if noresample:
                        pass
                    else:
                        resampler(result_name, results_dir=results_dir,
                                   resampled_dir=resampled_dir, sampling=sample)


if __name__ == '__main__':
    args = vars(_parser())
    startype = args.pop("startype")  # positional arguments

    opts = {k: args[k] for k in args}

    main(startype, **opts)
