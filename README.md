# pymista

Pymista (Python Microscopy Stage) is a Python module to control an electronic stage, especially, but not nessecarily, for microscopy. It's goal is to provide a universal programming interface for different stages, hiding complexities a specific producer may introduce.

It is really only intended for use in our lab, but who knows, maybe it is usefull to someone else out there.

The general procedure for usage would be:

``` python
with connect_stage("zaber") as Stage:
    Stage.home()                                       # home and callibrate postion if not yet the case.
    Stage.move_absolute((x,y), wait_until_idle=False)  # start moving to x,y. But do not block further excecution during movement
    x,y = Stage.get_position()                         # get current position
    Stage.move_relative((dx,dy), wait_until_idle=True) # start moving by dx and dy. Wait until movement is complete
    Stage.move_absolute((x,y), wait_until_idle=False)  # move back to original position
    Stage.stop()                                       # stop immediately, someones finger got crushed or something
    Stage.wait_until_idle()                            # wait until no longer moving
```
Where we move a Zaber-brand stage around.

Units of distance are always given in micrometers!

## Currently implemented stages:

- Dummystage - a fake stage, usefull for troubleshoothing
- [Zaber](https://www.zaber.com) - all-in-one easy stages.

Implementing more stages is (or should be) not so difficult. I will only add things I use/need, beacuse this is mostly for use in our lab. If you want/need to add your own stage, you can always ask me for help.

## Installation

Note that this module is designed such that you do *not* need all packages to control all stages, even if you don't have this particular brand. Instead, you specify which stages you have, and thus which packages you need/want. We use 'extras' for that. Possible extras are:

- `zaber` - For zaber stages.
- `test`  - For testing.

Since this module is not added to Pypi (yet), you will have to install it manually from this repo. In the examples, below we include the `zaber` extra. 

Using *pip*, run:
``` bash
python -m pip install -e "pymista[zaber] @ git+https://github.com/WetenSchaap/pymista.git"
```

Using, *poetry*, you can add the following to your `pyproject.toml`:

``` toml
pymista = { git = "https://github.com/WetenSchaap/pymista.git", extras = ["zaber"]}
```

## Accessing and edditing stage settings

Settings are not so easy to harmonize between different brands because of different kind of settings, units, etc. That means that until I spend time on this, you will probably need to do this all by yourself.

There is one exception: the min and max location of the stage, since this is really quite important. It can be accessed directly via ´Stage.get_bounds()´.

other settings you can get/set by doing

``` python
Stage.settings_get(SETTING, UNIT)
# or
Stage.settings_set(SETTING, VALUE, UNIT)
```
where SETTING is the setting name (say 'limit.max'), find [here for zaber for instance](https://www.zaber.com/protocol-manual#topic_settings), UNIT is the unit (defaults to µm if but this is sometimes just wrong!) and VALUE is the value to set the setting to.


## Internal workings

A stage contains axis. Typically, there are 2 or 3 axis (x,y,z). 

The axis object is shaped after the [zaber axis object](https://software.zaber.com/motion-library/api/py/ascii/axis), so it should contain the same basic functionality, or the stage object cannot work.

