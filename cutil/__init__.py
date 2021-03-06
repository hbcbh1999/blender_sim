#!/usr/bin/env python

from os.path import dirname, basename, isfile
import glob
import sys
import traceback
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
skipping_ros = False
ros_mods = ["rosbag", "roslib", "rospy", "sensor_msgs"]
for f in modules:
    if isfile(f) and "__init__" not in f and "install" not in f:
        try:
            exec('from %s import *' % basename(f)[:-3])
        except Exception as e:
            if basename(f)[:-3] == 'drawing':
                continue
            #err = traceback.format_exc()
            err = str(e)
            if err.startswith("No module named"):
                found = False
                for ros_mod in ros_mods:
                    if ros_mod in err[15:]:
                        found = True
                if found:
                    skipping_ros = True
                    continue
            raise
if skipping_ros:
    print("Package cutil: Skipping ROS imports.")
