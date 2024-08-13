#!/usr/bin/env python3
import sys
import json

# Tool to visualize a board while testing

def usage():
  print("./visusalize_board.py tiles.json board.json")
  sys.exit(1)

def find_tile(tiles, tile_id):
  for _t in tiles:
    if _t["id"] == tile_id:
        return _t
  return None

def draw_special(_tile, tiles):
  print("-> %s" % _tile["special"])

def draw_tile(board_tile):
  print("-> %s (tiers: %d, rev: %d)" % (board_tile["name"], board_tile["tiers"], board_tile["revenue"]))

def draw_board(board, tiles):
  for _tile in board:
    if _tile["type"] == "special":
        draw_special(_tile, tiles)
    elif _tile["type"] == "tile":
        board_tile = find_tile(tiles, _tile["tile"])
        draw_tile(board_tile)
    else:
        print("hello bug")

def main():
  if len(sys.argv) != 3:
    usage()
  else:
    board = json.load(open(sys.argv[2], "r"))
    tiles = json.load(open(sys.argv[1], "r"))
    draw_board(board, tiles)


if __name__ == "__main__":
  main()
