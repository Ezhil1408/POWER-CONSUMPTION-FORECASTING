from setuptools import setup, find_packages

setup(
    name='power-consumption-forecasting-for-smart-grids',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A data-driven system for forecasting power consumption in smart grids using PySpark.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyspark>=3.0.0',
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'scikit-learn>=0.24.0',
        'pyyaml>=5.3.1',
        'jupyter>=1.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)