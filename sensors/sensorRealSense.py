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
        except Exception as exception:
            print(
                f'Error occurred in createPipeline!\n{exception}', 'error')

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
        except Exception as exception:
            print(
                f'Error occurred in startPipeline!\n{exception}', 'error')

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
                f'Error occurred in grabFrames!\n{exception}', 'error')

    def getColorFrame(self, frames):
        '''
        Gets color frames from the RealSense camera.

        Parameters
        ----------
        frames: list
            Grabbed frame from the camera

        Raises
        ------
        Exception
            If an error occurs while getting a color frame.
        '''
        try:
            # Get the color frame
            colorFrame = frames.get_color_frame()
            # Convert the color frame to a numpy array
            colorImage = np.asanyarray(colorFrame.get_data())
            # Return
            return colorImage
        except Exception as exception:
            print(
                f'Error occurred in getColorFrame!\n{exception}', 'error')

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
                f'Error occurred in stopPipeline!\n{exception}', 'error')
