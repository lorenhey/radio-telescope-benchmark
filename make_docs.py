import os

os.makedirs('docs', exist_ok=True)
files = [
    'QuickStart.md', 'Philosophy.md', 'SystemModel.md', 'ConfigurationEpochs.md', 
    'BenchmarkSessions.md', 'TestEquipment.md', 'UnitsAndUncertainty.md', 'QuickHealth.md', 
    'ReceiverGain.md', 'NoiseTemperature.md', 'YFactor.md', 'SystemTemperature.md', 
    'NoiseCascades.md', 'Bandpass.md', 'ENBW.md', 'Linearity.md', 'ADCHealth.md', 
    'RadiometerPerformance.md', 'AllanStability.md', 'FrequencyAccuracy.md', 'FrequencyDrift.md', 
    'ThermalDrift.md', 'SkyTests.md', 'Beamwidth.md', 'Pointing.md', 'Sensitivity.md', 
    'RFIEnvironment.md', 'ScienceSuitability.md', 'BenchmarkHistory.md', 'CLI.md', 
    'PythonAPI.md', 'Schemas.md', 'Verification.md', 'Limitations.md', 'Contributing.md'
]

for f in files:
    with open(os.path.join('docs', f), 'w', encoding='utf-8') as out:
        title = f.replace(".md", "")
        out.write(f"# {title}\n\nDocumentation placeholder.\n")
