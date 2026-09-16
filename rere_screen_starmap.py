# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_starmap(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, solarsystems, shipgroups_spaceforces):

        self.screentype = "starmap"

        self.menu_icons = [ "BACK TO M.SCREEN" ]
        self.menu_text  = [ "BACK TO M.SCREEN" ]
        self.menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.anim_exists = True
        self.add_anim("selectdestination", 2, 5, 1)  # should be 0.2s

        self.gamedata_static = gamedata_static
        self.solarsystems = solarsystems
        self.shipgroups_spaceforces = shipgroups_spaceforces
        self.set_starmaplocation((1, 0))  # System 1 view by default
        self.orbit_pixposes = [ [10+planet_no*35, 64] for planet_no in range(8) ]
        self.planet_and_moon_mode = False
        self.selected_planet = None
        self.mousecursor = "normal"
        self.mode = "surface"


    def set_starmaplocation(self, new_starmaplocation):

        self.starmaplocation = new_starmaplocation
        self.planetandmoonlist = {}
        for location_id in self.solarsystems[self.starmaplocation[0]].planets.keys():
            if location_id[0:2] == self.starmaplocation:
                self.planetandmoonlist[location_id] = self.solarsystems[self.starmaplocation[0]].planets[location_id]
        self.selected_solarsystem = self.solarsystems[self.starmaplocation[0]]


    def set_mode(self, starmap_mode, shipgroup_to_be_moved_location = None):

        if starmap_mode == "controlmove":
            self.mode = "controlmove"
            self.menu_icons = [ "ABORT" ]
            self.menu_text  = [ "ABORT MOVE" ]
            self.menu_sfx   = [ "ABORT" ]
            self.animstates["selectdestination"].activate(1)
            self.shipgroup_to_be_moved_location = shipgroup_to_be_moved_location
            self.set_starmaplocation(shipgroup_to_be_moved_location[0:2])
            self.planet_and_moon_mode = True
            self.selected_planet = self.selected_solarsystem.planets[shipgroup_to_be_moved_location[0:2] + (0,)]
        else:
            self.mode = "surface"
            self.menu_icons = [ "BACK TO M.SCREEN" ]
            self.menu_text  = [ "BACK TO M.SCREEN" ]
            self.menu_sfx   = [ "BACK" ]
            self.animstates["selectdestination"].activate(0)

        if self.planet_and_moon_mode:
            self.menu_icons.append("ZOOM OUT")
            self.menu_text.append("ZOOM OUT")
            self.menu_sfx.append("ZOOMOUT")

        self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.mousecursor = "normal"

        if self.planet_and_moon_mode:  # Planet view

            # Fleet names
            if (49 <= mouse_pos[1] <= 199) and (256 <= mouse_pos[0] <= 319):

                # TODO
                mouse_over_fleet_no = int((mouse_pos[1] - 49)/19)

            elif ( 49+75-16 <= mouse_pos[1] <= 49+75+16) and \
                 (   160-16 <= mouse_pos[0] <= 160+16):

                self.menu_info["actiontext"] = self.selected_planet.planetname
                if mouse_buttonevent[0]:
                    if self.mode == "controlmove":
                        self.sfx_to_play = "MOVESHIP"
                        self.action = "CONTROL PANEL"
                        self.action_params = [ self.starmaplocation + (0, ) ]
                    else:
                        self.sfx_to_play = "SURFACE"
                        self.action = "PLANET MAIN"
                        self.action_params = [ self.starmaplocation + (0, ), None ]
                else:
                    self.mousecursor = "cross"

            else:

                for moon_no in range(len(self.selected_planet.moons_ids)):
                    if (self.orbit_pixposes[moon_no][1] <= mouse_pos[1] <= self.orbit_pixposes[moon_no][1] + 16) and \
                       (self.orbit_pixposes[moon_no][0] <= mouse_pos[0] <= self.orbit_pixposes[moon_no][0] + 16):

                        selected_moon_id = self.selected_planet.moons_ids[moon_no]
                        self.menu_info["actiontext"] = self.selected_solarsystem.planets[selected_moon_id].planetname
                        if mouse_buttonevent[0]:
                            if self.mode == "controlmove":
                                self.sfx_to_play = "MOVESHIP"
                                self.action = "CONTROL PANEL"
                                self.action_params = [ self.starmaplocation + (moon_no + 1,) ]
                            else:
                                self.sfx_to_play = "SURFACE"
                                self.action = "PLANET MAIN"
                                self.action_params = [ self.starmaplocation + (moon_no + 1,), None ]
                            break
                        else:
                            self.mousecursor = "cross"

        else:  # Solarsys view

            # System names
            if (49 <= mouse_pos[1] <= 199) and (256 <= mouse_pos[0] <= 319):

                mouse_over_system_no = int((mouse_pos[1] - 49)/19)
                if gamedata_dynamic["systems_available"][mouse_over_system_no] > -1:
                    self.menu_info["actiontext"] = self.gamedata_static["system_names"][mouse_over_system_no]
                    if mouse_buttonevent[0]:
                        self.set_starmaplocation((mouse_over_system_no+1, 0))
                        self.zoomout()
                        self.sfx_to_play = "X"

            else:

                for planet_no in range(self.selected_solarsystem.num_of_planets):
                    if (self.orbit_pixposes[planet_no][1] <= mouse_pos[1] <= self.orbit_pixposes[planet_no][1] + 32) and \
                       (self.orbit_pixposes[planet_no][0] <= mouse_pos[0] <= self.orbit_pixposes[planet_no][0] + 32):

                        full_location = (self.starmaplocation[0], planet_no + 1, 0)
                        self.menu_info["actiontext"] = self.selected_solarsystem.planets[full_location].planetname
                        self.mousecursor = "cross"
                        if mouse_buttonevent[0]:
                            self.planet_and_moon_mode = True
                            self.set_starmaplocation(full_location[:2])
                            self.selected_planet = self.selected_solarsystem.planets[full_location]
                            if self.mode == "controlmove":
                                self.menu_icons = [ "ABORT", "ZOOM OUT" ]
                                self.menu_text  = [ "ABORT MOVE", "ZOOM OUT" ]
                                self.menu_sfx   = [ "ABORT", "ZOOMOUT" ]
                            else:
                                self.menu_icons = [ "BACK TO M.SCREEN", "ZOOM OUT" ]
                                self.menu_text  = [ "BACK TO M.SCREEN", "ZOOM OUT" ]
                                self.menu_sfx   = [ "BACK", "ZOOMOUT" ]
                            self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
                            self.sfx_to_play = "X"
                            break


    def zoomout(self):

        self.planet_and_moon_mode = False
        self.set_starmaplocation((self.starmaplocation[0], 0))
        if self.mode == "controlmove":
            self.menu_icons = [ "ABORT" ]
            self.menu_text  = [ "ABORT MOVE" ]
            self.menu_sfx   = [ "ABORT" ]
        else:
            self.menu_icons = [ "BACK TO M.SCREEN" ]
            self.menu_text  = [ "BACK TO M.SCREEN" ]
            self.menu_sfx   = [ "BACK" ]
        self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
