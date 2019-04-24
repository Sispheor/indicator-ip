import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='indicator-ip',
    version='0.1',
    scripts=['indicator-ip'],
    author="Nicolas Marcq",
    author_email="nico.marcq@gmail.com",
    description="Show all interface IP in gnome taskbar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sispheor/indicator-ip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
