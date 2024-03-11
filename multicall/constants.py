import asyncio
import os
from enum import IntEnum
from typing import Dict

from aiohttp import ClientTimeout

# If brownie is installed and connected, we will use brownie's Web3
# Otherwise, we will use w3 from web3py.
try:
    from brownie import network, web3  # type: ignore

    if network.is_connected():
        w3 = web3
    else:
        from web3.auto import w3
except ImportError:
    from web3.auto import w3

GAS_LIMIT: int = int(os.environ.get("GAS_LIMIT", 50_000_000))

MULTICALL2_BYTECODE = '0x608060405234801561001057600080fd5b50600436106100b45760003560e01c806372425d9d1161007157806372425d9d1461013d57806386d516e814610145578063a8b0574e1461014d578063bce38bd714610162578063c3077fa914610182578063ee82ac5e14610195576100b4565b80630f28c97d146100b9578063252dba42146100d757806327e86d6e146100f8578063399542e91461010057806342cbb15c146101225780634d2301cc1461012a575b600080fd5b6100c16101a8565b6040516100ce919061083b565b60405180910390f35b6100ea6100e53660046106bb565b6101ac565b6040516100ce9291906108ba565b6100c1610340565b61011361010e3660046106f6565b610353565b6040516100ce93929190610922565b6100c161036b565b6100c161013836600461069a565b61036f565b6100c161037c565b6100c1610380565b610155610384565b6040516100ce9190610814565b6101756101703660046106f6565b610388565b6040516100ce9190610828565b6101136101903660046106bb565b610533565b6100c16101a3366004610748565b610550565b4290565b8051439060609067ffffffffffffffff8111156101d957634e487b7160e01b600052604160045260246000fd5b60405190808252806020026020018201604052801561020c57816020015b60608152602001906001900390816101f75790505b50905060005b835181101561033a5760008085838151811061023e57634e487b7160e01b600052603260045260246000fd5b6020026020010151600001516001600160a01b031686848151811061027357634e487b7160e01b600052603260045260246000fd5b60200260200101516020015160405161028c91906107f8565b6000604051808303816000865af19150503d80600081146102c9576040519150601f19603f3d011682016040523d82523d6000602084013e6102ce565b606091505b5091509150816102f95760405162461bcd60e51b81526004016102f090610885565b60405180910390fd5b8084848151811061031a57634e487b7160e01b600052603260045260246000fd5b602002602001018190525050508080610332906109c2565b915050610212565b50915091565b600061034d60014361097b565b40905090565b43804060606103628585610388565b90509250925092565b4390565b6001600160a01b03163190565b4490565b4590565b4190565b6060815167ffffffffffffffff8111156103b257634e487b7160e01b600052604160045260246000fd5b6040519080825280602002602001820160405280156103eb57816020015b6103d8610554565b8152602001906001900390816103d05790505b50905060005b825181101561052c5760008084838151811061041d57634e487b7160e01b600052603260045260246000fd5b6020026020010151600001516001600160a01b031685848151811061045257634e487b7160e01b600052603260045260246000fd5b60200260200101516020015160405161046b91906107f8565b6000604051808303816000865af19150503d80600081146104a8576040519150601f19603f3d011682016040523d82523d6000602084013e6104ad565b606091505b509150915085156104d557816104d55760405162461bcd60e51b81526004016102f090610844565b604051806040016040528083151581526020018281525084848151811061050c57634e487b7160e01b600052603260045260246000fd5b602002602001018190525050508080610524906109c2565b9150506103f1565b5092915050565b6000806060610543600185610353565b9196909550909350915050565b4090565b60408051808201909152600081526060602082015290565b80356001600160a01b038116811461058357600080fd5b919050565b600082601f830112610598578081fd5b8135602067ffffffffffffffff808311156105b5576105b56109f3565b6105c2828385020161094a565b83815282810190868401865b8681101561068c57813589016040601f198181848f030112156105ef578a8bfd5b6105f88261094a565b6106038a850161056c565b81528284013589811115610615578c8dfd5b8085019450508d603f850112610629578b8cfd5b898401358981111561063d5761063d6109f3565b61064d8b84601f8401160161094a565b92508083528e84828701011115610662578c8dfd5b808486018c85013782018a018c9052808a01919091528652505092850192908501906001016105ce565b509098975050505050505050565b6000602082840312156106ab578081fd5b6106b48261056c565b9392505050565b6000602082840312156106cc578081fd5b813567ffffffffffffffff8111156106e2578182fd5b6106ee84828501610588565b949350505050565b60008060408385031215610708578081fd5b82358015158114610717578182fd5b9150602083013567ffffffffffffffff811115610732578182fd5b61073e85828601610588565b9150509250929050565b600060208284031215610759578081fd5b5035919050565b60008282518085526020808601955080818302840101818601855b848110156107bf57858303601f19018952815180511515845284015160408585018190526107ab818601836107cc565b9a86019a945050509083019060010161077b565b5090979650505050505050565b600081518084526107e4816020860160208601610992565b601f01601f19169290920160200192915050565b6000825161080a818460208701610992565b9190910192915050565b6001600160a01b0391909116815260200190565b6000602082526106b46020830184610760565b90815260200190565b60208082526021908201527f4d756c746963616c6c32206167677265676174653a2063616c6c206661696c656040820152601960fa1b606082015260800190565b6020808252818101527f4d756c746963616c6c206167677265676174653a2063616c6c206661696c6564604082015260600190565b600060408201848352602060408185015281855180845260608601915060608382028701019350828701855b8281101561091457605f198887030184526109028683516107cc565b955092840192908401906001016108e6565b509398975050505050505050565b6000848252836020830152606060408301526109416060830184610760565b95945050505050565b604051601f8201601f1916810167ffffffffffffffff81118282101715610973576109736109f3565b604052919050565b60008282101561098d5761098d6109dd565b500390565b60005b838110156109ad578181015183820152602001610995565b838111156109bc576000848401525b50505050565b60006000198214156109d6576109d66109dd565b5060010190565b634e487b7160e01b600052601160045260246000fd5b634e487b7160e01b600052604160045260246000fdfea2646970667358221220c1152f751f29ece4d7bce5287ceafc8a153de9c2c633e3f21943a87d845bd83064736f6c63430008010033'
MULTICALL3_BYTECODE = '0x6080604052600436106100f35760003560e01c80634d2301cc1161008a578063a8b0574e11610059578063a8b0574e1461025a578063bce38bd714610275578063c3077fa914610288578063ee82ac5e1461029b57600080fd5b80634d2301cc146101ec57806372425d9d1461022157806382ad56cb1461023457806386d516e81461024757600080fd5b80633408e470116100c65780633408e47014610191578063399542e9146101a45780633e64a696146101c657806342cbb15c146101d957600080fd5b80630f28c97d146100f8578063174dea711461011a578063252dba421461013a57806327e86d6e1461015b575b600080fd5b34801561010457600080fd5b50425b6040519081526020015b60405180910390f35b61012d610128366004610a85565b6102ba565b6040516101119190610bbe565b61014d610148366004610a85565b6104ef565b604051610111929190610bd8565b34801561016757600080fd5b50437fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0140610107565b34801561019d57600080fd5b5046610107565b6101b76101b2366004610c60565b610690565b60405161011193929190610cba565b3480156101d257600080fd5b5048610107565b3480156101e557600080fd5b5043610107565b3480156101f857600080fd5b50610107610207366004610ce2565b73ffffffffffffffffffffffffffffffffffffffff163190565b34801561022d57600080fd5b5044610107565b61012d610242366004610a85565b6106ab565b34801561025357600080fd5b5045610107565b34801561026657600080fd5b50604051418152602001610111565b61012d610283366004610c60565b61085a565b6101b7610296366004610a85565b610a1a565b3480156102a757600080fd5b506101076102b6366004610d18565b4090565b60606000828067ffffffffffffffff8111156102d8576102d8610d31565b60405190808252806020026020018201604052801561031e57816020015b6040805180820190915260008152606060208201528152602001906001900390816102f65790505b5092503660005b8281101561047757600085828151811061034157610341610d60565b6020026020010151905087878381811061035d5761035d610d60565b905060200281019061036f9190610d8f565b6040810135958601959093506103886020850185610ce2565b73ffffffffffffffffffffffffffffffffffffffff16816103ac6060870187610dcd565b6040516103ba929190610e32565b60006040518083038185875af1925050503d80600081146103f7576040519150601f19603f3d011682016040523d82523d6000602084013e6103fc565b606091505b50602080850191909152901515808452908501351761046d577f08c379a000000000000000000000000000000000000000000000000000000000600052602060045260176024527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060445260846000fd5b5050600101610325565b508234146104e6576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601a60248201527f4d756c746963616c6c333a2076616c7565206d69736d6174636800000000000060448201526064015b60405180910390fd5b50505092915050565b436060828067ffffffffffffffff81111561050c5761050c610d31565b60405190808252806020026020018201604052801561053f57816020015b606081526020019060019003908161052a5790505b5091503660005b8281101561068657600087878381811061056257610562610d60565b90506020028101906105749190610e42565b92506105836020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff166105a66020850185610dcd565b6040516105b4929190610e32565b6000604051808303816000865af19150503d80600081146105f1576040519150601f19603f3d011682016040523d82523d6000602084013e6105f6565b606091505b5086848151811061060957610609610d60565b602090810291909101015290508061067d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601760248201527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060448201526064016104dd565b50600101610546565b5050509250929050565b43804060606106a086868661085a565b905093509350939050565b6060818067ffffffffffffffff8111156106c7576106c7610d31565b60405190808252806020026020018201604052801561070d57816020015b6040805180820190915260008152606060208201528152602001906001900390816106e55790505b5091503660005b828110156104e657600084828151811061073057610730610d60565b6020026020010151905086868381811061074c5761074c610d60565b905060200281019061075e9190610e76565b925061076d6020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff166107906040850185610dcd565b60405161079e929190610e32565b6000604051808303816000865af19150503d80600081146107db576040519150601f19603f3d011682016040523d82523d6000602084013e6107e0565b606091505b506020808401919091529015158083529084013517610851577f08c379a000000000000000000000000000000000000000000000000000000000600052602060045260176024527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060445260646000fd5b50600101610714565b6060818067ffffffffffffffff81111561087657610876610d31565b6040519080825280602002602001820160405280156108bc57816020015b6040805180820190915260008152606060208201528152602001906001900390816108945790505b5091503660005b82811015610a105760008482815181106108df576108df610d60565b602002602001015190508686838181106108fb576108fb610d60565b905060200281019061090d9190610e42565b925061091c6020840184610ce2565b73ffffffffffffffffffffffffffffffffffffffff1661093f6020850185610dcd565b60405161094d929190610e32565b6000604051808303816000865af19150503d806000811461098a576040519150601f19603f3d011682016040523d82523d6000602084013e61098f565b606091505b506020830152151581528715610a07578051610a07576040517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152601760248201527f4d756c746963616c6c333a2063616c6c206661696c656400000000000000000060448201526064016104dd565b506001016108c3565b5050509392505050565b6000806060610a2b60018686610690565b919790965090945092505050565b60008083601f840112610a4b57600080fd5b50813567ffffffffffffffff811115610a6357600080fd5b6020830191508360208260051b8501011115610a7e57600080fd5b9250929050565b60008060208385031215610a9857600080fd5b823567ffffffffffffffff811115610aaf57600080fd5b610abb85828601610a39565b90969095509350505050565b6000815180845260005b81811015610aed57602081850181015186830182015201610ad1565b81811115610aff576000602083870101525b50601f017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0169290920160200192915050565b600082825180855260208086019550808260051b84010181860160005b84811015610bb1578583037fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe001895281518051151584528401516040858501819052610b9d81860183610ac7565b9a86019a9450505090830190600101610b4f565b5090979650505050505050565b602081526000610bd16020830184610b32565b9392505050565b600060408201848352602060408185015281855180845260608601915060608160051b870101935082870160005b82811015610c52577fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa0888703018452610c40868351610ac7565b95509284019290840190600101610c06565b509398975050505050505050565b600080600060408486031215610c7557600080fd5b83358015158114610c8557600080fd5b9250602084013567ffffffffffffffff811115610ca157600080fd5b610cad86828701610a39565b9497909650939450505050565b838152826020820152606060408201526000610cd96060830184610b32565b95945050505050565b600060208284031215610cf457600080fd5b813573ffffffffffffffffffffffffffffffffffffffff81168114610bd157600080fd5b600060208284031215610d2a57600080fd5b5035919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff81833603018112610dc357600080fd5b9190910192915050565b60008083357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe1843603018112610e0257600080fd5b83018035915067ffffffffffffffff821115610e1d57600080fd5b602001915036819003821315610a7e57600080fd5b8183823760009101908152919050565b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc1833603018112610dc357600080fd5b600082357fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa1833603018112610dc357600080fdfea2646970667358221220bb2b5c71a328032f97c676ae39a1ec2148d3e5d6f73d95e9b17910152d61f16264736f6c634300080c0033'
# ordered by chain id for easy extension
class Network(IntEnum):
    Mainnet = 1
    Ropsten = 3
    Rinkeby = 4
    Gorli = 5
    Optimism = 10
    CostonTestnet = 16
    ThundercoreTestnet = 18
    SongbirdCanaryNetwork = 19
    Cronos = 25
    RSK = 30
    RSKTestnet = 31
    Kovan = 42
    Bsc = 56
    OKC = 66
    OptimismKovan = 69
    BscTestnet = 97
    Gnosis = 100
    Velas = 106
    Thundercore = 108
    Coston2Testnet = 114
    Fuse = 122
    Heco = 128
    Polygon = 137
    Fantom = 250
    Boba = 288
    KCC = 321
    OptimismGorli = 420
    Astar = 592
    Metis = 1088
    Moonbeam = 1284
    Moonriver = 1285
    MoonbaseAlphaTestnet = 1287
    Milkomeda = 2001
    Kava = 2222
    KavaTestnet = 2221
    Neon = 245022934
    NeonTestnet = 245022926
    Scroll = 534352
    ScrollSepolia = 534351
    FantomTestnet = 4002
    Canto = 7700
    Klaytn = 8217
    Base = 8453
    EvmosTestnet = 9000
    Evmos = 9001
    Arbitrum = 42161
    Celo = 42220
    Oasis = 42262
    AvalancheFuji = 43113
    Avax = 43114
    GodwokenTestnet = 71401
    Godwoken = 71402
    Mumbai = 80001
    ArbitrumRinkeby = 421611
    ArbitrumGorli = 421613
    Sepolia = 11155111
    Aurora = 1313161554
    Harmony = 1666600000
    PulseChain = 369
    PulseChainTestnet = 943

