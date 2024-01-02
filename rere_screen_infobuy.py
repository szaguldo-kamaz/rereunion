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


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.invention_item_list = []
        for inv_no in gamedata_dynamic["inventions"].keys():
            currinv = gamedata_dynamic["inventions"][inv_no]
            if currinv['research_state'] == 5:
                self.invention_item_list.append( (inv_no, currinv['name']) )

        self.selected_item_invno = self.invention_item_list[self.selected_item_listno][0]

        self.invention_item_list_len = len(self.invention_item_list)

        self.invention_description = self.gamedata_static["inventions_desc"][self.selected_item_invno - 1]

        selectedinv = gamedata_dynamic["inventions"][self.selected_item_invno]
        self.minerals = selectedinv['minerals']

        if selectedinv['can_be_produced_asis'] == 1:
            self.can_be_produced = True
            self.stores = selectedinv['quantity_in_storage']
            self.bought_items = selectedinv['quantity_in_production']
            self.total_price = selectedinv['quantity_in_production'] * selectedinv['price']
            self.time_to_go = (selectedinv['quantity_in_production'] * selectedinv['time_to_produce_one']) / 10 + \
                               selectedinv['time_to_produce_next']
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
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
            elif menuaction == 'SELECT':
                self.menu_icons = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "INFO-BUY", "PROJECT UP", "PROJECT DOWN" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "RESEARCH-DESIGN", "BUY ITEM", "SELECT OFF", "PROJECT UP", "PROJECT DOWN" ]
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
            else:
                self.action = menuaction

        # Select from list
        if (54 <= mouse_pos[1] <= 172) and (16 <= mouse_pos[0] <= 110):
            if mouse_buttonevent[0]:
                self.selected_item_listno = self.scroll_start + int((mouse_pos[1] - 54)/9)

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
        if (49 <= mouse_pos[1] <= 174) and (128 <= mouse_pos[0] <= 319):

            if self.picturemode:
                self.menu_info["actiontext"] = "See info"
            else:
                self.menu_info["actiontext"] = "See picture"

            if mouse_buttonevent[0]:
                self.picturemode = not self.picturemode
                # TODO menu change -> SELECT / INFO-BUY - SELECT / SELECT OFF
                self.sfx_to_play = "X"
