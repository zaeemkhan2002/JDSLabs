import keyboard
from robomaster import robot


def move_robot(direction):
    x_val = 0.2
    y_val = 0.2

    if direction == 'w':
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
    elif direction == 's':
        ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
    elif direction == 'a':
        ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
    elif direction == 'd':
        ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()


def main():
    global ep_chassis
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis

    print("Gaddi Saddi beja")

    try:
        while True:
            if keyboard.is_pressed('w'):
                print("Moving Aagay")
                move_robot('w')
            elif keyboard.is_pressed('s'):
                print("Moving Peeche")
                move_robot('s')
            elif keyboard.is_pressed('a'):
                print("Moving baein")
                move_robot('a')
            elif keyboard.is_pressed('d'):
                print("Moving daein")
                move_robot('d')
            elif keyboard.is_pressed('q'):
                print("Bas hogai bro")
                break
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        ep_robot.close()


if __name__ == '__main__':
    main()
