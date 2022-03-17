import logging
import random
import threading
import time

import service.transfer
from blockchain.blockchain import check_transaction_status, \
    transfer_nft_in_block_chain_batch

batch_size = 100
start_time = time.time()
checker_start_time = time.time()


def run_ms_ia_final_section(nft_data, owner_address, batch):
    logging.info("Initiating Final section transfer of NFT_ID %s (MS-IA)", nft_data[0].nft_id)
    # Final section
    if nft_data[0].owner != owner_address:
        logging.error("Unauthorized transaction detected at Off-Chain in final section of MS-IA. Not an owner. \n"
                      "Try to update the balance sheet")
    else:
        transfer_nft_in_block_chain_batch(batch)


# This is the batching strategy with batch size N.
def ms_ia_on_chain_consumer(database):
    global start_time
    global checker_start_time
    # This keeps track of the in process NFTs. Initially empty
    in_process_nfts = set()
    # Keeps track of next available NFTs
    pending_nfts = set()
    while True:
        # If threshold is reached or if time has reached
        if service.transfer.queue.qsize() > 100 or (time.time() - start_time) > 1000:
            # update the pending transactions
            if time.time() - checker_start_time > 100:
                for nft in in_process_nfts:
                    status = check_transaction_status(nft[0])
                    if status == "Success":
                        logging.info("Transfer successful at the OnChain.")
                        in_process_nfts.remove(nft)
                    elif status == "Failure":
                        # Can be done in a separate thread.
                        actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"
                        while actual_owner == nft[1]:
                            actual_owner = str(random.randint(0, len(database.data) - 1)) + "x"

                        database.update(nft[0].nft_id, actual_owner)
                        time.sleep(1)

                        logging.error("Transfer un-successful at the OnChain. This is not the final state. \n"
                                      "Actual owner is %s", actual_owner)
                        in_process_nfts.remove(nft)
                    else:
                        # Pending
                        pass

                checker_start_time = time.time()

            batch = []
            for nft in pending_nfts:
                if nft not in in_process_nfts:
                    batch.append(nft)

            for _ in range(100):
                nft = service.transfer.queue.get()
                if nft not in in_process_nfts:
                    batch.append(nft)
                else:
                    pending_nfts.add(nft)
                in_process_nfts.add(nft)

            t = threading.Thread(target=run_ms_ia_final_section,
                                 args=(batch,))
            t.start()

            # reset the time
            start_time = time.time()
