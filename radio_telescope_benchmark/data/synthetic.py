import numpy as np
from ..core.system import TelescopeSystem, ConfigurationEpoch, Component, SignalChainNode
from ..core.benchmark import BenchmarkSession
from ..core.equipment import TestEquipment

def generate_synthetic_telescope() -> TelescopeSystem:
    antenna = Component(id="dish1", type="Antenna", specifications={"diameter_m": "1.5", "illumination_taper": "1.2"})
    feed = Component(id="feed1", type="Feed", specifications={"center_freq_mhz": "1420"})
    lna = Component(id="lna1", type="LNA", specifications={"noise_figure_db": "0.6", "gain_db": "30"})
    filter_rf = Component(id="filter1", type="Filter", specifications={"loss_db": "1.0"})
    cable = Component(id="cable1", type="Cable", specifications={"loss_db": "2.0"})
    sdr = Component(id="sdr1", type="SDR", specifications={"sample_rate_msps": "2.4", "adc_bits": "8"})

    epoch = ConfigurationEpoch(
        id="2026-09-A",
        date_start="2026-09-01T00:00:00Z",
        description="Initial build",
        components=[antenna, feed, lna, filter_rf, cable, sdr],
        signal_chain=[
            SignalChainNode(component_id="dish1", stage_index=0),
            SignalChainNode(component_id="feed1", stage_index=1),
            SignalChainNode(component_id="lna1", stage_index=2),
            SignalChainNode(component_id="filter1", stage_index=3),
            SignalChainNode(component_id="cable1", stage_index=4),
            SignalChainNode(component_id="sdr1", stage_index=5),
        ]
    )

    return TelescopeSystem(
        name="RT-01 (Demo)",
        epochs=[epoch]
    )

def generate_y_factor_data():
    """
    Synthetic Y-factor test data.
    True Trx ~ 90K.
    """
    # Let's say Thot = 295K, Tcold = 77K (LN2) or maybe sky (Tcold_eff = 10K)
    t_hot = 295.0
    t_cold = 15.0 # Effective cold sky
    t_rx_true = 91.0
    
    # Y = (Thot + Trx) / (Tcold + Trx)
    y_true = (t_hot + t_rx_true) / (t_cold + t_rx_true)
    
    p_cold_base = 1.0 # arbitrary linear power
    p_hot_base = y_true * p_cold_base
    
    return {
        "t_hot": t_hot,
        "t_cold": t_cold,
        "p_hot": p_hot_base,
        "p_cold": p_cold_base,
        "p_hot_err": p_hot_base * 0.02, # 2% error
        "p_cold_err": p_cold_base * 0.02,
        "t_rx_true": t_rx_true
    }

def generate_drift_scan_data():
    """
    Synthetic drift scan over a point source.
    HPBW ~ 9.4 deg.
    """
    angles = np.linspace(-20, 20, 100)
    hpbw_true = 9.4
    std_true = hpbw_true / 2.355
    offset_true = 0.6
    
    power_clean = 10.0 * np.exp(-((angles - offset_true)**2) / (2 * std_true**2)) + 2.0
    noise = np.random.normal(0, 0.5, len(angles))
    
    return angles, np.clip(power_clean + noise, 0, None)
