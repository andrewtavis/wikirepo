try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='wikirepo',
    version='0.0.1',
    description='Python based ETL and ELT tools for Wikidata',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    license='new BSD',
    url="https://github.com/andrewtavis/wikirepo",
    author='Andrew Tavis McAllister',
    author_email='andrew.t.mcallister@gmail.com'
)

install_requires = [
    'numpy',
    'scipy',
    'pandas',
    'matplotlib',
    'seaborn',
    'wikidata',
    'dateutil',
    'tqdm'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)