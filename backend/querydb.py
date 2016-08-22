import nfldb
import json

from collections import defaultdict

def get_scores(scoring_config, years):
    """Returns a dictionary of players and their scores at each position.

    Example: {'passing': {'Josh McCown': 111, ...}, ...}
    """
    score = {}
    # TODO: Rename 'passing', 'rushing', ... to the actual position.
    score['passing'] = score_players(scoring_config, 'QB', years)
    score['rushing'] = score_players(scoring_config, 'RB', years)
    score['receiving'] = score_players(scoring_config, 'WR', years)
    score['kicking'] = score_players(scoring_config, 'K', years)
    with open('scores.json', 'w') as fp:
        json.dump(score, fp)

    return score


def get_players_by_position(position, years):
    """Returns a dictionary of {player_id: player_name} for a position."""
    players = {}

    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=years, season_type='Regular').player(position=position)
    for player in q.as_players():
        players[player.player_id] = player.full_name
    return players


def get_player_detail_stats(player_id, years):
    """Returns a dictionary of {stat: value, ...} over a year."""
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=years, season_type='Regular').player(player_id=player_id)
    ## Odd for loop. Returns immediately b/c 1 player per id.
    for stats in q.as_aggregate():
        return stats


def score_players(scoring_config, position, years):
    """Returns a fantasy score over a time period.

    Example: {'Josh McCown': 111}
    """
    scores = defaultdict(int)
    players = get_players_by_position(position, years)

    db = nfldb.connect()

    # Passing, Rushing, Receiving
    for p in players:
        stats = get_player_detail_stats(p, years)
        try:
            # Points from passing
            scores[players[p]] += int(stats.passing_yds) / int(scoring_config['passing']['25PY'])
            scores[players[p]] += int(stats.passing_tds) * int(scoring_config['passing']['TD-pass'])
            scores[players[p]] += int(stats.passing_twoptm) * int(scoring_config['passing']['2pt-thrown'])
            scores[players[p]] += int(stats.passing_int) * int(scoring_config['passing']['interception-thrown'])

            # Points from rushing
            scores[players[p]] += int(stats.rushing_yds) / int(scoring_config['rushing']['10RY'])
            scores[players[p]] += int(stats.rushing_tds) * int(scoring_config['rushing']['TD-rush'])
            scores[players[p]] += int(stats.rushing_twoptm) * int(scoring_config['rushing']['2pt-rush'])

            # Points from receiving
            scores[players[p]] += int(stats.receiving_yds) / int(scoring_config['receiving']['10RecY'])
            scores[players[p]] += int(stats.receiving_tds) * int(scoring_config['receiving']['TD-rec'])
            scores[players[p]] += int(stats.receiving_twoptm) * int(scoring_config['receiving']['2pt-rec'])

            # Points from miscellaneous
            scores[players[p]] += int(stats.fumbles_rec_tds) * int(scoring_config['miscellaneous']['fr-td'])
            scores[players[p]] += int(stats.kickret_tds) * int(scoring_config['miscellaneous']['kickoff-td'])
            scores[players[p]] += int(stats.fumbles_lost) * int(scoring_config['miscellaneous']['fumble'])
            scores[players[p]] += int(stats.puntret_tds) * int(scoring_config['miscellaneous']['punt-td'])
            # Points from kicking
            scores[players[p]] += int(stats.kicking_xpmade) * int(scoring_config['kicking']['made-PAT'])
            scores[players[p]] += int(stats.kicking_xpmissed) * int(scoring_config['kicking']['missed-PAT'])
            scores[players[p]] += score_fg_39(p, years) * int(scoring_config['kicking']['fg-39'])
            scores[players[p]] += score_fg_49(p, years) * int(scoring_config['kicking']['fg-49'])
            scores[players[p]] += score_fg_50(p, years) * int(scoring_config['kicking']['fg-50'])
        except:
            continue
    return scores


def score_fg_39(player_id, years):
    """Returns number of field goals under 40 yards."""
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')
    return len([pp for pp in q.player(player_id=player_id).play_player(kicking_fgm_yds__lt=40).as_plays()])


def score_fg_49(player_id, years):
    """Returns number of field goals gte 40 yards and lt 50 yards."""
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')
    return len([pp for pp in q.player(player_id=player_id).play_player(kicking_fgm_yds__gte=40, kicking_fgm_yds__lt=50).as_plays()])


def score_fg_50(player_id, years):
    """Returns number of field goals gte 50 yards."""
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(season_year=2015, season_type='Regular')
    return len([pp for pp in q.player(player_id=player_id).play_player(kicking_fgm_yds__gte=50).as_plays()])


if __name__ == "__main__":
    scoring_config = {"kicking":
                      {"fg-39": "3",
                       "fg-49": "4",
                       "fg-50": "5",
                       "made-PAT": "1",
                       "missed-PAT": "-1"},
                      "miscellaneous":
                      {"fr-td": "6",
                       "fumble": "-2",
                       "kickoff-td": "6",
                       "punt-td": "6"},
                      "passing":
                      {"2pt-thrown": "2",
                       "25PY": "25",
                       "TD-pass": "4",
                       "interception-thrown": "-2"},
                      "receiving":
                      {"2pt-rec": "2",
                       "10RecY": "10",
                       "TD-rec": "6"},
                      "rushing":
                      {"2pt-rush": "2",
                       "10RY": "10",
                       "TD-rush": "6"}}

    score_players(scoring_config, 2015, "WR")
