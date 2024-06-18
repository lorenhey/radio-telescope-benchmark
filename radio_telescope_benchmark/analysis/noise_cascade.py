from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class CascadeStage:
    name: str
    gain_linear: float
    t_noise: float

def compute_cascade(stages: List[CascadeStage]) -> Tuple[float, float]:
    """
    Compute total cascaded noise temperature and total gain.
    
    Returns:
        (total_t_noise, total_gain_linear)
    """
    total_t = 0.0
    current_gain = 1.0
    
    for stage in stages:
        total_t += stage.t_noise / current_gain
        current_gain *= stage.gain_linear
        
    return total_t, current_gain

def passive_component_noise(loss_linear: float, t_phys: float = 290.0) -> CascadeStage:
    """
    Helper to create a cascade stage for a passive lossy component.
    loss_linear is > 1 (e.g., 3dB loss -> 1.995)
    """
    if loss_linear < 1.0:
        raise ValueError("Loss must be >= 1.0 in linear scale")
        
    gain = 1.0 / loss_linear
    t_noise = (loss_linear - 1.0) * t_phys
    return CascadeStage(name="Passive", gain_linear=gain, t_noise=t_noise)
