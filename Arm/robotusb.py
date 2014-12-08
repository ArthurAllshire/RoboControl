import usb.core, usb.util

RoboArm = None

#list of commands that can be sent over usb to the arm
commands = {
'BASE_AC' : [ 0,1,0], 'BASE_CL' : [  0,2,0],
'SLDR_UP' : [64,0,0], 'SLDR_DN' : [128,0,0],
'ELBW_UP' : [16,0,0], 'ELBW_DN' : [ 32,0,0],
'WRST_UP' : [ 4,0,0], 'WRST_DN' : [  8,0,0],
'GRIP_OP' : [ 2,0,0], 'GRIP_CS' : [  1,0,0],
'LIGT_ON' : [ 0,0,1], 'LIGT_OF' : [  0,0,0],
}

# Define a procedure to execute each movement
def MoveArm(ArmCmd):
    global RoboArm, commands
    if RoboArm is None:
        RoboArm = usb.core.find(idVendor=0x1267,idProduct=0x0000)
        if RoboArm is None:
            raise ValueError("Robot arm not found")
    # Start the movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,commands[ArmCmd], 1000)

def StopArm():
    global RoboArm
    if RoboArm is None:
        RoboArm = usb.core.find(idVendor=0x1267,idProduct=0x0000)
        if RoboArm is None:
            raise ValueError("Robot arm not found")
    RoboArm.ctrl_transfer(0x40,6,0x100, 0,[0,0,0],1000)
