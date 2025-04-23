"""
📝 'iMarker Detector Sensor Interfaces' Software
    SPDX-FileCopyrightText: (2025) University of Luxembourg
    © 2025 University of Luxembourg
    Developed by: Ali TOURANI et al. at SnT / ARG.

'iMarker Detector Sensor Interfaces' is licensed under the "SNT NON-COMMERCIAL" License.
You may not use this file except in compliance with the License.

-----------------------------------------------

📝 USB Camera Interface Module

This module provides a simple OpenCV-based interface for working with
plug-and-play USB cameras (e.g., ELP). It allows you to initialize a camera,
capture frames, and retrieve basic intrinsic parameters.
"""

import cv2
from typing import Tuple, Dict


def createCameraObject(port: int = 0) -> cv2.VideoCapture:
    """
    Creates an OpenCV `VideoCapture` object given a port number.

    Parameters
    ----------
    port: int, optional
        Port number for the camera. Default is 0 (usually the first detected camera).

    Returns
    -------
    camObj: cv2.VideoCapture
        An initialized OpenCV `VideoCapture` object for the specified port.
    """
    # Create a VideoCapture object
    camObj = cv2.VideoCapture(port)

    # Check if the camera opened successfully
    if not camObj.isOpened():
        raise RuntimeError(f"Camera on port {port} could not be opened.")

    # Return the VideoCapture object
    return camObj


def grabImage(videoCap: cv2.VideoCapture) -> Tuple[bool, any]:
    """
    Reads a frame from an open `VideoCapture` object.

    Parameters
    ----------
    videoCap: cv2.VideoCapture
        OpenCV VideoCapture object.

    Returns
    -------
    ret: videoCap.read()
        A tuple containing a boolean indicating if the frame was read successfully.
    """
    return videoCap.read()


def getCameraParameters(videoCap: cv2.VideoCapture) -> Dict[str, float]:
    """
    Retrieves basic intrinsic parameters from the `VideoCapture` object.
    This function assumes a simple pinhole camera model and uses the
    camera's resolution to estimate the focal length and principal point.
    The distortion model is assumed to be 'plumb_bob' with zero coefficients.
    This is a simplified approach and may not be accurate for all cameras.

    Parameters
    ----------
    videoCap: cv2.VideoCapture
        OpenCV `VideoCapture` object.

    Returns
    -------
    camParams: dict
        A dictionary containing:
        - width, height: Image dimensions.
        - focal_length: Estimated focal length.
        - fx, fy: Approximated focal lengths along x and y.
        - ppx, ppy: Principal point coordinates (assumed image center).
        - distortion_model: Distortion model (assumed 'plumb_bob').
        - coeffs: Distortion coefficients (assumed zero for simplicity).
    """
    # Capture width and height (resolution)
    frameWidth = int(videoCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Estimate focal length using a default FoV if needed
    focalLength = (frameWidth + frameHeight) / 2

    # Create a dictionary to hold camera parameters
    camParams = {
        'width': frameWidth,
        'height': frameHeight,
        'focal_length': focalLength,
        'fx': focalLength,
        'fy': focalLength,
        'ppx': frameWidth / 2,
        'ppy': frameHeight / 2,
        'distortion_model': 'plumb_bob',
        'coeffs': [0, 0, 0, 0, 0]
    }

    # Return the camera parameters
    return camParams
