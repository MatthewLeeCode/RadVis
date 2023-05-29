from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='radvis',
    version='0.1.2',
    url='https://github.com/medlee-code/RadVis',
    author='Matthew lee',
    author_email='matthewlee@medlee.io',
    description='A visualization tool for medical images',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'scikit-image==0.20.0',
        'pydicom==2.3.1',
        'nibabel==5.1.0',
        'matplotlib==3.7.1'
    ],
    python_requires='>=3.10',
)