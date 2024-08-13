#!/usr/bin/env python3
import sys
import json

def usage():
  print("./apply_rolls.py tiles.json board.json teams.json state.json rolls...")
  sys.exit(1)

def find_team_in_state(state, team_id):
    for t in state["teams"]:
        if t["id"] == team_id:
            return t
    return None

def find_team_def(teams, team_id):
    for i in teams:
        if i["id"] == team_id:
            return i
    return None

def find_tile_def(tiles, tile_id):
    for i in tiles:
        if i["id"] == tile_id:
            return i
    return None

def find_tile_name_on_board(tiles, board_tile):
    if board_tile["type"] == "special":
        return "special: %s" % board_tile["special"]
    if board_tile["type"] == "tile":
        tdef = find_tile_def(tiles, board_tile["tile"])
        return tdef["name"]
    return "???"

def find_owner_id(state, tile_id):
    for team in state["teams"]:
        if tile_id in team["owned"]:
            return team["id"]
    return None

def find_state_tile(state, tile_id):
    for i in state["tiles"]:
        if i["id"] == tile_id:
            return i
    return None

def find_revenue(board, tiles, state, tile_id):
    state_tile = find_state_tile(state, tile_id)
    tier = state_tile["tier"]
    sset = state_tile["set"]
    base_revenue = find_tile_def(tiles, tile_id)["revenue"]
    return base_revenue * sset * tier


def apply_roll(board, tiles, state, teams, team_id, roll):
    team = find_team_in_state(state, team_id)

    # determine where they'll land
    next_pos = (team["position"] + roll) % len(board)
    next_tile = board[next_pos]
    print("Team %s" % (
        find_team_def(teams, team["id"])["name"]))
    print("- Advanced to pos %d: %s" % (next_pos,
        find_tile_name_on_board(tiles, next_tile)))

    # Do coffer updates
    if next_tile["type"] == "tile":
        owning_team_id = find_owner_id(state, next_tile["tile"])
        owning_team = find_team_def(teams, owning_team_id)
        if owning_team is None:
            print("- Tile is not owned by anyone")
        else:
            print("- Tile is owned by %s" % owning_team["name"])
            # Find how much to pay them
            rev = find_revenue(board, tiles, state, next_tile["tile"])
            state["updates"].append({
                "type": "payment",
                "from": team_id,
                "to": owning_team_id,
                "amount": rev
            })
    print("")
    return state

def apply_rolls(board, tiles, state, teams, rolls):
    state["updates"] = []
    for i in range(0, len(rolls)):
        roll = int(rolls[i])
        team_id = state["teams"][i]["id"]
        state = apply_roll(board, tiles, state, teams, team_id, roll)

    process_updates(state, board, tiles, teams)

def process_updates(state, board, tiles, teams):
    for team in state["teams"]:
        tdef = find_team_def(teams, team["id"])
        print("Team %s coffer updates:" % tdef["name"])
        old_coffer = team["coffer"]
        for update in state["updates"]:
            if update["type"] == "payment":
                if update["to"] == team["id"]:
                    team["coffer"] += update["amount"]
                if update["from"] == team["id"]:
                    team["coffer"] -= update["amount"]
        print("Coffer: %d -> %d" % (old_coffer, team["coffer"]))


def main():
    tiles = json.load(open(sys.argv[1], "r"))
    board = json.load(open(sys.argv[2], "r"))
    teams = json.load(open(sys.argv[3], "r"))
    state = json.load(open(sys.argv[4], "r"))
    rolls = list(sys.argv[5:])
    apply_rolls(board, tiles, state, teams, rolls)

if __name__ == "__main__":
  main()
