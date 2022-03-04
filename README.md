# eth-brownie-bgp

## Documentation:

### Getting setup with Brownie
https://iamdefinitelyahuman.medium.com/getting-started-with-brownie-part-1-9b2181f4cb99

## Sending ETH from acct1 to acct2 triggered by the reception of an HTTP packet with the header "eth-header" to a Flask Server
### Setup
Install dependencies 
```
pip install Web3
pip install eth-brownie
pip install Flask
pip install scapy
```

Add sudo for python in virtual environment
```
echo "psudo() { sudo env PATH="$PATH" "$@"; }" > ~/.bashrc 
```
^ Now when we want to run python with sudo, use `psudo`

Launch flask app on localhost:5100
```
python eth-brownie-bgp/bgp/netfilter/app.py
```

Install IPTables rule to forward packets up to nfqueue so we can process it
```
sudo iptables -I INPUT -p tcp -d 192.168.1.211 --dport 5100 -j NFQUEUE --queue-num 1
```

Start Brownie in it's own terminal window
```
brownie console
```

In another terminal, run the transfer method -> will hang and wait for packet sent from IPTables
```
psudo python eth-brownie-bgp/bgp/greg_tests/test-transfer.py
```
^ MUST run with psudo (aka need sudo to run this)

### Run
Send an HTTP request to the flask server to trigger the transfer of ETH
```
curl -H "eth-header: true" http://127.0.0.1:5100
```

Logs of the transaction should appear in the terminal where `psudo python test-transfer.py` was run

---------------------------------

### Signing Transactions and Multisig
e.g. get soon to be owner of AS and IANA to sign off on AS ownership (ASN => AS address)
https://web3py.readthedocs.io/en/stable/web3.eth.account.html

## Some steps
Launch container and enter container
```
sudo docker run -it -d --network="host" gregcusack/eth-brownie-bgp:latest
sudo docker exec -it <docker-containerID> /bin/bash
```

From within container
```
git clone git@github.com:gregcusack/eth-brownie-bgp.git
cd eth-brownie-bgp
brownie compile
brownie console
```

Create accounts
```
acct = web3.eth.account.create() # owner of Smart contract account (IANA)
acct2 = web3.eth.account.create() # AS we will use to assign an ASM
```

Deploy contracts
```
contract = IANA.deploy({'from': acct.address})
contract_recover = Recover.deploy({'from': acct.address})
contract = IANA[0]
contract_recover = Recover[0]
```

Imports and helper function
```
from web3 import Web3
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message
def to_32byte_hex(val):return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))
```

WIP: Add an ASN/address pair to ASNList -> signed by both IANA and AS that is to get assigned an ASN
```
msgToBeSigned = contract.IANA_getSignatureMessage(2, acct2.address) 	# say -> let's give acct2 ASN 2
msgToBeSignedEncoded = encode_defunct(text=msgToBeSigned.hex()) 	# encode msg
private_key = acct2._private_key 					# extract private key to sign msg
msgSigned = w3.eth.account.sign_message(msgToBeSignedEncoded, private_key=private_key) # sign message
```

Sanity check -> check we can recover message
```
w3.eth.account.recover_message(msgToBeSignedEncoded, signature=msgSigned.signature) # output should be public address of acct2
```

Get acct2 public address:
```
acct2.address
```

Generate sigV, sigR, sigS for IANA validation
```
ec_recover_args_iana = (msgSignedHash, sigV, sigR, sigS) = (Web3.toHex(msgSigned.messageHash), msgSigned.v, to_32byte_hex(msgSigned.r), to_32byte_hex(msgSigned.s))
```

Check we can recover via Recover contract -> output should be acct2.address
```
tx = contract_recover.ecr(msgSignedHash, sigV, sigR, sigS)
```

### Add ASN -> NOTE: this is very much WIP and is not working as i would like. Still need to think about how this should work
Add ASN (1)
```
contract.IANA_addASN(1, acct.address, sigV, sigR, sigS)
```
^ this will get reverted. see IANA.sol contract. function not validating signature (msgSigned). Will fail.

Add ASN (2)
```
tx = contract.IANA_addASNSigned(1, acct.address, msgSignedHash, sigV, sigR, sigS)
```
^ this WILL work but will allow you to place in any value for ASN (1). Can put 2 or 4000 or whatever and it will succeed. Need to validate properly here. Not sure if need to do in smart contract function here or not. BUT `acct` needs to validate that `msgSigned` is valid from `acct2` and ensure that the ASN placed in `IANA_addASNSigned()` matches the ASN that was used in msgToBeSigned. Note, since `IANA_addASNSigned()` has a `onlyOwners` modifier, we ensure that IANA aka `acct` is essentially signing the transaction as well.
Need to think more about this and how to do.














