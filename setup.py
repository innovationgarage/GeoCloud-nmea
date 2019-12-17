#!/usr/bin/env python

import setuptools

setuptools.setup(name='geocloud-nmea',
      version='0.7',
      description='NMEA parser service',
      long_description="""NMEA parser service""",
      long_description_content_type="text/markdown",
      author='Egil Moeller',
      author_email='egil@innovationgarage.no',
      url='https://github.com/innovationgarage/geocloud-nmea',
      packages=setuptools.find_packages(),
      install_requires=[
          'libais',
          'socket-tentacles'
      ],
      include_package_data=True,
      entry_points='''
      [console_scripts]
      geocloud-nmea = geocloud_nmea:main
      '''
  )
