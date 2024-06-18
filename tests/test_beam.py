import pytest
import numpy as np
from radio_telescope_benchmark.analysis.beam import fit_beam_1d, gaussian_1d

def test_fit_beam_1d_golden():
    # True parameters
    amp = 10.0
    mean = 2.5
    stddev = 1.5
    baseline = 1.0
    
    angles = np.linspace(-10, 10, 100)
    power = gaussian_1d(angles, amp, mean, stddev, baseline)
    
    res = fit_beam_1d(angles, power)
    assert res["success"]
    assert np.isclose(res["center"], mean, atol=0.01)
    assert np.isclose(res["amplitude"], amp, atol=0.01)
    assert np.isclose(res["hpbw"], 2.355 * stddev, atol=0.01)
