import sys
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

import GlobalSettings
import Utils

import PlotHandleAgent_SubPlot_1
import PlotHandleAgent_SubPlot_2


show_plots = False


class PlottingAgent :

    """
    Implements a class which is responsible for generating plots.

    The plots which this class generates, will be of the terms which are involved in a quaternionic rotation. Each plot
    will be composed of two sub-plots, where each of the two sub-plots is handled by its own class within this class.

    The terms which are involved in the quaternionic rotation - along with the viewing angle information, need to be
    passed into this class before it can generate a plot. Upon receiving all of this information, the class will store
    its own copies of it. By doing this, the information is then available to its two subclasses.
    """

    class PlotHandleAgent_Plot :

        def __init__(self,

            plotting_agent : PlottingAgent
        ) :

            self._plotting_agent = plotting_agent


    def __init__(

            self,
            title_plot
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._initialise_attributes(title_plot)
        self._initialise_plot()

        # We can create the sub-plots now that the main plot has been fully initialised.

        self._create_subplots()
        self._initialise_subplots()

        print(nameMethod + " : %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(nameMethod + " : %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(nameMethod + " : Exit")
        print(nameMethod + " : %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(nameMethod + " : %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    def _initialise_attributes(self,

        title_plot
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Attributes which pertain to the layout of the plot.

        self._fig                         = None
        self._ax1                         = None
        self._ax2                         = None

        self._title_plot                  = title_plot

        # Attributes which pertain to the quaternion rotation.
        #
        # These are local copies of externally generated data.

        self._angle_rotation              = None

        self._quaternion_axis_rotation    = None
        self._quaternion_to_rotate        = None
        self._quaternion_pre_multiply     = None
        self._quaternion_rotated          = None

        self._quaternion_pre_multiply_min = None
        self._quaternion_pre_multiply_max = None

        # Component arrays to hold the history of the rotated vector.

        self._x_components                = []
        self._y_components                = []
        self._z_components                = []

        # Attributes which pertain to the plot's viewing angle.

        self._azimuth_view                = None
        self._elevation_view              = None

        self._subPlot_1                   = None
        self._subPlot_2                   = None

        print(nameMethod + " : Exit")


    # Invoked by : __init__

    def _initialise_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._create_figure_and_axes()

        print(nameMethod + " : Exit")


    def _create_subplots(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # self.plot_handle_agent = PlottingAgent.PlotHandleAgent_Plot(self)
        self._subPlot_1 = PlotHandleAgent_SubPlot_1.PlotHandleAgent_SubPlot_1(self)
        self._subPlot_2 = PlotHandleAgent_SubPlot_2.PlotHandleAgent_SubPlot_2(self)

        print(nameMethod + " : Exit")


    def _initialise_subplots(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._subPlot_1.configure()
        self._subPlot_2.configure()

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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Update the quaternion values.

        self._quaternion_axis_rotation = quaternion_axis_rotation
        self._quaternion_to_rotate     = quaternion_to_rotate
        self._quaternion_pre_multiply  = quaternion_pre_multiply
        self._quaternion_rotated       = quaternion_rotated

        self._update_quaternion_history()

        self._update_min_max_values()

        print(nameMethod + " : Exit")


    def _update_quaternion_history(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Add the point to the list of points.

        self._x_components.append(self._quaternion_rotated.x)
        self._y_components.append(self._quaternion_rotated.y)
        self._z_components.append(self._quaternion_rotated.z)

        print(f"Length self.x_components = {len(self._x_components):d}")
        print(f"Length self.y_components = {len(self._y_components):d}")
        print(f"Length self.z_components = {len(self._z_components):d}")

        print(nameMethod + " : self._plotting_agent.x_components = ")
        print(self._x_components)
        print(nameMethod + " : self._plotting_agent.y_components = ")
        print(self._y_components)
        print(nameMethod + " : self._plotting_agent.z_components = ")
        print(self._z_components)

        print(nameMethod + " : Exit")


    # Invoked by : _initialise_plot

    def _create_figure_and_axes(self) :

        # self.fig = plt.figure(figsize=(8, 8))

        self.fig, (self.ax1, self.ax2) = plt.subplots(

            2, 1,
            figsize=GlobalSettings.image_dimensions,
            subplot_kw={'projection': '3d'}
        )


    # Invoked by : _plot_quaternion_pre_multiply

    def plot_unit_sphere_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        axis = self.ax1


        print(nameMethod + " : Enter")

        self._subPlot_1.plot_unit_sphere(axis)

        print(nameMethod + " : Exit")


    # Invoked by : _generate_subplot_1

    def _plot_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._subPlot_1.plot_quaternion_pre_multiply()
        self._subPlot_2.plot_quaternion_pre_multiply()

        print(nameMethod + " : Exit")


    def _update_min_max_values(self) :

        if (
            (self._quaternion_pre_multiply_max is None) or
            (self._quaternion_pre_multiply.w > self._quaternion_pre_multiply_max)
           ) :

            self._quaternion_pre_multiply_max = self._quaternion_pre_multiply.w

            hue_value = ((self._quaternion_pre_multiply.w) * 0.5) + 0.5

            self.rgb_value_max = colorsys.hsv_to_rgb(

                hue_value,  # hue (0–1)
                1.0,  # saturation
                1.0  # value
            )

        # Check if the scalar component of qv has reached a new minimum.

        if (
            (self._quaternion_pre_multiply_min is None) or
            (self._quaternion_pre_multiply.w < self._quaternion_pre_multiply_min)
           ) :

            self._quaternion_pre_multiply_min = self._quaternion_pre_multiply.w

            hue_value = ((self._quaternion_pre_multiply.w) * 0.5) + 0.5

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

        label_quaternion_pre_multiply_min = format_component("", False, self.quaternion_pre_multiply_min)
        label_quaternion_pre_multiply_max = format_component("", False, self.quaternion_pre_multiply_max)

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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        self.metadata = {
            "view" : {
                "azimuth"   : self._azimuth_view,
                "elevation" : self._elevation_view
            },
            "rotation" : {
                "angle" : self.angle_rotation,
                "axis" : {
                    "scalar" : self._quaternion_axis_rotation.w,
                    "x"      : self._quaternion_axis_rotation.x,
                    "y"      : self._quaternion_axis_rotation.y,
                    "z"      : self._quaternion_axis_rotation.z
                },
            },
            "quaternion_to_rotate": {
                "scalar"     : self._quaternion_to_rotate.w,
                "x"          : self._quaternion_to_rotate.x,
                "y"          : self._quaternion_to_rotate.y,
                "z"          : self._quaternion_to_rotate.z
            },
            "quaternion_pre_multiply": {
                "scalar"     : self._quaternion_pre_multiply.w,
                "x"          : self._quaternion_pre_multiply.x,
                "y"          : self._quaternion_pre_multiply.y,
                "z"          : self._quaternion_pre_multiply.z
            },
            "quaternion_rotated": {
                "scalar"     : self._quaternion_rotated.w,
                "x"          : self._quaternion_rotated.x,
                "y"          : self._quaternion_rotated.y,
                "z"          : self._quaternion_rotated.z
            },
        }


    def _display_metadata(

            self,
            filename
        ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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


    # Invoked by : PlottingAgent::_generate_subplot_1

    def _set_title_and_legend_subplot_1(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # ----------------------------
        # Labels
        # ----------------------------

        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        # ax.set_zlabel('z')
        # self.fig.set_title("Poop")

        # Set the title for subplot 1.

        self._subPlot_1.set_title(GlobalSettings.title_sub_plot_1, GlobalSettings.raise_exception_if_already_set)

        self._subPlot_1.set_legend()

        print(nameMethod + " : MARKER A")

        # Set the legend for subplot 1.

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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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

        self._azimuth_view   = azimuth_view
        self._elevation_view = elevation_view


    def _save_plot_to_file(

            self,
            filename
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        print("Saving the figure to file : " + str(filename) + "\n")

        self.fig.savefig(

            filename,
            dpi         = GlobalSettings.image_dpi,
            bbox_inches = GlobalSettings.image_bbox_argument
        )

        with Image.open(filename) as image_handle :

            print(nameMethod + " : ????????????????????????????????????????")
            print(nameMethod + " : ????????????????????????????????????????")
            print(nameMethod + " : Image dimensions = " + str(image_handle.size))
            print(nameMethod + " : ????????????????????????????????????????")
            print(nameMethod + " : ????????????????????????????????????????")

        print(nameMethod + " : Exit")


    def _encode_metadata_into_file(

            self,
            filename
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._encode_metadata()
        self._add_metadata_to_file(filename)
        self._display_metadata(filename)

        print(nameMethod + " : Exit")


    # Invoked by : _remove_artifacts_from_subplots

    def _remove_artifacts_from_subplot_1(self):

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : Enter")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # Remove certain artifacts that are used by the sub-plot self.ax1.
        #
        # Keep the following artifacts however, because they don't change and will simply get redrawn in the next plot.
        #
        #   self.plot_handle_quaternion_to_rotate.remove()
        #   self.plot_handle_quaternion_axis_rotation.remove()
        #
        # Also, keep the history plot points as they just get added to.

        self.subPlot_2_handle_agent.clear_artifacts()
        self.subPlot_1_handle_agent.clear_artifacts()

        print(nameMethod + " : Exit")


    # Invoked by : _remove_artifacts_from_subplots

    def _remove_artifacts_from_subplot_2(self):

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        print(nameMethod + " : Enter")

        self.subPlot_2_handle_agent.clear_artifacts()

        print(nameMethod + " : Exit")


    # Invoked by : _remove_artifacts_from_plot

    def _remove_artifacts_from_subplots(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._subPlot_2.clear_artifacts()
        self._subPlot_1.clear_artifacts()

        print(nameMethod + " : Exit")


    def _remove_artifacts_from_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Generate the sub-plots for both self.ax1 and self.ax2.

        self._subPlot_1.generate_plot()
        self._subPlot_2.generate_plot()

        print(nameMethod + " : Exit")


    def _set_title_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Set the title for the entire plot.

        self.fig.suptitle(
            GlobalSettings.title_plot,
            fontsize=20
        )

        print(nameMethod + " : Exit")


    def _show_plot_if_enabled(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if show_plots :

            plt.show()

        print(nameMethod + " : Exit")


    # Invoked by : generate_plot

    def _set_rgb_values_for_sphere_surfaces(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._subPlot_1._set_rgb_value_for_sphere_surface()

        print(nameMethod + " : MARKER 1")

        self._subPlot_2._set_rgb_value_for_sphere_surface()

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

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : Enter")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(nameMethod + " : >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        self._plot_result_display_diagnostics()

        # Plot handles may be created by the following methods.

        self._set_title_plot()
        self._set_rgb_values_for_sphere_surfaces()
        self._generate_subplots()

        # Plot handles shouldn't be created by the following methods.

        self._save_plot_to_file(filename)
        self._encode_metadata_into_file(filename)
        self._show_plot_if_enabled()

        # Destroy those plot handles which aren't required anymore.

        self._remove_artifacts_from_plot()

        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : Exit")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(nameMethod + " : <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


    def _destroy_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Close the figure so that we can free up the memory it is using.

        plt.close(self.fig)

        self.fig = None
        self.ax  = None

        print(nameMethod + " : Exit")