import numpy as np
from typing import Tuple, Dict
from ..core.uncertainty import MeasurementResult, Uncertainty

def compute_y_factor(p_hot: float, p_cold: float, p_hot_err: float = 0.0, p_cold_err: float = 0.0, 
                     n_samples: int = 10000) -> Tuple[float, float]:
    """
    Compute Y-factor and its statistical uncertainty using Monte Carlo.
    Powers must be in linear units (not dB).
    """
    if p_hot <= 0 or p_cold <= 0:
        raise ValueError("Powers must be positive linear values")
        
    y_val = p_hot / p_cold
    
    if p_hot_err == 0 and p_cold_err == 0:
        return y_val, 0.0
        
    p_hot_dist = np.random.normal(p_hot, p_hot_err, n_samples)
    p_cold_dist = np.random.normal(p_cold, p_cold_err, n_samples)
    
    # Filter out non-physical values if errors are huge
    valid = (p_hot_dist > 0) & (p_cold_dist > 0)
    
    y_dist = p_hot_dist[valid] / p_cold_dist[valid]
    y_err = float(np.std(y_dist))
    return y_val, y_err

def compute_t_rx(y: float, t_hot: float, t_cold: float, 
                 y_err: float = 0.0, t_hot_err: float = 0.0, t_cold_err: float = 0.0,
                 n_samples: int = 100000) -> Tuple[float, float]:
    """
    Compute Receiver Noise Temperature (T_rx) using Y-factor method.
    Uses Monte Carlo to propagate uncertainties, correctly handling Y ~ 1 explosion.
    """
    if y <= 1.0:
        raise ValueError("Y-factor must be > 1 for passive loads")
        
    t_rx_val = (t_hot - y * t_cold) / (y - 1.0)
    
    if y_err == 0 and t_hot_err == 0 and t_cold_err == 0:
        return t_rx_val, 0.0
        
    y_dist = np.random.normal(y, y_err, n_samples)
    th_dist = np.random.normal(t_hot, t_hot_err, n_samples)
    tc_dist = np.random.normal(t_cold, t_cold_err, n_samples)
    
    # Filter non-physical (Y <= 1)
    valid = y_dist > 1.0001
    
    if np.sum(valid) < n_samples * 0.1:
        # If too many are invalid, the uncertainty is effectively infinite/unbounded
        return t_rx_val, np.inf
        
    trx_dist = (th_dist[valid] - y_dist[valid] * tc_dist[valid]) / (y_dist[valid] - 1.0)
    
    # Use robust statistics (MAD or percentiles) if distribution is heavy-tailed
    # But for standard reporting, standard deviation is expected unless infinite.
    # Let's use the 1-sigma interpercentile range for stability near Y=1
    q16, q84 = np.percentile(trx_dist, [15.865, 84.135])
    t_rx_err = (q84 - q16) / 2.0
    
    return t_rx_val, float(t_rx_err)
