## Only issues found were as followed.
# The meteor sprite sheet for the falling blocks is in the code, but was not included as I could not figure out how to
# make the sprite resize itself for each of the differently sized meteors that are present in the game. I thought it was
# too important to have differently sized meteors, so I decided to leave the code commented out in the game, but not
# include it in the final product.
## Game details
# If you go 10 score higher than the win screen, the game will stop displaying the winner sign and let you continue to
# rack up a higher score for an infinite amount of time.
# Game has 3 levels of increasing difficulty and then infinite mode at level 3 difficulty
# Options that were added:
# 1. Levels of difficulty (Level 2 at score 25, Level 3 at score 50) Higher level = Greater meteor numbers
# 2. Scrolling level
# 3. Enemies (the meteors)
# 4. Health Bar
# 5. Timer (Counter counts up similar to a timer for each jump the player does)

##### START CODE FOR THE GAME

import pygame
import gamebox
import random
camera = gamebox.Camera(800, 600) # creates the camera box for the game to be played on


####COUNTERS FOR PLATFORMS, SCORE, ENEMIES, AND SPRITE
plat_counter = 0
enemy_meteor_counter = 0
score_counter = 0
sprite_num_frame_counter = 4
sprite_total_step_counter = 0
sprite_curr_frame_counter = 1


#####
##### CHARACTER BOXES + SPRITE SHEET
main_character_sheet = gamebox.load_sprite_sheet("man_sprite_sheet.png", 1, 4)
# meteor_sprite_sheet = gamebox.load_sprite_sheet('Meteor_sprite_new.jpg', 1, 1)
# main_character = gamebox.from_color(50, 100, "green", 20, 40)
main_character = gamebox.from_image(50,100, main_character_sheet[sprite_curr_frame_counter])
# player_box = gamebox.from_color(400,100,"blue", 25, 25)
# starting_platform = gamebox.from_color(130,400,"white", 580, 20)
#  x, y, color, width, height

platforms = [
gamebox.from_color(130,400,"white", 580, 20)
]
enemies_meteor = []

#HEALTH BAR
current_health = 100

game_on = False

