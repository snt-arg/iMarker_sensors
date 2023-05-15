import cv2


def createCameraObject(port):
    '''
    Creates an openCV VideoCapture object.

    Parameters
    ----------
    port: int
        port number of the camera that is connected

    Returns
    -------
    cameraObject: cv2.VideoCapture
        VideoCapture object
    '''
    return cv2.VideoCapture(port)


def grabImage(videoCap):
    '''
    returns the VideoCapture frame and return value.

    Parameters
    ----------
    videoCap: cv2.VideoCapture
        VideoCapture object

    Returns
    -------
    ret: bool
        boolean value of the returned frame.
    frame: numpy.ndarray
        Image
    '''
    return videoCap.read()
