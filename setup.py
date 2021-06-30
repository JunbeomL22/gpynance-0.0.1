from setuptools import setup, find_packages
from gpynance.utils._numbautils import cc as utilscc

setup(name='gpynance',
      version='0.0.1',
      description='Testing installation of Package',
      url='',
      author='Junbeom Lee',
      author_email='junbeoml22@gmail.com',
      license='MIT',
      packages=find_packages(),
      ext_modules=[utilscc.distutils_extension()],
      zip_safe=False)
