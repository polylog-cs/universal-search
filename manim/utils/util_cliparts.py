def clipart_arrow():
    return ImageMobject("img/arrow.png").scale_to_fit_height(0.7)

def clipart_yes_no_maybe(which, height):
    pnts_yes = [
        np.array([174.042, 364.002, 0]),
        np.array([169.653, 359.498, 0]),
        np.array([181.318, 347.66, 0]),
        np.array([200.663, 367.236, 0]),
        np.array([195.928, 371.625, 0]),
        np.array([181.376, 356.553, 0])
    ]
    pnts_no = [
        np.array([397.791, 350.711, 0]),
        np.array([402.185, 346.322, 0]),
        np.array([410.393, 354.779, 0]),
        np.array([417.863, 347.317, 0]),
        np.array([421.913, 351.489, 0]),
        np.array([414.443, 358.95, 0]),
        np.array([421.999, 366.735, 0]),
        np.array([417.606, 371.123, 0]),
        np.array([410.049, 363.339, 0]),
        np.array([401.857, 371.522, 0]),
        np.array([397.807, 367.35, 0]),
        np.array([406.359, 359.167, 0])
    ]
    pnts_maybe = [
        #np.array([300.242, 355.568, 0]),
        np.array([300.329, 356.423, 0]),
        np.array([300.478, 357.373, 0]),
        np.array([300.915, 358.039, 0]),
        np.array([301.621, 358.773, 0]),
        np.array([302.28, 359.361, 0]),
        np.array([302.983, 359.868, 0]),
        np.array([303.927, 360.481, 0]),
        np.array([304.549, 360.903, 0]),
        np.array([305.347, 361.538, 0]),
        np.array([305.847, 362.036, 0]),
        np.array([306.411, 362.764, 0]),
        np.array([306.822, 363.514, 0]),
        np.array([307.069, 364.183, 0]),
        np.array([307.247, 364.906, 0]),
        np.array([307.382, 365.766, 0]),
        np.array([307.454, 366.456, 0]),
        np.array([307.5, 367.296, 0]),
        np.array([307.483, 368.449, 0]),
        np.array([307.368, 369.476, 0]),
        np.array([307.122, 370.533, 0]),
        np.array([306.738, 371.538, 0]),
        np.array([306.243, 372.415, 0]),
        np.array([305.63, 373.196, 0]),
        np.array([305.216, 373.623, 0]),
        np.array([304.639, 374.132, 0]),
        np.array([304.202, 374.464, 0]),
        np.array([303.471, 374.93, 0]),
        np.array([302.656, 375.315, 0]),
        np.array([301.972, 375.546, 0]),
        np.array([301.166, 375.736, 0]),
        np.array([300.224, 375.859, 0]),
        np.array([298.285, 375.953, 0]),
        np.array([296.657, 375.957, 0]),
        np.array([294.859, 375.787, 0]),
        np.array([294.403, 375.672, 0]),
        np.array([293.672, 375.397, 0]),
        np.array([292.749, 374.913, 0]),
        np.array([291.972, 374.442, 0]),
        np.array([290.817, 373.659, 0]),
        np.array([289.949, 372.98, 0]),
        np.array([289.316, 372.386, 0]),
        np.array([288.951, 371.975, 0]),
        np.array([288.621, 371.532, 0]),
        np.array([288.237, 370.902, 0]),
        np.array([287.855, 370.102, 0]),
        np.array([287.6, 369.378, 0]),
        np.array([287.436, 368.697, 0]),
        np.array([287.307, 367.822, 0]),
        np.array([287.235, 366.977, 0]),
        np.array([287.282, 366.009, 0]),
        np.array([292.414, 366.022, 0]),
        np.array([293.403, 366.042, 0]),
        np.array([294.352, 366.039, 0]),
        np.array([294.433, 366.942, 0]),
        np.array([294.533, 367.926, 0]),
        np.array([294.593, 368.426, 0]),
        np.array([294.835, 368.99, 0]),
        np.array([295.18, 369.352, 0]),
        np.array([295.838, 369.706, 0]),
        np.array([296.789, 369.93, 0]),
        np.array([297.278, 369.977, 0]),
        np.array([298.182, 369.937, 0]),
        np.array([298.87, 369.745, 0]),
        np.array([299.466, 369.41, 0]),
        np.array([299.913, 369.01, 0]),
        np.array([300.142, 368.711, 0]),
        np.array([300.326, 368.337, 0]),
        np.array([300.399, 368.005, 0]),
        np.array([300.392, 367.466, 0]),
        np.array([300.315, 366.959, 0]),
        np.array([300.217, 366.476, 0]),
        np.array([300.052, 365.885, 0]),
        np.array([299.736, 365.153, 0]),
        np.array([299.328, 364.545, 0]),
        np.array([298.823, 363.99, 0]),
        np.array([298.173, 363.384, 0]),
        np.array([297.472, 362.763, 0]),
        np.array([296.921, 362.255, 0]),
        np.array([296.5, 361.84, 0]),
        np.array([295.955, 361.235, 0]),
        np.array([295.516, 360.609, 0]),
        np.array([295.169, 359.915, 0]),
        np.array([294.877, 358.949, 0]),
        np.array([294.851, 358.451, 0]),
        np.array([294.803, 357.471, 0]),
        np.array([294.769, 356.475, 0]),
        np.array([294.771, 355.811, 0]),
        np.array([300.261, 355.911, 0]),
    ]

    color = ""
    
    if which == "yes":
        color = GREEN
        clipart = Polygon(
            *pnts_yes,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2
        )

    if which == "no":
        color = RED
        clipart = Polygon(
            *pnts_no,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2
        )
    
    if which == "maybe":
        color = ORANGE
        clipart = Polygon(
            *pnts_maybe,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2.5
        )
        small_circle = Circle(
            radius = height/12.5,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).next_to(clipart, DOWN, buff = height/20)
        Group(clipart, small_circle).move_to(ORIGIN)
    

    circle = Circle(
        radius = height/2,
        color = color,
        fill_color = color,
        fill_opacity = 1,
    ).move_to(ORIGIN)

    if which != "maybe":
        return Group(circle, clipart)
    else:
        return Group(circle, clipart, small_circle)

