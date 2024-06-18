import numpy as np

def compute_enbw(power_spectrum: np.ndarray, frequency_spacing: float) -> float:
    """
    Compute Equivalent Noise Bandwidth (ENBW) from a power spectrum.
    
    Args:
        power_spectrum: Linear power spectrum (e.g., |H(f)|^2). MUST NOT be in dB.
        frequency_spacing: Delta f between frequency bins.
        
    Returns:
        ENBW in the same units as frequency_spacing.
    """
    if np.any(power_spectrum < 0):
        raise ValueError("Power spectrum must be in linear units, non-negative.")
        
    peak_power = np.max(power_spectrum)
    if peak_power == 0:
        return 0.0
        
    integrated_power = np.sum(power_spectrum) * frequency_spacing
    return integrated_power / peak_power

def enbw_from_window(window: np.ndarray, sample_rate: float, n_fft: int) -> float:
    """
    Compute ENBW for a specific FFT window function.
    """
    s1 = np.sum(window)
    s2 = np.sum(window**2)
    
    # ENBW in bins = N * sum(w^2) / (sum(w))^2
    enbw_bins = len(window) * s2 / (s1**2)
    
    # Convert bins to Hz
    bin_width = sample_rate / n_fft
    return enbw_bins * bin_width
