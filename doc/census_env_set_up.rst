Setting Up Environment
======================

Here are the steps for setting up the environment. Please make sure that you have `anaconda <https://docs.anaconda.com/anaconda/install/index.html>`_ installed on your system. You can also install `miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, which is the lightweight version of anaconda. On HPC systmes you may need to load the modules. Developers environment requires extra packages and libraries to surpport generating documentation.   

    -  Researchers: use ``environment.yml``
    -  Developers: use ``environment_dev.yml``

The following exmaples are based on `environment_dev.yml` file.

Setting up a new environment
----------------------------

If you have not set up any environment for the project, you need to create a new environment. The following command will generate a new environment using the `environment_dev.yml` file. 

.. code-block:: console

    $ conda env create --name your_env_name --file environment_dev.yml 


Updating an existing environment
--------------------------------

If you have set up the environment and you want to make sure that it is the latest version, you can use the following command.

.. code-block:: console

    $ conda env update --name your_env_name --file environment_dev.yml 

After setting up the environment, you need to install the `census` package. 

Installing census
-----------------

Navigate to the package folder and use the following code to install the package.

.. code-block:: console

    $ pip3 install -e .

``-e`` flag installs the package in the development mode. As a result, you do not need to reintall the package by chaning the code.




Setting up Census API Key
-------------------------

In order to interact with the US Census API at scale, you'll a Census API
key. You can get one `here <https://api.census.gov/data/key_signup.html>`_. Once
you have your key, you'll need to add it to your environment. You can either do that
through ``conda`` (``conda env config vars set CENSUS_API_KEY=<your key>``), setting
the key directly in your ``.rc`` file, or by using the ``get_census.set_api_key`` function
(this only affects your current session, and isn't permanent).


Registering the Conda Kernal
----------------------------

If you plan onn testing the package using Jupyter Notebook, you need to register the package using the following command:

.. code-block:: console

    $ conda activate your_env_name
    $ python3 -m ipykernel install --user --name your_env_name


Updating the Environment Recipe
-------------------------------

If you added new features to the package which is dependent on a library that is not available in the current environment, you need to update the environment recipe. While the conda environment is activated, use the following command:

.. code-block:: console

    $ conda env export > environment_dev.yml

Make sure to manually remove `name` and `prefix` sections as well as `dorieh`
from the dependencies section in the `.yml` file.





