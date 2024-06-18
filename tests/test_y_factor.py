import pytest
import numpy as np
from radio_telescope_benchmark.analysis.y_factor import compute_y_factor, compute_t_rx

def test_compute_y_factor_exact():
    # Golden case
    t_hot = 300.0
    t_cold = 77.0
    t_rx = 100.0
    
    p_cold = 1.0
    p_hot = p_cold * (t_hot + t_rx) / (t_cold + t_rx)
    
    y, y_err = compute_y_factor(p_hot, p_cold)
    assert np.isclose(y, (t_hot + t_rx) / (t_cold + t_rx))
    assert y_err == 0.0

def test_compute_t_rx_exact():
    # Golden case
    t_hot = 300.0
    t_cold = 77.0
    t_rx_true = 100.0
    
    y = (t_hot + t_rx_true) / (t_cold + t_rx_true)
    
    trx, trx_err = compute_t_rx(y, t_hot, t_cold)
    assert np.isclose(trx, t_rx_true)
    assert trx_err == 0.0

def test_y_factor_uncertainty_explosion():
    # Y ≈ 1 case should have huge uncertainty
    t_hot = 290.0
    t_cold = 280.0
    t_rx_true = 1000.0 # Very noisy receiver
    
    y = (t_hot + t_rx_true) / (t_cold + t_rx_true)
    assert np.isclose(y, 1.0078, atol=0.01)
    
    # 1% power error
    y, y_err = compute_y_factor(y, 1.0, 0.01, 0.01, n_samples=100000)
    
    # Trx error should be massive
    trx, trx_err = compute_t_rx(y, t_hot, t_cold, y_err=y_err)
    
    # Uncertainty should be hundreds of Kelvin
    assert trx_err > 200.0
