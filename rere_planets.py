# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

# TODO ground forces, race known

class solarsystem:


    class planet:


        class building:

            def __init__(self, building_type, building_type_data, pos):
                self.building_type = building_type
                self.building_data = building_type_data  # gamestatic["buildings_info"] -bol csak a tipusra vonatkozo
                self.pos = pos
                self.time_to_finish = 100 # +- random ? TODO
                self.performance = 0
                self.active = 0
                self.workers = 0
                self.energy_use = 0
                self.working = 0
                # used by gfx when rendering on map (calculate here just once, not at every rendering)
                self.pixelpos = ( (pos[0] - 1) * 16, (pos[1] - 1) * 16 )


            def update(self):
                self.time_to_finish -= 10
                if self.time_to_finish <= 0:
                    self.time.to_finish = 0
                    self.active = 1
                    self.energy_use = self.building_data["energy_use"]  # * random(0.5-1.0)?
                    self.workers = self.building_data["workers"]


        class planetsurface:

            def __init__(self, maptuple):

                self.map_major = maptuple[0]
                self.map_minor = maptuple[1]
                mapfile = open("MAP/MAP%d_%d.MAP"%(self.map_major, self.map_minor), "rb")
                self.map_size = list(mapfile.read(2))
                self.map_data = mapfile.read()
                mapfile.close()

        #############
        ### planet
        #######
        def __init__(self, planet_data, gamedata_static, cache):

            self.gamedata_static = gamedata_static

            self.planetname = planet_data["planetname"]
            self.planettype = planet_data["planettype"]
            self.mapnumber = planet_data["mapnumber"]
            self.map_id = (self.planettype, self.mapnumber)
            self.diameter = planet_data["diameter"]
            self.temperature = planet_data["temperature"]
            self.orbitingvelocity = planet_data["orbitingvelocity"]
            self.orbitdistance = planet_data["orbitdistance"]
            self.mainplanet = planet_data["mainplanet"]
            self.mineable = planet_data["mineable"]
            self.lifesupporting = planet_data["lifesupporting"]
            self.race = planet_data["race"]
            self.colony = planet_data["colony"]
            self.miner_droids = planet_data["miner_droids"]
            self.population_count = planet_data["population_count"]
            self.population_mood = planet_data["population_mood"]
            self.development_level = planet_data["development_level"]
            self.tax_level = planet_data["tax_level"]
            self.mineral_storage = planet_data["mineral_storage"]
            self.mineral_production = planet_data["mineral_production"]
            self.deployed_sat_type = planet_data["deployed_sat_type"]
            self.deployed_spy_ship = planet_data["deployed_spy_ship"]
            self.solarsat_count = planet_data["solarsat_count"]
            self.sat_exploration_timecount = planet_data["sat_exploration_timecount"]

            self.storage = { "miner_droids" : 0, "hunter" : 0 }

            self.has_radar = False
            self.has_spaceport = False
            self.has_university = False
            self.has_stadium = False
            self.has_builder_plant = False
            self.has_vehicle_plant = False
            self.has_medicine_plant = False
            self.has_radshield = False

            self.solar_plants = 0

            self.food_production = 0
            self.food_need = 0
            self.hospital_production = 0
            self.hospital_need = 0
            self.power_production = 0
            self.power_need = 0

            self.radiation = False
            self.meteors = False

            self.possible_buildings_list = []
            self.buildings = []

            if "planetsurfaces" not in cache.keys():
                cache["planetsurfaces"] = {}

            if self.map_id not in cache["planetsurfaces"].keys():
                cache["planetsurfaces"][self.map_id] = self.planetsurface(self.map_id)

            # "raw" binary map
            self.map_terrain = cache["planetsurfaces"][self.map_id]

            self.recreate_map_of_buildings()
            self.update_sat_exploration()
            self.update_possible_buildings_list()


        def update_possible_buildings_list(self):

            self.possible_buildings_list = []
            for building_type in range(1, len(self.gamedata_static["buildings_info"])):
                if self.gamedata_static["buildings_info"][building_type]["can_be_built_on_planet_type"][self.planettype - 1] > 0:
# TODO: "required_invention_no"
# TODO: anti rad shield vs. planet has radiation - original reunion allows radshiled on non-rad planets...
                    self.possible_buildings_list.append(building_type)


        def update_sat_exploration(self):

            if self.deployed_sat_type > 0:
                if self.sat_exploration_timecount < 60:
                    self.sat_exploration_timecount += 1  # mi az egyseg?

            self.mineable_known = (self.sat_exploration_timecount >= 10)
            self.lifesupporting_known = (self.sat_exploration_timecount >= 30)


        def update(self):

            self.update_sat_exploration()

            # new taxlevel
            # TODO
            # new population count
            self.population_count_update()
            # new population morale
            self.population_morale_update()
            # buildings
            self.buildings_update()


        def build_new_building(self, building_type, pos, force_build = False):

            building_type_data = self.gamedata_static["buildings_info"][building_type]

