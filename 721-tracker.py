from dotenv import dotenv_values
import requests
import json
import time

config = dotenv_values(".env")
api_key = config["ETHERSCAN_API_KEY"]
os_api_key = config["OPENSEA_API_KEY"]
hot_addr = config["HOT_ADDRESS"]
cold_addr = config["COLD_ADDRESS"]

def json_print(json_obj):
    try: 
        ret = json.dumps(json_obj, sort_keys=True, indent=2)
        print(ret)
        return
    
    except:
        print("Argument isn't a JSON interpretable object")
        return


def get_wei_balance(address):
    req_url = "https://api.etherscan.io/api?module=account&action=balance&address=" + address + "&tag=latest&apikey=" + api_key

    response = requests.get(req_url)
    if response.status_code == 200:
        #json_print(response.json())
        return response.json()["result"]
    
    else:
        print("Error retrieving collection wei balance from Etherscan API")
        return 0

def get_token_balance(token_address, wallet_address): 
    req_url = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + token_address + "&address=" + wallet_address + "&tag=latest&apikey=" + api_key

    response = requests.get(req_url)
    
    if response.status_code == 200: 
        #json_print(response.json())
        return response.json()["result"]
    
    else:
        print("Error retrieving token balance from Etherscan API")

def get_incoming_721_transactions(wallet_address):
    req_url = "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + wallet_address + "&page=1&offset=100&startblock=0&endblock=27025780&sort=asc&apikey=" + api_key

    response = requests.get(req_url)
    ret_list = []

    if response.status_code != 200:
        print("Error retrieving transactions balance from Etherscan API")
        return ret_list

    try:
        tx_list = response.json()["result"]
    except:
        print("Unable to access to result from transaction")
        return[]

    for tx in tx_list:
        try:
            to = tx["to"].lower()
            if to == wallet_address.lower():
            #json_print(tx)
                ret_list.append(tx)

        except:
            print("Unable to access to address from transaction")
            continue

        
    
    return ret_list

def get_held_721_contracts(transactions, walletAddress):
    held_721_tokens = {}

    for tx in transactions:
        try:
            contractAddress = str(tx["contractAddress"])
        except:
            print("Unable to access contract address from transaction")
            continue

        qty = int(get_token_balance(contractAddress, walletAddress))
        if (qty > 0 and not contractAddress in held_721_tokens.keys()):
            held_721_tokens[contractAddress] = qty

    #json_print(held_721_tokens) 
    return held_721_tokens

def get_collection_slug(contract_address):
    req_url = "https://api.opensea.io/api/v1/asset_contract/" + contract_address

    headers = {"X-API-KEY": os_api_key}

    response = requests.get(req_url, headers=headers)

    if response.status_code == 200:
        #print(response.json()["collection"]["slug"])
        return response.json()["collection"]["slug"]
    
    else:
        print("Error retrieving collection slug from OpenSea API")
        return ""

def get_floorprice(url_slug):
    if url_slug == "":
        return -1.0
    
    req_url = "https://api.opensea.io/api/v1/collection/" + url_slug + "/stats"

    headers = {
        "Accept": "application/json",
        "X-API-KEY": os_api_key
    }

    response = requests.get(req_url, headers=headers)

    if response.status_code == 200:
        try:
            #print(response.json()["stats"]["floor_price"])
            return response.json()["stats"]["floor_price"]
        except:
            print("Error accessing floor_price element from stats")
            return -1.0
    
    else:
        print("Error retrieving collection stats from OpenSea API")
        return -1.0


def get_contract_address_to_floor_price(contract_addresses):

    contract_address_to_fp = {}

    for adr in contract_addresses:
        slug = get_collection_slug(adr)
        fp = get_floorprice(slug)

        if (fp == -1.0):
            continue

        contract_address_to_fp[adr] = fp
        time.sleep(0.255)
    
    return contract_address_to_fp

def get_portolio_value(held_contract_addresses_to_qtys, contract_addresses_to_fp):
    total = 0

    for contract_adr in held_contract_addresses_to_qtys.keys():
        try:
            total += held_contract_addresses_to_qtys[contract_adr] * contract_addresses_to_fp[contract_adr]
        
        except:
            continue
    
    return total

def convert_eth_usd(eth_amt):
    req_url = "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=" + api_key


    response = requests.get(req_url)
    if (response.status_code != 200):
        return 0.0

    try:
        eth_usd = float(response.json()["result"]["ethusd"])
    except:
        print("Error retrieving 'ethusd' from Etherscan API")
        eth_usd = 0

    return eth_amt * eth_usd

def convert_wei_eth(wei_amt):
    return int(wei_amt) / (10 ** 18)

if __name__ == "__main__":
    hot_wei_amt = get_wei_balance(hot_addr)
    hot_eth_amt = convert_wei_eth(hot_wei_amt)

    cold_wei_amt = get_wei_balance(cold_addr)
    cold_eth_amt = convert_wei_eth(cold_wei_amt)

    print("Hot wallet wei amount: " + str(hot_wei_amt))
    print("Hot wallet eth amount: " + str(hot_eth_amt))

    print("Cold wallet wei amount: " + str(cold_wei_amt))
    print("Cold wallet eth amount: " + str(cold_eth_amt))

    in_721_list = get_incoming_721_transactions(cold_addr)
    held_721_tokens_and_qtys = get_held_721_contracts(in_721_list, cold_addr)
    
    contract_address_to_floor_price_dict = get_contract_address_to_floor_price(held_721_tokens_and_qtys.keys())

    final_portfolio_value = get_portolio_value(held_721_tokens_and_qtys, contract_address_to_floor_price_dict)

    usd_value = convert_eth_usd(final_portfolio_value)

    print("ETH Portfolio Value: " + str(final_portfolio_value))
    print("USD Portfolio Value: " + str(usd_value))