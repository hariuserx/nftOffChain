def print_nft_data(database):
    data = database.data

    print("----------------NFT DATA -----------------")

    for _, value in data.items():
        nft_data = value[0]
        print(str(nft_data.nft_id) + " " + nft_data.owner)

    print("---------------- END -----------------")


