import pytest
import numpy as np
from radio_telescope_benchmark.analysis.noise_cascade import compute_cascade, passive_component_noise, CascadeStage

def test_loss_before_lna():
    # Cable with 3dB loss at 290K before LNA with 0.6 dB NF (approx 43K)
    # L_linear = 10^(3/10) = 1.99526
    L = 10**(3.0/10.0)
    cable = passive_component_noise(L, 290.0)
    
    # LNA
    lna_t = 290 * (10**(0.6/10) - 1)
    lna = CascadeStage(name="LNA", gain_linear=100.0, t_noise=lna_t)
    
    total_t, total_g = compute_cascade([cable, lna])
    
    # Expected: T_cable + T_lna * L
    # T_cable = (1.995 - 1) * 290 = 288.6K
    # total = 288.6 + 43.0 * 1.995 = 374.4 K
    assert np.isclose(total_t, 288.6 + lna_t * L, rtol=0.01)
