## ReReunion

A python/pygame reimplementation of (Merit's Galactic) Reunion.

### How to run?

You will need:
 - original data files of Reunion (you can try google)
 - python 3+ (3.9.2 is used currently for development) 
 - pygame 2.4+ (2.4.0 is used currently for development)

1. Copy all files from this repo to the directory where your Reunion data files are located.
2. Prepare a saved game in the first save slot (e.g. by running the original Reunion in DosBox first).
3. Launch `rereunion.py`

### Why?

Well, if you have the original game you can enjoy it in DosBox... So then what's the point in redoing it?

The basic idea is to extend it with new features, and more detailed and extended storyline:

***ReReunion 1.0***  
The reimplementation of the original game, with only bugfixes, or tiny upgrades for better usability (mouse scroll wheel, etc.).  
***ReReunion 1.5***  
The original game as it is supposed to be: piracy, more advanced (ground) battles, manufacturing is not concentrated on main planet, more battles, automate boring tasks (planet surface micromanagement, minerals transport etc.)  
***ReReunion 2.0***  
More inventions, more buildings, more planets, more races, more interaction with aliens, more story, more battles, a little bit more of everything :-)  

### Current status

Aiming for ReReunion 1.0.

Many things do work, but so many more do not (yet).

Features as of now:  
 - usable framework for the game
 - use the original graphics, sound and text message files
   - decoding
   - slicing up parts (sprites)
 - menu (icons, sfx, labels, scroll)
 - infobar (label, money, date)
 - screens
   - control room
   - planet main
   - research-design
   - info-buy
   - ship info
   - starmap
   - messages
 - control room - almost everything
   - render hero/commanders
   - navigate to other screens
 - planet surface - almost everything
   - render surface with buildings
   - scrolling, selecting building
   - demolish buildings
   - radar view navigation
   - animated surface (flowing river, etc.)
 - info-buy
   - browse inventions
   - show production status
   - invention info / pic
 - starmap
   - show solar systems/planets/moons
   - navigate between solsystems/planets
   - go to planet surfaces
 - research-design
   - show status of inventions
   - show scientist skills
   - some animations
 - messages
   - show messages
 - read and process raw data from saved games
   - inventions, solar systems, planet and building data, fleet data, some other game states
 - read and process raw data from original executable
   - building definitions, solar systems, names, and some other static game data

### Contributing

Please, please do contribute if you can! Thank you!

If you could work on:
 - missing features
 - gathering info on the original algos from the game
   - how to calculate: tax, population growth, population mood, power/food/hospital production on planets etc.
   - find the meanings of the "unknown" fields in rere_processrawdata.py
 - extract synthesyzer (midi?) music
 - etc.

That would be great!

But please don't start refactoring, tidying etc. Maybe later.
