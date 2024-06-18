import numpy as np
from scipy.optimize import curve_fit
from typing import Tuple, Dict

def gaussian_1d(x: np.ndarray, amplitude: float, mean: float, stddev: float, baseline: float) -> np.ndarray:
    return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2)) + baseline

def fit_beam_1d(angles: np.ndarray, power: np.ndarray) -> Dict[str, float]:
    """
    Fit a 1D Gaussian to a beam scan.
    
    Args:
        angles: Array of angular coordinates (e.g. degrees)
        power: Linear power measurements
        
    Returns:
        Dict with HPBW, center_offset, amplitude, baseline, and their errors.
    """
    # Initial guess
    baseline_guess = np.median(power)
    amp_guess = np.max(power) - baseline_guess
    mean_guess = angles[np.argmax(power)]
    
    # Rough stddev guess (width at half max)
    half_max = baseline_guess + amp_guess / 2.0
    above_half = power > half_max
    if np.sum(above_half) > 1:
        fwhm_guess = angles[above_half][-1] - angles[above_half][0]
        std_guess = fwhm_guess / 2.355
    else:
        std_guess = (np.max(angles) - np.min(angles)) / 10.0

    p0 = [amp_guess, mean_guess, std_guess, baseline_guess]
    
    try:
        popt, pcov = curve_fit(gaussian_1d, angles, power, p0=p0)
        perr = np.sqrt(np.diag(pcov))
        
        amplitude, mean, stddev, baseline = popt
        amp_err, mean_err, std_err, base_err = perr
        
        # HPBW = 2.355 * stddev
        hpbw = abs(2.355 * stddev)
        hpbw_err = 2.355 * std_err
        
        return {
            "hpbw": hpbw,
            "hpbw_err": hpbw_err,
            "center": mean,
            "center_err": mean_err,
            "amplitude": amplitude,
            "baseline": baseline,
            "success": True
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def expected_hpbw(wavelength: float, diameter: float, illumination_factor: float = 1.22) -> float:
    """
    Expected HPBW in degrees.
    k-factor depends on illumination taper. 1.22 is for uniform circular aperture.
    """
    return np.degrees(illumination_factor * (wavelength / diameter))
