import tweepy
from dotenv import load_dotenv
import os
import time
import webbrowser


def apiAuthenticaion():
    load_dotenv()
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    try:
        redirect_url = auth.get_authorization_url()
        webbrowser.open(redirect_url)
        print("Your web browser has been redirected to this link to authorize the script: "+redirect_url)
        verifier = input('enter the PIN you just received: ').strip()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    
    auth.get_access_token(verifier)
    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def getfollowers(api):
    followers = []
    for page in tweepy.Cursor(api.get_followers,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers

def getfriends(api):
    friends=[]
    for page in tweepy.Cursor(api.get_friends,count=200).pages():
        try:
            friends.extend(page)
        except tweepy.TweepError as e:
            print('Going to sleep:',e)
            time.sleep(60)
    return friends

def getnonfollowing(followers,friends):
    nonfollowing=[]
    for follower in followers:
        if(follower not in friends):
            nonfollowing.append(follower)
    return nonfollowing



def run():
    api=apiAuthenticaion()
    print("authentication successful!")
    followers=getfollowers(api)
    print("fetched your list of followers")
    friends=getfriends(api)
    print("fetched your list of friends")
    nonfollowing=getnonfollowing(followers,friends)
    print("fetched accounts you don't follow")
    while True:
        print("Would you like to start the process of going incognito? this will result in removing {} accounts from your followers, it will also take a while, press y to continue and n to exit.\n".format(len(nonfollowing)))
        decision=input('y/n: ').lower()
        if decision =='y':
            while True:
                confirm=input("You're sure you want to proceed? this action is irreversible! press y to confirm, n to exit: ").lower()
                if confirm=='y':
                    for follower in nonfollowing:   
                        api.create_block(user_id=follower.id)                     
                        print("blocked"+follower.screen_name +' https://twitter.com/'+follower.screen_name)
                        time.sleep(5)
                        api.destroy_block(user_id=follower.id)
                        time.sleep(5)
                    print("We're done here, good luck with your private life")        
                elif confirm=='n':
                    exit()
                else:
                    print("That sounds like wrong input, try again.")
        elif decision=='n':
            exit()
        else:
            print("That sounds like wrong input, try again.")
            

if __name__ == '__main__':
    run()