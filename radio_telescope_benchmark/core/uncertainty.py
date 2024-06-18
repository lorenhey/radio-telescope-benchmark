import numpy as np
from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, Any

class Uncertainty(BaseModel):
    value: float = Field(..., description="Estimated uncertainty value")
    type: Literal["statistical", "systematic", "combined", "unknown"] = "unknown"
    distribution: Literal["gaussian", "uniform", "unknown"] = "unknown"
    confidence_level: Optional[float] = Field(None, description="Confidence level, e.g., 0.95 or 0.68 for 1-sigma")

class MeasurementResult(BaseModel):
    value: float = Field(..., description="Measured or derived value")
    unit: str = Field(..., description="Physical unit of the value")
    uncertainty: Optional[Uncertainty] = Field(None, description="Uncertainty of the measurement")
    method: str = Field(..., description="Method used to obtain the value (e.g., 'Y-factor', 'Allan variance')")
    date: str = Field(..., description="Date of measurement or derivation")
    source: str = Field(..., description="Source of the data (e.g., file path, synthetic generator)")
    is_limit: bool = Field(False, description="True if value is an upper or lower limit")
    
    def format(self) -> str:
        if self.uncertainty:
            return f"{self.value:.4g} ± {self.uncertainty.value:.4g} {self.unit}"
        return f"{self.value:.4g} {self.unit}"
