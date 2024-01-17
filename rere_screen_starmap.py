# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_starmap(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, solarsystems):

        self.screentype = "starmap"

        self.menu_icons = [ "BACK TO M.SCREEN" ]
        self.menu_text  = [ "BACK TO M.SCREEN" ]
        self.menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.anim_exists = False
        self.gamedata_static = gamedata_static
        self.solarsystems = solarsystems
        self.location = (1, 0)  # System 1 view by default
        self.parent_location = self.location
        self.selected_solarsystem = self.solarsystems[self.location[0]]
        self.orbit_pixposes = [ [10+planet_no*35, 64] for planet_no in range(8) ]
        self.planet_and_moon_mode = False
        self.selected_planet = None
        self.mousecursor = "normal"


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
                    self.sfx_to_play = "SURFACE"
                    self.action = "PLANET MAIN"
                    self.action_params = [ self.location + (0, ), None ]
                else:
                    self.mousecursor = "cross"

            else:

                for moon_no in range(len(self.selected_planet.moons_ids)):
                    if (self.orbit_pixposes[moon_no][1] <= mouse_pos[1] <= self.orbit_pixposes[moon_no][1] + 16) and \
                       (self.orbit_pixposes[moon_no][0] <= mouse_pos[0] <= self.orbit_pixposes[moon_no][0] + 16):

                        selected_moon_id = self.selected_planet.moons_ids[moon_no]
                        self.menu_info["actiontext"] = self.selected_solarsystem.planets[selected_moon_id].planetname
                        if mouse_buttonevent[0]:
                            self.sfx_to_play = "SURFACE"
                            self.action = "PLANET MAIN"
                            self.action_params = [ self.location + (moon_no + 1,), None ]
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
                        self.zoomout()
                        self.location = (mouse_over_system_no+1, 0)
                        self.selected_solarsystem = self.solarsystems[self.location[0]]
                        self.sfx_to_play = "X"

            else:

                for planet_no in range(self.selected_solarsystem.num_of_planets):
                    if (self.orbit_pixposes[planet_no][1] <= mouse_pos[1] <= self.orbit_pixposes[planet_no][1] + 32) and \
                       (self.orbit_pixposes[planet_no][0] <= mouse_pos[0] <= self.orbit_pixposes[planet_no][0] + 32):

                        full_location = (self.location[0], planet_no + 1, 0)
                        self.menu_info["actiontext"] = self.selected_solarsystem.planets[full_location].planetname
                        self.mousecursor = "cross"
                        if mouse_buttonevent[0]:
                            self.planet_and_moon_mode = True
                            self.parent_location = self.location
                            self.location = full_location[:2]
                            self.selected_solarsystem = self.solarsystems[self.location[0]]
                            self.selected_planet = self.selected_solarsystem.planets[full_location]
                            self.menu_icons = [ "BACK TO M.SCREEN", "ZOOM OUT" ]
                            self.menu_text  = [ "BACK TO M.SCREEN", "ZOOM OUT" ]
                            self.menu_sfx   = [ "BACK", "ZOOMOUT" ]
                            self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
                            self.sfx_to_play = "X"
                            break


    def zoomout(self):

        self.planet_and_moon_mode = False
        self.location = self.parent_location
        self.menu_icons = [ "BACK TO M.SCREEN" ]
        self.menu_text  = [ "BACK TO M.SCREEN" ]
        self.menu_sfx   = [ "BACK" ]
        self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
