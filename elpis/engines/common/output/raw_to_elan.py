#!/usr/bin/python3

import dict2xml
import subprocess
import re
from typing import Any, Dict

def convert_raw_to_elan(transcription_data: Dict[str, Any], xml_path: str, elan_path: str, style_path: str = "/elpis/elpis/engines/common/output/templates/elan.xsl"):
    """
    Convert a dict of raw data to an XML-Elan file.

    :param transcription_data: dict of various data (author, participant, tier id, segments, etc.).
    :param xml_path: xml path (output file of dict and input file for XSL transformation).
    :param elan_path: final output path.
    :param style_path: XSL style path for XSL transformation.
    :return: elan_path output path.
    """
    xml_data = dict2xml.dict2xml(transcription_data, wrap="data", indent=" " * 4)
    with open(xml_path, "w") as xml_file:
        xml_file.write(xml_data)
    xslt_command = "/elpis-gui/node_modules/.bin/xslt3"  # Later put this folder in $PATH?
    parameters = " ".join([f'%s="{value}"' % re.sub(r"\s", "_", key) for key, value in transcription_data.items() if key != "segments"])
    command = f"""{xslt_command} -s:'{xml_path}' -xsl:'{style_path}' -o:'{elan_path}' {parameters}"""
    stream = subprocess.run(command, shell=True)
    return elan_path
