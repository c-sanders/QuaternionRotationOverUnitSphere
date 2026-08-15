import sys
import colorsys

import numpy as np

from   matplotlib.ticker import MultipleLocator


class SubPlotAgent :

    def __init__(self,

        plotting_agent: PlottingAgent
    ) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._plotting_agent = plotting_agent

        # Declare the following attributes;
        #
        #   - axis which this sub-plot belongs to
        #   - title of sub-plot
        #   - RGB color code for the surface of unit sphere
        #   - unit sphere

        self._axis                                        = None

        self._plot_handle_title_subplot                   = None

        self._rgb_value_sphere                            = None
        self._plot_handle_surface                         = None

        self._v                                           = np.array([1.2, 0.8, 0.5])
        self._x                                           = None
        self._y                                           = None
        self._z                                           = None

        self._plot_handle_sphere_wire_frame               = None
        self._plot_handle_sphere_surface                  = None

        print(nameMethod + " : Exit")


    # Invoked by : configure

    def _plot_axes(self) :

        # Plot;
        #
        #   x axis
        #   y axis
        #   z axis

        self._axis.quiver(
            -1.2, 0, 0,
            2.4, 0, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        self._axis.quiver(
            0, -1.2, 0,
            0, 2.4, 0,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )

        self._axis.quiver(
            0, 0, -1.2,
            0, 0, 2.4,
            color='black',
            linewidth=1,
            arrow_length_ratio=0.025
        )


    def _fill_panes(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._axis.xaxis.pane.fill = False
        self._axis.yaxis.pane.fill = False
        self._axis.zaxis.pane.fill = False

        print(nameMethod + " : Exit")


    def _configure_grid(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # ax.grid(False)

        self._axis.xaxis.set_major_locator(MultipleLocator(1))
        self._axis.yaxis.set_major_locator(MultipleLocator(1))
        self._axis.zaxis.set_major_locator(MultipleLocator(1))

        print(nameMethod + " : Exit")


    def _set_rgb_value_for_sphere_surface(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        if self._plotting_agent._quaternion_pre_multiply is None :

            hue_value = 0.5

        else :

            hue_value = ((self._plotting_agent._quaternion_pre_multiply.w) * 0.5) + 0.5

        self._rgb_value_sphere = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        print(nameMethod + " : Exit")


    # Invoked by : configure
    #            : generate_plot

    def _plot_unit_sphere(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Only generate the sphere components if needed.

        if (
            (self._x is None) or
            (self._y is None) or
            (self._z is None)
        ) :

            # Generate the necessary components for the unit sphere.

            self._generate_sphere_components()

        # Plot the following components of the unit sphere;
        #
        #   - surface
        #   - wire frame

        self._plot_sphere_surface()
        self._plot_sphere_wire_frame()

        print(nameMethod + " : Exit")


    def _generate_sphere_components(self) :

        # Generate the components for the unit sphere.

        u = np.linspace(0, 2 * np.pi, 100)
        v_sphere = np.linspace(0, np.pi, 100)

        self._x = np.outer(np.cos(u), np.sin(v_sphere))
        self._y = np.outer(np.sin(u), np.sin(v_sphere))
        self._z = np.outer(np.ones_like(u), np.cos(v_sphere))


    def _plot_sphere_surface(self) :

        self._plot_handle_surface = self._axis.plot_surface(

                                                     self._x, self._y, self._z,
                                                     color=self._rgb_value_sphere,
                                                     alpha=0.2,
                                                     linewidth=0
                                                    )


    def _plot_sphere_wire_frame(self) :

        # Plot the wireframe of the unit sphere.

        self._axis.plot_wireframe(

            self._x, self._y, self._z,
            color='black',
            linewidth=0.4,
            rstride=4,
            cstride=4
        )