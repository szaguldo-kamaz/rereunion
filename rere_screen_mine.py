# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_mine(screen):

    def __init__(self, gamedata_dynamic, planet, preserved_surface_position):

        self.screentype = "mine"

        menu_icons = [ "BACK TO M.SCREEN", "PLANET MAIN", "ADD DROIDS" ]
        menu_text  = [ "BACK TO M.SCREEN", "PLANET MAIN", "ADD DROIDS" ]
        menu_sfx   = [ "BACK", "PLANET", "ADDROID" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = False
        self.planet = planet
        self.current_planet_surface = self.planet.planet_id
        self.preserved_surface_position = preserved_surface_position
        self.update(gamedata_dynamic, (0, 0), [0,0,0], [0,0,0])


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.num_of_droids_active = self.planet.miner_droids
        self.num_of_droids_stock = min(self.planet.storage["miner_droids"], 99)
        self.num_of_mines = min(self.planet.num_of_mines, 99)
        self.mineral_storage = self.planet.mineral_storage
        self.mineral_production = self.planet.mineral_production_actual.copy()
        self.mineral_production["Detoxin"] = -1  # Detoxin production is censored

        [ menuaction, menuaction_params ] = self.get_action()
        if menuaction != None:
            if   menuaction == 'ADD DROIDS':
                if not self.planet.add_droid():
                    self.sfx_to_play = "X"
            else:
                self.action = menuaction
                self.action_params = menuaction_params

        if (53 <= mouse_pos[1] <= 199) and (0 <= mouse_pos[0] <= 320):
            self.menu_info["actiontext"] = 'Back to surface'
            if mouse_buttonevent[0]:
                self.action = "PLANET MAIN"
                self.action_params = [ self.current_planet_surface, self.preserved_surface_position ]
                self.sfx_to_play = "SURFACE"
