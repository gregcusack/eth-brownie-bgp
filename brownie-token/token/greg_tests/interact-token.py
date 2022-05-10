
import brownie

if __name__ == "__main__":

    brownie.network.connect('development')
    if not brownie.network.is_connected():
        print("error can't conenct to brownie network")
        sys.exit(-1)
    
    contract = brownie.Contract('0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87')
