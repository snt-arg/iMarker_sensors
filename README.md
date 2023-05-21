# csr_sensors
A repository to keep different sensors of CSR detector setup

# IDS Camera Class Documentation

The `idsCamera` class provides a convenient interface for interacting with IDS cameras using the IDS peak library in Python. This documentation aims to provide an overview of the class and its methods to help users understand how to utilize it in their projects.

## Class Initialization

### `__init__(self, port)`

**Description:** Initializes the IDS camera object.

**Parameters:**
- `port` (int): Port number of the camera that is connected.

## Camera Configuration

### `loadCameraParameters(self, file)`

**Description:** Loads camera parameters from a YAML file.

**Parameters:**
- `file` (str): Path to the YAML file containing camera parameters.

### `setROI(self, xNew, yNew, widthNew, heightNew)`

**Description:** Sets the region of interest (ROI) for the camera.

**Parameters:**
- `xNew` (int): The x-coordinate of the top-left corner of the ROI.
- `yNew` (int): The y-coordinate of the top-left corner of the ROI.
- `widthNew` (int): The width of the ROI.
- `heightNew` (int): The height of the ROI.

### `syncAsMaster(self)`

**Description:** Synchronizes the camera as a master for triggering.

### `syncAsSlave(self)`

**Description:** Synchronizes the camera as a slave for synchronization with a master camera.

### `setExposureTime(self, exposureTime)`

**Description:** Sets the exposure time for the camera.

**Parameters:**
- `exposureTime` (float): The exposure time to set in milliseconds.

## Data Acquisition

### `startAquisition(self)`

**Description:** Starts the data acquisition from the camera.

### `getFrame(self)`

**Description:** Triggers the camera to capture a frame and returns the frame as a NumPy array.

**Returns:**
- `np.ndarray`: The captured frame as a NumPy array.

## Library Cleanup

### `closeLibrary(self)`

**Description:** Closes the IDS peak library and releases associated resources.

## Example Usage

Below is an example of how to use the `idsCamera` class:

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