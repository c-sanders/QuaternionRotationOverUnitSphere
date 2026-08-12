import sys
import colorsys


class PlotHandleAgent_SubPlot_1 :


    def __init__(self,

        plotting_agent: PlottingAgent
    ) :

        self._plotting_agent = plotting_agent

        # Set the following attributes;
        #
        #   - title of sub-plot
        #   - RGB color code for surface of unit sphere
        #   - unit sphere
        #   - colormap and its associated arrow
        #   - vector and history of vector points

        self._plot_handle_title_subplot                   = None

        self._rgb_value_sphere                            = None
        self._plot_handle_surface                         = None

        self._plot_handle_colormap                        = None
        self._plot_handle_colormap_arrow                  = None

        self._plot_handle_quaternion_pre_multiply         = None
        self._plot_handle_quaternion_pre_multiply_history = None


    def set_title(self,

        plot_handle_title,
        raise_if_set
    ) :

        if (
            (raise_if_set) and
            (self._plot_handle_title_subplot is not None)
        ) :

            raise Exception("Attribute _plot_handle_title_subplot_1 : Trying to set this attribute whilst it is already set.")

        self.plot_handle_title_subplot_1 = plot_handle_title


    def clear_plot_handle_title_subplot_1(self) :

        if self._plot_handle_title_subplot_1 is not None :

            self._plot_handle_title_subplot_1.remove()
            self._plot_handle_title_subplot_1 = None


    # Invoked by : PlottingAgent::_plot_unit_sphere_quaternion_pre_multiply

    def clear_sphere_surface(self):

        if self._plot_handle_surface is not None :

            self._plot_handle_surface.remove()
            self._plot_handle_surface = None


    def clear_plot_handle_colormap_arrow(self):

        if self._plot_handle_colormap_arrow is not None :

            self._plot_handle_colormap_arrow.remove()
            self._plot_handle_colormap_arrow = None


    def clear_plot_handle_quaternion_pre_multiply(self) :

        if self._plot_handle_quaternion_pre_multiply is not None :

            self._plot_handle_quaternion_pre_multiply.remove()
            self._plot_handle_quaternion_pre_multiply = None


    def clear_artifacts(self):

        self.clear_plot_handle_quaternion_pre_multiply()
        self.clear_sphere_surface()
        self.clear_plot_handle_colormap_arrow()


    def set_rgb_value_for_sphere_surface(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if self._plotting_agent.quaternion_pre_multiply is None :

            hue_value = 0.5

        else :

            hue_value = ((self._plotting_agent.quaternion_pre_multiply.w) * 0.5) + 0.5

        self._rgb_value_sphere = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        print(nameMethod + " : Exit")


    def plot_unit_sphere(self,

            axis
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


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

        self.clear_sphere_surface()

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


    def generate_plot(self,

            axis
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        #

        self._plot_quaternion_pre_multiply()
        # self.add_labels_to_plot(axis)

        print(nameMethod + " : MARKER 0")

        self._set_title_and_legend_subplot_1()

        print(nameMethod + " : MARKER 1")

        # If an arrow currently points to the colorbar, then remove it.
        # Then place a new updated arrow next to the colorbar.

        self.clear_plot_handle_colormap_arrow()

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

        axis.view_init(

            elev=self._plotting_agent.elevation_view,
            azim=self._plotting_agent.azimuth_view
        )

        print(nameMethod + " : Exit")


    # Invoked by : _generate_subplot_1

    def plot_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)

        sub_plot = self._plotting_agent.ax1


        print(nameMethod + " : Enter")

        if self._plot_handle_quaternion_pre_multiply is not None :

            raise Exception("Attribute _plot_handle_quaternion_pre_multiply : Trying to set this attribute whilst it is already set.")

        self._plot_handle_quaternion_pre_multiply = self._plotting_agent.ax1.quiver(

            0, 0, 0,
            self._plotting_agent.quaternion_pre_multiply.x, self._plotting_agent.quaternion_pre_multiply.y,
            self._plotting_agent.quaternion_pre_multiply.z,
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

        print(nameMethod + " : Exit")


    def set_legend(self,

        raise_if_set
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if (
            (raise_if_set) and
            (self.plot_handle_title_subplot_1 is not None)
        ) :

            raise Exception("Attribute _plot_handle_title_subplot_1 : Trying to set this attribute whilst it is already set.")


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