from svgpathtools import Path, wsvg, parse_path
import xml.etree.ElementTree as ET
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import math

def GetGlyphDictionary(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    glyphs = root.findall(".//*[@unicode]")
    dict = {}
    for glyph in glyphs[::-1]:
        try:
            d = glyph.attrib['d']
        except:
            continue
        
        try:
            horiz_adv_x = glyph.attrib['horiz-adv-x']
        except:
            horiz_adv_x = str(0)
        dict[glyph.attrib['unicode']] = [d,horiz_adv_x]
    return dict

def GenerateGcode(move_speed, cut_speed):
    gcode_compiler = Compiler(
        interfaces.Gcode,
        movement_speed=move_speed,
        cutting_speed=cut_speed,
        pass_depth=0,
    )

    curves = parse_file("svg.svg")  # Parse an svg file into geometric curves

    gcode_compiler.append_curves(curves)
    gcode = gcode_compiler.compile(passes=1)

    # gcode_compiler.compile_to_file("drawing.gcode", passes=1)
    # save the gcode to a file
    return gcode

def SaveSvg(paths):
    xmin, xmax, ymin, ymax = Path(*[seg for pa in paths for seg in pa]).bbox()
    dx = xmax - xmin
    dy = ymax - ymin
    viewbox = f'{xmin} {ymin} {dx} {dy}'
    print(viewbox)
    attr = {
        'width': '50%',
        'height': '50%',
        'viewBox': viewbox,
        'preserveAspectRatio': 'xMinYMin meet'
    }
    wsvg(paths=paths,
            svg_attributes=attr, filename='svg.svg')
    
    
def CheckAr(paths):
    xmin, xmax, ymin, ymax = Path(*[seg for pa in paths for seg in pa]).bbox()
    return (xmax - xmin)/(ymax - ymin)

def GcodeScale(gcode, xScale,yScale):
    lines = gcode.split(";\n")
    modified_lines = []
    for line in lines:
        if line.startswith(('G0', 'G1')):  # Look for lines starting with G0 or G1
            x = None
            y = None

            # Extract X and Y values from the line
            for command in line.split():
                if command.startswith('X'):
                    x = float(command[1:])
                elif command.startswith('Y'):
                    y = float(command[1:])

            if x is not None and y is not None:
                # Replace the old X and Y values with the modified values
                line = line.replace(f'X{x}', f'X{x*xScale}').replace(f'Y{y}', f'Y{y*yScale}')

        modified_lines.append(line)

    modified_gcode = ";\n".join(modified_lines)
    return modified_gcode

def GcodeMove(gcode, xMove,yMove):
    lines = gcode.split(";\n")
    modified_lines = []
    for line in lines:
        if line.startswith(('G0', 'G1')):  # Look for lines starting with G0 or G1
            x = None
            y = None

            # Extract X and Y values from the line
            for command in line.split():
                if command.startswith('X'):
                    x = float(command[1:])
                elif command.startswith('Y'):
                    y = float(command[1:])

            if x is not None and y is not None:
                # Replace the old X and Y values with the modified values
                line = line.replace(f'X{x}', f'X{x+xMove}').replace(f'Y{y}', f'Y{y+yMove}')

        modified_lines.append(line)

    modified_gcode = ";\n".join(modified_lines)
    return modified_gcode

def GcodeBBox(gcode):
    lines = gcode.split(";\n")

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for line in lines:
        if line.startswith(('G0', 'G1')):
            for command in line.split():
                if command.startswith('X'):
                    x = float(command[1:])
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                elif command.startswith('Y'):
                    y = float(command[1:])
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

    return [min_x, max_x, min_y, max_y]

def GetSingleLine(text, fontDict):
    paths = []
    pointer = 0
    for char in text:
        if char == ' ':
            pointer += 400
            continue

        d = parse_path(fontDict[char][0]).translated(complex(pointer,0))
        pointer = d.bbox()[1]
        paths.append(d)
    return paths

def GetMultiLine(text, fontDict):
    words = text.split(' ')
    word_splice_index = math.ceil(len(words)/2)
    split_index = len(" ".join(words[:word_splice_index]))

    #calculating values for positioning alignment, couldnt get a reference cuz it was acting weird
    pointer = [0,0]
    line1_extremes = [0,0]
    line2_extremes = [0,0]
    for char in text[split_index+1:]:
        if char == ' ':
            pointer[0] += 400
            continue

        d = parse_path(fontDict[char][0]).translated(complex(pointer[0],pointer[1]))
        pointer[0] = d.bbox()[1]
        if(d.bbox()[1]>line2_extremes[0]): line2_extremes[0] = d.bbox()[1]
        if(d.bbox()[3]>line2_extremes[1]): line2_extremes[1] = d.bbox()[3]

    pointer = [0, line2_extremes[1] + 200]

    for char in text[:split_index]:
        if char == ' ':
            pointer[0] += 400
            continue

        d = parse_path(fontDict[char][0]).translated(complex(pointer[0],pointer[1]))
        pointer[0] = d.bbox()[1]
        if(d.bbox()[1]>line1_extremes[0]): line1_extremes[0] = d.bbox()[1]
        if(d.bbox()[3]>line1_extremes[1]): line1_extremes[1] = d.bbox()[3]

    #actually moving and adding letters to path list for rendering
    paths = []
    pointer = [(line1_extremes[0]/2) - (line2_extremes[0]/2),0]
    for char in text[split_index+1:]:
        if char == ' ':
            pointer[0] += 400
            continue

        d = parse_path(fontDict[char][0]).translated(complex(pointer[0],pointer[1]))
        pointer[0] = d.bbox()[1]
        if(d.bbox()[1]>line2_extremes[0]): line2_extremes[0] = d.bbox()[1]
        if(d.bbox()[3]>line2_extremes[1]): line2_extremes[1] = d.bbox()[3]
        paths.append(d)
    
    pointer = [0,line2_extremes[1] + 400]

    for char in text[:split_index]:
        if char == ' ':
            pointer[0] += 400
            continue
        d = parse_path(fontDict[char][0]).translated(complex(pointer[0],pointer[1]))
        pointer[0] = d.bbox()[1]
        if(d.bbox()[1]>line1_extremes[0]): line1_extremes[0] = d.bbox()[1]
        if(d.bbox()[3]>line1_extremes[1]): line1_extremes[1] = d.bbox()[3]
        paths.append(d)

    return paths


def GetGcode(text = 'Enjoy', fontFile = f'Fonts/SVGFONT ({0}).svg', xOffset = 0, yOffset = 0, max_bed_x = 60, max_bed_y = 20, move_speed = 300, cut_speed = 300, letterLimit = 25, arThres = 8):
    
    fontDict = GetGlyphDictionary(fontFile)

    if len(text)>letterLimit:
        print('Thats wat she said')
        exit(0)

    #single line attempt
    final_paths = GetSingleLine(text, fontDict)

    print(CheckAr(final_paths))
    if CheckAr(final_paths) > arThres and len(text.split(' ')) > 1:
        final_paths = GetMultiLine(text, fontDict)

    SaveSvg(final_paths)
    gcode = GenerateGcode(move_speed, cut_speed)
    bbox = GcodeBBox(gcode)
    gcode = GcodeMove(gcode,bbox[0] * -1,bbox[3] * -1)
    gcode = GcodeScale(gcode,1,-1)
    bbox = GcodeBBox(gcode)
    scalefactor = max_bed_x/bbox[1]
    gcode = GcodeScale(gcode,scalefactor,scalefactor)
    bbox = GcodeBBox(gcode)
    if(bbox[3]>20):
        scalefactor = max_bed_y/bbox[3]
        gcode = GcodeScale(gcode,scalefactor,scalefactor)
    return gcode