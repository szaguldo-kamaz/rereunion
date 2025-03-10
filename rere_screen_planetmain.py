# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_planetmain(screen):

    def __init__(self, gamedata_static, gamedata_dynamic, planet, selected_building_index = 0, map_position = None):

        self.gamedata_static = gamedata_static

        self.screentype = "planetmain"

        menu_icons = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET INFO", "SHIP INFO", "PLANET FORCES" ]
        menu_text  = [ "BACK TO M.SCREEN", "GALACTIC MAP", "PLANET INFO", "SPACEPORT", "PLANET FORCES" ]
        menu_sfx   = [ "BACK", "STARMAP", "PLANETIN", "SHIP", "PLANETFO" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = True
        self.add_anim("surface",       3, 5, 1)
        self.add_anim("builddemolish", 2, 5, 1)

        self.screenmode_buildinginfo = False
        self.screenmode_buildinginfo_specific = False
        self.selected_building_on_map = None

        self.planet = planet
        if self.planet.possible_buildings_list != []:
            self.__select_building_by_index(selected_building_index)
        else:
            self.selected_building_is_first = True
            self.selected_building_is_last = True

        map_size_x_half = int(self.planet.map_terrain.map_size[0] / 2)
        map_size_y_half = int(self.planet.map_terrain.map_size[1] / 2)
        if map_position == None:
            map_position_center = (map_size_x_half - 7, map_size_y_half - 4)
            self.map_position = map_position_center
        else:
            self.map_position = map_position
        self.demolish_mode = False
        self.build_mode = False
        self.build_mode_building_pos = None
        self.build_mode_building_tiles = None

#        self.map_of_scrolls = "qqqquuuuuueeee" + \
#                              "qqqquuuuuueeee" + \
#                              "qqlluuuuuurree" + \
#                              "lllllluurrrrrr" + \
#                              "lllllllrrrrrrr" + \
#                              "llllllddrrrrrr" + \
#                              "zzllddddddrrcc" + \
#                              "zzzzddddddcccc" + \
#                              "zzzzddddddcccc"

        self.scroll_vectors = [ (-1, -1), (-1, -1), (-1, -1), (-1, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), (+1, -1), (+1, -1), (+1, -1), (+1, -1),
                                (-1, -1), (-1, -1), (-1, -1), (-1, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), (+1, -1), (+1, -1), (+1, -1), (+1, -1),
                                (-1, -1), (-1, -1), (-1,  0), (-1,  0), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), ( 0, -1), (+1,  0), (+1,  0), (+1, -1), (+1, -1),
                                (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), ( 0, -1), ( 0, -1), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0),
                                (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0),
                                (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), (-1,  0), ( 0, +1), ( 0, +1), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0), (+1,  0),
                                (-1, +1), (-1, +1), (-1,  0), (-1,  0), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), (+1,  0), (+1,  0), (+1, +1), (+1, +1),
                                (-1, +1), (-1, +1), (-1, +1), (-1, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), (+1, +1), (+1, +1), (+1, +1), (+1, +1),
                                (-1, +1), (-1, +1), (-1, +1), (-1, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), ( 0, +1), (+1, +1), (+1, +1), (+1, +1), (+1, +1) ]

        self.toscroll_horizontal = 0
        self.toscroll_vertical = 0

        # yellow frame
        self.radar_frame_centerpos = (45, 168)
        self.radar_frame_rect_size = ( self.planet.map_terrain.map_size[0] + 2,
                                       self.planet.map_terrain.map_size[1] + 2)
        self.radar_frame_rect_pos  = ( ( self.radar_frame_centerpos[0] - map_size_x_half,
                                         self.radar_frame_centerpos[1] - map_size_y_half ),   # top left
                                       ( self.radar_frame_centerpos[0] + map_size_x_half,
                                         self.radar_frame_centerpos[1] + map_size_y_half ) )  # bottom right
        # red frame
        self.radar_viewer_rect_size = (14, 9)


    def __select_building_by_index(self, building_index):

        self.selected_building_index = building_index
        self.selected_building_type = self.planet.possible_buildings_list[building_index]
        self.selected_building_typeinfo = self.planet.gamedata_static["buildings_info"][self.selected_building_type]

        if self.selected_building_type == 1:
            self.selected_building_is_first = True
        else:
            self.selected_building_is_first = False

        if self.selected_building_type == self.planet.possible_buildings_list[-1]:
            self.selected_building_is_last = True
        else:
            self.selected_building_is_last = False


    def __select_building_by_type(self, building_type):

        for building_index in range(len(self.planet.possible_buildings_list)):
            if self.planet.possible_buildings_list[building_index] == building_type:
                break

        self.__select_building_by_index(building_index)


    def set_map_position(self, new_map_position):
        # 14x9 tile-bol all a surface map
        map_size = self.planet.map_terrain.map_size
        new_map_position[0] = max(0, new_map_position[0])
        new_map_position[1] = max(0, new_map_position[1])
        new_map_position[0] = min(map_size[0] - 14, new_map_position[0])
        new_map_position[1] = min(map_size[1] -  9, new_map_position[1])
        self.map_position = tuple(new_map_position)


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        if (self.toscroll_horizontal != 0) or (self.toscroll_vertical != 0):
            self.set_map_position([ self.map_position[0] + self.toscroll_horizontal,
                                    self.map_position[1] + self.toscroll_vertical ])
        self.toscroll_horizontal = 0
        self.toscroll_vertical = 0

        self.build_mode_building_pos = None
        self.build_mode_building_tiles = None

        if self.screenmode_buildinginfo:

            if (53 <= mouse_pos[1] <= 199) and (90 <= mouse_pos[0] <= 319) or \
               (64 <= mouse_pos[1] <= 127) and (12 <= mouse_pos[0] <=  90):
                self.menu_info["actiontext"] = 'See surface'
                if mouse_buttonevent[0]:  # mouse button was pressed
                    self.screenmode_buildinginfo = False
                    self.screenmode_buildinginfo_specific = False
                    self.sfx_to_play = "X"

        else:

            # Terrain
            if (53 <= mouse_pos[1] <= 196) and (93 <= mouse_pos[0] <= 316):

                self.menu_info["actiontext"] = 'Terrain'

                if self.build_mode:

                    mouse_on_terrain_tile = ( int((mouse_pos[0] - 93) / 16), int((mouse_pos[1] - 53) / 16) )
                    mouse_on_terrain_tile_1d = mouse_on_terrain_tile[0] + mouse_on_terrain_tile[1] * 14

                    self.build_mode_building_pos = mouse_on_terrain_tile
                    tobuild_tiles_y = len(self.selected_building_typeinfo['tilecodes'])
                    tobuild_tiles_x = len(self.selected_building_typeinfo['tilecodes'][0])

                    self.build_mode_building_tiles = []

                    build_mode_building_can_be_built = True
                    build_mode_tobuild_basepos = (self.map_position[0] + mouse_on_terrain_tile[0] + 1,
                                                  self.map_position[1] + mouse_on_terrain_tile[1] + 1)
                    for tilepos_y in range(tobuild_tiles_y):
                        self.build_mode_building_tiles.append([])
                        self.build_mode_building_tiles[tilepos_y] = []
                        for tilepos_x in range(tobuild_tiles_x):
                            abs_tilepos_x = build_mode_tobuild_basepos[0] + tilepos_x
                            abs_tilepos_y = build_mode_tobuild_basepos[1] + tilepos_y
                            if abs_tilepos_x > self.planet.map_terrain.map_size[0] or \
                               abs_tilepos_y > self.planet.map_terrain.map_size[1]:
                                tilecode = -1
                                build_mode_building_can_be_built = False
                            else:
                                map_xy_index = abs_tilepos_x + \
                                               (abs_tilepos_y) * (self.planet.map_terrain.map_size[0] + 1)
                                if self.planet.map_buildings[map_xy_index] != -1 or \
                                   self.planet.map_terrain.map_obstacles[map_xy_index] == 1:
                                    tilecode = -1
                                    build_mode_building_can_be_built = False
                                else:
                                    tilecode = self.selected_building_typeinfo['tilecodes'][tilepos_y][tilepos_x]
                            self.build_mode_building_tiles[tilepos_y].append(tilecode)


                # Scroll over surface map (terrain) using right mouse button
                if mouse_buttonstate[2]:  # right mouse button is being pressed

                    mouse_on_terrain_tile = ( int((mouse_pos[0] - 93) / 16), int((mouse_pos[1] - 53) / 16) )
                    mouse_on_terrain_tile_1d = mouse_on_terrain_tile[0] + mouse_on_terrain_tile[1] * 14
                    [ self.toscroll_horizontal, self.toscroll_vertical ] = self.scroll_vectors[mouse_on_terrain_tile_1d]

                # Select building on surface map (terrain)
                if mouse_buttonevent[0] and mouse_buttonstate[0]:

                    if self.build_mode:  # left mouse button was pressed - while in build mode
                        if build_mode_building_can_be_built:
                            self.sfx_to_play = "BUILDIN"
                            self.build_mode = False
                            building_cost = self.planet.build_new_building(self.selected_building_type, build_mode_tobuild_basepos)
                            gamedata_dynamic["money"] -= building_cost
                        else:
                            self.sfx_to_play = "HIBA"

                    else:  # left mouse button was pressed - not in build mode
                        mouse_on_map_pos = ( int((mouse_pos[0] - 93)/16) + 1, int((mouse_pos[1] - 52)/16) + 1 )
                        map_xy_index = self.map_position[0] + mouse_on_map_pos[0] + \
                                       (self.map_position[1] + mouse_on_map_pos[1]) * (self.planet.map_terrain.map_size[0] + 1)
                        building_no = self.planet.map_buildings[map_xy_index]

                        if building_no > -1:  # valid building has been selected ?
                            if self.demolish_mode:
                                if self.planet.demolish_building(building_no):
                                    self.sfx_to_play = "DESTRUCT"
                                else:
                                    self.sfx_to_play = "X"
                                self.demolish_mode = False
                            else:
                                self.sfx_to_play = "X"
                                self.selected_building_on_map = self.planet.buildings[building_no]
                                if self.selected_building_on_map.building_type in [ 4, 25 ]:  # mine, miner station
                                    self.action = "MINE"
                                    self.action_params = [ self.planet, self.map_position ]
                                    self.sfx_to_play = "MINE"
                                else:
                                    self.__select_building_by_type(self.selected_building_on_map.building_type)
                                    self.screenmode_buildinginfo = True
                                    self.screenmode_buildinginfo_specific = True

            elif 53 <= mouse_pos[1] <= 196 and 90 <= mouse_pos[0] <= 92:

                self.menu_info["actiontext"] = 'Left'
                if mouse_buttonstate[0]:  # left mouse button is being pressed
                    self.toscroll_horizontal = -1

            elif 53 <= mouse_pos[1] <= 196 and 317 <= mouse_pos[0] <= 319:

                self.menu_info["actiontext"] = 'Right'
                if mouse_buttonstate[0]:  # left mouse button is being pressed
                    self.toscroll_horizontal = +1

            elif 50 <= mouse_pos[1] <= 52 and 93 <= mouse_pos[0] <= 316:

                self.menu_info["actiontext"] = 'Up'
                if mouse_buttonstate[0]:  # left mouse button is being pressed
                    self.toscroll_vertical = -1

            elif 197 <= mouse_pos[1] <= 199 and 93 <= mouse_pos[0] <= 316:

                self.menu_info["actiontext"] = 'Down'
                if mouse_buttonstate[0]:  # left mouse button is being pressed
                    self.toscroll_vertical = +1

            # Radar viewer
            elif 138 <= mouse_pos[1] <= 200 and 0 <= mouse_pos[0] <= 89:

                self.menu_info["actiontext"] = 'Radar'
                if any(mouse_buttonstate):  # any mouse button is being pressed
                    new_radar_viewer_pos = [mouse_pos[0] - self.radar_frame_rect_pos[0][0] - int(self.radar_viewer_rect_size[0] / 2),
                                            mouse_pos[1] - self.radar_frame_rect_pos[0][1] - int(self.radar_viewer_rect_size[1] / 2)]
                    new_radar_viewer_pos[0] = max(0, new_radar_viewer_pos[0])
                    new_radar_viewer_pos[1] = max(0, new_radar_viewer_pos[1])
                    new_radar_viewer_pos[0] = min(self.planet.map_terrain.map_size[0] - self.radar_viewer_rect_size[0], new_radar_viewer_pos[0])
                    new_radar_viewer_pos[1] = min(self.planet.map_terrain.map_size[1] - self.radar_viewer_rect_size[1], new_radar_viewer_pos[1])

                    self.set_map_position(new_radar_viewer_pos)

            # Build icon
            elif 50 <= mouse_pos[1] <= 62 and 0 <= mouse_pos[0] <= 43:

                if self.planet.colony == 0:
                    self.menu_info["actiontext"] = 'No effect'
                else:
                    self.menu_info["actiontext"] = 'Build'
                    if mouse_buttonevent[0]:  # mouse button pressed
                        if not self.build_mode:
                            if gamedata_dynamic["commanders"][1] == 0:
                                print(self.gamedata_static["planetmain_messages"][5])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif gamedata_dynamic["commanders"][1] < self.selected_building_typeinfo['minimum_developer']:
                                current_builder_name = self.gamedata_static["commander_names"][1][gamedata_dynamic["commanders"][1]-1]
                                print(current_builder_name + self.gamedata_static["planetmain_messages"][0])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif self.selected_building_typeinfo['price'] > gamedata_dynamic["money"]:
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif self.selected_building_typeinfo['requires_builder_plant'] == 1 and not self.planet.has_builder_plant:
                                print(self.gamedata_static["planetmain_messages"][2])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif self.selected_building_typeinfo['requires_vehicle_plant'] == 1 and not self.planet.has_vehicle_plant:
                                print(self.gamedata_static["planetmain_messages"][1])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif self.selected_building_typeinfo['name'] == b'Command centre':
                                print(self.gamedata_static["planetmain_messages"][4])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            elif self.selected_building_typeinfo['name'] == b'Miner station ':
                                print(self.gamedata_static["planetmain_messages"][3])
                                self.sfx_to_play = "HIBA"
                                self.build_mode = False
                            else:
                                self.sfx_to_play = "BUILD"
                                self.build_mode = True
                                self.demolish_mode = False
                                self.animstates["builddemolish"].setframe(1)
                                self.animstates["builddemolish"].resettick()
                        else:
                            self.sfx_to_play = "X"
                            self.build_mode = False

            # Demolish icon
            elif 50 <= mouse_pos[1] <= 62 and 45 <= mouse_pos[0] <= 88:

                if self.planet.colony == 0:
                    self.menu_info["actiontext"] = 'No effect'
                else:
                    self.menu_info["actiontext"] = 'Destroy'
                    if mouse_buttonevent[0]:  # mouse button pressed
                        if not self.demolish_mode:
                            self.sfx_to_play = "X"
                            self.build_mode = False
                            self.demolish_mode = True
                            self.animstates["builddemolish"].setframe(1)
                            self.animstates["builddemolish"].resettick()
                        else:
                            self.sfx_to_play = "X"
                            self.demolish_mode = False

            # Invention info
            elif (64 <= mouse_pos[1] <= 127) and (12 <= mouse_pos[0] <=  88):
                self.menu_info["actiontext"] = 'Invention Info'
                if mouse_buttonevent[0]:
                    self.screenmode_buildinginfo = True
                    self.screenmode_buildinginfo_specific = False
                    self.sfx_to_play = "X"


        # Common in Terrain / Building info mode

        if not self.screenmode_buildinginfo_specific:
            # Invention up
            if 64 <= mouse_pos[1] <= 95 and 0 <= mouse_pos[0] <= 10:

                if self.planet.colony == 0:
                    self.menu_info["actiontext"] = 'No effect'
                else:
                    self.menu_info["actiontext"] = 'Invention up'
                    self.build_mode = False
                    self.demolish_mode = False
                    if mouse_buttonevent[0]:  # mouse button pressed
                        self.sfx_to_play = "X"
                        if not self.selected_building_is_first:
                            self.__select_building_by_index(self.selected_building_index - 1)

            # Invention down
            elif 97 <= mouse_pos[1] <= 128 and 0 <= mouse_pos[0] <= 10:

                if self.planet.colony == 0:
                    self.menu_info["actiontext"] = 'No effect'
                else:
                    self.menu_info["actiontext"] = 'Invention down'
                    self.build_mode = False
                    self.demolish_mode = False
                    if mouse_buttonevent[0]:  # mouse button pressed
                        self.sfx_to_play = "X"
                        if not self.selected_building_is_last:
                            self.__select_building_by_index(self.selected_building_index + 1)

