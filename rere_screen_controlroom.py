# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_controlroom(screen):

    def __init__(self, gamedata_static, gamedata_dynamic):

        self.screentype = "controlroom"

        menu_icons = [ "INFO-BUY", "RESEARCH-DESIGN", "SHIP INFO", "GALACTIC MAP", "PLANET MAIN", "MESSAGES", "COMMANDERS", "SPACE LOCAL", "MESSAGES", "DISK OPERATIONS" ]
        menu_text  = [ "INFO-BUY", "RESEARCH-DESIGN", "SHIP INFO", "GALACTIC MAP", "PLANET MAIN", "MESSAGES", "COMMANDERS", "SPACE LOCAL", "MAIN COMPUTER", "DISK OPERATIONS" ]
        menu_sfx   = [ "PRODUCTI", "RESEARCH", "SHIP", "STARMAP", "SURFACE", "MESSAGES", "COMMANDE", "LOCAL", "MAINCPU", "DISK" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = True
        self.add_anim("radarscreen",   38, 2, 1)
        self.add_anim("liftpanel",     10, 2, 1)
        self.add_anim("liftlights",    16, 2, 4, delay = -1, delaymin = 4, delaymax = 16)
        self.add_anim("liftlights_up",  7, 2, 0)
        self.add_anim("liftlights_dn", 10, 2, 0)
        self.add_anim("liftdoor",       4, 2, 0)
        self.add_anim("rightdoor",      6, 2, 0)
        self.add_anim("commanderdoor",  4, 2, 0)
        self.add_anim("messagescomputer", 20, 1, 0)
        self.add_anim("researchcomputer", 26, 1, 0)

        self.commander_names = gamedata_static["commander_names"]
        self.current_commanders = self.gamedata_dynamic["commanders"]
        self.current_planet_surface = (1, 5, 0)  # New-Earth


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        if self.waitingforanim != None:

            if self.animstates[self.waitingforanim].active == 2:

                if self.waitingforanim == "rightdoor":
                    self.action = "INFO-BUY"
                    self.action_params = []
                elif self.waitingforanim in [ "liftlights_dn", "liftlights_up" ]:
                    self.waitingforanim = "liftdoor"
                    self.animstates["liftdoor"].activate(1)
                elif self.waitingforanim == "liftdoor":
                    self.action = "SHIP INFO"
                    self.action_params = []
                elif self.waitingforanim == "commanderdoor":
#                    self.action = "COMMANDERS"
                    self.action = "BACK TO M.SCREEN"
                    self.action_params = []
                elif self.waitingforanim == "messagescomputer":
                    self.action = "MESSAGES"
                    self.action_params = []
                elif self.waitingforanim == "researchcomputer":
                    self.action = "RESEARCH-DESIGN"
                    self.action_params = []


            return

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.current_commanders = self.gamedata_dynamic["commanders"]

        # Builder
        if 51+49 <= mouse_pos[1] <= 51+49+65 and 200 <= mouse_pos[0] <= 200+46:

            if self.current_commanders[1] != 0:
                self.menu_info["actiontext"] = self.commander_names[1][self.current_commanders[1] - 1]
                if mouse_buttonevent[0]:  # mouse button pressed
                    self.sfx_to_play = "BUILDERS"

        # Fighter
        elif 38+49 <= mouse_pos[1] <= 38+49+84 and 77 <= mouse_pos[0] <= 77+57:

            if self.current_commanders[2] != 0:
                self.menu_info["actiontext"] = self.commander_names[2][self.current_commanders[2] - 1]
                if mouse_buttonevent[0]:  # mouse button pressed
                    self.sfx_to_play = "FIGHTERS"

        # Developers
        elif 56+49 <= mouse_pos[1] <= 56+49+95 and 43 <= mouse_pos[0] <= 43+49:

            if self.current_commanders[3] != 0:
                self.menu_info["actiontext"] = self.commander_names[3][self.current_commanders[3] - 1]
                if mouse_buttonevent[0]:  # mouse button pressed
                    self.sfx_to_play = "DEVELOPE"

        # Pilots
        elif 54+49 <= mouse_pos[1] <= 54+49+97 and 245 <= mouse_pos[0] <= 245+50:

            if self.current_commanders[0] != 0:
                self.menu_info["actiontext"] = self.commander_names[0][self.current_commanders[0] - 1]
                if mouse_buttonevent[0]:  # mouse button pressed
                    self.sfx_to_play = "PILOTS"

        # Starmap
        elif 0+49 <= mouse_pos[1] <= 22+49 and 0 <= mouse_pos[0] <= 80:

            self.menu_info["actiontext"] = 'STARMAP'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "STARMAP"

        # Messages
        elif 23+49 <= mouse_pos[1] <= 98+49 and 0 <= mouse_pos[0] <= 40:

            self.menu_info["actiontext"] = 'MESSAGE'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "MESSAGES"
                self.waitingforanim = "messagescomputer"
                self.animstates["messagescomputer"].activate(1)

        # Research
        elif 23+49 <= mouse_pos[1] <= 98+49 and 41 <= mouse_pos[0] <= 80:

            self.menu_info["actiontext"] = 'RESEARCH-DESIGN'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "RESEARCH"
                self.waitingforanim = "researchcomputer"
                self.animstates["researchcomputer"].activate(1)

        # Local
        elif 0+49 <= mouse_pos[1] <= 46+49 and 83 <= mouse_pos[0] <= 128:

            self.menu_info["actiontext"] = 'SPACE LOCAL'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "LOCAL"

        # Commanders door
        elif 0+49 <= mouse_pos[1] <= 55+49 and 164 <= mouse_pos[0] <= 195:

            self.menu_info["actiontext"] = 'COMMANDERS'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "DOOR1"
                self.waitingforanim = "commanderdoor"
                self.animstates["commanderdoor"].activate(1)

        # Ship info door
        elif 0+49 <= mouse_pos[1] <= 82+49 and 196 <= mouse_pos[0] <= 247:

            self.menu_info["actiontext"] = 'SHIP INFO'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "DOOR3"
                if self.animstates["liftlights"].backwards:
                    liftlights_direction = "liftlights_dn"
                else:
                    liftlights_direction = "liftlights_up"
                self.waitingforanim = liftlights_direction
                self.animstates[liftlights_direction].activate(1)

        # Info-buy door
        elif 0+49 <= mouse_pos[1] <= 88+49 and 256 <= mouse_pos[0] <= 319:

            self.menu_info["actiontext"] = 'INFO-BUY'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "DOOR2"
                self.waitingforanim = "rightdoor"
                self.animstates["rightdoor"].activate(1)

        # Planet main
        elif 108+49 <= mouse_pos[1] <= 151+49 and 76 <= mouse_pos[0] <= 260:

            self.menu_info["actiontext"] = 'PLANET MAIN'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "SURFACE"
                self.action = "PLANET MAIN"
                self.action_params = [ (1, 5, 0), None ]  # New-Earth

