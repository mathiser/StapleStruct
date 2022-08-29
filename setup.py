from setuptools import setup, find_namespace_packages

setup(name='StapleStruct',
      packages=find_namespace_packages(include=["StapleStruct", "StapleStruct.*"]),
      version='0.1',
      description='Wrapper of dcmrtstruct2nii, simpleitk and rt-utils, which allows a direct STAPLE of rtstruct-files',
      url='',
      author='Mathis Ersted Rasmussen',
      author_email='mathis.rasmussen@rm.dk',
      license='Apache License Version 2.0, January 2004',
      install_requires=[
            "simpleitk", "dcmrtstruct2nii", "rt_utils", "pydicom"
      ],
      keywords=['']
      )
