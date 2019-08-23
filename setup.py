from setuptools import setup

setup(name="SX1276-python",
    version="0.1",
    description='Rough API that runs on Python for the SX1276 chip',
    url='https://github.com/linardsbi/SX1276-python',
    author='linardsbi',
    author_email='kaktoss@inbox.lv',
    license='MIT',
    packages=['SX1276'],
    install_requires=['pyA20', 'pyserial'],
    zip_safe=False)
