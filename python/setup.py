import glob
from setuptools import setup

setup(
    name="mraspberry-scripts",
    version="1.0",
    author="Matthew Raspberry",
    author_email="3092450+mraspberry@users.noreply.github.com",
    scripts=glob.glob("bin/*"),
    description="Personal scripts",
)
