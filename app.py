from flask import Flask, request, jsonify
from my_spotify import MySpotify, Artist, Album

app = Flask(__name__)


@app.route("/api", methods=['GET'])
def api_query():
    query = str(request.args['query'])
    action = str(request.args['action'])

    max_tries = 3

    if action == 'image':
        d = {}
        d['image'] = Artist(query).artist_image
        return d

    elif action == 'album':
        albumDic = {}

        trial = 0

        while trial < max_tries:
            try:
                album = Album(query)
                albumDic['tracks']  = album.tracks
                albumDic['album']   = album.album
            except:
                trial += 1

        return albumDic

    else:
        my_spotify_obj = MySpotify()
        return my_spotify_obj.search_query(query)




if __name__ == "__main__":
    app.run()
