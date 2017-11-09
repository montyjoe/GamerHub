import requests
import json

def search_database(search):
    games = 'http://www.giantbomb.com/api/search?api_key=94df9c6218b439f9805399a8633b9cae74c4d00d&format=json&query='+str(search)+'&resources=game'
    json_data = requests.get(games).json()
    # json_data = requests.get(multi_search).json()
    try:
        errrors = json_data['errors'];
        final_list = []
        return final_list
    except:
        results = json_data['results']
        # newlist = sorted(results, key=lambda k: k['popularity'], reverse=True)
        final_list = []

        for result in results:
            data = {
            'name': result['name'],
            'game_id': result['giantbomb_id'],
            'cover_img': result['image']['original_url'],
            }
            final_list.append(data)

            # if result['media_type'] == "movie":

        return final_list

def add_game(id):
    game = 'https://www.giantbomb.com/api/game/'+id+'/?api_key=94df9c6218b439f9805399a8633b9cae74c4d00d'
    json_data = requests.get(game).json()
    # json_data = requests.get(multi_search).json()
    try:
        errrors = json_data['errors'];
        final_list = []
        return final_list
    except:
        results = json_data['results']
        # newlist = sorted(results, key=lambda k: k['popularity'], reverse=True)
        game_to_add = []

        for result in results:
            data = {
            'name': result['name'],
            "id": result['giantbomb_id'],
            "cover-img": result['image']['original_url'],
            "background-img": result['images']['original'],
            "description":result['description']
            }
            game_to_add.append(data)

            # if result['media_type'] == "movie":

        return game_to_add






# multi_search = 'https://api.twitch.tv/kraken/search/games?query=' + str(search)
# headers={'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': '2w5qsci3na5nzblfr60mcgju4g9zi9'}
# if search == 'battlefront':
#     search = 'star wars'
# game = 'https://api.twitch.tv/kraken/search/games?query='+str(search)
# r = requests.get(game, headers=headers)
# json_data = r.json()


    # end
