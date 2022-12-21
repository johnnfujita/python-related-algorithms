from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage(account):
    simple_storage = SimpleStorage.deploy({"from": account})
    return simple_storage


def read_simple_storage(index=-1):
    return SimpleStorage[index]


def simple_storage_store(account, value):
    simple_storage = read_simple_storage()
    transaction = simple_storage.store(value, {"from": account})
    return transaction


def simple_storage_retrive():
    simple_storage = read_simple_storage()
    return simple_storage.retrieve()


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
        return account


def main():
    account = get_account()
    if len(SimpleStorage) < 1:
        simple_storage = deploy_simple_storage(account)
    else:
        simple_storage = read_simple_storage()

    stored_value = simple_storage_retrive()
    print(f"Contract {simple_storage} with stored value {stored_value}")
    transaction = simple_storage_store(account, stored_value + 1)
    transaction.wait(1)
    stored_value = simple_storage.retrieve()
    print(f"Contract {simple_storage} with stored value {stored_value}")


if __name__ == "__main__":
    main()
