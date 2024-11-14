import cv2


def createCameraObject(port):
    '''
    Creates an openCV `VideoCapture` object given a port number.

    Parameters
    ----------
    port: int
        Port number of the camera that is connected

    Returns
    -------
    ret: cv2.VideoCapture
        VideoCapture object
    '''
    return cv2.VideoCapture(port)


def grabImage(videoCap):
    '''
    Grabs the `VideoCapture` object and returns the frame.

    Parameters
    ----------
    videoCap: cv2.VideoCapture
        VideoCapture object

    Returns
    -------
    ret: videoCap.read()
        boolean value of the returned frame.
    '''
    return videoCap.read()


def getCameraParameters(videoCap):
    '''
    Retrieves basic intrinsic camera parameters from the `VideoCapture` object.

    Parameters
    ----------
    videoCap: cv2.VideoCapture
        VideoCapture object.

    Returns
    -------
    cameraParams: dict
        A dictionary containing focal length, frame width and height.
        Note: Limited by OpenCV's `VideoCapture` capabilities.
    '''
    # Capture width and height (resolution)
    frameWidth = int(videoCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Estimate focal length using a default field of view if needed
    # Focal length approximation (this will not be accurate without calibration)
    focalLength = (frameWidth + frameHeight) / 2

    cameraParams = {
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

    return cameraParams
