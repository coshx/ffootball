import nfldb

from collections import defaultdict

def get_scores(scoring_config):
    score = {}
    score['passing'] = score_players(scoring_config, 2015, 'QB')
    score['rushing'] = score_players(scoring_config, 2015, 'RB')
    score['receiving'] = score_players(scoring_config, 2015, 'WR')

    return score

def score_players(scoring_config, year, position):
    scores = defaultdict(int)

    db = nfldb.connect()
    players = get_players_by_position(position)

    # Passing
    for p in players:
        q = nfldb.Query(db).game(season_year=year, season_type='Regular')
        for pp in q.play_player(player_id=p).as_aggregate():
            # Points from passing
            scores[players[p]] += int(pp.passing_yds) / int(scoring_config['passing']['25PY'])
            scores[players[p]] += int(pp.passing_tds) * int(scoring_config['passing']['TD-pass'])
            scores[players[p]] += int(pp.passing_twoptm) * int(scoring_config['passing']['2pt-thrown'])
            scores[players[p]] += int(pp.passing_int) * int(scoring_config['passing']['interception-thrown'])

            # Points from rushing
            scores[players[p]] += int(pp.rushing_yds) / int(scoring_config['rushing']['10RY'])
            scores[players[p]] += int(pp.rushing_tds) * int(scoring_config['rushing']['TD-rush'])
            scores[players[p]] += int(pp.rushing_twoptm) * int(scoring_config['rushing']['2pt-rush'])

            # Points from receiving
            scores[players[p]] += int(pp.receiving_yds) / int(scoring_config['receiving']['10RecY'])
            scores[players[p]] += int(pp.receiving_tds) * int(scoring_config['receiving']['TD-rec'])
            scores[players[p]] += int(pp.receiving_twoptm) * int(scoring_config['receiving']['2pt-rec'])

            # Points from kicking
            # scores[players[p]] += int(pp.kicking_xpmade) * int(scoring_config['kicking']['made-PAT'])

            # Points from miscellaneous
            scores[players[p]] += int(pp.fumbles_rec_tds) * int(scoring_config['miscellaneous']['fr-td'])
            scores[players[p]] += int(pp.kickret_tds) * int(scoring_config['miscellaneous']['kickoff-td'])
            scores[players[p]] += int(pp.fumbles_lost) * int(scoring_config['miscellaneous']['fumble'])
            scores[players[p]] += int(pp.puntret_tds) * int(scoring_config['miscellaneous']['punt-td'])


    return scores

def get_players_by_position(pos):
    """Returns a dict of up to 200 players in a position.

    Dictionary format is {'player_id': 'full_name'}"""
    positions = {'QB': 'passing_yds',
                 'RB': 'rushing_yds',
                 'WR': 'receiving_yds'}
    db = nfldb.connect()
    q = nfldb.Query(db)
    players = {}
    q.player(position=pos)
    for pp in q.sort(positions[pos]).limit(200).as_aggregate():
        players[pp.player.player_id] = pp.player.full_name
    return players

'''Passing stats...'''
def get_passing_yards_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    qbs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('passing_yds').limit(100).as_aggregate():
        qbs[pp.player.full_name] = int(pp.passing_yds)
    return qbs

def get_passing_tds_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    qbs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('passing_tds').limit(100).as_aggregate():
        qbs[pp.player.full_name] = int(pp.passing_tds)
    return qbs


'''Rushing stats...'''
def get_rushing_yards_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    rbs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('rushing_yds').limit(100).as_aggregate():
        rbs[pp.player.full_name] = int(pp.rushing_yds)
    return rbs

def get_rushing_tds_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    rbs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('rushing_tds').limit(100).as_aggregate():
        rbs[pp.player.full_name] = int(pp.rushing_yds)
    return rbs

'''Receiving stats...'''
def get_receiving_yards_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    wrs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('receiving_yards').limit(100).as_aggregate():
        wrs[pp.player.full_name] = int(pp.passing_yds)
    return wrs

def get_receiving_tds_for_single_season(year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    wrs = {}
    q.game(season_year=year, season_type='Regular')
    for pp in q.sort('receiving_tds').limit(100).as_aggregate():
        wrs[pp.player.full_name] = int(pp.passing_yds)
    return wrs

'''Multiple years...'''
def get_passing_yards_for_multiple_years(start, end):
    db = nfldb.connect()
    q = nfldb.Query(db)
    total_passing_yards = {}
    cursor = start
    while cursor < end:
        if len(total_passing_yards) == 0:
            qb_stats = get_passing_yards_for_single_season(cursor)
            total_passing_yards = dict(total_passing_yards.items() + qb_stats.items())
            cursor += 1
        else:
            qb_stats = get_passing_yards_for_single_season(cursor)
            total_passing_yards = { k: total_passing_yards.get(k, 0) + qb_stats.get(k, 0) for k in set(total_passing_yards) | set(qb_stats)}
            cursor += 1
    return total_passing_yards

def get_rushing_yards_for_multiple_years(start, end):
    db = nfldb.connect()
    q = nfldb.Query(db)
    total_rushing_yards = {}
    cursor = start
    while cursor < end:
        if len(total_rushing_yards) == 0:
            qb_stats = get_rushing_yards_for_single_season(cursor)
            total_rushing_yards = dict(total_rushing_yards.items() + qb_stats.items())
            cursor += 1
        else:
            qb_stats = get_rushing_yards_for_single_season(cursor)
            total_rushing_yards = { k: total_rushing_yards.get(k, 0) + qb_stats.get(k, 0) for k in set(total_rushing_yards) | set(qb_stats)}
            cursor += 1
    return total_rushing_yards


if __name__ == "__main__":
    pass
