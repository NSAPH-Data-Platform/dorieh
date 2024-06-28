from setuptools import setup, find_packages

find_packages()
with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='dorieh',
    version="0.1.2",
    url='https://github.com/NSAPH-Data-Platform/dorieh',
    license='Apache 2.0',
    author='Michael A Bouzinier',
    author_email='mbouzinier@g.harvard.edu',
    description='Dorieh Data Engineering Platform',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    entry_points={
        'console_scripts': [
            'cwl2md=dorieh.docutils.cwl2md:main',
            'mkpgpass=dorieh.platform.util.pgpass:main',
            'copy_section=dorieh.docutils.copy_section:main',
            'collector=dorieh.docutils.collector:main',
            'dorieh_version=dorieh.version:main',
            'validate_domain=dorieh.platform.loader.validator:main'
        ],
    },
    packages=find_packages(where='./src/python') + [
        'dorieh.resources',
        'dorieh.sql',
        'dorieh.cwl'
    ],
    package_dir={
        "dorieh": "./src/python/dorieh",
        "dorieh.sql": "./src/sql",
        "dorieh.resources": "./resources",
        "dorieh.cwl": "./src/cwl"
    },
    package_data = {
        "dorieh": ["**/*.yaml", "**/*.yml"],
        "dorieh.sql": ["*.sql"],
        "dorieh.resources": ["**/*", "*/*/*", "*/*/*/*"],
        "dorieh.cwl": ["./src/cwl/*.cwl"],
        "dorieh.gis": ["data/*.csv"]
    },
    install_requires=[
        'alembic>=1.4.3',
        'apispec>=1.3.3',
        'argcomplete>=1.12.1',
        'attrs>=19.3.0',
        'Babel>=2.8.0',
        'bagit>=1.7.0',
        'boto3',
        'CacheControl>=0.11.7',
        'cached-property>=1.5.2',
        'cattrs>=1.0.0',
        'certifi>=2023.7.22',
        'chardet>=3.0.4',
        'click>=7.1.2',
        'clickclick>=20.10.2',
        'colorama>=0.4.4',
        'coloredlogs>=14.0',
        'colorlog>=4.0.2',
        'configparser>=3.5.3',
        'connexion>=2.7.0',
        'croniter>=0.3.35',
        'cwltest>=2.0.20200626112502',
        'cwltool>=3.0.20200710214758',
        'decorator>=4.4.2',
        'defusedxml>=0.6.0',
        'deprecated',
        'dill>=0.3.2',
        'dnspython>=2.0.0',
        'docker>=4.3.1',
        'docutils>=0.16',
        'funcsigs>=1.0.2',
        'future>=0.18.2',
        "geopandas",
        "geopy",
        'GitPython',
        'graphviz>=0.14.2',
        'gunicorn>=20.0.4',
        'h5py',
        'hydra-core',
        'humanfriendly>=8.2',
        'idna>=2.10',
        'importlib-metadata>=2.0.0',
        'inflection>=0.5.1',
        'iso8601>=0.1.13',
        'isodate>=0.6.0',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'json-merge-patch>=0.2',
        'jsonmerge>=1.7.0',
        'jsonschema>=3.2.0',
        'junit-xml>=1.9',
        'lazy-object-proxy>=1.5.1',
        'lockfile>=0.12.2',
        'lxml>=4.6.1',
        'Mako>=1.1.3',
        'Markdown>=2.6.11',
        'marko',
        'MarkupSafe>=1.1.1',
        'marshmallow>=2.21.0',
        'marshmallow-enum>=1.5.1',
        'marshmallow-sqlalchemy>=0.23.1',
        'mistune>=0.8.4',
        'mypy-extensions>=0.4.3',
        'myst-parser',
        'netCDF4',
        'natsort>=7.0.1',
        'networkx>=2.5',
        "numpy",
        'openapi-spec-validator>=0.2.9',
        "openpyxl",
        'pandas',
        'paramiko',
        'pyarrow',
        'pendulum>=1.4.4',
        'prison>=0.1.3',
        'prov>=1.5.1',
        'psutil>=5.7.2',
        'psycopg2-binary>=2.8.6',
        'pygeos',
        'PyGithub',
        'Pygments>=2.7.1',
        'PyJWT>=1.7.1',
        'pyparsing>=2.4.7',
        'pyresourcepool',
        'pyrsistent>=0.17.3',
        'pyshp',
        "pytest",
        'python-daemon>=2.2.4',
        'python-dateutil>=2.8.1',
        'python-editor>=1.0.4',
        'python-nvd3>=0.15.0',
        'python-slugify>=4.0.1',
        'python3-openid>=3.2.0',
        'pytz>=2020.1',
        'pytzdata>=2020.1',
        'PyYAML>=5.3.1',
        "rasterstats",
        'rdflib>=4.2.2',
        'rdflib-jsonld>=0.5.0',
        'requests',
        'rioxarray',
        "rtree",
        'ruamel.yaml>=0.16.5',
        'ruamel.yaml.clib>=0.2.2',
        'sas7bdat',
        'schema-salad>=7.0.20200811075006',
        'setproctitle>=1.1.10',
        "shapely",
        'shellescape>=3.4.1',
        'six>=1.15.0',
        'sortedcontainers',
        'sphinx',
        'sphinx_paramlinks',
        'sphinx_rtd_theme',
        'sqlparse',
        'SQLAlchemy>=1.3.20',
        'SQLAlchemy-JSONField>=0.9.0',
        'SQLAlchemy-Utils>=0.36.8',
        'tabulate>=0.8.7',
        'tenacity>=4.12.0',
        'text-unidecode>=1.3',
        'thrift>=0.13.0',
        'tornado>=6.0.4',
        "tqdm",
        'typing-extensions',
        'tzlocal>=1.5.1',
        'unicodecsv>=0.14.1',
        'urllib3>=1.25.11',
        'websocket-client>=0.57.0',
        'Werkzeug>=0.16.1',
        'zipp>=3.3.1',
        'zope.deprecation>=4.4.0',
        'sshtunnel',
        'xarray',
        'xlrd'
    ],
    extras_require = {
        "FST": [
            'rpy2',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
