from brownie import VegaToken, BoostPool, accounts, network, project
from brownie import web3
import toml

BSC_USDT = "0x55d398326f99059ff775485246999027b3197955"
VGA_CTR = "0x4EfDFe8fFAfF109451Fc306e0B529B088597dd8d"
LP_VGABBNB = "0xda6f484f5ffe2382c20f80dcedcb860cea955461"

yuri = "0x337f8365689d587391B32d4CC428Ca1540F3a4f9"
# vga2 = "0x0B4a10c19bC8bB925F6D53dF906aFF97fD0530f8"

# usdt.transfer(yuri, 100 * 10**usdt_dec, {"from": mainaccount})
from pathlib import Path


def main():
    # requires brownie account to have been created
    net = network.show_active()
    # network.disconnect()
    # network.connect("bscmain")
    if net == "bscmain":
        # add these accounts to metamask by importing private key

        x = Path(Path.home(), ".chaindev/bsc_mainnet.toml")
        z = toml.load(x)
        accounts.add(z["PRIVATEKEY"])
        # # owner = accounts[0]
        mainaccount = accounts[0]
        print(mainaccount)

        vega = VegaToken.at(VGA_CTR)
        bv = vega.balanceOf(mainaccount)
        print("Vega ", bv / 10 ** 18)

        usdt = VegaToken.at(BSC_USDT)
        b = usdt.balanceOf(mainaccount)
        usdt_dec = 18
        print("USDT balance ", b / 10 ** usdt_dec)

        bnb = network.web3.eth.get_balance(mainaccount.address)
        print(bnb / 10 ** 18)

        _stakeToken = BSC_USDT
        _yieldToken = VGA_CTR
        hour = 60*60
        day = 24 * hour
        _duration = hour * 6
        f = 10 ** 18
        _maxYield = 4000 * f
        _maxTotalStake = 500 * f
        _stakeDecimals = 18
        _yieldDecimals = 18
        _maxPerStake = 1000 * f
        _minStake = 10 * f
        _rewardSteps = [15, 11, 8, 6, 4]        
        _stakeSteps = [100 * f, 200 * f, 300 * f, 400 * f] 
        rewardQuote = 1

        i = 0
        totalr = 0
        for x in _stakeSteps:
            r = _rewardSteps[i]
            rw = r * x
            print(rw)
            i+=1
            totalr += rw
        print("total ", totalr/10**18)

        bpool = BoostPool.deploy(
            _stakeToken,
            _yieldToken,
            _duration,
            _maxYield,
            _maxTotalStake,
            _stakeDecimals,
            _yieldDecimals,
            _maxPerStake,
            #$_minStake,
            _rewardSteps,
            _stakeSteps,
            rewardQuote,
            {"from": mainaccount},
        )
        print(bpool)

        # print("deployed pool", bpool)
        # bpool.activateStaking({"from": accounts[0]})
        # bpool.setReward(15,{"from": accounts[0]})

        # boostpool.stake(1000, 30, {"from": accounts[0]})
