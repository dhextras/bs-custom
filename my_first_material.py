"""
    My First material by Dhextras
"""

# ba_meta require api 8

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence, Dict, Type, List, Optional, Union

# Necessory imports
import math
import babase
import bascenev1 as bs
import bauiv1 as bui
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.bomb import BombFactory

class FreezeBomb(bs.Actor):
    def __init__(
        self,
        position=(0.0, 1.0, 0.0),
        velocity=(0.0, 0.0, 0.0),
        blast_radius=2.5,  # Adjust the blast radius as needed.
        bomb_scale=1.0,  # Adjust the scale as needed.
        source_player=None,
        owner=None,
    ):
        super().__init__()

        shared = SharedObjects.get()
        factory = BombFactory.get()

        self.bomb_type = 'freeze'  # Set the bomb type to 'freeze'.

        self._exploded = False
        self.scale = bomb_scale
        self.blast_radius = blast_radius

        materials = (shared.object_material)

        self.node = bs.newnode(
            'bomb',
            delegate=self,
            attrs={
                'position': position,
                'velocity': velocity,
                'angular_velocity': angular_velocity,
                'mesh': factory.bomb_mesh,
                'body_scale': self.scale,
                'shadow_size': 0.3,
                'color_texture': factory.ice_tex,  # Use the 'ice' texture.
                'reflection': 'sharper',
                'reflection_scale': [1.8],
                'materials': materials,
            },
        )

        sound = bs.newnode(
            'sound',
            owner=self.node,
            attrs={'sound': factory.fuse_sound, 'volume': 0.25},
        )
        self.node.connectattr('position', sound, 'position')
        #bs.animate(self.node, 'fuse_length', {0.0: 1.0})  # Fuse animation.

    def explode(self):
        # Freeze Bomb does not explode, so this method is empty.
        pass

