"""
    My First try by Dhextras
"""

# ba_meta require api 9

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

# Necessory imports
import random

import babase
import bascenev1 as bs


# Defining the main funciton for the gamemod plugin
# ba_meta export bascenev1.GameActivity
class MyFirstTry(bs.TeamGameActivity[bs.Player, bs.Team]):
    name = "Birth Day Mod"
    description = "Make your birthday wish with some cool animation with bombs\n"
    tips = ["Make em impressed.."]

    # Difining the game mode to support on only freefor all sessions
    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.FreeForAllSession)

    # Defining supported maps, I only wanted 'football' stadium as of now
    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        del sessiontype  # Unused arg.
        assert babase.app.classic is not None
        return babase.app.classic.getmaps("football")

    # Here we define the game mode and settings and stuff
    def __init__(self, settings: dict):
        super().__init__(settings)
        self.settings = settings

    # Here is the main logic for this game where we spawn and make them move to make the words
    def on_begin(self) -> None:
        super().on_begin()
        self.hdisplay = bs.newnode(
            "text",
            attrs={
                "v_attach": "bottom",
                "h_attach": "left",
                "h_align": "left",
                "color": (1, 1, 1),
                "flatness": 0.5,
                "shadow": 0.5,
                "position": (20, 10),
                "scale": 1.0,
                "text": "By DhextraS",
            },
        )

    # overiding the charector spawning to disable punch and bomb
    def spawn_player(self, player: bs.Player) -> bs.Actor:
        # It simply call spawn_player_spaz for provided player
        x_cord = round(random.uniform(-13.4, 13.4), 1)
        spaz = self.spawn_player_spaz(player, position=(x_cord, 1.5, 7))
        spaz.connect_controls_to_player(enable_bomb=False, enable_punch=False)

        return spaz
