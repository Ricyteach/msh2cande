from setuptools import setup

setup(
    name='msh2cande',
    version='0.1',
    packages=['msh2cande'],
    url='https://github.com/Ricyteach/msh2cande',
    license='MIT',
    author='Rick Teachey',
    author_email='ricky@teachey.org',
    description='Dead simple conversion of a mesh2D file to CANDE',
    install_requires=['pandas', 'plotly']
)
