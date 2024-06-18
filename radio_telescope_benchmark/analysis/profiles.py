from typing import Dict, Any, List
from ..core.benchmark import BenchmarkSession, SuitabilityProfile

def evaluate_suitability(session: BenchmarkSession, profile_name: str) -> SuitabilityProfile:
    """
    Evaluate science suitability based on hardcoded profiles (for v1).
    """
    profiles = {
        "hi-21cm": {
            "version": "1.0",
            "req": {
                "max_t_sys": 200.0,
                "min_integration_stability_s": 60.0,
                "max_gain_drift_db_per_h": 0.5,
                "beam_measured": True
            }
        },
        "solar-continuum": {
            "version": "1.0",
            "req": {
                "max_t_sys": 1500.0,
                "min_integration_stability_s": 1.0,
                "max_gain_drift_db_per_h": 2.0,
                "beam_measured": True
            }
        }
    }
    
    if profile_name not in profiles:
        raise ValueError(f"Profile {profile_name} not found.")
        
    prof = profiles[profile_name]
    reqs = prof["req"]
    
    status = "READY"
    limitations = []
    missing = []
    
    # Evaluate Tsys
    if "system_temperature" in session.results:
        t_sys = session.results["system_temperature"].metrics["t_sys"].value
        if t_sys > reqs["max_t_sys"]:
            status = "READY_WITH_LIMITATIONS" if t_sys < reqs["max_t_sys"]*1.5 else "NOT_READY"
            limitations.append(f"T_sys ({t_sys:.1f} K) exceeds ideal {reqs['max_t_sys']} K")
    else:
        missing.append("system_temperature")
        status = "UNKNOWN"
        
    # Evaluate Stability
    if "integration_stability" in session.results:
        stab_time = session.results["integration_stability"].metrics["thermal_time_limit_s"].value
        if stab_time < reqs["min_integration_stability_s"]:
            status = "READY_WITH_LIMITATIONS" if status != "NOT_READY" else "NOT_READY"
            limitations.append(f"Thermal integration limit ({stab_time:.1f} s) below required {reqs['min_integration_stability_s']} s")
    else:
        missing.append("integration_stability")
        if status != "NOT_READY":
            status = "UNKNOWN"
            
    # Beam
    if reqs["beam_measured"]:
        if "beam_characterization" not in session.results:
            missing.append("beam_characterization")
            if status != "NOT_READY":
                status = "UNKNOWN"
                
    if missing and status == "READY":
        status = "UNKNOWN"
        
    return SuitabilityProfile(
        profile_name=profile_name,
        version=prof["version"],
        requirements=reqs,
        status=status,
        limitations=limitations,
        missing_measurements=missing
    )
