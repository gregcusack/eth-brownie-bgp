from netfilterqueue import NetfilterQueue
from scapy.all import *
import brownie
from web3 import Web3, HTTPProvider
from eth_account import Account


def print_and_accept(pkt):
    # print(pkt)
    pkt.accept()
    # print(pkt)
    spkt=IP(pkt.get_payload())

    print(spkt[IP].src)
    print(spkt.haslayer(TCP))

    # print(dir(spkt))

    # print(type(pkt))
    # print(spkt)

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
