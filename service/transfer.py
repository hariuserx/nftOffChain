import random
import threading
import time
import logging
from queue import Queue

from blockchain.blockchain import transfer_nft_in_block_chain

# A stream data store. Like Kafka. This has to be thread safe. So we will use python queue
# which is mean for multi producer and multi consumer
queue = Queue()

sentinel = True
sentinel_ms_ia = True

file_ms_ia_total = open("results_ms_ia_total.csv", "w")
file_ms_ia_initial = open("results_ms_ia_initial.csv", "w")
file_ms_sr_total = open("results_ms_sr_total.csv", "w")
file_ms_sr_initial = open("results_ms_sr_initial.csv", "w")


def run_ms_ia_final_section(nft_data, owner_address, receiver_address, database, start_time):
    logging.info("Initiating Final section transfer of NFT_ID %s (MS-IA)", nft_data[0].nft_id)
    # Final section

    nft_id = nft_data[0].nft_id
    nft_data = database.data_ms_ia_on_chain[nft_id]

    with nft_data[1]:
        # release the lock for the next command
        global sentinel_ms_ia
        sentinel_ms_ia = True

        if nft_data[0].owner != owner_address:
            logging.error("Unauthorized transaction detected at Off-Chain in final section of MS-IA. Not an owner. \n"
                          "Try to update the balance sheet")
        else:
            response = transfer_nft_in_block_chain(nft_id, owner_address, receiver_address)
            if response:
                logging.info("Transfer successful at the OnChain.")
                database.update_on_chain_ms_ia(nft_id, receiver_address)
            else:
                actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"
                while actual_owner == owner_address:
                    actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"

                database.update_on_chain_ms_ia(nft_id, actual_owner)
                time.sleep(0.00)

                logging.error("Transfer un-successful at the OnChain. This is not the final state. \n"
                              "Actual owner is %s", actual_owner)

    diff = time.time() - start_time
    file_ms_ia_total.write("{0:0.7f}".format(diff * 1000) + "\n")
    file_ms_ia_total.flush()


def ms_ia_on_chain_consumer():
    while True:
        nft_data, owner_address, receiver_address, database, start_time = queue.get()
        t = threading.Thread(target=run_ms_ia_final_section, args=(nft_data, owner_address, receiver_address,
                                                                   database, start_time))
        global sentinel_ms_ia
        sentinel_ms_ia = False
        t.start()
        # while sentinel_ms_ia is not True:
        #     pass


def ms_ia(owner_address, receiver_address, nft_id, database):
    start_time = time.time()
    logging.info("Initiating transfer of NFT_ID %s (MS-IA)", nft_id)
    nft_data = database.data[nft_id]
    with nft_data[1]:
        # release the lock for the next command
        global sentinel
        sentinel = True

        if nft_data[0].owner != owner_address:
            logging.error("Unauthorized transaction detected at Off-Chain. Not an owner. \n"
                          "Try to update the balance sheet")
        else:
            # initial section
            database.update(nft_id, receiver_address)
            time.sleep(0.0)
            diff = time.time() - start_time
            file_ms_ia_initial.write("{0:0.7f}".format(diff * 1000) + "\n")
            file_ms_ia_initial.flush()
            logging.info("Transfer successful at the OffChain. This is not the final state")
            queue.put((nft_data, owner_address, receiver_address, database, start_time))


def ms_sr(owner_address, receiver_address, nft_id, database):
    start_time = time.time()
    logging.info("Initiating transfer of NFT_ID %s (MS-SR)", nft_id)
    nft_data = database.data[nft_id]

    with nft_data[1]:
        # release the lock for the next command
        global sentinel
        sentinel = True

        if nft_data[0].owner != owner_address:
            logging.error("Unauthorized transaction detected at Off-Chain. Not an owner. \n"
                          "Try to update the balance sheet")
        else:
            # initial section
            database.update(nft_id, receiver_address)
            time.sleep(0.00)
            logging.info("Transfer successful at the OffChain. This is not the final state")
            diff = time.time() - start_time
            file_ms_sr_initial.write("{0:0.7f}".format(diff * 1000) + "\n")
            file_ms_sr_initial.flush()
            # Final section
            response = transfer_nft_in_block_chain(nft_id, owner_address, receiver_address)
            if response:
                logging.info("Transfer successful at the OnChain.")
            else:
                actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"
                while actual_owner == owner_address:
                    actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"

                database.update(nft_id, actual_owner)
                time.sleep(0.00)

                logging.error("Transfer un-successful at the OnChain. This is not the final state. \n"
                              "Actual owner is %s", actual_owner)
    diff = time.time() - start_time
    file_ms_sr_total.write("{0:0.7f}".format(diff * 1000) + "\n")
    file_ms_sr_total.flush()


def transfer_nft(owner_address, receiver_address, nft_id, database, use_ms_sr):
    global sentinel
    if use_ms_sr:
        t = threading.Thread(target=ms_sr, args=(owner_address, receiver_address, nft_id, database))
        sentinel = False
        t.start()
        # while sentinel is not True:
        #     pass
    else:
        t = threading.Thread(target=ms_ia, args=(owner_address, receiver_address, nft_id, database))
        sentinel = False
        t.start()
        # while sentinel is not True:
        #     pass
    # x.join() // Don't join the thread. No need to wait.
