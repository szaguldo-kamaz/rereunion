# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import os
import struct
import pygame
import time
from rere_planets import solarsystem
from rere_shipgroups import shipgroup
from rere_screen_controlroom import *
from rere_screen_infobuy import *
from rere_screen_ship import *
from rere_screen_planetmain import *
from rere_screen_mine import *
from rere_screen_researchdesign import *
from rere_screen_starmap import *
from rere_screen_messages import *
from rere_screen_spacelocal import *
from rere_screen_commanders import *


class ReReGame:

    # how to extract this from the main binary?...
    gamedata_const = {}
    gamedata_const["planets_id_mapping"] = {}
    gamedata_const["planets_id_mapping"][1] = {
         # System 1
         1: (1, 1, 0), # 'Amnesty 1'
         2: (1, 2, 0), # 'Klatoo'
         3: (1, 3, 0), # 'Amnesty 2'
         4: (1, 4, 0), # 'Zeus'
         5: (1, 5, 0), # 'New Earth'
         6: (1, 6, 0), # 'Amnesty 3'
         7: (1, 7, 0), # 'Jade'

         8: (1, 1, 1), # 'Ranger'
         9: (1, 1, 2), # 'Venyera'
        10: (1, 1, 3), # 'Explorer'

        11: (1, 2, 1), # 'Barada'
        12: (1, 2, 2), # 'Nikto'

        13: (1, 5, 1), # 'Apollo'

        14: (1, 4, 1), # 'Odysseus'
        15: (1, 4, 2), # 'Syren'
        16: (1, 4, 3), # 'Kyclops'
        17: (1, 4, 4), # 'Penelope'
        18: (1, 4, 5), # 'Ithaca'

        19: (1, 3, 1), # 'Vostok'
        20: (1, 3, 2), # 'Mariner'
        21: (1, 3, 3), # 'Mir'
        22: (1, 3, 4), # 'Arianne'

        23: (1, 6, 1), # 'East'
        24: (1, 6, 2), # 'West'

        25: (1, 7, 1), # 'Wright'
        26: (1, 7, 2), # 'Russel'
        27: (1, 7, 3), # 'Armstrong'
        28: (1, 7, 4), # 'Hartmann'
        29: (1, 7, 5), # 'Aldrin'
        30: (1, 7, 6), # 'Einstein'
        31: (1, 7, 7), # 'Gallilei'
        32: (1, 7, 8)  # 'Kepler'
    }

    gamedata_const["planets_id_mapping"][2] = {
        # System 2

         1: (2, 1, 0), # 'Phoenix 1'
         2: (2, 2, 0), # 'Phoenix 2'
         3: (2, 3, 0), # 'Phoenix 3'
         4: (2, 4, 0), # 'Phoenix 4'
         5: (2, 5, 0), # 'Phoenix 5'

         6: (2, 3, 1), # 'Moon 1'
         7: (2, 3, 2), # 'Moon 2'

         8: (2, 4, 1), # 'Moon 1'
         9: (2, 4, 2), # 'Moon 2'
        10: (2, 4, 3), # 'Moon 3'
        11: (2, 4, 4), # 'Moon 4'

        12: (2, 5, 1)  # 'Moon 1'
    }

    gamedata_const["planets_id_mapping"][3] = {
        # System 3

         1: (3, 1, 0), # 'Mirach 1'
         2: (3, 2, 0), # 'Mirach 2'
         3: (3, 3, 0), # 'Mirach 3'
         4: (3, 4, 0), # 'Mirach 4'
         5: (3, 5, 0), # 'Mirach 5'

         6: (3, 2, 1), # 'Moon 1'
         7: (3, 2, 2), # 'Moon 2'

         8: (3, 3, 1), # 'Moon 1'
         9: (3, 3, 2), # 'Moon 2'

        10: (3, 4, 1), # 'Moon 1'
        11: (3, 4, 2), # 'Moon 2'
        12: (3, 4, 3), # 'Moon 3'
        13: (3, 4, 4), # 'Moon 4'
        14: (3, 4, 5), # 'Moon 5'

        15: (3, 5, 1), # 'Moon 1'
        16: (3, 5, 2), # 'Moon 2'
        17: (3, 5, 3), # 'Moon 3'
        18: (3, 5, 4), # 'Moon 4'
    }


    def extract_dynamic_strings(self, raw_data, rawdata_start, number_of_strings):

        stroffset = 0
        extracted_strings = []
        for planetname_no in range(number_of_strings):
            strlen = int(raw_data[rawdata_start + stroffset])
            stroffset += 1
            extracted_strings.append(raw_data[rawdata_start + stroffset: rawdata_start + stroffset + strlen].decode('ascii'))
            stroffset += strlen

        return extracted_strings


    # raw data from savegame/reunion.prg for one solar system
    def process_raw_planetsdata(self, raw_planetsdata, num_of_planets_and_moons):

        planet_imagepos = 0
        planetsdata = {}

        keys1 = [ "planetname", "orbitingvelocity", "orbitdistance" ]
        for planetno in range(1, num_of_planets_and_moons + 1):  # no 0, to keep original numbering
            unpacklist1 = struct.unpack_from("<10pBH", raw_planetsdata, planet_imagepos)
            planet_imagepos += 13
            planetsdata[planetno] = dict(zip(keys1, unpacklist1))

        keys2 = [ "race", "mainplanet", "lifesupporting", "mineable", "unknown1", "unknown2", "colony", "unknown3",
                  "deployed_sat_type", "deployed_spy_ship", "miner_droids", "solarsat_count", "sat_exploration_timecount",
                  "population_count", "development_level", "tax_level", "population_mood", "unknown4",
                  "planettype", "mapnumber", "diameter", "temperature" ]

        for planetno in range(1, num_of_planets_and_moons + 1):  # no 0, to keep original numbering

            # race:
            #  1 - humans
            #  2 - ja'nos
            #  3 - morg?
            #  4 - kalls?
            #  5 - phelo?
            # unknown1 - csak sajat emberi kolonianal van nullatol kulonbozo erteke
            # unknown2 - csak sajat emberi kolonianal van nullatol kulonbozo erteke, altalaban 255
            # unknown3 - ?
            # unknown4 - ?
            # deployed_sat_type -> 0 - none, 1 - normal sat, 2 - spy sat
            # sat_exploration_timecount - max 60-ig megy miutan ki lett love a sat?, 31-nel megall ha nem ismert a faj?, 40-nel felismeri a fajt?
            #
            # planet_taxlevel
            # 0 - none
            # 1 very low
            # 2 low
            # 3 normal
            # 4 high
            # 5 difficult
            # 6 very difficult
            #
            # development_level
            # 00-19 Under developed
            # 20-29 Poor
            # 30-39 Developing
            # 40-49 Enhanced
            # 50-59 High-tech
            # 60    Super-tech
            #
            # planet_population_mood:
            # 0-9 rebel
            # 10-19 hate
            # 20-29 don't like
            # 30-39 neutral
            # 40-49 find symp
            # 50-59 like
            # 60-69 loyal

            unpacklist2 = struct.unpack_from("<BBBBBBBBBBBBBIBBBBBBHH", raw_planetsdata, planet_imagepos)
            planet_imagepos += 27

            planetsdata[planetno] |= dict(zip(keys2, unpacklist2))

            # minerals storage
            planetsdata[planetno]["mineral_storage"] = {}
            for mineral in self.gamedata_static["mineral_names"]:
                mineral_bytes = raw_planetsdata[planet_imagepos:planet_imagepos + 4]
                planetsdata[planetno]["mineral_storage"][mineral] = struct.unpack("<I", mineral_bytes)[0]
                planet_imagepos += 4

            planetsdata[planetno]["unknown6"] = raw_planetsdata[planet_imagepos:planet_imagepos + 32 - 24]
            planet_imagepos += 32 - 24

            # minerals production (/10)
            planetsdata[planetno]["mineral_production"] = {}
            for mineral in self.gamedata_static["mineral_names"]:
                mineral_bytes = raw_planetsdata[planet_imagepos:planet_imagepos + 1]
                planetsdata[planetno]["mineral_production"][mineral] = struct.unpack("B", mineral_bytes)[0]
                planet_imagepos += 1

            planetsdata[planetno]["planetname"] = planetsdata[planetno]["planetname"].decode('ascii')

    #        print("%d: %s %s"%(planetno, planetsdata[planetno], gamedata_const["planettypes"][planetsdata[planetno]["planettype"]]))

        return planetsdata


    def process_raw_groupdata(self, raw_groupdata, num_of_groups):

        group_imagepos = 0
        groups = {}

        # type: 1 army, 2 trade, (3 pirate), 4 carrier
        # orbit status: 1 grounded, 2 orbiting planet, ?4 in transit within system?, ?6 in transit through systems?

        keys = [ "type", "name", "system_no", "planet_no", "moon_no", "orbit_status",
                 "travel_time_between_solsystems", "outside_destination_solsystem", "travel_time_inside_solsystem",
                 "Ship1", "Ship1_Laser", "Ship1_Twin", "Ship1_Miss", "Ship1_Plasma",
                 "Ship2", "Ship2_Laser", "Ship2_Twin", "Ship2_Miss", "Ship2_Plasma",
                 "Ship3", "Ship3_Laser", "Ship3_Twin", "Ship3_Miss", "Ship3_Plasma",
                 "Ship4", "Ship4_Laser", "Ship4_Twin", "Ship4_Miss", "Ship4_Plasma",
                 "Trooper", "Trooper_Laser", "Trooper_Twin", "Trooper_Miss", "Trooper_Plasma",
                 "Tank", "Tank_Laser", "Tank_Twin", "Tank_Miss", "Tank_Plasma",
                 "Aircraft", "Aircraft_Laser", "Aircraft_Twin", "Aircraft_Miss", "Aircraft_Plasma",
                 "Launcher", "Launcher_Laser", "Launcher_Twin", "Launcher_Miss", "Launcher_Plasma",
                 "Transfer_Detoxin", "Transfer_Energon", "Transfer_Kremir", "Transfer_Lepitium", "Transfer_Raenium", "Transfer_Texon",
                 "Transfer_Hunter", "Transfer_unknown1", "Transfer_unknown2", "Transfer_unknown3",  # star fight?, destroyer?, cruiser?
                 "Transfer_Trooper", "Transfer_Battle tank", "Transfer_Aircraft?", "Transfer_Missilie launcher?",
                 "Transfer_Laser cannon", "Transfer_Twin Laser gun", "Transfer_Missile", "Transfer_Plasma gun?",
                 "Transfer_Miner droid", "Transfer_unknown4" ]

        if num_of_groups > 24:
            print(f"FATAL: number of groups larger than 24 ({num_of_groups})")
            exit(1)  # TODO
        for groupno in range(num_of_groups):  # 24 groups max
            unpacklist = struct.unpack_from("<B18pBBBBHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHIIIIIIHHHHHHHHHHHHHH", raw_groupdata, group_imagepos)
            group_imagepos += 161
            groups[groupno] = dict(zip(keys, unpacklist))
            groups[groupno]["name"] = groups[groupno]["name"].decode("ascii")

