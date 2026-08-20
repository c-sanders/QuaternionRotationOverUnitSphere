import sys


def format_component(

        name,
        space,
        value
) :
    nameMethod = "::" + str(sys._getframe().f_code.co_name)


    print(nameMethod + " : Enter")

    print(nameMethod + " : name  = " + str(name))
    print(nameMethod + " : space = " + str(space))
    print(nameMethod + " : value = " + str(value))

    if value == 0 :

        print(nameMethod + " : MARKER 0")

        if space :

            return f" {name}{abs(value):.3f}"

        else :

            print(nameMethod + " : MARKER 0A")

            return_value = f"+{name}{abs(value):.3f}"

            print(nameMethod + " : return_value = " + str(return_value))

            return return_value

    elif value < 0 :

        if space :

            return f"- {name}{abs(value):.3f}"

        else :

            return f"-{name}{abs(value):.3f}"

        print(nameMethod + " : MARKER 1")

    else :

        if space :

            return f"+ {name}{value:.3f}"

        else :

            return f"+{name}{value:.3f}"

        print(nameMethod + " : MARKER 2")

    print(nameMethod + " : Exit")


def generate_string(

        scalar_value,
        i_value,
        j_value,
        k_value
) :

    label = format_component("", False, scalar_value) + " "
    label += f"{format_component('i', True, i_value)} "
    label += f"{format_component('j', True, j_value)} "
    label += f"{format_component('k', True, k_value)}"

    return label