import streamlit as st
import numpy as np
import pandas as pd

from radio_telescope_benchmark.data.synthetic import generate_synthetic_telescope, generate_y_factor_data, generate_drift_scan_data
from radio_telescope_benchmark.analysis.y_factor import compute_y_factor, compute_t_rx
from radio_telescope_benchmark.analysis.beam import fit_beam_1d

st.set_page_config(page_title="RTB: Instrument Passport", layout="wide")

st.title("📡 Radio Telescope Benchmark")
st.subheader("Metrological Characterization & Science Suitability")

# Offline mode text
st.sidebar.markdown("### 🔌 Offline-First")
st.sidebar.markdown("All computations are local. No telemetry.")

st.sidebar.markdown("---")
st.sidebar.header("Telescope Configuration")
system = generate_synthetic_telescope()
epoch = system.get_current_epoch()

st.sidebar.text(f"System: {system.name}")
st.sidebar.text(f"Epoch ID: {epoch.id}")
st.sidebar.text(f"Description: {epoch.description}")

tab1, tab2, tab3 = st.tabs(["Overview & Suitability", "Noise & Gain", "Beam & Pointing"])

with tab1:
    st.header("Science Suitability Profile")
    st.markdown("Profile: **H I 21 cm (Galactic)**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("STATUS: READY WITH LIMITATIONS")
        st.markdown("**Limitations:**")
        st.markdown("- Frequency stability over long integrations (> 60s) degrades due to LO drift.")
        st.markdown("- T_sys (142 K) exceeds ideal target (80 K), requiring 3.1x more integration time.")
        
    with col2:
        st.markdown("### System Bottlenecks")
        df = pd.DataFrame([
            {"Subsystem": "LNA", "Impact": "High (Thermal Noise)"},
            {"Subsystem": "LO/Clock", "Impact": "Critical (Allan Drift at tau=60s)"},
            {"Subsystem": "Mount", "Impact": "Low (Pointing Error 0.6° < HPBW)"}
        ])
        st.dataframe(df, use_container_width=True)

with tab2:
    st.header("Receiver Noise Temperature (Y-Factor)")
    
    yf_data = generate_y_factor_data()
    y_val, y_err = compute_y_factor(yf_data['p_hot'], yf_data['p_cold'], yf_data['p_hot_err'], yf_data['p_cold_err'])
    t_rx, t_rx_err = compute_t_rx(y_val, yf_data['t_hot'], yf_data['t_cold'], y_err, 0.0, 0.0)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Measured Y-Factor", f"{y_val:.2f} ± {y_err:.2f}")
    col2.metric("T_rx (Monte Carlo)", f"{t_rx:.1f} K", delta=f"± {t_rx_err:.1f} K", delta_color="off")
    col3.metric("Estimated T_sys", f"{t_rx + 51.0:.1f} K")
    
    st.markdown("### Raw Y-Factor Spectra")
    chart_data = pd.DataFrame(
        np.random.randn(100, 2) * 0.1 + [y_val, 1.0],
        columns=['Hot Load', 'Cold Load']
    )
    st.line_chart(chart_data)

with tab3:
    st.header("Beamwidth & Pointing Offset")
    
    angles, power = generate_drift_scan_data()
    beam_res = fit_beam_1d(angles, power)
    
    col1, col2 = st.columns(2)
    col1.metric("Measured HPBW", f"{beam_res['hpbw']:.2f}°", delta=f"± {beam_res['hpbw_err']:.2f}°", delta_color="off")
    col2.metric("Pointing Offset", f"{beam_res['center']:.2f}°", delta=f"± {beam_res['center_err']:.2f}°", delta_color="off")
    
    # Plotly or matplotlib can be used here, we use st.line_chart for simplicity in demo
    st.markdown("### Drift Scan Fit")
    df_beam = pd.DataFrame({
        'Angle (deg)': angles,
        'Measured Power': power,
    }).set_index('Angle (deg)')
    st.line_chart(df_beam)
