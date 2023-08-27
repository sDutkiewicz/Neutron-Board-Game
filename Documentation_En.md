# Documentation

## Author Information
- **Author:** Stanisław Dutkiewicz (329076)

## Project Name
### Neutron Board Game

## Project Description
The project is a simulation of the Neutron Board Game, an abstract two-player strategy game played on a 5x5 square board. Players alternate moving their pieces across the board and the neutron, aiming to move the neutron pawn to their side of the board. Players can choose between two computer player modes: 
1. Random move mode, where the computer chooses a random possible move each turn.
2. Best move mode, where the computer selects the best move based on certain simple criteria. 

The project includes a graphical user interface (GUI).

Neutron game wikipedia: https://en.wikipedia.org/wiki/Neutron_(game)

## Program Structure
The program is divided into four classes:
- **NeutronBoard:** The main class representing the game board. It includes methods for board initialization, moving pawns, checking for a winner, and other game logic.
- **Player:** Represents players in the Neutron game. It contains methods and properties to determine player moves and strategy.
- **NeutronBoardGUI:** A subclass of NeutronBoard representing the game's GUI version. It allows players to interact with the game board using the Tkinter interface.
- **main:** Contains the main function to launch the game.

## Class Descriptions
- **NeutronBoard:** Represents the board and its logic for the Neutron game. Includes methods for board initialization, making moves, and checking for a winner. It holds the current game state, board, and neutron location.
- **Player:** Represents a player in the Neutron game. Contains methods and properties for determining moves and player strategy.
- **NeutronBoardGUI:** A subclass of NeutronBoard responsible for creating the game's GUI. Includes methods for button creation, displaying the game board, and handling user interaction with the GUI.
- **main:** Contains the main function that starts the game.

## User Guide
To play the game, run the `main.py` file. The game will prompt the user to select a strategy for the computer player. Players can then click on a pawn or the neutron in the GUI, choose moves from a list provided, and finally move the pawn by clicking the "Move" button.

The goal is to move the neutron to your home row or make the opponent move the neutron to your home row. Completely blocking the neutron, so the opponent can't move it, also results in a win for the player blocking the neutron.

After the game ends, a message will display indicating the winner and an option to replay the game.

## Reflections
The project was successfully completed and includes all planned features. The game can be played in two modes: random and smart. In the random mode, the computer makes random moves, while in the smart mode, it uses an algorithm to determine the best move. The game ends when a player moves the neutron to their row or completely blocks it.

One of the challenges faced during the project was implementing the smart move algorithm for the computer player. It was difficult to devise an algorithm that consistently made the best move. Another challenge was integrating the GUI with the game logic. Ensuring the GUI accurately reflected the current board state and enabling or disabling buttons correctly was challenging. Creating the GUI itself was also time-consuming.

If given more time, I would have added icons for the pawns and neutron on the board.

Overall, I'm pleased with the project outcome. The game is functional and playable. The smart move algorithm for the computer player could be improved, but it still makes challenging moves for the human player. The game's GUI version provides a more immersive experience for the player.
