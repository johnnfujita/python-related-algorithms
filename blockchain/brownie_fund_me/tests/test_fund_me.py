from scripts.deploy import get_account, deploy_fund_me
from brownie import FundMe
from scripts.fund_and_withdraw import fund, withdraw


def test_can_fund():
    account = get_account()
    deploy_fund_me()
    tx = fund()
    tx.wait(1)
    # address to amount funded not unit tested maybe not needed
    assert (
        FundMe[-1].addressToAmountFunded(account.address) == FundMe[-1].getEntranceFee()
    )


# this test is dependent on the previous test... it is not a good pratice to do not unmount after each test
# this is a kind of weid integration test in two steps
def test_can_withdraw():
    account = get_account()

    tx = withdraw()
    # entrance_fee not unit tested
    tx.wait(1)
    assert FundMe[-1].addressToAmountFunded(account.address) == 0
