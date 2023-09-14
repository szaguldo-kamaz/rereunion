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
        self.anim_states["radarscreen"] = { "currframe" : 0, "frames" : 6, "currtick" : 0, "ticks" : 5, "loop" : 1 }

        self.commander_names = gamedata_static["commander_names"]
        self.current_commanders = self.gamedata_dynamic["commanders"]


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

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

        # Research
        elif 23+49 <= mouse_pos[1] <= 98+49 and 41 <= mouse_pos[0] <= 80:

            self.menu_info["actiontext"] = 'RESEARCH-DESIGN'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "RESEARCH"
                self.action = "RESEARCH-DESIGN"

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

        # Ship info door
        elif 0+49 <= mouse_pos[1] <= 82+49 and 196 <= mouse_pos[0] <= 247:

            self.menu_info["actiontext"] = 'SHIP INFO'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "DOOR3"

        # Info-buy door
        elif 0+49 <= mouse_pos[1] <= 88+49 and 256 <= mouse_pos[0] <= 319:

            self.menu_info["actiontext"] = 'INFO-BUY'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "DOOR2"

        # Planet main
        elif 108+49 <= mouse_pos[1] <= 151+49 and 76 <= mouse_pos[0] <= 260:

            self.menu_info["actiontext"] = 'PLANET MAIN'
            if mouse_buttonevent[0]:  # mouse button pressed
                self.sfx_to_play = "SURFACE"
                self.action = "PLANET MAIN"
