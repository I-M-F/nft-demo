// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

// An NFT Contract
// Where the tokenURI can be one of 3 different imgs
// Randomly selected

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Tribe {
        NORTHERN,
        SOUTHERN
    }
    mapping(uint256 => Tribe) public tokenIdToTribe;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester); 
    event tribeAssigned(uint256 indexed tokenID, Tribe tribe);

    //Double Inherited constructor
    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Maasai Worrior", "MWR")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Tribe tribe = Tribe(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToTribe[newTokenId] = tribe;
        emit tribeAssigned(newTokenId, tribe);
        address owner = requestIdToSender[requestId];
        //Working with in-flight CHainlink VRF requests
        _safeMint(owner, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);

    }
}
