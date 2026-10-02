# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_transfer(screen):

    def __init__(self, gamedata_const, gamedata_static, gamedata_dynamic, solarsystems, shipgroups_spaceforces):

        self.screentype = "transfer"

        self.menu_icons = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "GROUP" ]
        self.menu_text  = [ "BACK TO M.SCREEN", "SHIP INFO", "CONTROL PANEL", "GROUP" ]
        self.menu_sfx   = [ "BACK", "SHIP", "CONTROLL", "GROUP" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_const = gamedata_const
        self.gamedata_static = gamedata_static
        self.solarsystems = solarsystems

        self.selected_group_no_current = gamedata_dynamic["groups_selectedgroupno"][0]
        self.current_shipgroup = shipgroups_spaceforces[self.selected_group_no_current]

#        if self.current_shipgroup.type == 2:
#            self.menu_icons.insert(3, "TRANSFER")
#            self.menu_text.insert(3, "TRANSFER")
#            self.menu_sfx.insert(3, "TRANSFER")
#            self.update_menu(gamedata_dynamic, (0,0), (False, False, False), [0,0,0])

        self.planet = self.solarsystems[self.current_shipgroup.location[0]].planets[self.current_shipgroup.location]

        self.anim_exists = False

        self.gen_cargolist()

        self.selected_button_no = None
        self.selected_text_red_count = 0
        self.selected_text_redflash_timer = 0

        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def gen_cargolist(self):

        self.cargoids = self.gamedata_const["mineral_names_general"].copy()
        self.cargonames = self.gamedata_static["mineral_names"].copy()
        self.cargoquantity_planet = []
        self.cargoquantity_ship = []
        mineral_idx = 0
        for mineral_idx in range(len(self.cargoids)):
            self.cargoquantity_planet.append(self.planet.storage[self.cargoids[mineral_idx]])
            self.cargoquantity_ship.append(self.current_shipgroup.transfer[self.cargoids[mineral_idx]])

        for cargo_id in ( "ArmyShip1",
                          "ArmyVehicle1",
                          "ArmyVehicle2",
                          "ArmyVehicle3",
                          "ArmyVehicle4",
                          "ArmyEquip1",
                          "ArmyEquip2",
                          "ArmyEquip3",
                          "ArmyEquip4",
                          "MinerDroid",
                        ):

            invention_no = self.gamedata_const["storage_to_invention_mapping"][cargo_id]
            if self.gamedata_dynamic["inventions"][invention_no]['research_state'] == 5:
                self.cargoids.append(cargo_id)
                self.cargonames.append(self.gamedata_dynamic["inventions"][invention_no]['name'].decode('utf-8'))
                self.cargoquantity_planet.append(self.planet.storage[cargo_id])
                self.cargoquantity_ship.append(self.current_shipgroup.transfer[cargo_id])


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.gen_cargolist()

        if self.selected_text_red_count > 0 and \
           self.selected_text_redflash_timer > 0:

                self.selected_text_redflash_timer -= 1
                if self.selected_text_redflash_timer == 0:
                    self.selected_text_red_count -= 1
                    if self.selected_text_red_count == 0:
                        self.timed_screen_event_active = False
                    elif self.selected_text_red_count == 1:
                        self.selected_text_redflash_timer = 3

        self.cargotext_color = int(0 < self.selected_text_redflash_timer < 3) + 1  # 1 yellow, 2 red

        self.planet_cargo_part_available = self.current_shipgroup.orbit_status == 1 and \
                                           self.planet.colony == 1 and \
                                           self.planet.race == 1

        if self.planet_cargo_part_available and \
           (61 <= mouse_pos[1] <= 187):

            transfer_button_to_planet = False
            transfer_button_to_ship = False
            if (69 <= mouse_pos[0] <= 82):
                transfer_button_to_planet = True
            elif (236 <= mouse_pos[0] <= 249):
                transfer_button_to_ship = True

            if transfer_button_to_planet or transfer_button_to_ship:
                transfer_button_no = None
                if (mouse_pos[1] - 61) % 8 != 7:
                    transfer_button_no = (mouse_pos[1] - 61) // 8
                    if transfer_button_no >= len(self.cargoids):
                        transfer_button_no = None

                if transfer_button_no != None:
                    if transfer_button_to_planet:
                        self.menu_info["actiontext"] = self.gamedata_static['texts']['txt_transfer_to_planet']
                    elif transfer_button_to_ship:
                        self.menu_info["actiontext"] = self.gamedata_static['texts']['txt_transfer_to_ship']

                if transfer_button_no != None and \
                   (mouse_buttonstate[0] or mouse_buttonstate[2]):

                    if not self.planet.has_spaceport and\
                       transfer_button_no >= 6:

                        print("MSG:", self.gamedata_static['texts']['msg_transfer_need_spaceport'])

                    else:

                        cargoid = self.cargoids[transfer_button_no]
                        is_mineral_transfer = (cargoid[:7] == "Mineral")
                        ship_cargo_capacity_free = (self.current_shipgroup.cargo_capacity_total - self.current_shipgroup.cargo_capacity_used)
                        if is_mineral_transfer:
                            planet_cargo_capacity_free = (self.planet.mineral_storage_capacity - self.planet.storage[cargoid])

                        if mouse_buttonstate[0]:

                            self.selected_text_red_count = 1
                            transfer_unit = [ 1, 100 ][is_mineral_transfer]

                            if transfer_button_to_ship:

                                if self.planet.storage[cargoid] >= transfer_unit:
                                    transfer_amount = transfer_unit
                                else:
                                    transfer_amount = self.planet.storage[cargoid]

                                if is_mineral_transfer:
                                    transfer_capacity_needed = transfer_amount
                                    if ship_cargo_capacity_free < transfer_capacity_needed:
                                        transfer_amount = ship_cargo_capacity_free
                                else:
                                    transfer_capacity_needed = self.gamedata_static['tradeship_capacities_needed'][cargoid]
                                    if ship_cargo_capacity_free < transfer_capacity_needed:
                                        transfer_amount = 0

                                self.current_shipgroup.transfer[cargoid] += transfer_amount
                                self.planet.storage[cargoid] -= transfer_amount

                            elif transfer_button_to_planet:

                                if self.current_shipgroup.transfer[cargoid] >= transfer_unit:
                                    transfer_amount = transfer_unit
                                else:
                                    transfer_amount = self.current_shipgroup.transfer[cargoid]

                                if is_mineral_transfer:
                                    transfer_capacity_needed = transfer_amount
                                    if planet_cargo_capacity_free < transfer_capacity_needed:
                                        transfer_amount = planet_cargo_capacity_free
                                # planet storage only limits minerals

                                self.current_shipgroup.transfer[cargoid] -= transfer_amount
                                self.planet.storage[cargoid] += transfer_amount

                        elif mouse_buttonstate[2]:

                            self.selected_text_red_count = 2

                            if transfer_button_to_ship:

                                if is_mineral_transfer:
                                    transfer_capacity_wanted = self.planet.storage[cargoid]
                                else:
                                    transfer_capacity_wanted = self.planet.storage[cargoid] * self.gamedata_static['tradeship_capacities_needed'][cargoid]

                                if ship_cargo_capacity_free >= transfer_capacity_wanted:
                                    transfer_amount = self.planet.storage[cargoid]
                                else:
                                    if is_mineral_transfer:
                                        transfer_amount = ship_cargo_capacity_free
                                    else:
                                        transfer_amount = ship_cargo_capacity_free // self.gamedata_static['tradeship_capacities_needed'][cargoid]

                                self.current_shipgroup.transfer[cargoid] += transfer_amount
                                self.planet.storage[cargoid] -= transfer_amount

                            elif transfer_button_to_planet:

                                if is_mineral_transfer:
                                    transfer_capacity_wanted = self.current_shipgroup.transfer[cargoid]
                                    if planet_cargo_capacity_free >= transfer_capacity_wanted:
                                        transfer_amount = self.current_shipgroup.transfer[cargoid]
                                    else:
                                        transfer_amount = planet_cargo_capacity_free

                                else:  # planet storage only limits minerals
                                    transfer_amount = self.current_shipgroup.transfer[cargoid]

                                self.current_shipgroup.transfer[cargoid] -= transfer_amount
                                self.planet.storage[cargoid] += transfer_amount

                        self.current_shipgroup.update_cargo_capacity()

                        if self.selected_text_redflash_timer == 0:
                            self.selected_text_redflash_timer = 4
                        self.selected_button_no = transfer_button_no
                        self.timed_screen_event_active = True
