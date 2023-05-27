============
Installation
============

Naturally, this project requires that Python 3.6+ is installed on your system. To install the required packages, you can either use a virtual environment or install the packages manually.

Windows
-------

Virtual Environment
~~~~~~~~~~~~~~~~~~~

To install on windows, simply run the following command within the root directory::

   .\install_venv.bat

The batch file will create a virtual environment and install all the required packages, as specified in 'requirements.txt'.

Manual Installation
~~~~~~~~~~~~~~~~~~~

To install without a virtual environment, run the following command within the root directory::

   pip install -r requirements.txt

.. note::
   This will install the packages globally on your system. It's recommended to use a virtual environment instead, and avoid any dependency conflicts with other projects.
