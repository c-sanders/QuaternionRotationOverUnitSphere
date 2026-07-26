import sys
import math
from   matplotlib        import font_manager
import subprocess
import numpy             as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from   matplotlib.lines  import Line2D
from   matplotlib.ticker import MultipleLocator

# Import the Numerical Python package, aka numpy.

import numpy as np
import quaternion

# Import the Python Image Library, aka PIL.

import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo


# Global settings used by this program.

utility_quaternion_rotation = "/home/craig/local/source_code/haskell/HaskellQuaternionRotation/dist-newstyle/build/x86_64-linux/ghc-9.14.1/quaternion-0.1.0.0/x/quaternion/build/quaternion/quaternion"
verbose_operation           = "False"

show_plots = False


class PlotAgent :

    def __init__(

            self,
            title_plots
    ) :

        self.fig = None
        self.ax  = None

        self.title_plots = title_plots

        self.v   = np.array([1.2, 0.8, 0.5])

        self.angle_rotation = None

        self.quaternion_axis_rotation = None
        self.quaternion_to_rotate     = None
        self.quaternion_pre_multiply  = None
        self.quaternion_rotated       = None

        self.plot_handle_axis_rotation                   = None
        self.plot_handle_to_rotate                       = None
        self.plot_handle_quaternion_pre_multiply         = None
        self.plot_handle_quaternion_rotated              = None
        self.plot_handle_quaternion_pre_multiply_history = None

        # Component arrays to hold the history of the rotated vector.

        self.x_components = []
        self.y_components = []
        self.z_components = []

        self.azimuth_view   = None
        self.elevation_view = None


        self.initialise_plot()


    def initialise_plot(self) :

        nameMethod = "PlotAgent::initialise_plot"


        print(nameMethod + " : Enter")

        self.create_figure()
        self.plot_unit_sphere()
        self.plot_axes()

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self.set_aspect_ratios_and_extents()

        self.fill_panes()
        self.configure_grid()
        # self.create_static_labels()

        print(nameMethod + " : Exit")


    def set_angle_rotation(

            self,
            angle_rotation
    ) :

        self.angle_rotation = angle_rotation


    def set_quaternions(

        self,
        quaternion_axis_rotation,
        quaternion_to_rotate,
        quaternion_pre_multiply,
        quaternion_rotated
    ) :

        self.quaternion_axis_rotation = quaternion_axis_rotation
        self.quaternion_to_rotate     = quaternion_to_rotate
        self.quaternion_pre_multiply  = quaternion_pre_multiply
        self.quaternion_rotated       = quaternion_rotated


    def format_component(

            self,
            name,
            value
        ) :

            if value < 0 :

                return f"- {name}{abs(value):.3f}"

            else :

                return f"+ {name}{value:.3f}"


    def generate_string(

            self,
            scalar_value,
            i_value,
            j_value,
            k_value
        ) :

        label  = f"{scalar_value:.3f} "

        label += f"{self.format_component('i', i_value)} "
        label += f"{self.format_component('j', j_value)} "
        label += f"{self.format_component('k', k_value)}"

        return label


    def create_figure(self) :

        self.fig = plt.figure(figsize=(8, 8))

        self.ax = self.fig.add_subplot(111, projection='3d')


    def plot_axes(self) :

        # Plot;
        #
        #   x axis
        #   y axis
        #   z axis

        self.ax.quiver(
            -1.2, 0, 0,
            2.4, 0, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        self.ax.quiver(
            0, -1.2, 0,
            0, 2.4, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        self.ax.quiver(
            0, 0, -1.2,
            0, 0, 2.4,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )


    def plot_unit_sphere(self) :

        # ----------------------------
        # Plot the unit sphere.
        # ----------------------------

        u = np.linspace(0, 2 * np.pi, 100)
        v_sphere = np.linspace(0, np.pi, 100)

        x = np.outer(np.cos(u), np.sin(v_sphere))
        y = np.outer(np.sin(u), np.sin(v_sphere))
        z = np.outer(np.ones_like(u), np.cos(v_sphere))

        # ax.plot_surface(
        #     x, y, z,
        #     alpha=0.25,
        #     linewidth=0,
        #     antialiased=True
        # )

        # ax.plot_wireframe(
        #     x, y, z,
        #     color='gray',
        #     linewidth=0.5,
        #     alpha=0.5,
        #     rstride=5,
        #     cstride=5
        # )

        self.ax.plot_surface(
            x, y, z,
            color='lightyellow',
            alpha=0.2,
            linewidth=0
        )

        self.ax.plot_wireframe(
            x, y, z,
            color='black',
            linewidth=0.4,
            rstride=4,
            cstride=4
        )


    def plot_quaternions(self) :

        nameMethod = "PlotAgent::plot_quaternions"


        self.plot_handle_quaternion_axis_rotation = self.ax.quiver(

            0, 0, 0,
            self.quaternion_axis_rotation.x, self.quaternion_axis_rotation.y, self.quaternion_axis_rotation.z,
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_to_rotate = self.ax.quiver(

            0, 0, 0,
            self.quaternion_to_rotate.x, self.quaternion_to_rotate.y, self.quaternion_to_rotate.z,
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_pre_multiply = self.ax.quiver(

            0, 0, 0,
            self.quaternion_pre_multiply.x, self.quaternion_pre_multiply.y, self.quaternion_pre_multiply.z,
            color='blue',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_rotated = self.ax.quiver(

            0, 0, 0,
            self.quaternion_rotated.x, self.quaternion_rotated.y, self.quaternion_rotated.z,
            color='magenta',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Add the point to the list of points.

        self.x_components.append(self.quaternion_rotated.x)
        self.y_components.append(self.quaternion_rotated.y)
        self.z_components.append(self.quaternion_rotated.z)

        print(f"Length self.x_components = {len(self.x_components):d}")
        print(f"Length self.y_components = {len(self.y_components):d}")
        print(f"Length self.z_components = {len(self.z_components):d}")

        self.plot_handle_quaternion_pre_multiply_history = self.ax.plot(

            self.x_components,
            self.y_components,
            self.z_components,
            marker=None,
            linestyle='-',
            color='magenta'
        )


    def add_labels_to_plot(self) :

        # Label vector tip

        # label_vector_a_tip = "<" + str(vector_a[0])   + ", " + str(vector_a[1])   + ", " + str(vector_a[2]) + ">"
        # label_quaternion_to_rotate_tip = "<" + str(quaternion_to_rotate[0])   + ", " + str(quaternion_to_rotate[1])   + ", " + str(quaternion_to_rotate[2]) + ">"
        # label_vector_c_tip = "<" + str(quaternion[1]) + ", " + str(quaternion[1]) + ", " + str(quaternion[2]) + ", " + str(quaternion[2]) + ">"
        # label_vector_d_tip = "<" + str(vector_d[0])   + ", " + str(vector_d[1])   + ", " + str(vector_d[2]) + ">"

        # label_vector_a_tip = f"Axis       : 0.000 + i{vector_a[0]:.3f} + j{vector_a[1]:.3f} + k{vector_a[2]:.3f}"
        # label_quaternion_to_rotate_tip = f"Vector     : 0.000 + i{quaternion_to_rotate[0]:.3f} + j{quaternion_to_rotate[1]:.3f} + k{quaternion_to_rotate[2]:.3f}"
        # label_vector_c_tip = f"Partial    : {quaternion[0]:.3f} + i{quaternion[1]:.3f} + j{quaternion[2]:.3f} + k{quaternion[3]:.3f}"

        label_quaternion_axis_rotation = self.generate_string(self.quaternion_axis_rotation.w,
                                                              self.quaternion_axis_rotation.x,
                                                              self.quaternion_axis_rotation.y,
                                                              self.quaternion_axis_rotation.z)

        label_quaternion_to_rotate     = self.generate_string(self.quaternion_to_rotate.w, self.quaternion_to_rotate.x,
                                                              self.quaternion_to_rotate.y, self.quaternion_to_rotate.z)

        label_quaternion_pre_multiply  = self.generate_string(self.quaternion_pre_multiply.w,
                                                              self.quaternion_pre_multiply.x,
                                                              self.quaternion_pre_multiply.y,
                                                              self.quaternion_pre_multiply.z)

        label_quaternion_rotated       = self.generate_string(self.quaternion_rotated.w, self.quaternion_rotated.x,
                                                              self.quaternion_rotated.y, self.quaternion_rotated.z)

        self.label_quaternion_axis_rotation = f"Axis of rotation (q)     : " + label_quaternion_axis_rotation
        self.label_quaternion_to_rotate     = f"Quaternion to rotate (v) : " + label_quaternion_to_rotate
        self.label_quaternion_pre_multiply  = f"Pre multiplication (qv)  : " + label_quaternion_pre_multiply
        self.label_quaternion_rotated       = f"Quaternion rotated (v')  : " + label_quaternion_rotated
        self.label_angle_rotation           = f"Angle of rotation        = {self.angle_rotation:8.3f} degrees"

        self.ax.text(
            1.3, 0, 0,
            "x",
            color="black"
        )

        self.ax.text(
            0, 1.3, 0,
            "y",
            color="black"
        )

        self.ax.text(
            0, 0, 1.3,
            "z",
            color="black"
        )

        # ax.text(
        #     quaternion_to_rotate[0], quaternion_to_rotate[1], quaternion_to_rotate[2],
        #     label_quaternion_to_rotate_tip,
        #     color="green"
        # )

        # ax.text(
        #     quaternion[1], quaternion[2], quaternion[3],
        #     label_vector_c_tip,
        #     color="blue"
        # )

        # ax.text(
        #     quaternion_rotated[0], quaternion_rotated[1], quaternion_rotated[2],
        #     label_quaternion_rotated_tip,
        #     color="magenta"
        # )

    def generate_plot(

            self,
            filename,
            azimuth_view,
            elevation_view
    ) :

        self.plot_result(filename, azimuth_view, elevation_view)


    def encode_metadata(self) :

        nameMethod = "encode_metadata"


        self.metadata = {
            "view" : {
                "azimuth"   : self.azimuth_view,
                "elevation" : self.elevation_view
            },
            "rotation" : {
                "angle" : self.angle_rotation,
                "axis" : {
                    "scalar" : self.quaternion_axis_rotation.w,
                    "x"      : self.quaternion_axis_rotation.x,
                    "y"      : self.quaternion_axis_rotation.y,
                    "z"      : self.quaternion_axis_rotation.z
                },
            },
            "quaternion_to_rotate": {
                "scalar"     : self.quaternion_to_rotate.w,
                "x"          : self.quaternion_to_rotate.x,
                "y"          : self.quaternion_to_rotate.y,
                "z"          : self.quaternion_to_rotate.z
            },
            "quaternion_pre_multiply": {
                "scalar"     : self.quaternion_pre_multiply.w,
                "x"          : self.quaternion_pre_multiply.x,
                "y"          : self.quaternion_pre_multiply.y,
                "z"          : self.quaternion_pre_multiply.z
            },
            "quaternion_rotated": {
                "scalar"     : self.quaternion_rotated.w,
                "x"          : self.quaternion_rotated.x,
                "y"          : self.quaternion_rotated.y,
                "z"          : self.quaternion_rotated.z
            },
        }


    def display_metadata(

            self,
            filename
        ) :

        nameMethod = "display_metadata"


        # Check that the JSON was written into the file properly.

        with Image.open(filename) as img:

            metadata = json.loads(img.text["com.example.simulation"])

            w = metadata["quaternion_pre_multiply"]["scalar"]
            x = metadata["quaternion_pre_multiply"]["x"]
            y = metadata["quaternion_pre_multiply"]["y"]
            z = metadata["quaternion_pre_multiply"]["z"]

            quaternion_pre_multiply = np.quaternion(w,x,y,z)

            print(f"quaternion_pre_multiply = <{quaternion_pre_multiply.w:.03f}, {quaternion_pre_multiply.x:.03f}, {quaternion_pre_multiply.y:.03f}, {quaternion_pre_multiply.z:.03f}>")

            print("========================================")
            print("JSON metadata from the file :")
            print("-----------------------------")
            print("View azimuth   = " + str(metadata["view"]["azimuth"]))
            print("View elevation = " + str(metadata["view"]["elevation"]))
            print("Rotation angle = " + str(metadata["rotation"]["angle"]))
            print("Rotation axis  = " + str(metadata["rotation"]["axis"]["scalar"]))
            print("========================================")


    def set_aspect_ratios_and_extents(self) :

        nameMethod = "set_aspect_ratios_and_extents"


        print(nameMethod + " : Enter")

        # ----------------------------
        # Set equal aspect ratio
        # ----------------------------

        max_extent = max(
            np.max(np.abs(self.v)),
            1.0
        )

        self.ax.set_xlim([-max_extent, max_extent])
        self.ax.set_ylim([-max_extent, max_extent])
        self.ax.set_zlim([-max_extent, max_extent])

        self.ax.set_box_aspect([1, 1, 1])

        print(nameMethod + " : Exit")


    def set_title_and_legend(self):

        nameMethod = "set_title_and_legend"


        print(nameMethod + " : Enter")

        # ----------------------------
        # Labels
        # ----------------------------

        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        # ax.set_zlabel('z')
        self.ax.set_title(self.title_plots)

        legend_elements = [
            Line2D([0], [0], color='red',     lw=1, label=self.label_quaternion_axis_rotation),
            Line2D([0], [0], color='green',   lw=1, label=self.label_quaternion_to_rotate),
            Line2D([0], [0], color='blue',    lw=1, label=self.label_quaternion_pre_multiply),
            Line2D([0], [0], color='magenta', lw=1, label=self.label_quaternion_rotated),
            Line2D([0], [0], color='white',   lw=1, label=self.label_angle_rotation)
        ]

        print(nameMethod + " : MARKER 9")

        legend = self.ax.legend(
            handles=legend_elements,
            prop={
                "family": "Liberation Mono",
                "size": 10
            },
            loc='upper right',
            fontsize=10
        )

        # If the scalar part of the quaternion is not close in value to 0, then display its text in red

        if abs(self.quaternion_pre_multiply.x) > 0.001 :

            legend.get_texts()[2].set_color("red")

        print(nameMethod + " : Exit")


    def fill_panes(self) :

        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False


    def configure_grid(self) :

        # ax.grid(False)

        self.ax.xaxis.set_major_locator(MultipleLocator(1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.ax.zaxis.set_major_locator(MultipleLocator(1))


    # Client : VectorManipulator::generate_plots

    def plot_result(

            self,
            filename,
            azimuth_view,
            elevation_view
    ) :

        """
        Plot the current data.

        Parameters
        ----------
        angle_rotation : Float

        The angle of rotation around the axis of rotation.

        quaternion_axis_rotation : numpy.quaternion

            Quaternion representing the axis of rotation.
        """

        nameMethod = "PlotAgent::plot_result"

        self.azimuth_view   = azimuth_view
        self.elevation_view = elevation_view


        print(nameMethod + " : Enter")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        print(nameMethod + " : About to invoke : self.plot_quaternions")

        self.plot_quaternions()

        print(nameMethod + " : About to invoke : self.add_labels_to_plot")

        self.add_labels_to_plot()

        ### print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")

        ### self.set_aspect_ratios_and_extents()

        print(nameMethod + " : About to invoke : self.set_title_and_legend")

        self.set_title_and_legend()

        self.ax.view_init(elev=self.elevation_view, azim=self.azimuth_view)

        print("Saving the figure to file : " + str(filename) + "\n")

        self.fig.savefig(filename, dpi=300, bbox_inches="tight")

        self.encode_metadata()

        with Image.open(filename) as img :

            info = PngInfo()
            info.add_itxt(
                "com.example.simulation",
                json.dumps(self.metadata, indent=2)
            )

            img.save(filename, pnginfo=info)

        self.display_metadata(filename)

        print(nameMethod + " : MARKER 11")

        if show_plots:

            plt.show()

        # Keep the core of the plot and delete everything else.
        #
        # Keep;
        #
        #   - the axes
        #   - the grid associated with the axes
        #   - the unit sphere.
        #
        # Delete;
        #
        #   - the legend
        #   - the 4 plots associated with each of the quaternions
        #   - the history plot associated with the pre multiplication quaternion.

        self.plot_handle_quaternion_pre_multiply_history.remove()
        self.plot_handle_quaternion_rotated.remove()
        self.plot_handle_quaternion_pre_multiply.remove()
        self.plot_handle_quaternion_to_rotate.remove()
        self.plot_handle_quaternion_axis_rotation.remove()


        print(nameMethod + " : Exit")


    def destroy_plot(self) :

        nameMethod = "PlotAgent::destroy_plot"


        print(nameMethod + " : Enter")

        # Close the figure so that we can free up the memory it is using.

        plt.close(self.fig)

        self.fig = None
        self.ax  = None

        print(nameMethod + " : Exit")


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


    # Invoked by : VectorManipulator::run

    def generate_plots(self) :

        nameMethod = "VectorManipulator::generate_plots"

        plotAgent = PlotAgent(self.title_plots)


        print(nameMethod + " : Enter")

        counter = 0

        while self.azimuth_view <= 720 :

            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(nameMethod + f" : counter = {counter:d}")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"Azimuth view = {self.azimuth_view:f}")

            filename = f"rotation-{counter:04d}.png"

            # Perform the quaternionic operations.

            self.preMultiplyVectorUsingQuaternion()
            self.rotateVectorUsingQuaternion()

            # Pass the necessary data to the plotting agent.

            print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
            print(nameMethod + " : About to invoke : plotAgent.set_angle_rotation")

            plotAgent.set_angle_rotation(self.angle_rotation)

            plotAgent.set_quaternions(

                self.quaternion_axis_rotation,
                self.quaternion_to_rotate,
                self.quaternion_pre_multiply,
                self.quaternion_rotated
            )

            # Instruct the plotting agent to plot the data which was just passed to it.

            plotAgent.generate_plot(

                filename,
                self.azimuth_view,
                self.elevation_view
            )

            # self.plot_result(filename)

            # Update the loop parameters.

            counter = counter + 1

            angle_rotation_next = (counter * self.angle_rotation_increment) + self.angle_rotation_start

            if angle_rotation_next < self.angle_rotation_full :



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


def main() :

    nameMethod = "main"

    vector_manipulator = VectorManipulator()


    print(nameMethod + " : Enter")

    if len(sys.argv) != 10 :

        displayUsage()

        raise ValueError()

    try :

        # vector_manipulator.run()
        #   |- self.generate_plots()
        #        |- self.set_angle_rotation()
        #        |- self.set_quaternions()
        #        |- self.generate_plot()

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