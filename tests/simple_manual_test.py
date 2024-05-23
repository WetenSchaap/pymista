#%% Initial Connection
import pymista
import time

Stage = pymista.connect_stage("zaber")

#%% home
Stage.home()                                       # home and callibrate postion if not yet the case.

#%% Move around for fun
Stage.move_absolute((1000,1000), wait_until_idle=False)  # start moving to x,y. But do not block further excecution during movement
while Stage.is_moving():
    print(Stage.get_position())
    time.sleep(.1)

#%% Move some more
Stage.move_relative((-103,1012.21), wait_until_idle=True) # start moving by dx and dy. Wait until movement is complete
Stage.move_absolute((1000,1000), wait_until_idle=False)  # move back to original position
time.sleep(0.1)
Stage.stop()                                             # stop immediately, someones finger got crushed or something
# %%