MULTICALL_ADDRESSES: Dict[int,str] = {
    Network.Mainnet: '0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441',
    Network.Kovan: '0x2cc8688C5f75E365aaEEb4ea8D6a480405A48D2A',
    Network.Rinkeby: '0x42Ad527de7d4e9d9d011aC45B31D8551f8Fe9821',
    Network.Gorli: '0x77dCa2C955b15e9dE4dbBCf1246B4B85b651e50e',
    Network.Gnosis: '0xb5b692a88BDFc81ca69dcB1d924f59f0413A602a',
    Network.Polygon: '0x95028E5B8a734bb7E2071F96De89BABe75be9C8E',
    Network.Bsc: '0x1Ee38d535d541c55C9dae27B12edf090C608E6Fb',
    Network.Fantom: '0xb828C456600857abd4ed6C32FAcc607bD0464F4F',
    Network.Heco: '0xc9a9F768ebD123A00B52e7A0E590df2e9E998707',
    Network.Harmony: '0xFE4980f62D708c2A84D3929859Ea226340759320',
    Network.Cronos: '0x5e954f5972EC6BFc7dECd75779F10d848230345F',
    Network.Optimism: '0x187C0F98FEF80E87880Db50241D40551eDd027Bf',
    Network.OptimismKovan: '0x2DC0E2aa608532Da689e89e237dF582B783E552C',
    Network.Kava: "0x7ED7bBd8C454a1B0D9EdD939c45a81A03c20131C",
    Network.KavaTestnet: "0x1Af096bFA8e495c2F5Eeb56141E7E2420066Cf78",
    Network.Neon: "",
    Network.NeonTestnet: "0xcFC8002c27985410F7a5Df76f418E5F1a460e1eb",
    Network.Scroll: "",
    Network.ScrollSepolia: "0xA17786896F1b5CF22600925cB680998cae8401f5"
}

