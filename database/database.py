import logging
import time


class FakeDatabase:
    def __init__(self, data, data_ms_ia_on_chain):
        self.data = data
        self.data_ms_ia_on_chain = data_ms_ia_on_chain

    def is_owner(self, nft_id, owner_id):
        return self.data[nft_id][0].owner == owner_id

    def is_owner_on_chain_ms_ia(self, nft_id, owner_id):
        return self.data_ms_ia_on_chain[nft_id][0].owner == owner_id

    def update(self, nft_id, new_owner_id):
        self.data[nft_id][0].owner = new_owner_id
        logging.info("Finished Database update for nft %s with new owner %s", nft_id, new_owner_id)

    def update_on_chain_ms_ia(self, nft_id, new_owner_id):
        self.data_ms_ia_on_chain[nft_id][0].owner = new_owner_id
        logging.info("Finished Database update for nft %s with new owner %s", nft_id, new_owner_id)
