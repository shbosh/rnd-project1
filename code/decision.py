import numpy as np

# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):
    if Rover.nav_angles is not None:
        if Rover.mode == 'forward':
            forward_loop(Rover)
        elif Rover.mode == 'stop':
            stop_loop(Rover)
        elif Rover.mode == 'stuck':
            stuck_loop(Rover)
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True

    return Rover

def forward_loop(Rover):
    #print("In forward mode:")
    if is_vision_data_available(Rover):
        if (Rover.vel <= 0.2):
            print("Rover stuck", Rover.stop_time)
            Rover.stop_time += 1
        else:
            Rover.stop_time = 0

        if (Rover.throttle >= 0 and Rover.vel <= 0.2 and Rover.stop_time > Rover.max_stop_time):
            print("Rover stuck. Steering right...")
            steer_right(Rover)

        move_and_hug_left_wall(Rover)
    else:
        print("Terrain not unnavigable, stop mode activated.")
        stop_moving(Rover)
        Rover.mode = 'stop'


def stop_loop(Rover):
    print("In stop mode:")
    if Rover.vel > 0.2:
        stop_moving(Rover)
    elif Rover.vel <= 0.2:
        if is_vision_data_available(Rover):
            print("Vision data is available.")
            move_and_hug_left_wall(Rover)
            Rover.mode = 'forward'
            Rover.stop_time = 0
        else:
            steer_right(Rover) # Could be more clever here about which way to turn

def stuck_loop(Rover):
    print("Rover stuck. Steering right...")
    steer_right(Rover)

def is_vision_data_available(Rover):
    return len(Rover.nav_angles) >= Rover.go_forward

def stop_moving(Rover):
    print("Braking...")
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    Rover.steer = 0

def steer_right(Rover):
    print("Steering right...")
    Rover.throttle = 0
    Rover.brake = 0
    Rover.steer = -15

def move_and_hug_left_wall(Rover):
    #print("Terrain navigable, moving forward...")
    if Rover.vel < Rover.max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    Rover.brake = 0
    Rover.steer = np.clip(np.mean(get_near_nav_angles(Rover)) * 180/np.pi + 13, -15, 15)

def get_near_nav_angles(Rover):
    valid_nav_angles = []
    valid_value_indices = [i for i,v in enumerate(Rover.nav_dists) if v <= 60]
    for v in valid_value_indices:
        valid_nav_angles.append(Rover.nav_angles[v])
    print("angles ", np.mean(Rover.nav_angles))
    print("valid ", np.mean(valid_nav_angles))
    return valid_nav_angles