#            if 0 < groups[groupno]["type"] < 5:
#                print(groups[groupno])

        return groups


    def process_raw_inventionsdata(self, raw_inventionsdata):

        invention_imagepos = 0
        inventions = {}
        keys1 = [ "name", "research_state", "research_requiredtime", "research_remaining", "price",
                  "quantity_in_production", "quantity_in_storage", "time_to_produce_one", "time_to_produce_next",
                  "can_be_produced_asis", "needs_spacestation" ]

        # 35 inventions in total
        for invention_seqno in range(1, 36):

            unpacklist1 = struct.unpack_from("<17pHHHIHHHHBB", raw_inventionsdata, invention_imagepos)
            invention_imagepos += 37

            # research state 0 - unavailable (not shown)
            # research state 1 - tray with "?" CD
            # research state 2 - tray with "?" CD - in research
            # research state 3 - tray without CD
            # research state 4 - tray without CD - in research
            # research state 5 - done

            inventions[invention_seqno] = dict(zip(keys1, unpacklist1))
#            inventions[invention_seqno]["minerals"] = dict(zip(self.gamedata_static["mineral_names"], struct.unpack("<HHHHHH", raw_inventionsdata[invention_imagepos:invention_imagepos + 12])))
            inventions[invention_seqno]["minerals"] = struct.unpack_from("<HHHHHH", raw_inventionsdata, invention_imagepos)
            invention_imagepos += 12
