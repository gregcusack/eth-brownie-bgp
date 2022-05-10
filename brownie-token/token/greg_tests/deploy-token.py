
import brownie

if __name__ == "__main__":

    brownie.network.connect('development')
    if not brownie.network.is_connected():
        print("error can't conenct to brownie network")
        sys.exit(-1)
    brownie.Token.deploy("Test Token", "TST", 18, 1e21, {'from': brownie.accounts[0]})
