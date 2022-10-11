# Overview 
The purpose of this document is to list and explain functions and their requirements for our arcade game's interface and performance
 
# Functional Requirements 
1. Main menu 
    1. The main menu shall have a ‘list’ of games a user can select from. 
    2. The main menu shall open a game when chosen by a user.
    3. The main menu shall have options for users to change key binds.
2. Pac-man
    1. The Pacman character shall be able to move up, down, left, and right by a specific number of units
    2. When Pacman hits a ghost while it is vunerable from the power pellet, it shall enter it's 'death' state.
4. Pong
    1. After scoring a point the score board shall increase by 1.
    2. The “paddles” shall only move vertically up and down.
    3. The ball shall bounce off the top and bottom at the same angle at which it met the wall.
    4. After scoring a point, the ball shall be respawned in the middle horizontally and at the same vertical height          at which the ball contacted the “goal”.
5. Frogger
    1. In frogger, the character shall move exactly one tile at a time
    2. When the player character comes into contact with a car in Frogger, they shall receieve a game over.
6. General
    1. The keyboard inputs shall properly control the player character and not tamper with anything outside of the window.

# Non-Functional Requirements
1. Interface
    1. The interface shall allow more than one user to play on a single device without affecting the game performance.
    2. The interface shall have a record of hi-scores and current game score displayed for the user to see. 
    3. The interface shall have images displayed for the games in the ‘list’ of games.
    4. The interface shall show proper graphics in order to portray the games in an appealing manner. 
2. Pac-man
    1. The pacman AI shall be convincing to play against
    2. The ghosts shall be visually distinguishable from each other.
3. Pong
    1. The pong AI shall be reasonably skilled.
    2. The paddles shall move at a speed that is able to return the ball most of the time
    3. The ball shall travel at a speed that is difficult yet fun.
4. Frogger
    1. Frogger shall always have an available path
5. General
    1. The system shall work on any computer
    2. The volume feature shall add sound to the games.
