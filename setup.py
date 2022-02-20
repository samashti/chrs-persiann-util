import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chrs_persiann_util",
    version="1.0.0",
    author="Nikhil S Hubballi",
    author_email="nikhil@samashti.space",
    description="A utility to search, download global level PERSIANN precipitation data from CHRS Data Portal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samashti/chrs-persiann-util",
    packages=['chrs_persiann'],
    install_requires=['setuptools'],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
)
