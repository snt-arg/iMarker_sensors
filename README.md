# iMarker Detector Sensor Interfaces

![Sensors](docs/cameraSetups.png "Sensors")

This repository contains the interfaces for acquiring visual data from the hardware desgined for **iMarker Detection**. It is mainly used alongside [the detector algorithms](https://github.com/snt-arg/csr_detector) and wrapped by [GUI-enabled standalone version](https://github.com/snt-arg/csr_detector_standalone) and [ROS-based version](https://github.com/snt-arg/csr_detector_ros) frameworks.

The current version of the code supports the vision sensors listed below, but it can extend to cover others in the future:

| Sensor                                                                       | Interface              | Description                                                                                                                                                                   |
| ---------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ELP-USB8MP02G-L75](https://github.com/snt-arg/csr_sensors#usb-cam)          | USB 2.0                | HD 8MP Camera UVC SONY IMX179 CMOS - [link](http://www.webcamerausb.com/elp-8mp-highdefinition-usb-camera-module-usb20-sony-imx179-color-cmos-sensor-75degree-lens-p-45.html) |
| [iDS U3-3271LE-C-HQ Rev.1.2](https://github.com/snt-arg/csr_sensors#ids-cam) | USB 3.0 and uEye+      | Sony Pregius IMX265 3MP - [link](https://en.ids-imaging.com/store/u3-3271le-rev-1-2.html)                                                                                     |
| [intel RealSense D435(i)](https://github.com/snt-arg/csr_sensors#rs-cam)     | USB 3.0 and RS library | RealSense Depth Camera D435 4MP - [link](https://www.intelrealsense.com/depth-camera-d435/)                                                                                   |

## ⚒️ Sensors Setup <a id="setup"></a>

The hardware to detect iMarkers and CSRs are designed in two ways:

- **A. Dual-vision Setup:** a homogeneous perception system containing two (synchronized) cameras fixed perpendicular to each other in a pack, facing two different surfaces of an optical component, _i.e.,_ a beamsplitter. Setups designed for [ELP](https://github.com/snt-arg/csr_sensors#usb-cam) and [iDS](https://github.com/snt-arg/csr_sensors#ids-cam) cameras are the designed solutions.
- **B. Single-vision Setup:** a single camera with a polarizer (fixed or changable) attached to its lens. [RealSense](https://github.com/snt-arg/csr_sensors#rs-cam) is used for this purpose.

## ⚙️ Installation

As different sensors come with different hardware/software interfaces, picking the proper interface for using the sensor is essential. The required libraries to be installed are listed below:

### ELP Cameras <a id="usb-cam"></a>

For ELP cameras, the only required interface is **USB 2.0**, making the usage of the sensor as "plug & play." Thus, you only need to install OpenCV using the command `pip install opencv-python` (tested with `opencv-python>4.10`).

### iDS Cameras (Optional) <a id="ids-cam"></a>

iDS cameras require **USB 3.0** and **iDS Peak** library and its Python binding introduced in [this link](https://en.ids-imaging.com/download-details/AB03448.html). Thus, you need to follow the steps described below:

1. Go to the [downloads](https://en.ids-imaging.com/downloads.html) section of iDS website and search for the camera name (in this case, `U3-3271LE-C-HQ Rev.1.2`). Choose the proper OS (Ubuntu, Windows, or Mac) and download the file (without uEye Transport Layer), such as _IDS peak 2.4 for Linux 64-bit - Debian package_.
2. Follow the instructions provided in [this (Ubuntu)](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-linux-readme-2.4_EN.html) or [this (Windows)](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html) links to install the files. As a summary:
   - [Ubuntu] you first need to install libraries using `sudo apt install libqt5core5a libqt5gui5 libqt5widgets5 libqt5quick5 qml-module-qtquick-window2 qml-module-qtquick2 qml-module-qtquick-dialogs qml-module-qtquick-controls qml-module-qtquick-layouts libusb-1.0-0 libqt5multimedia5`. Then, go to the path you downloaded the **ids-peak** file and run `sudo apt install ./ids-peak_[version]_[arch].deb`.
3. Finally, you should add the below Python bindings to make it work. You can also access the binding `whl` files from [this directory](/docs/iDS/):

- `Windows 64bit` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html)):

  - Go to _C:\Program Files\IDS\ids*peak\generic_sdk\api\binding\python\wheel\x86*[32|64]_
  - Choose "File > Open Windows PowerShell" in Windows Explorer.
  - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win_amd64.whl`
  - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win_amd64.whl`

- `Windows 32bit` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-windows-readme-2.4_EN.html)):

  - Go to _C:\Program Files\IDS\ids*peak\generic_sdk\api\binding\python\wheel\x86*[32|64]_
  - Choose "File > Open Windows PowerShell" in Windows Explorer.
  - Run: `pip install src/IDS/Windows/ids_peak_ipl-1.6.0.0-cp310-cp310-win32.whl`
  - Run: `pip install src/IDS/Windows/ids_peak-1.5.0.0-cp310-cp310-win32.whl`

- `Linux` ([link](https://en.ids-imaging.com/files/downloads/ids-peak/readme/ids-peak-linux-readme-2.4_EN.html)):
  - Go to _/usr/local/share/ids/bindings/python/wheel/_
  - Run `pip install ids_peak-1.4.3.0-cp38-cp38-linux_x86_64.whl`
  - Run `pip install ids_peak_ipl-1.5.0.0-cp38-cp38-linux_x86_64.whl`

### RealSense Cameras <a id="rs-cam"></a>

For RealSense cameras, the required interface is **USB 3.0**. Install the libraries using the command `pip install opencv-python pyrealsense2`.

## 📑 Code Structure

It should be noted that this repository contains the functions to use the introduced sensors in the `/sensors/` directory, described as below:

- **A. ELP USB Camera:** in `sensorUSB.py`, you can find functions `createCameraObject` and `grabImage` for creating camera objects and grabbing the frames, respectively.
- **B. iDS Camera:** in `sensorIDS.py`, you can find below functions:
  - `loadCameraParameters`: loading camera parameters from a yaml file
  - `setROI`: setting a Region of Interest (ROI) for the camera
  - `syncAsMaster`: synchronizing a camera as a master
  - `syncAsSlave`: synchronizing a camera as a slave
  - `startAquisition`: starting data acquisition from the camera
  - `setExposureTime`: setting the given exposure time for the camera
  - `getFrame`: triggering the camera to capture a frame and returns the frame as a numpy array
  - `getCalibrationConfig`: getting the calibration configuration for the camera
  - `closeLibrary`: closing the IDS peak library and releases associated resources
- **C. RealSense Camera:** in `sensorRealSense.py`, you can find below functions:
  - `createPipeline`: creating a pipeline for the RealSense camera
  - `startPipeline`: starting the pipeline for the RealSense camera
  - `grabFrames`: grabbing frames from the RealSense camera
  - `getColorFrame`: fetching color frames from the RealSense camera
  - `stopPipeline`: stopping the pipeline and releasing memory

## Calibration

You might need to calibrate the cameras, specially for the dual-vision sensors, if you are using the sensor for the first time. To do this, follow the instructions in the [calibration page](/src/csr_sensors/sensors/calibration/README.md).

## 🚀 Running the Code

⚠️ As mentioned before, the current repository is a sub-module and wrapped by [GUI-enabled standalone version](https://github.com/snt-arg/csr_detector_standalone) and [ROS-based version](https://github.com/snt-arg/csr_detector_ros) frameworks. Accordingly, take a look at the mentioned repositories to see examples of using sensors.

As an example, you can find a sample of running iDS cameras to fetch frames:

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
```
