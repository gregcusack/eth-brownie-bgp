#import web3
from web3 import Web3 #, HTTPProvider
import brownie
import sys
#from web3.auto import w3

from netfilterqueue import NetfilterQueue
from scapy.all import *

def transfer_tokens():
    acct1_balance = brownie.accounts[0].balance()
    acct2_balance = brownie.accounts[1].balance()

    print("acct1 balance pre: " + str(acct1_balance.to("ether")))
    print("acct2 balance pre: " + str(acct2_balance.to("ether")))

    tx = brownie.accounts[0].transfer(brownie.accounts[1], "1.2 ether")
    # print("tx: " + tx)

    acct1_balance = brownie.accounts[0].balance()
    acct2_balance = brownie.accounts[1].balance()

    print("acct1 balance post: " + str(acct1_balance.to("ether")))
    print("acct2 balance post: " + str(acct2_balance.to("ether")))


def print_and_accept(pkt):
    # print(pkt)
    pkt.accept()
    # print(pkt)
    spkt=IP(pkt.get_payload())

    print(spkt[IP].src)
    print(spkt.haslayer(TCP))
    transfer_tokens()

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


#from brownie import *


if __name__ == "__main__":
    # w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    # acct = w3.eth.account.create()

    brownie.network.connect('development')
    if not brownie.network.is_connected():
        print("error can't conenct to brownie network")
        sys.exit(-1)

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')

    nfqueue.unbind()



    #return Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

