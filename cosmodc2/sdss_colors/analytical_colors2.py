"""
Module storing the analytical model for SDSS restframe colors
"""
import numpy as np
from astropy.utils.misc import NumpyRNGContext
from halotools.empirical_models import conditional_abunmatch


__all__ = ('gr_ri_monte_carlo',)


default_red_peak_gr = [0.9, 0.85, 0.8, 0.7, 0.7, 0.7]
default_red_peak_ri = [0.41, 0.41, 0.4, 0.385, 0.375, 0.35, 0.31]
red_peak_ri_abscissa = [-23, -21, -20., -19.5, -19.0, -18.0, -15.]

ms_peak_gr_abscissa = [-22.5, -21, -20, -19, -18, -15]
ms_peak_ri_abscissa = [-22.5, -21, -20, -19, -18, -15]
default_ms_peak_ri = [0.4, 0.35, 0.3, 0.24, 0.2, 0.185]
default_ms_peak_gr = [0.8, 0.75, 0.6, 0.4, 0.4, 0.35]
red_peak_gr_abscissa = ms_peak_gr_abscissa
red_peak_ri_abscissa = ms_peak_ri_abscissa

fq_gr_abscissa = [-22.5, -22., -21, -20, -19.5, -19, -18.5, -18, -15]
default_fq_gr = [0.9, 0.775, 0.6, 0.55, 0.525, 0.50, 0.25, 0.2, 0.1]

fq_ri_abscissa = [-25, -22.5, -21, -20, -19.5, -19, -18.5, -18, -15]
default_fq_ri = [0.9, 0.8, 0.65, 0.60, 0.465, 0.35, 0.2, 0.1, 0.1]

blueshift_z_table = [0.25, 0.5, 1.0]
default_fq_gr_blueshift_table = (1., 1.5, 3.)
default_fq_ri_blueshift_table = (1., 1.5, 3.)

default_peak_shift_factor_gr = [0, -0.1, -0.3, -0.35]
default_peak_shift_factor_ri = [0, -0.1, -0.2, -0.2]
peak_shift_factor_z_table = [0.1, 0.25, 0.5, 1]
default_ms_peak_gr_zevol = [0, -0.1, -0.3, -0.35]
default_ms_peak_ri_zevol = [0, -0.1, -0.2, -0.2]

default_red_peak_gr_zevol = [0, -0.05, -0.1, -0.1]


def apply_z_evolution_of_fq(fq_z0p0, redshift, z_table, reduction_factor):
    """
    """
    reduction_factor = np.interp(redshift, z_table, reduction_factor)
    result = fq_z0p0/reduction_factor
    return np.where(result < 0, 0., result)


def sequence_width(magr, x, y):
    """ Numpy kernel used to fit a 2-degree polynomial to an input
    data table storing the level of scatter in Mr at fixed Mr.
    """
    c2, c1, c0 = np.polyfit(x, y, deg=2)
    result = c0 + c1*magr + c2*magr**2

    #  Now clip endpoints
    xmin, xmax = np.min(x), np.max(x)
    faint_edge_value = c0 + c1*xmax + c2*xmax**2
    bright_edge_value = c0 + c1*xmin + c2*xmin**2
    result = np.where(magr > xmax, faint_edge_value, result)
    result = np.where(magr < xmin, bright_edge_value, result)
    return result


def sequence_peak(magr, x, y):
    """ Numpy kernel used to fit a 2-degree polynomial to an input
    data table storing the median value <color | Mr>.
    """
    c2, c1, c0 = np.polyfit(x, np.log(y), deg=2)
    result = np.exp(c0 + c1*magr + c2*magr**2)

    #  Now clip endpoints
    xmin, xmax = np.min(x), np.max(x)
    faint_edge_value = np.exp(c0 + c1*xmax + c2*xmax**2)
    bright_edge_value = np.exp(c0 + c1*xmin + c2*xmin**2)
    result = np.where(magr > xmax, faint_edge_value, result)
    result = np.where(magr < xmin, bright_edge_value, result)
    return result


def redshift_evolution_factor(magr, redshift, z_table, shift_table):
    """ Function responsible for modulating the redshift-dependence
    of the relation <Mr | M*>(z) by an overall multiplicative factor.
    The multiplicative factor is determined by linearly interpolating from
    the set of input points in redshift.
    """
    return np.interp(redshift, z_table, shift_table)


def ms_peak_gr_zevol_factor(redshift, shift_table, z_table=peak_shift_factor_z_table):
    """ Function responsible for modulating the redshift-dependence
    of the relation <Mr | M*>(z) by an overall multiplicative factor.
    The multiplicative factor is determined by linearly interpolating from
    the set of input points in redshift.
    """
    return np.interp(redshift, z_table, shift_table)


