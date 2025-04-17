from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='imarker_sensors',
        version='1.0.0',
        author='Ali Tourani',
        author_email='ali.tourani@uni.lu',
        description='Interfaces for various sensors (ELP, iDS, RealSense) to detect iMarkers',
        long_description='A Python package providing clean interfaces for connecting to multiple camera sensors used in iMarker detection setups.',
        long_description_content_type='text/plain',
        url='https://github.com/snt-arg/imarker_sensors',
        packages=find_packages(include=['sensors', 'sensors.*']),
        install_requires=[
            'numpy>=1.24.4',
            'opencv-python>=4.10.0.84',
            'pyrealsense2>=2.55.1.6486',
        ],
        python_requires='>=3.8',
    )
