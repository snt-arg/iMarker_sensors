"""
🎯 Stereo Camera Calibration Script for ELP

This script captures stereo images using ELP cameras, performs calibration,
and displays sample parameters from the result.
"""

import os
from utils import (
    stereoCalibration,
    captureStereoImages,
    getCalibrationParams,
)


def main():
    print("Camera calibration started ...")

    # Step 1 - Capture images
    print("Capturing stereo images ...")
    captureStereoImages()

    # Step 2 - Run stereo calibration
    print("Running stereo calibration ...")
    stereoCalibration('elp')
    print("Calibration completed!\n")

    # Step 3 - Display sample calibration results
    print("Loading calibration parameters from output ...")
    # Get the current path
    currentPath = os.getcwd()
    outputFilePath = f'{currentPath}/output/elpStereoMap.xml'
    if not os.path.exists(outputFilePath):
        print(f"[Error] Calibration file not found at: {outputFilePath}")
        return

    sample = getCalibrationParams(outputFilePath)
    # Convert to integer and show a few elements from one of the maps (e.g., stereoMapL_x)
    sampleInt = sample[0].astype(int)

    print("Sample integers from stereoMapL_x:")
    print(sampleInt.flatten()[:5])  # Show first 5 values


# Run the main function
if __name__ == '__main__':
    main()
