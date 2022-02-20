import base64
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee
from terra_sdk.util.contract import get_code_id, get_contract_address

terra = LCDClient(
    url = 'http://localhost:1317',
    chain_id = 'localterra',
    gas_prices = "0.5uluna",
    gas_adjustment = 1.4
)
mk1 = MnemonicKey(
    mnemonic = "notice oak worry limit wrap speak medal online prefer cluster roof addict wrist behave treat actual wasp year salad speed social layer crew genius"
)
mk2 = MnemonicKey(
    mnemonic = "quality vacuum heart guard buzz spike sight swarm shove special gym robust assume sudden deposit grid alcohol choice devote leader tilt noodle tide penalty"
)
deployer = terra.wallet(mk1)
deployer_addr = deployer.key.acc_address
test2 = terra.wallet(mk2)
test2_addr = test2.key.acc_address
#deployer = terra.wallets["test1"]

def store_contract(contract_name: str):
    contract_file = open(f"../artifacts/{contract_name}", "rb")
    file_bytes = base64.b64encode(contract_file.read()).decode()
    store_code = MsgStoreCode(deployer.key.acc_address, file_bytes)
    store_code_tx = deployer.create_and_sign_tx(CreateTxOptions(
        msgs=[store_code],
        memo="create contract",
        fee=Fee(4000000, "10000000uluna")
    ))
    store_code_tx_result = terra.tx.broadcast(store_code_tx)
    print(store_code_tx_result)

    #code_id = store_code_tx_result.logs[0].events_by_type["store_code"]["code_id"][0]
    code_id = get_code_id(store_code_tx_result)
    return code_id

def instantiate_contract(code_id: str, init_msg):
    instantiate = MsgInstantiateContract(
        sender = deployer.key.acc_address,
        admin = None,
        code_id = code_id,
        init_msg = init_msg,
        init_coins = {"uluna": 10000000},
    )
    instantiate_tx = deployer.create_and_sign_tx(CreateTxOptions(
        msgs=[instantiate],
        memo="instantiating contract",
        #gas_prices="1500uluna",
        fee=Fee(4000000, "10000000uluna")
    ))
    instantiate_tx_result = terra.tx.broadcast(instantiate_tx)
    print(instantiate_tx_result)

    contract_address = get_contract_address(instantiate_tx_result)
    return contract_address

def execute_contract(sender: str, contract_address: str, execute_msg):
    execute = MsgExecuteContract(
        sender = sender.key.acc_address,
        contract = contract_address,
        execute_msg = execute_msg
    )

    execute_tx = sender.create_and_sign_tx(CreateTxOptions(
        msgs=[execute],
        memo="execute contract",
        fee=Fee(4000000, "10000000uluna")
    ))
    execute_tx_result = terra.tx.broadcast(execute_tx)
    return execute_tx_result

def mint(signer, to, amount):
    """
    signer: the actual wallet of the contract caller
    to: address of
    """
    return execute_contract(signer, cw20_contract_address, {"mint": {"txSigner":signer.key.acc_address, "recipient":to.key.acc_address, "amount":amount}})

def transfer(signer, to, amount):
    return execute_contract(signer, cw20_contract_address, {"transfer":{"txSigner":signer.key.acc_address, "recipient":to.key.acc_address, "amount":amount}})


def balance(sender_address: str):
    bal = terra.wasm.contract_query(
        cw20_contract_address,
        {"balance": {"address": sender_address}}
    )
    return bal


# code_id = store_contract("nft2.wasm")
# contract_address = instantiate_contract(code_id, {"count": 5})

# print(code_id, contract_address)
# execute_contract(deployer, contract_address, {"increment": {}})
# execute_contract(deployer, contract_address, {"increment": {}})
# print(terra.wasm.contract_query(contract_address, { "get_count": {} }))

cw20_code_id = store_contract("cw20_base.wasm")
cw20_contract_address = instantiate_contract(
    cw20_code_id,
    {
        "name": "pog_token",
        "symbol": "POG",
        "decimals": 6,
        "initial_balances": [
            {
                "address": deployer_addr,
                "amount": "1000000"
            }
        ],
        "mint": {
            "minter": deployer_addr
        }
    })

print(cw20_code_id, cw20_contract_address)
print(balance(deployer_addr))

print(mint(deployer, test2, "100"))
print(balance(test2_addr))

print(transfer(test2, deployer, "50"))
print(balance(test2_addr))
print(balance(deployer_addr))

