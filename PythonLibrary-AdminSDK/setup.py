from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cloudwinterstore',
  version='0.0.1',
  description='Admin SDK for Winterstore Cloud Storage Service',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ryan Ben',
  author_email='rbryanben@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Winterstore', 
  packages=find_packages(),
  install_requires=['requests','requests_toolbelt'] 
)
