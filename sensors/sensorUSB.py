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
