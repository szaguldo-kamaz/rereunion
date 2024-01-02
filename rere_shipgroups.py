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
                             "Detoxin",
                             "Energon",
                             "Kremir",
                             "Lepitium",
                             "Raenium",
                             "Texon",
                             "Hunter",
                             "unknown1",  # maybe unused
                             "unknown2",  # maybe unused
                             "unknown3",  # maybe unused
                             "Trooper",
                             "Battle tank",
                             "Aircraft?",
                             "Missilie launcher?",
                             "Laser cannon",
                             "Twin Laser gun",
                             "Missile",
                             "Plasma gun?",
                             "Miner droid",
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
                    "Hunter":    0, "Hunter_Laser":    0, "Hunter_Twin":    0, "Hunter_Miss":    0, "Hunter_Plasma":    0,
                    "Fighter":   0, "Fighter_Laser":   0, "Fighter_Twin":   0, "Fighter_Miss":   0, "Fighter_Plasma":   0,
                    "Destroyer": 0, "Destroyer_Laser": 0, "Destroyer_Twin": 0, "Destroyer_Miss": 0, "Destroyer_Plasma": 0,
                    "Cruiser":   0, "Cruiser_Laser":   0, "Cruiser_Twin":   0, "Cruiser_Miss":   0, "Cruiser_Plasma":   0,
                    "Trooper":   0, "Trooper_Laser":   0, "Trooper_Twin":   0, "Trooper_Miss":   0, "Trooper_Plasma":   0,
                    "Tank":      0, "Tank_Laser":      0, "Tank_Twin":      0, "Tank_Miss":      0, "Tank_Plasma":      0,
                    "Aircraft":  0, "Aircraft_Laser":  0, "Aircraft_Twin":  0, "Aircraft_Miss":  0, "Aircraft_Plasma":  0,
                    "Launcher":  0, "Launcher_Laser":  0, "Launcher_Twin":  0, "Launcher_Miss":  0, "Launcher_Plasma":  0
                }

            elif self.type == 2:  # trade

                self.fleet = {
                     "Sloop":       0, "Sloop_Mine":        0,
                     "Trade ship":  0, "Trade ship_Mine":   0,
                     "Piracy ship": 0, "Piracy ship_Laser": 0, "Piracy ship_Twin": 0, "Piracy ship_Miss": 0,
                     "Galleon":     0, "Galleon_Laser":     0, "Galleon_Mine":     0
                }

            elif self.type == 4:  # carrier

                self.fleet = {
                     "Sat Carr": 0, "Satellite": 0, "Spy Sat": 0, "Spy Ship": 0, "Solar Plant": 0
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
                    "Hunter":           initial_groupraw_data['Ship1'],
                    "Hunter_Laser":     initial_groupraw_data['Ship1_Laser'],
                    "Hunter_Twin":      initial_groupraw_data['Ship1_Twin'],
                    "Hunter_Miss":      initial_groupraw_data['Ship1'],
                    "Hunter_Plasma":    initial_groupraw_data['Ship1_Plasma'],
                    "Fighter":          initial_groupraw_data['Ship2'],
                    "Fighter_Laser":    initial_groupraw_data['Ship2_Laser'],
                    "Fighter_Twin":     initial_groupraw_data['Ship2_Twin'],
                    "Fighter_Miss":     initial_groupraw_data['Ship2'],
                    "Fighter_Plasma":   initial_groupraw_data['Ship2_Plasma'],
                    "Destroyer":        initial_groupraw_data['Ship3'],
                    "Destroyer_Laser":  initial_groupraw_data['Ship3_Laser'],
                    "Destroyer_Twin":   initial_groupraw_data['Ship3_Twin'],
                    "Destroyer_Miss":   initial_groupraw_data['Ship3'],
                    "Destroyer_Plasma": initial_groupraw_data['Ship3_Plasma'],
                    "Cruiser":          initial_groupraw_data['Ship4'],
                    "Cruiser_Laser":    initial_groupraw_data['Ship4_Laser'],
                    "Cruiser_Twin":     initial_groupraw_data['Ship4_Twin'],
                    "Cruiser_Miss":     initial_groupraw_data['Ship4'],
                    "Cruiser_Plasma":   initial_groupraw_data['Ship4_Plasma'],
                    "Trooper":          initial_groupraw_data['Trooper'],
                    "Trooper_Laser":    initial_groupraw_data['Trooper_Laser'],
                    "Trooper_Twin":     initial_groupraw_data['Trooper_Twin'],
                    "Trooper_Miss":     initial_groupraw_data['Trooper_Miss'],
                    "Trooper_Plasma":   initial_groupraw_data['Trooper_Plasma'],
                    "Tank":             initial_groupraw_data['Tank'],
                    "Tank_Laser":       initial_groupraw_data['Tank_Laser'],
                    "Tank_Twin":        initial_groupraw_data['Tank_Twin'],
                    "Tank_Miss":        initial_groupraw_data['Tank_Miss'],
                    "Tank_Plasma":      initial_groupraw_data['Tank_Plasma'],
                    "Aircraft":         initial_groupraw_data['Aircraft'],
                    "Aircraft_Laser":   initial_groupraw_data['Aircraft_Laser'],
                    "Aircraft_Twin":    initial_groupraw_data['Aircraft_Twin'],
                    "Aircraft_Miss":    initial_groupraw_data['Aircraft_Miss'],
                    "Aircraft_Plasma":  initial_groupraw_data['Aircraft_Plasma'],
                    "Launcher":         initial_groupraw_data['Launcher'],
                    "Launcher_Laser":   initial_groupraw_data['Launcher_Laser'],
                    "Launcher_Twin":    initial_groupraw_data['Launcher_Twin'],
                    "Launcher_Miss":    initial_groupraw_data['Launcher_Miss'],
                    "Launcher_Plasma":  initial_groupraw_data['Launcher_Plasma']
                }

            elif self.type == 2:  # trade
                self.fleet = {
                    "Sloop":             initial_groupraw_data['Ship1'],
                    "Sloop_Mine":        initial_groupraw_data['Ship1_Plasma'],
                    "Trade ship":        initial_groupraw_data['Ship2'],
                    "Trade ship_Mine":   initial_groupraw_data['Ship2_Plasma'],
                    "Piracy ship":       initial_groupraw_data['Ship3'],
                    "Piracy ship_Laser": initial_groupraw_data['Ship3_Laser'],
                    "Piracy ship_Twin":  initial_groupraw_data['Ship3_Twin'],
                    "Piracy ship_Miss":  initial_groupraw_data['Ship3_Miss'],
                    "Galleon":           initial_groupraw_data['Ship4'],
                    "Galleon_Laser":     initial_groupraw_data['Ship4_Laser'],
                    "Galleon_Mine":      initial_groupraw_data['Ship4_Plasma']
                }

            elif self.type == 4:  # carrier
                self.fleet = {
                    "Sat Carr":    initial_groupraw_data['Ship1'],
                    "Satellite":   initial_groupraw_data['Ship1_Laser'],
                    "Spy Sat":     initial_groupraw_data['Ship1_Twin'],
                    "Spy Ship":    initial_groupraw_data['Ship1_Miss'],
                    "Solar Plant": initial_groupraw_data['Ship1_Plasma']
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