#            inventions[invention_seqno]["requiredskills"] = dict(zip(self.gamedata_static["skill_names"], struct.unpack("BBBB", raw_inventionsdata[invention_imagepos:invention_imagepos + 4])))
            inventions[invention_seqno]["requiredskills"] = struct.unpack_from("BBBB", raw_inventionsdata, invention_imagepos)
            invention_imagepos += 4

    #        print("%d %s"%(invention_seqno, inventions[invention_seqno]))

        return inventions


    def decode_text(self, encoded_text):

        sentences = encoded_text.split(b'\r\n')
        decoded_text = []

        for sentence in sentences:
            decoded_sentence = ''
            charno = 1
            for character in sentence:
                decoded_sentence += chr(((22400 + character - (charno * 79)) % 224) - 32)
                charno += 1
            decoded_text.append(decoded_sentence)

        return decoded_text


    def load_rawtext(self, rawtext_filename, stringlength, num_of_entries, groupby, strip_right = True, omit_empty = True):

        rawtextfile = open(rawtext_filename, "rb")
        rawtext = rawtextfile.read()
        rawtextfile.close()

        alltext = struct.unpack("<" + f"{stringlength}p" * groupby * num_of_entries, rawtext)

        grouped_text = []
        for idx in range(num_of_entries):
            grouped_text.append([])
            for text_line in range(groupby):
                current_sentence = alltext[groupby*idx + text_line].decode('ascii')
                if strip_right:
                    current_sentence = current_sentence.rstrip()
                if omit_empty:
                    if current_sentence != '':
                        grouped_text[idx].append(current_sentence)
                else:
                    grouped_text[idx].append(current_sentence)

        return grouped_text


    def load_inventionsdesc(self, inventionsdesc_filename = "TEXT/SZ_TALAL.RAW"):
        inventionsdesc = self.load_rawtext(inventionsdesc_filename, 31, 35, 7, omit_empty = False)
        return inventionsdesc


    def load_commandersdesc(self, commandersdesc_filename = "TEXT/SZ_FACE.RAW"):
        commandersdesc = self.load_rawtext(commandersdesc_filename, 41, 12, 4)
        return commandersdesc


    def load_buildingsdesc(self, buildingsdesc_filename = "TEXT/SZ_FELSZ.TXT"):

        buildingsdesc = open(buildingsdesc_filename, "rb")
        buildingsdesc_encodedtext = buildingsdesc.read(3750)
        buildingsdesc.close()

        bldg_desc_alltext = self.decode_text(buildingsdesc_encodedtext)
        bldg_desc = []
        for bldg_desc_idx in range(25):
            bldg_desc.append([])
            for bldg_desc_line in range(6):
                current_sentence = bldg_desc_alltext[6*bldg_desc_idx + bldg_desc_line].rstrip()
                if current_sentence != '':
                    bldg_desc[bldg_desc_idx].append(current_sentence)

        return bldg_desc


    def process_raw_systemplanetsdata(self, raw_systemplanetsdata):

        systemplanets_imagepos = 0
        systemplanets = {};

        #-9 F7 - nincs bolygo (nem is lehet felfedezni)
        #-4 FC - mental radar kell hozza
        #-3 FD - felfedezheto?
        #-2 FE - felfedezheto?
        #-1 FF - azonnal felfedezve amint belep a systembe
        # 0 felfedezve
        # 1 felfedezve a holdakkal egyutt

        for systemno in range(1,9):
            systemplanets["System%d"%(systemno)] = struct.unpack_from("<bbbbbbbb", raw_systemplanetsdata, systemplanets_imagepos)
            systemplanets_imagepos += 8

        return systemplanets


    def process_raw_buildingslistdata(self, numberofbuildings, raw_buildingslistdata):

        buildingslist_imagepos = 0
        buildingslist = []

        keys1 = [ "type", "system", "planet", "moon", "pos_x", "pos_y", "time_to_finish", "performance", "active", "workers", "energy_use", "working" ]
        # 0x00: tipus (1:controlcetner, 2:atom, 7:building, 10:church -> exe-bol)
        # 0x01: system
        # 0x02: planet
        # 0x03: moon
        # 0x04: x-pos on map (starts with 1) upleft corner
        # 0x05: y-pos on map (starts with 1) upleft corner
        # 0x06: remaining time to build
        # 0x07: real performance (% of reference capacity)
        # 0x08: active
        # 0x09-0xa: workers
        # 0x0b-0x0c: short - energy usage (production?)
        # 0x0d: working %

        # one entry is 14 bytes
        for buildinglist_entry_seqno in range(numberofbuildings):

            unpacklist1 = struct.unpack_from("<BBBBBBBBBHHB", raw_buildingslistdata, buildingslist_imagepos)
            buildingslist_imagepos += 14

            buildingslist_entry = dict(zip(keys1, unpacklist1))

            buildingslist.append(buildingslist_entry)

        return buildingslist


    def process_raw_buildingsinfodata(self, buildingsinfodata):

        buildingsinfo_imagepos = 0
        buildingsinfo = [ {"name" : "dummy"} ]

        keys1 = [ "name", "required_invention_no", "minimum_developer", "building_typegroup?",
                  "requires_builder_plant", "requires_vehicle_plant" ]
        keys2 = [ "workers", "power_consumption", "zero1", "zero2", "production", "price",
                  "power_off_priority", "time_to_build_mean", "building_size_x", "building_size_y" ]

        # "building_typegroup?"
        # 1 - power production
        # 2 - mining
        # 3 - others
        # 4 - radar
        # 6 - food production
        # 7 - living space
        # 8 - cmdcenter
        # 9 - miner station

        # 25 buildings in total - one entry is 63 bytes
        for building_seqno in range(1, 26):

            unpacklist1 = struct.unpack_from("<15pBBBBB", buildingsinfodata, buildingsinfo_imagepos)
            buildingsinfo_imagepos += 20
            building_can_be_built_on_planet_type = buildingsinfodata[buildingsinfo_imagepos:buildingsinfo_imagepos + 11]
            buildingsinfo_imagepos += 11
            unpacklist2 = struct.unpack_from("<HHBBHIBBBB", buildingsinfodata, buildingsinfo_imagepos)
            buildingsinfo_imagepos += 16

            building = dict(zip(keys1+keys2, unpacklist1+unpacklist2))

            # 16 byte
            building_tilecodes = []
            for tile_y_dim in range(4):
                if tile_y_dim < building["building_size_y"]:
                    building_tilecodes.append(list(buildingsinfodata[buildingsinfo_imagepos:buildingsinfo_imagepos + building["building_size_x"]]))
                buildingsinfo_imagepos += 4

            building["tilecodes"] = building_tilecodes
            building["can_be_built_on_planet_type"] = list(building_can_be_built_on_planet_type)

            buildingsinfo.append(building)

    #        print(building["name"], building["unknown1"], building["unknown2"], building["something"])

        return buildingsinfo


    def process_raw_racedata(self, racedata):

        race_imagepos = 0
        races = {}

    #45ebe - race start - name len 14?
    #45fa2 - second race start
    #len 228

    #[0, 1, 20, 1, 7, 1, 0, 0, 0, 1, 0, 0, 0
    # ?, living, ?, mainplanet_system, mainplanet_no_in_system, has_hunter, sfight, destroy, crusier, troop, btank, airc, mlaunch

    #    keys1 = [ "name", "", "" ]
        for raceno in range(11):
    #        unpacklist = struct.unpack_from("<13pBH", racedata, race_imagepos)
            unpacklist = struct.unpack_from("<14p", racedata, race_imagepos)
            race_imagepos += 14

    #        races[raceno] = dict(zip(keys1, unpacklist))

            race_unknown1 = racedata[race_imagepos:race_imagepos + 214]
            race_imagepos += 214

            print("%14s %s"%(unpacklist[0], list(race_unknown1)))


    def process_raw_spacelocaldata(self, spacelocaldata):

        spacelocal_imagepos = 0
        spacelocal_guests = {};

    #0x355 - 0x370
    #len 27

        keys1 = [ "name" ]
        for spaceguest_no in range(10):
            unpacklist = struct.unpack_from("<13p", spacelocaldata, spacelocal_imagepos)
            spacelocal_imagepos += 13

            spacelocal_guests[spaceguest_no] = dict(zip(keys1, unpacklist))

            spacelocal_unknown1 = spacelocaldata[spacelocal_imagepos:spacelocal_imagepos + 14]
            spacelocal_imagepos += 14

            print("%14s %s"%(unpacklist[0], list(spacelocal_unknown1)))


    def load_reunionprg(self, reunionprg_filename = "GRWAR/REUNION.PRG"):

        exepos_planettypenames     = 0x2A4AE  # len + string (es tenyleg csak olyan hosszu) 10 db
        exepos_cannotbuy_reasons   = 0x28DEE  # len + string (es tenyleg csak olyan hosszu) 6+1 db

