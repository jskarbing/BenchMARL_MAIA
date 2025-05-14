# TODO: Update copyright and license bit to be correctly formatted for crediting the original authors

# Slightly modified version of meltingpot/configs/substrates/commons_harvest__open.py with:
    # Copyright 2022 DeepMind Technologies Limited.
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     https://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
"""Configuration for Harvest MAIA.

Apples are spread around the map and can be consumed for a reward of 1. Apples
that have been consumed do not regrow, and so this substrate does not have a 
tragedy of the commons element (as the original Melting Pot Commons Harvest does).

Further changes from the original substrate include:
- Replacing the map with a smaller one, 
- Reducing the number of players to 2, 
- Reducing the player observation size to 5x5 (from 11x11),
- Making each player always spawn in the same position and with the same orientation.

"""

from typing import Any, Dict, Mapping, Sequence

from meltingpot.utils.substrates import colors
from meltingpot.utils.substrates import shapes
from meltingpot.utils.substrates import specs
from ml_collections import config_dict
import numpy as np

# Warning: setting `_ENABLE_DEBUG_OBSERVATIONS = True` may cause slowdown.
_ENABLE_DEBUG_OBSERVATIONS = False

#MAIA: Removing apple regrowth, and thereby removing the tragedy of the commons element.
APPLE_RESPAWN_RADIUS = 0.
REGROWTH_PROBABILITIES = [0.]

ASCII_MAP = """
WWWWWWWWWWWW
WAA AAAA AAW
WA   AA   AW
W  W QP W  W
WA  WWWW  AW
WAA AAAA AAW
WWWWWAAWWWWW
"""

# `prefab` determines which prefab game object to use for each `char` in the
# ascii map.
CHAR_PREFAB_MAP = {
    "P": {"type": "all", "list": ["floor", "spawn_point"]},
    "Q": {"type": "all", "list": ["floor", "inside_spawn_point"]},
    " ": "floor",
    "W": "wall",
    "A": {"type": "all", "list": ["grass", "apple"]},
}

_COMPASS = ["N", "E", "S", "W"]

FLOOR = {
    "name": "floor",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "floor",
                "stateConfigs": [{
                    "state": "floor",
                    "layer": "background",
                    "sprite": "Floor",
                }],
            }
        },
        {
            "component": "Transform",
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Floor"],
                "spriteShapes": [shapes.GRAINY_FLOOR],
                "palettes": [{"*": (220, 205, 185, 255),
                              "+": (210, 195, 175, 255),}],
                "noRotates": [False]
            }
        },
    ]
}

GRASS = {
    "name":
        "grass",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState":
                    "grass",
                "stateConfigs": [
                    {
                        "state": "grass",
                        "layer": "background",
                        "sprite": "Grass"
                    },
                    {
                        "state": "dessicated",
                        "layer": "background",
                        "sprite": "Floor"
                    },
                ],
            }
        },
        {
            "component": "Transform",
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Grass", "Floor"],
                "spriteShapes": [
                    shapes.GRASS_STRAIGHT, shapes.GRAINY_FLOOR
                ],
                "palettes": [{
                    "*": (158, 194, 101, 255),
                    "@": (170, 207, 112, 255)
                }, {
                    "*": (220, 205, 185, 255),
                    "+": (210, 195, 175, 255),
                }],
                "noRotates": [False, False]
            }
        },
    ]
}

WALL = {
    "name": "wall",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "wall",
                "stateConfigs": [{
                    "state": "wall",
                    "layer": "upperPhysical",
                    "sprite": "Wall",
                }],
            }
        },
        {
            "component": "Transform",
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Wall"],
                "spriteShapes": [shapes.WALL],
                "palettes": [{"*": (95, 95, 95, 255),
                              "&": (100, 100, 100, 255),
                              "@": (109, 109, 109, 255),
                              "#": (152, 152, 152, 255)}],
                "noRotates": [False]
            }
        },
        {
            "component": "BeamBlocker",
            "kwargs": {
                "beamType": "zapHit"
            }
        },
    ]
}

SPAWN_POINT = {
    "name": "spawnPoint",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "spawnPoint",
                "stateConfigs": [{
                    "state": "spawnPoint",
                    "layer": "alternateLogic",
                    "groups": ["spawnPoints"]
                }],
            }
        },
        {
            "component": "Transform",
        },
    ]
}

INSIDE_SPAWN_POINT = {
    "name": "spawnPoint",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "spawnPoint",
                "stateConfigs": [{
                    "state": "spawnPoint",
                    "layer": "alternateLogic",
                    "groups": ["insideSpawnPoints"]
                }],
            }
        },
        {
            "component": "Transform",
        },
    ]
}

