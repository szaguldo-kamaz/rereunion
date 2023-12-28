# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_ship(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, shipgroups_spaceforces, shipgroups_planetforces):

        self.screentype = "ship"

        self.menu_icons = [ "BACK TO M.SCREEN" ]
        self.menu_text  = [ "BACK TO M.SCREEN" ]
        self.menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_static = gamedata_static

        self.anim_exists = False

        self.selected_group_no_current = gamedata_dynamic["groups_selectedgroupno"][0]
        self.selected_group_no = [ gamedata_dynamic["groups_selectedgroupno"][1], gamedata_dynamic["groups_selectedgroupno"][2] ]
        self.currentview = gamedata_dynamic["groups_currentview"]  # 0 - normal, 1 - planet forces
        self.shipgroups_spaceforces = shipgroups_spaceforces
        self.shipgroups_planetforces = shipgroups_planetforces
        self.current_shipgroup = self.shipgroups_spaceforces
        self.__set_location_string()

        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def __set_location_string(self, use_long_name = False):

        loctmp = self.current_shipgroup[self.selected_group_no_current].location
        if use_long_name:
            sysname = self.gamedata_static["system_names"][loctmp[0]-1]
        else:
            sysname = self.gamedata_static["system_shortnames"][loctmp[0]-1]

        self.selected_group_location = [ sysname, str(loctmp[1]), str(loctmp[2]) ]


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        if self.currentview == 0:

            self.current_shipgroup = self.shipgroups_spaceforces
            if self.current_shipgroup[self.selected_group_no_current].type == 2:  # trade
                self.menu_icons = [ "BACK TO M.SCREEN", "CONTROL PANEL", "GROUP", "NEW GROUP", "TRANSFER", "PLANET MAIN" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "CONTROL PANEL", "GROUP", "NEW UNIT",  "TRANSFER", "PLANET MAIN" ]
                self.menu_sfx   = [ "BACK", "CONTROLL", "GROUP", "GROUPNEW", "TRANSFER", "PLANET" ]
            else:
                self.menu_icons = [ "BACK TO M.SCREEN", "CONTROL PANEL", "GROUP", "NEW GROUP", "PLANET MAIN" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "CONTROL PANEL", "GROUP", "NEW UNIT",  "PLANET MAIN" ]
                self.menu_sfx   = [ "BACK", "CONTROLL", "GROUP", "GROUPNEW", "PLANET" ]

        else:
            self.current_shipgroup = self.shipgroups_planetforces
            self.menu_icons = [ "BACK TO M.SCREEN", "GROUP", "PLANET MAIN" ]
            self.menu_text  = [ "BACK TO M.SCREEN", "GROUP", "PLANET MAIN" ]
            self.menu_sfx   = [ "BACK", "GROUP", "PLANET" ]

        self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)


        if (60 <= mouse_pos[1] <= 187) and (0 <= mouse_pos[0] <= 191):

            rowpos = int(((mouse_pos[1] - 60) / 16) + 1)
            colpos = int(mouse_pos[0] / 48)
            mouse_over_groupno = colpos * 8 + rowpos

            if (       mouse_pos[0] <=  15) or \
               ( 48 <= mouse_pos[0] <=  63) or \
               ( 96 <= mouse_pos[0] <= 111) or \
               (144 <= mouse_pos[0] <= 159):

                    is_icon = False
            else:
                    is_icon = True

            if mouse_over_groupno < len(self.current_shipgroup):

                self.menu_info["actiontext"] = self.current_shipgroup[mouse_over_groupno].name

                if mouse_buttonevent[0]:
                    self.selected_group_no[self.currentview] = mouse_over_groupno
                    self.selected_group_no_current = self.selected_group_no[self.currentview]
                    self.__set_location_string(bool(self.currentview))
                    if is_icon:
                        self.sfx_to_play = "GROUP"

        # CHANGE at the bottom
        if (188 <= mouse_pos[1] <= 200) and (0 <= mouse_pos[0] <= 191):
            self.menu_info["actiontext"] = "Change mode"
            if mouse_buttonevent[0]:
                self.currentview = int(not self.currentview)
                self.selected_group_no_current = self.selected_group_no[self.currentview]
                self.update(gamedata_dynamic, mouse_pos, [0,0,0], [0,0,0])
                self.__set_location_string(bool(self.currentview))
