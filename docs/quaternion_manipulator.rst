Module : QuaternionManipulator
==============================

----

Module overview
---------------

This module implements the class :class:`QuaternionManipulator.QuaternionManipulator`

* This class is used by the function main.
* Note that only one method of the class is public and that is :meth:`QuaternionManipulator.QuaternionManipulator.run`

----

Class : QuaternionManipulator
-----------------------------

.. automodule:: QuaternionManipulator
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:


----

Source code : QuaternionManipulator.py
-----------------------------------------------------

.. literalinclude:: ../QuaternionManipulator.py
   :language: python
   :linenos:


----

QuaternionManipulator call hierarchy
====================================

.. raw:: html

    <div class="mermaid-wrapper">

.. mermaid::

    %%{init: {
      "theme": "base",
      "darkMode": false,
      "themeVariables": {
        "background": "black",
        "primaryColor": "blue",
        "primaryTextColor": "white",
        "primaryBorderColor": "red",
        "lineColor": "orange",

        "fontSize": "24px",
        "actorFontSize": "24px",
        "messageFontSize": "24px",

        "actorBkg": "black",
        "actorBorder": "orange",
        "actorTextColor": "white",
        "actorLineColor": "green",

        "activationBkgColor": "black",
        "activationBorderColor": "green",

        "signalColor": "lightblue",
        "signalTextColor": "white",

        "loopBkgColor": "white",
        "loopTextColor": "white"
      }
    }}%%

    sequenceDiagram

        actor User

        participant QM as QuaternionManipulator
        participant EXE as Quaternion Utility
        participant PA as PlottingAgent

        User->>QM: run()

        activate QM

        QM->>QM: _set_values_from_command_line_args()

        QM->>QM: _generate_plots()

        loop while azimuth_view <= 720

            QM->>QM: _generate_plots_display_diagnostics()

            QM->>QM: _perform_quaternion_operations()

            QM->>EXE: partial_multiplication(...)
            activate EXE
            EXE-->>QM: quaternion_pre_multiply
            deactivate EXE

            QM->>EXE: rotation(...)
            activate EXE
            EXE-->>QM: quaternion_rotated
            deactivate EXE

            QM->>QM: _update_plotting_agent()

            QM->>PA: set_angle_rotation(angle)
            activate PA
            PA-->>QM:
            deactivate PA

            QM->>PA: set_quaternions(q, v, qv, v')
            activate PA
            PA-->>QM:
            deactivate PA

            QM->>PA: set_view(azimuth, elevation)
            activate PA
            PA-->>QM:
            deactivate PA

            QM->>PA: generate_plot(filename)
            activate PA
            PA-->>QM: plot saved
            deactivate PA

            QM->>QM: _update_loop_parameters()

        end

        deactivate QM

.. raw:: html

    </div>
