import json
import ipfshttpclient
from web3 import Web3

client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi_contract = json.loads('[{\"constant\":true,\"inputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"name\":\"files\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"}],\"name\":\"popFiles\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"hash\",\"type\":\"string\"}],\"name\":\"pushFiles\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]')

contract = web3.eth.contract(
    address = "0xBe80C4520DcD84916b85eDB47E869F1Fa09c6Ac5",
    abi = abi_contract
)



#nonce = web3.eth.getTransactionCount(myAccount)
#res = client.add("HelloWorld.txt")

#print(client.cat('Qmbe6AH1TVu9WH8uk5V5AFVAvAQpPnm6d4PazpjfEF9NUj'))

#print(Eth.getBalance('0x444f5541eF19f97963131336fe7f40356f6eFdF5'))

def updateList(filename):
    filehash = contract.functions.popFiles("file_name_list").call()
    filebuffer = client.get_json(filehash)
    filebuffer.append(filename)
    ipfshash = client.add_json(filebuffer)
    contract.functions.pushFiles("file_name_list", ipfshash).transact()
    

def uploader():
    print()
    addr = input("Enter the address of the file: ")
    ipfshash = client.add(addr)
    print (ipfshash)
    contract.functions.pushFiles(ipfshash['Name'], ipfshash['Hash']).transact()
    
    updateList(ipfshash['Name'])
    
    #print(contract.functions.popFiles("Test").call())
    #print(client.get_json("QmZEtadz3VkpYEcnRP9nBfn9PBT92LNgahuRWmoiqrsmz5"))

def downloader():
    print()
    filename = input("Enter the name of the file: ")
    filehash = contract.functions.popFiles(filename).call()
    filebuffer = client.cat(filehash)
    print(filebuffer)

def printFileList():
    print()
    filehash = contract.functions.popFiles("file_name_list").call()
    print(client.get_json(filehash))

def initialize():
    ipfshash = client.add_json([])
    contract.functions.pushFiles("file_name_list", ipfshash).transact()
    print("\nInitialize success, file_name_list hash stored at blockchain ")
    
if __name__ == '__main__':
    i = input("\nAre you first time user? (y/n): ")
    if(i == 'y'):
        initialize()
    while (i != '3'):
        printFileList()
        i = input("\nPress 1 to upload the file, \nPress 2 to download the file, \nPress 3 to exit the program: ")
        if (i == '1'):
            uploader()
        if (i == '2'):
            downloader()
        
