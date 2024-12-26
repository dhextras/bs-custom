# Standard Library Imports
import random
import time

# Ballistica Scene and Actor and Materials Imports
import bascenev1 as bs
from bascenev1lib.actor.bomb import BombFactory
from bascenev1lib.gameutils import SharedObjects


class ImpactTexBomb(bs.Actor):
    """
    Custom bomb class inheriting from the 'Bomb' class in the 'babase' module
    Enables creation of bombs with customized properties and behaviors
    """

    def __init__(self, position=(0, 0.2, 0), angular_velocity=(0.1, 0, 0)):
        # Initialize a new bomb actor
        super().__init__()

        # Get shared objects and bomb factory instances
        shared = SharedObjects.get()
        factory = BombFactory.get()

        # Create a new node for the bomb with specified attributes
        self.node = bs.newnode(
            "prop",
            delegate=self,
            attrs={
                "position": position,
                "angular_velocity": angular_velocity,
                "body": "sphere",
                "body_scale": 0.6,
                "mesh_scale": 0.6,
                "shadow_size": 0.2,
                "mesh": bs.getmesh("bomb"),
                "color_texture": factory.impact_lit_tex,
                "reflection": "sharper",
                "reflection_scale": [2],
                "materials": (shared.footing_material, shared.object_material),
            },
        )
    

    def handleMessage(self, msg):
        # Check if the node exists before handling the message
        if not self.node.exists():
            return

        if isinstance(msg, bs.DieMessage):
            # If the bomb was killed before reaching the target position,
            # perform necessary cleanup by deleting the bomb's node
            self.node.delete()
        else:
            # For other message types, call the base class's handleMessage method
            super().handleMessage(msg)


class FreezeBomb(bs.Actor):
    """
    Custom bomb class with freezing Bomb effect, derived from the 'Actor' class
    Represents a freeze Bomb with the fuse which wont explode
    """

    def __init__(
        self,
        position=(0.0, 1.0, 0.0),
        angular_velocity=(0.1, 0.0, 0.0),
        blast_radius=2.5,  # Adjust the blast radius as needed.
        bomb_scale=0.6,  # Adjust the scale as needed.
        source_player=None,
        owner=None,
    ):
        # Initialize a new freeze bomb actor
        super().__init__()

        # Get shared objects and bomb factory instances
        shared = SharedObjects.get()
        factory = BombFactory.get()

        # Set the bomb type to 'freeze'
        self.bomb_type = "freeze"

        # Initialize variables for bomb properties
        self._exploded = False
        self.scale = bomb_scale
        self.blast_radius = blast_radius

        # Define materials for the bomb's appearance
        materials = (shared.object_material, shared.footing_material)

        # Create a new bomb node with specified attributes
        self.node = bs.newnode(
            "bomb",
            delegate=self,
            attrs={
                "position": position,
                "angular_velocity": angular_velocity,
                "mesh": factory.bomb_mesh,
                "body_scale": self.scale,
                "mesh_scale": self.scale,
                "shadow_size": 0.2,
                "color_texture": factory.ice_tex,  # Use the 'ice' texture.
                "reflection": "sharper",
                "reflection_scale": [1],
                "materials": materials,
                "fuse_length": 0.3,
            },
        )

        # Attach a fuse sound to the bomb
        sound = bs.newnode(
            "sound",
            owner=self.node,
            attrs={"sound": factory.fuse_sound, "volume": 0.25},
        )
        self.node.connectattr("position", sound, "position")
        # bs.animate(self.node, 'fuse_length', {0.0: 1.0})  # Fuse animation.

    def explode(self):
        # Freeze Bomb does not explode, so this method is empty.
        pass


class AlphabetPositions:
    """
    Class representing the positions of letters in a grid
    Each letter is represented by a 5x5 grid of 1s (bomb present) and 0s (empty space)
    """

    def __init__(self):
        # Define the positions for each letter in the alphabet
        self.positions = {
            "A": [
                [0, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
            ],
            "B": [
                [1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0],
            ],
            "C": [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
            ],
            "D": [
                [1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0],
            ],
            "E": [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
            ],
            "F": [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
            ],
            "G": [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 0, 1, 0],
                [0, 1, 1, 1, 0],
            ],
            "H": [
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
            ],
            "I": [
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
            ],
            "J": [
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
            ],
            "K": [
                [1, 0, 0, 1, 0],
                [1, 0, 1, 0, 0],
                [1, 1, 0, 0, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0],
            ],
            "L": [
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
            ],
            "M": [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
            ],
            "N": [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 1],
            ],
            "O": [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0],
            ],
            "P": [
                [1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
            ],
            "Q": [
                [0, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 1, 0],
            ],
            "R": [
                [1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0],
            ],
            "S": [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 1, 1, 1, 0],
            ],
            "T": [
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
            ],
            "U": [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0],
            ],
            "V": [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            "W": [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 0, 0, 1],
            ],
            "X": [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1],
            ],
            "Y": [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
            ],
            "Z": [
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 1, 1, 1, 0],
            ],
            " ": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "#": [
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
            ],
        }

    def generate_letter_positions(self, letter, center_position):
        # Retrieve the grid positions for the specified letter
        letter_positions = self.positions.get(letter)
        if letter_positions is None:
            # If the letter is not supported, raise a ValueError
            raise ValueError(f"Letter '{letter}' is not supported.")

        # Initialize an offset for positioning the letters within the grid
        offset = (-1, 0, -1)

        # Initialize an empty list to store the calculated positions
        positions = []

        # Iterate through each row in the letter_positions grid
        for row in letter_positions:
            # Iterate through each column value in the row
            for col in row:
                if col == 1:
                    # If the column value is 1, add a position for the letter
                    positions.append(
                        (
                            center_position[0] + offset[0],
                            center_position[1],
                            center_position[2] + offset[2],
                        )
                    )

                # Update the horizontal offset for the next column
                offset = (offset[0] + 0.5, 0, offset[2])

            # Update the vertical and horizontal offset for the next row
            offset = (-1, 0, offset[2] + 0.5)

        # Return the list of calculated positions for the letter
        return positions


