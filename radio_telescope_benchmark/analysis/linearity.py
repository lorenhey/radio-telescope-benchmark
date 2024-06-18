import numpy as np
from typing import Dict, Tuple

def compute_linearity(input_power_dbm: np.ndarray, output_power_dbfs: np.ndarray) -> Dict[str, float]:
    """
    Evaluate linearity and find the 1dB compression point.
    Assuming the lower 30% of the points are in the linear regime to fit the gain.
    """
    if len(input_power_dbm) < 4:
        raise ValueError("Not enough points to compute linearity.")
        
    # Sort by input power
    idx = np.argsort(input_power_dbm)
    pin = input_power_dbm[idx]
    pout = output_power_dbfs[idx]
    
    # Fit linear region (assume first 30% or at least 3 points)
    n_linear = max(3, int(len(pin) * 0.3))
    
    # pout = pin * slope + offset
    # In an ideal system, slope is 1 (dB/dB). We fit the slope to check.
    coefs = np.polyfit(pin[:n_linear], pout[:n_linear], 1)
    slope, offset = coefs
    
    # Calculate ideal linear output
    pout_ideal = pin * slope + offset
    
    # Find compression (departure by 1 dB)
    deviation = pout_ideal - pout
    compression_idx = np.where(deviation >= 1.0)[0]
    
    if len(compression_idx) > 0:
        p1db_in = pin[compression_idx[0]]
        p1db_out = pout[compression_idx[0]]
    else:
        p1db_in = np.nan
        p1db_out = np.nan
        
    return {
        "linear_slope": slope,
        "gain_offset": offset,
        "p1db_in_dbm": p1db_in,
        "p1db_out_dbfs": p1db_out
    }

def calculate_adc_utilization(raw_iq: np.ndarray, bit_depth: int = 8) -> Dict[str, float]:
    """
    Analyze ADC health from raw IQ data.
    """
    max_val = 2**(bit_depth - 1) - 1
    min_val = -(2**(bit_depth - 1))
    
    i_chan = np.real(raw_iq)
    q_chan = np.imag(raw_iq)
    
    i_max, i_min = np.max(i_chan), np.min(i_chan)
    q_max, q_min = np.max(q_chan), np.min(q_chan)
    
    # Clipping detection (if we hit the rail)
    i_clipped = np.sum((i_chan >= max_val) | (i_chan <= min_val))
    q_clipped = np.sum((q_chan >= max_val) | (q_chan <= min_val))
    total_clipped = i_clipped + q_clipped
    clip_fraction = total_clipped / (2 * len(raw_iq))
    
    i_mean = np.mean(i_chan)
    q_mean = np.mean(q_chan)
    
    full_scale_usage = max(abs(i_max), abs(i_min), abs(q_max), abs(q_min)) / max_val
    
    return {
        "dc_offset_i": i_mean,
        "dc_offset_q": q_mean,
        "clipping_fraction": clip_fraction,
        "full_scale_usage": full_scale_usage,
        "headroom_db": -20 * np.log10(full_scale_usage) if full_scale_usage > 0 else np.inf
    }
