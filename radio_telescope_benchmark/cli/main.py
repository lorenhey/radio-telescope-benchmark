import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json
import numpy as np

from ..data.synthetic import generate_synthetic_telescope, generate_y_factor_data, generate_drift_scan_data
from ..analysis.y_factor import compute_y_factor, compute_t_rx
from ..analysis.beam import fit_beam_1d, expected_hpbw

app = typer.Typer(help="Radio Telescope Benchmark CLI")
test_app = typer.Typer(help="Run specific benchmark tests")
beam_app = typer.Typer(help="Beam and pointing tests")

app.add_typer(test_app, name="test")
app.add_typer(beam_app, name="beam")

console = Console()

@app.command()
def demo():
    """Run a synthetic flagship demo of the instrument passport."""
    console.print(Panel.fit("[bold blue]RADIO TELESCOPE CHARACTERIZATION[/bold blue]\n[italic]Synthetic Demo[/italic]"))
    
    system = generate_synthetic_telescope()
    epoch = system.get_current_epoch()
    console.print(f"System: [bold]{system.name}[/bold]")
    console.print(f"Epoch: {epoch.id} ({epoch.description})")
    
    # Run Y-factor test
    yf_data = generate_y_factor_data()
    y_val, y_err = compute_y_factor(yf_data['p_hot'], yf_data['p_cold'], yf_data['p_hot_err'], yf_data['p_cold_err'])
    t_rx, t_rx_err = compute_t_rx(y_val, yf_data['t_hot'], yf_data['t_cold'], y_err, 0.0, 0.0)
    
    t_sys = t_rx + 51.0 # arbitrary sky + spillover
    t_sys_err = np.sqrt(t_rx_err**2 + 10.0**2)
    
    # Run drift scan
    angles, power = generate_drift_scan_data()
    beam_res = fit_beam_1d(angles, power)
    exp_hpbw = expected_hpbw(0.21, 1.5) # 21cm, 1.5m dish
    
    # Present results
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    
    table.add_row("Receiver noise temperature", f"{t_rx:.0f} ± {t_rx_err:.0f} K")
    table.add_row("System temperature", f"{t_sys:.0f} ± {t_sys_err:.0f} K")
    table.add_row("Usable spectral bandwidth", "1.74 MHz")
    table.add_row("Gain drift", "0.31 dB/hour")
    table.add_row("Frequency drift", "1.7 kHz/hour")
    
    if beam_res['success']:
        table.add_row("Measured HPBW", f"{beam_res['hpbw']:.1f} ± {beam_res['hpbw_err']:.1f}°")
    table.add_row("Expected HPBW model", f"{exp_hpbw:.1f}°")
    if beam_res['success']:
        table.add_row("Pointing offset", f"{beam_res['center']:.1f} ± {beam_res['center_err']:.1f}°")
        
    table.add_row("Thermal integration regime", "up to ~55 s")
    table.add_row("", "")
    table.add_row("H I 21 cm", "[yellow]READY WITH LIMITATIONS[/yellow]")
    table.add_row("Primary limitation", "frequency stability over long integrations")
    
    console.print(table)

if __name__ == "__main__":
    app()
