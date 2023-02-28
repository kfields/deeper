
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

If you don't have Hatch, learn to install it at: https://hatch.pypa.io/latest/install/

TLDR:

.. code:: bash

        pipx install hatch

Activate the environment and install dependencies

.. code:: bash

        hatch shell

Build the Rust Extension

You need to have Rust installed: https://www.rust-lang.org/tools/install

.. code:: bash

        hatch run develop


And then run the app!
----------------------

.. code:: bash

    deeper

