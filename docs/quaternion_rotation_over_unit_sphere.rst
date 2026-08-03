Module : quaternion_rotation_over_unit_sphere
=============================================

----


Module overview
---------------

This module is the entry point for the quaternion rotation visualisation
application.

It contains a single function called main which implements the program.

The program:

* Creates an object of class :class:`QuaternionManipulator.QuaternionManipulator`
* Checks that the correct number of arguments were passed in from the command line.
* Invokes the :meth:`QuaternionManipulator.QuaternionManipulator.run` method of the :class:`QuaternionManipulator.QuaternionManipulator` object which was created.
* Once invoked, the object should generate the required plots.

----


Command line entry point
------------------------

.. automodule:: quaternion_rotation_over_unit_sphere
   :members:

----


Source code : quaternion_rotation_over_unit_sphere.py
-----------------------------------------------------

.. literalinclude:: ../quaternion_rotation_over_unit_sphere.py
   :language: python
   :linenos:
