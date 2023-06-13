# CSR Detector - Sensors

This repository contains the interfaces for the hardware that uses **CSR Marker Detector**. The current version of the code supports cameras introduced below:

| Camera | Interface | Links and Description |
| ------------ | ------------ | ------------ |
| ELP-USB8MP02G-L75 | USB 2.0 | HD 8MP Camera UVC SONY IMX179 CMOS - [link](http://www.webcamerausb.com/elp-8mp-highdefinition-usb-camera-module-usb20-sony-imx179-color-cmos-sensor-75degree-lens-p-45.html) |
| iDS U3-3271LE-C-HQ Rev.1.2 | USB 3.0 and uEye+ | Sony Pregius IMX265 3 MP - [link](https://en.ids-imaging.com/store/u3-3271le-rev-1-2.html) |
| RealSense D435(i) | USB 3.0 and RS library | RealSense Depth Camera D435 4 MP - [link](https://www.intelrealsense.com/depth-camera-d435/) |


## 🎥 Sensor Descriptions

Generally, the sensors are connected to a beamsplitter to provide exact outputs at the same time (as shown below).
![ELP Cameras](docs/cameraSetups.png "ELP Cameras")

### I. ELP Cameras

For ELP cameras, the only required interfaces are USB 2.0 interfaces. Accordingly, the usage of the sensor is "plug & play." First, install the required library (OpenCV) using the command `pip install opencv-python`. The functions defined in `sensorUSB.py` file contain:

- `createCameraObject`: creates an openCV `VideoCapture` object given a port number.
- `grabImage`: grabs the `VideoCapture` object and returns the frame.

### II. iDS Cameras

For iDS cameras, it is necessary to install **iDS Peak** library and its Python binding according to [this link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-linux-readme-2.3_EN.html). Then, add the below Python bindings to make it work. You can also access the binding `whl` files from [this directory](/docs/iDS/):

- `Windows 64bit`:
    - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win_amd64.whl`
    - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win_amd64.whl`

- `Windows 32Bit`:
    - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win32.whl`
    - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win32.whl`

- `Linux`:
    - Go to */usr/local/share/ids/bindings/python/wheel/* 
    - Run `pip install ids_peak-1.4.3.0-cp38-cp38-linux_x86_64.whl`
    - Run `pip install ids_peak_ipl-1.5.0.0-cp38-cp38-linux_x86_64.whl`

The `idsCamera` class provides a convenient interface for interacting with IDS cameras using the `IDS peak library` in Python. Here, we aim to provide an overview of the class and its methods to help users understand how to utilize it in their projects. The functions defined in `sensorIDS.py` file contain:

- `__init__`: initializes the class for interacting with IDS peak library using the port number of the connected camera.
- `loadCameraParameters`: loads camera parameters from a yaml file containing camera parameters, requires the path to the file.
- `setROI`: sets a region of interest (ROI) for the camera.
- `syncAsMaster`: synchronizes the camera as a master.
- `syncAsSlave`: synchronizes the camera as a slave for synchronization with a master camera.
- `startAquisition`: starts the data acquisition from the camera.
- `setExposureTime`: the exposure time to set in milliseconds.
- `getFrame`: triggers the camera to capture frames and returns them as a `numpy` array.
- `closeLibrary`: closes an open object library.

### III. RealSense Cameras

For RealSense cameras, the required interfaces are USB 3.0 interfaces. Install the required libraries (OpenCV and PyRealSense) using the command `pip install opencv-python pyrealsense2`. The functions defined in `sensorRealSense.py` file contain:

- `createPipeline`: creates a pipeline for the RealSense camera.
- `startPipeline`: starts a pipeline for the RealSense camera.
- `grabFrames`: grabs frames from camera.
- `getColorFrame`: gets color frames from the RealSense camera.
- `stopPipeline`: stops the pipeline and releases memory.


### Installation

Finally, install the package using `pip install -e .` to install the packages.


## ⚙️ Sample Usage

Below you can find an example of how to use the `idsCamera` class:

```python
from ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl
import numpy as np

class idsCamera:
    # class implementation...

def main():
    # Create the camera object
    cap = idsCamera(0)

    # Load camera parameters (optional)
    cap.loadCameraParameters("camera_parameters.cset")

    # Set the region of interest (optional)
    cap.setROI(0, 0, 640, 480)

    # Synchronize the camera as master
    cap.syncAsMaster()

    # Start data acquisition
    cap.startAquisition()

    # Set exposure time (optional)
    cap.setExposureTime(20000) 

    while True:
        # Capture a frame
        frame = cap.getFrame()

        # Process the frame...

    # Close the camera and release resources
    cap.closeLibrary()

# Run the program
main()