import os
import glob
import yaml
import cv2 as cv
import numpy as np


def readConfig():
    config = {}
    # Read config YAML from file
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    # Return the config
    return config


def captureStereoImagesELP():
    # Variables
    counter = 0
    # Read configurations from the config file
    config = readConfig()['configs']
    # Prepare a hint for the user
    print('- Press "s" to save the images and "ESC" to exit ...')
    # Capture the video stream
    capL = cv.VideoCapture(config['elp']['ports']['lCam'])
    capR = cv.VideoCapture(config['elp']['ports']['rCam'])
    # Loop to capture images
    while capL.isOpened() and capR.isOpened():
        # Read the frames
        succesL, imgL = capL.read()
        succesR, imgR = capR.read()
        # Need flip the image
        imgR = cv.flip(imgR, 1)
        # Check for any stoppage
        key = cv.waitKey(5)
        if key == 27:
            break
        # Run the code
        elif key == ord('s'):  # wait for 's' key to save and exit
            cv.imwrite(f'{config["outputPath"]}/imgL/image' +
                       str(counter) + '.png', imgL)
            cv.imwrite(f'{config["outputPath"]}/imgR/image' +
                       str(counter) + '.png', imgR)
            counter += 1
        # Show the images
        cv.imshow('Image Left', imgL)
        cv.imshow('Image Right', imgR)
    # Release and destroy all windows before termination
    capL.release()
    capR.release()
    # Stop
    cv.destroyAllWindows()


def stereoCalibration(cameraType: str):
    # Read configurations from the config file
    config = readConfig()['configs']
    # Variables
    imagePointsL = []
    imagePointsR = []
    points3dArray = []  # 3d point in real world space
    imageSize = config['elp']['imageSize']
    chessboardDims = config['calibration']['chessboardDims']
    chessboardSquareSize = config['calibration']['chessboardSquareSize']
    # Read the images
    imagesLeft = sorted(glob.glob(f'{config["outputPath"]}imgL/*.png'))
    imagesRight = sorted(glob.glob(f'{config["outputPath"]}imgR/*.png'))
    # Termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objectPoints = np.zeros(
        (chessboardDims[0] * chessboardDims[1], 3), np.float32)
    objectPoints[:, :2] = np.mgrid[0:chessboardDims[0],
                                   0:chessboardDims[1]].T.reshape(-1, 2)
    objectPoints *= chessboardSquareSize
    # Loop through the images to find the corners
    for imgLeft, imgRight in zip(imagesLeft, imagesRight):
        # Read the images
        imgL = cv.imread(imgLeft)
        imgR = cv.imread(imgRight)
        # Convert to grayscale
        grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
        grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        retL, cornersL = cv.findChessboardCorners(grayL, chessboardDims, None)
        retR, cornersR = cv.findChessboardCorners(grayR, chessboardDims, None)
        # If found, add object points, image points (after refining them)
        if retL and retR == True:
            # Append the points
            points3dArray.append(objectPoints)
            # Add the corners
            cornersL = cv.cornerSubPix(
                grayL, cornersL, (11, 11), (-1, -1), criteria)
            cornersR = cv.cornerSubPix(
                grayR, cornersR, (11, 11), (-1, -1), criteria)
            imagePointsL.append(cornersL)
            imagePointsR.append(cornersR)
            # Draw and display the corners
            cv.drawChessboardCorners(imgL, chessboardDims, cornersL, retL)
            cv.drawChessboardCorners(imgR, chessboardDims, cornersR, retR)
            cv.imshow('Image Left', imgL)
            cv.imshow('Image Right', imgR)
            cv.waitKey(1000)
    cv.destroyAllWindows()
    # I. Calibrating Each Camera Individually
    print("- Calibrating the cameras individually ...")
    heightL, widthL, channelsL = imgL.shape
    heightR, widthR, channelsR = imgR.shape
    retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(
        points3dArray, imagePointsL, imageSize, None, None)
    retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(
        points3dArray, imagePointsR, imageSize, None, None)
    newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(
        cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))
    newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(
        cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))
    # II. Calibrating the stereo vision system
    print("- Calibrating the stereo vision system ...")
    flags = 0
    flags |= cv.CALIB_FIX_INTRINSIC
    # Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
    # Hence intrinsic parameters are the same
    stereoCriteria = (cv.TERM_CRITERIA_EPS +
                      cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
    retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(
        points3dArray, imagePointsL, imagePointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], stereoCriteria, flags)
    # III. Rectification
    print("- Rectifying the stereo vision system ...")
    rectifyScale = 1
    rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv.stereoRectify(
        newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale, (0, 0))
    stereoMapL = cv.initUndistortRectifyMap(
        newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
    stereoMapR = cv.initUndistortRectifyMap(
        newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)
    print("- Saving parameters ...")
    cvFile = cv.FileStorage(
        f'{config["outputPath"]}{cameraType}StereoMap.xml', cv.FILE_STORAGE_WRITE)
    cvFile.write('stereoMapL_x', stereoMapL[0])
    cvFile.write('stereoMapL_y', stereoMapL[1])
    cvFile.write('stereoMapR_x', stereoMapR[0])
    cvFile.write('stereoMapR_y', stereoMapR[1])
    cvFile.release()


def getCalibrationParams(cameraType: str):
    # Get the current path
    currentPath = os.getcwd()
    # Read the calibration parameters
    cvFile = cv.FileStorage(
        f'{currentPath}/output/{cameraType}StereoMap.xml', cv.FILE_STORAGE_READ)
    stereoMapL_x = cvFile.getNode('stereoMapL_x').mat()
    stereoMapL_y = cvFile.getNode('stereoMapL_y').mat()
    stereoMapR_x = cvFile.getNode('stereoMapR_x').mat()
    stereoMapR_y = cvFile.getNode('stereoMapR_y').mat()
    cvFile.release()
    # Return the calibration parameters
    return stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y
