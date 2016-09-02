import requests
import sys
import random

apikey = 'dc6zaTOxFJmzC'
hostid = 'http://api.giphy.com/v1/gifs/'


def getgif(giphy):
    '''
    Create a session to giphy
    '''
    getme = giphy[0].split()[0]
    url = "{0}search?q={1}&api_key={2}&rating=pg&offset=2".format(hostid, getme, apikey)
    session = requests.session()
    response = session.get(url)
    pullimg = random.choice(response.json()['data'])
    gifurl = pullimg['images']['original']['url']
    return gifurl


if __name__ == "__main__":

    giphy = sys.argv[1:]
    print getgif(giphy)
