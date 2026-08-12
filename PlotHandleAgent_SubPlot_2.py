import sys
import colorsys


class PlotHandleAgent_SubPlot_2:


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
                 ):

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


    def generate_plot(self) :

        nameMethod = str(self.__class__.__name__) + "::" + str(sys._getframe().f_code.co_name)


        print(nameMethod + " : Enter")

        # self.add_labels_to_plot(axis)
        self._set_title()
        self._set_legend()
        self._plot_quaternions()

        self._axis.view_init(

            elev=self.elevation_view,
            azim=self.azimuth_view
        )

        print(nameMethod + " : Exit")


    def _set_title(self) :

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


        # Plot an arrow from the origin which represents : the axis of rotation

        self.plot_handle_quaternion_axis_rotation = self._axis.quiver(

            0, 0, 0,
            self.quaternion_axis_rotation.x, self.quaternion_axis_rotation.y, self.quaternion_axis_rotation.z,
            color='red',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion which is to be rotated.

        self.plot_handle_quaternion_to_rotate = self._axis.quiver(

            0, 0, 0,
            self.quaternion_to_rotate.x, self.quaternion_to_rotate.y, self.quaternion_to_rotate.z,
            color='green',
            linewidth=1,
            arrow_length_ratio=0.1
        )

        # Plot an arrow from the origin which represents : the vector/quaternion after it has been rotated.

        self.plot_handle_quaternion_rotated = self._axis.quiver(

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

            self._axis.plot(

                self.quaternion_rotated.x,
                self.quaternion_rotated.y,
                self.quaternion_rotated.z,
                marker='.',
                linestyle='-',
                color='magenta'
            )