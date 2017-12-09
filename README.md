NeoBattleship - Group Project

https://github.com/Felipemguerra/NeoBattleship

Members: Ernest Besse, Brian Smith, Felipe Guerra

PyQt5 Documentation: http://pyqt.sourceforge.net/Docs/PyQt5/modules.html

Execution: Game can be run by executing start script "./start" 
	   or by going into the "game" directory and running 
	   "python3 game.py"

Proposal:
	This project implements a simple version of the classic "Battleship" game 
	with online singleplay and multiplay.  The game will have three difficulties 
	for computer play, "Easy, Medium, Hard", where easy uses strict random 
	search, medium uses random and hit based decision algorithm, and hard uses 
	clustering and hit based decision algorithm.  Players will have drag and 
	drop ship placement while computer will use a ship placement algorithm 
	for unique ship locations.
	
Missing Features:
	-drag and drop ship placements for player
	-sophisticated ship placement algorithm for computer
	-hard difficulty that uses clustering to make better dicisions on where to find ships
	-networking
	-multiplayer

Instructions:
	-Original difficulty is set to "Hard", can be changed in drop down
	 menu
	-Restarting the game keeps the currently set difficulty
	-Changing the difficuly restarts the game
	-Game starts immediatly upon running "python3 game.py" with the player having the
	 first move

Libraries used:
	-PyQt5(QtWidgets,QtCore,QtGui)
	-sys
	-random

Image Resources used:
	water.jpeg: used as board backgrounds
		-https://pxhere.com/en/photo/1373790
	metal.jpg and ship.jpg: used to show player ships
		-https://pixnio.com/textures-and-patterns/metal-texture/aluminium-gray-textured-metal-sheet-metal-texture
	explosion.jpg: used to show hits on the board and sunken ships
		-https://pixabay.com/en/explosion-fire-brand-destroy-1039943/