# TODO
        exepos_commanderhire_okhired = 0x34D0B
        exepos_commanderhire_nomoney = 0x34D6E
        exepos_commanderhire_already = 0x34DE7
        exepos_commanderhire_noskill = 0x34E4D

        exepos_spacelocal_guest    = 0x3F42A  # len: 10 * 27
        exepos_planets_system1     = 0x40D8C  # System 1 planets in reunion.prg
        exepos_systemplanets       = 0x43AC6  # 8*8
        exepos_commander_salaries  = 0x44A8C  # 12 * int (32bit)
# TODO
        exepos_commander_levels    = 0x44ABC  # 4*3*short int (16bit)
        exepos_commander_levelsmax = 0x44AD4  # 4*3*char
        exepos_developer_skills    = 0x44AE0  # 3*4*char
        exepos_developer_skillsmax = 0x44AEC  # 3*4*char
# TODO eddig
        # 0x44AF8 .. 0x44B33 unknown
        exepos_commandernames      = 0x44B34  # len + string (mind 18 char) (pilot, builder, fighter, developer) 18*12
        exepos_shipnames_ground    = 0x44CE4  # 4
        exepos_vehiclenames_ground = 0x44D0C  # 4
        exepos_mineralnames        = 0x44D6C  # len + string (de amugy mind 8 char) - 6*8
        exepos_racenames           = 0x44DA2  # len + string (de amugy mind 9 char) - 12*9
        exepos_skillnames          = 0x44E3E  # len + string (fix 7 char) - 7*4
        exepos_systemnames         = 0x44E5E  # 8*8
        exepos_systemshortnames    = 0x44EA6  # 8*6
        exepos_charset             = 0x44EDE  # 78
        exepos_inventions          = 0x4509C
        exepos_buildings_info      = 0x45882  # 25*
        exepos_races               = 0x45EBE

        reunionexe = open(reunionprg_filename, "rb")
        reunionexe_image = reunionexe.read(288992)
        reunionexe.close()

        buildings_info = self.process_raw_buildingsinfodata(reunionexe_image[exepos_buildings_info:exepos_buildings_info + 25*63])
        planettype_names_from_exe = self.extract_dynamic_strings(reunionexe_image, exepos_planettypenames, 10)
        planettype_names = [ "" ] + planettype_names_from_exe + [ "Artificial" ]
        commander_salaries = struct.unpack_from("<"+"I"*12, reunionexe_image, exepos_commander_salaries)
        commander_salaries_processed = [ commander_salaries[0:3], commander_salaries[3:6], commander_salaries[6:9], commander_salaries[9:12] ]
        commander_names   = list(map(lambda x:x.decode("ascii"), struct.unpack_from("19p"*12, reunionexe_image, exepos_commandernames)))
        commander_names_processed = [ commander_names[0:3], commander_names[3:6], commander_names[6:9], commander_names[9:12] ]
        commander_hire_txt = {
                'ok': self.extract_dynamic_strings(reunionexe_image, exepos_commanderhire_okhired, 1)[0],
                'nomoney': self.extract_dynamic_strings(reunionexe_image, exepos_commanderhire_nomoney, 1)[0],
                'already': self.extract_dynamic_strings(reunionexe_image, exepos_commanderhire_already, 1)[0],
                'noskill': self.extract_dynamic_strings(reunionexe_image, exepos_commanderhire_noskill, 1)[0]
            }
        mineral_names     = list(map(lambda x:x.decode("ascii"), struct.unpack_from( "9p"*6,  reunionexe_image, exepos_mineralnames)))
        race_names        = list(map(lambda x:x.decode("ascii"), struct.unpack_from("10p"*12, reunionexe_image, exepos_racenames)))
        skill_names       = list(map(lambda x:x.decode("ascii"), struct.unpack_from( "8p"*4,  reunionexe_image, exepos_skillnames)))
        system_names      = list(map(lambda x:x.decode("ascii"), struct.unpack_from( "9p"*8,  reunionexe_image, exepos_systemnames)))
        system_shortnames = list(map(lambda x:x.decode("ascii"), struct.unpack_from( "7p"*8,  reunionexe_image, exepos_systemshortnames)))

