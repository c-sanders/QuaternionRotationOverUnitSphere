import sys
import numpy             as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from   matplotlib.lines  import Line2D
from   matplotlib.ticker import MultipleLocator
from   matplotlib.colors import LinearSegmentedColormap
from   matplotlib.cm     import ScalarMappable
from   matplotlib.colors import Normalize
import json

# Import the Python Image Library, aka PIL.

from PIL import Image
from PIL.PngImagePlugin import PngInfo

import colorsys

import GlobalSettings


show_plots = False

my_colormap = LinearSegmentedColormap.from_list(
    "my_rainbow",
    [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet"
    ]
)


class PlottingAgent :

    class PlotHandleAgent_Plot :

        def __init__(self,

            plotting_agent : PlottingAgent
        ) :

            self._plotting_agent = plotting_agent

            # Title of sub-plot.

            self._plot_handle_title_subplot_1                 = None

            # Vector and history of vector points.

            self._plot_handle_quaternion_pre_multiply         = None
            self._plot_handle_quaternion_pre_multiply_history = None

            # The unit sphere.

            self._plot_handle_surface                         = None

            # Colormap and associated arrow.

            self._plot_handle_colormap                        = None
            self._plot_handle_colormap_arrow                  = None


    class PlotHandleAgent_SubPlot_1 :

        def __init__(self,

            plotting_agent: PlottingAgent
        ) :

            self._plotting_agent = plotting_agent

            # Title of sub-plot.

            self._plot_handle_title_subplot              = None

            # Vectors and history of vector points.

            self._plot_handle_axis_rotation              = None
            self._plot_handle_to_rotate                  = None
            self._plot_handle_quaternion_rotated         = None
            self._plot_handle_quaternion_rotated_history = None


        def set_plot_handle_title_subplot_1(self,

                plot_handle_title
        ) :

            if self._plot_handle_title_subplot_1 is not None :

                raise Exception("Attribute _plot_handle_title_subplot_1 : Trying to set this attribute whilst it is already set.")

            self.plot_handle_title_subplot_1 = plot_handle_title


        def clear_plot_handle_title_subplot_1(self) :

            if self._plot_handle_title_subplot_1 is not None:

                self._plot_handle_title_subplot_1.remove()
                self._plot_handle_title_subplot_1 = None



    class PlotHandleAgent_SubPlot_2 :

        """This class handles all the artifacts/artists that are required by the plots.

        By placing all the artifacts/artists in this class, it allows the class to maintain
        strict control over the artifacts/artists, i.e. control when and how they are created,
        and under what conditions they are destroyed.

        Attributes:
            owner (str): The account owner's name.
            balance (float): The current account balance.
        """

        def __init__(self,

            plotting_agent : PlottingAgent
        ) :

            self._plotting_agent = plotting_agent


        def set_plot_handle_title_subplot_2(self,

                plot_handle_title
        ) :

            if self._plot_handle_title_subplot_2 is not None :

                raise Exception("Attribute _plot_handle_title_subplot_2 : Trying to set this attribute whilst it is already set.")

            self.plot_handle_title_subplot_2 = plot_handle_title


        def clear_plot_handle_surface(self) :

            if self._plot_handle_surface is not None:

                self._plot_handle_surface.remove()
                self._plot_handle_surface = None


        def set_plot_handle_quaternion_pre_multiply(self) :

            if self._plot_handle_quaternion_pre_multiply is not None:

                raise Exception("Attribute _plot_handle_quaternion_pre_multiply : Trying to set this attribute whilst it is already set.")

            self._plot_handle_quaternion_pre_multiply = self._plotting_agent.ax1.quiver(

                0, 0, 0,
                self._plotting_agent.quaternion_pre_multiply.x, self._plotting_agent.quaternion_pre_multiply.y, self._plotting_agent.quaternion_pre_multiply.z,
                color='blue',
                linewidth=1,
                arrow_length_ratio=0.1
            )


    def __init__(

            self,
            title_plots
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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

        self.rgb_value_sphere_subplot_1 = None
        self.rgb_value_sphere_subplot_2 = None

        self.plot_handle_agent = PlottingAgent.PlotHandleAgent(self)

        # Component arrays to hold the history of the rotated vector.

        self.x_components = []
        self.y_components = []
        self.z_components = []

        self.azimuth_view   = None
        self.elevation_view = None

        self.rgb_value_min = colorsys.hsv_to_rgb(0, 0, 1.0)
        self.rgb_value_max = colorsys.hsv_to_rgb(0, 0, 1.0)

        self.label_quaternion_axis_rotation    = ""
        self.label_quaternion_to_rotate        = ""
        self.label_quaternion_pre_multiply     = ""
        self.label_quaternion_pre_multiply_min = ""
        self.label_quaternion_pre_multiply_max = ""
        self.label_quaternion_rotated          = ""
        self.label_angle_rotation              = ""

        self._initialise_plot()


    def _initialise_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._create_figure_and_axes()

        self._initialise_subplot_1()
        self._initialise_subplot_2()

        print(nameMethod + " : Exit")


    def _add_colormap(self) :

        nameMethod  = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        # Place a color scale on the right hand side of this sub-plot.

        norm = Normalize(vmin=-1.0, vmax=1.0)

        sm = ScalarMappable(
            norm=norm,
            cmap=my_colormap
        )
        sm.set_array([])

        self.plot_handle_colormap = self.fig.colorbar(
            sm,
            ax=self.ax1,
            location="left",
            pad=0.05,
            shrink=0.75
        )

        self.plot_handle_colormap.set_label(GlobalSettings.title_colormap)


    def _initialise_subplot_1(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        axis = self.ax1


        print(nameMethod + " : Enter")

        # self._plot_unit_sphere_quaternion_pre_multiply()
        self._plot_axes(axis)

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self._set_aspect_ratios_and_extents(axis)

        self._fill_panes(axis)
        self._configure_grid(axis)
        # self.create_static_labels()
        self._add_colormap()

        print(nameMethod + " : Exit")


    def _initialise_subplot_2(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        axis = self.ax2


        print(nameMethod + " : Enter")

        self._plot_unit_sphere_quaternion_rotation()
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


    def _format_component(

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


    def _generate_string(

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

            2, 1,
            figsize=(8, 10),
            subplot_kw={'projection': '3d'}
        )


    # Invoked by : _initialise_subplot_1

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


    # Invoked by : _plot_quaternion_pre_multiply

    def _plot_unit_sphere_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        axis = self.ax1


        print(nameMethod + " : Enter")

        # ----------------------------
        # Plot the unit sphere.
        # ----------------------------

        u = np.linspace(0, 2 * np.pi, 100)
        v_sphere = np.linspace(0, np.pi, 100)

        x = np.outer(np.cos(u), np.sin(v_sphere))
        y = np.outer(np.sin(u), np.sin(v_sphere))
        z = np.outer(np.ones_like(u), np.cos(v_sphere))

        # If this sub-plot already contains a plot of a unit sphere, then delete it.

        self.plot_handle_agent.clear_plot_handle_surface()

        print(nameMethod + " : MARKER 2")

        self.plot_handle_surface = axis.plot_surface(x, y, z,
                                                     color=self.rgb_value_sphere_subplot_1,
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

        print(nameMethod + " : Exit")


    def _plot_unit_sphere_quaternion_rotation(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        axis = self.ax2


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

        hue_value = 0.5

        rgb_value = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        axis.plot_surface(
            x, y, z,
            color=rgb_value,
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


    # Invoked by : _generate_subplot_1

    def _plot_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        sub_plot = self.ax1


        print(nameMethod + " : Enter")

        self._plot_unit_sphere_quaternion_pre_multiply()

        print(nameMethod + " : MARKER 0")

        self.plot_handle_agent.set_plot_handle_quaternion_pre_multiply()

        # If w = 0, plot this quaternion in the pure imaginary space as well and keep this plot
        # there. That is, do not remove it from the plot.

        if abs(self.quaternion_pre_multiply.w) < 0.001 :

            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : Plotting vector in the pure imaginary space")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # We do not need a handle to this artifact, as we are never going to remove it.

            self.ax2.quiver(

                0, 0, 0,
                self.quaternion_pre_multiply.x, self.quaternion_pre_multiply.y, self.quaternion_pre_multiply.z,
                color='blue',
                linewidth=1,
                arrow_length_ratio=0.1
            )

        if GlobalSettings.plot_quaternion_pre_multiply_history :

            # Append the current point onto the end of the plot history.

            hue_value = ((self.quaternion_pre_multiply.x) * 0.5) + 0.5

            rgb_value = colorsys.hsv_to_rgb(

                hue_value,  # hue (0–1)
                1.0,  # saturation
                1.0  # value
            )

            markersize_value = (hue_value * 4) + 2

            if self.quaternion_pre_multiply.w < 0 :

                marker_value = 'v'

            else :

                marker_value = '^'

            sub_plot.plot(

                self.quaternion_pre_multiply.x,
                self.quaternion_pre_multiply.y,
                self.quaternion_pre_multiply.z,
                marker=marker_value,
                markersize=markersize_value,
                linestyle='-',
                color=rgb_value
            )


    def _plot_quaternions(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        sub_plot = self.ax2


        # Plot an arrow from the origin which represents : the axis of rotation

        self.plot_handle_quaternion_axis_rotation = sub_plot.quiver(

            0, 0, 0,
            self.quaternion_axis_rotation.x, self.quaternion_axis_rotation.y, self.quaternion_axis_rotation.z,
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion which is to be rotated.

        self.plot_handle_quaternion_to_rotate = sub_plot.quiver(

            0, 0, 0,
            self.quaternion_to_rotate.x, self.quaternion_to_rotate.y, self.quaternion_to_rotate.z,
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion after it has been rotated.

        self.plot_handle_quaternion_rotated = sub_plot.quiver(

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

        if GlobalSettings.plot_quaternion_rotated_history :

            sub_plot.plot(

                self.quaternion_rotated.x,
                self.quaternion_rotated.y,
                self.quaternion_rotated.z,
                marker='.',
                linestyle='-',
                color='magenta'
            )


    def _check_min_max_values(self) :

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


    def _add_labels_to_plot(

            self,
            axis
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

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

        axis.text(
            1.3, 0, 0,
            "x",
            color="black"
        )

        axis.text(
            0, 1.3, 0,
            "y",
            color="black"
        )

        axis.text(
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


    def _encode_metadata(self) :

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


    def _display_metadata(

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


    def _set_legend_subplot_1(self) :

        nameMethod = "PlottingAgent::_set_legend_subplot_1"


        print(nameMethod + " : Enter")

        # Configure the individual elements which will comprise the legend.

        legend_elements = [

            # Line2D([0], [0], color='red',             lw=1, label=self.label_quaternion_axis_rotation),
            # Line2D([0], [0], color='green',           lw=1, label=self.label_quaternion_to_rotate),
            Line2D([0], [0], color='none',     lw=1,        label=self.label_quaternion_pre_multiply),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_min),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_max),
            # Line2D([0], [0], color='magenta',         lw=1, label=self.label_quaternion_rotated),
            Line2D([0], [0], linestyle='None', marker=None, label=self.label_angle_rotation)
        ]

        # Configure the legend itself and set the subplot to use it.

        self.plot_handle_legend = self.ax1.legend(

            handles=legend_elements,
            prop={
                "family": "Liberation Mono",
                "size": 10
            },
            loc='lower center',
            fontsize=10
        )

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

        self.plot_handle_legend.get_texts()[2].set_color(rgb_value_local)

        print(nameMethod + " : Exit")


    # Invoked by : PlottingAgent::_generate_subplot_1

    def _set_title_and_legend_subplot_1(self) :

        nameMethod = "PlottingAgent::_set_title_and_legend_subplot_1"


        print(nameMethod + " : Enter")

        # ----------------------------
        # Labels
        # ----------------------------

        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        # ax.set_zlabel('z')
        # self.fig.set_title("Poop")

        # Set the title for subplot 1.

        self.plot_handle_agent.set_plot_handle_title_subplot_1(GlobalSettings.title_sub_plot_1)

        # Set the legend for subplot 1.

        if (
            (GlobalSettings.display_legend_subplot_1) and
            (self.plot_handle_title_subplot_1 is None)
        ) :

            self._set_legend_subplot_1()

        print(nameMethod + " : Exit")


    # Invoked by : _generate_subplot_2()

    def _set_title_and_legend_subplot_2(self):

        """
        Set the title and legend for the specified plot or sub-plot.

        This method sets the title and legend for the plot or sub-plot which was passed to the argument axis.

        Args:
            axis (matplotlib.axes.Axes):
                The plot or sub-plot which is to be operated on.

        Returns:
            None:
                This method only updates the internal state of the object.
        """

        nameMethod = "PlottingAgent::_set_title_and_legend_subplot_2"


        print(nameMethod + " : Enter")

        self.ax2.set_title(GlobalSettings.title_sub_plot_2)

        # ----------------------------
        # Labels
        # ----------------------------

        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        # ax.set_zlabel('z')

        if GlobalSettings.display_legend_subplot_2 :

            legend_elements = [
                Line2D([0], [0], color='red',             lw=1, label=self.label_quaternion_axis_rotation),
                Line2D([0], [0], color='green',           lw=1, label=self.label_quaternion_to_rotate),
                Line2D([0], [0], color='none',            lw=1, label=self.label_quaternion_pre_multiply),
                Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_min),
                Line2D([0], [0], linestyle='None', marker=None, label=self.label_quaternion_pre_multiply_max),
                Line2D([0], [0], color='magenta',         lw=1, label=self.label_quaternion_rotated),
                Line2D([0], [0], linestyle='None', marker=None, label=self.label_angle_rotation)
            ]

            legend = self.ax2.legend(
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


    def _add_metadata_to_file(

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


    def _plot_result_display_diagnostics(self) :

        nameMethod = "PlottingAgent::_plot_result_display_diagnostics"


        print(nameMethod + " : Enter")

        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : self.angle_rotation = " + str(self.angle_rotation))
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        print(nameMethod + " : Exit")


    def set_titles(

        self,
        title_plot,
        title_sub_plot_1,
        title_sub_plot_2
    ) :

        self.title_plot       = title_plot
        self.title_sub_plot_1 = title_sub_plot_1
        self.title_sub_plot_2 = title_sub_plot_2


    def set_view(

            self,
            azimuth_view,
            elevation_view
    ) :

        self.azimuth_view   = azimuth_view
        self.elevation_view = elevation_view


    # Invoked by : _generate_subplots

    def _generate_subplot_1(self) :

        nameMethod = "PlottingAgent::_generate_subplot_1"


        print(nameMethod + " : Enter")

        #

        self._plot_quaternion_pre_multiply()
        # self.add_labels_to_plot(axis)

        print(nameMethod + " : MARKER 0")

        self._set_title_and_legend_subplot_1()

        print(nameMethod + " : MARKER 1")

        # Update the arrow that points to the colorbar.

        current_value = self.quaternion_pre_multiply.w

        print(nameMethod + " : MARKER 2")

        self.plot_handle_colormap_arrow = self.plot_handle_colormap.ax.annotate(
            "",
            xy=(1.0, current_value),  # Arrow tip
            xytext=(1.5, current_value),  # Arrow tail
            xycoords=("axes fraction", "data"),
            textcoords=("axes fraction", "data"),
            arrowprops=dict(
                arrowstyle="simple",
                color="black",
                lw=2
            )
        )

        self.ax1.view_init(

            elev=self.elevation_view,
            azim=self.azimuth_view
        )

        print(nameMethod + " : Exit")


    def _generate_subplot_2(self) :

        nameMethod = "PlottingAgent::_generate_subplot_2"


        print(nameMethod + " : Enter")

        self._plot_quaternions()
        # self.add_labels_to_plot(axis)
        self._set_title_and_legend_subplot_2()

        self.ax2.view_init(

            elev=self.elevation_view,
            azim=self.azimuth_view
        )

        print(nameMethod + " : Exit")


    def _save_plot_to_file(

            self,
            filename
    ) :

        nameMethod = "PlottingAgent::_save_plot_to_file"


        print(nameMethod + " : Enter")

        print("Saving the figure to file : " + str(filename) + "\n")

        self.fig.savefig(

            filename,
            dpi=300,
            bbox_inches="tight"
        )

        print(nameMethod + " : Exit")


    def _encode_metadata_into_file(

            self,
            filename
    ) :

        nameMethod = "PlottingAgent::_encode_metadata_and_add_to_file"


        print(nameMethod + " : Enter")

        self._encode_metadata()
        self._add_metadata_to_file(filename)
        self._display_metadata(filename)

        print(nameMethod + " : Exit")


    # Invoked by : _remove_artifacts_from_subplots

    def _remove_artifacts_from_subplot_1(self):

        nameMethod = "PlottingAgent::_remove_artifacts_from_subplot_1"


        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : Enter")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # Remove the artifacts from the plot self.ax2

        if self.plot_handle_colormap_arrow is not None:

            self.plot_handle_colormap_arrow.remove()
            self.plot_handle_colormap_arrow = None

        if self.plot_handle_surface is not None:

            self.plot_handle_surface.remove()
            self.plot_handle_surface = None

        if self.plot_handle_quaternion_pre_multiply is not None :

            self.plot_handle_quaternion_pre_multiply.remove()
            self.plot_handle_quaternion_pre_multiply = None

        print(nameMethod + " : Exit")


    # Invoked by : _remove_artifacts_from_subplots

    def _remove_artifacts_from_subplot_2(self):

        nameMethod = "PlottingAgent::_remove_artifacts_from_subplot_2"

        print(nameMethod + " : Enter")

        # Remove certain artifacts that are used by the sub-plot self.ax1.
        #
        # Keep the following artifacts however, because they don't change and will simply get redrawn in the next plot.
        #
        #   self.plot_handle_quaternion_to_rotate.remove()
        #   self.plot_handle_quaternion_axis_rotation.remove()
        #
        # Also, keep the history plot points as they just get added to.

        if self.plot_handle_quaternion_rotated is not None:

            self.plot_handle_quaternion_rotated.remove()
            self.plot_handle_quaternion_rotated = None

        print(nameMethod + " : Exit")


    # Invoked by : generate_plot

    def _remove_artifacts_from_subplots(self) :

        nameMethod = "PlottingAgent::_remove_artifacts_from_subplots"


        print(nameMethod + " : Enter")

        self._remove_artifacts_from_subplot_2()
        self._remove_artifacts_from_subplot_1()

        print(nameMethod + " : Exit")


    def _remove_artifacts_from_plot(self) :

        nameMethod = "PlottingAgent::_remove_artifacts_from_plot"


        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : Enter")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # Remove artifacts from the sub-plots.

        self._remove_artifacts_from_subplots()

        # Remove artifacts from the plot itself.

        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : Exit")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


    # Invoked by : generate_plot

    def _generate_subplots(self) :

        # Generate the sub-plots for both self.ax1 and self.ax2.

        self._generate_subplot_1()
        self._generate_subplot_2()


    def _set_title_plot(self) :

        nameMethod = "PlottingAgent::_set_title_plot"


        print(nameMethod + " : Enter")

        # Set the title for the entire plot.

        self.fig.suptitle(
            GlobalSettings.title_plot,
            fontsize=14
        )

        print(nameMethod + " : Exit")


    def _show_plot_if_enabled(self) :

        nameMethod = "PlottingAgent::_show_plot"


        print(nameMethod + " : Enter")

        if show_plots :

            plt.show()

        print(nameMethod + " : Exit")


    def _set_rgb_value_for_sphere_surface_subplot_1(self) :

        nameMethod = "PlottingAgent::_set_rgb_value_for_sphere_surface_subplot_1"


        print(nameMethod + " : Enter")

        if self.quaternion_pre_multiply is None :

            hue_value = 0.5

        else :

            hue_value = ((self.quaternion_pre_multiply.w) * 0.5) + 0.5

        self.rgb_value_sphere_surface_subplot_1 = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        print(nameMethod + " : Exit")


    def _set_rgb_value_for_sphere_surface_subplot_2(self):

        nameMethod = "PlottingAgent::_set_rgb_value_for_sphere_surface_subplot_2"


        print(nameMethod + " : Enter")

        print(nameMethod + " : Exit")


    # Invoked by :

    def _set_rgb_values_for_sphere_surfaces(self) :

        nameMethod = "PlottingAgent::_set_rgb_values_for_sphere_surfaces"


        print(nameMethod + " : Enter")

        self._set_rgb_value_for_sphere_surface_subplot_1()
        self._set_rgb_value_for_sphere_surface_subplot_2()

        self.hue_value_sphere_subplot_1 = None
        self.hue_value_sphere_subplot_2 = None

        print(nameMethod + " : Exit")


    # Invoked by : QuaternionManipulator::generate_plots
    #
    # generate_plot
    #   |- self._plot_result_display_diagnostics
    #   |
    #   |- self._set_title_plot()
    #   |- self._set_rgb_values_for_sphere_surfaces()
    #   |- self._generate_subplots()
    #   |    |- self._generate_subplot_1()
    #   |    |- self._generate_subplot_2()
    #   |         |- self._plot_quaternions()
    #   |         |- self.add_labels_to_plot()
    #   |         |- self._set_title_and_legend_subplot_2()
    #   |
    #   |- self._save_plot_to_file
    #   |- self._encode_metadata_into_file
    #   |- self._remove_artifacts_from_subplots

    def generate_plot(self,

            filename
    ) :

        nameMethod = "PlottingAgent::generate_plot"


        print(nameMethod + " : Enter")

        self._plot_result_display_diagnostics()

        # Plot handles may be created by the following methods.
        #
        #

        self._set_title_plot()
        self._set_rgb_values_for_sphere_surfaces()
        self._generate_subplots()

        # Plot handles shouldn't be created by the following methods.

        self._save_plot_to_file(filename)
        self._encode_metadata_into_file(filename)
        self._show_plot_if_enabled()

        # Destroy those plot handles which aren't required anymore.

        self._remove_artifacts_from_plot()

        print(nameMethod + " : Exit")


    def _destroy_plot(self) :

        nameMethod = "PlottingAgent::destroy_plot"


        print(nameMethod + " : Enter")

        # Close the figure so that we can free up the memory it is using.

        plt.close(self.fig)

        self.fig = None
        self.ax  = None

        print(nameMethod + " : Exit")