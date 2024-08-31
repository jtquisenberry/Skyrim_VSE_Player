import adbutils

HOST = "127.0.0.1"
PORT = 5037

print("BEGIN DEVICES")
print()

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(f"Serial: {info.serial}, State: {info.state}")
    # Serial: emulator-5554, State: device

print()
print("END DEVICES")

# d = adb.device(serial=info.serial)
# d.reboot()