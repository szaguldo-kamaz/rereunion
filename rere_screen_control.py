# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_control(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, solarsystems, shipgroups_spaceforces, shipgroups_planetforces, target_planet):

        self.screentype = "control"

        self.menu_icons = [ "BACK TO M.SCREEN", "SHIP INFO", "GROUP", "GALACTIC MAP", "PLANET MAIN" ]
        self.menu_text  = [ "BACK TO M.SCREEN", "SHIP INFO", "GROUP", "GALACTIC MAP", "PLANET MAIN" ]
        self.menu_sfx   = [ "BACK", "SHIP", "GROUP", "STARMAP", "PLANET" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_static = gamedata_static
        self.solarsystems = solarsystems

        self.selected_group_no_current = gamedata_dynamic["groups_selectedgroupno"][0]
        if gamedata_dynamic["groups_currentview"] == 0:
            self.current_shipgroup = shipgroups_spaceforces[self.selected_group_no_current]
        else:
            self.current_shipgroup = shipgroups_planetforces[self.selected_group_no_current]

        if self.current_shipgroup.type == 2:
            self.menu_icons.insert(3, "TRANSFER")
            self.menu_text.insert(3, "TRANSFER")
            self.menu_sfx.insert(3, "TRANSFER")
            self.update_menu(gamedata_dynamic, (0,0), (False, False, False), [0,0,0])

        if target_planet != None:
            if self.current_shipgroup.location[0] == target_planet[0]:
                self.current_shipgroup.orbit_status = 4  # intra-system
            else:
                self.current_shipgroup.orbit_status = 6  # inter-system
            self.current_shipgroup.location = target_planet
            # TODO: calculate flight time
            self.current_shipgroup.remaining_flight_time = 15

        self.current_planet_surface = self.current_shipgroup.location

        self.planet = self.solarsystems[self.current_shipgroup.location[0]].planets[self.current_shipgroup.location]

        if self.current_shipgroup.orbit_status in [ 4, 6 ]:  # 5?
            self.shipgroup_moving = True
        else:
            self.shipgroup_moving = False

        if self.shipgroup_moving:
            self.menu_icons.remove("GALACTIC MAP")
            self.menu_text.remove("GALACTIC MAP")
            self.menu_sfx.remove("STARMAP")

            self.menu_icons.remove("PLANET MAIN")
            self.menu_text.remove("PLANET MAIN")
            self.menu_sfx.remove("PLANET")

        self.anim_exists = True
        self.add_anim("transfer",      3, 2, 1)
        self.add_anim("stick",         4, 1, 0)
        self.add_anim("redlights",     2, 2, 1)
        self.add_anim("radiodetector", 4, 3, 1)
        self.add_anim("terminal",      5, 3, 1)
        self.add_anim("throttleup",    4, 2, 0)
        self.add_anim("throttledown",  4, 2, 0)

        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        if self.waitingforanim != None:

            if self.animstates[self.waitingforanim].active == 2:

                if self.waitingforanim == "throttledown":
                    self.animstates[self.waitingforanim].activate(0)
                    self.waitingforanim = "throttleup"
                    self.animstates[self.waitingforanim].activate(1)
                elif self.waitingforanim == "throttleup":
                    self.animstates[self.waitingforanim].activate(0)
                    self.waitingforanim = None

                elif self.waitingforanim == "stick":
                    self.action = "GALACTIC MAP"
                    self.action_params = [ "controlmove" ]
                    self.waitingforanim = None

            return


        # Arrived
        if self.shipgroup_moving and \
           self.current_shipgroup.orbit_status not in [ 4, 6 ]:  # 5?

            self.shipgroup_moving = False

            self.menu_icons.append("GALACTIC MAP")
            self.menu_text.append("GALACTIC MAP")
            self.menu_sfx.append("STARMAP")

            self.menu_icons.append("PLANET MAIN")
            self.menu_text.append("PLANET MAIN")
            self.menu_sfx.append("PLANET")


        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)


        # Planet main
        if not self.shipgroup_moving and \
           (49 <= mouse_pos[1] <= 134):
            self.menu_info["actiontext"] = "Planet main"
            if mouse_buttonevent[0]:
                self.sfx_to_play = "SURFACE"
                self.action = "PLANET MAIN"
                self.action_params = [ self.current_shipgroup.location, None ]

        # Docking / Launch
        elif (149 <= mouse_pos[1] <= 200) and (0 <= mouse_pos[0] <= 72):

            if self.current_shipgroup.orbit_status == 2:  # in orbit
                self.menu_info["actiontext"] = "Docking"
                if mouse_buttonevent[0]:
                    if self.current_shipgroup.type == 4:
                        print("The satellite carriers can only land on your main planet")
                    else:
                        if self.planet.planettype == 2:
                            print("You cannot land on this type of planet, since it is gaseous!")
                        else:
                            self.current_shipgroup.orbit_status = 1
                            self.sfx_to_play = "LANDING"
                            self.waitingforanim = "throttledown"
                            self.animstates["throttledown"].activate(1)

            elif self.current_shipgroup.orbit_status == 1:  # landed
                self.menu_info["actiontext"] = "Launch"
                if mouse_buttonevent[0]:
                    self.current_shipgroup.orbit_status = 2
                    self.sfx_to_play = "LAUNCH"
                    self.waitingforanim = "throttledown"
                    self.animstates["throttledown"].activate(1)

            else:
                self.menu_info["actiontext"] = "No effect"

        # Transfer
        elif (142 <= mouse_pos[1] <= 180) and (77 <= mouse_pos[0] <= 104):

            if self.current_shipgroup.type == 2:
                self.menu_info["actiontext"] = "Transfer"
                if mouse_buttonevent[0]:
                    self.sfx_to_play = "TRANSFER"
                    self.action = "TRANSFER"

        # Move
        elif (138 <= mouse_pos[1]) and (132 <= mouse_pos[0] <= 188):

            if self.current_shipgroup.orbit_status == 1:
                self.menu_info["actiontext"] = "No effect"
            else:
                if self.shipgroup_moving:
                    self.menu_info["actiontext"] = "Change destination"
                else:
                    self.menu_info["actiontext"] = "Move"
                if mouse_buttonevent[0]:
                    self.sfx_to_play = "CONTROLL"
                    self.waitingforanim = "stick"
                    self.animstates["stick"].activate(1)

        # Ships
        elif (145 <= mouse_pos[1] <= 184) and (202 <= mouse_pos[0] <= 249):

            self.menu_info["actiontext"] = "Ships"
            if mouse_buttonevent[0]:
                self.sfx_to_play = "SHIP"
                self.action = "SHIP INFO"

        # Group
        elif (154 <= mouse_pos[1]) and (254 <= mouse_pos[0]):

            self.menu_info["actiontext"] = "Group"
            if mouse_buttonevent[0]:
                self.sfx_to_play = "GROUP"
                self.action = "GROUP"

