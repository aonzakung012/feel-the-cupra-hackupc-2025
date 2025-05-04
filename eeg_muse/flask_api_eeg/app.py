#!/usr/bin/env python3
import numpy as np
import threading
import time
import joblib
from flask import Flask, jsonify
from pylsl import StreamInlet, resolve_byprop

# ---- Parameters ----
FS         = 256           # sampling rate (Hz)
WINDOW_SEC = 1.0           # window length (s)
SAMPLES    = int(FS * WINDOW_SEC)
ALPHA_BAND = (8, 14)
BETA_BAND  = (14, 30)
CHANNELS   = [0, 1, 2, 3]   # channels to include
MODEL_PATH = 'eeg_focus_classifier.pkl'

SHIFT = 9000

# ---- State storage ----
current_state = "Unknown"

# ---- Helper: compute band-power via FFT ----
def bandpower(x, fs, band):
    freqs = np.fft.rfftfreq(len(x), 1/fs)
    psd   = np.abs(np.fft.rfft(x))**2
    idx   = np.logical_and(freqs >= band[0], freqs <= band[1])
    return np.mean(psd[idx])

# ---- EEG data collection and processing thread ----
def eeg_processing_loop():
    global current_state

    # 1) Load trained classifier pipeline
    clf = joblib.load(MODEL_PATH)
    print(f"Loaded model from '{MODEL_PATH}' → ready to predict.")

    # 2) Find EEG LSL stream
    print("Looking for an EEG LSL stream…")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    if not streams:
        raise RuntimeError("No EEG stream found.")
    inlet = StreamInlet(streams[0], max_chunklen=SAMPLES)
    print(f"Connected to EEG → classifying every {WINDOW_SEC}s window.")

    # 3) Main loop
    while True:
        samples, _ = inlet.pull_chunk(timeout=1.5, max_samples=SAMPLES)
        if len(samples) < SAMPLES:
            continue

        data = np.array(samples)  # shape (SAMPLES, n_channels)

        # 4) Extract features: alpha & beta power per channel
        feats = []
        for ch in CHANNELS:
            x = data[:, ch]
            feats.append(bandpower(x, FS, ALPHA_BAND)-SHIFT)
            feats.append(bandpower(x, FS, BETA_BAND)-SHIFT)

        # 5) Predict label
        label = clf.predict([feats])[0]  # yields 0 or 1 if you saved numeric, or “Relaxed”/“Focused” if you saved text

        # 6) Map numeric to string if needed
        if isinstance(label, (int, np.integer)):
            current_state = "Focused" if label == 1 else "Relaxed"
        else:
            current_state = label

        # 7) Print status
        feat_str = ", ".join(f"{v:.1f}" for v in feats)
        print(f"[{time.strftime('%H:%M:%S')}] {feat_str} → {current_state}")

        time.sleep(WINDOW_SEC)

# ---- Flask API ----
app = Flask(__name__)

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({"state": current_state})

# ---- Main execution ----
if __name__ == "__main__":
    # 1) Start EEG thread
    threading.Thread(target=eeg_processing_loop, daemon=True).start()
    # 2) Launch Flask
    app.run(host="0.0.0.0", port=5000)
