"""simple-dmidecode.py is a Python interface to the 22 dmidecode keyword strings."""

import os
import subprocess
import string
import json
import sys


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
        """
        handle.write(json.dumps(self.dmidict, indent=4, separators=(',', ': ')))
