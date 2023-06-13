from setuptools import find_packages, setup

setup(name='csr_sensors',
      version='1.0',
      author='Ali Tourani',
      description='CSR detector sensors',
      url='https://github.com/snt-arg/csr_sensors',
      packages=find_packages(
          include=['sensors']),
      install_requires=[
          'numpy',
          'opencv-python',
          'pyrealsense2'
      ],
      )
