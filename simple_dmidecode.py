"""simple-dmidecode.py is a Python interface to the 22 dmidecode keyword strings."""

import os
import subprocess
import string
import json
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Dmi:
    """Core dmidecode output class."""

    def __init__(self):
        """Initialize the class and pull core dmi information."""
        self.dmipath = ''
        self.dmikeys = ["bios-vendor", "bios-version", "bios-release-date", "system-manufacturer",
                        "system-product-name", "system-version", "system-serial-number", "system-uuid",
                        "baseboard-manufacturer", "baseboard-product-name", "baseboard-version",
                        "baseboard-serial-number", "baseboard-asset-tag", "chassis-manufacturer", "chassis-type",
                        "chassis-version", "chassis-serial-number", "chassis-asset-tag", "processor-family",
                        "processor-manufacturer", "processor-version", "processor-frequency"]
        self.dmidict = {}
        # Get the evironment PATH variable and search it for dmidecode, if found, set dmidecode path.
        for location in os.environ.get("PATH").split(":"):
            if os.path.exists(location + "/dmidecode"):
                # print("Found dmidecode binary at " + location + "/dmidecode.\n")
                self.dmipath = location + "/dmidecode"
        # If the dmidecode binary is not found in the path, raise an error and exit.
        if self.dmipath == '':
            raise EnvironmentError("No dmidecode binary found in PATH.\n")
            exit()

    def decode(self):
        """Decode the system dmi and store the result in a dict."""
        for dmikey in self.dmikeys:
            response = subprocess.check_output([self.dmipath, "-s", dmikey])
            self.dmidict[dmikey] = string.strip(response.splitlines()[0])
        return self.dmidict

    def dumpjson(self, handle=sys.stdout):
        """JSON output method.

        Dump the contents of the self.dmidict to a file in JSON format.
        If no filehandle is specified, dump to stdout.
        If "None" is specified, no output will be written.
        Return is a string object containing the json formatted output.
        """
        output = json.dumps(self.dmidict, indent=4, separators=(',', ': '))
        if handle is not None:
            handle.write(output)
        return output

    def dumpxml(self, handle=sys.stdout):
        """XML output method.

        Build an XML document around the DMI information organized by category.
        If no filehandle is specified, dump the XML document to stdout.
        If "None" is specified as the filehandle, no output will be written.
        Return value is an xml.etree.ElementTree.ElementTree object containing the XML.
        """
        # Create the root and SubElements of the XML tree.
        root = ET.Element("DMI")
        bios = ET.SubElement(root, "bios")
        system = ET.SubElement(root, "system")
        baseboard = ET.SubElement(root, "baseboard")
        chassis = ET.SubElement(root, "chassis")
        processor = ET.SubElement(root, "processor")
        # For each SubElement, walk through the dict keys and assign attributes to the SubElements.
        for key in self.dmidict.keys():
            if key.startswith("bios"):
                bios.set(key[5:], self.dmidict[key])
            elif key.startswith("system"):
                system.set(key[7:], self.dmidict[key])
            elif key.startswith("baseboard"):
                baseboard.set(key[10:], self.dmidict[key])
            elif key.startswith("chassis"):
                chassis.set(key[8:], self.dmidict[key])
            elif key.startswith("processor"):
                processor.set(key[10:], self.dmidict[key])
        tree = ET.ElementTree(root)
        if handle is not None:
            ugly = ET.tostring(root, "utf-8")
            gugly = minidom.parseString(ugly)
            handle.write(gugly.toprettyxml(indent="    "))
        return tree

    def dumpsql(self, table, uidcol, uidval, mode, keylist=None):
        """SQL output method.

        For obvious reasons, SQL output is going to be a little different.
        The goal here is a method which, given a table name and an ID (column and value) as input, will generate SQL
        to insert or update the row identified by that ID in the table indicated.
        If all keys are not wanted, a list object containing the desired keys in the desired order can be
        passed as well. Otherwise the dmikeys list is used.
        Return value is a string containing the constructed SQL.
        """
        # Initialize the SQL string.
        if upper(mode) not in ["UPDATE", "INSERT"]:
            raise ValueError("Only UPDATE and INSERT methods are supported.\n")
        mode = upper(mode)
        # Set the default keylist value to self.dmikeys.
        if keylist is None:
            keylist = self.dmikeys
        # Iterate over the keylist and make sure that all of the keys are legal dmidecode keywords.
        for key in keylist:
            if key not in self.dmikeys:
                raise ValueError("Unknown keyword " + str(key) + "in keylist.\n")
        # Execute INSERT mode logic.
        if mode == "INSERT":
            keystr = "'" + uidcol + "'" + str(keylist).strip("[]")
            valstr = "'" + str(uidval) + "', "
            for key in range(0, len(keylist)-2):
                key = keylist[key]
                valstr = valstr + "'" + self.dmidict[key] + "', "
            key = keylist[len(keylist)-1]
            valstr = valstr + "'" + self.dmidict[key] + "')"
            sqlstmt = "INSERT into " + table + " (" + keystr + ") VALUES (" + valstr
            print(sqlstmt)
            return(sqlstmt)
        # Or UPDATE mode logic.
        else:
            sqlstmt = mode + " " + table + " SET ("
            for key in range(0, len(keylist)-2):
                key = keylist[key]
                sqlstmt = sqlstmt + key + '="' + self.dmidict[key] + '", '
            key = keylist[(len(keylist)-1)]
            sqlstmt = sqlstmt + key + '="' + self.dmidict[key] + '") '
            sqlstmt = sqlstmt + "WHERE " + str(uidcol) + "=" + str(uidval) + ";"
            print(sqlstmt)
            return(sqlstmt)
