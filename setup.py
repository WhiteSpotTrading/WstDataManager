from setuptools import setup
from pip.req import parse_requirements

setup(name='WstDataManager',
      version='0.1',
      description='Library of classes for maintaining Data used in WST-trading services',
      url='https://github.com/WhiteSpotTrading/WstDataManager',
      author='CarlWestman',
      author_email='carl.westman@gmail.com',
      license='None',
      packages=['WstDataManager', 'WstDataManager.morningstar'],
      install_requires = [
          'lxml',
          're',
          'datetime',
          'requests'
      ],
      zip_safe=False)