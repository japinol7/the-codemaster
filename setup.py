from setuptools import setup

setup(
    name='codemaster',
    author='Joan A. Pinol  (japinol)',
    version='0.0.14',
    license='MIT',
    description="The CodeMaster",
    long_description="The CodeMaster. Nightmare on Bots' Island",
    url='https://github.com/japinol7/the-codemaster',
    packages=['codemaster'],
    python_requires='>=3.13',
    install_requires=['pygame-ce', 'pygame-gui'],
    entry_points={
        'console_scripts': [
            'codemaster=codemaster.__main__:main',
            ],
    },
)
