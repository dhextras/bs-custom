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

class Puck(bs.Actor):
    """A lovely giant hockey puck."""

    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        print(activity)

        # Spawn just above the provided point.
        self._spawn_pos = (position[0], position[1] + 1.0, position[2])
        self.last_players_to_touch: Dict[int, Player] = {}
        self.scored = False
        assert activity is not None
        pmats = [shared.object_material, activity.puck_material]
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': activity.puck_model,
                                   'color_texture': activity.puck_tex,
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2],
                                   'shadow_size': 0.5,
                                   'is_area_of_interest': True,
                                   'position': self._spawn_pos,
                                   'materials': pmats
                               })
        bs.animate(self.node, 'mesh_scale', {0: 0, 0.2: 1.3, 0.26: 1})
        
class FreezeBomb(bs.Actor):
    def __init__(
        self,
        position=(0.0, 1.0, 0.0),
        velocity=(0.0, 0.0, 0.0),
        blast_radius=2.5,  # Adjust the blast radius as needed.
        bomb_scale=1.2,  # Adjust the scale as needed.
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


class NewBomb(bs.Actor):
    def __init__(self, position, velocity):
        super().__init__()
        shared = SharedObjects.get()
        self.node = bs.newnode('prop', delegate=self, attrs={
            'position': position,
            'velocity': velocity,
            'body': 'sphere',
            'mesh': bs.getmesh('bomb'),
            'color_texture': bs.gettexture('freezeBombColor'),
            'reflection': 'powerup',
            'reflection_scale': [0.2],
            'materials': (shared.footing_material, shared.object_material)
        })

    def handleMessage(self, msg):
        if not self.node.exists():
            return
        if isinstance(msg, bs.DieMessage):
            # The bomb was killed before reaching the target position.
            # Perform any cleanup necessary.
            self.node.delete()
        else:
            # Call the base class handlemessage method for other messages.
            super().handleMessage(msg)



