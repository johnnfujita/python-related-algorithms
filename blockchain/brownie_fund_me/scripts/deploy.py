from brownie import FundMe, accounts, config, network, MockV3Aggregator


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_PRICE = 400000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
        return account


def deploy_mocks():
    account = get_account()
    print(f"we are at the {network.show_active()}")

    if len(MockV3Aggregator) <= 0:
        print("Deploying mocks...")

        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
        print("Mocks deployed")
    else:
        print("Mocks already available in this network")


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"]["rinkeby"]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fund_me.address}")


def main():

    deploy_fund_me()


if __name__ == "__main__":
    main()
