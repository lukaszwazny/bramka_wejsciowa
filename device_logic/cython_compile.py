from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Faster accelerometer',
    ext_modules=cythonize('accelerometer_faster.pyx'),
    zip_safe=False,
)