import random
import time


# Mock blockchain layer. Returns True for success response and False for failure
def transfer_nft_in_block_chain():
    time.sleep(20)
    value = random.random()

    # use this to control failure ratio
    probability_of_failure = 0.1

    if value <= probability_of_failure:
        return False
    else:
        return True
