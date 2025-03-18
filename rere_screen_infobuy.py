# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_infobuy(screen):

    def __init__(self, gamedata_static, gamedata_dynamic):

        self.screentype = "infobuy"

        self.menu_icons = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "INFO-BUY", "PROJECT UP", "PROJECT DOWN" ]
        self.menu_text  = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "SELECT OFF", "PROJECT UP", "PROJECT DOWN" ]
        self.menu_sfx   = [ "BACK", "RESEARCH", "BUY", "SELECT", "X", "X" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_static = gamedata_static

        self.anim_exists = False
        # TODO vector anim

        self.selected_item_listno = 0  # Nuclear gen
        self.selected_item_invno = 1  # Nuclear gen
        self.scroll_start = 0
        self.picturemode = True
        self.selectmode = True
        self.buysellmode = False
        self.needed_minerals = {}
        self.mineral_names_list = list(gamedata_dynamic["minerals_main"].keys())


    def __update_needed_minerals(self):
        mineral_index = 0
        for mineral_name in self.mineral_names_list:
            self.needed_minerals[mineral_name] = self.minerals[mineral_index] * self.selected_invention['quantity_in_production']
            mineral_index += 1


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        if self.timed_screen_event_active:
            self.mineral_flash_timer -= 1
            if self.mineral_flash_timer == 0:
                self.timed_screen_event_active = False

        self.invention_item_list = []
        for inv_no in gamedata_dynamic["inventions"].keys():
            currinv = gamedata_dynamic["inventions"][inv_no]
            if currinv['research_state'] == 5:
                self.invention_item_list.append( (inv_no, currinv['name']) )

        self.selected_item_invno = self.invention_item_list[self.selected_item_listno][0]

        self.invention_item_list_len = len(self.invention_item_list)

        self.invention_description = self.gamedata_static["inventions_desc"][self.selected_item_invno - 1]

        self.selected_invention = gamedata_dynamic["inventions"][self.selected_item_invno]
        self.minerals = self.selected_invention['minerals']

        if self.selected_invention['can_be_produced_asis'] == 1:
            self.can_be_produced = True
            self.stores = self.selected_invention['quantity_in_storage']
            self.items_in_production = self.selected_invention['quantity_in_production']
            self.total_price = self.selected_invention['quantity_in_production'] * self.selected_invention['price']
            if self.selected_invention['time_to_produce_next'] == 0 and self.selected_invention['quantity_in_production'] > 0:
                self.time_to_go = ((self.selected_invention['quantity_in_production']) * self.selected_invention['time_to_produce_one']) / 10
            else:
                self.time_to_go = ((self.selected_invention['quantity_in_production'] - 1) * self.selected_invention['time_to_produce_one']) / 10 + \
                                   self.selected_invention['time_to_produce_next'] / 10
        else:
            self.can_be_produced = False
            self.cannot_be_produced_reason = "This will be fitted on your nose."

        [ menuaction, _ ] = self.get_action()
        if menuaction != None:
            if   menuaction == 'PROJECT UP':
                if self.selected_item_listno > 0:
                    self.selected_item_listno -= 1
            elif menuaction == 'PROJECT DOWN':
                if self.selected_item_listno < (self.invention_item_list_len - 1):
                    self.selected_item_listno += 1
            elif menuaction == 'SELECT OFF':
                self.menu_icons = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "SELECT", "PROJECT UP", "PROJECT DOWN" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "SELECT", "PROJECT UP", "PROJECT DOWN" ]
                self.menu_sfx   = [ "BACK", "RESEARCH", "BUY", "SELECT", "X", "X" ]
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
            elif menuaction == 'SELECT':
                self.menu_icons = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "INFO-BUY", "PROJECT UP", "PROJECT DOWN" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "SELECT OFF", "PROJECT UP", "PROJECT DOWN" ]
                self.menu_sfx   = [ "BACK", "RESEARCH", "BUY", "SELECT", "X", "X" ]
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])

            elif menuaction == 'BUY ITEM' and self.can_be_produced:
                self.previous_menu_icons = self.menu_icons
                self.previous_menu_text = self.menu_text
                self.previous_menu_sfx = self.menu_sfx
                self.menu_icons = [ "ADD TEN", "ADD ONE", "MINUS ONE", "MINUS TEN", "OK,BUY", "CANCEL BUY" ]
                self.menu_text  = [ "ADD TEN", "ADD ONE", "MINUS ONE", "MINUS TEN", "OK.BUY", "CANCEL BUY" ]
                self.menu_sfx   = [ "X", "X", "X", "X", "OKAY", "NOTHANKS" ]
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
                self.buysellmode = True
                self.original_quantity_in_production = self.selected_invention['quantity_in_production']
                self.__update_needed_minerals()
                self.gamedata_dynamic["time_stopped"] = True
                self.gamedata_dynamic["money"] += self.total_price
                for mineralname in self.mineral_names_list:
                    self.gamedata_dynamic["minerals_main"][mineralname] += self.needed_minerals[mineralname]

            elif menuaction in [ 'CANCEL BUY', 'OK.BUY' ]:
                self.menu_icons = self.previous_menu_icons
                self.menu_text  = self.previous_menu_text
                self.menu_sfx   = self.previous_menu_sfx
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
                self.buysellmode = False
                self.gamedata_dynamic["time_stopped"] = False
                if menuaction == 'CANCEL BUY':
                    self.selected_invention['quantity_in_production'] = self.original_quantity_in_production
                self.total_price = self.selected_invention['quantity_in_production'] * self.selected_invention['price']
                self.gamedata_dynamic["money"] -= self.total_price
                self.__update_needed_minerals()
                for mineralname in self.mineral_names_list:
                    self.gamedata_dynamic["minerals_main"][mineralname] -= self.needed_minerals[mineralname]

            elif menuaction in [ 'ADD ONE', 'ADD TEN' ]:
                if menuaction == 'ADD ONE':
                    want_to_buy = 1
                else:
                    want_to_buy = 10

                need_money_redflash = False
                need_mineral_flash = dict(zip(self.mineral_names_list, [False]*6))
                self.selected_invention['quantity_in_production'] += want_to_buy

                while True:
                    not_enough_resource = False
                    self.__update_needed_minerals()
                    self.total_price = self.selected_invention['quantity_in_production'] * self.selected_invention['price']
                    for mineralname in self.mineral_names_list:
                        if self.needed_minerals[mineralname] > self.gamedata_dynamic["minerals_main"][mineralname]:
                            need_mineral_flash[mineralname] = True
                            not_enough_resource = True

                    if self.total_price > self.gamedata_dynamic["money"]:
                        need_money_redflash = True
                        not_enough_resource = True

                    if not_enough_resource:
                        self.selected_invention['quantity_in_production'] -= 1
                    else:
                        break

                if need_money_redflash:
                    self.trigger_infobar_money_redflash()

                if any([ mflsh[1] for mflsh in need_mineral_flash.items() ]):
                    self.timed_screen_event_active = True
                    self.mineral_flash_timer = 5
                    self.mineral_flash_minerals = need_mineral_flash

            elif menuaction in [ 'MINUS ONE', 'MINUS TEN' ]:
                if menuaction == 'MINUS ONE':
                    want_to_sell = 1
                else:
                    want_to_sell = 10
                self.selected_invention['quantity_in_production'] -= want_to_sell
                if self.selected_invention['quantity_in_production'] <= 0:
                    if self.selected_invention['time_to_produce_next'] == 0:
                        self.selected_invention['quantity_in_production'] = 0
                    else:
                        self.selected_invention['quantity_in_production'] = 1
                self.__update_needed_minerals()
                self.total_price = self.selected_invention['quantity_in_production'] * self.selected_invention['price']
            else:
                self.action = menuaction

        # Select from list
        if (54 <= mouse_pos[1] <= 170) and (16 <= mouse_pos[0] <= 110) and \
           not self.buysellmode:
            if mouse_buttonevent[0]:
                self.selected_item_listno = self.scroll_start + int((mouse_pos[1] - 54)/9)
                if self.selected_item_listno >= self.invention_item_list_len:
                    self.selected_item_listno = self.invention_item_list_len - 1

        # Scroll up
        if (49 <= mouse_pos[1] <= 66) and ( (0 <= mouse_pos[0] <= 11) or (115 <= mouse_pos[0] <= 126) ):
            self.menu_info["actiontext"] = "Scroll up"
            if any(mouse_buttonstate):
                if self.scroll_start > 0:
                    self.scroll_start -= 1

        # Scroll Down
        if (158 <= mouse_pos[1] <= 174) and ( (0 <= mouse_pos[0] <= 11) or (115 <= mouse_pos[0] <= 126) ):
            self.menu_info["actiontext"] = "Scroll down"
            if any(mouse_buttonstate):
                if self.scroll_start < (self.invention_item_list_len - 13):
                    self.scroll_start += 1

        # Info/pic screen
        if (49 <= mouse_pos[1] <= 174) and (128 <= mouse_pos[0] <= 319) and \
           not self.buysellmode:

            if self.picturemode:
                self.menu_info["actiontext"] = "See info"
            else:
                self.menu_info["actiontext"] = "See picture"

            if mouse_buttonevent[0]:
                self.picturemode = not self.picturemode
                # TODO menu change -> SELECT / INFO-BUY - SELECT / SELECT OFF
                self.sfx_to_play = "X"
