# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import random


class screen:

    def __init__(self, gamedata_dynamic, menu_data, tickspersec = 10):

        self.gamedata_dynamic = gamedata_dynamic

        self.tickspersec = tickspersec

        self.anim_exists = False
        self.anim_states = {}

        self.action = None
        self.action_params = None
        self.sfx_to_play = None

        if menu_data == None:
            self.has_menu = False
        else:
            self.has_menu = True
            self.define_menu(menu_data)


    def define_menu(self, menu_data):

        [ menu_icons, menu_text, menu_sfx ] = menu_data
        self.menu_info = { "icons": menu_icons, "text": menu_text, "sfx": menu_sfx,
                           "updown": 0, "actiontext": "",
                           "date": self.gamedata_dynamic["date"],
                           "money": self.gamedata_dynamic["money"] }
        self.menuicon_pointerover = None
        self.infobar_timespinning = False
        self.infobar_timespinning_type = 0


    def get_action(self):

        if self.action != None:
            action = self.action
            action_params = self.action_params
            self.action = None
            self.action_params = None
            return [ action, action_params ]
        else:
            return [ None, None ]


    def get_sfx(self):

        if self.sfx_to_play != None:
            sfx = self.sfx_to_play
            self.sfx_to_play = None
            return sfx
        else:
            return None


    def tick_anim(self):

        if not self.anim_exists:
            return

        # loop == 0: no looping
        # loop == 1: loop forever
        # loop == 2: loop forever, but pause between repeats (delay)
        # loop == 3: loop forever and change direction (forward/backward) after each loop
        # loop == 4: loop forever, but pause between repeats (delay) and change direction (forward/backward) after each loop

        for curr_state_id in self.anim_states.keys():
            animstate = self.anim_states[curr_state_id]

            if animstate["loop"] in [1, 3] or (animstate["loop"] in [2, 4] and animstate["active"] == 1):

                animstate["currtick"] += 1

                if animstate["currtick"] == animstate["ticks"]:

                    animstate["currtick"] = 0
                    loopend = False

                    if animstate["backwards"]:
                        animstate["currframe"] -= 1
                        if animstate["currframe"] == -1:
                            loopend = True
                            if animstate["loop"] in [3, 4]:  # change direction to forward
                                animstate["backwards"] = False
                                animstate["currframe"] = 0
                            else:
                                animstate["currframe"] = animstate["frames"] - 1

                    else:  # forward
                        animstate["currframe"] += 1
                        if animstate["currframe"] == animstate["frames"]:
                            loopend = True
                            if animstate["loop"] in [3, 4]:  # change direction to backwards
                                animstate["currframe"] = animstate["frames"] - 1
                                animstate["backwards"] = True
                            else:
                                animstate["currframe"] = 0

                    if loopend and animstate["loop"] in [2, 4]:
                        animstate["active"] = 0
                        animstate["delay"] = int(animstate["delaymin"] + random.random() * (animstate["delaymax"] - animstate["delaymin"]))

            if animstate["loop"] in [2, 4] and animstate["active"] == 0:
                animstate["delay"] -= 1
                if animstate["delay"] == 0:
                    animstate["active"] = 1


    def update_menu(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

            if not self.has_menu:
                return None

            self.menu_info["date"] = gamedata_dynamic["date"]
            self.menu_info["money"] = gamedata_dynamic["money"]

            pointer_inside_timespin_area = (34 <= mouse_pos[1] <= 44 and 219 <= mouse_pos[0] <= 320)

            if mouse_pos[1] < 31:

                # menu items
                if mouse_pos[0] < (6 * 48):
                    menuicon_pointerover_index = int(mouse_pos[0]/48) + 6 * self.menu_info["updown"]
                    if menuicon_pointerover_index < len(self.menu_info["icons"]):
                        menuicon_pointerover_new = self.menu_info["icons"][menuicon_pointerover_index]
                        if self.menuicon_pointerover != menuicon_pointerover_new:
                            self.menuicon_pointerover = menuicon_pointerover_new
                            self.menu_info["actiontext"] = self.menu_info["text"][menuicon_pointerover_index]
                        if mouse_buttonevent[0]:  # buttondown
                            print("activate menuitem: ", self.menu_info["text"][menuicon_pointerover_index])
                            self.action = self.menu_info["text"][menuicon_pointerover_index]
                            if self.action == "PLANET MAIN":
                                if hasattr(self, 'preserved_surface_position'):
                                    preserved_position = self.preserved_surface_position
                                else:
                                    preserved_position = None
                                self.action_params = [ self.current_planet_surface, preserved_position ]
                            self.sfx_to_play = self.menu_info["sfx"][menuicon_pointerover_index]
                    else:
                        self.menuicon_pointerover = ''
                        self.menu_info["actiontext"] = ''

                # scroll up/down
                else:
                    self.menuicon_pointerover = ''
                    self.menu_info["actiontext"] = ''
                    if len(self.menu_info["icons"]) > 6:
                        if mouse_buttonevent[0]:  # buttondown
                            if self.menu_info["updown"] == 0:
                                self.sfx_to_play = "ICON"
                                self.menu_info["updown"] = 1
                            else:
                                self.sfx_to_play = "ICON"
                                self.menu_info["updown"] = 0

            else:
                self.menuicon_pointerover = ''
                self.menu_info["actiontext"] = ''

            if pointer_inside_timespin_area:
                self.menuicon_pointerover = ''
                self.menu_info["actiontext"] = 'Time'
                if   mouse_buttonstate[0] and (not self.infobar_timespinning or self.infobar_timespinning_type != 1):
                    print("idoporgetes lassu start")
                    self.infobar_timespinning = True
                    self.infobar_timespinning_type = 1
                elif mouse_buttonstate[2] and (not self.infobar_timespinning or self.infobar_timespinning_type != 2):
                    print("idoporgetes gyors start")
                    self.infobar_timespinning = True
                    self.infobar_timespinning_type = 2
            else:
                if self.infobar_timespinning > 0:
                    self.infobar_timespinning = False
                    print("idoporgetes STOP")

            if mouse_buttonevent[1]:  # buttonup
                if self.infobar_timespinning:
                    print("idoporgetes stop")
                    self.infobar_timespinning = False
                    self.infobar_timespinning_type = 0

