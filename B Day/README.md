# BombSpawner Mod - Birthday Edition

This project is a heartfelt gift for **someone special** on their birthday. It's a way to add a touch of creativity and excitement to the celebration. Unfortunately, due to unforeseen circumstances, I couldn't finish it in time for the birthday celebration. However, I'm making it avilable for everyone now, hoping that you can find joy in tinkering with and enhancing this project.

## Prerequisites

Before you begin, ensure you have the following set up:

- [Ballistica Game Engine](https://github.com/efroemling/ballistica/): Install the Ballistica game engine to run and enjoy the BombSpawner game.

- [Ballistica Cloud Console](https://tools.ballistica.net/devices): Connect your game to the Ballistica Cloud Console to execute the game code.

## Setting Up the Game

1. **Create a New Game Environment**: Start by creating a new file `map.py` file provided in your [workspace](https://tools.ballistica.net/workspaces). This map will provide a clean and spacious area for spawning.

2. **Update Prop Node Files**: Replace the `prop_node.h` and `prop_node.c` files in the `src/ballistica/scene_v1/node` folder of your Ballistica game engine source code. These updated files are essential for the functioning of the BombSpawner game.

3. **Stage the Build**: Stage the Build using the game engine by running the below command. 

```bash
make cmake
```

## Running the Mod

1. **Connect to the Cloud Console**: Access the [Ballistica Cloud Console](https://tools.ballistica.net/devices) and connect your game to it. This will allow you to execute the main code.

2. **Prepare the Spawning Environment**: Open the game and create a new game type `Birth Day` in a new Playlist. This is where the dynamic bomb arrangement will take place.

3. **Execute the Game Code**: Copy the code from the `bday.py` file provided in this repository and paste it into the Ballistica Cloud Console.

4. **Start the Bomb Arrangement**: Run the copied code (from `bday.py`) in the Cloud Console. This will set up the BombSpawner and other needed Modules.

5. **Spawn the Bombs**: In the in game console / local console, use the following command to initiate the bomb spawning process:

```python
BombSpawner(120, '  happy birthday')
```

Here, `120` is the number of bombs you want to spawn, and `'  happy birthday'` is the text you want to form using the bombs. Remember to divide your text into groups of 8 letters each for optimal alignment using spaces. In this example, `happy` is in one 8-letter group and `birthday` is in the other.

6. **Enjoy the Spectacle**: Watch as the bombs dynamically arrange themselves to spell out the text you provided. It's a festive and visually captivating way to celebrate birthdays!

# Note

The mod is designed to support words with a maximum of 8 letters in each group. If your words are longer, feel free to split them into 8-letter segments with spaces for the best alignment and appearance. Alternatively, you can dive into the code and explore possibilities like adjusting rows and columns for more flexibility.

Have a fantastic time experimenting with the BombSpawner birthday edition! For additional information about Ballistica and its features, please visit the [Ballistica wiki](https://github.com/efroemling/ballistica/wiki/).
