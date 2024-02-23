# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_spacelocal(screen):

    def __init__(self, gamedata_dynamic):

        self.screentype = "spacelocal"

        menu_icons = [ "BACK TO M.SCREEN" ]
        menu_text  = [ "BACK TO M.SCREEN" ]
        menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = True
        self.add_anim("greenlights",     21, 2, 1)
        self.add_anim("lavalampa",        5, 1, 1)
        self.add_anim("kartyazoszormok", 14, 2, 1) #, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("hatsoatjaro",     13, 2, 1)
        self.add_anim("kisasztal1",      14, 2, 1) #, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("kisasztal2",      15, 2, 1) #, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("rosszlampa",      12, 2, 1) #, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("rossztv",          5, 2, 1)
        self.add_anim("zagyva",          15, 2, 1)
        self.add_anim("nagyasztal",      32, 2, 1) #, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("knightrider",     18, 2, 1)


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        # Bartender
        if 28+49 <= mouse_pos[1] <= 49+96 and 32 <= mouse_pos[0] <= 84:

            self.menu_info["actiontext"] = "Bartender"
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "TALK"

        # Informer
        elif 80+49 <= mouse_pos[1] <= 199 and 0 <= mouse_pos[0] <= 74:

            self.menu_info["actiontext"] = "Informer"
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "TALK"

        # Spy-Hunter
        elif 11+49 <= mouse_pos[1] <= 200 and 279 <= mouse_pos[0] <= 319:

            self.menu_info["actiontext"] = "Spy-Hunter"
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "TALK"

        # 
#        elif +49 <= mouse_pos[1] <= +49+ and  <= mouse_pos[0] <= +46:
#
#            self.menu_info["actiontext"] = ""
#            if mouse_buttonevent[0]:  # mouse button pressed
#                self.sfx_to_play = "TALK"
#
