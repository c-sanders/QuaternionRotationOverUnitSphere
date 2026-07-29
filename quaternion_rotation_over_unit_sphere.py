# Global settings used by this program.

utility_quaternion_rotation = "/home/craig/local/source_code/haskell/HaskellQuaternionRotation/dist-newstyle/build/x86_64-linux/ghc-9.14.1/quaternion-0.1.0.0/x/quaternion/build/quaternion/quaternion"
verbose_operation           = "False"


rgb_value = colorsys.hsv_to_rgb(1.0, 1.0, 1.0)


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
    print("  rotationAngle : the angle in degrees by which the 3d vector is to be rotated")
    print("                - Haskell type : Double")
    print("                - Measured in degrees")
    print("  vector_x      : the x component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_y      : the y component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("  vector_z      : the z component of the 3d vector that is to be rotated")
    print("                - Haskell type : Double")
    print("")
    print("Example:")
    print("")
    print("  vectorQuaternionRotate False rotation 1 0 0 90 0 0 1")
    print("")
    print("Rotate the 3d vector <0,0,1> by 90 degrees, i.e. pi/2 radians, around the axis which is represented by the")
    print("vector <1,0,0>.")
    print("")
    print("> Notes on the operation of this utility")
    print("  ===========================")
    print("")
    print("If the vector which denotes the axis of rotation, is not a unit vector, then this utility will convert it")
    print("into one first before using it in the calculations.")
    print("")
    print("This utility will not do the same however with the vector that is to be rotated. This is mentioned, because")
    print("if this vector is too long, then it won't be displayed properly in the resulting plot.")


# main
#   |- VectorManipulator::run
#        |- VectorManipulator::set_values_from_command_line_args
#        |- VectorManipulator::generate_plots
#           |- VectorManipulator::perform_quaternion_operations
#           |- VectorManipulator::update_plotting_agent
#           |- VectorManipulator::generate_plot
#                |- PlotAgent::generate_plot

def main() :

    nameMethod = "main"

    vector_manipulator = VectorManipulator()


    print(nameMethod + " : Enter")

    if len(sys.argv) != 10 :

        displayUsage()

        raise ValueError()

    try :

        vector_manipulator.run()


    except Exception as e :

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("The following exception was caught.")
        print("")
        print("  " + str(e))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    print(nameMethod + " : Exit")


if __name__ == "__main__":

    main()