def red_peak_gr_zevol_factor(redshift, shift_table, z_table=peak_shift_factor_z_table):
    """ Function responsible for modulating the redshift-dependence
    of the relation <Mr | M*>(z) by an overall multiplicative factor.
    The multiplicative factor is determined by linearly interpolating from
    the set of input points in redshift.
    """
    return np.interp(redshift, z_table, shift_table)


def red_sequence_width_gr(magr, red_scatter_gr,
        x=[-22.5, -21, -20, -18, -15]):
    """
    Level of scatter about the median value of <g-r | Mr> for red sequence galaxies.
    """
    return sequence_width(magr, x, red_scatter_gr)


def main_sequence_width_gr(magr, ms_scatter_gr,
        x=[-22.5, -21, -20, -18, -15]):
    """
    Level of scatter about the median value of <g-r | Mr> for star-forming galaxies.
    """
    return sequence_width(magr, x, ms_scatter_gr)


def red_sequence_peak_gr(magr, red_peak_gr,
        x=[-22.5, -21, -20, -19, -18, -15]):
    """
    Location of the median value of <g-r | Mr> for red sequence galaxies.
    """
    return sequence_peak(magr, x, red_peak_gr)


def red_sequence_peak_gr2(magr, red_peak_gr, redshift, red_gr_shift_table, x=red_peak_gr_abscissa):
    """
    Location of the median value of <g-r | Mr> for star-forming galaxies.
    """
    z0_peak = sequence_peak(magr, x, red_peak_gr)
    zevol_factor = red_peak_gr_zevol_factor(redshift, red_gr_shift_table)
    return z0_peak + zevol_factor


def main_sequence_peak_gr(magr, ms_peak_gr, x=[-22.5, -21, -20, -19, -18, -15]):
    return sequence_peak(magr, x, ms_peak_gr)


def main_sequence_peak_gr2(magr, ms_peak_gr, redshift, ms_gr_shift_table, x=ms_peak_gr_abscissa):
    """
    Location of the median value of <g-r | Mr> for star-forming galaxies.
    """
    z0_peak = sequence_peak(magr, x, ms_peak_gr)
    zevol_factor = ms_peak_gr_zevol_factor(redshift, ms_gr_shift_table)
    return z0_peak + zevol_factor


def quiescent_fraction_gr(magr, redshift, fq_gr, blueshift_factor):
    """
    Fraction of galaxies on the g-r red sequence as a function of Mr.
    """
    fq_z0 = np.interp(magr, fq_gr_abscissa, fq_gr)
    return apply_z_evolution_of_fq(fq_z0, redshift, blueshift_z_table, blueshift_factor)


def g_minus_r(magr, redshift, seed=None, z_table=peak_shift_factor_z_table,
            peak_shift_factor_gr=default_peak_shift_factor_gr,
            fq_gr=default_fq_gr,
            red_peak_gr=default_red_peak_gr,
            ms_peak_gr=default_ms_peak_gr,
            ms_scatter_gr=[0.08, 0.08, 0.08, 0.08, 0.08],
            red_scatter_gr=[0.04, 0.04, 0.04, 0.04, 0.04],
            fq_gr_blueshift_factor_table=default_fq_gr_blueshift_table, **kwargs):
    """ Generate a Monte Carlo realization of g-r restframe color.

    Parameters
    ----------
    magr : ndarray
        Numpy array of shape (ngals, ) storing the
        r-band absolute restframe magnitude of every galaxy

    redshift : ndarray
        Numpy array of shape (ngals, ) storing the redshift of each galaxy

    Returns
    -------
    gr : ndarray
        Numpy array of shape (ngals, ) storing g-r restframe color for every galaxy

    is_quiescent : ndarray
        Numpy boolean array of shape (ngals, ) storing whether or not
        the galaxy is on the g-r red sequence
    """
    magr = np.atleast_1d(magr)

    ngals = len(magr)
    with NumpyRNGContext(seed):
        is_quiescent = np.random.rand(ngals) < quiescent_fraction_gr(
            magr, redshift, fq_gr, fq_gr_blueshift_factor_table)

    red_sequence_loc = red_sequence_peak_gr(magr[is_quiescent], red_peak_gr)
    red_sequence_loc = red_sequence_loc + red_sequence_loc*redshift_evolution_factor(
        magr[is_quiescent], redshift[is_quiescent], z_table, peak_shift_factor_gr)
    red_sequence_scatter = red_sequence_width_gr(magr[is_quiescent], red_scatter_gr)
    red_sequence = np.random.normal(loc=red_sequence_loc, scale=red_sequence_scatter)

    main_sequence_loc = main_sequence_peak_gr(magr[~is_quiescent], ms_peak_gr)
    main_sequence_loc = main_sequence_loc + main_sequence_loc*redshift_evolution_factor(
                magr[~is_quiescent], redshift[~is_quiescent], z_table, peak_shift_factor_gr)
    main_sequence_scatter = main_sequence_width_gr(magr[~is_quiescent], ms_scatter_gr)
    star_forming_sequence = np.random.normal(loc=main_sequence_loc, scale=main_sequence_scatter)

    result = np.zeros(ngals).astype('f4')
    result[is_quiescent] = red_sequence
    result[~is_quiescent] = star_forming_sequence
    return result, is_quiescent


