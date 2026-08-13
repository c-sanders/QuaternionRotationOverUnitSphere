import sys

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