def clipart_house(color = RED, height = 1, z_index = 100):
    pnts = [
        np.array([232.535, 333.808, 0.0]),
        np.array([277.698, 333.811, 0.0]),
        np.array([277.387, 373.503, 0.0]),
        np.array([318.11, 373.566, 0.0]),
        np.array([318.057, 333.881, 0.0]),
        np.array([363.215, 333.935, 0.0]),
        np.array([362.703, 419.758, 0.0]),
        np.array([368.717, 425.367, 0.0]),
        np.array([379.969, 415.454, 0.0]),
        np.array([390.258, 426.885, 0.0]),
        np.array([297.362, 509.816, 0.0]),
        np.array([256.582, 472.796, 0.0]),
        np.array([256.626, 497.065, 0.0]),
        np.array([232.588, 497.017, 0.0]),
        np.array([232.899, 451.371, 0.0]),
        np.array([204.978, 426.922, 0.0]),
        np.array([215.11, 415.777, 0.0]),
        np.array([225.569, 425.578, 0.0]),
        np.array([232.235, 419.834, 0.0]),
        np.array([232.549, 333.833, 0.0]),
    ]

    house = Polygon(
        *pnts,
        color = color,
        fill_color = color,
		fill_opacity = 1,
        z_index = z_index
    ).move_to(
        0*DOWN
    ).scale_to_fit_height(
        height
    )

    return house   

def clipart_icon(color = BLUE, height = 1, z_index = 100):
    pnts = [
        np.array([407.837, 313.233, 0.0]),
        np.array([340.843, 431.234, 0.0]),
        np.array([297.995, 558.503, 0.0]),
        np.array([253.986, 431.689, 0.0]),
        np.array([187.414, 311.624, 0.0]),
    ]

    icon = ArcPolygon(
        *pnts,
        color = color,
        arc_config = [
            { 'radius': 119.256, 'color': color},
            { 'radius': 70.9444, 'color': color},
            { 'radius': 70.9444, 'color': color},
            { 'radius': 119.256, 'color': color},
            { 'radius': 216.488, 'color': color},

        ],
        fill_color = color,
		fill_opacity = 1,
        z_index = z_index
    ).move_to(
        0*DOWN
    ).scale_to_fit_height(
        height
    )

    return icon
