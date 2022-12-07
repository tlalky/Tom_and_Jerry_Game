import pygame
from pygame.locals import *
import random
import re

size = width, height = (1200, 800)  # size of the screen
road_w = int(width / 1.6)  # width of the road
roadmark_w = int(width / 80)  # width of the lines on road
right_lane = width / 2 + road_w / 4  # location on right side of the road
left_lane = width / 2 - road_w / 4  # location on left side of the road
speed = 5  # speed of Tom on the beginning of game
score_value = 0  # score value displayed in the game
counter = 0  # counter used to speed up the game and update score
clock = pygame.time.Clock()

pygame.init()  # initialize all imported pygame modules

font = pygame.font.Font("freesansbold.ttf", 32)  # font to display score
running = True  # variable controlling if game is running

screen = pygame.display.set_mode(size)  # set size of screen using size variable
pygame.display.set_caption("Tom & Jerry Game")  # set title on top of the screen

jerry = pygame.image.load("jerry.png")  # load Jerry image
jerry_loc = jerry.get_rect()  # Jerry location
jerry_loc.center = right_lane, height * 0.85  # set Jerry center location

tom = pygame.image.load("tom.png")  # load Tom image
tom_loc = tom.get_rect()  # Tom location
tom_loc.center = left_lane, height * 0.2  # set Tom center location

tree = pygame.image.load("tree.png")  # load tree image
tree_loc = tree.get_rect()  # tree location

while running:  # main loop of the game
    clock.tick(60)  # 60 FPS
    screen.fill((60, 220, 0))  # set background color
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    tom_loc[1] += speed  # increase speed and difficulty as the game progresses
    counter += 1  # counter used to display score and speed up the game
    if counter % 100 == 0:  # update the score as the game progresses
        score_value += 1
    if counter == 800:  # increase speed and reset the counter
        speed += 1
        counter = 0
        print("Level up! Speed = ", speed)  # print increased difficulty
    if tom_loc[1] > height - 50:  # if Tom goes under the Jerry
        if random.randint(0, 1) == 0:  # generate randomly 0 or 1 and if it is 0
            tom_loc.center = right_lane, -200  # spawn Tom on right lane on top of the screen
        else:
            tom_loc.center = left_lane, -200  # spawn Tom on left lane on top of the screen
    # if Tom and Jerry are on same lane and Tom is touching Jerry end the game
    if jerry_loc[0] == tom_loc[0] and tom_loc[1] > jerry_loc[1] - 200:
        print("GAME OVER! Score:", score_value)  # print acquired score
        break

    for event in pygame.event.get():  # get events from the queue
        if event.type == QUIT:  # if event is quit
            running = False  # exit while loop
        if event.type == KEYDOWN:  # all keys on keyboard
            if event.key in [K_a, K_LEFT]:  # select only A and LEFT key
                if jerry_loc[0] > width / 2:  # check if Jerry is on right lane, prevent from going over the road
                    jerry_loc = jerry_loc.move([-road_w // 2, 0])  # move Jerry to left lane
            if event.key in [K_d, K_RIGHT]:  # select only D and RIGHT key
                if jerry_loc[0] < width / 2:  # check if Jerry is on left lane, prevent from going over the road
                    jerry_loc = jerry_loc.move([road_w // 2, 0])  # move Jerry to right lane

    pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height)) # black road in center of screen
    for i in range(0, height, 80):  # to draw dashed line -> for loop and draw.rect() method
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - roadmark_w / 2, i, roadmark_w, 40))  # line in the middle
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2, 0, roadmark_w, height))  # right borderline
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2, 0, roadmark_w, height))  # left borderline

    # TREES
    x = [width / 9, width - 100, width - 100, width / 9]  # list of X coordinates of trees
    y = [height * 0.5, height * 0.3, height * 0.7, height * 0.1]  # list of Y coordinates of trees
    for i in range(len(x)):  # loop through all of trees
        tree_loc.center = x[i], y[i]  # set center location for each tree
        screen.blit(tree, tree_loc)  # draw tree

    screen.blit(jerry, jerry_loc)  # draw Jerry
    screen.blit(tom, tom_loc)  # draw Tom
    screen.blit(score, (width - width / 6, 10))  # draw score
    pygame.display.update()  # update the screen

pygame.quit()  # uninitialize all pygame modules

if score_value >= 50:  # set minimal score to be saved to record list
    name = input("Enter your name to save your score to record base: ")  # ask for name to save
    infile = open("records.txt", "a")  # open file in append mode
    infile.write(f"\n{name}:{score_value}")  # write file with given name and score
    print("Score successfully saved in database!")  # print confirmation
    infile = open('records.txt', 'r')   # open in read mode
    high = 0    # set lowest possible value
    for line in infile:  # go through all lines
        line = re.sub('^.*:', '', line).strip('\n')  # regex to match ":" sign and then remove "\n" sign
        if int(line) > high:    # compare
            high = int(line)    # set new high score to highest value
    infile.close()  # close file
    print(f'Current high score: {high}')  # display highest score


