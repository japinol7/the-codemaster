"""Package persistence.
Persists the game state in some files:

items.json:
  Persists changes to the items defined in each level.
  It only persists items from the levels that the player has visited,
  since levels not visited will not be changed.
  Note that when recovering the saved game, we look up in this file
  just the item ids that are present in the game levels and update
  the items state regarding their attributes on the file.

items_not_initial.json:
  Persists items added dynamically to each level.
  These items must be recreated dynamically again.
  Note that the item ids when recreated will probably be different
  from the ones in the file.

npcs.json:
  Persists changes to the NPCs defined in each level.
  It only persists NPCs from the levels that the player has visited,
  since levels not visited will not be changed.
  Note that when recovering the saved game, we look up in this file
  just the NPCs ids that are present in the game levels and update
  the NPC state regarding their attributes on the file.

npcs_not_initial.json:
  Persists NPCs added dynamically to each level.
  These NPCs must be recreated dynamically again.
  Note that the NPCs ids when recreated will probably be different
  from the ones in the file.

player.json:
  Persists the Player's state.
"""