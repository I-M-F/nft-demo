from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_tribe


tribe_to_image_uri = {
    "SOUTHERN": "https://ipfs.io/ipfs/Qme25KUHexhW49Vkx95qDboxgTBV4bSZzLxEfX9DHt6PpS?filename=southern.png",
    "NORTHERN": "https://ipfs.io/ipfs/QmRMVbN8fqmedvbqAKcCxvDWPXqSycgA68sCeQbmBsXkhj?filename=northern.png",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    no_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {no_of_collectibles} tokenIds")
    for token_id in range(no_of_collectibles):
        tribe = get_tribe(advanced_collectible.tokenIdToTribe(token_id))
        # check if token uri its set
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, tribe_to_image_uri[tribe])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome ;-) you can your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("20 min wait period ")
