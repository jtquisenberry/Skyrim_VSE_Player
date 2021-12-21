from skyrimvsep.main import SkyrimVSEPlayer

if __name__ == '__main__':
    svsep = SkyrimVSEPlayer(outfile='skyrim.txt')
    ret_val = svsep.start()
    print(str(ret_val))
