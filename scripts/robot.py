#!/usr/bin/env python

#robot.py implementation goes here

import rospy
import numpy
import mdp
import qlearning
import pprint
from read_config import read_config
from std_msgs.msg import Bool
from cse_190_assi_3.msg import AStarPath, PolicyList
from astar import astar

class Robot(): 
    def __init__(self):
    	# Configuration setup
	self.config = read_config()
	rospy.init_node("robot", anonymous=True)

	rospy.sleep(3)

	# Publishers
	self.astar_publisher = rospy.Publisher(
	    "/results/path_list",
	    AStarPath,
	    queue_size = 10
	)

	self.mdp_publisher = rospy.Publisher(
	    "/results/policy_list",
	    PolicyList,
	    queue_size = 10
	)

	self.sim_complete_publisher = rospy.Publisher(
	    "/map_node/sim_complete",
	    Bool,
	    queue_size = 1
	)

	path = astar(
            self.config["move_list"], 
            self.config["start"],
            self.config["goal"],
            self.config["map_size"],
	    self.config["walls"],
            self.config["pits"]
        )

	print "A* Path"
	print path
	
	rospy.sleep(2)
	for p in path:
            self.astar_publisher.publish(p)
	    rospy.sleep(0.1)

	rospy.sleep(2)

        mdp_object = mdp.mdp(	
            self.config["move_list"], 
            self.config["map_size"],
            self.config["goal"],
	    self.config["walls"],
            self.config["pits"]
        )

	oldValues = list()

	for x in range(mdp_object.height):
	    for y in range(mdp_object.width):
	        oldValues.append(mdp_object.values[x][y])
	takeNewValues = True
        while mdp_object.iteration < self.config["max_iterations"] and takeNewValues:
	    newValues = list()
	    policy = list()
	    differences = list()
	    takeNewValues = False
	    mdp_object.value_iteration()
	    newValueSum = 0
	    for x in range(mdp_object.height):
	        for y in range(mdp_object.width):
		    newValues.append(mdp_object.values[x][y])

	    for x in range(mdp_object.height):
	        for y in range(mdp_object.width):
	            policy.append(mdp_object.policy[x][y])

	    for i in range(len(newValues)):
	   	newValueSum += abs(oldValues[i] - newValues[i])

	    if (newValueSum > self.config["threshold_difference"]):
		takeNewValues = True
	    oldValues = newValues
	    self.mdp_publisher.publish(policy)
	    rospy.sleep(0.1)

	print policy
	rospy.sleep(2)

	# Q Value Learning - Final Project 
	q_object = qlearning.qlearning()
	oldQValues = 0.0
	takeNewValues = True

	while q_object.iteration < self.config["max_iterations"]:
	    newQValues = 0.0
	    difference = 0.0
	    takeNewValues = False
	    next_state = q_object.update_q_values()

	    (x, y) = q_object.position
	    
	    newQValues = sum(q_object.q_values[x][y])
		
	    difference = abs(oldQValues - newQValues)
	    print "Q Learning Iteration: "
	    print q_object.iteration
	    pprint.pprint(q_object.q_values)
	    if difference > self.config["threshold_difference"]:
		takeNewValues = True

	    oldQValues = newQValues 

	    q_object.position = next_state
	    rospy.sleep(0.1)

	self.sim_complete_publisher.publish(True)
	rospy.sleep(2)
	rospy.signal_shutdown("End")

if __name__ == '__main__':
    rt = Robot()
