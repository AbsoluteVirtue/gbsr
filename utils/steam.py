import valve.source
import valve.source.a2s
import valve.source.master_server


def get_server_list_with_players():
    result = []
    with valve.source.master_server.MasterServerQuerier() as msq:
        try:
            for address in msq.find(gamedir=u"groundbranch"):
                with valve.source.a2s.ServerQuerier(address) as server:
                    info = server.info()
                    players = server.players()
                # print("{player_count}/{max_players} {server_name}".format(**info))
                s = info.values
                s.pop('server_type', None)
                s.pop('platform', None)
                p = []
                for player in sorted(players["players"],
                                     key=lambda p: p["duration"], reverse=True):
                    # print("{index} {name}".format(**player))
                    p.append({
                        'index': player.values.get('index'),
                        'name': player.values.get('name'),
                        'score': player.values.get('score'),
                        'duration': player.values.get('duration')
                    })
                s.update(players=p)
                result.append(s)
        except valve.source.NoResponseError:
            print("Master server request timed out!")

    return result
