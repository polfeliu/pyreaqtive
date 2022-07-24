from xml.dom import minidom
import os

# parse an xml file by name
file = minidom.parse('coverage.xml')

percent = file.getElementsByTagName('coverage')[0].attributes['line-rate'].value
percent = float(percent) * 100

os.environ["COVERAGE_PERCENT"] = str(percent)

color = "red"

if percent == 100:
    color = "brightgreen"
elif percent > 90:
    color = "orange"

os.environ["COVERAGE_COLOR"] = color
