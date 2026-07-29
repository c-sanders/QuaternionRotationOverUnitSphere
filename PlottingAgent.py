import numpy             as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from   matplotlib.lines  import Line2D
from   matplotlib.ticker import MultipleLocator
import json

# Import the Python Image Library, aka PIL.

from PIL import Image
from PIL.PngImagePlugin import PngInfo

import colorsys


plot_quaternion_pre_multiply_history = True
plot_quaternion_rotated_history      = False

show_plots = False


class PlottingAgent :

    def __init__(

            self,
            title_plots
    ) :

        self.fig = None
        self.ax1 = None
        self.ax2 = None

        self.title_plots = title_plots

        self.v   = np.array([1.2, 0.8, 0.5])

        self.angle_rotation = None

        self.quaternion_axis_rotation = None
        self.quaternion_to_rotate     = None
        self.quaternion_pre_multiply  = None
        self.quaternion_rotated       = None

        self.quaternion_pre_multiply_min = None
        self.quaternion_pre_multiply_max = None

        self.plot_handle_axis_rotation                   = None
        self.plot_handle_to_rotate                       = None
        self.plot_handle_quaternion_pre_multiply         = None
        self.plot_handle_quaternion_pre_multiply_history = None
        self.plot_handle_quaternion_rotated              = None
        self.plot_handle_quaternion_rotated_history      = None

        # Component arrays to hold the history of the rotated vector.

        self.x_components = []
        self.y_components = []
        self.z_components = []

        self.azimuth_view   = None
        self.elevation_view = None

        self.rgb_value_min = colorsys.hsv_to_rgb(0, 0, 1.0)
        self.rgb_value_max = colorsys.hsv_to_rgb(0, 0, 1.0)

        self._initialise_plot()


    def _initialise_plot(self) :

        nameMethod = "PlottingAgent::initialise_plot"


        print(nameMethod + " : Enter")

        self._create_figure_and_axes()

        self._initialise_subplot_1()
        self._initialise_subplot_2()

        print(nameMethod + " : Exit")


    def _initialise_subplot_1(self) :

        nameMethod = "PlottingAgent::initialise_subplot_1"

        axis = self.ax1


        print(nameMethod + " : Enter")

        self._plot_unit_sphere(axis)
        self._plot_axes(axis)

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self._set_aspect_ratios_and_extents(axis)

        self._fill_panes(axis)
        self._configure_grid(axis)
        # self.create_static_labels()

        print(nameMethod + " : Exit")


    def _initialise_subplot_2(self) :

        nameMethod = "PlottingAgent::initialise_subplot_2"

        axis = self.ax2


        print(nameMethod + " : Enter")

        self._plot_unit_sphere(axis)
        self._plot_axes(axis)

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self._set_aspect_ratios_and_extents(axis)

        self._fill_panes(axis)
        self._configure_grid(axis)
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
            space,
            value
        ) :

            if value < 0 :

                if space :

                    return f"- {name}{abs(value):.3f}"

                else :

                    return f"-{name}{abs(value):.3f}"

            else :

                if space :

                    return f"+ {name}{value:.3f}"

                else :

                    return f" {name}{value:.3f}"


    def generate_string(

            self,
            scalar_value,
            i_value,
            j_value,
            k_value
        ) :

        label  = self.format_component("", False, scalar_value) + " "
        label += f"{self.format_component('i', True, i_value)} "
        label += f"{self.format_component('j', True, j_value)} "
        label += f"{self.format_component('k', True, k_value)}"

        return label


    # Invoked by : _initialise_plot

    def _create_figure_and_axes(self) :

        # self.fig = plt.figure(figsize=(8, 8))

        self.fig, (self.ax1, self.ax2) = plt.subplots(

            1, 2,
            figsize=(10, 4),
            subplot_kw={'projection': '3d'}
        )


    def _plot_axes(

            self,
            axis
    ) :

        # Plot;
        #
        #   x axis
        #   y axis
        #   z axis

        axis.quiver(
            -1.2, 0, 0,
            2.4, 0, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        axis.quiver(
            0, -1.2, 0,
            0, 2.4, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        axis.quiver(
            0, 0, -1.2,
            0, 0, 2.4,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )


    def _plot_unit_sphere(

            self,
            axis
    ) :

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

        axis.plot_surface(
            x, y, z,
            color='lightyellow',
            alpha=0.2,
            linewidth=0
        )

        axis.plot_wireframe(
            x, y, z,
            color='black',
            linewidth=0.4,
            rstride=4,
            cstride=4
        )


    def plot_quaternions(

            self,
            axis
    ) :

        nameMethod = "PlottingAgent::plot_quaternions"


        self.plot_handle_quaternion_axis_rotation = axis.quiver(

            0, 0, 0,
            self.quaternion_axis_rotation.x, self.quaternion_axis_rotation.y, self.quaternion_axis_rotation.z,
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_to_rotate = axis.quiver(

            0, 0, 0,
            self.quaternion_to_rotate.x, self.quaternion_to_rotate.y, self.quaternion_to_rotate.z,
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_pre_multiply = axis.quiver(

            0, 0, 0,
            self.quaternion_pre_multiply.x, self.quaternion_pre_multiply.y, self.quaternion_pre_multiply.z,
            color='blue',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        self.plot_handle_quaternion_rotated = axis.quiver(

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

        print(nameMethod + " : self.x_components = ")
        print(self.x_components)
        print(nameMethod + " : self.y_components = ")
        print(self.y_components)
        print(nameMethod + " : self.z_components = ")
        print(self.z_components)

        if plot_quaternion_rotated_history :

            axis.plot(

                self.quaternion_rotated.x,
                self.quaternion_rotated.y,
                self.quaternion_rotated.z,
                marker='.',
                linestyle='-',
                color='magenta'
            )

        hue_value = ((self.quaternion_pre_multiply.x) * 0.5) + 0.5

        rgb_value = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        if plot_quaternion_pre_multiply_history :

            markersize_value = (hue_value * 4) + 2

            if self.quaternion_pre_multiply.w < 0 :

                marker_value = 'v'

            else :

                marker_value = '^'

            axis.plot(

                self.quaternion_pre_multiply.x,
                self.quaternion_pre_multiply.y,
                self.quaternion_pre_multiply.z,
                marker=marker_value,
                markersize=markersize_value,
                linestyle='-',
                color=rgb_value
            )


    def check_min_max_values(self) :

        if (
            (self.quaternion_pre_multiply_max is None) or
            (self.quaternion_pre_multiply.w > self.quaternion_pre_multiply_max)
           ) :

            self.quaternion_pre_multiply_max = self.quaternion_pre_multiply.w

            hue_value = ((self.quaternion_pre_multiply.w) * 0.5) + 0.5

            self.rgb_value_max = colorsys.hsv_to_rgb(

                hue_value,  # hue (0–1)
                1.0,  # saturation
                1.0  # value
            )

        # Check if the scalar component of qv has reached a new minimum.

        if self.quaternion_pre_multiply_min is None :

            self.quaternion_pre_multiply_min = self.quaternion_pre_multiply.w

        else :

            if (self.quaternion_pre_multiply.w < self.quaternion_pre_multiply_min) :

                self.quaternion_pre_multiply_min = self.quaternion_pre_multiply.w

                hue_value = ((self.quaternion_pre_multiply.w) * 0.5) + 0.5

                self.rgb_value_min = colorsys.hsv_to_rgb(

                    hue_value,  # hue (0–1)
                    1.0,  # saturation
                    1.0  # value
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

        self.check_min_max_values()

        label_quaternion_pre_multiply_min = self.format_component("", False, self.quaternion_pre_multiply_min)
        label_quaternion_pre_multiply_max = self.format_component("", False, self.quaternion_pre_multiply_max)

        self.label_quaternion_axis_rotation    = f"Axis of rotation (q)     : " + label_quaternion_axis_rotation
        self.label_quaternion_to_rotate        = f"Quaternion to rotate (v) : " + label_quaternion_to_rotate
        self.label_quaternion_pre_multiply     = f"Pre multiplication (qv)  : " + label_quaternion_pre_multiply
        self.label_quaternion_pre_multiply_min =  "  - qv scalar min value  : " + label_quaternion_pre_multiply_min
        self.label_quaternion_pre_multiply_max =  "  - qv scalar max value  : " + label_quaternion_pre_multiply_max
        self.label_quaternion_rotated          = f"Quaternion rotated (v')  : " + label_quaternion_rotated
        self.label_angle_rotation              = f"Angle of rotation        = {self.angle_rotation:8.3f} degrees"

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


    def _set_aspect_ratios_and_extents(

            self,
            axis
    ) :

        nameMethod = "set_aspect_ratios_and_extents"


        print(nameMethod + " : Enter")

        # ----------------------------
        # Set equal aspect ratio
        # ----------------------------

        max_extent = max(
            np.max(np.abs(self.v)),
            1.0
        )

        axis.set_xlim([-max_extent, max_extent])
        axis.set_ylim([-max_extent, max_extent])
        axis.set_zlim([-max_extent, max_extent])

        axis.set_box_aspect([1, 1, 1])

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
            Line2D([0], [0], color='red',             lw=1, label=self.label_quaternion_axis_rotation),
            Line2D([0], [0], color='green',           lw=1, label=self.label_quaternion_to_rotate),
            Line2D([0], [0], color='none',            lw=1, label=self.label_quaternion_pre_multiply),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_min),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_max),
            Line2D([0], [0], color='magenta',         lw=1, label=self.label_quaternion_rotated),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_angle_rotation)
        ]

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

        # if abs(self.quaternion_pre_multiply.x) > 0.001 :

        hue_value = ((self.quaternion_pre_multiply.w) * 0.5) + 0.5

        rgb_value_local = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + f" : About to set legend color to = <{hue_value:f}, 1.0, 1.0>")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(nameMethod + " : @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        legend.get_texts()[2].set_color(rgb_value_local)

        print(nameMethod + " : Exit")


    def _fill_panes(

            self,
            axis
    ) :

        axis.xaxis.pane.fill = False
        axis.yaxis.pane.fill = False
        axis.zaxis.pane.fill = False


    def _configure_grid(

            self,
            axis
    ) :

        # ax.grid(False)

        axis.xaxis.set_major_locator(MultipleLocator(1))
        axis.yaxis.set_major_locator(MultipleLocator(1))
        axis.zaxis.set_major_locator(MultipleLocator(1))


    def add_metadata_to_file(

            self,
            filename
    ) :

        with Image.open(filename) as img :

            info = PngInfo()
            info.add_itxt(
                "com.example.simulation",
                json.dumps(self.metadata, indent=2)
            )

            img.save(filename, pnginfo=info)


    def plot_result_display_diagnostics(self) :

        nameMethod = "PlottingAgent::plot_result_display_diagnostics"


        print(nameMethod + " : Enter")

        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        print(nameMethod + " : About to invoke : self.plot_quaternions")

        print(nameMethod + " : Exit")


    def set_view(

            self,
            azimuth_view,
            elevation_view
    ) :

        self.azimuth_view   = azimuth_view
        self.elevation_view = elevation_view


    # Client : VectorManipulator::generate_plots

    def generate_plot(

            self,
            filename
    ) :

        nameMethod = "PlottingAgent::generate_plot"


        self.plot_result_display_diagnostics()

        # We need to generate the sub-plots in both self.ax1 and self.ax2.

        # Sub-plot self.ax1

        axis = self.ax1

        self.plot_quaternions(axis)
        self.add_labels_to_plot()
        self.set_title_and_legend()

        axis.view_init(

            elev=self.elevation_view,
            azim=self.azimuth_view
        )

        # Sub-plot self.ax2

        axis = self.ax2

        self.plot_quaternions(axis)
        self.add_labels_to_plot()
        self.set_title_and_legend()

        axis.view_init(

            elev=self.elevation_view,
            azim=self.azimuth_view
        )

        print("Saving the figure to file : " + str(filename) + "\n")

        self.fig.savefig(

            filename,
            dpi=300,
            bbox_inches="tight"
        )

        self.encode_metadata()
        self.add_metadata_to_file(filename)
        self.display_metadata(filename)

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

        # self.plot_handle_quaternion_rotated_history.remove()
        self.plot_handle_quaternion_rotated.remove()
        self.plot_handle_quaternion_pre_multiply.remove()
        self.plot_handle_quaternion_to_rotate.remove()
        self.plot_handle_quaternion_axis_rotation.remove()


        print(nameMethod + " : Exit")


    def destroy_plot(self) :

        nameMethod = "PlottingAgent::destroy_plot"


        print(nameMethod + " : Enter")

        # Close the figure so that we can free up the memory it is using.

        plt.close(self.fig)

        self.fig = None
        self.ax  = None

        print(nameMethod + " : Exit")