import random

from . import strrand


def _gen_server_list():
    for _ in range(1, 100):
        k = random.random()
        _server = {
            "info": {
                "values": {
                    "server_name": strrand(18),
                    "map": strrand(6),
                    "player_count": int(k * 100),
                    "max_players": 99,
                    "vac_enabled": k > 0.2,
                    "password_protected": k < 0.5,
                }
            },
            "players": [],
        }

        for j in range(0, int(k * 100)):
            _server["players"].append({
                "values": {
                    "index": str(j),
                    "name": strrand(8),
                    "score": int(k * j * 1000),
                    "duration": j,
                },
            })

        yield _server


async def get_server_list_with_players(logger):
    result = []
    count = 0

    for server in _gen_server_list():
        s = server["info"]["values"]

        count += s['player_count']
        p = []
        for player in server.get("players", []):
            p.append({
                'index': player["values"].get('index'),
                'name': player["values"]['name'],
                'score': player["values"].get('score'),
                'duration': player["values"].get('duration')
            })

        s.update(players=p)
        result.append(s)

    return {'data': sorted(result, key=lambda k: k["player_count"], reverse=True), 'total_player_count': count}
