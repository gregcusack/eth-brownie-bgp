#import web3
from web3 import Web3 #, HTTPProvider
import brownie
import sys
#from web3.auto import w3

from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.layers.http import HTTPRequest

w3 = None

def transfer_tokens():
    accounts = w3.eth.accounts
    acct1_balance = w3.eth.getBalance(accounts[0])
    acct2_balance = w3.eth.getBalance(accounts[1])

    acct1_balance = float(w3.fromWei(acct1_balance, 'ether'))
    acct2_balance = float(w3.fromWei(acct2_balance, 'ether'))

    print("acct1 balance pre: " + str(acct1_balance) + " eth")
    print("acct2 balance pre: " + str(acct2_balance) + " eth")

    # send 1 eth from acct0 to acct1
    payload = {
        'from': accounts[0],
        'to': accounts[1],
        'value': w3.toWei(1, 'ether')        # 'value' takes in wei val. so convert eth to wei
    }

    tx_hash = w3.eth.sendTransaction(payload)

    acct1_balance = w3.eth.getBalance(accounts[0])
    acct2_balance = w3.eth.getBalance(accounts[1])

    acct1_balance = float(w3.fromWei(acct1_balance, 'ether'))
    acct2_balance = float(w3.fromWei(acct2_balance, 'ether'))

    print("acct1 balance post: " + str(acct1_balance) + " eth")
    print("acct2 balance post: " + str(acct2_balance) + " eth")


def print_and_accept(pkt):
    # print(pkt)
    pkt.accept()
    # print(pkt)
    # headers = pkt.haslayer(TCP)
    # print(headers)
    load_layer("http")
    spkt=IP(pkt.get_payload())
    if spkt.haslayer(Raw):
        if b"eth-header" in spkt[Raw].load:
            transfer_tokens()

    # if spkt.haslayer(TCP):
    #     if spkt.dport == 5100:
    #         if spkt.haslayer(Raw):
    #             print(spkt[Raw].load)

    # print(spkt[IP].src)
    # print(spkt.haslayer(TCP))
    # transfer_tokens()

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


#from brownie import *


if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider("http://192.168.1.2:8545"))

    if not w3.isConnected():
        print("error can't connect to ganache network")
        sys.exit(-1)

    nfqueue = NetfilterQueue()
    nfqueue.bind(2, print_and_accept)
    print("waiting for nfqueue packets in queue...")
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')

    nfqueue.unbind()



    #return Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

