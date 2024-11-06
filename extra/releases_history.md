# Release History

## v0.0.8

### New features and improvements:

* Add two new game levels. Current level count: 30.
* Add new NPCs:
  * Alien Felines.
* Improve the test suite:
  * Allow tests to set empty levels iterables. 
    * You can use it whenever you need to test things that do not require creating some levels.
  * Execute the garbage collector when loading last game inside tests.
    * This will reduce the total memory used when running tests with multiple game loads.
  * Current tests count: 65.

<br>

## v0.0.7

### New features and improvements:

* Add persistence of the game state:
  * When the player exits a game, it automatically saves the game state.
  * The player can start a new game or continue the previous one.
* Add a new game level. Current level count: 28.
* Add spells: 
  * Mutentrinos Bolt A.
  * Mutentrinos Bolt B.
* Improve energy shields effectiveness. 
* Improve spells: 
  * Drain life.
* Add new NPCs:
  * Ewlans.
* Improve NPCs:
  * Kung Fu Fighters.
  * Mages.
* Add a debug feature that allows to:
  * Copy items and NPCs as selected actors.
  * Paste the selected actor to the mouse position.
    * This is only implemented within the same level.
* Improve the test suite:
  * Facilitate testing persistence.
  * Remove support of the game test decorator for methods.
  * Current tests count: 62.

<br>

## v0.0.6

### New features and improvements:

* Add three new game levels. Current level count: 27.
* Add new NPCs:
  * Kung Fu Fighters.
  * Squirrels.
* Improve actor models. 
* Improve level models.
* Improve the test suite.
* Fix some minor issues.

<br>

## v0.0.5

### New features and improvements:

* Add twelve new game levels. Current level count: 24.
* Improve NPCs: 
  * Demons now can cast these spells:
    * Fire Breath B: Most of the time they will cast this one.
    * Fire Breath A: Low change to cast this one.
    * VortexOfDoom B: Very low change to cast this one.
  * They have great resistance to magic. 
* Add new NPCs:
  * Dragons.
    * They have good or great resistance to magic.
    * They can cast these spells: 
      * Fire Breath B: Most of the time they will cast this one.
      * Fire Breath A: Some change to cast this one.
      * VortexOfDoom B: Low change to cast this one.
  * Pumpkin zombies.
    * They have some resistance to magic.
    * They can cast these spells: 
      * Drain life B: Most of the time they will cast this one.
      * Drain life A: Some change to cast this one.
  * Pumpkin heads (zombies).
    * They have some resistance to magic.
    * They can cast these spells: 
      * Drain life B: Most of the time they will cast this one.
      * Drain life A: Some change to cast this one.
      * VortexOfDoom B: Low change to cast this one.
  * Samurais.
    * They can shoot.
    * They have a bit of a resistance to magic.
    * They can cast these spells:
      * Samutrinos Bolt B: Most of the time they will cast this one.
      * Samutrinos Bolt A: Low change to cast this one.
  * Tethloriens.
    * They can shoot.
    * They have a bit of a resistance to magic.
    * They can cast these spells:
      * Neutrinos Bolt B: Most of the time they will cast this one.
      * Neutrinos Bolt A: Low change to cast this one.
* Add spells: 
  * Fire Breath B.
  * Fire Breath A.
  * Neutrinos Bolt A.
  * Neutrinos Bolt B.
  * Samutrinos Bolt A.
  * Samutrinos Bolt B.
* Improve spell casting and spells.
* Improve the test suite.

<br>

## v0.0.4

### New features and improvements:

* Add six new game levels. Current level count: 12.
* Add new NPCs:
  * Pokoyos.
  * Robots.
  * Mages.
* Add magic resistance attribute for actors.
* Add new spells: 
  * Drain life.
* Improve spell casting and spells.
* Improve actor text messages.
* Improve debug logs.
* Improve the test suite.
