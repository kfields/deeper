
****************
Installation
****************


From PyPI
#########

TLDR - do this at your own risk
-------------------------------

.. code:: bash

    pip install deeper-rpg

Recommended - pipX
------------------

If you don't already have it installed go to https://pypi.org/project/pipx/ for instructions

.. code:: bash

    pipx install deeper-rpg

And then run it!
----------------

.. code:: bash

    deeper


From GitHub
###########

Clone the repository

.. code:: bash

        git clone https://github.com/kfields/deeper.git
        
Navigate to the new directory which contains the repository

.. code:: bash

        cd deeper

If you don't have Poetry, learn to install it at: https://python-poetry.org/docs/

TLDR:  (Use Git Bash if your running Windows)

.. code:: bash

        curl -sSL https://install.python-poetry.org | python3 -

Activate the environment

.. code:: bash

        poetry shell

Install required packages

.. code:: bash

        poetry install

Build the Rust Extension

You need to have Rust installed: https://www.rust-lang.org/tools/install

.. code:: bash

        maturin develop


And then run the app!
----------------------

.. code:: bash

    deeper

