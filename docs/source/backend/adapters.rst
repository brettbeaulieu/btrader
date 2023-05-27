========
Adapters
========

Usage
-----
    Adapters act as a bridge between various exchange APIs and the rest of the program. They are primarily responsible for converting the exchange API's data into a common format that the rest of the program can understand.
    Adapters are implemented as a class that inherits from the :ref:`BaseAdapter` class.

Implemented Adapters
~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 3
    
   adapters/bitget

.. _BaseAdapter:

Base Adapter
~~~~~~~~~~~~

.. autoclass:: source.adapters.base.BaseAdapter
   :members: 