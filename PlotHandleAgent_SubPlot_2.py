import sys
import colorsys

import numpy             as np

import GlobalSettings
import SubPlotAgent


class PlotHandleAgent_SubPlot_2(SubPlotAgent.SubPlotAgent) :


    """This class handles all the artifacts/artists that are required by the plots.

    By placing all the artifacts/artists in this class, it allows the class to maintain
    strict control over the artifacts/artists, i.e. control when and how they are created,
    and under what conditions they are destroyed.

    Attributes:
        owner (str): The account owner's name.
        balance (float): The current account balance.
    """

    def __init__(self,

        plotting_agent: PlottingAgent
    ) :

        super().__init__(plotting_agent)

        self._plotting_agent = plotting_agent

        # Set the following attributes;
        #
        #   - title of sub-plot
        #   - RGB color code for surface of unit sphere
        #   - vectors and history of vector points

        self._axis = self._plotting_agent.ax2

        self._rgb_value_sphere    = None
        self._plot_handle_surface = None

        self._plot_handle_axis_rotation = None
        self._plot_handle_to_rotate     = None

        self.label_quaternion_axis_rotation    = ""
        self.label_quaternion_to_rotate        = ""
        self.label_quaternion_pre_multiply     = ""
        self.label_quaternion_pre_multiply_min = ""
        self.label_quaternion_pre_multiply_max = ""
        self.label_quaternion_rotated          = ""
        self.label_angle_rotation              = ""

        # Vector and history of vector points.

        self._plot_handle_quaternion_rotated         = None
        self._plot_handle_quaternion_rotated_history = None


    def set_plot_handle_title_subplot_2(self,

        plot_handle_title
    ) :

        if self._plot_handle_title_subplot_2 is not None :

            raise Exception("Attribute _plot_handle_title_subplot_2 : Trying to set this attribute whilst it is already set.")

        self.plot_handle_title_subplot_2 = plot_handle_title


    def clear_artifacts(self):

        if self._plot_handle_quaternion_rotated is not None :

            self._plot_handle_quaternion_rotated.remove()
            self._plot_handle_quaternion_rotated = None


    def _set_rgb_value_for_sphere_surface(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        hue_value = 0.5

        self._rgb_value_sphere = colorsys.hsv_to_rgb(

            hue_value,  # hue (0–1)
            1.0,  # saturation
            1.0  # value
        )

        print(nameMethod + " : Exit")


    def generate_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # self.add_labels_to_plot(axis)
        self._set_title()
        self._set_legend()
        self._plot_quaternions()

        self._axis.view_init(

            elev=self._plotting_agent._elevation_view,
            azim=self._plotting_agent._azimuth_view
        )

        print(nameMethod + " : Exit")


    def configure(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        self._plot_unit_sphere_quaternion_rotation()
        self._plot_axes()

        print(nameMethod + " : About to invoke : self.set_aspect_ratios_and_extents")
        self._set_aspect_ratios_and_extents()

        self._fill_panes()
        self._configure_grid()
        # self.create_static_labels()

        print(nameMethod + " : Exit")


    def _set_title(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        print(nameMethod + " : Exit")


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


    def _set_legend(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        print(nameMethod + " : Exit")


    def plot_quaternion_pre_multiply(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # If w = 0, plot this quaternion in the pure imaginary space as well and keep this plot
        # there. That is, do not remove it from the plot.

        if abs(self.plotting_agent.quaternion_pre_multiply.w) < 0.001 :

            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : Plotting vector in the pure imaginary space")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(nameMethod + " : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # We do not need a handle to this artifact, as we are never going to remove it.

            self._axis.quiver(

                0, 0, 0,
                self.plotting_agent.quaternion_pre_multiply.x, self.plotting_agent.quaternion_pre_multiply.y, self.plotting_agent.quaternion_pre_multiply.z,
                color='blue',
                linewidth=1,
                arrow_length_ratio=0.1
            )

        print(nameMethod + " : Exit")


    def _plot_quaternions(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # Plot an arrow from the origin which represents : the axis of rotation

        self.plot_handle_quaternion_axis_rotation = self._axis.quiver(

            0, 0, 0,
            self._plotting_agent._quaternion_axis_rotation.x, self._plotting_agent._quaternion_axis_rotation.y, self._plotting_agent._quaternion_axis_rotation.z,
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion which is to be rotated.

        self.plot_handle_quaternion_to_rotate = self._axis.quiver(

            0, 0, 0,
            self._plotting_agent._quaternion_to_rotate.x, self._plotting_agent._quaternion_to_rotate.y, self._plotting_agent._quaternion_to_rotate.z,
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion after it has been rotated.

        self.plot_handle_quaternion_rotated = self._axis.quiver(

            0, 0, 0,
            self._plotting_agent._quaternion_rotated.x, self._plotting_agent._quaternion_rotated.y, self._plotting_agent._quaternion_rotated.z,
            color='magenta',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        if GlobalSettings.plot_quaternion_rotated_history :

            self._axis.plot(

                self._plotting_agent._quaternion_rotated.x,
                self._plotting_agent._quaternion_rotated.y,
                self._plotting_agent._quaternion_rotated.z,
                marker='.',
                linestyle='-',
                color='magenta'
            )

        print(nameMethod + " : Exit")


    def _plot_unit_sphere_quaternion_rotation(self) :

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

        self._axis.plot_surface(
            x, y, z,
            color=rgb_value,
            alpha=0.2,
            linewidth=0
        )

        self._axis.plot_wireframe(
            x, y, z,
            color='black',
            linewidth=0.4,
            rstride=4,
            cstride=4
        )

        print(nameMethod + " : Exit")