#        print(skill_names)
#        exit(1)

        #self.process_raw_racedata(reunionexe_image[exepos_races:exepos_races+228*11])

        gamedata_static = {
                "buildings_info": buildings_info,
                "planettype_names": planettype_names,
                "commander_salaries": commander_salaries_processed,
                "commander_names": commander_names_processed,
                "commander_hire_txt": commander_hire_txt,
                "mineral_names": mineral_names,
                "race_names": race_names,
                "skill_names": skill_names,
                "system_names": system_names,
                "system_shortnames": system_shortnames
            }

        gamedata_dynamic = {}

        return [ gamedata_static, gamedata_dynamic ]


    def load_savegame(self, savegame_filename, develmode = False):

        #0xa283-84 az idovel csokken (oraneknt)
        savegamepos_savename              = 0x0000
        savegamepos_savename_len          = 20

        savegamepos_pilots_levels         = 0x0014  # 3x short
        savegamepos_builders_levels       = 0x001A  # 3x short
        savegamepos_developers_levels     = 0x0020  # 3x short
        savegamepos_fighters_levels       = 0x0026  # 3x short
        savegamepos_developers_skills     = 0x002C  # 3x4x char
#        savegamepos_messages_hdr          = 0x0038  # 0x63 'c' 0x00 color (0x63 piros, 0x02 sarga)
        savegamepos_messages              = 0x003A
        savegamepos_message_count         = 0x0353
        savegamepos_message_len           = 53
        savegamepos_spacelocal_guests     = 0x0355
        savegamepos_spacelocal_guests_len = 27 * 10
        # 0x463 ... 0x56A unknown
        savegamepos_planets_in_system_count = [ 0, 32, 12, 18, 7, 13, 23, 5, 32 ]  # planets+moons # = 142
        savegamepos_planets_in_system = [0]*9
        savegamepos_planets_in_system[1] = 0x056B  # 32 - (13 + 65) * num of planets
        savegamepos_planets_in_system[2] = 0x0F2B  # 12
        savegamepos_planets_in_system[3] = 0x12D3  # 18
        savegamepos_planets_in_system[4] = 0x184F  #  7
        savegamepos_planets_in_system[5] = 0x1A71  # 13
        savegamepos_planets_in_system[6] = 0x1E67  # 23
        savegamepos_planets_in_system[7] = 0x2569  #  5
        savegamepos_planets_in_system[8] = 0x26EF  # 32 - ends at 0x3093
        savegamepos_planets_in_one_system_len = 13 + 65
        #[ 7, 5, 5, 3, 3, 7, 2, 8 ] justplanets # = 40

        # 0x3094 ... 0x30AE unknown
        # 0x30A4 a spidy12-ben 115, a tobbi mindenhol nulla

        savegamepos_systemplanets     = 0x30AF  # 8*8
        savegamepos_systemplanets_len = 64
        savegamepos_systemsavailable  = 0x30EF  # 8 byte - (1 planets known, 0 planet unknown, -1 system not available)

        # 0x30F7 ... 0x312A unknown
        savegamepos_herotype        = 0x312B   # short
        # 0x312D ... 0x312E unknown
        savegamepos_inventions      = 0x312F
        savegamepos_inventions_len  = 53 * 35  # 35 inventions

        # 0x386E ... 0x3871 unknown  (all zeroes)

        savegamepos_commander_level = 0x3872  # 4x short (pbfd)
