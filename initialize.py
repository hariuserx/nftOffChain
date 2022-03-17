# initializes a dictionary of NFT ID to owner mapping.
# we also give a lock to every row for data read/write operations

# At this point this is just random data.
# TODO: Fill it using the NodeJs Blockchain interface
import logging
import threading

from database.model import NFTData


def initialize_nft_data():
    data = {}
    data_ms_ia_on_chain = {}

    for nft_id in range(10):
        nft = NFTData(nft_id=nft_id, owner=str(nft_id) + "x")
        nft_dup = NFTData(nft_id=nft_id, owner=str(nft_id) + "x")
        data[nft_id] = (nft, threading.Lock())
        data_ms_ia_on_chain[nft_id] = (nft_dup, threading.Lock())

    logging.info("Initialized dummy NFT data: %s", data)

    return data, data_ms_ia_on_chain
