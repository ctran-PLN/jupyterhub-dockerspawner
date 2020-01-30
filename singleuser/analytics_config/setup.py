import setuptools

setuptools.setup(
    name="vibrent_analytics_config",
    version="0.0.1",
    author="Cat Din Tran",
    description="An abstract class for allowing to connect to PMI, PMI-PRD and PMT databases",
    packages=['analytics_config'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
