import sys
import os
import os.path
import json
import xmltodict
import zipfile
import shutil

TEMPLATE = '''
{
    "type": "shape",
    "name": "Shape",
    "meta": {
      "ux": {
        "nameL10N": "SHAPE_PATH"
      }
    },
    "transform": {
      "a": 1,
      "b": 0,
      "c": 0,
      "d": 1,
      "tx": 0,
      "ty": 0
    },
    "style": {
      "fill": {
        "type": "solid",
        "color": {
          "mode": "RGB",
          "value": {
            "r": 0,
            "g": 0,
            "b": 0
          }
        }
      },
      "stroke": {
        "type": "none",
        "color": {
          "mode": "RGB",
          "value": {
            "r": 0,
            "g": 0,
            "b": 0
          }
        },
        "width": 0
      }
    },
    "shape": {
      "type": "path",
      "path": ""
    }
}
'''

def zip(src, dst):
    zf = zipfile.ZipFile("%s" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()

def unzip(src, dst):
    zip_ref = zipfile.ZipFile(src, 'r')
    zip_ref.extractall(dst)
    zip_ref.close()


if __name__ == '__main__':

    # Get the svg file from command line argument
    if len(sys.argv) == 3:
        svg_file_name = sys.argv[1]
        xd_file_name = sys.argv[2]
    else:
        raise Exception('Missing parameters!')

    # Check if the SVG file exists
    if not os.path.isfile(svg_file_name):
        raise Exception(svg_file_name + ' does not exist!')

    # Check if the XD file exists
    if not os.path.isfile(xd_file_name):
        raise Exception(xd_file_name + ' does not exist!')

    # Check if file is an SVG
    extension = os.path.splitext(svg_file_name)[-1]
    if extension != '.svg':
        raise Exception(svg_file_name + ' is not an SVG file!')

    # Check if file is XD file
    extension = os.path.splitext(xd_file_name)[-1]
    if extension != '.xd':
        raise Exception(xd_file_name + ' is not an XD file!')


    # Extract all paths from SVG file
    with open(svg_file_name) as file:
        doc = xmltodict.parse(file.read())
        file.close()

    paths = []
    temp = doc['svg']['path']
    if type(temp) is not list:
        temp = [temp]
    for shape in temp:
        paths.append(shape['@d'])

    # Use TEMPLATE to create a shape representation in JSON
    shapes = []
    for path in paths:
        new_template = json.loads(TEMPLATE)
        new_template['shape']['path'] = path
        shapes.append(new_template)

    # Unzip XD file
    dst = xd_file_name + "_CONTENTS"
    unzip(xd_file_name, dst)

    # Check if there are is artwork in the XD File contents
    path_to_agc_file = dst + '/artwork/pasteboard/graphics/graphicContent.agc'
    if not os.path.isfile(path_to_agc_file):
        raise Exception('Before you can add an svg, open the XD file, add a shape OUTSIDE AN ARTBOARD. Then save it. Then run the program again')
    
    # Process the JSON file
    with open(path_to_agc_file) as file:
        graphic_content_data = json.loads(file.read())
        file.close()

    # Add the shapes taken from SVG file
    for shape in shapes:
        graphic_content_data['children'].append(shape)

    JSON_data = json.dumps(graphic_content_data)

    # Write the JSON data to file
    with open(path_to_agc_file, 'w') as file:
        file.write(JSON_data)
        file.close()

    # Zip contents and clean up
    zip(dst, xd_file_name)
    print("SVG Added")
    shutil.rmtree(dst)
    print("Temporary Files Deleted")
