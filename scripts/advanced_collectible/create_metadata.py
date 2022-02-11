import json, os, requests
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadata_template
from scripts.helpful_scripts import get_tribe
from pathlib import Path


tribe_to_image_uri = {
    "SOUTHERN": "https://ipfs.io/ipfs/Qme25KUHexhW49Vkx95qDboxgTBV4bSZzLxEfX9DHt6PpS?filename=southern.png",
    "NORTHERN": "https://ipfs.io/ipfs/QmRMVbN8fqmedvbqAKcCxvDWPXqSycgA68sCeQbmBsXkhj?filename=northern.png",

}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"You  have created {number_of_advanced_collectible} collectibles!")
    for token_id in range(number_of_advanced_collectible):
        tribe = get_tribe(advanced_collectible.tokenIdToTribe(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{tribe}.json"
        )
        print(metadata_file_name)
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name} ")
            collectible_metadata["name"] = tribe
            collectible_metadata["description"] = f"An adorable {tribe} maasai girl"
            print(collectible_metadata)
            image_path = "./img/" + tribe.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else tribe_to_image_uri[tribe]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
