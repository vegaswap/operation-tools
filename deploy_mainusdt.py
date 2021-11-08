from brownie import VegaToken, BoostPool, accounts, network, project
from brownie import web3
import toml

BSC_USDT = "0x55d398326f99059ff775485246999027b3197955"
VGA_CTR = "0x4EfDFe8fFAfF109451Fc306e0B529B088597dd8d"
LP_VGABBNB = "0xda6f484f5ffe2382c20f80dcedcb860cea955461"

from pathlib import Path

pool1 = "0x8634490eB5a8d7Db8Db82104aE73E2C84009592F"

def deploy():
    
    net = network.show_active()
    # network.disconnect()
    # network.connect("bscmain")
    if net == "bscmain":
        x = Path(Path.home(), ".chaindev/bsc_mainnet.toml")
        z = toml.load(x)
        accounts.add(z["PRIVATEKEY"])

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
        #_duration = hour * 6
        _duration = 7 * day
        f = 10 ** 18
        #TODO
        _maxYield = 300000 * f
        _maxTotalStake = 25000 * f
        # _stakeDecimals = 18
        # _yieldDecimals = 18
        _maxPerStake = 5000 * f
        #_minStake = 10 * f
        #TODO review: reward steps and stake steps have different length
        _rewardSteps = [20, 15, 12, 8, 5]
        xstep = 5000
        _stakeSteps = [xstep * f, (xstep*2) * f, (xstep*3) * f, (xstep*4) * f]
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

        #2pm
        _startTime = 1636354800

        #7pm
        #_startTime = 1636372800

        bpool = BoostPool.deploy(
            _startTime,
            _duration,
            _stakeToken,
            _yieldToken,
            _maxYield,
            _maxTotalStake,
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

def main():
