import random
import time


# Mock blockchain layer. Returns True for success response and False for failure
def transfer_nft_in_block_chain(nft_id, owner, receiver):
    time.sleep(5)
    value = random.random()

    # use this to control failure ratio
    probability_of_failure = 0.0

    if value <= probability_of_failure:
        return False
    else:
        return True


def transfer_nft_in_block_chain_batch(batch):
    time.sleep(5)


# This periodically checks the batched transactions status in blockchain
# Returns "Success" or "Failure" or "Pending"
def check_transaction_status(nft_id):
    transfer_nft_in_block_chain(nft_id, None, None)
