# generate_data.py
import numpy as np
import pandas as pd
import neurokit2 as nk

# Parameters
duration = 900                 # total duration (seconds)
fs = 50                        # sampling rate (Hz)
timestamps = np.arange(0, duration, 1/fs)

# Simulate ECG and Respiration signals
ecg = nk.ecg_simulate(duration=duration, sampling_rate=fs, heart_rate=70, noise=0.01)
resp = nk.rsp_simulate(duration=duration, sampling_rate=fs, respiratory_rate=15)

# Create baseline vital sign arrays (simulate simple waveforms or random noise)
heart_rate = 60 + 5*np.sin(2*np.pi*timestamps/60) + np.random.normal(0, 1, size=len(timestamps))
bp_systolic = 120 + 10*np.sin(2*np.pi*timestamps/300) + np.random.normal(0, 2, len(timestamps))
bp_diastolic = 80 + 5*np.sin(2*np.pi*timestamps/300) + np.random.normal(0, 1, len(timestamps))
spo2 = 98 + 0.5*np.sin(2*np.pi*timestamps/180) + np.random.normal(0, 0.2, len(timestamps))
body_temp = 37 + 0.2*np.sin(2*np.pi*timestamps/600) + np.random.normal(0, 0.05, len(timestamps))
co2 = 40 + 2*np.sin(2*np.pi*timestamps/240) + np.random.normal(0, 0.5, len(timestamps))

# Introduce arrhythmia at t=520s: e.g., reduce ECG amplitude irregularly and spike HR
idx_arr = int(520 * fs)
ecg[idx_arr:idx_arr+fs*2] *= 0.5  # drop ECG amplitude briefly
heart_rate[idx_arr:idx_arr+fs*2] += 20  # transient tachycardia
# Introduce signal dropout at t=890s: set all signals to NaN for 5 seconds
idx_drop = int(890 * fs)
duration_drop = int(5 * fs)
ecg[idx_drop:idx_drop+duration_drop] = np.nan
resp[idx_drop:idx_drop+duration_drop] = np.nan
heart_rate[idx_drop:idx_drop+duration_drop] = np.nan
bp_systolic[idx_drop:idx_drop+duration_drop] = np.nan
bp_diastolic[idx_drop:idx_drop+duration_drop] = np.nan
spo2[idx_drop:idx_drop+duration_drop] = np.nan
body_temp[idx_drop:idx_drop+duration_drop] = np.nan
co2[idx_drop:idx_drop+duration_drop] = np.nan

# Assemble into DataFrame
df = pd.DataFrame({
    "Time": timestamps,
    "ECG": ecg,
    "Resp": resp,
    "Heart_Rate": heart_rate,
    "BP_Systolic": bp_systolic,
    "BP_Diastolic": bp_diastolic,
    "SpO2": spo2,
    "Body_Temp": body_temp,
    "CO2": co2
})
# Add anomaly labels
df["Arrhythmia_Event"] = 0
df.loc[idx_arr:idx_arr+fs*2-1, "Arrhythmia_Event"] = 1
df["Signal_Dropout"] = 0
df.loc[idx_drop:idx_drop+duration_drop-1, "Signal_Dropout"] = 1

# Save to CSV
df.to_csv("synthetic_vitals.csv", index=False)
