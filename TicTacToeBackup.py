from sre_constants import BRANCH
import time
import random
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

n.calibrate_auto()

global score_grid, totalScore, tempCords
global gameEnd, redCirBool, greenCirBool, blueCirBool, redSquareBool
global zero, one, two, three, four, five, six, seven, eight

try:
    gameEnd,redCirBool, greenCirBool, blueCirBool, redSquareBool = False

    tempCords = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    zero = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    one = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    two = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    three = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    four = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    five = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    six = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    seven = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    eight = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    #Int based grid to represent spots taken on grid
    score_grid = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ]

    def startGame(): #FIXXXXXXXXXXXXXXXXXXXXXX
        pickUpFromStack()
        n.move_pose(0.160, -0.061, 0.079, 0, 1.57, 0) #AI will start in bottom right corner everytime. GET UPDATED CORDS FOR ALL SPOTS FOR ROBOT
        n.push_air_vacuum_pump()
        updateBoardFromAi(8)
        n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496) #Move to observation Pose

    def updateBoardFromAi(cordsInt):
        score_grid[cordsInt] = -1
        totalScore = totalScore + 1

    def placePeice(cords):

        if cords == 0:
            tempCords = zero[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 1:
            tempCords = one[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 2:
            tempCords = two[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif tempCords == 3:
            tempCords = three[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 4:
            tempCords = four[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 5:
            tempCords = five[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 6:
            tempCords = six[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        elif cords == 7:
            tempCords = seven[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])
        else:
            tempCords = eight[:]
            n.move_pose(tempCords[0], tempCords[1], tempCords[2], tempCords[3], tempCords[4], tempCords[5])


    def pickUpFromStack():
        #Find adjusted height after each peice is picked up.
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Move to AI's stack of objects.
        n.pull_air_vacuum_pump()
        n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496) #Move to observation Pose

    def scanBoard():
        n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496) #Move to observation pose.
        time.sleep(15)
        while True:
            if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.RED)[0] & redCirBool == False:#If red circle is found on board and is not known about
                if n.move_to_object('default_workspace', 0, ObjectShape.CIRCLE, ObjectColor.RED):
                    tempCords = n.get_pose_as_list()
                    findSpotAndUpdate()
                totalScore = totalScore + 1
                redCirBool = True
                break
            elif n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.RED)[0] & redCirBool == True: #If red circle is found on board and is known about already

                if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0] & greenCirBool == False:#If green circle is found on board and is not known about
                    if n.move_to_object('default_workspace', 0, ObjectShape.CIRCLE, ObjectColor.RED):
                        tempCords = n.get_pose_as_list()
                        findSpotAndUpdate()
                    totalScore = totalScore + 1
                    greenCirBool = True
                    break
                elif n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0] & greenCirBool == True:#If green circle is found on board and is known about already
                    n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496) #Move to observation pose.

                    if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.BLUE)[0] & blueCirBool == False: #If blue circle is found on board and is not known about
                        if n.move_to_object('default_workspace', 0, ObjectShape.CIRCLE, ObjectColor.RED):
                            tempCords = n.get_pose_as_list()
                            findSpotAndUpdate()
                        totalScore = totalScore + 1
                        blueCirBool = True
                        break
                    elif n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.BLUE)[0] & blueCirBool == True:#If blue circle is found on board and is known about already
                        n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496) #Move to observation pose.

                        if n.detect_object('default_workspace', ObjectShape.SQUARE, ObjectColor.RED)[0] & redSquareBool == False:#If red square is found on board and is not known about
                            if n.move_to_object('default_workspace', 0, ObjectShape.CIRCLE, ObjectColor.RED):
                                tempCords = n.get_pose_as_list()
                                findSpotAndUpdate()
                            totalScore = totalScore + 1
                            redSquareBool = True
                            break
                        else:
                            break #End of all possible player peices.

        def findSpotAndUpdate():
            if  (tempCords[0] < 0.200) & (tempCords[0] > 0.100) :  #figure out row. (Top row)
                #n.move_joints(-0.002, 0.601, -0.648, 0.000, -1.348, 1.496)
                if (tempCords[1] < -0.030) & (tempCords[1] >= -0.080): #spot 0
                    score_grid[0] = 1
                elif (tempCords[1] <= 0.025 ) & (tempCords[1] >= -0.020):#spot 1
                    score_grid[1] = 1
                else:                                                         #spot 2
                    score_grid[2] = 1
                    

            if  (tempCords[0] > 0.205) & (tempCords[0] < 0.250):  #figure out row. (Middle row)
                if (tempCords[1] < -0.030) & (tempCords[1] >= -0.080): #spot 3
                    score_grid[3] = 1
                elif (tempCords[1] <= 0.025 ) & (tempCords[1] >= -0.020):#spot 4
                    score_grid[4] = 1
                else:
                    score_grid[5] = 1                                    #spot 5


            if  (tempCords[0] < 0.300) & (tempCords[0] > 0.255) :  #figure out row. (Bottom row)
                if (tempCords[1] < -0.030) & (tempCords[1] >= -0.080): #spot 6
                    score_grid[6] = 1
                elif (tempCords[1] <= 0.025 ) & (tempCords[1] >= -0.020):#spot 7
                    score_grid[7] = 1
                else:
                    score_grid[8] = 1
   
                            
    def placePeiceLogic():
        num = random.randint(0, 7)

        while score_grid[num] != 0:
            num = random.randint(0, 7)
        
        placePeice(num)
        updateBoardFromAi(num)


    
    def checkGameEnd():
        #All spots are taken up.
        if totalScore >= 9: #All spots have been taken up.
            n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
            #Place holder to make the robot do a little dance or something.


        if score_grid[0] == score_grid[3] == score_grid[6] & gameEnd == False: #Vertical Win
            n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
            gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[1] == score_grid[4] == score_grid[7] & gameEnd == False: #Vertical Win
            n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
            gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[2] == score_grid[5] == score_grid[8] & gameEnd == False: #Vertical Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[0] == score_grid[1] == score_grid[2] & gameEnd == False: #Horizontal Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[3] == score_grid[4] == score_grid[5] & gameEnd == False: #Horizontal Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[6] == score_grid[7] == score_grid[8] & gameEnd == False: #Horizontal Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[0] == score_grid[4] == score_grid[8] & gameEnd == False: #Diagonal Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


        if score_grid[2] == score_grid[4] == score_grid[6] & gameEnd == False: #Horizontal Win
             n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
             gameEnd = True
            #Place holder to make the robot do a little dance or something.


    def cleanUp():
        if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.RED)[0]:
            n.vision_pick_w_obs_joints('default_workspace', -5/1000.0, ObjectShape.CIRCLE, ObjectColor.RED, [-0.002, 0.601, -0.648, 0.000, -1.348, 1.496])
            #move to player spot

        if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0]):
            n.vision_pick_w_obs_joints('default_workspace', -5/1000.0, ObjectShape.CIRCLE, ObjectColor.GREEN, [-0.002, 0.601, -0.648, 0.000, -1.348, 1.496])
            #move to player spot

        if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0]):
            n.vision_pick_w_obs_joints('default_workspace', -5/1000.0, ObjectShape.CIRCLE, ObjectColor.BLUE, [-0.002, 0.601, -0.648, 0.000, -1.348, 1.496])
            #move to player spot

        if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0]):
            n.vision_pick_w_obs_joints('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.RED, [-0.002, 0.601, -0.648, 0.000, -1.348, 1.496])
            #move to player spot

        num = 0

        while num <= 8:
            if score_grid[num] == -1:
                n.move_pose(0.16, 0, 0.35, 0, 1.57, 0)  #PLACE HOLDER FOR PUTTING PEICE BACK INTO AI STACK.
            num = num + 1
                
    startGame()

    while gameEnd == False:
        scanBoard() #Will wait for player to place a peice, when it does, it will update the score_grid.
        placePeiceLogic() #thinks about what pawn to play next and uses placePeice() and Update from AI
        checkGameEnd() #Will check for a tie game or a winner 

    cleanUp()

    n.move_to_sleep_pose()
    n.set_learning_mode(True)

except NiryoRosWrapperException as e:
   sys.stderr.write(str(e))