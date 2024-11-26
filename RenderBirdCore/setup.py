from setuptools import setup, find_packages

setup(
    name="RenderBirdCore",
    version="0.1.0",
    author="Wojtekb30 (Wojciech B)",
    author_email="wojtekb30.player@gmail.com",
    description="A easy to use 3D rendering engine for Python based on PyGame and OpenGL",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wojtekb30/RenderBird-Python-3D-engine",
    packages=find_packages(),
    py_modules=["RenderBirdCore"],
    install_requires=[
        "pygame>=2.0.0",
        "PyOpenGL>=3.1.6",
        "Pillow>=8.0.0",
        "numpy>=1.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
    ],
    python_requires=">=3.11",
    include_package_data=True,
)

