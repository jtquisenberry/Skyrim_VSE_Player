# https://pypi.org/project/pure-python-adb/
from ppadb.client import Client

HOST = '127.0.0.1'
PORT = 5037

# Connect to ADB server.
# Default is "127.0.0.1" and 5037
adb = Client(host=HOST, port=PORT)
devices = adb.devices()

print("DEVICES")
for device in devices:
    print(device.serial)

print("\nEND OF DEVICES")
