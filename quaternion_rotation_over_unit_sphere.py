import sys
import math
from   matplotlib        import font_manager
import subprocess
import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
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


class vectorManipulator :

    def __init__(self) :

        self.angle_rotation              = None
        self.quaternion_axis_rotation    = None
        self.quaternion_vector_to_rotate = None

        self.x_components = np.array([])
        self.y_components = np.array([])
        self.z_components = np.array([])


    # Set the angle of rotation.
    #
    # The argument must be specified in radians, not degrees.

    def set_angle_rotation(self, angle_rotation) :

        self.angle_rotation = angle_rotation


    def set_axis_rotation(self, quaternion_axis_rotation) :

        self.quaternion_axis_rotation = quaternion_axis_rotation


    def set_vector_to_rotate(self, quaternion_vector_to_rotate) :

        self.quaternion_vector_to_rotate = quaternion_vector_to_rotate


    def generate_string(self, scalar_value, i_value, j_value, k_value) :

        label = ""

        # Scalar value

        if scalar_value < 0 :

            label = label + f"{scalar_value:.3f} "

        else :

            label = label + f" {scalar_value:.3f} "

        # i value

        if i_value < 0 :

            label = label + f"- i{abs(i_value):.3f} "

        else :

            label = label + f"+ i{i_value:.3f} "

        # j value

        if j_value < 0:

            label = label + f"- j{abs(j_value):.3f} "

        else:

            label = label + f"+ j{j_value:.3f} "

        # k value

        if k_value < 0:

            label = label + f"- k{abs(k_value):.3f} "

        else:

            label = label + f"+ k{k_value:.3f} "

        return label


    def preMultiplyVectorUsingQuaternion(self) :

        operation_type = "partial_multiplication"

        result = subprocess.run(
            [
             utility_quaternion_rotation,
             verbose_operation,
             operation_type,
             str(self.quaternion_vector_to_rotate.x),
             str(self.quaternion_vector_to_rotate.y),
             str(self.quaternion_vector_to_rotate.z),
             str(self.angle_rotation),
             str(self.quaternion_axis_rotation.x),
             str(self.quaternion_axis_rotation.y),
             str(self.quaternion_axis_rotation.z)
            ],
            capture_output=True,
            text=True
        )

        # Convert the string into a list of strings, breaking the original string at "," symbols.

        string_quaternion = (result.stdout).split(",")

        # Convert the list of strings into a numpy vector.

        v = np.array([float(x) for x in string_quaternion])

        quaternion_result = np.quaternion(0, 0, 0, 0)

        quaternion_result.w = v[0]
        quaternion_result.x = v[1]
        quaternion_result.y = v[2]
        quaternion_result.z = v[3]

        # print(result.stdout)
        # print(result.stderr)
        # print(result.returncode)

        return quaternion_result


    def rotateVectorUsingQuaternion(self) :

        operation_type = "rotation"

        result = subprocess.run(
            [
             utility_quaternion_rotation,
             verbose_operation,
             operation_type,
             str(self.quaternion_vector_to_rotate.x),
             str(self.quaternion_vector_to_rotate.y),
             str(self.quaternion_vector_to_rotate.z),
             str(self.angle_rotation),
             str(self.quaternion_axis_rotation.x),
             str(self.quaternion_axis_rotation.y),
             str(self.quaternion_axis_rotation.z)
            ],
            capture_output=True,
            text=True
        )

        # Convert the string into a list of strings, breaking the original string at "," symbols.

        string_quaternion = (result.stdout).split(",")

        # Convert the list of strings into a numpy vector.

        v = np.array([float(x) for x in string_quaternion])

        # quaternion_result = np.quaternion(0, 0, 0, 0)

        quaternion_result = quaternion.as_quat_array(v)

        # quaternion_result.w = v[0]
        # quaternion_result.x = v[1]
        # quaternion_result.y = v[2]
        # quaternion_result.z = v[3]

        # print(result.stdout)
        # print(result.stderr)
        # print(result.returncode)

        return quaternion_result


    def plotResult(

            self,
            angle_rotation,
            vector_a,
            vector_b,
            quaternion,
            vector_d,
            filename,
            azimuth_view,
            elevation_view
    ) :

        # ----------------------------
        # Input vector
        # ----------------------------
        v = np.array([1.2, 0.8, 0.5])

        # ----------------------------
        # Create figure
        # ----------------------------
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

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

        ax.plot_surface(
            x, y, z,
            color='lightyellow',
            alpha=0.2,
            linewidth=0
        )

        ax.plot_wireframe(
            x, y, z,
            color='black',
            linewidth=0.4,
            rstride=4,
            cstride=4
        )

        # ----------------------------
        # Plot vectors
        # ----------------------------

        ax.quiver(
            0, 0, 0,
            vector_a[0], vector_a[1], vector_a[2],
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        ax.quiver(
            0, 0, 0,
            vector_b[0], vector_b[1], vector_b[2],
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        ax.quiver(
            0, 0, 0,
            quaternion[1], quaternion[2], quaternion[3],
            color='blue',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        ax.quiver(
            0, 0, 0,
            vector_d[0], vector_d[1], vector_d[2],
            color='magenta',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Add the point to the list of points.

        self.x_components = np.append(self.x_components, vector_d[0])
        self.y_components = np.append(self.y_components, vector_d[1])
        self.z_components = np.append(self.z_components, vector_d[2])

        print(f"Length self.x_components = {len(self.x_components):d}")
        print(f"Length self.y_components = {len(self.y_components):d}")
        print(f"Length self.z_components = {len(self.z_components):d}")

        ax.plot(self.x_components, self.y_components, self.z_components, marker=None, linestyle='-', color='magenta')

        # Label vector tip

        # label_vector_a_tip = "<" + str(vector_a[0])   + ", " + str(vector_a[1])   + ", " + str(vector_a[2]) + ">"
        # label_vector_b_tip = "<" + str(vector_b[0])   + ", " + str(vector_b[1])   + ", " + str(vector_b[2]) + ">"
        # label_vector_c_tip = "<" + str(quaternion[1]) + ", " + str(quaternion[1]) + ", " + str(quaternion[2]) + ", " + str(quaternion[2]) + ">"
        # label_vector_d_tip = "<" + str(vector_d[0])   + ", " + str(vector_d[1])   + ", " + str(vector_d[2]) + ">"

        # label_vector_a_tip = f"Axis       : 0.000 + i{vector_a[0]:.3f} + j{vector_a[1]:.3f} + k{vector_a[2]:.3f}"
        # label_vector_b_tip = f"Vector     : 0.000 + i{vector_b[0]:.3f} + j{vector_b[1]:.3f} + k{vector_b[2]:.3f}"
        # label_vector_c_tip = f"Partial    : {quaternion[0]:.3f} + i{quaternion[1]:.3f} + j{quaternion[2]:.3f} + k{quaternion[3]:.3f}"

        label_vector_a = self.generate_string(0.000,         vector_a[0],   vector_a[1],   vector_a[2])
        label_vector_b = self.generate_string(0.000,         vector_b[0],   vector_b[1],   vector_b[2])
        label_vector_c = self.generate_string(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
        label_vector_d = self.generate_string(0.000,         vector_d[0],   vector_d[1],   vector_d[2])

        label_vector_a = f"Axis         : " + label_vector_a
        label_vector_b = f"Vector       : " + label_vector_b
        label_vector_c = f"Partial (qv) : " + label_vector_c
        label_vector_d = f"Vector rot   : " + label_vector_d

        label_angle_rotation = f"Angle of rotation = {angle_rotation:8.3f} degrees"

        # ax.text(
        #     vector_a[0], vector_a[1], vector_a[2],
        #     label_vector_a_tip,
        #     color="red"
        # )

        # ax.text(
        #     vector_b[0], vector_b[1], vector_b[2],
        #     label_vector_b_tip,
        #     color="green"
        # )

        # ax.text(
        #     quaternion[1], quaternion[2], quaternion[3],
        #     label_vector_c_tip,
        #     color="blue"
        # )

        # ax.text(
        #     vector_d[0], vector_d[1], vector_d[2],
        #     label_vector_d_tip,
        #     color="magenta"
        # )

        # ----------------------------
        # Set equal aspect ratio
        # ----------------------------

        max_extent = max(
            np.max(np.abs(v)),
            1.0
        )

        ax.set_xlim([-max_extent, max_extent])
        ax.set_ylim([-max_extent, max_extent])
        ax.set_zlim([-max_extent, max_extent])

        ax.set_box_aspect([1, 1, 1])

        # ----------------------------
        # Labels
        # ----------------------------
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('3d vectors and the unit sphere')

        legend_elements = [
            Line2D([0], [0], color='red',     lw=1, label=label_vector_a),
            Line2D([0], [0], color='green',   lw=1, label=label_vector_b),
            Line2D([0], [0], color='blue',    lw=1, label=label_vector_c),
            Line2D([0], [0], color='magenta', lw=1, label=label_vector_d),
            Line2D([0], [0], color='white',   lw=1, label=label_angle_rotation)
        ]

        legend = ax.legend(
                           handles=legend_elements,
                           prop={
                                 "family": "Liberation Mono",
                                 "size": 10
                                },
                           loc='upper right',
                           fontsize=10
                          )

        # If the scalar part of the quaternion is not close in value to 0, then display its text in red

        if abs(quaternion[0]) > 0.001 :

            legend.get_texts()[2].set_color("red")

        # ax.grid(False)

        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.zaxis.set_major_locator(MultipleLocator(1))

        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        ax.view_init(elev=elevation_view, azim=azimuth_view)

        matplotlib.use("QtAgg")

        print("Saving the figure to file : " + filename + "\n")

        fig.savefig(filename, dpi=300, bbox_inches="tight")


        metadata = {
            "view": {
                "azimuth"   : azimuth_view,
                "elevation" : elevation_view
            },
            "rotation": {
                "angle": angle_rotation,
                "axis": {
                    "scalar": 0.0,
                    "x": vector_a[0],
                    "y": vector_a[1],
                    "z": vector_a[2]
                },
            },
            "vector_to_rotate": {
                "scalar": 0.0,
                "x": vector_b[0],
                "y": vector_b[1],
                "z": vector_b[2]
            },
            "quaternion_pre_multiply": {
                "scalar": quaternion[0],
                "x": quaternion[1],
                "y": quaternion[2],
                "z": quaternion[3]
            },
            "vector_rotated": {
                "scalar": 0.0,
                "x": vector_d[0],
                "y": vector_d[1],
                "z": vector_d[2]
            },
        }

        img = Image.open(filename)

        info = PngInfo()
        info.add_itxt(
            "com.example.simulation",
            json.dumps(metadata, indent=2)
        )

        img.save(filename, pnginfo=info)

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

        if show_plots :

            plt.show()

        # Close the figure so that we can free up the memory it is using.

        plt.close(fig)


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
    print("  rotationAngle : the angle by which the 3d vector is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_x      : the x component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_y      : the y component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_z      : the z component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("")
    print("Example:")
    print("")
    print("  vectorQuaternionRotate False rotation 1 0 0 1.570796 0 0 1")
    print("")
    print("Rotate the 3d vector <0,0,1> by 1.570796 radians, i.e. pi/2 radians, or 90 degrees, around the axis which")
    print("is represented by the vector <1,0,0>.")
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

    vector_manipulator = vectorManipulator()


    if len(sys.argv) != 10 :

        displayUsage()

        raise ValueError()

    try :

        # Read the arguments in from the command line.

        verbose_operation = sys.argv[1]
        operation_type    = sys.argv[2]
        axis_x            = float(sys.argv[3])
        axis_y            = float(sys.argv[4])
        axis_z            = float(sys.argv[5])
        angle_rotation    = float(sys.argv[6])
        vector_x          = float(sys.argv[7])
        vector_y          = float(sys.argv[8])
        vector_z          = float(sys.argv[9])

        axis_rotation    = np.array([axis_x,axis_y,axis_z])
        angle_rotation   = angle_rotation
        vector_to_rotate = np.array([vector_x,vector_y,vector_z])

        quaternion_axis_rotation    = np.quaternion(0, axis_x, axis_y, axis_z)
        quaternion_vector_to_rotate = np.quaternion(0, vector_x, vector_y, vector_z)

        counter           = 0
        # number_increments = 1

        azimuth_plot_start = 0
        azimuth_view_start = 0

        azimuth_plot = azimuth_plot_start

        azimuth_plot_increment = 5
        azimuth_view_increment = 2.5

        elevation_view = 28

        vector_manipulator.set_axis_rotation(quaternion_axis_rotation)
        vector_manipulator.set_vector_to_rotate(quaternion_vector_to_rotate)

        while azimuth_plot <= 720 :

            azimuth_plot = (counter * azimuth_plot_increment) + azimuth_plot_start
            azimuth_view = (counter * azimuth_view_increment) + azimuth_view_start

            print(f"Counter = {counter:d}")
            print(f"Azimuth plot = {azimuth_plot:f}")
            print(f"Azimuth view = {azimuth_view:f}")

            # Set the parameters for the quaternionic computations.

            vector_manipulator.set_angle_rotation(math.radians(azimuth_plot))

            # fonts = sorted(set(f.name for f in font_manager.fontManager.ttflist))
            # for font in fonts:
            #     print(font)

            quaternion_partial = vector_manipulator.preMultiplyVectorUsingQuaternion()

            print("quaternion_partial = ", quaternion_partial)

            vector_partial = (quaternion.as_float_array(quaternion_partial))[1:4]

            # vector_partial = np.array([0,0,0])
            # vector_partial[0] = quaternion_partial.x
            # vector_partial[1] = quaternion_partial.y
            # vector_partial[2] = quaternion_partial.z

            # Call the Haskell quaternion rotation utility and get the result.

            quaternion_rotated = vector_manipulator.rotateVectorUsingQuaternion()

            vector_rotated = (quaternion.as_float_array(quaternion_rotated))[1:4]

            print("quaternion = ", quaternion)

            filename = f"rotation-{counter:04d}.png"

            vector_manipulator.plotResult(
                                          float(azimuth_plot),
                                          axis_rotation,
                                          vector_to_rotate,
                                          quaternion.as_float_array(quaternion_partial),
                                          vector_rotated,
                                          filename,
                                          azimuth_view,
                                          elevation_view
                                         )

            counter = counter + 1

    except Exception as e :

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("An error occurred:", e)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        displayUsage()


if __name__ == "__main__":

    main()