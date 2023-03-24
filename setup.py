from setuptools import setup, find_packages

setup(
    name='ArguePy',
    version='v 1.0',
    packages=find_packages(),
    url='https://github.com/AlessioMichelassi/ArguePyV1_0',
    license='GPL',
    author='Alessio Michelassi',
    author_email='alessio.michelassi@gmail.com',
    description='python code editor',
    install_requires=['PyQt5'],
    entry_points={'console_scripts': ['arguepy=arguepy.main:main']}
)
