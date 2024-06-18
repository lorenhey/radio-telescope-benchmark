import pytest
import numpy as np
from radio_telescope_benchmark.analysis.enbw import compute_enbw, enbw_from_window

def test_enbw_rectangular_window():
    # Ideal rectangular filter
    power = np.array([0, 0, 1, 1, 1, 0, 0])
    df = 10.0
    enbw = compute_enbw(power, df)
    # Sum = 3, Max = 1 => ENBW = 3 * 10 = 30
    assert enbw == 30.0

def test_enbw_hann_window():
    # Hann window analytical ENBW is 1.5 bins
    N = 1024
    window = np.hanning(N)
    fs = 1024.0 # 1 Hz per bin
    enbw = enbw_from_window(window, fs, N)
    
    # 1.5 bins * 1 Hz/bin = 1.5 Hz
    assert np.isclose(enbw, 1.5, rtol=0.01)
