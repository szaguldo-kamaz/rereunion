# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import pygame
import struct


class ReReGFX:

    ICONALL_names = [ "blank", "DISK OPERATIONS", "RESEARCH-DESIGN", "TRANSFER", "MESSAGES",
                  "COLONIZATION?", "GAME CREDITS", "U_TRADE", "U_RESOURCE-MINE", "PLANET INFO",
                  "ADD MINER STATION", "DECREASE TAX", "?ADD TROOPER", "SHIP INFO", "COMMANDERS",
                  "NEW GROUP", "CONTROL PANEL", "U_TALK TO MAN", "BUY ITEM", "ADD TANK UNIT",
                  "ADD SATELLITE", "PROJECT DOWN", "PROJECT UP", "INFO-BUY", "BACK TO M.SCREEN",
                  "ADD DROIDS", "ADD ONE", "MINUS ONE", "ADD TEN", "MINUS TEN",
                  "OK,BUY", "SELECT", "CANCEL BUY", "ZOOM OUT", "GALACTIC MAP",
                  "INCREASE TAX", "HIRE MAN", "PLANET MAIN", "ADD MISSILE UNIT", "SPACE LOCAL",
                  "SAVE", "LOAD", "GROUP", "PILOTS", "BUILDERS",
                  "FIGHTERS", "DEVELOPERS", "U_END TALK", "DISBAND UNIT", "ADD AIRCRAFT UNIT",
                  "OK, ATTACK", "MOVE UNIT", "ABORT", "OK.CREATE IT", "FIGHT?",
                  "COLINFO?", "YOUR PLANETS", "VICTORY?", "PLANET FORCES", "ADD SPY SAT",
                  "ADD SPY SHIP", "ADD SOLAR SAT", "GROUND WAR", "USEFUL PLANETS", "DEATH PLANET?",
                  "RETREAT", "EXIT TO DOS", "ALIEN PLANETS" ]


    def __init__(self, config, game_obj):

        self.config = config
        self.gamedata_static = game_obj.gamedata_static

        self.major_vs_felszin = [ 0, 1, 8, 2, 7, 10, 3, 9, 5, 4, 6, 11 ]
        # maptype_majorX - felszinX
        # 1 earth - 1 earth - ANIM
        # 2 - 8 gas
        # 3 - 2 icy
        # 4 - 7 szigetek
        # 5 - 10 tropic - ANIM
        # 6 - 3 desert
        # 7 - 9 oily
        # 8 - 5 rocky - ANIM
        # 9? - 4 vulkan
        # 10? - 6 devil
        #  - 11 rigel

        self.cache_rendered_surfaces = {}

        self.window_size = (320 * self.config["gfx_scalefactor"], 200 * self.config["gfx_scalefactor"])

        # load all of the PICs
        self.PICs = self.load_allPICs()
        # load ICON.ALL
        self.ICONALL = self.loadICONALL()

        self.prepare_charsets()
        self.prepare_icons()
        self.prepare_mousepointers()
        self.prepare_heroes_and_commanders()
        self.prepare_felszin()
        self.prepare_planetmain()

        self.menu_full = pygame.Surface((320, 64))
        self.infobar = pygame.Surface((320, 17))
        self.surface_building = pygame.Surface((77, 64))

        self.screen_controlroom = pygame.Surface((320, 200))
        self.screen_buffer = pygame.Surface((320, 200))

        self.window = pygame.display.set_mode(self.window_size)
        #self.window = pygame.display.set_mode((320, 200), flags = pygame.SCALED | pygame.RESIZABLE)

        self.set_mousecursor("normal")


    def set_mousecursor(self, towhat):

        pygame.mouse.set_cursor(self.mousecursors[towhat])


    def draw(self, current_game):

        current_screen_gfx = self.render_screen(current_game.current_screen)
        output_screen = pygame.transform.scale(current_screen_gfx, self.window_size)
        self.window.blit(output_screen, (0, 0))


    def decode_rawPCX(self, PCXdata_compressed_raw, imagesize, palette, PCXdata_pointer_compressed_raw = 12):

        PCXdata_pointer_uncompressed_RGB = 0
        PCXdata_uncompressed_RGB = bytearray(imagesize)

        while PCXdata_pointer_uncompressed_RGB < imagesize:

            if PCXdata_compressed_raw[PCXdata_pointer_compressed_raw] < 0xC0:

                palette_pos = PCXdata_compressed_raw[PCXdata_pointer_compressed_raw] * 3
    #            PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB:PCXdata_pointer_uncompressed_RGB+3] = palette[ palette_pos: palette_pos+3 ]
    #            PCXdata_pointer_uncompressed_RGB += 3
    # this is faster... :
                PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos ]
                PCXdata_pointer_uncompressed_RGB += 1
                PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 1 ]
                PCXdata_pointer_uncompressed_RGB += 1
                PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 2 ]
                PCXdata_pointer_uncompressed_RGB += 1

            else:

                repeat = PCXdata_compressed_raw[PCXdata_pointer_compressed_raw] - 0xC0
                PCXdata_pointer_compressed_raw += 1
                palette_pos = PCXdata_compressed_raw[PCXdata_pointer_compressed_raw] * 3
                for minoroffset in range(repeat):
    #                PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB:PCXdata_pointer_uncompressed_RGB+3] = palette[ palette_pos: palette_pos+3 ];
    #                PCXdata_pointer_uncompressed_RGB += 3
    # this is faster... :
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos ];
                    PCXdata_pointer_uncompressed_RGB += 1
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 1 ];
                    PCXdata_pointer_uncompressed_RGB += 1
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 2 ];
                    PCXdata_pointer_uncompressed_RGB += 1

            PCXdata_pointer_compressed_raw += 1

        return bytes(PCXdata_uncompressed_RGB)


    def loadPIC(self, PICfilename):

        # PIC files are actually PCX files with headers stripped

        PICfile = open(PICfilename, 'rb')
        PICdata_compressed_raw = PICfile.read()
        PICfile.close()

        if PICdata_compressed_raw[0:8] != b'SpidyGfx':
            print('Error in PIC file (no magic id string): ', PICfilename)
            return [ None, [ 0, 0 ] ]

        [ width, height ] = struct.unpack("<HH", PICdata_compressed_raw[8:12]);
        PICimagesize = width * height * 3;

        if PICdata_compressed_raw[-769] != 0x0C:
            print('Error in PIC file (no palette magic): ', PICfilename)
            return [ None, [ 0, 0 ] ]

        palette = PICdata_compressed_raw[-768:]

        PICdata_uncompressed_RGB = self.decode_rawPCX(PICdata_compressed_raw, PICimagesize, palette)

        return [ PICdata_uncompressed_RGB, [ width, height ] ]


    # load 68 icons from ICON.ALL
    def loadICONALL(self):

        palette_icons = open('ICON/ICONMAIN.PIC', 'rb').read()[-768:]

        ICONALLfile = open('ICON/ICON.ALL', 'rb')
        ICONALLdata = ICONALLfile.read()
        ICONALLfile.close()

        ICONALL = []
        PICimagesize = 40 * 24 * 3
        ICONALLdata_pointer = 0

        while ICONALLdata_pointer < len(ICONALLdata):

            compressed_raw_length = struct.unpack("<H", ICONALLdata[ICONALLdata_pointer:ICONALLdata_pointer+2])[0]
            ICONALLdata_pointer += 2
            PICdata_compressed_raw = ICONALLdata[ICONALLdata_pointer:ICONALLdata_pointer+compressed_raw_length]
            ICONALLdata_pointer += compressed_raw_length
            PICdata_uncompressed_RGB = self.decode_rawPCX(PICdata_compressed_raw, PICimagesize, palette_icons, PCXdata_pointer_compressed_raw = 0)
            ICONALL.append(PICdata_uncompressed_RGB)

        return ICONALL


    def load_allPICs(self):

        PIClist = [ ]

        PIClist.append("PLANETS/PLANET0.PIC")  # Planet info pic (extra 0 - unexplored planet)
        for planet_no in range(1,12):
        #    PIClist.append("PLANETS/PLANET%d.PIC"%(planet_no))  # Planet info pic
            PIClist.append("PLANETS/FELSZ%d.PIC"%(planet_no))  # Felszinek listaja - MAP elements (element size is 32x32)
            PIClist.append("PLANETS/EPUL%d.PIC"%(planet_no))  # Epuletek a felszinen - Buildings on the surface
        #    PIClist.append("PLANETS/EPULT%d.PIC"%(planet_no))  # Idegen bazis a felszinen - Alien base on the surface
        #    PIClist.append("PLANETS/RADAR%d.PIC"%(planet_no))  # Felszin a radaron - Surface on radar

        for epulet_no in range(1,27):
            PIClist.append("EPULET/EPULET%d.PIC"%(epulet_no))  # Epulet illusztraciok listaja - Building illustrations

        PIClist.append("PLANETS/FANIM1.PIC")  # Felszin animacio - Surface anim (earth-like)
        PIClist.append("PLANETS/FANIM5.PIC")  # Felszin animacio - Surface anim (rocky)
        PIClist.append("PLANETS/FANIM10.PIC")  # Felszin animacio - Surface anim (tropical)

        PIClist.append("GRAFIKA/CHARSET1.PIC")  # Karakterkeszlet - Charset

        PIClist.append("GRAFIKA/DESIGNER.PIC")  # Bolygo felszin nezet - Planet main

        PIClist.append("ICON/ICONMAIN.PIC")  # Ikonok keretei es egermutatok - Icon frames and mouse pointers

        PIClist.append("GRAFIKA/MAIN.PIC")  # Fokepernyo - Main screen
        PIClist.append("GRAFIKA/TEXT.PIC")  # Fokepernyo - gomb funkcioja, penz, datum - Main screen button function, money, date
        PIClist.append("GRAFIKA/HEROES.PIC")  # Heroes
        PIClist.append("GRAFIKA/MAINFACE.PIC")  # Commanders

        # Fajok
        for faj_no in range(14):
            PIClist.append("PLANETS/FAJ%d.PIC"%(faj_no))  # Fajok - Species

        # Nagy
        #for nagy_no in range(13):
        #    PIClist.append("PLANETS/NAGY%d.PIC"%(nagy_no))  #.

        # Hatter - Background
        #for hatter_no in range(1,5):
        #    PIClist.append("PLANETS/HATTER%d.PIC"%(hatter_no))  # Naprendszerek hatter, hatter 1-8 kerettel, kisikonok, nagyikonok

        # Naprendszer - Solar System
        #for napr_no in range(1,9):
        #    PIClist.append("PLANETS/NAPR%d.PIC"%(napr_no))  # Nap, bolygok, holdak
        #PIClist.append("PLANETS/MUSZI.PIC")  # Urhajo Muszerfal
        #PIClist.append("PLANETS/MUSZIANM.PIC")  # Urhajo Muszerfal animacio
        #PIClist.append("PLANETS/MASZK1.PIC")  #.
        #PIClist.append("PLANETS/MASZK2.PIC")  #.

        PICs = {}

        for PICname in PIClist:
            [ PICdata, PICsize ] = self.loadPIC(PICname)
            PICs[PICname[:-4].split("/")[1]] = pygame.image.frombytes(PICdata, PICsize, 'RGB')

        return PICs


    ######################
    ### Prepare GFX ###
    ################

    def prepare_charsets(self):

        self.charset = [ {}, {}, {} ]  # blue, yellow, red
        char_xpos = 0
        char_ypos = 0
        yellow_charset_full = pygame.surfarray.array2d(self.PICs["CHARSET1"])
        red_charset_full = pygame.surfarray.array2d(self.PICs["CHARSET1"])
        for pixel_x in range(len(yellow_charset_full)):
            for pixel_y in range(len(yellow_charset_full[0])):
                if  yellow_charset_full[pixel_x][pixel_y] == 0x17579f:
                    yellow_charset_full[pixel_x][pixel_y] = 0x827500
                    red_charset_full[pixel_x][pixel_y] = 0xe74518
                elif yellow_charset_full[pixel_x][pixel_y] == 0x3b87df:
                    yellow_charset_full[pixel_x][pixel_y] = 0xb6aa00
                    red_charset_full[pixel_x][pixel_y] = 0xa63410

        yellow_charset_full_surface = pygame.Surface((320, 32))
        red_charset_full_surface = pygame.Surface((320, 32))
        pygame.surfarray.blit_array(yellow_charset_full_surface, yellow_charset_full)
        pygame.surfarray.blit_array(red_charset_full_surface, red_charset_full)

        for currchar in """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz?![]'"+-:;.,1234567890%& /""":
            if char_xpos == 20 * 16:
                char_xpos = 0
                char_ypos += 8
            self.charset[0][currchar] = self.PICs["CHARSET1"].subsurface(pygame.Rect(char_xpos, char_ypos, 5, 7))
            self.charset[1][currchar] = yellow_charset_full_surface.subsurface(pygame.Rect(char_xpos, char_ypos, 5, 7))
            self.charset[2][currchar] = red_charset_full_surface.subsurface(pygame.Rect(char_xpos, char_ypos, 5, 7))
            char_xpos += 16


    def prepare_icons(self):

        self.icons = {
                       "emptyframe": self.PICs["ICONMAIN"].subsurface(pygame.Rect(  0, 0, 48, 32)),
                       "scrollup":   self.PICs["ICONMAIN"].subsurface(pygame.Rect( 48, 0, 32, 32)),
                       "scrolldown": self.PICs["ICONMAIN"].subsurface(pygame.Rect( 80, 0, 32, 32)),
                       "noscroll":   self.PICs["ICONMAIN"].subsurface(pygame.Rect(112, 0, 32, 32))
                     }


        for icon_no in range(len(self.ICONALL)):
            self.icons[self.ICONALL_names[icon_no]] = pygame.image.frombytes(self.ICONALL[icon_no], (40, 24), 'RGB').subsurface(pygame.Rect(  0, 0, 39, 24))


    def prepare_mousepointers(self):

        # slice sprites and scale them as required
        # mouse pointers need to be scaled independently
        hotspot_temp = 5 * self.config["gfx_scalefactor"]
        mousepointerpics = {
                             "normal": { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(144, 1, 10, 10)), (10 * self.config["gfx_scalefactor"], 10 * self.config["gfx_scalefactor"])), "hotspot": (           0,            0) },
                             "left":   { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(160, 1,  6, 11)), ( 6 * self.config["gfx_scalefactor"], 11 * self.config["gfx_scalefactor"])), "hotspot": (           0, hotspot_temp) },
                             "right":  { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(176, 1,  6, 11)), ( 6 * self.config["gfx_scalefactor"], 11 * self.config["gfx_scalefactor"])), "hotspot": (hotspot_temp, hotspot_temp) },
                             "up":     { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(192, 1, 11,  6)), (11 * self.config["gfx_scalefactor"],  6 * self.config["gfx_scalefactor"])), "hotspot": (hotspot_temp,            0) },
                             "down":   { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(208, 1, 11,  6)), (11 * self.config["gfx_scalefactor"],  6 * self.config["gfx_scalefactor"])), "hotspot": (hotspot_temp, hotspot_temp) },
                             "cross":  { "cbmp": pygame.transform.scale(self.PICs["ICONMAIN"].subsurface(pygame.Rect(224, 1, 11, 11)), (11 * self.config["gfx_scalefactor"], 11 * self.config["gfx_scalefactor"])), "hotspot": (hotspot_temp, hotspot_temp) }
                           }

        self.mousecursors = {}
        for mousepointerpic_name in mousepointerpics.keys():
            mousepointerpics[mousepointerpic_name]["cbmp"].set_colorkey(pygame.Color(0, 0, 0))
            self.mousecursors[mousepointerpic_name] = pygame.cursors.Cursor(mousepointerpics[mousepointerpic_name]["hotspot"], mousepointerpics[mousepointerpic_name]["cbmp"])


    def prepare_heroes_and_commanders(self):

        # slice heroes
        self.heroes = [ self.PICs["HEROES"].subsurface(pygame.Rect(  1, 1, 67, 59)),
                        self.PICs["HEROES"].subsurface(pygame.Rect( 69, 1, 67, 59)) ]
        self.heroes[0].set_colorkey(pygame.Color(0, 0, 0xFF))
        self.heroes[1].set_colorkey(pygame.Color(0, 0, 0xFF))

        # slice commanders
        self.commanders = {
               "developers": [
                   0,
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(  1, 1, 49, 95)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect( 51, 1, 49, 95)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(101, 1, 49, 95)) ],

               "pilots": [
                   0,
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(152, 1, 50, 97)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(203, 1, 50, 97)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(254, 1, 50, 97)) ],

               "fighters": [
                   0,
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(  1, 100, 57, 84)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect( 59, 100, 57, 84)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(117, 100, 57, 84)) ],

               "builders": [
                   0,
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(175, 100, 46, 65)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(222, 100, 46, 65)),
                   self.PICs["MAINFACE"].subsurface(pygame.Rect(269, 100, 46, 65)) ]

             }

        for commander_type in self.commanders.keys():
            for commander_no in range(1,4):
                self.commanders[commander_type][commander_no].set_colorkey(pygame.Color(0, 0, 0xFF))


    def prepare_planetmain(self):

        self.planetmain_arrowup   = [ self.PICs["DESIGNER"].subsurface(pygame.Rect( 118, 50, 11, 32)),   # bright
                                      self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 50, 11, 32)) ]  # dark

        self.planetmain_arrowdown = [ self.PICs["DESIGNER"].subsurface(pygame.Rect( 142, 50, 11, 32)),   # bright
                                      self.PICs["DESIGNER"].subsurface(pygame.Rect( 130, 50, 11, 32)) ]  # dark

        self.planetmain_buildicon = [ self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 23, 44, 13)),   # normal
                                      self.PICs["DESIGNER"].subsurface(pygame.Rect( 150, 23, 44, 13)) ]  # red

        self.planetmain_demolishicon = [ self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 36, 44, 13)),   # normal
                                         self.PICs["DESIGNER"].subsurface(pygame.Rect( 150, 36, 44, 13)) ]  # red

        self.planetmain_horiz_lines = [ self.PICs["DESIGNER"].subsurface(pygame.Rect( 106,  5,  90,  2)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 106,  8,  90,  2)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 11, 111,  2)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 14, 111,  2)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 17, 111,  2)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 106, 20, 111,  2)) ]

        self.planetmain_horiz_lines = [ self.PICs["DESIGNER"].subsurface(pygame.Rect(  94,  5,  2, 68)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect(  97,  5,  2, 68)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 100,  5,  2, 65)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 103,  5,  2, 65)) ]


    # slice up felszin/epulet (surface/building) PICs into 16x16 tiles
    def prepare_felszin(self):

        self.felszinek = [[]]  # 0 is unused, just wanted to keep the original index numbers
        felszinek_number_of_elements = [ [0, 0], [20, 4], [20, 6], [20, 12], [20, 10], [20, 12], [20, 12], [20, 6], [20, 2], [20, 6], [20, 8], [20, 12] ]  # hardcoded

        for currfelszin_no in range(1,12):
            currfelszin_name = "FELSZ%d"%(currfelszin_no)
            self.felszinek.append([]);
            for felszin_y in range(0, felszinek_number_of_elements[currfelszin_no][1] * 16, 16):
                for felszin_x in range(0, felszinek_number_of_elements[currfelszin_no][0] * 16, 16):
                    self.felszinek[currfelszin_no].append(self.PICs[currfelszin_name].subsurface(pygame.Rect(felszin_x, felszin_y, 16, 16)))

        self.felszinanimok = [[]]  # 0 is unused, just wanted to keep the original index numbers
        felszinanimok_number_of_elements = [ [0, 0], [20, 12], [0, 0], [0, 0], [0, 0], [20, 3], [0, 0], [0, 0], [0, 0], [0, 0], [20, 12], [0, 0] ]  # hardcoded
        felszinanimok_number_of_animtiles = [ 0, 80, 0, 0, 0, 20, 0, 0, 0, 0, 80, 0 ]  # hardcoded

        for currfelszinanim_no in range(1,12):
            self.felszinanimok.append([[]])
            if currfelszinanim_no in [1, 5, 10]:
                currfelszinanim_name = "FANIM%d"%(currfelszinanim_no)
                tilecounter = 0
                animstate = 0
                for felszin_y in range(felszinanimok_number_of_elements[currfelszinanim_no][1]):
                    for felszin_x in range(felszinanimok_number_of_elements[currfelszinanim_no][0]):
                        if tilecounter == felszinanimok_number_of_animtiles[currfelszinanim_no]:
                            tilecounter = 0
                            animstate += 1
                            self.felszinanimok[currfelszinanim_no].append([])
                        tilecounter += 1
                        self.felszinanimok[currfelszinanim_no][animstate].append(self.PICs[currfelszinanim_name].subsurface(pygame.Rect(felszin_x * 16, felszin_y * 16, 16, 16)))

        self.felszinepuletek = [[]]  # 0 is unused, just wanted to keep the original index numbers
        felszinepuletek_number_of_elements = [ [0, 0], [20, 12], [20, 12], [20, 12], [0, 0], [20, 12], [4, 4], [0, 0], [0, 0], [0, 0], [20, 12], [0, 0] ]  # hardcoded

        for currfelszinepulet_no in range(1,12):
            self.felszinepuletek.append([])
            if currfelszinepulet_no in [1, 2, 3, 5, 10]:
                currfelszinepulet_name = "EPUL%d"%(currfelszinepulet_no)
                for felszinepulet_y in range(0, felszinepuletek_number_of_elements[currfelszinepulet_no][1] * 16, 16):
        #            for felszinepulet_x in range(0, felszinepuletek_number_of_elements[currfelszinepulet_no][0] * 16, 16):
                    for felszinepulet_x in range(0, 20 * 16, 16):
                        self.felszinepuletek[currfelszinepulet_no].append(self.PICs[currfelszinepulet_name].subsurface(pygame.Rect(felszinepulet_x, felszinepulet_y, 16, 16)))
                        if felszinepulet_x == felszinepuletek_number_of_elements[currfelszinepulet_no][0] * 16:  # epul6 has miner station only
                            self.felszinepuletek[currfelszinepulet_no].append([]*16)  # check todo
                            break

    #################
    ### Render ###
    ###########

    def render_text(self, text_to_render, textcolor = 0):
        # textcolor:
        #  0 original blue
        #  1 yellow
        #  2 red
        if type(text_to_render) == bytes:
            text_to_render = text_to_render.decode('ascii')
        textlength = len(text_to_render)
        rendered_text = pygame.Surface((textlength * 6, 8))
        for curr_char_no in range(textlength):
            rendered_text.blit(self.charset[textcolor][text_to_render[curr_char_no]], (curr_char_no * 6, 0))
        return rendered_text


    def render_surface(self, planet, animstate = 0):

        map_id = planet.map_terrain.map_major * 100 + planet.map_terrain.map_minor * 10 + animstate

        if map_id in self.cache_rendered_surfaces.keys():
            return self.cache_rendered_surfaces[map_id]

        map_size = planet.map_terrain.map_size
        map_major = planet.map_terrain.map_major
        map_felszin = self.major_vs_felszin[planet.map_terrain.map_major]
        map_data = planet.map_terrain.map_data

        rendered_map = pygame.Surface((map_size[0] * 16, map_size[1] * 16))

        fanim_changeovertiles = [ 0, 80, 0, 0, 0, 160, 0, 0, 240 ]  # planet types

        # render map - # 1, 5, 8 have animations
        if map_major in [ 1, 5, 8 ]:
            for map_pointer_y in range(map_size[1]):
                for map_pointer_x in range(map_size[0]):
                    if map_data[map_pointer_y * map_size[0] + map_pointer_x] >= fanim_changeovertiles[map_major]:
                        rendered_map.blit( self.felszinanimok[map_felszin][animstate][map_data[map_pointer_y * map_size[0] + map_pointer_x] - fanim_changeovertiles[map_major]], (map_pointer_x * 16, map_pointer_y * 16))
                    else:
                        rendered_map.blit( self.felszinek[map_felszin][map_data[map_pointer_y * map_size[0] + map_pointer_x]], (map_pointer_x * 16, map_pointer_y * 16))
        else:
            for map_pointer_y in range(map_size[1]):
                for map_pointer_x in range(map_size[0]):
                    rendered_map.blit( self.felszinek[map_felszin][map_data[map_pointer_y * map_size[0] + map_pointer_x]], (map_pointer_x * 16, map_pointer_y * 16))

        self.cache_rendered_surfaces[map_id] = rendered_map

        return self.cache_rendered_surfaces[map_id]


    def render_surface_with_buildings(self, planet, animstate = 0):

        map_felszin = self.major_vs_felszin[planet.planettype]

        base_mapsurface = self.render_surface(planet, animstate).copy()

        for curr_building in planet.buildings:
            for tilepos_y in range(curr_building.building_data["building_size_y"]):
                for tilepos_x in range(curr_building.building_data["building_size_x"]):
                    tilecode = curr_building.building_data["tilecodes"][tilepos_y][tilepos_x]
                    base_mapsurface.blit( self.felszinepuletek[map_felszin][tilecode], (curr_building.pixelpos[0] + tilepos_x * 16, curr_building.pixelpos[1] + tilepos_y * 16))

        return base_mapsurface


    def render_building(self, planet, building_data):

        map_felszin = self.major_vs_felszin[planet.planettype]

        building_size = (building_data["building_size_x"], building_data["building_size_y"])
        offset_x = 38 - (building_size[0]*8)
        offset_y = 32 - (building_size[1]*8)

        if planet.planettype == 6:  # desert
            for tilepos_y in range(0,4,2):
                for tilepos_x in range(0,5,2):
                    self.surface_building.blit( self.felszinek[map_felszin][0],  (tilepos_x * 16, tilepos_y * 16) )
                    self.surface_building.blit( self.felszinek[map_felszin][1],  ((tilepos_x + 1) * 16, tilepos_y * 16) )
                    self.surface_building.blit( self.felszinek[map_felszin][20], (tilepos_x * 16, (tilepos_y + 1) * 16) )
                    self.surface_building.blit( self.felszinek[map_felszin][21], ((tilepos_x + 1) * 16, (tilepos_y + 1) * 16) )
        else:
            for tilepos_y in range(0,4):
                for tilepos_x in range(0,5):
                    self.surface_building.blit( self.felszinek[map_felszin][0], (tilepos_x * 16, tilepos_y * 16) )

        for tilepos_y in range(building_size[1]):
            for tilepos_x in range(building_size[0]):
                tilecode = building_data["tilecodes"][tilepos_y][tilepos_x]
                self.surface_building.blit( self.felszinepuletek[map_felszin][tilecode], (offset_x + tilepos_x * 16, offset_y + tilepos_y * 16) )

        return self.surface_building


    def render_menu(self, menu_info):

        for menuicon_x in range(0, 241, 48):
            self.menu_full.blit(self.icons["emptyframe"], (menuicon_x,  0))
            self.menu_full.blit(self.icons["emptyframe"], (menuicon_x, 32))

        if len(menu_info["icons"]) <= 6:
            self.menu_full.blit(self.icons["noscroll"],   (288,  0))
        else:
            self.menu_full.blit(self.icons["scrolldown"], (288,  0))
            self.menu_full.blit(self.icons["scrollup"],   (288, 32))

        menuicon_y = 4
        menuicon_x = 4
        for menuicon in range(len(menu_info["icons"])):
            if menuicon == 6:
                menuicon_y = 36
                menuicon_x = 4
            self.menu_full.blit(self.icons[menu_info["icons"][menuicon]], (menuicon_x, menuicon_y))
            menuicon_x += 48

        # TODO, smooth scrolling, disappear/appear transition anim
        menu_visible = self.menu_full.subsurface(pygame.Rect(0, menu_info["updown"] * 32, 320, 32))

        return menu_visible


    def render_infobar(self, menu_info):

        text_action = self.render_text(menu_info["actiontext"])
        text_money = self.render_text("%d"%(menu_info["money"]))
        text_date = self.render_text("%d-%d-%d-%d"%(menu_info["date"][0], menu_info["date"][1], menu_info["date"][2], menu_info["date"][3]))

        self.infobar.blit(self.PICs["TEXT"], (0, 0))
        self.infobar.blit(text_action, (16, 5))
        self.infobar.blit(text_money, (144, 5))
        self.infobar.blit(text_date, (224, 5))

        return self.infobar


    def render_screen(self, screenobj):
        if   screenobj.screentype == "controlroom":
            return self.render_controlroom(screenobj)
        elif screenobj.screentype == "planetmain":
            return self.render_planetmain(screenobj)


    # current_commanders <- gamedata_dynamic["commanders"]
    def render_controlroom(self, screenobj_controlroom):

        current_commanders = screenobj_controlroom.current_commanders

        self.screen_controlroom.blit(self.render_menu(screenobj_controlroom.menu_info), (0, 0))
        self.screen_controlroom.blit(self.render_infobar(screenobj_controlroom.menu_info), (0, 32))

        # control room background
        self.screen_controlroom.blit(self.PICs["MAIN"], (0, 49))

        # hero
        self.screen_controlroom.blit(self.heroes[1], (131, 50 + 49) )

        # commanders - pilot builder figther developer
        if current_commanders[1] != 0:
            self.screen_controlroom.blit(self.commanders["builders"][current_commanders[1]], (200, 51 + 49) )
        if current_commanders[2] != 0:
            self.screen_controlroom.blit(self.commanders["fighters"][current_commanders[2]], (77, 38 + 49) )
        if current_commanders[3] != 0:
            self.screen_controlroom.blit(self.commanders["developers"][current_commanders[3]], (43, 56 + 49) )
        if current_commanders[0] != 0:
            self.screen_controlroom.blit(self.commanders["pilots"][current_commanders[0]], (245, 54 + 49) )

        # TODO: anim

        return self.screen_controlroom


    # planet main - planet surface
    def render_planetmain(self, screenobj_planetmain):

        self.screen_buffer.blit(self.render_menu(screenobj_planetmain.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_planetmain.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["DESIGNER"], (0, 49))

        # build icon
        buildicon_state = screenobj_planetmain.anim_states["builddemolish"]["state"] and screenobj_planetmain.build_mode
        self.screen_buffer.blit(self.planetmain_buildicon[buildicon_state], (0, 1 + 49))
        # demolish icon
        demolishicon_state = screenobj_planetmain.anim_states["builddemolish"]["state"] and screenobj_planetmain.demolish_mode
        self.screen_buffer.blit(self.planetmain_demolishicon[demolishicon_state], (45, 1 + 49))
        # building - invention up kammide
        self.screen_buffer.blit(self.planetmain_arrowup[screenobj_planetmain.selected_building_is_first], (0, 15 + 49))
        # building - invention down
        self.screen_buffer.blit(self.planetmain_arrowdown[screenobj_planetmain.selected_building_is_last], (0, 48 + 49))
        # building on surface illustration
        self.screen_buffer.blit(self.render_building(screenobj_planetmain.planet, self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]), (12, 15 + 49))
        # building name
        yellow_text_building_name = self.render_text(
                                        self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]["name"].decode('ascii'),
                                        textcolor = 1)
        self.screen_buffer.blit(yellow_text_building_name, (2, 81 + 49))

        # surface map
        planet_surface = self.render_surface_with_buildings(screenobj_planetmain.planet, screenobj_planetmain.anim_states["surface"]["state"])
        planet_surface_cropped = planet_surface.subsurface(pygame.Rect(screenobj_planetmain.map_position[0] * 16,
                                                                       screenobj_planetmain.map_position[1] * 16,
                                                                       14*16, 9*16))
        self.screen_buffer.blit(planet_surface_cropped, (93, 4 + 49))

        # radar yellow frame - kozeppont (45, 168)
        radar_frame_rect_size = (screenobj_planetmain.radar_frame_rect_pos[0][0],
                                 screenobj_planetmain.radar_frame_rect_pos[0][1],
                                 screenobj_planetmain.radar_frame_rect_size[0],
                                 screenobj_planetmain.radar_frame_rect_size[1])
        pygame.draw.rect(self.screen_buffer, (0xe3, 0xc3, 0x00), radar_frame_rect_size, 1)

        # radar red viewer frame
        radar_viewer_rect_pos = ( radar_frame_rect_size[0] + 1 + screenobj_planetmain.map_position[0],
                                  radar_frame_rect_size[1] + 1 + screenobj_planetmain.map_position[1],
                                  screenobj_planetmain.radar_viewer_rect_size[0],
                                  screenobj_planetmain.radar_viewer_rect_size[1])
        pygame.draw.rect(self.screen_buffer, (0xff, 0x0c, 0x00), radar_viewer_rect_pos, 1)

        return self.screen_buffer


