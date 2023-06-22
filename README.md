# CSR Detector - Sensors

![Sensors](docs/cameraSetups.png "Sensors")

This repository contains the interfaces for the hardware that uses **CSR Marker Detector**. The current version of the code supports cameras introduced below:

| Camera | Interface | Links and Description |
| ------------ | ------------ | ------------ |
| ELP-USB8MP02G-L75 | USB 2.0 | HD 8MP Camera UVC SONY IMX179 CMOS - [link](http://www.webcamerausb.com/elp-8mp-highdefinition-usb-camera-module-usb20-sony-imx179-color-cmos-sensor-75degree-lens-p-45.html) |
| iDS U3-3271LE-C-HQ Rev.1.2 | USB 3.0 and uEye+ | Sony Pregius IMX265 3 MP - [link](https://en.ids-imaging.com/store/u3-3271le-rev-1-2.html) |
| RealSense D435(i) | USB 3.0 and RS library | RealSense Depth Camera D435 4 MP - [link](https://www.intelrealsense.com/depth-camera-d435/) |


## 🎥 Interface Installation

Generally, the sensors are connected to a beamsplitter to provide exact outputs at the same time (as shown the cover image). However, there are some investigations to use a single camera for detecting CSR-based materials.

### I. ELP Cameras

For ELP cameras, the only required interfaces are USB 2.0 interfaces. Accordingly, the usage of the sensor is "plug & play." First, install the required library (OpenCV) using the command `pip install opencv-python`.

### II. iDS Cameras

For iDS cameras, it is necessary to install **iDS Peak** library and its Python binding according to [this link](https://en.ids-imaging.com/download-details/AB03448.html). Accordingly, you need to follow the steps described below:

1. Go to the [downloads](https://en.ids-imaging.com/downloads.html) web-page of iDS and search for the camera name (in this case, U3-3271LE-C-HQ Rev.1.2). Choose the proper OS and download the file according to it (without uEye Transport Layer), such as *IDS peak 2.4 for Linux 64-bit - Debian package*.
2. Follow the instructions provided in [this (Ubuntu)](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-linux-readme-2.4_EN.html) or [this (Windows)](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html) to install the files.
    - [Ubuntu] you first need to install libraries using `pip install libqt5core5a libqt5gui5 libqt5widgets5 libqt5quick5 qml-module-qtquick-window2 qml-module-qtquick2 qml-module-qtquick-dialogs qml-module-qtquick-controls qml-module-qtquick-layouts libusb-1.0-0 libqt5multimedia5`. Then, you can go to the path you downloaded the **ids-peak** file and run `sudo apt install ./ids-peak_[version]_[arch].deb`.
3. Finally, you should add the below Python bindings to make it work. You can also access the binding `whl` files from [this directory](/docs/iDS/):

- `Windows 64bit` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html)):
    - Go to *C:\Program Files\IDS\ids_peak\generic_sdk\api\binding\python\wheel\x86_[32|64]*
    - Choose "File > Open Windows PowerShell" in Windows Explorer.
    - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win_amd64.whl`
    - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win_amd64.whl`

- `Windows 32Bit` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html)):
    - Go to *C:\Program Files\IDS\ids_peak\generic_sdk\api\binding\python\wheel\x86_[32|64]*
    - Choose "File > Open Windows PowerShell" in Windows Explorer.
    - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win32.whl`
    - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win32.whl`

- `Linux` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-linux-readme-2.4_EN.html)):
    - Go to */usr/local/share/ids/bindings/python/wheel/* 
    - Run `pip install ids_peak-1.4.3.0-cp38-cp38-linux_x86_64.whl`
    - Run `pip install ids_peak_ipl-1.5.0.0-cp38-cp38-linux_x86_64.whl`


### III. RealSense Cameras

For RealSense cameras, the required interfaces are USB 3.0 interfaces. Install the required libraries (OpenCV and PyRealSense) using the command `pip install opencv-python pyrealsense2`.


### Installation

After installing proper interfaces, install the package using `pip install -e .` to install the packages.

## 🚀 Running the Code

For working with each of the mentioned sensors, there are some functions defined:

### ELP Cameras

The functions defined for this sensor are located in `sensorUSB.py` file and it contains:

- `createCameraObject`: creates an openCV `VideoCapture` object given a port number.
- `grabImage`: grabs the `VideoCapture` object and returns the frame.

### iDS Cameras

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

### RealSense Cameras

The functions defined for this sensor are located in `sensorRealSense.py` file and it contains:

- `createPipeline`: creates a pipeline for the RealSense camera.
- `startPipeline`: starts a pipeline for the RealSense camera.
- `grabFrames`: grabs frames from camera.
- `getColorFrame`: gets color frames from the RealSense camera.
- `stopPipeline`: stops the pipeline and releases memory.


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