MULTICALL2_ADDRESSES: Dict[int,str] = {
    Network.Mainnet: '0x5ba1e12693dc8f9c48aad8770482f4739beed696',
    Network.Kovan: '0x5ba1e12693dc8f9c48aad8770482f4739beed696',
    Network.Rinkeby: '0x5ba1e12693dc8f9c48aad8770482f4739beed696',
    Network.Gorli: '0x5ba1e12693dc8f9c48aad8770482f4739beed696',
    Network.Gnosis: '0x9903f30c1469d8A2f415D4E8184C93BD26992573',
    Network.Polygon: '0xc8E51042792d7405184DfCa245F2d27B94D013b6',
    Network.Bsc: '0xfF6FD90A470Aaa0c1B8A54681746b07AcdFedc9B',
    Network.Fantom: '0xBAD2B082e2212DE4B065F636CA4e5e0717623d18',
    Network.Moonriver: '0xB44a9B6905aF7c801311e8F4E76932ee959c663C',
    Network.Arbitrum: '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2',
    Network.Avax: '0xdf2122931FEb939FB8Cf4e67Ea752D1125e18858',
    Network.Heco: '0xd1F3BE686D64e1EA33fcF64980b65847aA43D79C',
    Network.Aurora: '0xe0e3887b158F7F9c80c835a61ED809389BC08d1b',
    Network.Cronos: '0x5e954f5972EC6BFc7dECd75779F10d848230345F',
    Network.Optimism: '0x2DC0E2aa608532Da689e89e237dF582B783E552C',
    Network.OptimismKovan: '0x2DC0E2aa608532Da689e89e237dF582B783E552C',
    Network.Kava: '0x45be772faE4a9F31401dfF4738E5DC7DD439aC0b',
}

