from setuptools import setup, find_packages

import json
import os


if __name__ == '__main__':
      setup(name='clean-folder-18042023',
            version='0.0.3dev',
            description='Clean, parser and normolize folders package',
            url='https://github.com/Kagev',
            author='Kagev',
            author_email='kagev@example.com',
            readme = "README.md",
            packages=['clean-folder'],
            install_requires=['markdown'],
            classifiers = [   "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                              "Operating System :: OS Independent",
            ]
      
            )