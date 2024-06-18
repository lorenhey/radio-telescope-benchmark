from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from .uncertainty import MeasurementResult

class Component(BaseModel):
    id: str = Field(..., description="Unique identifier for the component")
    type: Literal[
        "Antenna", "Feed", "Polarization", "LNA", "Filter", "BiasTee",
        "Cable", "Attenuator", "Mixer", "ReferenceClock", "SDR", "ADC",
        "Backend", "Computer", "Software", "Generic"
    ] = "Generic"
    model: Optional[str] = Field(None, description="Model or part number")
    specifications: Dict[str, str] = Field(default_factory=dict, description="Manufacturer specifications")

class SignalChainNode(BaseModel):
    component_id: str
    stage_index: int = Field(..., description="Order in the signal chain, starting from 0 (closest to sky)")

class ConfigurationEpoch(BaseModel):
    id: str = Field(..., description="Epoch identifier (e.g., '2026-09-A')")
    date_start: str = Field(..., description="Start date of this configuration")
    date_end: Optional[str] = Field(None, description="End date of this configuration")
    description: str = Field(..., description="Description of the epoch changes")
    components: List[Component] = Field(default_factory=list, description="Components present in this epoch")
    signal_chain: List[SignalChainNode] = Field(default_factory=list, description="Ordered signal chain")

class TelescopeSystem(BaseModel):
    name: str = Field(..., description="Name of the radio telescope system")
    epochs: List[ConfigurationEpoch] = Field(default_factory=list, description="Configuration history")
    
    def get_current_epoch(self) -> Optional[ConfigurationEpoch]:
        if not self.epochs:
            return None
        # Return the last one or the one without date_end
        for epoch in reversed(self.epochs):
            if epoch.date_end is None:
                return epoch
        return self.epochs[-1]
