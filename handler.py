import cairo

def handler(event, context):

    if ("queryStringParameters" not in event):
        event["queryStringParameters"] = {}

    # SVG Settings
    text = (
        event["queryStringParameters"]["text"]
        if "text" in event["queryStringParameters"]
        else "Hello World"
    )

    svg_width = (
        int(event["queryStringParameters"]["svg_width"])
        if "svg_width" in event["queryStringParameters"]
        else 80
    )

    svg_height = (
        int(event["queryStringParameters"]["svg_height"])
        if "svg_height" in event["queryStringParameters"]
        else 80
    )

    font_size = (
        int(event["queryStringParameters"]["font_size"])
        if "font_size" in event["queryStringParameters"]
        else 15
    )

    line_width = (
        int(event["queryStringParameters"]["line_width"])
        if "line_width" in event["queryStringParameters"]
        else 2
    )

    text_position_x = (
        int(event["queryStringParameters"]["text_position_x"])
        if "text_position_x" in event["queryStringParameters"]
        else 0
    )

    text_position_y = (
        int(event["queryStringParameters"]["text_position_y"])
        if "text_position_y" in event["queryStringParameters"]
        else 12
    )

    rgb_r = (
        int(event["queryStringParameters"]["rgb_r"])
        if "rgb_r" in event["queryStringParameters"]
        else 1
    )

    rgb_g = (
        int(event["queryStringParameters"]["rgb_g"])
        if "rgb_g" in event["queryStringParameters"]
        else 0
    )

    rgb_b = (
        int(event["queryStringParameters"]["rgb_b"])
        if "rgb_b" in event["queryStringParameters"]
        else 0
    )

    font_face = (
        event["queryStringParameters"]["font_face"]
        if "font_face" in event["queryStringParameters"]
        else "Arial"
    )

    # Gcode settings
    movement_speed = (
        int(event["queryStringParameters"]["movement_speed"])
        if "movement_speed" in event["queryStringParameters"]
        else 300
    )
    cutting_speed = (
        int(event["queryStringParameters"]["cutting_speed"])
        if "cutting_speed" in event["queryStringParameters"]
        else 300
    )
    pass_depth = (
        int(event["queryStringParameters"]["pass_depth"])
        if "pass_depth" in event["queryStringParameters"]
        else 0
    )
    passes = (
        int(event["queryStringParameters"]["passes"])
        if "passes" in event["queryStringParameters"]
        else 1
    )

    surface = cairo.SVGSurface("test.svg", svg_width * 2.83465, 13)

    # with cairo.SVGSurface("test.svg", 700, 700) as surface:

    # creating a cairo context object for SVG surface
    # using Context method
    Context = cairo.Context(surface)

    # setting color of the context
    Context.set_source_rgb(rgb_r, rgb_g, rgb_b)

    # approximate text height
    Context.set_font_size(font_size)

    # Font Style
    Context.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    # position for the text
    Context.move_to(text_position_x, text_position_y)

    # displays the text
    Context.text_path(text)

    # Width of outline
    Context.set_line_width(line_width)

    # stroke out the color and width property
    Context.stroke()

    Context.save()

    surface.finish()
    # saving the file
    surface.flush()

    # printing message when file is saved

    # print(svg)

    from svg_to_gcode.svg_parser import parse_file
    from svg_to_gcode.compiler import Compiler, interfaces

    # Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
    # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
    gcode_compiler = Compiler(
        interfaces.Gcode,
        movement_speed=movement_speed,
        cutting_speed=cutting_speed,
        pass_depth=pass_depth,
    )

    curves = parse_file("test.svg")  # Parse an svg file into geometric curves

    gcode_compiler.append_curves(curves)
    gcode = gcode_compiler.compile(passes=passes)

    gcode = gcode.replace("M3", "G0 F1000 Z-1")
    gcode = gcode.replace("M5", "G0 F1000 Z1")
    gcode = gcode.replace(" S255", "")

    # gcode_compiler.compile_to_file("drawing.gcode", passes=1)
    # save the gcode to a file
    with open("drawing.gcode", "w") as f:
        f.write(gcode)
    return {
        "statusCode": 200,
        "body": gcode,
        "headers": {
            "Content-Type": "text/plain",
            "Content-Disposition": 'attachment; filename="' + text + '.gcode"',
        },
    }


print(handler({"queryStringParameters": {}}, None))
