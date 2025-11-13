# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import pygame
from rere_game import ReReGame
from rere_gfx import ReReGFX
from rere_sfx import ReReSFX


# setup
config = {}
config["gfx_scalefactor"] = 4
config["verbose"] = 2

# init pyagme
pygame.init()
# init clock
clock = pygame.time.Clock()
# init game engine
rereunion_game = ReReGame(config)
if not rereunion_game.setup(savegame_filename = "SAVE/SPIDYSAV.1"):
    exit(1)
# init graphics
rereunion_gfx = ReReGFX(config, rereunion_game)
# init sound effects
rereunion_sfx = ReReSFX()


run = True

rereunion_sfx.play_music("ANIM/MAIN1.SPD")

while run:

    rereunion_gfx.draw(rereunion_game)

    mouseevent = False
    mouseevent_buttondown = False
    mouseevent_buttonup = False

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                run = False
                break

        if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ]:
            mouseevent = True
            if   event.type == pygame.MOUSEBUTTONDOWN:
                mouseevent_buttondown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseevent_buttonup = True
#            mouse_pos = ( int(event.pos[0] / config["gfx_scalefactor"]), int(event.pos[1] / config["gfx_scalefactor"]) )
            mouse_pos = event.pos

    if not mouseevent:
        mouse_pos = pygame.mouse.get_pos()

    scaled_mouse_pos = ( int(mouse_pos[0] / config["gfx_scalefactor"]), int(mouse_pos[1] / config["gfx_scalefactor"]) )

    mouse_buttonstate = pygame.mouse.get_pressed()  # (False, False, False)

    rereunion_game.update(scaled_mouse_pos, mouse_buttonstate, mouseevent, mouseevent_buttondown, mouseevent_buttonup)

    sfx_to_play = rereunion_game.get_sfx()
    if sfx_to_play != None:
        rereunion_sfx.play_effect(sfx_to_play)

    if rereunion_game.background_sfx_active():
        if rereunion_sfx.background_channel.get_queue() == None:
            sfx_to_play_in_background = rereunion_game.get_background_sfx()
            if sfx_to_play_in_background!= None:
                rereunion_sfx.background_queue_add(sfx_to_play_in_background)
    else:
        rereunion_sfx.background_channel.stop()

    rereunion_game.update_anims()

    pygame.display.update()

    clock.tick(25)

