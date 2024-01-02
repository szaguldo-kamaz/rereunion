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
        self.prepare_infobuy()
        self.prepare_researchdesign_computer()
        self.prepare_ship()
        self.prepare_starmap()
        self.prepare_felszin()
        self.prepare_planetmain()

        self.menu_full = pygame.Surface((320, 64))
        self.infobar = pygame.Surface((320, 17))
        self.surface_building = pygame.Surface((77, 64))

        self.screen_controlroom = pygame.Surface((320, 200))
        self.screen_buffer = pygame.Surface((320, 200))

        self.window = pygame.display.set_mode(self.window_size)
        #self.window = pygame.display.set_mode((320, 200), flags = pygame.SCALED | pygame.RESIZABLE)

        self.current_mousecursor = None
        self.set_mousecursor("normal")


    def set_mousecursor(self, towhat):

        if self.current_mousecursor != towhat:
            self.current_mousecursor = towhat
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
                    if PCXdata_pointer_uncompressed_RGB >= imagesize:  # e.g. INFO26
                        break
    #                PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB:PCXdata_pointer_uncompressed_RGB+3] = palette[ palette_pos: palette_pos+3 ];
    #                PCXdata_pointer_uncompressed_RGB += 3
    # this is faster... :
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos ]
                    PCXdata_pointer_uncompressed_RGB += 1
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 1 ]
                    PCXdata_pointer_uncompressed_RGB += 1
                    PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = palette[ palette_pos + 2 ]
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

        [ width, height ] = struct.unpack_from("<HH", PICdata_compressed_raw, 8)
        PICimagesize = width * height * 3

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

            compressed_raw_length = struct.unpack_from("<H", ICONALLdata, ICONALLdata_pointer)[0]
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

        PIClist.append("ICON/ICONMAIN.PIC")  # Ikonok keretei es egermutatok - Icon frames and mouse pointers

        PIClist.append("GRAFIKA/MAIN.PIC")  # Fokepernyo - Main screen
        PIClist.append("GRAFIKA/TEXT.PIC")  # Fokepernyo - gomb funkcioja, penz, datum - Main screen button function, money, date
        PIClist.append("GRAFIKA/HEROES.PIC")  # Heroes
        PIClist.append("GRAFIKA/MAINFACE.PIC")  # Commanders

        PIClist.append("GRAFIKA/RESEARCH.PIC")  # Talalmanyok nezet - Research-design
        PIClist.append("GRAFIKA/CDS.PIC")  # Talalmanyok nezet - CD-k

        PIClist.append("GRAFIKA/DESIGNER.PIC")  # Bolygo felszin nezet - Planet main

        PIClist.append("GRAFIKA/INFO.PIC")  # INFO-BUY main frame
        PIClist.append("GRAFIKA/SELECT.PIC")  # INFO-BUY list frame
        # Info pics
        for info_no in range(1,36):
            PIClist.append("INFO/INFO%d.PIC"%(info_no))  # INFO-BUY kepek - illustrations

        # Fajok
        for faj_no in range(14):
            PIClist.append("PLANETS/FAJ%d.PIC"%(faj_no))  # Fajok - Species

        # Naprendszerek / csillagterkep
        for hatter_no in range(1,5):
            PIClist.append(f"PLANETS/HATTER{hatter_no}.PIC")  # Starmap hatterek/ikonok - Starmap backgrounds/icons
        for napr_no in range(1,9):
            PIClist.append(f"PLANETS/NAPR{napr_no}.PIC")  # Naprendszer grafikak, nap/bolygok/holdak/flotta/ikonok - Solarsys graphics sun/planets/moons/fleet/icons

        PIClist.append("GRAFIKA/UZENET.PIC")  # Uzenetek - Messages screen

        PIClist.append("GRAFIKA/SHIP1.PIC")  # Ship Groups - space forces background
        PIClist.append("GRAFIKA/SHIP2.PIC")  # Ship Groups - planet forces background
        PIClist.append("GRAFIKA/SHIP3.PIC")  # Ship Groups - sprites

        # Nagy
        #for nagy_no in range(13):
        #    PIClist.append("PLANETS/NAGY%d.PIC"%(nagy_no))  #.

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
                    red_charset_full[pixel_x][pixel_y] = 0xa63410
                elif yellow_charset_full[pixel_x][pixel_y] == 0x3b87df:
                    yellow_charset_full[pixel_x][pixel_y] = 0xb6aa00
                    red_charset_full[pixel_x][pixel_y] = 0xe74518

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


    def prepare_infobuy(self):

        self.PICs["SELECT"] = self.PICs["SELECT"].subsurface(pygame.Rect(0, 0, 126, 126))
        for infopic_no in range(1,36):
            self.PICs["INFO%d"%(infopic_no)] = self.PICs["INFO%d"%(infopic_no)].subsurface(pygame.Rect(6, 6, 180, 115))


    def prepare_researchdesign_computer(self):

        self.researchdesign_invention_cds_anim = []
        self.researchdesign_invention_cds_init = []

        for cd_y in range(0, 5):
            self.researchdesign_invention_cds_anim.append([])
            for cd_x in range(0, 320, 32):
                self.researchdesign_invention_cds_anim[cd_y].append( self.PICs["CDS"].subsurface(pygame.Rect( cd_x, cd_y * 16, 32, 15)) )
            self.researchdesign_invention_cds_init.append(self.researchdesign_invention_cds_anim[cd_y].pop(0))

        self.researchdesign_computer_txt = ( self.PICs["CDS"].subsurface(pygame.Rect( 18, 79, 11, 5)),
                                             self.PICs["CDS"].subsurface(pygame.Rect(  0, 79, 11, 5)) )
        self.researchdesign_computer_led = ( self.PICs["CDS"].subsurface(pygame.Rect( 30, 79,  5, 5)),
                                             self.PICs["CDS"].subsurface(pygame.Rect( 12, 79,  5, 5)) )


    def prepare_ship(self):
        self.ship_icon_button_unselected = self.PICs["SHIP3"].subsurface(pygame.Rect( 197, 22, 7, 6))
        self.ship_icon_button_selected   = self.PICs["SHIP3"].subsurface(pygame.Rect( 213, 22, 7, 6))
        self.ship_icon_planetforces      = self.PICs["SHIP3"].subsurface(pygame.Rect( 6*32 + 1, 1, 30, 14))
        self.ship_icons_spaceforces = [ [], [], [], [], [] ]  # dummy, red, green, brown, blue
        for ship3_icon_y in range(0, 4):
            self.ship_icons_spaceforces[ship3_icon_y + 1].append(None)  # dummy orbit state
            for ship3_icon_x in range(1, 193, 32):
                self.ship_icons_spaceforces[ship3_icon_y + 1].append( self.PICs["SHIP3"].subsurface(pygame.Rect( ship3_icon_x, ship3_icon_y * 16 + 1, 30, 14)) )
                self.ship_icons_spaceforces[ship3_icon_y + 1][-1].set_colorkey(pygame.Color(0, 0, 0))

        self.ship_icon_planetforces.set_colorkey(pygame.Color(0, 0, 0))


    def prepare_starmap(self):

        self.starmap_suns = []
        self.starmap_labels = []
        self.starmap_planets = []  # for each solsys
        self.starmap_moons = []  # for each solsys

        for solsys_no in range(8):

            solsys_col = solsys_no // 4
            solsys_idx = solsys_no % 4
            self.starmap_labels.append(self.PICs["HATTER3"].subsurface(pygame.Rect(solsys_idx*64, solsys_col*19, 64, 19)))
            self.starmap_labels[solsys_no].set_colorkey(pygame.Color(0, 0, 0))

            self.starmap_suns.append(self.PICs[f"NAPR{solsys_no+1}"].subsurface(pygame.Rect(0, 1, 64, 64)))
            self.starmap_suns[solsys_no].set_colorkey(pygame.Color(0, 0, 0))

            self.starmap_planets.append([])
            for planet_no in range(8):
                self.starmap_planets[solsys_no].append(self.PICs[f"NAPR{solsys_no+1}"].subsurface(pygame.Rect(64 + planet_no*32, 1, 32, 32)))
                self.starmap_planets[solsys_no][planet_no].set_colorkey(pygame.Color(0, 0, 0))

            self.starmap_moons.append([])
            for moon_no in range(28):
                moon_col = moon_no // 14
                moon_idx = moon_no % 14
                self.starmap_moons[solsys_no].append(self.PICs[f"NAPR{solsys_no+1}"].subsurface(pygame.Rect(66 + moon_idx*17, 34 + (moon_col * 17), 16, 16)))
                self.starmap_moons[solsys_no][moon_no].set_colorkey(pygame.Color(0, 0, 0))


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
        elif screenobj.screentype == "researchdesign":
            return self.render_researchdesign(screenobj)
        elif screenobj.screentype == "infobuy":
            return self.render_infobuy(screenobj)
        elif screenobj.screentype == "ship":
            return self.render_ship(screenobj)
        elif screenobj.screentype == "starmap":
            return self.render_starmap(screenobj)
        elif screenobj.screentype == "messages":
            return self.render_messages(screenobj)


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


    # info-buy
    def render_infobuy(self, screenobj_infobuy):

        self.screen_buffer.blit(self.render_menu(screenobj_infobuy.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_infobuy.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["INFO"], (0, 49))
        self.screen_buffer.blit(self.PICs["SELECT"], (0, 49))

        # Item list
        for listitem_no in range(min(13,screenobj_infobuy.invention_item_list_len)):
            listitem_index = listitem_no + screenobj_infobuy.scroll_start
            if listitem_index == screenobj_infobuy.selected_item_listno:
                itemcolor = 2
            else:
                itemcolor = 1
            self.screen_buffer.blit(self.render_text(screenobj_infobuy.invention_item_list[listitem_index][1], textcolor = itemcolor),
                                    (16, 55 + listitem_no * 9) )

        if screenobj_infobuy.picturemode:
            # Item pic
            self.screen_buffer.blit(self.PICs["INFO%d"%(screenobj_infobuy.selected_item_invno)], (134, 55))
#            self.screen_buffer.blit(self.PICs["INFO26"], (134, 55))
        else:
            # Item info
            self.screen_buffer.blit(self.render_text(screenobj_infobuy.invention_description[0], textcolor = 2), (136, 59) )
            for descline_no in range(1, 7):
                self.screen_buffer.blit(self.render_text(screenobj_infobuy.invention_description[descline_no], textcolor = 1), (136, 61 + descline_no * 10) )
            self.screen_buffer.blit(self.render_text("Ore needed: [One piece]", textcolor = 2), (136, 133) )
            self.screen_buffer.blit(self.render_text("Detoxin:%5d"%(screenobj_infobuy.minerals[0]), textcolor = 1), (142, 142) )
            self.screen_buffer.blit(self.render_text("Energon:%5d"%(screenobj_infobuy.minerals[1]), textcolor = 1), (142, 151) )
            self.screen_buffer.blit(self.render_text("Raenium:%5d"%(screenobj_infobuy.minerals[4]), textcolor = 1), (142, 160) )
            self.screen_buffer.blit(self.render_text("Kremir  :%5d"%(screenobj_infobuy.minerals[2]), textcolor = 1), (225, 142) )
            self.screen_buffer.blit(self.render_text("Texon   :%5d"%(screenobj_infobuy.minerals[5]), textcolor = 1), (225, 151) )
            self.screen_buffer.blit(self.render_text("Lepitium:%5d"%(screenobj_infobuy.minerals[3]), textcolor = 1), (225, 160) )

        if screenobj_infobuy.can_be_produced:
            self.screen_buffer.blit(self.render_text("Stores:", textcolor = 1), (14, 189) )
            self.screen_buffer.blit(self.render_text("%d"%(screenobj_infobuy.stores), textcolor = 2), (100, 189) )
            if screenobj_infobuy.bought_items > 0:
                self.screen_buffer.blit(self.render_text("Bought items:", textcolor = 1), (14, 180) )
                self.screen_buffer.blit(self.render_text("%d"%(screenobj_infobuy.bought_items), textcolor = 2), (100, 180) )
                self.screen_buffer.blit(self.render_text("Time to go:", textcolor = 1), (160, 180) )
                self.screen_buffer.blit(self.render_text("%d"%(screenobj_infobuy.time_to_go), textcolor = 2), (264, 180) )
                self.screen_buffer.blit(self.render_text("Total price:", textcolor = 1), (160, 189) )
                self.screen_buffer.blit(self.render_text("%d"%(screenobj_infobuy.total_price), textcolor = 2), (264, 189) )
        else:
            self.screen_buffer.blit(self.render_text(screenobj_infobuy.cannot_be_produced_reason, textcolor = 2), (14, 189) )

        return self.screen_buffer


    # research-design - inventions
    def render_researchdesign(self, screenobj_researchdesign):

        self.screen_buffer.blit(self.render_menu(screenobj_researchdesign.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_researchdesign.menu_info), (0, 32))

        # TODO
        animstate = 0

        # main pic
        self.screen_buffer.blit(self.PICs["RESEARCH"], (0, 49))

        # CDs
        for invention_no in range(0,35):
            cd_state = screenobj_researchdesign.iconstates[invention_no]
            if cd_state == -1:
                continue
            if cd_state == 4:  # under analysis
                cd_to_blit = self.researchdesign_invention_cds_anim[cd_state][screenobj_researchdesign.anim_states["vumeter"]["currframe"]]
            else:
            # TODO
                cd_to_blit = self.researchdesign_invention_cds_init[cd_state]
            cd_pos = (0 + (invention_no % 5) * 32, 49 + 4 + int(invention_no / 5) * 16)
            self.screen_buffer.blit(cd_to_blit, cd_pos)

        # Project name / status
        if screenobj_researchdesign.project_selected != None:
            self.screen_buffer.blit(self.render_text("Project name :", textcolor = 1), (190, 76))
            self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_name, textcolor = 1), (200, 88))
            self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_status, textcolor = 1), (190, 100))
            if screenobj_researchdesign.project_selected_requiredskills != None:
                print("puzomajom", screenobj_researchdesign.project_selected_requiredskills[0])
            if screenobj_researchdesign.project_selected_completionratio != None:
                print("puzomajom2", screenobj_researchdesign.project_selected_completionratio)

        # computer state - on/off text
        self.screen_buffer.blit(self.researchdesign_computer_txt[screenobj_researchdesign.computer_state], ( 76, 170))
        # computer state - on/off led
        self.screen_buffer.blit(self.researchdesign_computer_led[screenobj_researchdesign.computer_state], (149, 170))

        # developer name
        yellow_text_developer_name = self.render_text(screenobj_researchdesign.developer_name, textcolor = 1)
        self.screen_buffer.blit(yellow_text_developer_name, (8, 188))
        # developer level
        yellow_text_developer_level_math  = self.render_text(str(screenobj_researchdesign.developer_level[0]), textcolor = 1)
        yellow_text_developer_level_phys  = self.render_text(str(screenobj_researchdesign.developer_level[1]), textcolor = 1)
        yellow_text_developer_level_elect = self.render_text(str(screenobj_researchdesign.developer_level[2]), textcolor = 1)
        yellow_text_developer_level_AI    = self.render_text(str(screenobj_researchdesign.developer_level[3]), textcolor = 1)
        self.screen_buffer.blit(yellow_text_developer_level_math,  (136, 188))
        self.screen_buffer.blit(yellow_text_developer_level_phys,  (203, 188))
        self.screen_buffer.blit(yellow_text_developer_level_elect, (259, 188))
        self.screen_buffer.blit(yellow_text_developer_level_AI,    (296, 188))

        return self.screen_buffer


    # starmap / galactic map
    def render_starmap(self, screenobj_starmap):

        self.screen_buffer.blit(self.render_menu(screenobj_starmap.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_starmap.menu_info), (0, 32))

        curr_solsys_no = screenobj_starmap.location[0] - 1

        if screenobj_starmap.planet_and_moon_mode:

            curr_planet_no = screenobj_starmap.location[1] - 1

            # background pic
            self.screen_buffer.blit(self.PICs["HATTER2"], (0, 49))

            # Planet
            self.screen_buffer.blit(self.starmap_planets[curr_solsys_no][curr_planet_no], (160-16, 49+75-16))

            # Moons
            mooncnt = 0
            for moon_seqid in screenobj_starmap.selected_planet.moons_seqids:
                self.screen_buffer.blit(self.starmap_moons[curr_solsys_no][moon_seqid], screenobj_starmap.orbit_pixposes[mooncnt])
                mooncnt += 1

        else:

            # background pic
            self.screen_buffer.blit(self.PICs["HATTER1"], (0, 49))

            # Sun
            self.screen_buffer.blit(self.starmap_suns[curr_solsys_no], (160-32, 49+75-32))

            # Planets
            for planet_no in range(screenobj_starmap.selected_solarsystem.num_of_planets):
                self.screen_buffer.blit(self.starmap_planets[curr_solsys_no][planet_no], screenobj_starmap.orbit_pixposes[planet_no])

            # System no. labels
            for system_no in range(8):
                if screenobj_starmap.gamedata_dynamic["systems_available"][system_no] > -1:
                    self.screen_buffer.blit(self.starmap_labels[system_no], (256, 49 + system_no * 19))


        return self.screen_buffer


    # groups/ships
    def render_ship(self, screenobj_ship):

        self.screen_buffer.blit(self.render_menu(screenobj_ship.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_ship.menu_info), (0, 32))

        # main pic
        if screenobj_ship.currentview == 0:  # space forces
            self.screen_buffer.blit(self.PICs["SHIP1"], (0, 49))
        else:  # planet forces
            self.screen_buffer.blit(self.PICs["SHIP2"], (0, 49))

        group_count = len(screenobj_ship.current_shipgroup)
        for group_no in range(1, 33):

            colpos = (group_no - 1) // 8
            rowpos = (group_no - 1) % 8

            # draw buttons
            if group_no == screenobj_ship.selected_group_no_current:
                buttonicon = self.ship_icon_button_selected
            else:
                buttonicon = self.ship_icon_button_unselected
            self.screen_buffer.blit(buttonicon, (5 + colpos * 48, 65 + rowpos * 16))
            if group_no >= group_count:
                continue

            curgrp = screenobj_ship.current_shipgroup[group_no]

            # draw forces icons
            if curgrp.type == 5:
                forces_icon = self.ship_icon_planetforces
            else:
                forces_icon = self.ship_icons_spaceforces[curgrp.type][curgrp.orbit_status]
            self.screen_buffer.blit(forces_icon, (17 + colpos * 48, 61 + rowpos * 16))

        # draw selected forces data text

        curgrp = screenobj_ship.current_shipgroup[screenobj_ship.selected_group_no_current]
        [ sysname, planetname, moonname ] = screenobj_ship.selected_group_location_names

        if curgrp.type in [1, 5]:
            shiplist = [ "Hunter", "Fighter", "Destroyer", "Cruiser" ]
