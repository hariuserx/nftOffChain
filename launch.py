import subprocess
import time
import csv
import threading
import sys
import os
#npx hardhat run scripts/interact.js --network ropsten

wd = os.getcwd()

class NFT:
    def __init__(self, n):
        self.N = n
        self.RTT_time = [0.0]*n
        self.on_chain_time = [0.0]*n
        self.transaction_result = [""]*n

    def mint_or_transfer_nft(self, from_address, to_address, nft_id, index, action):
        #RTT_time = []
        #start = [0.0]*10
        #on_chain_time =[]
        #transaction_result = []
        #for i in range(10):
        result = "Pass"
        start_time = time.time()
        p = None
        if action == "mint":
            print("Minting started")
            p = subprocess.Popen("node scripts/mint-nft-new.js".split(),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=wd+"/js/my-nft")
            #p.wait()
        elif action == "transfer":
            print("transfer started")
            p = subprocess.Popen(("node scripts/transfer-nft-new.js " + from_address + " " + to_address + " " + str(nft_id)).split(),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=wd+"/js/my-nft")
        out = p.stdout.read()
        out_err = p.stderr.read()
        print("time taken to complete " + str(index) + "th transaction", (time.time()-start_time)*1000, " ms")
        self.on_chain_time[index] = str((time.time()-start_time)*1000)
        print(out.decode("utf-8"))
        print(out_err.decode("utf-8"))
        #print(type(out.decode("utf-8")))
        if "$#$" in out.decode("utf-8"):
            self.RTT_time[index] = str(out.decode("utf-8").split("$#$")[1][1:-1])
        if "Transaction has been reverted by the EVM" in out_err.decode("utf-8"):
            result = "Fail"
            print("Transaction failed")
        self.transaction_result[index] = result


if __name__ == '__main__':
    n = 3
    myNFT = NFT(n)
    threads = []
    for i in range(n):
    #p = subprocess.Popen(['npx' , 'hardhat', 'run', 'scripts/interact.js --network ropsten'], stdout=subprocess.PIPE)
        #transfer_nft("0x358755b66dadcad3a0466f9a2ececc4d296d6964", "0x9a932e12B60cE08b891710e100Ed80bb0b2E63ba", 8).start()
        #dRecieved = connFile.readline()
        from_address = sys.argv[1]
        to_address = sys.argv[2]
        nft_id = int(sys.argv[3])
        processThread = threading.Thread(target=myNFT.mint_or_transfer_nft, args=[from_address, to_address, nft_id+i, i, "transfer"])  # <- 1 element list
        processThread.start()
        #time.sleep(30)
        threads.append(processThread)
    for i in range(len(threads)):
        threads[i].join()
    print(myNFT.RTT_time)
    print(myNFT.on_chain_time)
    print(myNFT.transaction_result)

    with open('stats_final_transfer.csv', 'a+', newline='') as outfile:
        header = ['RTT_time', 'on_chain_time', 'result']
        write = csv.DictWriter(outfile, fieldnames=header)
        write.writeheader()
        for i in range(n):
            #write = csv.writer(outfile)
            write.writerow({'RTT_time': myNFT.RTT_time[i], 'on_chain_time': myNFT.on_chain_time[i], 'result': myNFT.transaction_result[i]})
            #outfile.write(" ".join(RTT_time))
            #outfile.write("\n")
            #outfile.write(" ".join(on_chain_time))

#[763.7692170143127, 1950.4671800136566, 705.8138779401779, 858.222463965416, 586.9315050840378]