from ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl
import numpy as np


def createCameraObjectIDS(port):
    '''
    Creates an IDS Device object and a nodemap.

    Parameters
    ----------
    port: int
        port number of the camera that is connected

    Returns
    -------
    cap: ids_peak.Device (unsure of the type)
        camera capture object
    nodemap: ids_peak.Nodemap
        camera nodemap
    '''
    # initialize the camera manager
    ids_peak.Library.Initialize()
    device_manager = ids_peak.DeviceManager.Instance()
    device_manager.Update()

    cap = device_manager.Devices()[port].OpenDevice(
        ids_peak.DeviceAccessType_Exclusive)

    nodemap = cap.RemoteDevice().NodeMaps()[0]

    nodemap.FindNode(
        "AcquisitionMode").SetCurrentEntry("Continuous")

    return cap, nodemap


def loadCameraParameters(nodemap, file):
    '''
    Loads camera parameters from a yaml file.

    Parameters
    ----------
    nodemap: ids_peak.Nodemap
        camera nodemap
    file: str
        path to the yaml file containing camera parameters

    Raises
    ------
    Exception:
        if an error occurs while loading parameters from file
    '''
    try:
        nodemap.LoadFromFile(file)
    except Exception as exception:
        print(
            f'Error occurred in loadCameraParameters!\n{exception}', 'error')


def syncAsMaster(nodemap):
    '''
    Synchronizes the camera as a master.

    Parameters
    ----------
    nodemap: ids_peak.Nodemap
        camera nodemap

    Returns
    -------
    bool:
        True if synchronization is successful, False otherwise

    Raises
    ------
    Exception:
        if an error occurs while synchronizing the camera
    '''
    try:
        nodemap.FindNode(
            "TimerSelector").SetCurrentEntry("Timer0")
        nodemap.FindNode("TimerDuration").SetValue(1000)
        nodemap.FindNode(
            "TimerTriggerSource").SetCurrentEntry("Off")

        nodemap.FindNode("LineSelector").SetCurrentEntry("Line2")
        nodemap.FindNode("LineMode").SetCurrentEntry("Output")
        nodemap.FindNode(
            "LineSource").SetCurrentEntry("Timer0Active")

        nodemap.FindNode("LineInverter").SetValue(True)

        nodemap.FindNode(
            "TriggerSelector").SetCurrentEntry("ExposureStart")
        nodemap.FindNode("TriggerMode").SetCurrentEntry("On")
        nodemap.FindNode(
            "TriggerSource").SetCurrentEntry("Line2")
        nodemap.FindNode(
            "TriggerActivation").SetCurrentEntry("RisingEdge")
        return True
    except Exception as exception:
        print(
            f'Error occurred in syncAsMaster!\n{exception}', 'error')
        return False


def syncAsSlave(nodemap):
    '''
    Synchronizes the camera as a slave.

    Parameters
    ----------
    nodemap: ids_peak.Nodemap
        camera nodemap

    Returns
    -------
    bool:
        True if synchronization is successful, False otherwise

    Raises
    ------
    Exception:
        if an error occurs while synchronizing the camera
    '''
    try:
        nodemap.FindNode(
            "LineSelector").SetCurrentEntry("Line2")
        nodemap.FindNode("LineMode").SetCurrentEntry("Input")

        nodemap.FindNode(
            "TriggerSelector").SetCurrentEntry("ExposureStart")

        nodemap.FindNode("TriggerMode").SetCurrentEntry("On")
        nodemap.FindNode(
            "TriggerSource").SetCurrentEntry("Line2")
        nodemap.FindNode(
            "TriggerActivation").SetCurrentEntry("RisingEdge")
        return True
    except Exception as exception:
        print(
            f'Error occurred in syncAsSlave!\n{exception}', 'error')
        return False


def startAquisition(cap, nodemap):
    '''
    Starts the data acquisition from the camera and returns the data stream and buffer.

    Parameters
    ----------
    cap: ids_peak.Device
        camera capture object
    nodemap: ids_peak.Nodemap
        camera nodemap

    Returns
    -------
    datastream: ids_peak.DataStream
        the data stream for the camera
    buffer: ids_peak.Buffer
        the buffer for the data stream
    '''
    try:
        datastream = cap.DataStreams()[0].OpenDataStream()
        payload_size = nodemap.FindNode("PayloadSize").Value()
        for i in range(datastream.NumBuffersAnnouncedMinRequired()):
            buffer = datastream.AllocAndAnnounceBuffer(payload_size)
            datastream.QueueBuffer(buffer)

        datastream.StartAcquisition()
        nodemap.FindNode("AcquisitionStart").Execute()
        nodemap.FindNode("AcquisitionStart").WaitUntilDone()
        return datastream, buffer
    except Exception as exception:
        print(
            f'Error occurred in startAquisition!\n{exception}', 'error')


def setExposureTime(nodemap, exposureTime):
    '''
    Sets the exposure time for the camera.

    Parameters
    ----------
    nodemap: ids_peak.Nodemap
        camera nodemap
    exposureTime: float
        the exposure time to set in ms

    Returns
    -------
    bool
        True if the exposure time was successfully set, False otherwise
    '''
    try:
        nodemap.FindNode("ExposureTime").SetValue(exposureTime)
        return True
    except Exception as exception:
        print(
            f'Error occurred in setExposureTime!\n{exception}', 'error')
        return False


def getFrame(nodemap, datasream, buffer):
    '''
    Triggers the camera to capture a frame and returns the frame as a numpy array.

    Parameters
    ----------
    nodemap: ids_peak.Nodemap
        camera nodemap
    datastream: ids_peak.DataStream
        the data stream for the camera
    buffer: ids_peak.Buffer
        the buffer for the data stream

    Returns
    -------
    np.ndarray
        the captured frame as a numpy array
    '''
    try:
        # trigger image
        nodemap.FindNode("TimerReset").Execute()

        buffer = datasream.WaitForFinishedBuffer(1000)

        # obtain image and convert from IPL to numpy array
        raw_image = ids_peak_ipl.Image_CreateFromSizeAndBuffer(buffer.PixelFormat(
        ), buffer.BasePtr(), buffer.Size(), buffer.Width(), buffer.Height())

        color_image = raw_image.ConvertTo(
            ids_peak_ipl.PixelFormatName_BGR8)

        # queue buffer to be used again
        datasream.QueueBuffer(buffer)

        frame = color_image.get_numpy_3D()

        return frame

    except Exception as exception:
        print(
            f'Error occurred in getFrame!\n{exception}', 'error')


def closeLibrary():
    ids_peak.Library.Close()
