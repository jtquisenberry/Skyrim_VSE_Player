from skyrimvsep.main import SkyrimVSEPlayer

SERIAL = 'emulator-5554'
HOST = '127.0.0.1'
PORT = 5037
LOG = r'D:\Projects\skyrim.txt'

if __name__ == '__main__':
    svsep = SkyrimVSEPlayer(serial=SERIAL, host=HOST, port=PORT, outfile=LOG)
    ret_val = svsep.start()
    print(str(ret_val))
