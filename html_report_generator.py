# vim: abstop=4 shiftwidth=4 softtabstop=4

import os
import sys
from xml import etree
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element as E

try:
    import libxml2, libxslt
except:
    print("packages not completed, do not use python xml transmittion tool")

type_verification = "Verification"
type_error = "Error"
type_info = "Info"

class xml_parser(object):

    def __init__(self, reports_path = os.getcwd(), report_names = []):
        self.reports_path = reports_path
        self.report_names = report_names
        self.total = {}
        self.results = {}
        self.msg_path = "Shutdown/Message"

    def parse_xml(self, file_path):
        global type_error
        global type_verification
        global type_info

        if(os.path.exists(file_path)):
            xml_report = ET.parse(file_path)
            xml_root = xml_report.getroot()
            shutdown_msgs = xml_root.findall(self.msg_path)
            model_name = (file_path.split(os.sep)[1]).split(".")[0]
            
            for msg in shutdown_msgs:
                if( type_verification == msg.attrib["Type"]):
                    to = int(msg.attrib["Message"].split(" ")[0]) 
                    if model_name in self.total:
  			self.total[model_name] += to
			self.results[model_name] = 0
                    else:
                        self.total[model_name] = to

                elif( type_error == msg.attrib["Type"]):
                    res = int(msg.attrib["Message"].split(" ")[0]) 
                    self.results[model_name] = res
                    self.total[model_name] += res
                
                elif( type_info == msg.attrib["Type"]):
                    pass
                
                else:
                    print("Errors found in XML report")
#DEBUG
#		for mo in self.total:
#			print(mo)
#			print(self.total[mo])
#		for res in self.results:
#			print(res)
#			print(self.results[res])
    def generate_xml(self, report_path, template_path):
        et = ET.ElementTree()
        et._root = E("report", {})

        for res in self.results: 
            e_attr = {"name":str(res), "total":str(self.total[res]), "errors":str(self.results[res])}
            e_insert = E("module", e_attr)
            et._root.insert(-1, e_insert)
        
        et.write(report_path)
        fd = open(report_path, "r")
        fd_c = fd.read()
        fd.close()
        xml_beginning = "<?xml version='1.0' encoding='UTF-8'?>\n"
        fd = open(report_path, "w")
        fd.write(xml_beginning + fd_c)
        fd.close()

    def transmit(self, xsl_path):
        xml = libxml2.parseFile(report_path)
        xsl_style = libxml2.parseFile(xsl_path)
        xsl = libxslt.parseStylesheetDoc(xml_style)
        week_report = xsl.applyStyleSheet(xml)
        xsl.saveResultToFilename(os.getcwd(), week_report, 0)
		
if __name__ == "__main__":
    default_xmls_path = os.getcwd()
    xsl_sheet_path = os.getcwd() + "report.xsl"
    template_path = os.getcwd() + "report" + os.sep + "report_temp.xml"

    report_names = []
    for f in os.listdir(default_xmls_path):
        if "." in f and "xml" == (f.split(".")[1]).lower():
            report_names.append(f)
    
    parser = xml_parser(reports_path = default_xmls_path, report_names = report_names)
    
    for f in report_names:
		parser.parse_xml(default_xmls_path + f)
    parser.generate_xml(default_xmls_path + "report" + os.sep + "report.xml", template_path)
    
#FIXME: Because of parser.transmit method depends on libxml2 and libxslt,
#       but these tools are not installed,
#       so, please make sure these two packages exist in your environment
#
#   parser.transmit(xsl_sheet_path)

