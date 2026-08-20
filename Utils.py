def format_component(

        name,
        space,
        value
) :

    if value == 0 :

        if space :

            return f" {name}{abs(value):.3f}"

        else :

            return f"+{name}{abs(value):.3f}"

    elif value < 0 :

        if space :

            return f"- {name}{abs(value):.3f}"

        else :

            return f"-{name}{abs(value):.3f}"

    else :

        if space :

            return f"+ {name}{value:.3f}"

        else :

            return f"+{name}{value:.3f}"


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