class BombSpawner:
    """Class responsible for spawning bombs and managing their behavior for the mod"""

    def __init__(self, n_bombs=150, word="welcome"):
        # Initialize instance variables to store various data
        self.bombs = []  # List to store bomb instances
        self.positions = []  # List to store bomb positions

        self.used_bombs = []  # List to store used bomb instances
        self.non_used_bombs = []  # List to store non-used bomb instances

        self.letter = []  # List to store letters of the word
        self.letter_groups = []  # List to store groups of letters
        self.letter_centers = []  # List to store center positions for letters
        self.letter_positions = []  # List to store positions for letters

        self.word = word  # The word to be displayed using bombs
        self.group_size = 8  # Size of letter groups
        self.n_bombs = n_bombs  # Total number of bombs
        self.start_time = time.time()  # Store the starting time
        self.check_time = time.time()  # Store the time for checking

        # Create an instance of the AlphabetPositions class
        self.alphabet_positions = AlphabetPositions()

        # Divide the word into groups of specified size
        self.letter_groups = [
            self.word[i : i + self.group_size]
            for i in range(0, len(self.word), self.group_size)
        ]

        # Generate random positions for bombs and start spawning
        for _ in range(n_bombs):
            x = round(random.uniform(-9, 9), 0)
            z = round(random.uniform(-4, 4), 0)

            position = (x, 1, z)
            self.positions.append(position)

        bs.timer(0, bs.Call(self.on_begin, self.positions))

    def on_begin(self, positions):
        # Start spawning bombs with a delay
        bs.timer(1, bs.Call(self._spawn_bombs, positions))

    def _spawn_bombs(self, positions):
        # Start spawning individual bombs
        bs.timer(0.01, bs.Call(self._bombs, positions[self.n_bombs - 1]))

    def _bombs(self, position):
        # Spawn a new bomb with random angular velocity
        x = round(random.uniform(-7, 7), 1)
        y = round(random.uniform(-7, 7), 1)
        z = round(random.uniform(-7, 7), 1)

        bomb = ImpactTexBomb(position=position, angular_velocity=(x, y, z))

        self.n_bombs -= 1
        self.bombs.append(bomb)

        # If more bombs are left, continue spawning
        if int(self.n_bombs) > int(0):
            bs.timer(0, bs.Call(self._spawn_bombs, self.positions))

        # If all bombs are spawned, move them outwards
        else:
            self.non_used_bombs = self.bombs[:]
            self.letter = list(self.letter_groups[0].strip().upper())
            bs.timer(
                1.5,
                bs.Call(
                    self._move_bombs_outwards,
                    bombs=self.non_used_bombs,
                    center_position=(0, 0.2, 0),
                ),
            )

    def _move_bombs_outwards(self, bombs, center_position):
        # Move bombs outwards from the center position
        for bomb in bombs:
            x_distance = bomb.node.position[0] - center_position[0]
            z_distance = bomb.node.position[2] - center_position[2]

            if abs(x_distance) > 0 or abs(z_distance) > 0:
                # Calculate speed separately for x and z directions
                x_velocity = 1.0 / (x_distance + 0.1) * 15
                z_velocity = 1.0 / (z_distance + 0.1) * 20

                angular_velocity = (z_velocity, 0, -x_velocity)

            else:
                # If at the center, apply random angular velocity for tumbling effect
                angular_velocity = (
                    random.choice([-20, 20]),
                    0,
                    random.choice([-20, 20]),
                )

            # Set the angular_velocity for the bomb
            bomb.node.angular_velocity = angular_velocity
            # Start timer to reset bomb after a delay
            bs.timer(1.4, bs.Call(self._reset_bomb, bomb))

        if self.letter:
            # Prepare for generating letters of the next group
            self.used_bombs = []
            self.letter_groups.pop(0)
            self.non_used_bombs = self.bombs[:]
            bs.timer(1, bs.Call(self.generate_group_letters))

    def generate_group_letters(self):
        # Generate letters of the current group
        # Calculate desired positions for the group
        self.letter_centers = self._calculate_letter_center_positions(len(self.letter))

        letter = self.letter[0]
        letter_center = self.letter_centers[0]

        self.letter.pop(0)
        self.letter_centers.pop(0)
        bs.timer(0.01, bs.Call(self._generate_letter, letter, letter_center))

    def _calculate_letter_center_positions(self, group_length):
        # Calculate the desired center positions for the letters in the group
        num_columns = min(8, group_length)
        x_offsets = [-1.5 * (num_columns - 1) + i * 3 for i in range(num_columns)]

        # Center the desired positions around (0, 0, 0)
        center_position = (0.0, 0.2, 0.0)
        letter_centers = [
            (x + center_position[0], center_position[1], center_position[2])
            for x in x_offsets
        ]

        return letter_centers

    def _generate_letter(self, letter, letter_center):
        # Generate positions for the current letter using the AlphabetPositions class
        self.letter_positions = self.alphabet_positions.generate_letter_positions(
            letter, letter_center
        )

        desired_position = self.letter_positions[0] if self.letter_positions else None

        if desired_position:
            # Start timer to check the closest bomb position to the desired position
            bs.timer(0, bs.Call(self._check_closest_bomb_position, desired_position))

        else:
            # If no desired position, move on to the next letter or group
            bs.timer(0, bs.Call(self._iterate_through_letters))

    def _check_closest_bomb_position(self, desired_position):
        # Find the closest bomb to the desired position and set its velocity
        closest_bomb = None
        closest_distance = float("inf")

        for bomb in self.non_used_bombs:
            distance = sum(
                (a - b) ** 2 for a, b in zip(bomb.node.position, desired_position)
            )

            if distance < closest_distance:
                closest_bomb = bomb
                closest_distance = distance

        if closest_bomb:
            self.letter_positions.pop(0)
            self.used_bombs.append(closest_bomb)
            self.non_used_bombs.remove(closest_bomb)

            bs.timer(
                0.1, bs.Call(self._set_bomb_velocity, closest_bomb, desired_position)
            )
            bs.timer(0, bs.Call(self._reset_bomb, closest_bomb, desired_position, True))

    def _iterate_through_letters(self):
        # Iterate through the letters and their centers
        if self.letter and self.letter_centers:
            letter = self.letter[0]
            letter_center = self.letter_centers[0]

            self.letter.pop(0)
            self.letter_centers.pop(0)
            # Start timer to generate the next letter
            bs.timer(0.01, bs.Call(self._generate_letter, letter, letter_center))

        else:
            # If all letters are generated, move used bombs outward
            self.letter = (
                list(self.letter_groups[0].strip().upper())
                if self.letter_groups
                else None
            )
            bs.timer(
                2.0,
                bs.Call(
                    self._move_bombs_outwards,
                    self.used_bombs,
                    center_position=(0, 0.2, 0),
                ),
            )

    def _set_bomb_velocity(self, bomb, desired_position):
        # Set the bomb's angular velocity for rolling motion towards the desired position
        x_distance = desired_position[0] - bomb.node.position[0]
        z_distance = desired_position[2] - bomb.node.position[2]

        if abs(x_distance) > 0 or abs(z_distance) > 0:
            # Calculate speed separately for x and z directions
            x_velocity = 5.0 * (x_distance + 0.1)
            z_velocity = 5.0 * (z_distance + 0.1)

            # Calculate the angular velocity based on the velocity components
            angular_velocity = (z_velocity, 0, -x_velocity)

        # Set the angular velocity of the bomb for rolling motion
        bomb.node.angular_velocity = angular_velocity

        if self.letter_positions:
            # Start timer to check the closest bomb position to the next desired position
            bs.timer(
                0, bs.Call(self._check_closest_bomb_position, self.letter_positions[0])
            )

        else:
            # If no more desired positions, iterate to the next letter or group
            bs.timer(0, bs.Call(self._iterate_through_letters))

    def _reset_bomb(self, bomb, position=None, condition=False):
        # Reset the bomb's position and angular velocity
        if not position:
            position = bomb.node.position
            reset_position = position

        if condition:
            # If a condition is met, start timer to eliminate angular velocity
            bs.timer(1.28, bs.Call(self._eliminate_angular_velocity, bomb, position))

        else:
            # Set the bomb's position and apply angular velocity for rolling motion
            bomb.node.position = position
            bomb.node.angular_velocity = (0, 5, 0)

    def _eliminate_angular_velocity(self, bomb, position):
        # Eliminate angular velocity and stop movement
        bomb.node.velocity = (0, 0, 0)
        bomb.node.angular_velocity = (
            0,
            0,
            0,
        )  # Set angular_velocity to 0 to stop movement
        # Start timer to reset bomb after eliminating angular velocity
        bs.timer(0, bs.Call(self._reset_bomb, bomb, position))

    def _calc_run_time(self):
        # Calculate and return the elapsed time since start
        self.check_time = time.time()
        elapsed_time = (self.check_time - self.start_time) * 100

        milliseconds = round(elapsed_time, 2)

        return f"Elapsed Time: {milliseconds}ms"
