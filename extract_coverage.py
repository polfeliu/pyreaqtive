from xml.dom import minidom

file = minidom.parse('coverage.xml')

percent = file.getElementsByTagName('coverage')[0].attributes['line-rate'].value
percent = float(percent) * 100
print(percent)
