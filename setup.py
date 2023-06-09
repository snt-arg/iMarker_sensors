from setuptools import find_packages, setup

setup(name='csr_sensors',
      version='1.0',
      description='CSR detector with GUI',
      author='Ali Tourani',
      url='https://github.com/snt-arg/csr_sensors',
      packages=find_packages(
          include=['sensors']),
      install_requires=[
          'numpy',
          'opencv-python',
      ],
      )
