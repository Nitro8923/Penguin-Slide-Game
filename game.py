from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

# Variables
speed = 0.5
speed_min = 0.2
speed_max = 0.8
penguin_position = [1, 6]
time = 0

# Colours
orange = (252, 156, 13)
black = (0, 0, 0)
white = (235, 232, 237)

def draw_penguin():
  sense.set_pixel(penguin_position[0], penguin_position[1], black)
  sense.set_pixel(penguin_position[0] + 1, penguin_position[1], orange)
  sense.set_pixel(penguin_position[0], penguin_position[1] - 1, white)
  sense.set_pixel(penguin_position[0], penguin_position[1] - 2, black)

def update_spikes():
  pass

def update_coins():
  pass

def update_time():
    sleep(1)
    time += 1

def main():

      
main()