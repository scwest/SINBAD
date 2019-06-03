from setuptools import setup

import subprocess
import os

setup(
      name = 'SINBAD',
      version = '2.0',
      description = 'description',
      author = 'Sean West',
      url = 'tbd',
      packages = ['multi_granularity_graphs'],
      package_data = {
                      '':['docs/*']
                      },
      entry_points = {
                      'console_scripts':[
                                         'sinbad = multi_granularity_graphs.control:smain'
                                         ]
                      },
      long_description = 'Construct potential PPI mechanism changes using survival analysis results.',
      classifiers = ['Programming Language :: Python', \
                     'Programming Language :: Python :: 3', \
                     'Operating System :: Unix', \
                     'Development Status :: 1 - Planning', \
                     'Intended Audience :: Science/Research', \
                     'Topic :: Scientific/Engineering :: Bio-Informatics', \
                     'Topic :: Scientific/Engineering :: Mathematics', \
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', \
                     'Natural Language :: English']
      )










