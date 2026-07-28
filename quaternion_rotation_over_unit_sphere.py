import sys
import colorsys
import math
from   matplotlib        import font_manager
import subprocess
import numpy             as np

# Import the Numerical Python package, aka numpy.

import numpy as np
import quaternion

# Import the Python Image Library, aka PIL.

import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from PlottingAgent import PlottingAgent


# Global settings used by this program.

utility_quaternion_rotation = "/home/craig/local/source_code/haskell/HaskellQuaternionRotation/dist-newstyle/build/x86_64-linux/ghc-9.14.1/quaternion-0.1.0.0/x/quaternion/build/quaternion/quaternion"
verbose_operation           = "False"

show_plots = False

plot_quaternion_pre_multiply_history = True
plot_quaternion_rotated_history      = False

rgb_value = colorsys.hsv_to_rgb(1.0, 1.0, 1.0)


class VectorManipulator :

    def __init__(self) :

        self.title_plots = "Rotating a vector (v) around a quaternion (q)."

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


    def start(self) :

        self.run()


    def run(self) :

        nameMethod = "VectorManipulator::run"


        print(nameMethod + " : Enter")

        self.set_values_from_command_line_args()

        # Generate the plots.

        self.generate_plots()

        print(nameMethod + " : Exit")


    def set_values_from_command_line_args(self) :

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


    def preMultiplyVectorUsingQuaternion(self) :

        nameMethod     = "preMultiplyVectorUsingQuaternion"

        operation_type = "partial_multiplication"


        result = subprocess.run(
            [
             utility_quaternion_rotation,
             verbose_operation,
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


    def rotateVectorUsingQuaternion(self) :

        operation_type = "rotation"


        result = subprocess.run(
            [
             utility_quaternion_rotation,
             verbose_operation,
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


    def perform_quaternion_operations(self) :

        self.preMultiplyVectorUsingQuaternion()
        self.rotateVectorUsingQuaternion()


    def update_plotting_agent(self) :

        nameMethod = "VectorManipulator::update_plotting_agent"


        # Pass the necessary data to the plotting agent.

        print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
        print(nameMethod + " : About to invoke : plotAgent.set_angle_rotation")

        self.plottingAgent.set_angle_rotation(self.angle_rotation)

        self.plottingAgent.set_quaternions(

            self.quaternion_axis_rotation,
            self.quaternion_to_rotate,
            self.quaternion_pre_multiply,
            self.quaternion_rotated
        )


    def generate_plot(

            self,
            filename
    ) :

        # Instruct the plotting agent to plot the data which was just passed to it.

        self.plottingAgent.generate_plot(

            filename,
            self.azimuth_view,
            self.elevation_view
        )


    # Invoked by : VectorManipulator::run

    def generate_plots(self) :

        nameMethod         = "VectorManipulator::generate_plots"


        print(nameMethod + " : Enter")

        counter = 0

        while self.azimuth_view <= 720 :

            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(nameMethod + f" : counter = {counter:d}")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"Azimuth view = {self.azimuth_view:f}")

            filename = f"rotation-{counter:04d}.png"

            self.perform_quaternion_operations()
            self.update_plotting_agent()
            self.generate_plot(filename)

            # self.plot_result(filename)

            # Update the loop parameters.

            counter = counter + 1

            angle_rotation_next = (counter * self.angle_rotation_increment) + self.angle_rotation_start

            if angle_rotation_next <= self.angle_rotation_full :

                self.angle_rotation = angle_rotation_next

            self.azimuth_view = (counter * self.azimuth_view_increment) + self.azimuth_view_start

            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print()

        print(nameMethod + " : Exit")


def displayUsage() :

    print("")
    print("")
    print("Manipulate a 3d vector in one of three ways using a quaternion.")
    print("")
    print("Usage:")
    print("")
    print("  vectorQuaternionRotate verbose operation_type vector_x vector_y vector_z rotationAngle axis_x axis_y axis_z")
    print("")
    print("where:")
    print("")
    print("  verbose       : utility runs in a verbose fashion")
    print("                - Haskell type : Bool")
    print("                - [True | False]")
    print("  operation     : partially multiply, fully multiply, or rotate the 3d vector by the rotation quaternion")
    print("                - Haskell type : String")
    print("                - [partial_multiplication | full_multiplication | rotation]")
    print("  axis_x        : the x component of the 3d vector which acts as the axis of rotation")
    print("                - Haskell type : Double")
    print("  axis_y        : the y component of the 3d vector which acts as the axis of rotation")
    print("                - Haskell type : Double")
    print("  axis_z        : the z component of the 3d vector which acts as the axis of rotation")
    print("                - Haskell type : Double")
    print("  rotationAngle : the angle in degrees by which the 3d vector is to be rotated")
    print("                - Haskell type : Double")
    print("                - Measured in degrees")
    print("  vector_x      : the x component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_y      : the y component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_z      : the z component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("")
    print("Example:")
    print("")
    print("  vectorQuaternionRotate False rotation 1 0 0 90 0 0 1")
    print("")
    print("Rotate the 3d vector <0,0,1> by 90 degrees, i.e. pi/2 radians, around the axis which is represented by the")
    print("vector <1,0,0>.")
    print("")
    print("> Notes on the operation of this utility")
    print("  ===========================")
    print("")
    print("If the vector which denotes the axis of rotation, is not a unit vector, then this utility will convert it")
    print("into one first before using it in the calculations.")
    print("")
    print("This utility will not do the same however with the vector that is to be rotated. This is mentioned, because")
    print("if this vector is too long, then it won't be displayed properly in the resulting plot.")


# main
#   |- VectorManipulator::run
#        |- VectorManipulator::set_values_from_command_line_args
#        |- VectorManipulator::generate_plots
#           |- VectorManipulator::perform_quaternion_operations
#           |- VectorManipulator::update_plotting_agent
#           |- VectorManipulator::generate_plot
#                |- PlotAgent::generate_plot

def main() :

    nameMethod = "main"

    vector_manipulator = VectorManipulator()


    print(nameMethod + " : Enter")

    if len(sys.argv) != 10 :

        displayUsage()

        raise ValueError()

    try :

        vector_manipulator.run()


    except Exception as e :

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("The following exception was caught.")
        print("")
        print("  " + str(e))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    print(nameMethod + " : Exit")


if __name__ == "__main__":

    main()