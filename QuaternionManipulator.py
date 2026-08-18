import sys
import math
import subprocess

# Import the Numerical Python package, aka numpy, along with its definition of quaternion.

import numpy as np
import quaternion

import GlobalSettings
from   PlottingAgent import PlottingAgent


class QuaternionManipulator :

    def __init__(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        self.title_plots  = "Rotating a vector (v) around a quaternion (q)."

        self.counter_loop = 0

        # Rotation parameters.
        # --------------------

        self.angle_rotation_full      = 0
        self.angle_rotation_start     = 0
        self.angle_rotation_increment = 5
        self.angle_rotation           = self.angle_rotation_start

        #

        self.quaternion_axis_rotation = np.quaternion(0, 0, 0, 0)
        self.quaternion_to_rotate     = np.quaternion(0, 0, 0, 0)
        self.quaternion_pre_multiply  = np.quaternion(0, 0, 0, 0)
        self.quaternion_rotated       = np.quaternion(0, 0, 0, 0)

        # View parameters.
        # ----------------

        # Azimuth

        self.azimuth_view_start       = 280
        self.azimuth_view_increment   = 2.5

        self.azimuth_view             = self.azimuth_view_start

        # Elevation

        self.elevation_view_start     = 28
        self.elevation_view_increment = 0

        self.elevation_view           = self.elevation_view_start

        self.plottingAgent            = PlottingAgent(self.title_plots)


    def run(self) :

        nameMethod  = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._set_values_from_command_line_args()
        self._generate_plots()

        print(nameMethod + " : Exit")


    def _set_values_from_command_line_args(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        # Set values based on the arguments which were passed in from the command line.

        self.verbose_operation   = sys.argv[1]
        self.operation_type      = sys.argv[2]
        self.axis_x              = float(sys.argv[3])
        self.axis_y              = float(sys.argv[4])
        self.axis_z              = float(sys.argv[5])
        self.angle_rotation_full = float(sys.argv[6])
        self.vector_x            = float(sys.argv[7])
        self.vector_y            = float(sys.argv[8])
        self.vector_z            = float(sys.argv[9])

        # Set up the appropriate values for the rotation.

        self.quaternion_axis_rotation = np.quaternion(0, self.axis_x,   self.axis_y,   self.axis_z)
        self.quaternion_to_rotate     = np.quaternion(0, self.vector_x, self.vector_y, self.vector_z)


    def _preMultiplyVectorUsingQuaternion(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        operation_type = "partial_multiplication"


        result = subprocess.run(
            [
             GlobalSettings.utility_quaternion_rotation,
             str(self.verbose_operation),
             operation_type,
             str(self.quaternion_to_rotate.x),
             str(self.quaternion_to_rotate.y),
             str(self.quaternion_to_rotate.z),
             str(math.radians(self.angle_rotation)),
             str(self.quaternion_axis_rotation.x),
             str(self.quaternion_axis_rotation.y),
             str(self.quaternion_axis_rotation.z)
            ],
            capture_output=True,
            text=True
        )

        # Convert the string into a list of strings, breaking the original string at "," symbols.

        string_quaternion = (result.stdout).split(",")

        self.quaternion_pre_multiply.w = float(string_quaternion[0])
        self.quaternion_pre_multiply.x = float(string_quaternion[1])
        self.quaternion_pre_multiply.y = float(string_quaternion[2])
        self.quaternion_pre_multiply.z = float(string_quaternion[3])

        # print(result.stdout)
        # print(result.stderr)
        # print(result.returncode)

        return self.quaternion_pre_multiply


    def _rotateVectorUsingQuaternion(self) :

        operation_type = "rotation"


        result = subprocess.run(
            [
             GlobalSettings.utility_quaternion_rotation,
             str(self.verbose_operation),
             operation_type,
             str(self.quaternion_to_rotate.x),
             str(self.quaternion_to_rotate.y),
             str(self.quaternion_to_rotate.z),
             str(math.radians(self.angle_rotation)),
             str(self.quaternion_axis_rotation.x),
             str(self.quaternion_axis_rotation.y),
             str(self.quaternion_axis_rotation.z)
            ],
            capture_output=True,
            text=True
        )

        # Convert the string into a list of strings, breaking the original string at "," symbols.

        string_quaternion = (result.stdout).split(",")

        self.quaternion_rotated.w = float(string_quaternion[0])
        self.quaternion_rotated.x = float(string_quaternion[1])
        self.quaternion_rotated.y = float(string_quaternion[2])
        self.quaternion_rotated.z = float(string_quaternion[3])

        # print(result.stdout)
        # print(result.stderr)
        # print(result.returncode)

        return self.quaternion_rotated


    def _perform_quaternion_operations(self) :

        self._preMultiplyVectorUsingQuaternion()
        self._rotateVectorUsingQuaternion()


    # Invoked by : _generate_plots

    def _update_plotting_agent(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        # Pass the necessary data to the plotting agent.

        print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
        print(nameMethod + " : About to invoke : plotAgent.set_angle_rotation")

        self.plottingAgent.set_angle_rotation(self.angle_rotation)

        self.plottingAgent.set_quaternions_and_min_max_values(

            self.quaternion_axis_rotation,
            self.quaternion_to_rotate,
            self.quaternion_pre_multiply,
            self.quaternion_rotated
        )
        self.plottingAgent.set_view(

            self.azimuth_view,
            self.elevation_view
        )


    # Invoked by : _generate_plots

    def _update_loop_parameters(self) :

        self.counter_loop   += 1
        angle_rotation_next  = (self.counter_loop * self.angle_rotation_increment) + self.angle_rotation_start

        # The quaternionic rotation might stop, but the view can still keep spinning around.
        #
        # Check for this.

        if angle_rotation_next <= self.angle_rotation_full :

            self.angle_rotation = angle_rotation_next

        self.azimuth_view = (self.counter_loop * self.azimuth_view_increment) + self.azimuth_view_start


    def _generate_plots_display_diagnostics(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + f" : self.counter_loop = {self.counter_loop:d}")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f"Azimuth view = {self.azimuth_view:f}")


    # Invoked by : run

    def _generate_plots(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        while self.azimuth_view <= 720 :

            self._generate_plots_display_diagnostics()

            filename = f"rotation-{self.counter_loop:04d}.png"

            # - Perform the next set of quaternion operations.
            # - Update the Plotting agent with the results of this quaternion rotation.
            # - Instruct the Plotting agent to generate the new plot.

            self._perform_quaternion_operations()
            self._update_plotting_agent()

            self.plottingAgent.generate_plot(filename)

            self._update_loop_parameters()

            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print()

        print(nameMethod + " : Exit")