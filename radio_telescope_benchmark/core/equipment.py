from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict

class TestEquipment(BaseModel):
    id: str = Field(..., description="Unique identifier for the test equipment")
    type: Literal[
        "signal_generator", "noise_source", "power_meter", "spectrum_analyzer",
        "VNA", "attenuator", "temperature_sensor", "frequency_reference",
        "calibration_load", "other"
    ]
    model: str = Field(..., description="Equipment model")
    calibration_status: Literal["CALIBRATED", "UNCALIBRATED", "USER-VERIFIED", "UNKNOWN"] = "UNKNOWN"
    calibration_date: Optional[str] = Field(None, description="Last calibration date")
    specifications: Dict[str, str] = Field(default_factory=dict, description="Key specifications")
