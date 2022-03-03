
import brownie

if __name__ == "__main__":
    brownie.Token.deploy("Test Token", "TST", 18, 1e21, {'from': brownie.accounts[0]})