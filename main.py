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
jump = False
stop = False
slide = False
spikes = []


# Colours
orange = (252, 156, 13)
black = (90, 90, 90)
white = (235, 232, 237)
red = (255, 0, 0)
not_lit_up = (0, 0, 0)

def update_time():
    global time
    global stop

    while stop == False:
        sleep(1)
        time += 1


def clear_penguin_normal():
    sense.set_pixel(penguin_position[0], penguin_position[1], not_lit_up)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], not_lit_up)
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

    jump = True
    clear_penguin_normal()
    penguin_position = [1, 4]
    draw_penguin()
    
    sleep(1.6)
    clear_penguin_normal()
    penguin_position = [1, 5]
    draw_penguin()
    
    sleep(0.2)
    clear_penguin_normal()
    penguin_position = [1, 6]
    draw_penguin()

    jump = False

def penguin_slide():
    global slide
    global speed
    global penguin_position

    slide = True

    clear_penguin_normal()
    sense.set_pixel(penguin_position[0], penguin_position[1], orange)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], white)
    sense.set_pixel(penguin_position[0] + 2, penguin_position[1] - 1, black)
    sleep(1.2)
    clear_penguin_slide()

    draw_penguin()
    slide = False


def draw_penguin():
    sense.set_pixel(penguin_position[0], penguin_position[1], black)
    sense.set_pixel(penguin_position[0] + 1, penguin_position[1], orange)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 1, white)
    sense.set_pixel(penguin_position[0], penguin_position[1] - 2, black)


def generate_spike():
    global spikes
    while stop == False:
        sleep(randint(1000, 1200) / 100)
        output = randint(0, 1)
        spikes.append([output, 8, output + 4, 0])


def update_spikes():
    global spikes
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
    print(spikes)
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


def game():
    global jump
    global speed

    draw_penguin()
    while stop == False:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up" and jump == False:
                    penguin_jump()

                if event.direction == "down" and slide == False:
                    penguin_slide()

                if event.direction == "left" and (speed - speed_min) >= 0.1:
                    speed -= 0.1
                
                if event.direction == "right" and (speed_max - speed) >= 0.1:
                    speed += 0.1


def main():
    sense.clear()
    update_time_thread = Thread(target = update_time)
    game_thread = Thread(target = game)
    update_spike_thread = Thread(target = update_spikes)
    generate_spikes_thread = Thread(target = generate_spike)

    generate_spikes_thread.start()
    update_spike_thread.start()
    update_time_thread.start()
    game_thread.start()
      
main()
