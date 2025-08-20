from setuptools import setup, find_packages

from cvxlab.version import __version__

setup(
    name='cvxlab',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'cvxpy',
        'openpyxl',
        'pytest',
    ],
    author='Matteo V. Rocco',
    author_email='matteovincenzo.rocco@polimi.it',
    description='A Python-embedded, open-source modeling laboratory for convex numerical optimization problems.',
    url='https://github.com/cvxlab/cvxlab',
)
