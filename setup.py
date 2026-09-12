from setuptools import setup, find_packages

find_packages()
with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='dorieh',
    version="0.5.1.post2",
    url='https://github.com/ForomePlatform/dorieh',
    project_urls={
        'Documentation': 'https://foromeplatform.github.io/dorieh/',
        'Cite as (book)': 'https://doi.org/10.1007/978-3-032-21032-6',
        'Software DOI': 'https://doi.org/10.5281/zenodo.22728722',
        'How to cite': 'https://foromeplatform.github.io/dorieh/citing.html',
    },
    license='Apache 2.0',
    author='Michael A Bouzinier',
    author_email='mbouzinier@g.harvard.edu',
    description='Dorieh Data Engineering Platform',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'cwl2md=dorieh.docutils.cwl2md:main',
            'mkpgpass=dorieh.platform.util.pgpass:main',
            'copy_section=dorieh.docutils.copy_section:main',
            'collector=dorieh.docutils.collector:main',
            'dorieh_version=dorieh.version:main',
            'validate_domain=dorieh.platform.loader.validator:main',
            'export_dashboard=dorieh.platform.superset.export_dashboard:main',
            'import_dashboard=dorieh.platform.superset.import_dashboard:main',
            'cleanup_dashboard=dorieh.platform.superset.cleanup_dashboard:main'
        ],
    },
    packages=find_packages(where='./src/python') + [
        'dorieh.resources',
        'dorieh.sql',
        'dorieh.cwl',
        'dorieh.workflows'
    ],
    package_dir={
        "dorieh": "./src/python/dorieh",
        "dorieh.sql": "./src/sql",
        "dorieh.resources": "./resources",
        "dorieh.cwl": "./src/cwl",
        "dorieh.workflows": "./src/workflows"
    },
    package_data = {
        "dorieh": ["**/*.yaml", "**/*.yml"],
        "dorieh.sql": ["*.sql"],
        "dorieh.resources": ["**/*", "*/*/*", "*/*/*/*"],
        "dorieh.cwl": ["*.cwl"],
        "dorieh.workflows": ["*.cwl"],
        "dorieh.gis": ["data/*.csv"]
    },
    python_requires='>=3.12',
    install_requires=[
        'aiohttp',
        'argcomplete>=1.12.1',
        'boto3',
        'certifi>=2024.7.4',
        'cwltest>=2.0.20200626112502',
        'cwltool>=3.0.20200710214758',
        'deprecated',
        'fiona>=1.10.1',
        'fsspec',
        'geopandas',
        'geopy',
        'GitPython',
        'googlesearch-python',
        'graphviz>=0.14.2',
        'h5py',
        'hydra-core',
        'humanfriendly>=8.2',
        'importlib-metadata>=2.0.0',
        'isodate>=0.6.0',
        'Markdown>=2.6.11',
        'marko',
        'MarkupSafe>=1.1.1',
        'mypy-extensions>=0.4.3',
        'myst-parser',
        'netCDF4',
        "numpy",
        "openpyxl",
        'pandas',
        'paramiko',
        'pyarrow',
        'psutil>=5.7.2',
        'psycopg2-binary>=2.8.6',
        'PyGithub',
        'pyresourcepool',
        'pyshp',
        "pytest",
        'python-dateutil>=2.8.1',
        'PyYAML>=5.3.1',
        "rasterstats",
        'requests>=2.32.4',
        'rioxarray',
        "rtree",
        'ruamel.yaml>=0.16.5',
        'ruamel.yaml.clib>=0.2.2',
        'sas7bdat',
        'schema-salad>=7.0.20200811075006',
        'setproctitle>=1.1.10',
        "shapely>=2.1.2",
        'shellescape>=3.4.1',
        'six>=1.15.0',
        'sortedcontainers',
        'sphinx',
        'sphinx_paramlinks',
        'sphinx_rtd_theme',
        'sphinxcontrib-mermaid',
        'sphinx-togglebutton',
        'sqlparse',
        "tqdm>=4.66.3",
        'typing-extensions',
        'tzlocal>=1.5.1',
        'unicodecsv>=0.14.1',
        'urllib3>=2.5.0',
        'websocket-client>=0.57.0',
        'sshtunnel',
        'xarray',
        'xlrd'
    ],
    extras_require = {
        "FST": [
            'rpy2',
        ],
        "spark": [
            'pyspark',
            'pyhive'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