#            vehiclelist = [ "Trooper", "Tank", "Aircraft", "Miss Tank" ]
            vehiclelist = [ "Trooper", "Tank", "Aircraft", "Launcher" ]

        elif curgrp.type == 2:
            shiplist = [ "Sloop", "Trade ship", "Piracy ship", "Galleon" ]
            vehiclelist = []

        elif curgrp.type == 4:
            shiplist = [ "Sat Carr" ]
            vehiclelist = [ "Satellite", "Spy Sat", "Spy Ship", "Solar Plant" ]

        yellow_text_colon = self.render_text(":", textcolor = 1)

        allvehiclescount = 0
        horizoffset = 0
        vertoffset = 0
        for vehicletype in shiplist + vehiclelist:
            allvehiclescount += 1
            if curgrp.fleet[vehicletype] > 0:
                yellow_text_vehicletype_name = self.render_text(f"{vehicletype}", textcolor = 1)
                red_text_vehicletype_name = self.render_text(f"{curgrp.fleet[vehicletype]:3}", textcolor = 2)
                self.screen_buffer.blit(yellow_text_vehicletype_name, (204 + horizoffset, 116 + vertoffset))
                self.screen_buffer.blit(yellow_text_colon, (274, 116 + vertoffset))
                self.screen_buffer.blit(red_text_vehicletype_name, (280, 116 + vertoffset))
                vertoffset += 9
            if allvehiclescount == 4 and curgrp.type != 4:
                vertoffset += 3
            if curgrp.type == 4 and vehicletype == "Sat Carr":
                horizoffset = 4
                vertoffset += 3

        # group name
        red_text_group_name = self.render_text(curgrp.name, textcolor = 2)

        # location
        if curgrp.type == 5:
            locbasetext = "Base on:  "
        else:
            if 4 <= curgrp.orbit_status <= 6:
                locbasetext = "Destination:"
            else:
                locbasetext = "Currently on:"

        yellow_text_group_loc_basetext = self.render_text(f"{locbasetext}", textcolor = 1)
        yellow_text_group_loc_sysname = self.render_text(f"{sysname}", textcolor = 1)
        yellow_text_group_loc_planetname = self.render_text(f"{planetname}", textcolor = 1)
        self.screen_buffer.blit(red_text_group_name, (202, 60))
        self.screen_buffer.blit(yellow_text_group_loc_basetext, (202, 70))

        if screenobj_ship.currentview == 0:  # space forces
            self.screen_buffer.blit(yellow_text_group_loc_sysname, (282, 70))
        else:  # ground forces
            self.screen_buffer.blit(yellow_text_group_loc_sysname, (258, 70))

        self.screen_buffer.blit(yellow_text_group_loc_planetname, (211, 79))
        if moonname != None:
            yellow_text_group_loc_moonname = self.render_text(f"{moonname}", textcolor = 1)
            self.screen_buffer.blit(yellow_text_group_loc_moonname, (220, 89))

        # when flying
        if 4 <= curgrp.orbit_status <= 6:
            yellow_text_time_remaining = self.render_text(f"Time remaining:{curgrp.remaining_flight_time}", textcolor = 1)
            self.screen_buffer.blit(yellow_text_time_remaining, (202, 100))


        return self.screen_buffer


    # planet main - planet surface
    def render_planetmain(self, screenobj_planetmain):

        self.screen_buffer.blit(self.render_menu(screenobj_planetmain.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_planetmain.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["DESIGNER"], (0, 49))

        # build icon
        buildicon_state = screenobj_planetmain.anim_states["builddemolish"]["currframe"] and screenobj_planetmain.build_mode
        self.screen_buffer.blit(self.planetmain_buildicon[buildicon_state], (0, 1 + 49))
        # demolish icon
        demolishicon_state = screenobj_planetmain.anim_states["builddemolish"]["currframe"] and screenobj_planetmain.demolish_mode
        self.screen_buffer.blit(self.planetmain_demolishicon[demolishicon_state], (45, 1 + 49))
        # building - invention up kammide
        self.screen_buffer.blit(self.planetmain_arrowup[screenobj_planetmain.selected_building_is_first], (0, 15 + 49))
        # building - invention down
        self.screen_buffer.blit(self.planetmain_arrowdown[screenobj_planetmain.selected_building_is_last], (0, 48 + 49))
        # building on surface illustration
        self.screen_buffer.blit(self.render_building(screenobj_planetmain.planet, self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]), (12, 15 + 49))
        # building name
        yellow_text_building_name = self.render_text(
                                        self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]["name"],
                                        textcolor = 1)
        self.screen_buffer.blit(yellow_text_building_name, (2, 81 + 49))

        # surface map
        planet_surface = self.render_surface_with_buildings(screenobj_planetmain.planet, screenobj_planetmain.anim_states["surface"]["currframe"])
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


    # messages
    def render_messages(self, screenobj_messages):

        self.screen_buffer.blit(self.render_menu(screenobj_messages.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_messages.menu_info), (0, 32))

        animstate = 0

        # main pic
        self.screen_buffer.blit(self.PICs["UZENET"], (0, 49))

        # messages
        for msg_no in range(len(screenobj_messages.messages)):
            msgbitmap = self.render_text(screenobj_messages.messages[msg_no][0], textcolor = screenobj_messages.messages[msg_no][1])
            self.screen_buffer.blit(msgbitmap, (10, 57 + msg_no * 9))

        return self.screen_buffer

