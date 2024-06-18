import numpy as np
from typing import Tuple

def radiometer_equation(t_sys: float, bandwidth: float, tau: float, n_pol: int = 1) -> float:
    """
    Theoretical thermal noise (sigma_T) based on Radiometer Equation.
    """
    return t_sys / np.sqrt(n_pol * bandwidth * tau)

def compute_allan_variance(time_series: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute Overlapping Allan Variance.
    
    Args:
        time_series: 1D array of measurements (e.g. power or temperature)
        dt: Sample spacing in seconds
        
    Returns:
        tau_array, allan_var, allan_dev
    """
    N = len(time_series)
    max_m = N // 2
    
    # Generate logarithmically spaced tau indices to save computation
    m_array = np.unique(np.logspace(0, np.log10(max_m), 50).astype(int))
    
    tau_array = []
    avar = []
    
    for m in m_array:
        if m == 0:
            continue
            
        # Overlapping Allan Variance
        # y_k is the fractional frequency or power, here we just use the raw values
        # We need to average over m samples
        # A more efficient way using cumulative sum:
        cumsum_y = np.cumsum(np.insert(time_series, 0, 0))
        
        # mean over intervals of length m
        y_bar = (cumsum_y[m:] - cumsum_y[:-m]) / m
        
        # differences between adjacent intervals
        diff = y_bar[m:] - y_bar[:-m]
        
        var = 0.5 * np.mean(diff**2)
        
        tau_array.append(m * dt)
        avar.append(var)
        
    tau_array = np.array(tau_array)
    avar = np.array(avar)
    adev = np.sqrt(avar)
    
    return tau_array, avar, adev
