# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import random


class screen:

    class screen_anim:

        # loop == 0: no looping
        # loop == 1: loop forever
        # loop == 2: loop forever, but pause between repeats (delay)
        # loop == 3: loop forever and change direction (forward/backward) after each loop
        # loop == 4: loop forever, but pause between repeats (delay) and change direction (forward/backward) after each loop

        def __init__(self, frames, ticks, loop, backwards = False, active = -1, delay = 0, delaymin = 0, delaymax = 0, tickspersec = 10):

            self.frames = frames
            self.ticks = ticks
            self.loop = loop
            self.backwards = backwards

            if active == -1:
                if self.loop == 1:
                    self.activate(1)
                else:
                    self.activate(0)
            else:
                self.activate(active)

            self.delaymin = delaymin * tickspersec
            self.delaymax = delaymax * tickspersec
            if delay == -1:
                self.delay = self.__gen_delay()
            else:
                self.delay = delay


        def __gen_delay(self):
            return int(self.delaymin + random.random() * (self.delaymax - self.delaymin))


        def activate(self, activestate):

            self.active = activestate

            if self.backwards:
                self.setframe(self.frames - 1)
            else:
                self.setframe(0)

            self.resettick()


        def resettick(self):
            self.currtick = 0


        def setframe(self, newframeno):
            self.currframe = newframeno


        def update(self):

            anim_ended = False

            if self.loop in [1, 3] or (self.loop in [0, 2, 4] and self.active == 1):

                self.currtick += 1

                if self.currtick == self.ticks:

                    self.currtick = 0
                    loopend = False

                    if self.backwards:
                        self.currframe -= 1
                        if self.currframe == -1:
                            loopend = True
                            if self.loop in [0, 3, 4]:
                                self.currframe = 0
                                if self.loop in [3, 4]:   # change direction to forward
                                    self.backwards = False
                            else:
                                self.currframe = self.frames - 1

                    else:  # forward
                        self.currframe += 1
                        if self.currframe == self.frames:
                            loopend = True
                            if self.loop in [0, 3, 4]:
                                self.currframe = self.frames - 1
                                if self.loop in [3, 4]:   # change direction to backwards
                                    self.backwards = True
                            else:
                                self.currframe = 0

                    if loopend and self.loop in [0, 2, 4]:
                        if self.loop in [2, 4]:
                            self.active = 0  # inactive
                            self.delay = self.__gen_delay()
                        elif self.loop == 0:
                            self.active = 2  # inactive, finished
                            # anim ended, maybe it triggers and action
                            anim_ended = True

            if self.loop in [2, 4] and self.active == 0:
                self.delay -= 1
                if self.delay == 0:
                    self.active = 1

            return anim_ended


    def add_anim(self, name, frames, ticks, loop, backwards = False, active = -1, delay = 0, delaymin = 0, delaymax = 0, tickspersec = 10):

        self.animstates[name] = self.screen_anim(frames, ticks, loop, backwards, active, delay, delaymin, delaymax, tickspersec)


    def __init__(self, gamedata_dynamic, menu_data, tickspersec = 10):

        self.gamedata_dynamic = gamedata_dynamic

        self.tickspersec = tickspersec

        self.anim_exists = False
        self.animstates = {}
        self.waitingforanim = None

        self.action = None
        self.action_params = None
        self.sfx_to_play = None

        self.last_mouse_pos = None

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


    def update_anims(self):

        if not self.anim_exists:
            return

        for curr_anim_state_id in self.animstates.keys():
            anim_ended = self.animstates[curr_anim_state_id].update()
            if anim_ended:  # maybe there is an action to be set
                self.update(self.gamedata_dynamic, None, [0,0,0], [0,0,0])


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

