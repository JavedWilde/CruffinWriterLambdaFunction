import Helpers

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

    fontFile = f'Fonts/SVGFONT ({0}).svg' #change numbers for different fonts 0 - 18

    gcode = Helpers.GetGcode(text = 'Happy Birthday Dude dabs', fontFile = fontFile, xOffset = 0, yOffset = 0, max_bed_x = 60, max_bed_y = 20, move_speed = 300, cut_speed = 300, letterLimit = 25, arThres = 8)

    # post processing
    gcode = gcode.replace("M3", "G0 F1000 Z-1")
    gcode = gcode.replace("M5", "G0 F1000 Z1")
    gcode = gcode.replace(" S255", "")

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
