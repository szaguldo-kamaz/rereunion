# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_group(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, solarsystems, shipgroups_spaceforces, shipgroups_planetforces):

        self.screentype = "group"

        self.menu_icons = [ "BACK TO M.SCREEN" ]
        self.menu_text  = [ "BACK TO M.SCREEN" ]
        self.menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.anim_exists = False

        self.gamedata_static = gamedata_static
        self.solarsystems = solarsystems
        self.shipgroups_spaceforces = shipgroups_spaceforces
        self.shipgroups_planetforces = shipgroups_planetforces
        self.inventory_to_show_currentpage = 1

        self.__update_from_dynamic()
        self.__set_location_names()
        self.__gen_inventory_to_show()

        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def __update_from_dynamic(self):

        self.selected_group_no_current = self.gamedata_dynamic["groups_selectedgroupno"][0]
        self.selected_group_no = self.gamedata_dynamic["groups_selectedgroupno"][1:3]
        self.numofgroups_spaceforces = self.gamedata_dynamic["groups_numofgroups"][1]
        self.numofgroups_planetforces = self.gamedata_dynamic["groups_numofgroups"][2]
        self.currentview = self.gamedata_dynamic["groups_currentview"]  # 0 - normal, 1 - planet forces
        if self.currentview == 0:
            self.current_shipgroup = self.shipgroups_spaceforces
        else:
            self.current_shipgroup = self.shipgroups_planetforces
        self.current_planet_surface = self.current_shipgroup[self.selected_group_no_current].location


    def __set_location_names(self):

        [ sysno, planetno, moonno ] = self.current_shipgroup[self.selected_group_no_current].location

        planetname = self.solarsystems[sysno].planets[(sysno, planetno, 0)].planetname
        if moonno == 0:
            moonname = None
        else:
            moonname = self.solarsystems[sysno].planets[(sysno, planetno, moonno)].planetname

        sysname = self.gamedata_static["system_names"][sysno-1]

        self.selected_group_location_names = [ sysname, planetname, moonname ]


    def __gen_inventory_to_show(self):

        curgrp = self.current_shipgroup[self.selected_group_no_current]

        if curgrp.type in [1, 5]:

            if self.inventory_to_show_currentpage == 1:
                self.inventory_to_show_up_arrow = False
                self.inventory_to_show_down_arrow = True
                self.inventory_to_show_craft_names = self.gamedata_static["group_craftlist"][0]
                self.inventory_to_show_equip_names = self.gamedata_static["group_equiplist"][0]
                self.inventory_to_show_crafts = self.gamedata_dynamic["invented_army_ship_list"]
                self.inventory_to_show_equips = self.gamedata_dynamic["invented_army_ship_equip_list"]
            else:
                self.inventory_to_show_up_arrow = True
                self.inventory_to_show_down_arrow = False
                self.inventory_to_show_craft_names = self.gamedata_static["group_craftlist"][1]
                self.inventory_to_show_equip_names = self.gamedata_static["group_equiplist"][1]
                self.inventory_to_show_crafts = self.gamedata_dynamic["invented_army_vehicle_list"]
                self.inventory_to_show_equips = self.gamedata_dynamic["invented_army_vehicle_equip_list"]

        elif curgrp.type == 2:  # trade
            self.inventory_to_show_up_arrow = False
            self.inventory_to_show_down_arrow = False
            self.inventory_to_show_craft_names = self.gamedata_static["group_craftlist"][2]
            self.inventory_to_show_equip_names = self.gamedata_static["group_equiplist"][2]
            self.inventory_to_show_crafts = self.gamedata_dynamic["invented_trade_ship_list"]
            self.inventory_to_show_equips = self.gamedata_dynamic["invented_trade_equip_list"]

        else:  # carrier
            self.inventory_to_show_up_arrow = False
            self.inventory_to_show_down_arrow = False
            self.inventory_to_show_craft_names = self.gamedata_static["group_craftlist"][3]
            self.inventory_to_show_equip_names = self.gamedata_static["group_equiplist"][3]
            self.inventory_to_show_crafts = self.gamedata_dynamic["invented_carrier_ship_list"]
            self.inventory_to_show_equips = self.gamedata_dynamic["invented_carrier_equip_list"]


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.__update_from_dynamic()
        self.__set_location_names()
        self.__gen_inventory_to_show()

        if self.current_shipgroup[self.selected_group_no_current].type == 2:  # trade
            self.menu_icons = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "TRANSFER", "GALACTIC MAP", "PLANET MAIN" ]
            self.menu_text  = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "TRANSFER", "GALACTIC MAP", "PLANET MAIN" ]
            self.menu_sfx   = [ "BACK", "SHIP", "CONTROLL", "STARMAP", "TRANSFER", "PLANET" ]
        else:
            self.menu_icons = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "GALACTIC MAP", "PLANET MAIN" ]
            self.menu_text  = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "GALACTIC MAP", "PLANET MAIN" ]
            self.menu_sfx   = [ "BACK", "SHIP", "CONTROLL", "STARMAP", "PLANET" ]

        self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.currentview = self.gamedata_dynamic["groups_currentview"]  # 0 - normal, 1 - planet forces

        if self.currentview == 0 and \
           self.selected_group_no_current == 1:
            self.inventory_to_show_left_arrow = False
        else:
            self.inventory_to_show_left_arrow = True

        if self.currentview == 1 and \
           self.selected_group_no_current == self.numofgroups_planetforces:
            self.inventory_to_show_right_arrow = False
        else:
            self.inventory_to_show_right_arrow = True


        if (53 <= mouse_pos[1] <= 65) and (9 <= mouse_pos[0] <= 19) and \
           self.inventory_to_show_left_arrow:

            self.menu_info["actiontext"] = "Previous group"

            if mouse_buttonevent[0]:
                self.inventory_to_show_currentpage = 1

                if self.currentview == 1 and \
                   self.selected_group_no_current == 1:
                    self.gamedata_dynamic["groups_currentview"] = 0
                    self.gamedata_dynamic["groups_selectedgroupno"] = [ self.numofgroups_spaceforces, self.numofgroups_spaceforces, 1 ]
                else:
                    self.gamedata_dynamic["groups_selectedgroupno"][0] -= 1
                    self.gamedata_dynamic["groups_selectedgroupno"][1] -= 1

                self.__update_from_dynamic()
                self.__set_location_names()
                self.__gen_inventory_to_show()
                self.sfx_to_play = "X"

        elif (53 <= mouse_pos[1] <= 65) and (131 <= mouse_pos[0] <= 141) and \
           self.inventory_to_show_right_arrow:

            self.menu_info["actiontext"] = "Next group"
            if mouse_buttonevent[0]:
                self.inventory_to_show_currentpage = 1
                if self.currentview == 0 and \
                   self.selected_group_no_current == self.numofgroups_spaceforces:
                    self.gamedata_dynamic["groups_currentview"] = 1
                    self.gamedata_dynamic["groups_selectedgroupno"] = [ 1, self.numofgroups_spaceforces, 1 ]
                else:
                    self.gamedata_dynamic["groups_selectedgroupno"][0] += 1
                    self.gamedata_dynamic["groups_selectedgroupno"][1] += 1

                self.__update_from_dynamic()
                self.__set_location_names()
                self.__gen_inventory_to_show()
                self.sfx_to_play = "X"

        elif (87 <= mouse_pos[1] <= 115) and (294 <= mouse_pos[0] <= 311) and \
           self.inventory_to_show_up_arrow:

            self.menu_info["actiontext"] = "Page up"
            if mouse_buttonevent[0]:
                self.inventory_to_show_currentpage = 1
                self.__gen_inventory_to_show()
                self.sfx_to_play = "X"

        elif (125 <= mouse_pos[1] <= 153) and (294 <= mouse_pos[0] <= 311) and \
           self.inventory_to_show_down_arrow:

            self.menu_info["actiontext"] = "Page down"
            if mouse_buttonevent[0]:
                self.inventory_to_show_currentpage = 2
                self.__gen_inventory_to_show()
                self.sfx_to_play = "X"

        elif (53 <= mouse_pos[1] <= 64) and (22 <= mouse_pos[0] <= 127):

            self.menu_info["actiontext"] = "Change name"
            if mouse_buttonevent[0]:
                pass
