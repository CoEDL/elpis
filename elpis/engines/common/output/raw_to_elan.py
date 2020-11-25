import dict2xml
import subprocess
import re

def convert_raw_to_elan(transcription_data, xml_path, elan_path, style_path="/elpis/elpis/engines/common/output/elan.xsl"):
    xml_data = dict2xml.dict2xml(transcription_data, wrap="data", indent=" " * 4)
    with open(xml_path, "w") as xml_file:
        xml_file.write(xml_data)
    xslt_command = "/elpis-gui/node_modules/.bin/xslt3"  # Later put this folder in $PATH?
    parameters = " ".join([f'%s="{value}"' % re.sub(r"\s", "_", key) for key, value in transcription_data.items() if key != "segments"])
    command = f"""{xslt_command} -s:'{xml_path}' -xsl:'{style_path}' -o:'{elan_path}' {parameters}"""
    stream = subprocess.run(command, shell=True)
    return elan_path
