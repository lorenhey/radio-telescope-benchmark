import pytest
import numpy as np
from radio_telescope_benchmark.analysis.stability import compute_allan_variance, radiometer_equation

def test_radiometer_equation():
    tsys = 100.0
    bw = 1e6
    tau = 1.0
    sigma = radiometer_equation(tsys, bw, tau)
    # sigma = 100 / sqrt(1e6) = 100 / 1000 = 0.1 K
    assert np.isclose(sigma, 0.1)

def test_allan_variance_white_noise():
    np.random.seed(42)
    # White noise
    dt = 1.0
    N = 10000
    noise = np.random.normal(0, 1.0, N)
    
    taus, avar, adev = compute_allan_variance(noise, dt)
    
    # For white noise, ADEV roughly scales as 1/sqrt(tau)
    # adev(tau) / adev(1) ≈ 1 / sqrt(tau)
    ratio = adev[-1] / adev[0]
    expected_ratio = 1.0 / np.sqrt(taus[-1] / taus[0])
    
    # Should be close within factor of ~2 due to statistical fluctuation
    assert ratio < 2.0 * expected_ratio
    assert ratio > 0.5 * expected_ratio
