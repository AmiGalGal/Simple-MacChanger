##simple MacChanger
##python MacChanger.py --interface [interface] --mac [desired mac address]
import subprocess
import optparse
import re

def userinput():
    parse_obj = optparse.OptionParser()
    parse_obj.add_option("-i", "--interface", dest="interface", help = "the interface (example: eth0, wlan0)")
    parse_obj.add_option("-m", "--mac", dest="macAdd", help = "new mac address (xx:xx:xx:xx:xx:xx")
    return parse_obj.parse_args()

def change_macaddress(inputs):
    print("Mac Address changing...\n")

    subprocess.call(["ifconfig", inputs.interface, "down"])
    subprocess.call(["ifconfig", inputs.interface, "hw", "ether", inputs.macAdd])
    subprocess.call(["ifconfig", inputs.interface, "up"])

def inter(inputs):
    try:
        # Run the ifconfig command for the specified interface
        ifconfig_output = subprocess.check_output(["ifconfig", inputs.interface]).decode('utf-8')

        # Use regex to search for the MAC address pattern
        mac_address_pattern = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
        mac_address = re.search(mac_address_pattern, ifconfig_output)

        if mac_address:
            return mac_address.group(0)
        else:
            return "MAC address not found."

    except subprocess.CalledProcessError as e:
        return f"Error executing ifconfig: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def is_valid(inputs):
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(mac_regex.match(inputs.macAdd))


(inputs, args) =  userinput()
if not(is_valid(inputs)):
    print("Process Failed due to invalid desired address")
    exit()
old = inter(inputs)
if old == inputs.macAdd:
    print("Process Failed, the desired address is already the existing mac address")
    exit()
change_macaddress(inputs)
new = inter(inputs)
if new == inputs.macAdd:
    print("MacAddress changed to " + inputs.macAdd)
else:
    print("Process Failed for unknown reasons")
