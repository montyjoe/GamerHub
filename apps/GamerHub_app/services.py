import requests

def search_database(search):
    # multi_search = 'https://api.twitch.tv/kraken/search/games?query=' + str(search)
    headers={'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': '2w5qsci3na5nzblfr60mcgju4g9zi9'}
    game = 'https://api.twitch.tv/kraken/search/games?query='+str(search)
    r = requests.get(game, headers=headers)
    json_data = r.json()


    # json_data = requests.get(multi_search).json()

    try:
        errrors = json_data['errors'];
        final_list = []
        return final_list
    except:
        results = json_data['games']

        newlist = sorted(results, key=lambda k: k['popularity'], reverse=True)
        final_list = []

        for result in newlist:
            data = {
            'name': result['name'],
            "id": result['giantbomb_id'],
            "picture": result['box']['large'],
            }
            final_list.append(data)

            # if result['media_type'] == "movie":

        return final_list
