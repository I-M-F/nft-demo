from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time

def test_can_create_advanced_collectible_intergration():
    # deploy the contract
    # create an nft
    # get a random tribe back

    #Arrange 
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for intergration tetsing")
    #Act 
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(60)   

    #Assert
    assert advanced_collectible.tokenCounter() == 1
   