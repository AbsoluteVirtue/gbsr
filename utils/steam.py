import asyncio

import valve.source
import valve.source.a2s
import valve.source.master_server


async def get_server_list_with_players(logger):
    result = []
    count = 0
    with valve.source.master_server.MasterServerQuerier(timeout=30.0) as msq:
        try:
            for address in msq.find(gamedir=u"groundbranch"):
                with valve.source.a2s.ServerQuerier(address) as server:
                    info = server.info()
                    players = server.players()

                s = info.values

                count += info.values['player_count']
                s.pop('server_type', None)
                s.pop('platform', None)

                p = []
                for player in sorted(players["players"],
                                     key=lambda k: k["duration"], reverse=True):
                    if player.values.get('name'):
                        p.append({
                            'index': player.values.get('index'),
                            'name': player.values['name'],
                            'score': player.values.get('score'),
                            'duration': player.values.get('duration')
                        })

                s.update(players=p)
                result.append(s)
                await asyncio.sleep(1)
        except valve.source.NoResponseError:
            logger.warning("Steam master query server request timed out.")

    return {'data': sorted(result, key=lambda k: k["player_count"], reverse=True), 'total_player_count': count}