def tick(keys):
    global game_on
    global plat_counter
    global current_health
    global enemy_meteor_counter
    global score_counter
    global sprite_curr_frame_counter
    global sprite_num_frame_counter
    global sprite_total_step_counter
    global main_character_sheet
    # global meteor_sprite_sheet

    ##### TITLE SCREEN
    if game_on == False:

        title_name = gamebox.from_text(400, 210, "Platformerz", 80, "red", bold=True)
        # x, y, text, size, color; optionally True/False for bold ​and italic too
        made_by = gamebox.from_text(400, 260, "By: Claudio Cela (cc5hu)", 25, "red", bold=True)
        game_rules = gamebox.from_text(400, 300, "Use the arrow keys to jump across the platforms and", 20, "red")
        game_rules1 = gamebox.from_text(400, 320, "avoid enemies. Reach the end of all the levels (Score: 75)", 20, "red")
        game_rules2 = gamebox.from_text(400, 340, "with health remaining and you will be victorious!", 20, "red")
        game_rules3 = gamebox.from_text(400, 450, "Hit SPACE to begin!",35, "red")
        game_rules4 = gamebox.from_text(400, 500, "Hit the \"p\" key at any time to end the game.", 20, "red")
        camera.draw(title_name)
        camera.draw(made_by)
        camera.draw(game_rules)
        camera.draw(game_rules1)
        camera.draw(game_rules2)
        camera.draw(game_rules3)
        camera.draw(game_rules4)
        camera.display()
    ### GAME MECHANICS
    if pygame.K_SPACE in keys:
        game_on = True

    if game_on == True:
        camera.clear('black')  # resets the camera to black background

        main_character.yspeed += 1
        main_character.y = main_character.y + main_character.yspeed

        camera.x += 4
        if pygame.K_p in keys:
            gamebox.stop_loop()  # if the p key is hit, the loop will stop and the game will end
        if pygame.K_LEFT in keys:
            main_character.x -= 7
            sprite_total_step_counter -= .3
            current_image = int(sprite_total_step_counter) % sprite_num_frame_counter
            main_character.image = main_character_sheet[current_image]
        if pygame.K_RIGHT in keys:
            main_character.x += 7
            sprite_total_step_counter +=.3
            current_image = int(sprite_total_step_counter) % sprite_num_frame_counter
            main_character.image = main_character_sheet[current_image]
        if main_character.yspeed < 0:
            main_character.image = main_character_sheet[sprite_curr_frame_counter]
        # if pygame.K_DOWN in keys:
        #     main_character.y += 5
        plat_counter += 1
        if plat_counter % 40 == 0:
            new_plat = gamebox.from_color(camera.x + random.randint(65,80), random.randint(450, 580), "white", random.randint(60, 80),random.randint(10,30))
            platforms.append(new_plat)

        enemy_meteor_counter += 1
        if enemy_meteor_counter % 30 == 0:
            new_enemy = gamebox.from_color(camera.x + random.randint(-30,100), random.randint(100, 150), "red", random.randint(20, 30),random.randint(20, 40))
            # new_enemy = gamebox.from_image(camera.x + random.randint(-50,100), random.randint(100, 150), meteor_sprite_sheet)
            enemies_meteor.append(new_enemy)

        for platform in platforms:
            if main_character.bottom_touches(platform):
                main_character.yspeed = 0
                if pygame.K_UP in keys and main_character.yspeed == 0:  # or pygame.K_a in keys:
                    main_character.yspeed = -15
                    score_counter += 1
                    main_character.image = main_character_sheet[sprite_curr_frame_counter]
            if main_character.touches(platform):
                main_character.move_to_stop_overlapping(platform)
                main_character.move_speed()
            camera.draw(platform)
        for enemy in enemies_meteor:
            enemy.yspeed += 10
            enemy.y = enemy.yspeed
            camera.draw(enemy)
            # if main_character.x < enemy.x:
            #     enemy.x -= 3
            # if enemy.x > enemy.x:
            #     enemy.x += 3
            if enemy.touches(main_character):
                current_health -= 2.5
                if current_health <= 0:
                    camera.draw(gamebox.from_text(camera.x, 580, 'The meteor didn\'t want to cuddle.', 40, "red", italic=True))
                    gamebox.pause()

        health_bar = gamebox.from_text(camera.x + 280, 50,'Health: '+str(current_health) + '%', 40, "red")
        camera.draw(health_bar)

        score_counter_text = gamebox.from_text(camera.x - 300, 50, 'Score: ' + str(score_counter), 40, "red")
        camera.draw(score_counter_text)

        camera.draw(main_character)
        camera.display()

        if score_counter > 25:
            level_num = gamebox.from_text(camera.x + 320, 570, 'Level: 2', 40, "red")
            camera.draw(level_num)
            camera.display()
            if enemy_meteor_counter % 30 == 0:
                new_enemy = gamebox.from_color(camera.x + random.randint(-120,-65), random.randint(60, 100), "red",
                                               random.randint(20, 30), random.randint(20, 40))
                # new_enemy = gamebox.from_image(camera.x + random.randint(-50,100), random.randint(100, 150), meteor_sprite_sheet)
                enemies_meteor.append(new_enemy)
        if score_counter > 50:
            black_box = gamebox.from_color(camera.x +320, 570, "black", 100, 40)
            camera.draw(black_box)
            level_num = gamebox.from_text(camera.x + 320, 570, 'Level: 3', 40, "red")
            camera.draw(level_num)
            camera.display()
            if enemy_meteor_counter % 30 == 0:
                new_enemy = gamebox.from_color(camera.x + random.randint(-250, 250), random.randint(60, 100), "red",
                                               random.randint(20, 30), random.randint(20, 40))
                # new_enemy = gamebox.from_image(camera.x + random.randint(-50,100), random.randint(100, 150), meteor_sprite_sheet)
                enemies_meteor.append(new_enemy)


        if main_character.y >= camera.y + 400:
            camera.draw(gamebox.from_text(camera.x,580,'You didn\'t bounce.', 40, "red", italic=True))
            camera.display()
            # this line will end the game
            gamebox.pause()
        if main_character.x <= camera.x -450:
            camera.draw(gamebox.from_text(camera.x,580,'You couldn\'t keep up.', 40, "red", italic=True))
            camera.display()
            # this line will end the game
            gamebox.pause()
        if score_counter > 75 and score_counter < 85:
            camera.draw(gamebox.from_text(camera.x,100,'WINNER WINNER CHICKEN DINNER.', 60, "red", italic=True))
            camera.display()
        if score_counter > 85:
            camera.draw(gamebox.from_color(camera.x + 320, 570, "black", 120, 40))
            camera.draw(gamebox.from_text(camera.x + 270, 570, 'Level: INFINITE', 40, "red"))
            camera.display()



gamebox.timer_loop(30, tick)
# loops the keys/functions a certain number of times a second (30 frames per second) when the game is played
