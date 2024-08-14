import numpy as np

# Homography matrix for iDS cameras
# Structure: [[scaling x-axis, skewing x-axis, shift x-axis]
#             [skewing y-axis, scaling y-axis, shift y-axis]
#             [perspective x-axis, perspective y-axis, scaling all]]
homographyMatList = {
    'Settings1': np.array([[1.01621457e+00,  3.58445420e-02, -2.44065632e+01],
                          [-9.84581954e-03,  1.02765380e+00, -1.40367861e+01],
                          [4.41648502e-06,  3.15020103e-05,  1.00000000e+00]]),
    'Settings2': np.array([[1.00810034e+00, -8.35518266e-03,  8.24430129e+00],
                          [5.04865290e-03,  1.01568339e+00, -2.56132273e+00],
                          [-6.06091127e-06,  1.69549217e-05,  1.00000000e+00]]),
    'Settings3': np.array([[1.03330539e+00, -2.33383557e-02,  7.86579611e+00],
                           [2.72445070e-02,  1.01455844e+00, -1.21160907e+01],
                           [2.72468851e-05, -5.08436884e-06,  1.00000000e+00]]),
    'Settings4': np.array([[9.99409645e-01, -1.55228281e-02, -3.79768922e+00],
                           [1.65593615e-02,  1.00673047e+00, -4.11314756e+00],
                           [-9.96470609e-06, 1.68764309e-05,  1.00000000e+00]]),
    'Settings5': np.array([[1.01572100e+00, -1.51550480e-02, -9.08269647e+00],
                           [1.91107875e-02,  1.01081982e+00, -4.37920015e+00],
                           [-4.06011658e-06, 1.52890809e-05,  1.00000000e+00]])
}
homographyMat = homographyMatList['Settings4']
