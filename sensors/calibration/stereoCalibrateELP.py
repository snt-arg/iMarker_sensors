import os
from utils import captureStereoImagesELP, stereoCalibration, getCalibrationParams


def main():
    print("Camera calibration started ...")
    # Step#1 - Capture some images
    print("Capturing stereo images ...")
    captureStereoImagesELP()
    # Step#2 - Calibrate the stereo camera
    print("Now, calibration based on the captured images ...")
    stereoCalibration('elp')
    print("Calibration completed!")
    # Step#3 - Show the calibration results
    print("Use getCalibrationParams('elp') to access the calibration parameters. Sample: ")
    # Get the current path
    currentPath = os.getcwd()
    filePath = f'{currentPath}/output/elpStereoMap.xml'
    sample = getCalibrationParams(filePath)
    # Convert to integer and show a few elements from one of the maps (e.g., stereoMapL_x)
    sample_int = sample[0].astype(int)
    print("Sample integers from stereoMapL_x:")
    print(sample_int.flatten()[:5])  # Display the first 5 elements as integers


# Run the main function
if __name__ == '__main__':
    main()
