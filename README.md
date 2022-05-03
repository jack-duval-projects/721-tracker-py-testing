# 721-tracker-py-testing

A 'proof-of-concept' repository, written in Python for the 721-tracker widget

## Installation

To be determined as development continues. 

Need access to OpenSea API, LooksRare API, Etherscan API with keys in a .env file

The following fields need to be set in your .env file:
```bash
ETHERSCAN_API_KEY=YOUR_KEY_HERE
OPENSEA_API_KEY=YOUR_KEY_HERE
HOT_ADDRESS=YOUR_HOT_WALLET_ADDRESS
COLD_ADDRESS=YOUR_COLD_WALLET_ADDRESS
```

See requirements.txt for a list of required packagaes


## Usage
Enter your address when prompted, after building
```bash
<<<<<<< HEAD
pip3 install -r requirements.txt
=======
pip install -r requirements.txt
>>>>>>> e5b85f1e9194d430edc086f2818f4ae8288cbaad
python3 setup.py
```
setup.py will call the tracker file's main with hot and cold wallet addresses from the .env file

## Contributing
At this time, contributions are informal. If you would like to make contributions, please feel free to do so! Also please email me - always curious to see what other people are building in the space :) 

jackcduval(at)gmail(dot)com

## License
[MIT](https://choosealicense.com/licenses/mit/)