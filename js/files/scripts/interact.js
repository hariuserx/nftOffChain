console.log("Welcome to you NFT transaction APP\n")

const readline = require('readline');
const { mintNFT } = require('./mint-nft');
const { getOwnerOf } = require('./ownership');

// No need of concurrency control. There is just one thread. Thanks Node.
var counter = 1;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

var data = {
    // format: order, tokenID, fromAddress, toAddress, status, on-chain-status
    transactions: {},
    // format: tokenID : walletAddress
    userNFTData: {}
}

var waitForUserInput = function () {
    rl.question("Command: ", function (answer) {

        console.log("You have entered: " + answer)
        const splits = answer.split(" ");

        if (splits[0] == 'mint') {
            mintNFT(splits[1])
            console.log("Sent the minting transaction")
            waitForUserInput();
        }
        else if (splits[0] == 'transfer') {
            const fromAddress = splits[1]
            const toAddress = splits[2]
            const tokenID = parseInt(splits[3])

            if (data.userNFTData[tokenID] == fromAddress) {
                data.userNFTData[tokenID] = toAddress;
                data.transactions[counter] = {
                    "tokenID": tokenID,
                    "fromAddress": fromAddress,
                    "toAddress": toAddress,
                    "status": "success",
                }
            }

            counter++;

        }
        else if (answer == "init") {

            (async () => {
                console.log('starting initialization');

                for (let i = 1; i <= 8; i++) {
                    const owner = await getOwnerOf(i);
                    console.log("Owner of " + i + " is " + owner)
                    data.userNFTData[i] = owner;
                }

                console.log('finished initialization. Data is %j', data);
            })();
            waitForUserInput();
        }
        else if (answer == "exit") {
            rl.close();
        } else {
            waitForUserInput();
        }
    });
}

waitForUserInput()


rl.on('close', function () {
    console.log('\nBYE BYE !!!');
    process.exit(0);
});

