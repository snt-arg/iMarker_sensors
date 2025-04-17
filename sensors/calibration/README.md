# 📸 Calibrating Dual-Vision Sensors

This guide explains how to calibrate dual-vision sensor setups.

---

## ✅ Prerequisites

- Python ≥ 3.8
- Virtual environment (recommended)
- Required packages: `numpy`, `opencv-python`, `pyyaml`

---

## 📍 ELP Stereo Camera Calibration

1. **Navigate to the calibration folder**

   ```bash
   cd `[PATH]/imarker_sensors/sensors/calibration/`
   ```

2. **(Optional) Activate your virtual environment**

   ```bash
   source venv/bin/activate
   ```

3. **Check or edit configuration parameters**

   See [config.yaml](/sensors/calibration/config.yaml)

4. **Run the calibration script**

   ```bash
   python stereoCalibrateELP.py
   ```

5. **Calibration complete!**

   You will get a file named `elpStereoMap.xml` ([sample](/sensors/calibration/output/elpStereoMap.xml)) in the `output/` directory.
   Use this file to undistort and rectify stereo images in your applications.
