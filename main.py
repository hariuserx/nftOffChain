# Entry point
from database.database import FakeDatabase
from initialize import initialize_nft_data
from service.transfer import transfer_nft
import logging

# initialize logger
from service.view import print_nft_data

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")


# initialize the NFT data from Blockchain
nft_data = initialize_nft_data()

# initialize the database
database = FakeDatabase(data=nft_data)

# By default we use MS-IA
use_ms_sr = False

print("Type \"help\" for help or enter \"quit\" to quit")

while True:
    print("-------------------------------")
    command = input("Enter a command:\n")
    if command == "quit":
        print("Good Bye!!")
        break
    elif command == "help":
        print("This is the interface to interact with the NFT transaction Off Chain\n"
              "Available commands\n"
              "1. help : Display this help information\n"
              "2. transfer : This command transfers the NFT from your address to \n"
              "the receiver. This will prompt for <yourAddress> <toAddress> and <nftID>.\n"
              "3. view : To view the current Off-Chain data status\n"
              "4. set-safety : Give to command to set the safety. Will prompt for the input"
              ". Uses MS-IA by default\n"
              "5. quit : exit the application\n")
    elif command == "transfer":
        owner_address = input("Enter your address:\n")
        receiver_address = input("Enter the receiver address:\n")
        nft_id = input("Enter the NFT ID to transfer:\n")
        transfer_nft(owner_address=owner_address, receiver_address=receiver_address, nft_id=int(nft_id),
                     database=database, use_ms_sr=use_ms_sr)
    elif command == "view":
        print_nft_data(database)
    elif command == "set-safety":
        algo = input("Press 1 for MS-IA and 2 for MS-SR\n")
        if algo == "1":
            use_ms_sr = False
        elif algo == "2":
            use_ms_sr = True
        else:
            logging.error("Invalid input")
    else:
        print("Invalid Command")
