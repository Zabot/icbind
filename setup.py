from distutils.core import setup

setup(
    name='icbind',
    version='0.0.0',
    packages=['icbind'],
    python_requires=">=3.0",
    entry_points={
        'console_scripts': [
            'icbind = icbind.icbind:main',
            'icbind-compose = icbind.icbind_compose:main',
        ]
    },
    license='GPLv3',
    install_requires=[
        'pyyaml',
    ],
    long_description=open('readme.md').read(),
)

