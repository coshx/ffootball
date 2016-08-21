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
    print score['passing']
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
    """Returns a dictionary of {player_id: {stat: value}}"""
    player = {}

    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=years, season_type='Regular').player(player_id=player_id)
    for p in q.as_aggregate():
        player[player_id] = p
    return player


def score_players(scoring_config, position, years):
    """Returns a fantasy score over a time period.

    Example: {'Josh McCown': 111}
    """
    scores = defaultdict(int)
    players = get_players_by_position(position, years)

    db = nfldb.connect()

    # Passing, Rushing, Receiving
    for p in players:
        q = nfldb.Query(db).game(season_year=years, season_type='Regular')
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

            # Points from miscellaneous
            scores[players[p]] += int(pp.fumbles_rec_tds) * int(scoring_config['miscellaneous']['fr-td'])
            scores[players[p]] += int(pp.kickret_tds) * int(scoring_config['miscellaneous']['kickoff-td'])
            scores[players[p]] += int(pp.fumbles_lost) * int(scoring_config['miscellaneous']['fumble'])
            scores[players[p]] += int(pp.puntret_tds) * int(scoring_config['miscellaneous']['punt-td'])
            # Points from kicking
            # scores[players[p]] += int(pp.kicking_xpmade) * int(scoring_config['kicking']['made-PAT'])
            # scores[players[p]] += int(pp.kicking_xpmissed) * int(scoring_config['kicking']['missed-PAT'])
            # scores[players[p]] += int(pp.kicking_fgm_yds) * int(scoring_config['kicking']['fg-39'])
            # scores[players[p]] += int(pp.kicking_fgm_yds) * int(scoring_config['kicking']['fg-49'])
            # scores[players[p]] += int(pp.kicking_fgm_yds) * int(scoring_config['kicking']['fg-50']
    return scores


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
