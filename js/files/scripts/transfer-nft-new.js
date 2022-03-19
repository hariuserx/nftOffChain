require("dotenv").config()
const API_URL = process.env.API_URL
const PUBLIC_KEY = process.env.PUBLIC_KEY
const PRIVATE_KEY = process.env.PRIVATE_KEY

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
const { performance } = require('perf_hooks')
const web3 = createAlchemyWeb3(API_URL)

const contract = require("../artifacts/contracts/MyNFT.sol/MyNFT.json")
const contractAddress = "0x7318E15158a836f537B64bae13A607e199eC097D"
//const contractAddress = "0x7318E15158a836f537B64bae13A607e199eC097D"
const nftContract = new web3.eth.Contract(contract.abi, contractAddress)
//hari: 0x9a932e12B60cE08b891710e100Ed80bb0b2E63ba
//vineeth: 0x358755b66dadcad3a0466f9a2ececc4d296d6964
async function transferNFT(from_address, to_address, nft_id) {
console.log("came hereZZZZ")
  const nonce = await web3.eth.getTransactionCount(PUBLIC_KEY, "latest") //get latest nonce
  //const accountNonce = '0x' + (web3.eth.getTransactionCount(PUBLIC_KEY) + 1).toString(16)
  console.log("came here")
  //the transaction
  const tx = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    data: nftContract.methods.safeTransferFrom(PUBLIC_KEY, to_address, nft_id).encodeABI(),
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
console.log(PUBLIC_KEY, process.argv[2], process.argv[3], process.argv[4])
transferNFT(process.argv[2], process.argv[3], process.argv[4])