#    keys1 = [ "name", "required_invention_no", "minimum_developer", "unknown1", "requires_builder_plant", "requires_vehicle_plant" ]
#    keys2 = [ "workers", "power_consumption", "zero1", "zero2", "unknown2", "price",
#              "power_off_priority", "time_to_build_mean", "building_size_x", "building_size_y" ]

            if not force_build:
                if building_type_data["requires_builder_plant"] and not self.has_builder_plant:
                    return 1
                if building_type_data["requires_vehicle_plant"] and not self.has_vehicle_plant:
                    return 2

# TODO: building_type_data["minimum_developer"] vs actual commander

            newbuilding = self.building(building_type, building_type_data, pos)
            self.buildings.append(newbuilding)
            building_no = len(self.buildings) - 1

            self.add_building_to_map_of_buildings(building_no)

            return 0


        def add_building_to_map_of_buildings(self, building_to_add_no):

            building_to_add = self.buildings[building_to_add_no]

            for map_y in range(building_to_add.building_data["building_size_y"]):
                map_xy_index = building_to_add.pos[0] + (building_to_add.pos[1] + map_y) * self.map_terrain.map_size[0]
                for map_x in range(building_to_add.building_data["building_size_x"]):
                    self.map_buildings[map_xy_index + map_x] = building_to_add_no


        def recreate_map_of_buildings(self):
            # update map_buildings

            # "raw" map of building without terrain
            # (used for checking occupiedness when building new buildings and for showing building info on surface map)
            # let's waste some memory (first top and left "lines" won't be used), so we can save some cpu later (many "index-1"s)
            # as positiions on the surface map starts from 1
            self.map_buildings = [-1] * ( (self.map_terrain.map_size[0] + 1) * (self.map_terrain.map_size[1] + 1))

            for building_no in range(len(self.buildings)):
                self.add_building_to_map_of_buildings(building_no)


        def demolish_building(self, building_no):

            # "Command centre" cannot be demolished
            if self.buildings[building_no].building_type == 1:
                return False

            building_to_del = self.buildings.pop(building_no)
            del building_to_del

            self.recreate_map_of_buildings()

            return True


        def buildings_update(self):
            for building in self.buildings:
                building.update()
                if bulding.type == minerstation:
                    self.minerstation = True


        def population_count_update(self):
            if self.population_morale == 2:
                self.population += 5


        def population_morale_update(self):
            self.population_morale = 2


        def gather_tax(self):
            return self.population * self.tax_level / 1000  # just made this up, don't know yet how it is calculated originally


        def add_droid(self):
            if self.miner_droid_no < 10 and self.storage["miner_droids"] > 0:
                self.miner_droid_no += 1
                self.storage["miner_droids"] -= 1
                return True
            else:
                return False


        def remove_droid(self):
            if self.miner_droid_no > 0:
                self.miner_droid_no -= 1
                self.storage["miner_droids"] += 1
                return True
            else:
                return False


        def build_colony(self):
            if self.is_colony_possible and not self.colony:
                self.colony = True
                return True
            else:
                return False


        def is_colony_possible(self):
            if not self.lifesupporting_known:
                return None
            else:
                return self.lifesupporting


        def is_mining_possible(self):
            if not self.mineable_known:
                return None
            else:
                return self.mineable


        def increase_tax(self):
            if self.tax == 5:
                return False
            else:
                self.tax += 1


        def decrease_tax(self):
            if self.tax == 0:
                return False
            else:
                self.tax -= 1


    ##################
    ### solarsystem
    ############

    def __init__(self, solsys_id, solsys_name, planets_data, planets_id_mapping, gamedata_static, cache):

        self.solsys_id = solsys_id
        self.solsys_name = solsys_name
        self.num_of_planets = 0
        self.planets = {}

        for planetno in planets_data.keys():
            self.add_planet(planets_data[planetno], planets_id_mapping[planetno], gamedata_static, cache)


    def add_planet(self, planet_data, planet_id, gamedata_static, cache):

        self.num_of_planets += 1
        if planet_id in self.planets.keys():
            print('planets: FATAL: planet "%s" already added! This should never happen.'%(planet_id))
            sys.exit(1)
        self.planets[planet_id] = self.planet(planet_data, gamedata_static, cache)


    def get_numberofplanets(self):
        return len(self.planets)