#        savegamepos_pilot_level     = 0x3872  # short
#        savegamepos_builder_level   = 0x3874  # short
#        savegamepos_fighter_level   = 0x3876  # short
#        savegamepos_developer_level = 0x3878  # short
        savegamepos_developer_skills = 0x387A  # 4*short math/phys/elect/AI
        savegamepos_commanders      = 0x3884  # 1-1-1-1 short / pilot builder fighter developer
        savegamepos_money           = 0x388C  # (int 4bytes)
        savegamepos_minerals_main   = 0x3890  # (6*int 6*4bytes)
        savegamepos_date            = 0x38A8  # (4*short 4*2bytes)

        # 0x38B0 ... 0x3951 unknown

        savegamepos_buildings_count = 0x3952  # short
        savegamepos_buildings_list  = 0x3954  # 14 * max_no_of_buildings

        # .. 0x7003 ?

        savegamepos_races           = 0x7004
        savegamepos_races_len       = 228 * 11  # 11 races

        savegamepos_groups_numofgroups          = 0x79D0  # 3*short (in current view, space groups view, planet forces view)
        savegamepos_groups_selectedgroupno      = 0x79D6  # 3*short (in current view, space groups view, planet forces view)
        savegamepos_groups_currentview          = 0x79DC  # short (0 - space groups, 1 - planet forces)
        savegamepos_groups_spacegroups          = 0x79DE
        savegamepos_groups_spacegroups_len      = 161 * 32  # * (maxgroups = 32)
        savegamepos_groups_planetforces         = 0x8DFE
        savegamepos_groups_planetforces_len     = 161 * 32  # * (maxgroups = 32)
        # 0xA21E .. 0xA2C6

        savegame_filehndl = open(savegame_filename, "rb")
        savegame_fileimage = savegame_filehndl.read(41670)
        savegame_filehndl.close()

        savegame = {}

        #self.process_raw_spacelocaldata(savegame_fileimage[savegamepos_spacelocal_guests:savegamepos_spacelocal_guests + savegamepos_spacelocal_guests_len])
        #self.process_raw_racedata(savegame_fileimage[savegamepos_races:savegamepos_races+savegamepos_races_len])

        savegame["name"]              = struct.unpack_from("20p", savegame_fileimage, savegamepos_savename)[0].decode("ascii")
        savegame["commanders_levels"] = [ struct.unpack_from("<HHH", savegame_fileimage, savegamepos_pilots_levels),
                                          struct.unpack_from("<HHH", savegame_fileimage, savegamepos_builders_levels),
                                          struct.unpack_from("<HHH", savegame_fileimage, savegamepos_fighters_levels),
                                          struct.unpack_from("<HHH", savegame_fileimage, savegamepos_developers_levels) ]
        savegame["developers_skills"] = [ struct.unpack_from("BBBB", savegame_fileimage, savegamepos_developers_skills),
                                          struct.unpack_from("BBBB", savegame_fileimage, savegamepos_developers_skills + 4),
                                          struct.unpack_from("BBBB", savegame_fileimage, savegamepos_developers_skills + 8) ]
        savegame["message_count"]     = struct.unpack_from("<H", savegame_fileimage, savegamepos_message_count)[0]
        savegame["messages"]          = list(map(lambda x:x.decode("ascii"), struct.unpack_from("53p" * savegame["message_count"], savegame_fileimage, savegamepos_messages)))
        savegame["date"]              = list(struct.unpack_from("<HHHH", savegame_fileimage, savegamepos_date))
        savegame["money"]             = struct.unpack_from("<I", savegame_fileimage, savegamepos_money)[0]
        savegame["commander_level"]   = list(struct.unpack_from("<HHHH", savegame_fileimage, savegamepos_commander_level))  # pbfd
        savegame["developer_skills"]  = list(struct.unpack_from("<HHHH", savegame_fileimage, savegamepos_developer_skills))
        savegame["commanders"]        = list(struct.unpack_from("<HHHH", savegame_fileimage, savegamepos_commanders))
        savegame["minerals_main"]     = dict(zip(self.gamedata_static["mineral_names"], struct.unpack_from("<IIIIII", savegame_fileimage, savegamepos_minerals_main)))
        savegame["inventions"]        = self.process_raw_inventionsdata(savegame_fileimage[savegamepos_inventions:savegamepos_inventions + savegamepos_inventions_len])
        savegame["herotype"]          = struct.unpack_from("<H", savegame_fileimage, savegamepos_herotype)[0]
        savegame["systems_available"] = struct.unpack_from("bbbbbbbb", savegame_fileimage, savegamepos_systemsavailable)

        savegame["systems"] = [ 0 ]  # 0 dummy
        for systemno in range(1,9):
            raw_systemdata = savegame_fileimage[savegamepos_planets_in_system[systemno]:savegamepos_planets_in_system[systemno] + savegamepos_planets_in_system_count[systemno] * savegamepos_planets_in_one_system_len]
            savegame["systems"].append(self.process_raw_planetsdata(raw_systemdata, savegamepos_planets_in_system_count[systemno]))

        savegame["groups_numofgroups"]     = struct.unpack_from("<HHH", savegame_fileimage, savegamepos_groups_numofgroups)
        savegame["groups_selectedgroupno"] = struct.unpack_from("<HHH", savegame_fileimage, savegamepos_groups_selectedgroupno)
        savegame["groups_currentview"]     = struct.unpack_from("<H", savegame_fileimage, savegamepos_groups_currentview)[0]
        if savegame["groups_numofgroups"][1] > 0:
            savegame["groups_spacegroups"]     = self.process_raw_groupdata(savegame_fileimage[savegamepos_groups_spacegroups:savegamepos_groups_spacegroups + savegamepos_groups_spacegroups_len], savegame["groups_numofgroups"][1])
        if savegame["groups_numofgroups"][2] > 0:
            savegame["groups_planetforces"]    = self.process_raw_groupdata(savegame_fileimage[savegamepos_groups_planetforces:savegamepos_groups_planetforces + savegamepos_groups_planetforces_len], savegame["groups_numofgroups"][2])

        savegame["numberofbuildings"] = struct.unpack_from("<H", savegame_fileimage, savegamepos_buildings_count)[0]
        savegame["buildings_list"] = self.process_raw_buildingslistdata(savegame["numberofbuildings"], savegame_fileimage[savegamepos_buildings_list:savegamepos_buildings_list + savegame["numberofbuildings"]*14])

        if develmode:

        #print(savegame["systems_available"])

        #for msg in savegame["messages"]:
        #    print(msg)

        # 0x0014 .. 0x0039 unknown
        # storyline allapotok esetleg?
            print(list(savegame_fileimage[0x0014:0x0039+1]))

        # 0x463 ... 0x56A unknown
            print(list(savegame_fileimage[0x0463:0x056A+1]))

        # 0x3094 ... 0x30AE unknown
            print(list(savegame_fileimage[0x3094:0x30ae+1]))
        #print(struct.unpack("<HHHHHHH", savegame_fileimage[0x3094:0x30ae+1]))
        #print("systems talan: ", list(savegame_fileimage[savegamepos_systemsavailable:savegamepos_systemsavailable+8]))

        ## 0x30F8 ... 0x312E
            print(list(savegame_fileimage[0x30F8:0x312e+1]))
        #print(struct.unpack("<HHHHHHH", savegame_fileimage[0x30f8:0x312e+1]))

        # 0x38B0 ... 0x3951 unknown
            print(list(savegame_fileimage[0x38B0:0x3951+1]))

        # 0xA21E .. 0xA2C6
            print(list(savegame_fileimage[0xA21E:0xA2C6+1]))

        #print(self.process_raw_systemplanetsdata(savegame_fileimage[savegamepos_systemplanets:savegamepos_systemplanets+savegamepos_systemplanets_len]))

        return [ savegame ]


    def __setup_solarsystems(self, loc_gamedata_static, loc_gamedata_dynamic):

        # process solar system data
        self.solarsystems = [ 0 ]
        for systemno in range(1,4):
            if self.config["verbose"] > 1:
                print("System no", systemno)
            self.solarsystems.append(solarsystem(systemno,
                                            "System %d"%(systemno),
                                            loc_gamedata_dynamic["systems"][systemno],
                                            self.gamedata_const["planets_id_mapping"][systemno],
                                            loc_gamedata_static,
                                            self.cache))

    # setup existing buildings on planets
    def __setup_buildings_on_planets(self, loc_gamedata_dynamic):

        for building_no in range(loc_gamedata_dynamic["numberofbuildings"]):

            solsys_id = loc_gamedata_dynamic["buildings_list"][building_no]["system"]
            planet_id = ( solsys_id,
                          loc_gamedata_dynamic["buildings_list"][building_no]["planet"],
                          loc_gamedata_dynamic["buildings_list"][building_no]["moon"] )
            building_type = loc_gamedata_dynamic["buildings_list"][building_no]["type"]
            pos = ( loc_gamedata_dynamic["buildings_list"][building_no]["pos_x"],
                    loc_gamedata_dynamic["buildings_list"][building_no]["pos_y"] )

            time_to_finish = loc_gamedata_dynamic["buildings_list"][building_no]["time_to_finish"]
            performance = loc_gamedata_dynamic["buildings_list"][building_no]["performance"]
            active = loc_gamedata_dynamic["buildings_list"][building_no]["active"]
            workers = loc_gamedata_dynamic["buildings_list"][building_no]["workers"]
            energy_use = loc_gamedata_dynamic["buildings_list"][building_no]["energy_use"]
            working = loc_gamedata_dynamic["buildings_list"][building_no]["working"]

            self.solarsystems[solsys_id].planets[planet_id].build_new_building(
                                building_type,
                                pos,
                                force_build = True,
                                time_to_finish = time_to_finish,
                                performance = performance,
                                active = active,
                                workers = workers,
                                energy_use = energy_use,
                                working = working )


    def __setup_shipgroups(self, loc_gamedata_dynamic):

        self.shipgroups_spaceforces = [ [] ]
        self.shipgroups_planetforces = [ [] ]

        for group_no in range(loc_gamedata_dynamic["groups_numofgroups"][1]):  # space groups
            shipgroup_toadd = shipgroup("", 0, loc_gamedata_dynamic["groups_spacegroups"][group_no])
            self.shipgroups_spaceforces.append(shipgroup_toadd)

        for group_no in range(loc_gamedata_dynamic["groups_numofgroups"][2]):  # planet forces
            shipgroup_toadd = shipgroup("", 0, loc_gamedata_dynamic["groups_planetforces"][group_no])
            self.shipgroups_planetforces.append(shipgroup_toadd)


    def __init__(self, config, savegame_filename = "SAVE/SPIDYSAV.1"):

        self.config = config
        self.cache = {}
        self.date_iterations = 0

        # load static data (buildings_info) from reunion binary
        [ self.gamedata_static, self.gamedata_dynamic ] = self.load_reunionprg()
        # load dynamic data initial values (money, date, buildings_data, etc.) from savegame
        [ self.gamedata_dynamic ] = self.load_savegame(savegame_filename)  # needs self.gamedata_static !

        self.gamedata_static["inventions_desc"] = self.load_inventionsdesc()
        self.gamedata_static["buildings_desc"] = self.load_buildingsdesc()
        self.gamedata_static["commanders_desc"] = self.load_commandersdesc()

        self.__setup_solarsystems(self.gamedata_static, self.gamedata_dynamic)
        self.__setup_buildings_on_planets(self.gamedata_dynamic)

        self.__setup_shipgroups(self.gamedata_dynamic)

        #for planetno in self.gamedata_dynamic["systems"][systemno].keys():
        #    print(planetno, self.gamedata_dynamic["systems"][systemno][planetno]["planetname"], self.gamedata_const["planets_id_mapping"][systemno][planetno] )

        self.screens = {}
        self.screens["controlroom"] = screen_controlroom(self.gamedata_static, self.gamedata_dynamic)
        self.screens["infobuy"] = screen_infobuy(self.gamedata_static, self.gamedata_dynamic)
        self.screens["researchdesign"] = screen_researchdesign(self.gamedata_static, self.gamedata_dynamic)
        self.screens["ship"] = screen_ship(self.gamedata_static, self.gamedata_dynamic, self.solarsystems, self.shipgroups_spaceforces, self.shipgroups_planetforces)
        self.screens["starmap"] = screen_starmap(self.gamedata_static, self.gamedata_dynamic, self.solarsystems)
        self.screens["messages"] = screen_messages(self.gamedata_dynamic)
        self.screens["spacelocal"] = screen_spacelocal(self.gamedata_dynamic)
        self.screens["commanders"] = screen_commanders(self.gamedata_static, self.gamedata_dynamic)

        self.current_screen = self.screens["controlroom"]


    def update(self, mouse_pos, mouse_buttonstate, mouseevent, mouseevent_buttondown, mouseevent_buttonup):

        [ screen_action, screen_action_params ] = self.current_screen.get_action()
        screen_changed = False
        if   screen_action == "BACK TO M.SCREEN":
            self.screens["controlroom"] = screen_controlroom(self.gamedata_static, self.gamedata_dynamic)
            self.current_screen = self.screens["controlroom"]
            screen_changed = True
        elif screen_action == "PLANET MAIN":
            selected_planet = self.solarsystems[screen_action_params[0][0]].planets[screen_action_params[0]]
            selected_planet_map_position = screen_action_params[1]
            self.screens["planetmain"] = screen_planetmain(self.gamedata_dynamic, selected_planet, map_position = selected_planet_map_position)
            self.current_screen = self.screens["planetmain"]
            screen_changed = True
        elif screen_action == "MINE":
            selected_planet = screen_action_params[0]
            selected_planet_map_position_preserve = screen_action_params[1]
            self.screens["mine"] = screen_mine(self.gamedata_dynamic, selected_planet, selected_planet_map_position_preserve)
            self.current_screen = self.screens["mine"]
            screen_changed = True
        elif screen_action == "RESEARCH-DESIGN":
            self.current_screen = self.screens["researchdesign"]
            screen_changed = True
        elif screen_action == "INFO-BUY":
            self.current_screen = self.screens["infobuy"]
            screen_changed = True
        elif screen_action in [ "SHIP INFO", "SPACEPORT" ]:
            self.current_screen = self.screens["ship"]
            screen_changed = True
        elif screen_action == "GALACTIC MAP":
            self.current_screen = self.screens["starmap"]
            screen_changed = True
        elif screen_action == "ZOOM OUT":
            self.screens["starmap"].zoomout()
            screen_changed = True
        elif screen_action == "MESSAGES":
            self.current_screen = self.screens["messages"]
            screen_changed = True
        elif screen_action == "SPACE LOCAL":
            self.current_screen = self.screens["spacelocal"]
            screen_changed = True
        elif screen_action == "COMMANDERS":
            self.screens["commanders"] = screen_commanders(self.gamedata_static, self.gamedata_dynamic)
            self.current_screen = self.screens["commanders"]
            screen_changed = True

        if screen_changed:
            self.current_screen.update(self.gamedata_dynamic, mouse_pos, (False, False, False), [False, False])

        if mouseevent or any(mouse_buttonstate):
            self.current_screen.update(self.gamedata_dynamic, mouse_pos, mouse_buttonstate, [ mouseevent_buttondown, mouseevent_buttonup ])

        [ a_hour_has_passed, a_day_has_passed ] = self.update_date()

        if a_hour_has_passed:
            pass
            # todo, call updates for research, planet (build/mine), etc.

        if a_day_has_passed:

            # planet related
            total_daily_tax = 0
            for solsys_id in range(1,len(self.solarsystems)):
                for planet_id in self.solarsystems[solsys_id].planets.keys():
                    # gather tax
                    total_daily_tax += self.solarsystems[solsys_id].planets[planet_id].gather_tax()
                    self.solarsystems[solsys_id].planets[planet_id].update_daily()

            self.gamedata_dynamic["money"] += total_daily_tax

            # todo, call other updates


    def update_date(self):

        self.date_iterations += 1
        increase_date = False
        day_passed = False

        if self.current_screen.infobar_timespinning:
            if self.current_screen.infobar_timespinning_type == 1:
                if self.date_iterations >= 4:
                    increase_date = True
            elif self.current_screen.infobar_timespinning_type == 2:
                if self.date_iterations >= 1:
                    increase_date = True
        else:
            if self.date_iterations >= 40:
                increase_date = True

        if increase_date:
            self.date_iterations = 0
            # the original game uses 30 days in every month, so let's just follow that
            self.gamedata_dynamic["date"][3] += 1
            if self.gamedata_dynamic["date"][3] > 24:
                day_passed = True
                self.gamedata_dynamic["date"][3] = 1
                self.gamedata_dynamic["date"][2] += 1
            if self.gamedata_dynamic["date"][2] > 30:
                self.gamedata_dynamic["date"][2] = 1
                self.gamedata_dynamic["date"][1] += 1
            if self.gamedata_dynamic["date"][1] > 12:
                self.gamedata_dynamic["date"][1] = 1
                self.gamedata_dynamic["date"][0] += 1

        return [ increase_date, day_passed ]


    def update_anims(self):
        self.current_screen.update_anims()


    def get_sfx(self):
        return self.current_screen.get_sfx()

