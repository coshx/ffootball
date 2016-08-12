import nfldb

def score_passers(scoring_config):
    score = {'passing': {}}
    passing_yds = get_passing_yards_for_single_season(2015)
    for qb in passing_yds:
        score['passing'][qb] = passing_yds[qb] / int(scoring_config['passing']['25PY'])
    return score

def get_top_players():
    """Gets fields from database and applies scoring."""
    passing_yds = get_passing_yards_for_single_season(2015)
    passing_tds = get_passing_tds_for_single_season(2015)

    rushing_yds = get_rushing_yards_for_single_season(2015)
    rushing_yds = get_rushing_tds_for_single_season(2015)

    receiving_yds = get_receiving_yards_for_single_season(2015)
    receiving_yds = get_receiving_tds_for_single_season(2015)



    # TODO: Implement scoring multiplication here
    return fantasy_scores

# def get_quarterbacks(year):
#     db = nfldb.connect()
#     q = nfldb.Query(db)
#     qbs = {}
#     q.game(season_year=year, season_type='Regular')
#     for team in q.
#     import pdb
#     pdb.set_trace()

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
        qbs[pp.player.full_name] = int(pp.passing_yds)
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
