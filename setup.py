from setuptools import setup, find_packages

setup(
    name="monitor_manager",
    version="1.0.0",
    description="Monitor configuration manager for Linux using kscreen-doctor.",
    author="Your Name",
    author_email="xyzjohnjung@gmail.com",
    url="https://github.com/yourusername/monitor_manager",  # Falls du es hostest
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'monitormanager=monitormanager.main:main',  # Befehl für CLI
        ],
    },
    install_requires=[],  # Falls du Abhängigkeiten hast, hier angeben
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)