import random
import threading
import time
import logging
from blockchain.blockchain import transfer_nft_in_block_chain


# A stream data store. Like Kafka. This has to be thread safe. So we will use python queue
# which is mean for multi producer and multi consumer

def ms_sr(owner_address, receiver_address, nft_id, database):
    logging.info("Initiating transfer of NFT_ID %s", nft_id)
    nft_data = database.data[nft_id]

    with nft_data[1]:
        if nft_data[0].owner != owner_address:
            logging.error("Unauthorized transaction detected at Off-Chain. Not an owner. \n"
                          "Try to update the balance sheet")
        else:
            # initial section
            database.update(nft_id, receiver_address)
            time.sleep(1)
            logging.info("Transfer successful at the OffChain. This is not the final state")
            # Final section
            response = transfer_nft_in_block_chain()
            if response:
                logging.info("Transfer successful at the OnChain.")
            else:

                actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"
                while actual_owner == owner_address:
                    actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"

                database.update(nft_id, actual_owner)
                time.sleep(1)

                logging.error("Transfer un-successful at the OnChain. This is not the final state. \n"
                              "Actual owner is %s", actual_owner)


def ms_ia(owner_address, receiver_address, nft_id, database):
    pass


def transfer_nft(owner_address, receiver_address, nft_id, database, use_ms_sr):
    if use_ms_sr:
        t = threading.Thread(target=ms_sr, args=(owner_address, receiver_address, nft_id, database))
        t.start()
    else:
        t = threading.Thread(target=ms_sr, args=(owner_address, receiver_address, nft_id, database))
        t.start()
        pass
    # x.join() // Don't join the thread. No need to wait.
