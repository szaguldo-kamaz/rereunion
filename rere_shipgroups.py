# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import math

class shipgroup:


    def __init__(self, groupname, grouptype, initial_groupraw_data = None):

        self.__cargonames = (  # see also: process_raw_groupdata() in rere_game.py
                             "Mineral1",
                             "Mineral2",
                             "Mineral3",
                             "Mineral4",
                             "Mineral5",
                             "Mineral6",
                             "Ship1",
                             "unknown1",  # maybe unused
                             "unknown2",  # maybe unused
                             "unknown3",  # maybe unused
                             "Vehicle1",
                             "Vehicle2",
                             "Vehicle3",
                             "Vehicle4",
                             "Equip1",
                             "Equip2",
                             "Equip3",
                             "Equip4",
                             "MinerDroid",
                             "unknown4"
                            )

        if initial_groupraw_data == None:

            self.type = grouptype  # type: 1 army, 2 trade, (3 pirate), 4 carrier
            self.name = groupname
            self.location = ( 1, 5, 0 )  # groups are always created on New Earth
            self.orbit_status = 1  # orbit status: 1 grounded, 2 orbiting planet, ?4 in transit within system?, ?6 in transit through systems?
            self.remaining_travel_time_between_solsystems = 0
            self.outside_destination_solsystem = 0
            self.remaining_travel_time_inside_solsystem = 0

            if self.type in [1, 5]:  # army / ground forces

                self.fleet = {
                    "Ship1":    0, "Ship1_Equip1":     0, "Ship1_Equip2":     0, "Ship1_Equip3":    -1, "Ship1_Equip4":    -1,
                    "Ship2":    0, "Ship2_Equip1":    -1, "Ship2_Equip2":     0, "Ship2_Equip3":     0, "Ship2_Equip4":    -1,
                    "Ship3":    0, "Ship3_Equip1":    -1, "Ship3_Equip2":     0, "Ship3_Equip3":     0, "Ship3_Equip4":    -1,
                    "Ship4":    0, "Ship4_Equip1":    -1, "Ship4_Equip2":     0, "Ship4_Equip3":     0, "Ship4_Equip4":     0,
                    "Vehicle1": 0, "Vehicle1_Equip1":  0, "Vehicle1_Equip2": -1, "Vehicle1_Equip3": -1, "Vehicle1_Equip4": -1,
                    "Vehicle2": 0, "Vehicle2_Equip1":  0, "Vehicle2_Equip2":  0, "Vehicle2_Equip3": -1, "Vehicle2_Equip4": -1,
                    "Vehicle3": 0, "Vehicle3_Equip1": -1, "Vehicle3_Equip2":  0, "Vehicle3_Equip3":  0, "Vehicle3_Equip4": -1,
                    "Vehicle4": 0, "Vehicle4_Equip1": -1, "Vehicle4_Equip2": -1, "Vehicle4_Equip3":  0, "Vehicle4_Equip4": -1
                }

            elif self.type == 2:  # trade

                self.fleet = {
                     "Ship1": 0, "Ship1_Equip1": -1, "Ship1_Equip2": -1, "Ship1_Equip3": -1, "Ship1_Equip4":  0,
                     "Ship2": 0, "Ship2_Equip1": -1, "Ship2_Equip2": -1, "Ship2_Equip3": -1, "Ship2_Equip4":  0,
                     "Ship3": 0, "Ship3_Equip1":  0, "Ship3_Equip2":  0, "Ship3_Equip3":  0, "Ship3_Equip4": -1,
                     "Ship4": 0, "Ship4_Equip1":  0, "Ship4_Equip2": -1, "Ship4_Equip3": -1, "Ship4_Equip4":  0,
                }

            elif self.type == 4:  # carrier

                self.fleet = {
                     "Ship1": 0, "Ship1_Equip1": 0, "Ship1_Equip2": 0, "Ship1_Equip3": 0, "Ship1_Equip4": 0,
                }

            else:
                print(f"FATAL: Invalid shipgroup type: {self.type}!")
                exit(1)

            self.transfer = {}
            for cargoname in self.__cargonames:
                self.transfer[cargoname] = 0

        else:

            self.type = initial_groupraw_data['type']  # type: 1 army, 2 trade, (3 pirate), 4 carrier
            self.name = initial_groupraw_data['name']
            self.location = (
                             initial_groupraw_data['system_no'],
                             initial_groupraw_data['planet_no'],
                             initial_groupraw_data['moon_no']
                            )
            self.orbit_status = initial_groupraw_data['orbit_status']  # orbit status: 1 grounded, 2 orbiting planet, ?4 in transit wihtin system?, ?6 in transit through systems?
            self.remaining_travel_time_between_solsystems = initial_groupraw_data['travel_time_between_solsystems']
            self.outside_destination_solsystem = initial_groupraw_data['outside_destination_solsystem']
            self.remaining_travel_time_inside_solsystem = initial_groupraw_data['travel_time_inside_solsystem']

            if self.type in [1, 5]:  # army
                self.fleet = {
                    "Ship1":           initial_groupraw_data['Ship1'],
                    "Ship1_Equip1":    initial_groupraw_data['Ship1_Equip1'],
                    "Ship1_Equip2":    initial_groupraw_data['Ship1_Equip2'],
                    "Ship1_Equip3":    -1,
                    "Ship1_Equip4":    -1,
                    "Ship2":           initial_groupraw_data['Ship2'],
                    "Ship2_Equip1":    -1,
                    "Ship2_Equip2":    initial_groupraw_data['Ship2_Equip2'],
                    "Ship2_Equip3":    initial_groupraw_data['Ship2'],
                    "Ship2_Equip4":    -1,
                    "Ship3":           initial_groupraw_data['Ship3'],
                    "Ship3_Equip1":    -1,
                    "Ship3_Equip2":    initial_groupraw_data['Ship3_Equip2'],
                    "Ship3_Equip3":    initial_groupraw_data['Ship3'],
                    "Ship3_Equip4":    initial_groupraw_data['Ship3_Equip4'],
                    "Ship4":           initial_groupraw_data['Ship4'],
                    "Ship4_Equip1":    -1,
                    "Ship4_Equip2":    initial_groupraw_data['Ship4_Equip2'],
                    "Ship4_Equip3":    initial_groupraw_data['Ship4'],
                    "Ship4_Equip4":    initial_groupraw_data['Ship4_Equip4'],
                    "Vehicle1":        initial_groupraw_data['Vehicle1'],
                    "Vehicle1_Equip1": initial_groupraw_data['Vehicle1_Equip1'],
                    "Vehicle1_Equip2": -1,
                    "Vehicle1_Equip3": -1,
                    "Vehicle1_Equip4": -1,
                    "Vehicle2":        initial_groupraw_data['Vehicle2'],
                    "Vehicle2_Equip1": initial_groupraw_data['Vehicle2_Equip1'],
                    "Vehicle2_Equip2": initial_groupraw_data['Vehicle2_Equip2'],
                    "Vehicle2_Equip3": -1,
                    "Vehicle2_Equip4": -1,
                    "Vehicle3":        initial_groupraw_data['Vehicle3'],
                    "Vehicle3_Equip1": -1,
                    "Vehicle3_Equip2": initial_groupraw_data['Vehicle3_Equip2'],
                    "Vehicle3_Equip3": initial_groupraw_data['Vehicle3_Equip3'],
                    "Vehicle3_Equip4": -1,
                    "Vehicle4":        initial_groupraw_data['Vehicle4'],
                    "Vehicle4_Equip1": -1,
                    "Vehicle4_Equip2": -1,
                    "Vehicle4_Equip3": initial_groupraw_data['Vehicle4_Equip3'],
                    "Vehicle4_Equip4": -1,
                }

            elif self.type == 2:  # trade
                self.fleet = {
                    "Ship1":        initial_groupraw_data['Ship1'],
                    "Ship1_Equip1": -1,
                    "Ship1_Equip2": -1,
                    "Ship1_Equip3": -1,
                    "Ship1_Equip4": initial_groupraw_data['Ship1_Equip4'],
                    "Ship2":        initial_groupraw_data['Ship2'],
                    "Ship2_Equip1": -1,
                    "Ship2_Equip2": -1,
                    "Ship2_Equip3": -1,
                    "Ship2_Equip4": initial_groupraw_data['Ship2_Equip4'],
                    "Ship3":        initial_groupraw_data['Ship3'],
                    "Ship3_Equip1": initial_groupraw_data['Ship3_Equip1'],
                    "Ship3_Equip2": initial_groupraw_data['Ship3_Equip2'],
                    "Ship3_Equip3": initial_groupraw_data['Ship3_Equip3'],
                    "Ship3_Equip4": -1,
                    "Ship4":        initial_groupraw_data['Ship4'],
                    "Ship4_Equip1": initial_groupraw_data['Ship4_Equip1'],
                    "Ship4_Equip2": -1,
                    "Ship4_Equip3": -1,
                    "Ship4_Equip4": initial_groupraw_data['Ship4_Equip4']
                }

            elif self.type == 4:  # carrier
                self.fleet = {
                    "Ship1":        initial_groupraw_data['Ship1'],
                    "Ship1_Equip1": initial_groupraw_data['Ship1_Equip1'],
                    "Ship1_Equip2": initial_groupraw_data['Ship1_Equip2'],
                    "Ship1_Equip3": initial_groupraw_data['Ship1_Equip3'],
                    "Ship1_Equip4": initial_groupraw_data['Ship1_Equip4']
                }

            else:
                print(f"FATAL: Invalid shipgroup type: {self.type}!")
                exit(1)

            self.transfer = {}
            for cargoname in self.__cargonames:
                self.transfer[cargoname] = initial_groupraw_data[f"Transfer_{cargoname}"]

        self.update()


    def update(self):

        # TODO, get real value
        commander_pilot_scholar_level = 73

        self.remaining_flight_time = math.ceil(self.remaining_travel_time_between_solsystems / (commander_pilot_scholar_level) + 1)
        self.remaining_flight_time += math.ceil(self.remaining_travel_time_inside_solsystem / (commander_pilot_scholar_level) + 1)
