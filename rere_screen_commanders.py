# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_commanders(screen):

    def __init__(self, gamedata_dynamic):

        self.screentype = "commanders"

        menu_icons = [ "BACK TO M.SCREEN", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS", "HIRE MAN" ]
        menu_text  = [ "BACK TO M.SCREEN", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS", "HIRE MAN" ]
        menu_sfx   = [ "BACK", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPE", "WELCOME" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = False
        self.current_commanders = 'PILOTS'


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        [ menuaction, _ ] = self.get_action()
        if menuaction != None:
            if menuaction in [ "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS" ]:
                self.current_commanders = menuaction
            else:
                self.action = menuaction

        # Level 1 commander
        if 49 <= mouse_pos[1] <= 49+96 and 0 <= mouse_pos[0] <= 102:

            self.menu_info["actiontext"] = "L1 commander"
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "TALK"
