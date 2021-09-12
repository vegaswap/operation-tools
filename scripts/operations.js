import { duration, EIGHTEEN_DECS, getContext, latest } from "../utils";
import { ethers, network } from "hardhat";
import * as fs from "fs";
import { plainToClass, Transform } from "class-transformer";
import { BigNumber } from "ethers";

const csv = require("csv-parser");
const IERC20ABI = require("../build/abi/IERC20.json");

const VegaBucketABI = require("../custom_abis/VegaBucket.json");
const VegaTokenABI = require("../custom_abis/VegaToken.json");
const VegaBucketByteCode = fs.readFileSync(
  "./custom_abis/VegaBucket.bytecode",
  "utf8"
);
const VegaTokenByteCode = fs.readFileSync(
  "./custom_abis/VegaToken.bytecode",
  "utf8"
);

const CONFIG = {
  bscmainnet: {
    vegaTokenAddr: "0x4EfDFe8fFAfF109451Fc306e0B529B088597dd8d",
    deployedBucketAddresses: {
      Advisors: "0x4d91BaCD3F2CC3BCB18F0027381C7F1c44363C88",
      Development: "0x1dAA4943280C85be711A6bDbACb7b73c66601B6d",
      Ecosystem: "0x45f96c234140350182E33bDc83A649C27feF8369",
      LP_grants: "0x680052c12D864f7FD61673261453dE63732Fb102",
      LP_rewards: "0x13C4168962A3c1DFe02f8eD9591d8EDd28f3E047",
      Marketing: "0xed223E325006699418b9965458cB2c6D5bd08533",
      Private: "0x4464B3917d9A249ff99D8Aa89E5a35D373Af2305",
      Public_Vested: "0xB4df471B6509a1078a799a4f49CaB97e719d7Ab5",
      Seed: "0xAD558B957010B6C75463E883B109Dc9322Faa06f",
      Team: "0x3e632E8A689407a397f5713c6A581CC56410Ed7E",
      Trade_Mining: "0xD7a8B70c101A03b59d160abC18205191c9415070",
      Treasury: "0x69BC0fB381c0E5b030D72b33C3C311BCb6d8ceD5",
      Vega_Liquidity: "0x3A486587c0f5dbf18166FA7e470AfC9c2Ba73555",
    },
  },
};

const localNetwork = ["localhost", "hardhat", "bsctestnet"];

function getContractFactories(owner) {
  const Bucket = new ethers.ContractFactory(
    VegaBucketABI,
    VegaBucketByteCode,
    owner
  );
  const Token = new ethers.ContractFactory(
    VegaTokenABI,
    VegaTokenByteCode,
    owner
  );
  return {
    Bucket,
    Token,
  };
}

async function getBucketInfo(bucket) {
  const claimStats = {};
  const bucketTotalClaimAmount = await bucket.totalClaimAmount();

  for (let i = 0; i < 100; i++) {
    const claimAddr = await bucket.claim_addresses(i);
    if (claimAddr === "0x0000000000000000000000000000000000000000") {
      break;
    }
    const claim = await bucket.claims(claimAddr);
    claimStats[claim.claimAddress] = {
      totalClaim: claim.claimTotalAmount.toString(),
      claimPercentage: claim.claimTotalAmount
        .mul(100)
        .div(bucketTotalClaimAmount)
        .toString(),
    };
  }
  const res = {
    name: await bucket.name(),
    deployedAddress: bucket.address,
    openClaimAmount: await bucket.openClaimAmount(),
    totalClaimAmount: bucketTotalClaimAmount,
    totalAmount: await bucket.totalAmount(),
    cliffTime: await bucket.cliffTime(),
    numPeriods: await bucket.numPeriods(),
    period: await bucket.period(),
    claimStats,
  };

  // check list of claims
  console.log({
    name: res.name,
    deployedAddress: res.deployedAddress,
    openClaimAmount: res.openClaimAmount.toString(),
    totalClaimAmount: res.totalClaimAmount.toString(),
    totalAmount: res.totalAmount.toString(),
    cliffTime: res.cliffTime.toString(),
    numPeriods: res.numPeriods,
    claimStats,
  });
  return res;
}

async function info() {
  const { accounts } = await getContext();
  const [owner] = accounts;
  const { vegaTokenAddr, deployedBucketAddresses } = getConfig();
  const { Bucket, Token } = getContractFactories(owner);
  const token = await Token.attach(vegaTokenAddr);
  let totalTokenInBucket = BigNumber.from(0);

  const totalSupply = await token.totalSupply();
  const leftoverTokenBalance = await token.balanceOf(
    "0x3dd34225f14423fd3592c52634c1fc974e04f5c0"
  );

  getBuckets(async (mapOfBuckets) => {
    for (const deployedBucketAddressesKey in deployedBucketAddresses) {
      const bucket = mapOfBuckets[deployedBucketAddressesKey];
      const deployedAddr = deployedBucketAddresses[deployedBucketAddressesKey];
      const deployedBucket = await Bucket.attach(deployedAddr);
      const stat = await getBucketInfo(deployedBucket);
      totalTokenInBucket = totalTokenInBucket.add(stat.totalAmount);
    }

    const left = totalSupply.sub(totalTokenInBucket).sub(leftoverTokenBalance);

    console.log("token left over balance", leftoverTokenBalance.toString());
    console.log("all bucket balance", totalTokenInBucket.toString());
    console.log("left", left.toString());
  });
}

async function main() {
  await info();
}
main();
