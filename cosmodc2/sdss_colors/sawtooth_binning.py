""" Functions used to set up overlapping bin boundaries
"""
import numpy as np


__all__ = ('sawtooth_bin_indices', )


def sawtooth_bin_indices(x, bin_edges, min_counts=2):
    """ Function assigns each element of the input array `x` to a particular bin number.

    The bin boundaries have hard edges, but bin-assignment is probabilistic, such that
    when a point in `x` is halfway between two edges, is equally likely to be assigned
    to the bin to its left or right.

    The `sawtooth_bin_indices` function optionally enforces that elements of very sparsely
    populated bins are remapped to the nearest bin with more than `min_counts` elements.

    Parameters
    ----------
    x : ndarray
        Numpy array of shape (npts, ) storing the values to be binned

    bin_edges : ndarray
        Numpy array of shape (nbins, ) defining the binning scheme.
        The values of `bin_edges` must strictly encompass the range of values spanned by `x`.

    min_counts : int, optional
        Minimum required number of elements in a bin. For those bins not satisfying this requirement,
        all their elements will be reassigned to the nearest sufficiently populated bin.
        Default is two.

    Returns
    -------
    bin_indices : ndarray
        Numpy integer array of shape (npts, ) storing the bin number to which elements of `x`
        are assigned. All values of `bin_indices` will be between 0 and nbins-1, inclusive.
    """
    assert bin_edges[0] < x.min(), "smallest bin must be less than smallest element in x"
    assert bin_edges[-1] > x.max(), "largest bin must be less than largest element in x"

    npts_x = len(x)
    num_bin_edges = len(bin_edges)
    a = np.arange(npts_x)
    bin_indices = np.zeros_like(x).astype(int)-999
    for i, low, high in zip(np.arange(num_bin_edges).astype(int), bin_edges[:-1], bin_edges[1:]):
        bin_mask = (x >= low) & (x < high)

        npts_bin = np.count_nonzero(bin_mask)
        if npts_bin > 0:
            bin_indices[bin_mask] = i+1

            prob_low = np.interp(x[bin_mask], [1, 0], [low, high])
            p = prob_low/np.sum(prob_low)
            bin_rows = a[bin_mask]
            low_bin_selection = np.random.choice(bin_rows, size=npts_bin/2, p=p, replace=False)
            bin_indices[low_bin_selection] = i

    bin_indices[bin_indices == -999] = 0

    return enforce_bin_counts(bin_indices, min_counts)


def enforce_bin_counts(bin_indices, min_counts):
    """ Function enforces that each entry of `bin_indices` appears at least `min_counts` times.
    For entries not satisfying this requirement, the nearest index of a sufficiently populated bin
    will be used as a replacement.

    Parameters
    ----------
    bin_indices : ndarray
        Numpy integer array storing bin numbers

    min_counts : int
        Minimum acceptable number of elements per bin

    Returns
    -------
    output_bin_inidices : ndarray
        Numpy integer array storing bin numbers after enforcing the population requirement.
    """
    output_bin_indices = np.copy(bin_indices)
    unique_bin_numbers, counts = np.unique(bin_indices, return_counts=True)
    for i, bin_number, count in zip(np.arange(len(counts)), unique_bin_numbers, counts):
        new_bin_number = _find_nearest_populated_bin_number(
            counts, unique_bin_numbers, i, min_counts)
        if new_bin_number != bin_number:
            output_bin_indices[bin_indices==bin_number] = new_bin_number
    return output_bin_indices


def _find_nearest_populated_bin_number(counts, bin_numbers, bin_index, min_counts):
    """ Helper function used by the `enforce_bin_counts` function.
    """
    bin_numbers = np.atleast_1d(bin_numbers)
    bin_indices = np.arange(len(bin_numbers))
    counts = np.atleast_1d(counts)
    msg = "Must have at least one bin with greater than {0} elements"
    assert np.any(counts >= min_counts), msg.format(min_counts)

    counts_mask = counts >= min_counts
    available_bin_numbers = bin_numbers[counts_mask]
    available_indices = bin_indices[counts_mask]

    return available_bin_numbers[np.argmin(np.abs(available_indices - bin_index))]


