import base64
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract
from terra_sdk.core.bank import MsgSend
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee
from terra_sdk.util.contract import get_code_id, get_contract_address

from helpers import execute_contract, mint, transfer, balance
import json
import sys 

#args = [prog_name, price, restaurant]

if len(sys.argv) < 2:
    sys.exit('Needs price argument')

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
mk3 = MnemonicKey(
    mnemonic = "symbol force gallery make bulk round subway violin worry mixture penalty kingdom boring survey tool fringe patrol sausage hard admit remember broken alien absorb"
)
deployer = terra.wallet(mk1)
deployer_addr = deployer.key.acc_address
sender = terra.wallet(mk2)
sender_addr = sender.key.acc_address
restaurant = terra.wallet(mk3)
restaurant_addr = restaurant.key.acc_address

price = sys.argv[1]

addresses = None
with open("addresses.json", "r") as fp:
    addresses = json.load(fp)

cw20_contract_address = addresses["cw20"]["contract_address"]

# 1. Receive UST?
#price = 8.99 or something
print(balance(sender_addr, terra))
print("Sender Balance: " + balance(sender_addr, terra))
amt_uusd_str = str(int(float(price)*10e6))+"uusd"
print(amt_uusd_str)
receive_ust_msg = MsgSend(
    sender_addr,
    deployer_addr,
    amt_uusd_str
)
receive_ust_tx = sender.create_and_sign_tx(CreateTxOptions(
    msgs=[receive_ust_msg],
    memo="receive UST txn",
    fee=Fee(200000, "120000uusd")
))
receive_ust_tx_result = terra.tx.broadcast(receive_ust_tx)

# 2. Mint 1% of UST received as BAZ
fraction = int(float(price)*10e4)
mint(deployer, sender, fraction, terra)

print("Sender Balance: " + balance(sender_addr, terra))

# 3. Send UST to Restaurant's Wallet
send_ust_msg = MsgSend(
    deployer_addr,
    restaurant_addr,
    amt_uusd_str
)
send_ust_tx = sender.create_and_sign_tx(CreateTxOptions(
    msgs=[send_ust_msg],
    memo="send UST txn",
    fee=Fee(200000, "120000uusd")
))
send_ust_tx_result = terra.tx.broadcast(send_ust_tx)