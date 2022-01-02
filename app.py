from flask import Flask, request, jsonify
from my_spotify import MySpotify, Artist

app = Flask(__name__)


@app.route("/api", methods=['GET'])
def hello_world():
    print(request.args, '\n'*100)
    query = str(request.args['query'])
    action = str(request.args['action'])

    if action == 'image':
        d = {}
        d['image'] = Artist(query).artist_image
        return d

    else:
        my_spotify_obj = MySpotify()
        return my_spotify_obj.search_query(query)


if __name__ == "__main__":
    app.run()