def g_minus_r2(magr, redshift, seed=None, z_table=peak_shift_factor_z_table,
            peak_shift_factor_gr=default_peak_shift_factor_gr,
            ms_gr_shift_table=default_ms_peak_gr_zevol,
            red_gr_shift_table=default_red_peak_gr_zevol,
            red_sequence_gr_shift_table=default_red_peak_gr_zevol,
            fq_gr=default_fq_gr,
            red_peak_gr=default_red_peak_gr,
            ms_peak_gr=default_ms_peak_gr,
            ms_scatter_gr=[0.08, 0.08, 0.08, 0.08, 0.08],
            red_scatter_gr=[0.04, 0.04, 0.04, 0.04, 0.04],
            fq_gr_blueshift_factor_table=default_fq_gr_blueshift_table, **kwargs):
    """ Generate a Monte Carlo realization of g-r restframe color.

    Parameters
    ----------
    magr : ndarray
        Numpy array of shape (ngals, ) storing the
        r-band absolute restframe magnitude of every galaxy

    redshift : ndarray
        Numpy array of shape (ngals, ) storing the redshift of each galaxy

    Returns
    -------
    gr : ndarray
        Numpy array of shape (ngals, ) storing g-r restframe color for every galaxy

    is_quiescent : ndarray
        Numpy boolean array of shape (ngals, ) storing whether or not
        the galaxy is on the g-r red sequence
    """
    magr = np.atleast_1d(magr)

    ngals = len(magr)
    with NumpyRNGContext(seed):
        is_quiescent = np.random.rand(ngals) < quiescent_fraction_gr(
            magr, redshift, fq_gr, fq_gr_blueshift_factor_table)

    red_sequence_loc = red_sequence_peak_gr2(
        magr[is_quiescent], red_peak_gr, redshift[is_quiescent], red_gr_shift_table)

    red_sequence_scatter = red_sequence_width_gr(magr[is_quiescent], red_scatter_gr)
    red_sequence = np.random.normal(loc=red_sequence_loc, scale=red_sequence_scatter)

    main_sequence_loc = main_sequence_peak_gr2(
        magr[~is_quiescent], ms_peak_gr, redshift[~is_quiescent], ms_gr_shift_table)

    main_sequence_scatter = main_sequence_width_gr(magr[~is_quiescent], ms_scatter_gr)
    star_forming_sequence = np.random.normal(loc=main_sequence_loc, scale=main_sequence_scatter)

    result = np.zeros(ngals).astype('f4')
    result[is_quiescent] = red_sequence
    result[~is_quiescent] = star_forming_sequence
    return result, is_quiescent


def red_sequence_width_ri(magr, red_scatter_ri,
        x=[-22.5, -21, -20, -18, -15]):
    """
    Level of scatter about the median value of <r-i | Mr> for red sequence galaxies.
    """
    return sequence_width(magr, x, red_scatter_ri)


def main_sequence_width_ri(magr, ms_scatter_ri,
        x=[-22.5, -21, -20, -18, -15]):
    """
    Level of scatter about the median value of <r-i | Mr> for star-forming galaxies.
    """
    return sequence_width(magr, x, ms_scatter_ri)


def red_sequence_peak_ri(magr, red_peak_ri,
        x=[-23, -21, -20, -19.5, -19, -18, -15]):
    """
    Location of the median value of <r-i | Mr> for red sequence galaxies.
    """
    return sequence_peak(magr, x, red_peak_ri)


def main_sequence_peak_ri(magr, ms_peak_ri,
        x=[-25, -21, -20, -19, -18, -15]):
    """
    Location of the median value of <r-i | Mr> for star-forming galaxies.
    """
    return sequence_peak(magr, x, ms_peak_ri)


def quiescent_fraction_ri(magr, redshift, fq_ri, blueshift_factor_table_ri):
    """
    Fraction of galaxies on the r-i red sequence as a function of Mr.
    """
    fq_z0 = np.interp(magr, fq_ri_abscissa, fq_ri)
    return apply_z_evolution_of_fq(fq_z0, redshift, blueshift_z_table, blueshift_factor_table_ri)


