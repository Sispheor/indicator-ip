import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='indicator-ip',
    version='1.0',
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
    python_requires='>=3.6',
    entry_points={
        'console_scripts':
            ['indicator-ip = indicator_ip:main']
    },
    include_package_data=True,
    package_data={
        'indicator_ip': ['images/*.png']
    }
)

