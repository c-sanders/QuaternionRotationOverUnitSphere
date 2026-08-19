import sys
import colorsys

import numpy as np

from   matplotlib.lines  import Line2D
from   matplotlib.colors import LinearSegmentedColormap
from   matplotlib.colors import Normalize
from   matplotlib.cm     import ScalarMappable

import GlobalSettings
import Utils
import SubPlotAgent
import PlottingAgent


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


class PlotHandleAgent_SubPlot_1(SubPlotAgent.SubPlotAgent) :

    # Only create an instance of this class once an instance of the PlottingAgent class has been fully configures.

    def __init__(self,

        plotting_agent: PlottingAgent.PlottingAgent
    ) :

        super().__init__(plotting_agent)

        self._plot_handle_title                           = None

        # Set the following attributes;
        #
        #   - colormap and its associated arrow
        #   - vector and history of vector points

        self._plot_handle_colormap                        = None
        self._plot_handle_colormap_arrow                  = None
        self._plot_handle_colormap_arrow_min              = None
        self._plot_handle_colormap_arrow_max              = None

        self._plot_handle_quaternion_pre_multiply         = None
        self._plot_handle_quaternion_pre_multiply_history = None

        self.rgb_value_min                                = colorsys.hsv_to_rgb(0, 0, 1.0)
        self.rgb_value_max                                = colorsys.hsv_to_rgb(0, 0, 1.0)

        self._initialise_plot()


    def _initialise_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        print(nameMethod + " : Exit")


    def configure(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._axis = self._plotting_agent._ax1

        self._add_colormap()
        self._plot_unit_sphere()
        self._plot_axes()

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self._set_aspect_ratios_and_extents()

        self._fill_panes()
        self._configure_grid()
        # self.create_static_labels()

        print(nameMethod + " : Exit")


    # Invoked by : generate_plot

    def _set_title(self,

        plot_handle_title,
        raise_if_set
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if (
            (raise_if_set) and
            (self._plot_handle_title is not None)
        ) :

            raise Exception("Attribute _plot_handle_title : Trying to set this attribute whilst it is already set.")

        # self._plot_handle_title = plot_handle_title

        w = Utils.format_component("", False, self._plotting_agent._quaternion_pre_multiply.w)

        local_string = f"Hue = {self._hue_value:.3f}"

        title_sub_plot = r"$qv$ in $S^{3}$ with $w=" + str(w) + "$ : " + str(local_string)

        self._axis.set_title(
            title_sub_plot,
            fontsize=14
        )

        print(nameMethod + " : Exit")


    def clear_plot_title(self) :

        if self._plot_handle_title is not None :

            self._plot_handle_title.remove()
            self._plot_handle_title = None


    # Invoked by : configure

    def _set_aspect_ratios_and_extents(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # ----------------------------
        # Set equal aspect ratio
        # ----------------------------

        max_extent = max(
                         np.max(np.abs(self._v)),
                         1.0
                        )

        self._axis.set_xlim([-max_extent, max_extent])
        self._axis.set_ylim([-max_extent, max_extent])
        self._axis.set_zlim([-max_extent, max_extent])

        self._axis.set_box_aspect([1, 1, 1])

        print(nameMethod + " : Exit")


    # Invoked by : configure

    def _add_colormap(self) :

        nameMethod  = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        # Place a color scale on the right hand side of this sub-plot.

        norm = Normalize(vmin=-0.6, vmax=0.6)

        sm = ScalarMappable(
            norm=norm,
            cmap=my_colormap
        )
        sm.set_array([])

        self._plot_handle_colormap = self._plotting_agent._fig.colorbar(
            sm,
            ax=self._axis,
            location="left",
            pad=0.05,
            shrink=0.75
        )

        self._plot_handle_colormap.set_label(GlobalSettings.title_colormap)


    def _clear_sphere_wire_frame(self) :

        if self._plot_handle_sphere_wire_frame is not None :

            self._plot_handle_sphere_wire_frame.remove()
            self._plot_handle_sphere_wire_frame = None


    # Invoked by : PlottingAgent::_plot_unit_sphere_quaternion_pre_multiply

    def _clear_sphere_surface(self):

        if self._plot_handle_surface is not None :

            self._plot_handle_surface.remove()
            self._plot_handle_surface = None


    def _clear_plot_handle_colormap_arrows(self):

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : Enter")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if self._plot_handle_colormap_arrow is not None :

            print(nameMethod + " : self._plot_handle_colormap_arrow is not None")

            self._plot_handle_colormap_arrow.remove()
            self._plot_handle_colormap_arrow = None

        self._plot_handle_colormap_arrow_min.remove()
        self._plot_handle_colormap_arrow_max.remove()

        self._plot_handle_colormap_arrow_min = None
        self._plot_handle_colormap_arrow_max = None

        print(nameMethod + " : self._plot_handle_colormap_arrow is None")

        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : Exit")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(nameMethod + " : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def _clear_plot_handle_quaternion_pre_multiply(self) :

        if self._plot_handle_quaternion_pre_multiply is not None :

            self._plot_handle_quaternion_pre_multiply.remove()
            self._plot_handle_quaternion_pre_multiply = None


    def clear_artifacts(self):

        self._clear_plot_handle_quaternion_pre_multiply()
        self._clear_sphere_wire_frame()
        self._clear_sphere_surface()
        self._clear_plot_handle_colormap_arrows()


    # Invoked by : generate_plot

    def _update_colorbar(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # If an arrow currently points to the colorbar, then remove it.
        # Then place a new updated arrow next to the colorbar.

        # self.clear_plot_handle_colormap_arrow()

        current_value     = self._plotting_agent._quaternion_pre_multiply.w
        current_value_min = self._plotting_agent._quaternion_pre_multiply_min
        current_value_max = self._plotting_agent._quaternion_pre_multiply_max

        print(nameMethod + " : MARKER 2")

        # Plot the arrows which are associated with the color bar.
        #
        # - The arrow associated with the current value.
        # - The arrow associated with the minimum value.
        # - The arrow associated with the maximum value.

        self._plot_handle_colormap_arrow = self._plot_handle_colormap.ax.annotate(
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

        self._plot_handle_colormap_arrow_min = self._plot_handle_colormap.ax.annotate(
            "",
            xy=(1.0, current_value_min),  # Arrow tip
            xytext=(1.5, current_value_min),  # Arrow tail
            xycoords=("axes fraction", "data"),
            textcoords=("axes fraction", "data"),
            arrowprops=dict(
                arrowstyle="simple",
                color="red",
                lw=2
            )
        )

        self._plot_handle_colormap_arrow_max = self._plot_handle_colormap.ax.annotate(
            "",
            xy=(1.0, current_value_max),  # Arrow tip
            xytext=(1.5, current_value_max),  # Arrow tail
            xycoords=("axes fraction", "data"),
            textcoords=("axes fraction", "data"),
            arrowprops=dict(
                arrowstyle="simple",
                color="green",
                lw=2
            )
        )

        print(nameMethod + " : Exit")


    # Invoked by : _generate_subplot_1

    def _plot_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        sub_plot = self._plotting_agent._ax1


        print(nameMethod + " : Enter")

        if self._plot_handle_quaternion_pre_multiply is not None :

            raise Exception("Attribute _plot_handle_quaternion_pre_multiply : Trying to set this attribute whilst it is already set.")

        self._plot_handle_quaternion_pre_multiply = self._axis.quiver(

            0, 0, 0,
            self._plotting_agent._quaternion_pre_multiply.x, self._plotting_agent._quaternion_pre_multiply.y,
            self._plotting_agent._quaternion_pre_multiply.z,
            color='blue',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        if GlobalSettings.plot_quaternion_pre_multiply_history :

            # Append the current point onto the end of the plot history.

            hue_value = ((self._plotting_agent._quaternion_pre_multiply.x) * 0.5) + 0.5

            rgb_value = colorsys.hsv_to_rgb(

                hue_value,  # hue (0–1)
                1.0,  # saturation
                1.0  # value
            )

            markersize_value = (hue_value * 4) + 2

            if self._plotting_agent._quaternion_pre_multiply.w < 0 :

                marker_value = 'v'

            else :

                marker_value = '^'

            sub_plot.plot(

                self._plotting_agent._quaternion_pre_multiply.x,
                self._plotting_agent._quaternion_pre_multiply.y,
                self._plotting_agent._quaternion_pre_multiply.z,
                marker=marker_value,
                markersize=markersize_value,
                linestyle='-',
                color=rgb_value
            )

        print(nameMethod + " : Exit")


    # Invoked by : generate_plot

    def _set_legend(self,

        raise_if_set
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if (
            (raise_if_set) and
            (self._plot_handle_title is not None)
        ) :

            raise Exception("Attribute _plot_handle_title : Trying to set this attribute whilst it is already set.")


        if (GlobalSettings.display_legend_subplot_1) :

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

            # ####################################
            # Work out where to put the following.
            # ####################################

            self._legend1 = self._plotting_agent._fig.add_subplot(self._gs[1, 0])
            self._legend1.axis('off')

            # handles1, labels1 = self._ax1.get_legend_handles_labels()

            # Configure the legend itself and set the subplot to use it.

            # self.plot_handle_legend = self._plotting_agent._ax1.legend(
            #
            #     handles=legend_elements,
            #     prop={
            #         "family": "Liberation Mono",
            #         "size": 10
            #     },
            #     loc='lower center',
            #     fontsize=10
            # )

            # self.plot_handle_legend = self._plotting_agent._ax1.legend(

            self.plot_handle_legend = self._legend1.legend(

                handles=legend_elements,
                prop={
                    "family": "Liberation Mono",
                    "size": 10
                },
                loc='lower center',
                fontsize=10
            )

            hue_value = ((self._quaternion_pre_multiply.w) * 0.5) + 0.5

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


    def generate_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # - Set the title which is to be used for this sub-plot.
        # - Set the legend which is to be used for this sub-plot.

        # self._set_title(GlobalSettings.display_legend_subplot_1, GlobalSettings.raise_exception_if_already_set)
        print(nameMethod + " : MARKER 0")
        self._set_legend(True)
        print(nameMethod + " : MARKER 1")

        # - Move the arrow that is associated with the color bar.
        # - Set the color which is to be used for the surface of the sphere.

        self._update_colorbar()

        # Note that the following two methods are defined in the parent class.
        #
        #   - Set the current color for the surface of the unit sphere.
        #   - Plot the unit sphere.

        self._set_rgb_value_for_sphere_surface()
        self._plot_unit_sphere()

        self._plot_quaternion_pre_multiply()
        # self.add_labels_to_plot(axis)

        print(nameMethod + " : Elevation = " + str(self._plotting_agent._elevation_view))

        self._axis.view_init(

            elev=self._plotting_agent._elevation_view,
            azim=self._plotting_agent._azimuth_view
        )

        print(nameMethod + " : Exit")
