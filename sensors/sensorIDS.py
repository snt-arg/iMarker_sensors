from ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl


class idsCamera:
    def __init__(self, port):
        '''
        IDS Camera class for interacting with IDS peak library.

        Parameters
        ----------
        port: int
            Port number of the camera that is connected.
        '''
        # Initialize the camera manager
        try:
            ids_peak.Library.Initialize()
            deviceManager = ids_peak.DeviceManager.Instance()
            deviceManager.Update()

            self.cap = deviceManager.Devices()[port].OpenDevice(
                ids_peak.DeviceAccessType_Exclusive)

            self.nodemap = self.cap.RemoteDevice().NodeMaps()[0]

            self.nodemap.FindNode(
                "AcquisitionMode").SetCurrentEntry("Continuous")
            self.datastream = None
            self.buffer = None
            self.frame = None
        except Exception as exception:
            print(
                f'- Error occurred in initializing the iDS camera with port# {port}!\n- {exception}', 'error')

    def loadCameraParameters(self, file):
        '''
        Loads camera parameters from a yaml file.

        Parameters
        ----------
        file: str
            Path to the yaml file containing camera parameters.

        Raises
        ------
        Exception
            If an error occurs while loading parameters from the file.
        '''
        try:
            self.nodemap.LoadFromFile(file)
        except Exception as exception:
            print(
                f'- Error occurred in loading camera parameters!\n- {exception}', 'error')

    def setROI(self, xNew, yNew, widthNew, heightNew):
        try:
            '''
            Sets a Region of Interest (ROI) for the camera.

            Parameters
            ----------
            xNew: int
                The x-coordinate of the top-left corner of the ROI.
            yNew: int
                The y-coordinate of the top-left corner of the ROI.
            widthNew: int
                The width of the ROI.
            heightNew: int
                The height of the ROI.

            Raises
            ------
            Exception
                If an error occurs while setting the ROI.
            '''
            # Get the current ROI
            x = self.nodemap.FindNode("OffsetX").Value()
            y = self.nodemap.FindNode("OffsetY").Value()
            w = self.nodemap.FindNode("Width").Value()
            h = self.nodemap.FindNode("Height").Value()

            # Get the minimum ROI
            x_min = self.nodemap.FindNode("OffsetX").Minimum()
            y_min = self.nodemap.FindNode("OffsetY").Minimum()
            w_min = self.nodemap.FindNode("Width").Minimum()
            h_min = self.nodemap.FindNode("Height").Minimum()

            # Set the minimum ROI. This removes any size restrictions due to previous ROI settings
            self.nodemap.FindNode("OffsetX").SetValue(x_min)
            self.nodemap.FindNode("OffsetY").SetValue(y_min)
            self.nodemap.FindNode("Width").SetValue(w_min)
            self.nodemap.FindNode("Height").SetValue(h_min)

            x = xNew
            y = yNew
            width = widthNew
            height = heightNew

            # Set the valid ROI
            self.nodemap.FindNode("OffsetX").SetValue(x)
            self.nodemap.FindNode("OffsetY").SetValue(y)
            self.nodemap.FindNode(
                "Width").SetValue(width)
            self.nodemap.FindNode(
                "Height").SetValue(height)
        except Exception as exception:
            print(
                f'- Error occurred in setting ROI!\n- {exception}', 'error')

    def syncAsMaster(self):
        '''
        Synchronizes the camera as a master.

        Raises
        ------
        Exception
            If an error occurs while synchronizing the camera.
        '''
        try:
            self.nodemap.FindNode(
                "TimerSelector").SetCurrentEntry("Timer0")
            self.nodemap.FindNode("TimerDuration").SetValue(1000)
            self.nodemap.FindNode(
                "TimerTriggerSource").SetCurrentEntry("Off")

            self.nodemap.FindNode("LineSelector").SetCurrentEntry("Line2")
            self.nodemap.FindNode("LineMode").SetCurrentEntry("Output")
            self.nodemap.FindNode(
                "LineSource").SetCurrentEntry("Timer0Active")

            self.nodemap.FindNode("LineInverter").SetValue(True)

            self.nodemap.FindNode(
                "TriggerSelector").SetCurrentEntry("ExposureStart")
            self.nodemap.FindNode("TriggerMode").SetCurrentEntry("On")
            self.nodemap.FindNode(
                "TriggerSource").SetCurrentEntry("Line2")
            self.nodemap.FindNode(
                "TriggerActivation").SetCurrentEntry("RisingEdge")
        except Exception as exception:
            print(
                f'- Error occurred in syncing the master camera!\n- {exception}', 'error')

    def syncAsSlave(self):
        '''
        Synchronizes the camera as a slave.

        Raises
        ------
        Exception
            If an error occurs while synchronizing the camera.
        '''
        try:
            self.nodemap.FindNode(
                "LineSelector").SetCurrentEntry("Line2")
            self.nodemap.FindNode("LineMode").SetCurrentEntry("Input")

            self.nodemap.FindNode(
                "TriggerSelector").SetCurrentEntry("ExposureStart")

            self.nodemap.FindNode("TriggerMode").SetCurrentEntry("On")
            self.nodemap.FindNode(
                "TriggerSource").SetCurrentEntry("Line2")
            self.nodemap.FindNode(
                "TriggerActivation").SetCurrentEntry("RisingEdge")
        except Exception as exception:
            print(
                f'- Error occurred in syncing the slave camera!\n- {exception}', 'error')

    def startAquisition(self):
        '''
        Starts the data acquisition from the camera.

        Raises
        ------
        Exception
            If an error occurs while starting the acquisition.
        '''
        try:
            self.datastream = self.cap.DataStreams()[0].OpenDataStream()
            self.payload_size = self.nodemap.FindNode("PayloadSize").Value()
            for i in range(self.datastream.NumBuffersAnnouncedMinRequired()):
                buffer = self.datastream.AllocAndAnnounceBuffer(
                    self.payload_size)
                self.datastream.QueueBuffer(buffer)

            self.datastream.StartAcquisition()
            self.nodemap.FindNode("AcquisitionStart").Execute()
            self.nodemap.FindNode("AcquisitionStart").WaitUntilDone()
        except Exception as exception:
            print(
                f'- Error occurred in starting frame acquisition!\n- {exception}', 'error')

    def setExposureTime(self, exposureTime):
        '''
        Sets the given exposure time for the camera.

        Parameters
        ----------
        exposureTime: float
            The exposure time to set in milliseconds.

        Raises
        ------
        Exception
            If an error occurs while setting the exposure time.
        '''
        try:
            self.nodemap.FindNode("ExposureTime").SetValue(exposureTime)
        except Exception as exception:
            print(
                f'- Error occurred in setting the exposure time!\n- {exception}', 'error')

    def getFrame(self):
        '''
        Triggers the camera to capture a frame and returns the frame as a numpy array.

        Returns
        -------
        np.ndarray
            The captured frame as a numpy array.

        Raises
        ------
        Exception
            If an error occurs while capturing the frame.
        '''
        try:
            # trigger image
            self.nodemap.FindNode("TimerReset").Execute()

            self.buffer = self.datastream.WaitForFinishedBuffer(1000)

            # obtain image and convert from IPL to numpy array
            self.raw_image = ids_peak_ipl.Image_CreateFromSizeAndBuffer(self.buffer.PixelFormat(
            ), self.buffer.BasePtr(), self.buffer.Size(), self.buffer.Width(), self.buffer.Height())

            self.color_image = self.raw_image.ConvertTo(
                ids_peak_ipl.PixelFormatName_BGR8)

            # queue buffer to be used again
            self.datastream.QueueBuffer(self.buffer)

            self.frame = self.color_image.get_numpy_3D()

            return self.frame

        except Exception as exception:
            print(
                f'- Error occurred in getting frames!\n- {exception}', 'error')

    def getCalibrationConfig(self, rootPath: str, fileName: str):
        '''
        Gets the calibration configuration for the camera.
        '''
        self.loadCameraParameters(f"{rootPath}/{fileName}.cset")

    def closeLibrary(self):
        '''
        Closes the IDS peak library and releases associated resources.
        '''
        ids_peak.Library.Close()
