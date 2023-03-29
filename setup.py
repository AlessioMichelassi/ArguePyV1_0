from setuptools import setup, find_packages

setup(
    name='ArguePy',
    version='1.0',
    packages=find_packages(),
    long_description=open('readMe.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlessioMichelassi/ArguePyV1_0',
    license='GPL',
    author='Alessio Michelassi',
    author_email='alessio.michelassi@gmail.com',
    description='python code editor',
    install_requires=['PySide6'],
    entry_points={'console_scripts': ['arguepy=arguepy.main:main']}
)
