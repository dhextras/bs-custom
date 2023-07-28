"""
    My First try by Dhextras
"""

# ba_meta require api 8

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing import Any, Sequence, Dict, Type, List, Optional, Union

# Necessory imports
import random
import time
import babase
import bascenev1 as bs
from bascenev1lib.actor.spazbot import SpazBotSet, SpazBot
from bascenev1lib.actor.bomb import Bomb

# Defining the main funciton for the gamemod plugin
# ba_meta export bascenev1.GameActivity
class MyFirstTry(bs.TeamGameActivity[bs.Player, bs.Team]):
    name = 'My First Try'
    description = ('My first try to mod bombsquad\n')
    tips = ['U sucks fucker']
    
    # Difining the game mode to support on only freefor all sessions
    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.FreeForAllSession)
        
    # Defining supported maps, I only wanted 'football' stadium as of now
    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        del sessiontype  # Unused arg.
        assert babase.app.classic is not None
        return babase.app.classic.getmaps('football')
        
    # Here we define the game mode and settings and stuff
    def __init__(self, settings: dict):
        super().__init__(settings)   
        self.settings = settings
        self._bots = SpazBotSet()
        self._bomb_ttl = int(40)
        self._bomb_count = int(0)

    # Here is the main logic for this game where we spawn and make them move to make the words
    def on_begin(self) -> None:
        super().on_begin()
        bs.timer(2, self._bomb_timer)

    # overiding the charector spawning to disable punch and bomb
    def spawn_player(self, player: bs.Player) -> bs.Actor:
        # It simply call spawn_player_spaz for provided player
        x_cord = round(random.uniform(-13.4, 13.4), 1)
        spaz = self.spawn_player_spaz(player, position = (x_cord, 1.5, 7))
        spaz.connect_controls_to_player(enable_bomb = False, enable_punch = False)

        return spaz

    # starting a timer for bomb throw to make it look cool instead of all falling at the same time
    def _bomb_timer(self) -> None:
        bs.timer(0.1, self._bomb_throw)

    # Throwing the bombs on the field with the timing 
    def _bomb_throw(self) -> None:
        bs.timer(1, bs.Call(self._bomb, (0, 0, 1), (10, -3, 0)))
        self._bomb_count += 1

        if self._bomb_count < self._bomb_ttl:
            self._bomb_timer()
        else:
            pass

    # the actual bomb throwing
    def _bomb(self, position: Sequence[float], velocity: Sequence[float]) -> None:
        Bomb(position=position, velocity=velocity).autoretain()