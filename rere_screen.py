# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


class screen:

    def __init__(self, gamedata_dynamic, menu_data):

        self.gamedata_dynamic = gamedata_dynamic

        self.anim_exists = False
        self.anim_states = {}

        self.action = None
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
            self.action = None
            return action
        else:
            return None


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

        for curr_state_id in self.anim_states.keys():
            self.anim_states[curr_state_id]["currtick"] += 1
            if self.anim_states[curr_state_id]["currtick"] == self.anim_states[curr_state_id]["ticks"]:
                self.anim_states[curr_state_id]["currtick"] = 0
                self.anim_states[curr_state_id]["currframe"] += 1
                if self.anim_states[curr_state_id]["currframe"] == self.anim_states[curr_state_id]["frames"]:
                    self.anim_states[curr_state_id]["currframe"] = 0


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

