import random
from types import SimpleNamespace

from . import strrand


_server = {
    "info": {
        "values": {
            "server_name": "",
            "map": "",
            "player_count": 0,
            "max_players": 0,
            "vac_enabled": True,
            "password_protected": True,
        }
    },
    "players": [],
}


def _gen_server_list():
    for _ in range(1, 100):
        k = random.random()
        _server["info"]["values"]["server_name"] = strrand(18)
        _server["info"]["values"]["map"] = strrand(6)
        _server["info"]["values"]["player_count"] = int(k * 100)
        _server["info"]["values"]["max_players"] = 16
        _server["info"]["values"]["vac_enabled"] = k > 0.5 or False
        _server["info"]["values"]["password_protected"] = k > 0.5 or True
        __players = []
        for j in range(0, int(k * 100)):
            __players.append({
                "values": {
                    "index": str(j),
                    "name": strrand(8),
                    "score": int(k * j * 1000),
                    "duration": j,
                },
            })

        _server["players"] = __players
        yield SimpleNamespace(**_server)


async def get_server_list_with_players(logger):
    result = []
    count = 0

    for server in _gen_server_list():
        s = server.info.values

        count += s['player_count']
        p = []
        for player in server.players:
            p.append({
                'index': player.values.get('index'),
                'name': player.values['name'],
                'score': player.values.get('score'),
                'duration': player.values.get('duration')
            })

        s.update(players=p)
        result.append(s)

    return {'data': sorted(result, key=lambda k: k["player_count"], reverse=True), 'total_player_count': count}
