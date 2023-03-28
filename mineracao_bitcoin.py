import requests
import time
import tweepy

# Twitter API keys
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Get the latest block data
url_stats = "https://api.blockchair.com/bitcoin/stats"

url = "https://api.blockchair.com/bitcoin/blocks?limit=1"
response = requests.get(url).json()
block_data = response["data"][0]

# Loop indefinitely to check for new blocks every 5 minutes
while True:
   
    # Get the latest block data
    response = requests.get(url).json()
    new_block_data = response["data"][0]

    response_stats = requests.get(url_stats).json()
    stats_data = response_stats["data"]

    # Check if a new block has been mined
    if new_block_data["id"] != block_data["id"]:

        # Update the block data
        block_data = new_block_data

        # Get the relevant block information
        block = block_data["id"]
        block_time = block_data["time"]
        circulation = "{:,.0f}".format(stats_data["circulation"]/100000000)
        percent_mined = round(((stats_data["circulation"]/100000000)/21000000)*100, 2)
        btc_remaining = "{:,.0f}".format(21000000-(stats_data["circulation"]/100000000))
        percent_remaining = round(100-percent_mined, 2)
        guessed_miner = block_data["guessed_miner"]
        transaction_count = block_data["transaction_count"]
        fee_total = round(block_data["fee_total"]/100000000, 8)
        fee_total_usd = block_data["fee_total_usd"]
        avr_by_transaction = "{:,.8f}".format(fee_total/block_data["transaction_count"])
        avr_by_transaction_usd = round(block_data["fee_total_usd"]/block_data["transaction_count"], 2)
        generation = block_data["generation"]/100000000
        generation_usd = "{:,.2f}".format(block_data["generation_usd"])
        difficulty = "{:,.0f}".format(block_data["difficulty"])
        coinbase_data = block_data["coinbase_data_hex"]
        coinbase_data_string = bytes.fromhex(coinbase_data)
        coinbase_data_string = coinbase_data_string.decode("iso-8859-1")

        # Construct the tweet
        tweet = f'🚀 Novo bloco minerado! 🎉\n\n' \
             f'BTC in circulation: {circulation} of 21,000,000 ({percent_mined}%)\n' \
             f'BTC remaining: {btc_remaining} BTC ({percent_remaining}%)\n' \
             f'Block: {block}\n' \
             f'Time: {block_time}\n' \
             f'Miner: {guessed_miner}\n' \
             f'Number of transactions: {transaction_count}\n' \
             f'Total fee: {fee_total} BTC | {fee_total_usd} USD\n' \
             f'Average fee by transaction: {avr_by_transaction} BTC | {avr_by_transaction_usd} USD\n' \
             f'BTC genereted: {generation} BTC | {generation_usd} USD\n' \
             f'Difficulty: {difficulty}\n' \
             f'Coinbase data: {coinbase_data_string}'
        print(tweet)
        # Send the tweet
        # api.update_status(tweet) 
    # Wait for 5 minutes
    time.sleep(60)
