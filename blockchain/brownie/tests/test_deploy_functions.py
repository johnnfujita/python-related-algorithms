from brownie import accounts, SimpleStorage, config
from scripts import deploy


def test_deploy_simple_storage():
    account = deploy.get_account()
    simple_storage, stored_value = deploy.deploy_simple_storage(account)
    expected_value = 0
    assert expected_value == stored_value


def test_integration():
    account = deploy.get_account()
    simple_storage, stored_value = deploy.deploy_simple_storage(account)
    print(f"Contract {simple_storage} with stored value {stored_value}")
    transaction = deploy.simple_storage_store(simple_storage, account, 15)
    transaction.wait(1)
    stored_value = simple_storage.retrieve()
    print(f"Contract {simple_storage} with stored value {stored_value}")
    expected_value = 15
    assert stored_value == expected_value