# Primitive action components.
# pylint: disable=bad-whitespace
# pyformat: disable
NOOP       = {"move": 0, "turn":  0, "fireZap": 0}
FORWARD    = {"move": 1, "turn":  0, "fireZap": 0}
STEP_RIGHT = {"move": 2, "turn":  0, "fireZap": 0}
BACKWARD   = {"move": 3, "turn":  0, "fireZap": 0}
STEP_LEFT  = {"move": 4, "turn":  0, "fireZap": 0}
TURN_LEFT  = {"move": 0, "turn": -1, "fireZap": 0}
TURN_RIGHT = {"move": 0, "turn":  1, "fireZap": 0}
FIRE_ZAP   = {"move": 0, "turn":  0, "fireZap": 1}
# pyformat: enable
# pylint: enable=bad-whitespace

ACTION_SET = (
    NOOP,
    FORWARD,
    BACKWARD,
    STEP_LEFT,
    STEP_RIGHT,
    TURN_LEFT,
    TURN_RIGHT,
    FIRE_ZAP,
)

TARGET_SPRITE_SELF = {
    "name": "Self",
    "shape": shapes.CUTE_AVATAR,
    "palette": shapes.get_palette((50, 100, 200)),
    "noRotate": True,
}


def create_scene():
  """Creates the scene with the provided args controlling apple regrowth."""
  scene = {
      "name": "scene",
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": "scene",
                  "stateConfigs": [{
                      "state": "scene",
                  }],
              }
          },
          {
              "component": "Transform",
          },
          {
              "component": "Neighborhoods",
              "kwargs": {}
          },
          {
              "component": "StochasticIntervalEpisodeEnding",
              "kwargs": {
                  "minimumFramesPerEpisode": 1000,
                  "intervalLength": 100,  # Set equal to unroll length.
                  "probabilityTerminationPerInterval": 0.15
              }
          }
      ]
  }

  return scene


def create_apple_prefab(regrowth_radius=-1.0,  # pylint: disable=dangerous-default-value
                        regrowth_probabilities=[0, 0.0, 0.0, 0.0]):
  """Creates the apple prefab with the provided settings."""
  growth_rate_states = [
      {
          "state": "apple",
          "layer": "lowerPhysical",
          "sprite": "Apple",
          "groups": ["apples"]
      },
      {
          "state": "appleWait",
          "layer": "logic",
          "sprite": "AppleWait",
      },
  ]
  # Enumerate all possible states for a potential apple. There is one state for
  # each regrowth rate i.e., number of nearby apples.
  upper_bound_possible_neighbors = np.floor(np.pi*regrowth_radius**2+1)+1
  for i in range(int(upper_bound_possible_neighbors)):
    growth_rate_states.append(dict(state="appleWait_{}".format(i),
                                   layer="logic",
                                   groups=["waits_{}".format(i)],
                                   sprite="AppleWait"))

  apple_prefab = {
      "name": "apple",
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": "apple",
                  "stateConfigs": growth_rate_states,
              }
          },
          {
              "component": "Transform",
          },
          {
              "component": "Appearance",
              "kwargs": {
                  "renderMode": "ascii_shape",
                  "spriteNames": ["Apple", "AppleWait"],
                  "spriteShapes": [shapes.APPLE, shapes.FILL],
                  "palettes": [
                      {"x": (0, 0, 0, 0),
                       "*": (214, 88, 88, 255),
                       "#": (194, 79, 79, 255),
                       "o": (53, 132, 49, 255),
                       "|": (102, 51, 61, 255)},
                      {"i": (0, 0, 0, 0)}],
                  "noRotates": [True, True]
              }
          },
          {
              "component": "Edible",
              "kwargs": {
                  "liveState": "apple",
                  "waitState": "appleWait",
                  "rewardForEating": 1.0,
              }
          },
          {
              "component": "DensityRegrow",
              "kwargs": {
                  "liveState": "apple",
                  "waitState": "appleWait",
                  "radius": regrowth_radius,
                  "regrowthProbabilities": regrowth_probabilities,
              }
          },
      ]
  }

  return apple_prefab


def create_prefabs(regrowth_radius=-1.0,
                   # pylint: disable=dangerous-default-value
                   regrowth_probabilities=[0, 0.0, 0.0, 0.0]):
  """Returns a dictionary mapping names to template game objects."""
  prefabs = {
      "floor": FLOOR,
      "grass": GRASS,
      "wall": WALL,
      "spawn_point": SPAWN_POINT,
      "inside_spawn_point": INSIDE_SPAWN_POINT,
  }
  prefabs["apple"] = create_apple_prefab(
      regrowth_radius=regrowth_radius,
      regrowth_probabilities=regrowth_probabilities)
  return prefabs


