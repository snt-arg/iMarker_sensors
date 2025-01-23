import numpy as np

# RealSense D435i
cameraMatrix_RealSense = np.array(
    [[605.8, 0.0, 325.0],
        [0.0, 606.3, 244.8],
        [0.0, 0.0, 1.0]])

distCoeffs_RealSense = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

# iPhone 13
cameraMatrix_iPhone13 = np.array(
    [[2962.38, 0.0, 1980.12],
        [0.0, 2969.24, 1520.88],
        [0.0, 0.0, 1.0]])
distCoeffs_iPhone13 = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
