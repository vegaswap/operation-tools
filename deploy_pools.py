from brownie import VegaToken, BoostPool, accounts, network, project
from brownie import web3

BSC_USDT = "0x55d398326f99059ff775485246999027b3197955"
VGA_CTR = "0x4EfDFe8fFAfF109451Fc306e0B529B088597dd8d"

from pathlib import Path
import os

#TODO review: reward steps and stake steps have different length

hour = 60*60
day = 24 * hour
f = 10 ** 18
start7pm = 1636372800

def deploy_usdt(mainaccount):    
    
    _stakeToken = BSC_USDT
    _yieldToken = VGA_CTR
    _duration = 7 * day
    _maxYield = 300000 * f
    _maxTotalStake = 25000 * f
    _maxPerStake = 1000 * f
    _rewardSteps = [20, 15, 12, 8, 5]
    xstep = 5000
    _stakeSteps = [xstep * f, (xstep*2) * f, (xstep*3) * f, (xstep*4) * f]
    rewardQuote = 1
    _startTime = start7pm

    bpool = BoostPool.deploy(
        _startTime,
        _duration,
        _stakeToken,
        _yieldToken,
        _maxYield,
        _maxTotalStake,
        _maxPerStake,
        _rewardSteps,
        _stakeSteps,
        rewardQuote,
        {"from": mainaccount},
    )
    print(bpool)    
    print("deployed USDT pool", bpool)


def deploy_vga(mainaccount):
    
    vega = VegaToken.at(VGA_CTR)
    bv = vega.balanceOf(mainaccount)
    print("Vega ", bv / 10 ** 18)

    usdt = VegaToken.at(BSC_USDT)
    b = usdt.balanceOf(mainaccount)
    usdt_dec = 18
    print("USDT balance ", b / 10 ** usdt_dec)

    bnb = network.web3.eth.get_balance(mainaccount.address)
    print(bnb / 10 ** 18)

    _stakeToken = VGA_CTR
    _yieldToken = VGA_CTR
    _duration = 7 * day
    _maxYield = 325000 * f
    _maxTotalStake = 2500000 * f
    _maxPerStake = 5000 * f
    _rewardSteps = [20, 15, 12, 8, 5]
    xstep = 500000
    _stakeSteps = [xstep * f, (xstep*2) * f, (xstep*3) * f, (xstep*4) * f]
    rewardQuote = 100
    _startTime = start7pm

    bpool = BoostPool.deploy(
        _startTime,
        _duration,
        _stakeToken,
        _yieldToken,
        _maxYield,
        _maxTotalStake,
        _maxPerStake,
        _rewardSteps,
        _stakeSteps,
        rewardQuote,
        {"from": mainaccount},
    )
    print("deployed VGA pool", bpool)

def main():

    net = network.show_active()
    # network.disconnect()
    # network.connect("bscmain")
    if net == "bscmain":    
        accounts.add(os.environ["PRIVKEY"])
        mainaccount = accounts[0]
        print(mainaccount)

        # deploy_usdt(mainaccount)
        # deploy_vga(mainaccount)