def create_avatar_object(player_idx: int,
                         target_sprite_self: Dict[str, Any],
                         spawn_group: str) -> Dict[str, Any]:
  """Create an avatar object that always sees itself as blue."""
  # Lua is 1-indexed.
  lua_index = player_idx + 1

  # Setup the self vs other sprite mapping.
  source_sprite_self = "Avatar" + str(lua_index)
  custom_sprite_map = {source_sprite_self: target_sprite_self["name"]}

  live_state_name = "player{}".format(lua_index)
  avatar_object = {
      "name": "avatar",
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": live_state_name,
                  "stateConfigs": [
                      {"state": live_state_name,
                       "layer": "upperPhysical",
                       "sprite": source_sprite_self,
                       "contact": "avatar",
                       "groups": ["players"]},

                      {"state": "playerWait",
                       "groups": ["playerWaits"]},
                  ]
              }
          },
          {
              "component": "Transform",
          },
          {
              "component": "Appearance",
              "kwargs": {
                  "renderMode": "ascii_shape",
                  "spriteNames": [source_sprite_self],
                  "spriteShapes": [shapes.CUTE_AVATAR],
                  "palettes": [shapes.get_palette(
                      colors.human_readable[player_idx])],
                  "noRotates": [True]
              }
          },
          {
              "component": "AdditionalSprites",
              "kwargs": {
                  "renderMode": "ascii_shape",
                  "customSpriteNames": [target_sprite_self["name"]],
                  "customSpriteShapes": [target_sprite_self["shape"]],
                  "customPalettes": [target_sprite_self["palette"]],
                  "customNoRotates": [target_sprite_self["noRotate"]],
              }
          },
          {
              "component": "Avatar",
              "kwargs": {
                  "index": lua_index,
                  "aliveState": live_state_name,
                  "waitState": "playerWait",
                  "speed": 1.0,
                  "spawnGroup": spawn_group,
                  "postInitialSpawnGroup": "spawnPoints",
                  "actionOrder": ["move", "turn", "fireZap"],
                  "actionSpec": {
                      "move": {"default": 0, "min": 0, "max": len(_COMPASS)},
                      "turn": {"default": 0, "min": -1, "max": 1},
                      "fireZap": {"default": 0, "min": 0, "max": 1},
                  },
                  "view": {
                      "left": 2,
                      "right": 2,
                      "forward": 2,
                      "backward": 2,
                      "centered": False
                  },
                  "spriteMap": custom_sprite_map,
                  "randomizeInitialOrientation": False,
              }
          },
          {
              "component": "Zapper",
              "kwargs": {
                  "cooldownTime": 2,
                  "beamLength": 3,
                  "beamRadius": 1,
                  "framesTillRespawn": 4,
                  "penaltyForBeingZapped": 0,
                  "rewardForZapping": 0,
              }
          },
          {
              "component": "ReadyToShootObservation",
          },
      ]
  }
  if _ENABLE_DEBUG_OBSERVATIONS:
    avatar_object["components"].append({
        "component": "LocationObserver",
        "kwargs": {"objectIsAvatar": True, "alsoReportOrientation": True},
    })

  return avatar_object


def create_avatar_objects(roles: Sequence[str]):
  """Returns list of avatar objects of length 'num_players' - len(roles)."""
  avatar_objects = []
  for player_idx, role in enumerate(roles):
    if player_idx == 0:
      spawn_group = "insideSpawnPoints"
    elif player_idx == 1:
      spawn_group = "spawnPoints"

    game_object = create_avatar_object(player_idx,
                                       TARGET_SPRITE_SELF,
                                       spawn_group=spawn_group)
    avatar_objects.append(game_object)

  return avatar_objects


def get_config():
  """Default configuration for training on the commons_harvest level."""
  config = config_dict.ConfigDict()

  # Action set configuration.
  config.action_set = ACTION_SET
  # Observation format configuration.
  config.individual_observation_names = [
      "RGB",
      "READY_TO_SHOOT",
  ]
  config.global_observation_names = [
      "WORLD.RGB",
  ]

  # The specs of the environment (from a single-agent perspective).
  config.action_spec = specs.action(len(ACTION_SET))
  config.timestep_spec = specs.timestep({
      "RGB": specs.OBSERVATION["RGB"],
      "READY_TO_SHOOT": specs.OBSERVATION["READY_TO_SHOOT"],
      # Debug only (do not use the following observations in policies).
      "WORLD.RGB": specs.rgb(144, 192),
  })

  # The roles assigned to each player.
  config.valid_roles = frozenset({"default"})
  config.default_player_roles = ("default",) * 2

  return config


def build(
    roles: Sequence[str],
    config: config_dict.ConfigDict,
) -> Mapping[str, Any]:
  """Build substrate definition given player roles."""
  del config
  num_players = len(roles)
  # Build the rest of the substrate definition.
  substrate_definition = dict(
      levelName="commons_harvest",
      levelDirectory="meltingpot/lua/levels",
      numPlayers=num_players,
      # Define upper bound of episode length since episodes end stochastically.
      maxEpisodeLengthFrames=5000,
      spriteSize=8,
      topology="BOUNDED",  # Choose from ["BOUNDED", "TORUS"],
      simulation={
          "map": ASCII_MAP,
          "gameObjects": create_avatar_objects(roles),
          "prefabs": create_prefabs(APPLE_RESPAWN_RADIUS,
                                    REGROWTH_PROBABILITIES),
          "charPrefabMap": CHAR_PREFAB_MAP,
          "scene": create_scene(),
      },
  )
  return substrate_definition