def r_minus_i(magr, redshift, seed=None, z_table=peak_shift_factor_z_table,
            peak_shift_factor_ri=default_peak_shift_factor_ri,
            fq_ri=default_fq_ri,
            red_scatter_ri=[0.02, 0.02, 0.02, 0.02, 0.02],
            ms_scatter_ri=[0.02, 0.05, 0.05, 0.05, 0.05],
            red_peak_ri=default_red_peak_ri,
            ms_peak_ri=default_ms_peak_ri,
            blueshift_factor_table_ri=default_fq_ri_blueshift_table, **kwargs):
    """ Generate a Monte Carlo realization of r-i restframe color.

    Parameters
    ----------
    magr : ndarray
        Numpy array of shape (ngals, ) storing the
        r-band absolute restframe magnitude of every galaxy

    redshift : ndarray
        Numpy array of shape (ngals, ) storing the redshift of each galaxy

    Returns
    -------
    ri : ndarray
        Numpy array of shape (ngals, ) storing r-i restframe color for every galaxy

    is_quiescent : ndarray
        Numpy boolean array of shape (ngals, ) storing whether or not
        the galaxy is on the r-i red sequence
    """
    magr = np.atleast_1d(magr)

    ngals = len(magr)
    with NumpyRNGContext(seed):
        is_quiescent = np.random.rand(ngals) < quiescent_fraction_ri(
            magr, redshift, fq_ri, blueshift_factor_table_ri)

    red_sequence_loc = red_sequence_peak_ri(magr[is_quiescent], red_peak_ri)
    red_sequence_loc = red_sequence_loc + red_sequence_loc*redshift_evolution_factor(
        magr[is_quiescent], redshift[is_quiescent], z_table, peak_shift_factor_ri)
    red_sequence_scatter = red_sequence_width_ri(magr[is_quiescent], red_scatter_ri)
    red_sequence = np.random.normal(loc=red_sequence_loc, scale=red_sequence_scatter)

    main_sequence_loc = main_sequence_peak_ri(magr[~is_quiescent], ms_peak_ri)
    main_sequence_loc = main_sequence_loc + main_sequence_loc*redshift_evolution_factor(
                magr[~is_quiescent], redshift[~is_quiescent], z_table, peak_shift_factor_ri)
    main_sequence_scatter = main_sequence_width_ri(magr[~is_quiescent], ms_scatter_ri)
    star_forming_sequence = np.random.normal(loc=main_sequence_loc, scale=main_sequence_scatter)

    result = np.zeros(ngals).astype('f4')
    result[is_quiescent] = red_sequence
    result[~is_quiescent] = star_forming_sequence
    return result, is_quiescent


def gr_ri_monte_carlo(magr, sfr_percentile, redshift,
            local_random_scale=0.1, nwin=301, seed=43, **kwargs):
    """ Generate a Monte Carlo realization of (g-r) and (r-i) restframe colors.

    Parameters
    ----------
    magr : ndarray
        Numpy array of shape (ngals, ) storing the
        r-band absolute restframe magnitude of every galaxy

    sfr_percentile : ndarray
        Numpy array of shape (ngals, ) storing the SFR-percentile
        of each galaxy, Prob(< SFR | M*). This quantity can be calculated using
        the halotools.utils.sliding_conditional_percentile function.

    redshift : ndarray
        Numpy array of shape (ngals, ) storing the redshift of each galaxy

    Returns
    -------
    gr : ndarray
        Numpy array of shape (ngals, ) storing g-r restframe color for every galaxy

    ri : ndarray
        Numpy array of shape (ngals, ) storing r-i restframe color for every galaxy

    is_quiescent_ri : ndarray
        Numpy boolean array of shape (ngals, ) storing whether or not
        the galaxy is on the r-i red sequence

    is_quiescent_gr : ndarray
        Numpy boolean array of shape (ngals, ) storing whether or not
        the galaxy is on the g-r red sequence

    """
    p = np.random.normal(loc=1-sfr_percentile, scale=local_random_scale)

    ri_orig, is_quiescent_ri = r_minus_i(magr, redshift, **kwargs)
    gr_orig, is_quiescent_gr = g_minus_r(magr, redshift, **kwargs)
    gr = conditional_abunmatch(magr, p, magr, gr_orig, nwin)

    noisy_gr = np.random.normal(loc=gr, scale=0.1)
    ri = conditional_abunmatch(magr, noisy_gr, magr, ri_orig, nwin)

    return gr, ri, is_quiescent_ri, is_quiescent_gr