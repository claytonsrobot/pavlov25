setup(
    name="pavlov3d-exe",
    version="4.1.0",
    description="MSIX packaged deployment for Pavlov 3D",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/claytonsrobot/",
    author="Clayton Bennett, Pavlov Software & Services LLC",
    author_email="pavlov3d@proton.me",
    license="None",
    classifiers=[
        "License :: None",
        "Programming Language :: Python :: 3",
    ],
    packages=["pavlov3D"],
    include_package_data=True,
    install_requires=[
        "numpy"
    ],
    entry_points={"console_scripts": ["pavlov3d=backend.__main__:main"]},
)