require("dotenv").config()
const API_URL = process.env.API_URL
const PUBLIC_KEY = process.env.PUBLIC_KEY
const PRIVATE_KEY = process.env.PRIVATE_KEY

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
const { performance } = require('perf_hooks')
const web3 = createAlchemyWeb3(API_URL)

const contract = require("../artifacts/contracts/MyNFT.sol/MyNFT.json")
const contractAddress = "0x7318E15158a836f537B64bae13A607e199eC097D"
const nftContract = new web3.eth.Contract(contract.abi, contractAddress)

async function mintNFT(tokenURI) {
    console.log("came here 1")
  const nonce = await web3.eth.getTransactionCount(PUBLIC_KEY, "latest") //get latest nonce
   console.log("came here 2", nonce)
  //the transaction
  const tx = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    //maxPriorityFeePerGas: 50000000000,
    data: nftContract.methods.mintNFT(PUBLIC_KEY, tokenURI).encodeABI(),
  }
  var startTime = performance.now()
  const signPromise = web3.eth.accounts.signTransaction(tx, PRIVATE_KEY)
  signPromise
    .then((signedTx) => {
      web3.eth.sendSignedTransaction(
        signedTx.rawTransaction,
        function (err, hash) {
          if (!err) {
            console.log(
              "The hash of your transaction is: ",
              hash,
              "\nCheck Alchemy's Mempool to view the status of your transaction!"
            )
            console.log("Call to mintNFT took $#$", performance.now() - startTime, "$#$ milliseconds")
          } else {
            console.log(
              "Something went wrong when submitting your transaction:",
              err
            )
          }
        }
      )
    })
    .catch((err) => {
      console.log("Promise failed:", err)
    })
}

mintNFT(
  "https://gateway.pinata.cloud/ipfs/QmXLdWoG8HLEm3EVe6Eu1Enrx2Bdm6BEPaZqYdDzncmi2C"
)
