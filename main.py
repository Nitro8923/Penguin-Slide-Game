from sense_emu import SenseHat
from threading import Thread
from time import sleep
from random import randint
import pygame


sense = SenseHat()

# Variables
speed = 0.4
speed_min = 0.2
speed_max = 0.6
penguin_position = [1, 6]
time = 0
jump = [False, 0]
stop = False
slide = [False, 0]
spikes = []


# Colours
orange = (252, 156, 13)
black = (90, 90, 90)
white = (235, 232, 237)
red = (255, 0, 0)
not_lit_up = (0, 0, 0)
floor = (255, 255, 255)

def update_time():
    global time
    global stop

    while stop == False:
        sleep(1)
        time += 1


def update_speed():
    global speed
    global speed_max
    global speed_min
    global stop
    while stop == False:
        sleep(10)
        if not 1 - speed_max == 0.1:
            speed += 0.05
            speed_max += 0.05
            speed_min += 0.05


def draw_penguin_slide():
    sense.set_pixel(penguin_position[0], penguin_position[1], orange)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], white)
    sense.set_pixel(penguin_position[0] + 2, penguin_position[1] - 1, black)


def draw_penguin_jump():
    sense.set_pixel(penguin_position[0], penguin_position[1], black)
    sense.set_pixel(penguin_position[0], penguin_position[1] + 1, orange)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 1, white)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 2, black)


def draw_penguin_normal():
    sense.set_pixel(penguin_position[0], penguin_position[1], black)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], orange)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 1, white)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 2, black)


def clear_penguin_normal():
    sense.set_pixel(penguin_position[0], penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 1, not_lit_up)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 2, not_lit_up)


def clear_penguin_jump():
    sense.set_pixel(penguin_position[0], penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0], penguin_position[1] + 1, not_lit_up)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 1, not_lit_up)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 2, not_lit_up)


def clear_penguin_slide():
    sense.set_pixel(penguin_position[0], penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0] + 2, penguin_position[1] - 1, not_lit_up)


def penguin_jump():
    global jump
    global speed
    global penguin_position

    jump[0] = True
    jump[1] = 1
    clear_penguin_normal()
    penguin_position = [1, 3]
    draw_penguin_jump()
    
    sleep(1.7)
    jump[1] = 2
    clear_penguin_jump()
    penguin_position = [1, 4]
    draw_penguin_jump()

    sleep(0.2)
    clear_penguin_normal()
    penguin_position = [1, 6]
    draw_penguin_normal()

    jump[1] = 0
    jump[0] = False


def penguin_slide():
    global slide
    global speed
    global penguin_position

    slide[0] = True
    slide[1] = 1
    clear_penguin_normal()
    draw_penguin_slide()
    sleep(2)

    slide[1] = 0
    clear_penguin_slide()
    draw_penguin_normal()
    slide[0] = False


def generate_spike():
    global spikes
    global stop
    while stop == False:
        sleep(randint(400, 600) / 100)
        output = randint(0, 1)
        if output == 0:
            spikes.append([output, 8, 5, 0])
            spikes.append([output, 8, 6, 0])
        elif output == 1:
            spikes.append([output, 8, 4, 0])
            spikes.append([output, 8, 3, 0])
            spikes.append([output, 8, 2, 0])
            spikes.append([output, 8, 1, 0])
            spikes.append([output, 8, 0, 0])
        

def update_spikes():
    global spikes
    global stop
    while stop == False:
        for i in range(len(spikes)):
            move_spike(i)
        while True:
            for i in range(len(spikes)):
                if spikes[i][3] == 1:
                    spikes.pop(i)
                    break
            else:
                break
        sleep(1 - speed)


def move_spike(spike):
    global spikes
    if spikes[spike][1] == 8:
        spikes[spike][1] -= 1
        sense.set_pixel(spikes[spike][1], spikes[spike][2], red)
    elif spikes[spike][1] == 0:
        sense.set_pixel(spikes[spike][1], spikes[spike][2], not_lit_up)
        spikes[spike][3] = 1
    else:
        sense.set_pixel(spikes[spike][1], spikes[spike][2], not_lit_up)
        spikes[spike][1] -= 1
        sense.set_pixel(spikes[spike][1], spikes[spike][2], red)


def test_collisions():
    global stop
    while stop == False:
        for spike in spikes:
            if jump[0] == True:
                if jump[1] == 1 or jump[1] == 2:
                    if (spike[1] == penguin_position[0] and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 1) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] + 1) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 2):
                        stop = True
                elif jump[1] == 3:
                    if (spike[1] == penguin_position[0] and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 1) or (spike[1] == penguin_position[0] + 1 and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 2):
                        stop = True
            elif slide[0] == True:
                if (spike[1] == penguin_position[0] and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] + 2 and spike[2] == penguin_position[1] - 1) or (spike[1] == penguin_position[0] + 1 and spike[2] == penguin_position[1]):
                    stop = True
            else:
                if (spike[1] == penguin_position[0] and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 1) or (spike[1] == penguin_position[0] + 1 and spike[2] == penguin_position[1]) or (spike[1] == penguin_position[0] and spike[2] == penguin_position[1] - 2):
                    stop = True


def game():
    global jump
    global speed
    global stop
    for i in range(8):
        sense.set_pixel(i, 7, floor)
    draw_penguin_normal()


    while stop == False:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up" and jump[0] == False:
                    penguin_jump()

                if event.direction == "down" and slide[0] == False:
                    penguin_slide()

                if event.direction == "left" and (speed - speed_min) >= 0.1:
                    speed -= 0.1
                
                if event.direction == "right" and (speed_max - speed) >= 0.1:
                    speed += 0.1
    
    you_lost()


def you_lost():
    global time
    sense.clear()
    with open("record.txt", "r") as file:
        high_score = file.read()

    if time > int(high_score):
        with open("record.txt", "w") as file:
            file.write(str(time))
    sense.show_message("You survived " + str(time) + " seconds")



def main():
    global stop
    sense.clear()
    update_time_thread = Thread(target = update_time)
    game_thread = Thread(target = game)
    update_spike_thread = Thread(target = update_spikes)
    generate_spikes_thread = Thread(target = generate_spike)
    test_collisions_thread = Thread(target = test_collisions)
    update_speed_thread = Thread(target = update_speed)

    update_speed_thread.start()
    test_collisions_thread.start()
    generate_spikes_thread.start()
    update_spike_thread.start()
    update_time_thread.start()
    game_thread.start()

    if stop == True:
        update_speed_thread.join()
        test_collisions_thread.join()
        generate_spikes_thread.join()
        update_spike_thread.join()
        update_time_thread.join()
        game_thread.join()

if __name__ == "__main__":
    main()
