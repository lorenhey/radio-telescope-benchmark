# radio-telescope-benchmark

`radio-telescope-benchmark` caracteriza un radiotelescopio antes de utilizarlo para ciencia: sensibilidad, ruido, estabilidad, frecuencia, linealidad, bandwidth, beam y pointing medidos sobre el sistema real, con incertidumbre y provenance.

A component datasheet tells you what a part should do. This project measures what the complete telescope actually does.

```bash
rtb demo
```

## Concept
The core philosophy is grounded in metrology. We separate `SPECIFIED` from `MEASURED`. An LNA with a specified 0.6 dB noise figure does not automatically mean a 43 K system temperature. The antenna, feed, coax, filters, digitization, and RFI environment all degrade performance. This tool answers:
- ¿Cuál es realmente mi temperatura de receptor?
- ¿Cuánto mejora si integro un minuto?
- ¿Mi frecuencia se corre mientras calienta?
- ¿Cuál es realmente el ancho de mi haz?

## Project Architecture

```text
BUILD → CHARACTERIZE → CALIBRATE → OBSERVE → VALIDATE → PUBLISH
           (You are here)
```

The system builds an **Instrument Passport** — a versioned, measurement-backed snapshot of your telescope's capabilities. It allows you to select a **Science Profile** (e.g., `hi-21cm`) and automatically evaluate if your actual, measured system can meet the observational requirements, including identifying the primary limitation (bottleneck).

## Key Features
- **Y-Factor with Uncertainty**: Propagates noise temperature through Monte Carlo correctly, recognizing that $Y \approx 1$ creates enormous uncertainty.
- **Equivalent Noise Bandwidth (ENBW)**: Calculates true integration bandwidth based on spectral filters, avoiding the mistake of treating channel spacing as ENBW.
- **Allan Variance / Radiometer Scaling**: Evaluates where your system stops integrating like white noise and starts drifting, determining the maximum useful integration time.
- **Hardware Epochs**: Changing the LNA invalidates receiver gain and noise temperature, but preserves the physical dish pointing model.
- **Science Suitability**: Evaluates if your measured capability is sufficient for specific astronomical targets without using arbitrary "1-100 scores".

## Quick Start

```bash
pip install radio-telescope-benchmark
rtb demo
```

## CLI Usage

```bash
rtb system inspect telescope.yaml
rtb test quick-health capture.iq
rtb test y-factor --hot hot.fits --cold cold.fits --thot 295 --tcold 10
rtb test stability stable-load.csv
rtb test linearity sweep.csv
rtb beam drift-scan scan.fits
rtb compare before after
rtb suitability benchmark.json --profile hi-21cm
rtb report benchmark.json
```

## Offline-First & Reproducible
This tool is built for field engineering and observatory control rooms. It requires no cloud connection, no login, and performs no silent telemetry. All data provenance, raw files, and methodology are retained in the generated benchmark manifest to back up your scientific observations.
