# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_planetinfo(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, solarsystems, selected_planet, selected_planet_map_position_preserve):

        self.screentype = "planetinfo"
        self.menu_icons = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET MAIN" ]
        self.menu_text  = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET MAIN" ]
        self.menu_sfx   = [ "BACK", "STARMAP", "SURFACE" ]
        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_static = gamedata_static

        self.anim_exists = False

        self.surfacemode = False
        self.aliennfomode = False

        self.planet = selected_planet
        if self.planet.planet_id[2] == 0:  # is a planet
            self.orbitingplanet = None
            planetname_type_prefix = "PLANET"
        else:  # is a moon
            orbitingplanet_id = self.planet.planet_id[0:2] + ( 0, )
            self.orbitingplanet = solarsystems[orbitingplanet_id[0]].planets[orbitingplanet_id]
            planetname_type_prefix = "MOON"

        self.current_planet_surface = self.planet.planet_id
        self.preserved_surface_position = selected_planet_map_position_preserve
        self.facilities_list = []
        self.planet_type_desc = gamedata_static["planet_type_names"][self.planet.planettype]

        if self.planet.colony == 1:
            if self.planet.race == 1:  # human colony
                self.menu_icons = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET MAIN", "INCREASE TAX", "DECREASE TAX" ]
                self.menu_text  = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET MAIN", "INCREASE TAX", "DECREASE TAX" ]
                self.menu_sfx   = [ "BACK", "STARMAP", "SURFACE", "TAXINC", "TAXDEC" ]
                self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx])
                planetname_owner_prefix = "YOUR"
                self.planet_type_desc += ", colony"
                self.display_fajpic = 1
            else:  # alien colony
                planetname_owner_prefix = gamedata_static["race_nation_names"][self.planet.race-2]
                self.planet_type_desc += ", Alien colony"
                if self.planet.sat_exploration_timecount >= 40:  # race on planet is known
                    self.display_fajpic = self.planet.race
                else:
                    self.display_fajpic = "?"
        else:
            planetname_owner_prefix = ""
            self.display_fajpic = None

        self.planet_name_header = f"{planetname_owner_prefix} {planetname_type_prefix}'S NAME:  {self.planet.planetname}"


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        [ menuaction, menuaction_params ] = self.get_action()
        if menuaction != None:
            if menuaction == 'INCREASE TAX':
                if not self.planet.increase_tax():
                    self.sfx_to_play = "X"
            elif menuaction == 'DECREASE TAX':
                if not self.planet.decrease_tax():
                    self.sfx_to_play = "X"
            else:
                self.action = menuaction
                self.action_params = menuaction_params

        self.facilities_list = []
        if self.planet.colony == 1:
            self.facilities_list.append(self.gamedata_static["planet_facilities_names"][0])
        if self.planet.spacestation_count > 0:
            self.facilities_list.append(str(self.planet.spacestation_count) + self.gamedata_static["planet_facilities_names"][2])
        if self.planet.miner_droids > 0:
            self.facilities_list.append(str(self.planet.miner_droids) + self.gamedata_static["planet_facilities_names"][4])
        if self.planet.solarsat_count > 0:
            self.facilities_list.append(str(self.planet.solarsat_count) + self.gamedata_static["planet_facilities_names"][5])
        if self.planet.deployed_sat_type == 2:
            self.facilities_list.append(self.gamedata_static["planet_facilities_names"][6])
        if self.planet.deployed_spy_ship == 1:
            self.facilities_list.append(self.gamedata_static["planet_facilities_names"][7])

        if self.surfacemode or \
           self.aliennfomode:
            if 49 <= mouse_pos[1]:
                self.menu_info["actiontext"] = 'SEE PLANET INFO'
                if mouse_buttonevent[0]:
                    self.surfacemode = False
                    self.aliennfomode = False
                    self.sfx_to_play = "X"

        else:
            if (49 <= mouse_pos[1] <= 95) and (0 <= mouse_pos[0] <= 56):
                self.menu_info["actiontext"] = 'SEE OWNER INFO'
                if mouse_buttonevent[0]:
                    self.sfx_to_play = "X"
                    if self.planet.race > 1:
                        self.aliennfomode = True

            elif (97 <= mouse_pos[1] <= 143) and (0 <= mouse_pos[0] <= 56):
                self.menu_info["actiontext"] = 'SHIPS'
                if mouse_buttonevent[0]:
                    self.sfx_to_play = "SHIP"
                    self.action = "SHIP INFO"

            elif (145 <= mouse_pos[1] <= 199) and (0 <= mouse_pos[0] <= 95):
                self.menu_info["actiontext"] = 'SEE SURFACE'
                if mouse_buttonevent[0]:
                    self.sfx_to_play = "SURFACE"
                    self.surfacemode = True
