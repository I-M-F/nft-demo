from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    # deploy the contract
    # create an nft
    # get a random tribe back

    #Arrange 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local tetsing")
    #Act 
    advanced_collectible, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    random_no = 777
    get_contract("vrf_coordinator").callBackWithRandomness(requestId, random_no, advanced_collectible.address, {"from": get_account()})
    #Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToTribe(0) == random_no % 3