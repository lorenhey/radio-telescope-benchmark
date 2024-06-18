from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Any
from .uncertainty import MeasurementResult
from .system import TelescopeSystem, ConfigurationEpoch
from .equipment import TestEquipment

class BenchmarkCapability(BaseModel):
    test_name: str
    status: Literal["AVAILABLE", "AVAILABLE_WITH_LIMITATIONS", "NOT_AVAILABLE", "NOT_EVALUABLE"]
    reason: Optional[str] = None

class TestResult(BaseModel):
    test_name: str
    status: Literal["NOT_RUN", "RUN", "PASS", "REVIEW", "NOT_EVALUABLE"] = "NOT_RUN"
    metrics: Dict[str, MeasurementResult] = Field(default_factory=dict)
    findings: List[str] = Field(default_factory=list)
    raw_data_refs: List[str] = Field(default_factory=list)
    
class SuitabilityProfile(BaseModel):
    profile_name: str
    version: str
    requirements: Dict[str, Any]
    status: Literal["READY", "READY_WITH_LIMITATIONS", "NOT_READY", "UNKNOWN"] = "UNKNOWN"
    limitations: List[str] = Field(default_factory=list)
    missing_measurements: List[str] = Field(default_factory=list)

class BenchmarkSession(BaseModel):
    id: str = Field(..., description="Unique session ID")
    date: str
    system_snapshot: TelescopeSystem
    epoch_id: str
    test_equipment: List[TestEquipment] = Field(default_factory=list)
    environment: Dict[str, Any] = Field(default_factory=dict, description="Temperature, weather, etc.")
    results: Dict[str, TestResult] = Field(default_factory=dict)
    suitability: Dict[str, SuitabilityProfile] = Field(default_factory=dict)
    
    def add_result(self, result: TestResult):
        self.results[result.test_name] = result