# based on https://github.com/mds1/multicall#readme
MULTICALL3_ADDRESSES: Dict[int,str] = {
    Network.Mainnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Ropsten: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Rinkeby: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Gorli: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Optimism: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.CostonTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.ThundercoreTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.SongbirdCanaryNetwork: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Cronos: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.RSK: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.RSKTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Kovan: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Bsc: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.OKC: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.OptimismKovan: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.BscTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Gnosis: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Velas: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Thundercore: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Coston2Testnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Fuse: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Heco: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Polygon: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Fantom: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Boba: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.KCC: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.OptimismGorli: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Astar: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Metis: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Moonbeam: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Moonriver: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.MoonbaseAlphaTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Milkomeda: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.FantomTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Canto: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Klaytn: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.EvmosTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Evmos: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Arbitrum: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Celo: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Oasis: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.AvalancheFuji: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Avax: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.GodwokenTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Godwoken: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Mumbai: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.ArbitrumRinkeby: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.ArbitrumGorli: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Sepolia: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Aurora: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Harmony: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.PulseChain: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.PulseChainTestnet: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Base: '0xcA11bde05977b3631167028862bE2a173976CA11',
    Network.Kava: "0x30A62aA52Fa099C4B227869EB6aeaDEda054d121",
    Network.Neon: "",
    Network.NeonTestnet: "0x25ca3395E673DEDd37345639F65D011844931f1C",
    Network.Scroll: "0xcA11bde05977b3631167028862bE2a173976CA11",
    Network.ScrollSepolia: "0xcA11bde05977b3631167028862bE2a173976CA11"
}

# With default AsyncBaseProvider settings, some dense calls will fail
#   due to aiohttp.TimeoutError where they would otherwise succeed.
AIOHTTP_TIMEOUT = ClientTimeout(int(os.environ.get("AIOHTTP_TIMEOUT", 30)))

# Parallelism
user_choice = max(1, int(os.environ.get("MULTICALL_PROCESSES", 1)))
parallelism_capacity = max(1, os.cpu_count() - 1)
NUM_PROCESSES = min(user_choice, parallelism_capacity)

NO_STATE_OVERRIDE = [ Network.Gnosis, Network.Harmony, Network.Moonbeam, Network.Moonriver, Network.Kovan, Network.Fuse ]

# NOTE: If we run too many async calls at once, we'll have memory issues.
#       Feel free to increase this with the "MULTICALL_CALL_SEMAPHORE" env var if you know what you're doing.
ASYNC_SEMAPHORE = int(os.environ.get("MULTICALL_CALL_SEMAPHORE", 1000))
