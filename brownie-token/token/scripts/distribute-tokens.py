from brownie import Token, accounts
from scapy.all import *

def main():
    token = Token.deploy("Test Token", "TST", 18, 1e23, {'from': accounts[0]})

    acct1_balance = token.balanceOf(accounts[0])
    acct2_balance = token.balanceOf(accounts[1])
    print("acct1 balance pre: " + str(acct1_balance.to("ether")))
    print("acct2 balance pre: " + str(acct2_balance.to("ether")))

    token.transfer(accounts[1], 1e18, {'from': accounts[0]})
    
    acct1_balance = token.balanceOf(accounts[0])
    acct2_balance = token.balanceOf(accounts[1])
    print("acct1 balance post: " + str(acct1_balance.to("ether")))
    print("acct2 balance post: " + str(acct2_balance.to("ether")))


    return token

#def distribute_tokens(sender=accounts[0], receiver_list=accounts[1:]):
#    token = main()
#    for receiver in receiver_list:
#        token.transfer(receiver, 1e18, {'from': sender})
