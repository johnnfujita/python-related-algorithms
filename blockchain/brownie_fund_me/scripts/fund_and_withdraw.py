from brownie import FundMe
from brownie.network import account
from scripts.deploy import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print("Funding")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    return tx


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    tx = fund_me.withdraw({"from": account})
    return tx


def main():
    fund()
    withdraw()


if __name__ == "__main__":
    main()
