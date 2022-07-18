# This program reads a xlsx file containing boreholes logs and generate a drawing of these drawings in a dxf file

# Import libraries
import pandas as pd
import numpy as np
import ezdxf

from tkinter import Tk, filedialog

# Select the xls file containing the borehole log data
def get_file_path():
    Tk().withdraw()
    import_file_path = filedialog.askopenfilename()

    return import_file_path


# Read the file that will be used to draw the borehole log's and create de "df" data frame with it
def read_file(path):
    data = pd.read_excel(path)
    df = pd.DataFrame(data)

    return df


# Calculate the x coordinates of the 4 vertex of the squares that will be drawn and store into borehole_data
def vertex_calculator():
    borehole_data["x_1"] = borehole_data.multiplier * distance
    borehole_data["x_2"] = borehole_data.multiplier * distance + thickness

    return borehole_data


# Calculate the multiplier for each line of borehole_data
def multiplier():
    # Vector to carry the multiplier
    multiplier_vector = []

    # Iterate over all the lines of the data frame
    for borehole in borehole_data.borehole_name:
        # Get's the place of the borehole we are working with to use as a multiplier to separate the different boreholes
        multiplier = np.where(boreholes == borehole)[0][0]
        # Append the multiplier to it's vector
        multiplier_vector.append(multiplier)

    # Create "multiplier" column in the data frame borehole_data
    borehole_data["multiplier"] = multiplier_vector

    return borehole_data


# Create the log of the boreholes using associative Polyline and Hatch
def draw_log():
    # Iterable for changing layer color
    i = 1
    # Create a layer for each material
    for material in materials:
        # Create the layer for the material
        layer = doc.layers.add(material)
        # Set layer color
        layer.color = i
        # Increment
        i += 1

    # Draw the hatch's
    for key in borehole_data.index:
        # Get the y1 coordinate of the material
        y_1 = borehole_data.loc[borehole_data.index == key, 'initial_depth'].item()
        # Get the y2 coordinate of the material
        y_2 = borehole_data.loc[borehole_data.index == key, 'final_depth'].item()
        # Get the x1 coordinate of the material
        x_1 = borehole_data.loc[borehole_data.index == key, 'x_1'].item()
        # Get the x2 coordinate of the material
        x_2 = borehole_data.loc[borehole_data.index == key, 'x_2'].item()
        # Get the x2 coordinate of the material
        x_2 = borehole_data.loc[borehole_data.index == key, 'x_2'].item()

        # Get the material name to set the layer
        material = borehole_data.loc[borehole_data.index == key, 'material'].item()

        # Create hatch entity first, so it will be showed back of the lines // Color 256 = By Layer
        hatch = msp.add_hatch(color=256, dxfattribs={'layer': material})

        # Draw the square using polyline in the given layer
        points = [(x_1, -y_1), (x_2, -y_1), (x_2, -y_2), (x_1, -y_2)]
        # Create the Polyline to further association
        lwpolyline = msp.add_lwpolyline(points, format="xyb", close=True,  dxfattribs={'layer': 0})

        # Polyline path for hatch create the draw
        path = hatch.paths.add_polyline_path(
            # get path vertices from associated LWPOLYLINE entity
            lwpolyline.get_points(format="xyb"),
            # get closed state also from associated LWPOLYLINE entity
            is_closed=lwpolyline.closed,
        )
        # Set association between boundary path and LWPOLYLINE
        hatch.associate(path, [lwpolyline])


# Create the information box of the boreholes
def draw_box():
    # Create the layer for the information box
    layer = doc.layers.add("information")
    # Set layer color
    layer.color = 0

    # Draw the squares
    for borehole in boreholes:
        # Get the borehole multiplier
        multiplier = np.where(boreholes == borehole)[0][0]
        # Calculate the initial y1 coordinate of the borehole
        y_1 = 0
        # Calculate the x1 coordinate of the material
        x_1 = multiplier * distance + thickness / 2

        # Define the 6 polyline points of the information box
        p1 = (x_1, y_1)
        p2 = (x_1, y_1+2)
        p3 = (x_1 - width/2, y_1+2)
        p4 = (x_1 - width/2, y_1+2+height)
        p5 = (x_1 + width/2, y_1+2+height)
        p6 = (x_1 + width/2, y_1+2)
        p7 = p2
        center = (x_1, y_1 + 2 + height/2)

        # Draw the box using polyline in the given layer
        points = [p1, p2, p3, p4, p5, p6, p7]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'information'})

        # Write the name of the borehole
        msp.add_text(borehole,
                     dxfattribs={
                         'height': 0.3 * height,
                         'layer': 'information'}
                     ).set_pos(center, align='MIDDLE')


# Create the information box of the boreholes
def draw_legend():
    # Draw legend
    for material in materials:
        # Get the material multiplier (len used to invert the first element with the last, so it can be showed first)
        multiplier = len(materials) - 1 - np.where(materials == material)[0][0]
        # Calculate the initial y1 coordinate of the borehole multiplier (square height + distance between squares)
        y_1 = 10 + multiplier * (1 + .5)
        # Calculate the x1 coordinate of the material
        x_1 = 0

        # Define the 6 polyline points of the information box
        p1 = (x_1, y_1)
        p2 = (x_1, y_1 + 1)
        p3 = (x_1 + 1.5, y_1 + 1)
        p4 = (x_1 + 1.5, y_1)
        p5 = (x_1 + 1.5 + 1, y_1 + 1)

        # Create hatch entity first, so it will be showed back of the lines // Color 256 = By Layer
        hatch = msp.add_hatch(color=256, dxfattribs={'layer': material})

        # Draw the squares using polyline in the given layer
        points = [p1, p2, p3, p4, p1]
        # Create the Polyline to further association
        lwpolyline = msp.add_lwpolyline(points, format="xyb", close=True,  dxfattribs={'layer': 0})

        # Polyline path for hatch create the draw
        path = hatch.paths.add_polyline_path(
            # get path vertices from associated LWPOLYLINE entity
            lwpolyline.get_points(format="xyb"),
            # get closed state also from associated LWPOLYLINE entity
            is_closed=lwpolyline.closed,
        )
        # Set association between boundary path and LWPOLYLINE
        hatch.associate(path, [lwpolyline])

        # Write the name of the material
        msp.add_text(material,
                     dxfattribs={
                         'height': 1}
                     ).set_pos(p5, align='TOP_LEFT')


# Get's the file path
file_path = get_file_path()

# Create dataframe
borehole_data = read_file(file_path)

# Get the name of all materials in the file
materials = borehole_data.material.unique()

# Get the name of all boreholes in the file
boreholes = borehole_data.borehole_name.unique()

# Set the distance between log's and their thickness
distance = 10
thickness = 1

# Set information box measurements
height = 2
width = 8

# Calculate multiplier
borehole_data = multiplier()

# Calculate x coordinates of each line
borehole_data = vertex_calculator()

# Create a new DXF drawing
doc = ezdxf.new()

# Add new entities to the modelspace:
msp = doc.modelspace()

# Draw the associative hatch's and squares of the log's
draw_log()

# Draw the information box
draw_box()

# Draw the associative legend hatch and squares of the log's
draw_legend()

# Save the dxf file
doc.saveas("borehole_logs.dxf")
