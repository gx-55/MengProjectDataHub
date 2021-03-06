import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MengProjectDataHub", # Replace with your own username
    version="0.0.2",
    author="GengqiaoXie",
    author_email="gx55@cornell.edu",
    description="Data processing tools for Meng Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gx-55/MengProjectDataHub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)