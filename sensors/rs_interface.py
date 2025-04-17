import numpy as np
import pyrealsense2 as rs


class rsCamera:
    def __init__(self, resolution: tuple = (640, 480), fps: int = 30):
        '''
        RealSense Camera class for interacting with PyRealSense library.

        Parameters
        ----------
        resolution: tuple
            The pair of width and length of the camera resolution
        fps: int
            The frame-rate of the camera
        '''
        # Initialize class values
        self.fps = fps
        self.config = None
        self.pipeline = None
        self.frameWidth = resolution[0]
        self.frameHeight = resolution[1]

    def createPipeline(self):
        '''
        Creates a pipeline for the RealSense camera.

        Returns
        -------
        pipeline: dict
            The created pipeline of the camera
        config: dict
            The configurations file of the camera

        Raises
        ------
        Exception
            If an error occurs while creating a pipeline.
        '''
        try:
            # Get the configurations
            self.config = rs.config()
            # Create an stream based on the given values
            self.config.enable_stream(
                rs.stream.color, self.frameWidth, self.frameHeight, rs.format.bgr8, self.fps)
            # Create a pipeline for the RealSense camera
            self.pipeline = rs.pipeline()
            # Inform the user
            print('- Pipeline created successfully!')
        except Exception as exception:
            print(
                f'- Error occurred while creating a RealSense pipeline!\n- {exception}', 'error')

    def startPipeline(self):
        '''
        Starts a pipeline for the RealSense camera.

        Raises
        ------
        Exception
            If an error occurs while starting a pipeline.
        '''
        try:
            # Start the pipeline
            self.pipeline.start(self.config)
            # Inform the user
            print('- Pipeline started successfully!')
            return True
        except Exception as exception:
            print(
                f'- Error occurred while starting the pipeline!\n- {exception}', 'error')
            return False

    def grabFrames(self):
        '''
        Grabs frames from camera.

        Raises
        ------
        Exception
            If an error occurs while grabbing a frame.
        '''
        try:
            # Start the pipeline
            frames = self.pipeline.wait_for_frames()
            # Return
            return frames
        except Exception as exception:
            print(
                f'- Error occurred while trying to grab frames!\n- {exception}', 'error')

    def getColorFrame(self, frames):
        '''
        Gets color frames from the RealSense camera.

        Parameters
        ----------
        frames: numpy.ndarray
            Grabbed frame from the camera

        Returns
        -------
        colorImage: numpy.ndarray
            The color image from the camera
        cameraMatrix: numpy.ndarray
            The camera matrix of the color camera
        distCoeffs: numpy.ndarray
            The distortion coefficients of the color camera
        '''
        try:
            # Initializations
            colorCamIntrinsics = None
            # Get the color frame
            colorFrame = frames.get_color_frame()
            # Get intrinsics of the color camera
            if colorFrame:
                colorCamIntrinsics = colorFrame.profile.as_video_stream_profile().intrinsics
                # Extract the intrinsic parameters
                fx = colorCamIntrinsics.fx
                fy = colorCamIntrinsics.fy
                ppx = colorCamIntrinsics.ppx
                ppy = colorCamIntrinsics.ppy
                # Create the camera matrix
                cameraMatrix = np.array([[fx, 0, ppx],
                                        [0, fy, ppy],
                                        [0,  0,   1]], dtype=np.float32)
                # Create the distortion coefficients array
                distCoeffs = np.array(
                    colorCamIntrinsics.coeffs, dtype=np.float32)
            # Convert the color frame to a numpy array
            colorImage = np.asanyarray(colorFrame.get_data())
            # Return
            return colorImage, cameraMatrix, distCoeffs
        except Exception as exception:
            print(
                f'- Error occurred while getting color frames!\n- {exception}', 'error')

    def stopPipeline(self):
        '''
        Stops the pipeline and releases memory.

        Raises
        ------
        Exception
            If an error occurs while stopping the pipeline.
        '''
        try:
            # Start the pipeline
            self.pipeline.stop()
        except Exception as exception:
            print(
                f'- Error occurred while stopping the pipeline!\n- {exception}', 'error')
