import colorsys


# Global settings used by this program.

utility_quaternion_rotation = "/home/craig/local/source_code/haskell/HaskellQuaternionRotation/dist-newstyle/build/x86_64-linux/ghc-9.14.1/quaternion-0.1.0.0/x/quaternion/build/quaternion/quaternion"
verbose_operation           = "False"

rgb_value = colorsys.hsv_to_rgb(1.0, 1.0, 1.0)

plot_quaternion_pre_multiply_history = True
plot_quaternion_rotated_history      = True

title_plot       = "Progression of various quaternions as angle of rotation increases."
title_sub_plot_1 = r"$qv$ in $S^{3}$ with $w=0$"
title_sub_plot_2 = r"qvq'"

display_legend           = True
display_legend_subplot_1 = False
display_legend_subplot_2 = False

raise_exception_if_already_set = True

title_colormap = "Value of w for the 4d hyperspheres"

image_dimensions    = (8, 10)
image_dpi           = 300
image_bbox_argument = None