require("dotenv").config()
const API_URL = process.env.API_URL

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
const web3 = createAlchemyWeb3(API_URL)

const contract = require("../artifacts/contracts/MyNFT.sol/MyNFT.json")
const contractAddress = "0x7318E15158a836f537B64bae13A607e199eC097D"
const nftContract = new web3.eth.Contract(contract.abi, contractAddress)

async function getOwnerOf(tokenId) {
  const owner = await nftContract.methods.ownerOf(tokenId).call();
  return owner
}

module.exports = { getOwnerOf };