import tweepy
import csv
import time
import sys

# Replace with your API keys
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object with rate limit-handling // 15 calls every 15 minutes, and 180 calls every 15 minutes
api = tweepy.API(auth, wait_on_rate_limit=True)

# Get User ID
user = api.verify_credentials()
source_id = user.id

# Define limit-handling function
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TooManyRequests:
            	time.sleep(15 * 60)

# Get total number of friends
total_friends = user.friends_count
print(f"Total friends: {total_friends}")

# Init mutual followers and start time
mutual_followers = []
start_time = time.time()

try:
    for i, friend in enumerate(limit_handled(tweepy.Cursor(api.get_friends).items())):
        target_id = friend.id
        relationship = api.get_friendship(source_id=source_id, target_id=target_id)

        if relationship[0].followed_by:
            if friend not in mutual_followers:
                mutual_followers.append(friend)
                print(f"{i} - Follower added: {friend.name}")
        else:
            print(f"{i} - User does not follow you: {friend.name}")

        # Write mutual follower data to CSV every 100 followers
        if i % 100 == 0 and i > 0:
            with open('mutual_followers.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for follower in mutual_followers[-100:]:
                    writer.writerow([follower.name, follower.location, follower.description, f"https://twitter.com/{follower.screen_name}"])
                # Flush the data to the file
                file.flush()

                # Print elapsed time and create log file at the end of each iteration
                end_time = time.time()
                elapsed_time = end_time - start_time
                with open('logs.txt', 'a', encoding='utf-8') as file:
                    file.write(f"Iteration {i}: Elapsed time: {elapsed_time:.2f} seconds.\n")

except KeyboardInterrupt:
    # Handle keyboard interrupt by printing elapsed time and creating final log file
    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"Program canceled. Elapsed time: {elapsed_time:.2f} seconds.")
    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(f"Program canceled. Elapsed time: {elapsed_time:.2f} seconds.\n")
    sys.exit()

except StopIteration:
    # Handle reaching the end of the friend list
    file.write(f"End of the friend list. Elapsed time: {elapsed_time:.2f} seconds.\n")
    pass
