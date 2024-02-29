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
        # load all of the ANIs
        self.ANIs = self.load_allANIs()

        self.prepare_charsets()
        self.prepare_icons()
        self.prepare_mousepointers()
        self.prepare_controlroom_anims()
        self.prepare_heroes_and_commanders()
        self.prepare_infobuy()
        self.prepare_researchdesign_computer()
        self.prepare_ship()
        self.prepare_starmap()
        self.prepare_felszin()
        self.prepare_planetmain()
        self.prepare_mine_szamok()
        self.prepare_kocsma_anims()
        self.prepare_kocsmatoltelekek()

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


    def decode_rawANIframe(self, PCXdata_compressed_raw, imagesize, palette, previous_uncompressed_frame = None, PCXdata_pointer_compressed_raw = 0):

        PCXdata_pointer_uncompressed_RGB = 0
        PCXdata_uncompressed_RGB = bytearray(imagesize)

        compressed_size = len(PCXdata_compressed_raw)

        while PCXdata_pointer_compressed_raw < compressed_size:

            if PCXdata_compressed_raw[PCXdata_pointer_compressed_raw] < 0x80:

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

                currPCXdata = PCXdata_compressed_raw[PCXdata_pointer_compressed_raw]

                if currPCXdata in [ 0x80, 0xC0 ]:
                    repeat = struct.unpack_from("<H", PCXdata_compressed_raw, PCXdata_pointer_compressed_raw + 1)[0]
                    PCXdata_pointer_compressed_raw += 2
                else:
                    repeat = currPCXdata & 0x3F

                # copy from previous frame
                if currPCXdata < 0xC0:

                    for subpixcounter in range(repeat*3):
                        PCXdata_uncompressed_RGB[PCXdata_pointer_uncompressed_RGB] = previous_uncompressed_frame[PCXdata_pointer_uncompressed_RGB]
                        PCXdata_pointer_uncompressed_RGB += 1

                # repeat current pixel
                else:

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


    def loadANI(self, ANIfilename, palettePICfilename):

        palettePICfile = open(palettePICfilename, 'rb')
        palettePICrawdata = palettePICfile.read()
        palettePICfile.close()

        palette = palettePICrawdata[-768:]

        ANIfile = open(ANIfilename, 'rb')
        ANIdata_compressed_raw = ANIfile.read()
        ANIfile.close()
        ANIlength = len(ANIdata_compressed_raw)

        ANIframes_uncompressed_RGB = []
        currframe_start_pointer = 0
        previous_uncompressed_frame = None

        while currframe_start_pointer < ANIlength:

            ANIheader = struct.unpack_from("<H9sHH", ANIdata_compressed_raw, currframe_start_pointer)
            if ANIheader[1] != b'SpidyAnim':
                print('Error in ANI file (magic id string mismatch): ', ANIfilename)
                return [ None, [ 0, 0 ] ]
            framelen = ANIheader[0]
            width = ANIheader[2]
            height = ANIheader[3]
            ANIimagesize = width * height * 3

            currframe_start_pointer += 15
            compressed_framedata = ANIdata_compressed_raw[currframe_start_pointer:currframe_start_pointer + framelen]
            uncompressed_framedata = self.decode_rawANIframe(compressed_framedata, ANIimagesize, palette, previous_uncompressed_frame)
            ANIframes_uncompressed_RGB.append(uncompressed_framedata)
            previous_uncompressed_frame = uncompressed_framedata

            currframe_start_pointer += framelen

        return [ ANIframes_uncompressed_RGB, [ width, height ] ]


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

        PIClist.append("GRAFIKA/MINER.PIC")  # Banya - Mine
        PIClist.append("GRAFIKA/SZAMOK.PIC")  # Banya/szamok - Mine/numbers

        PIClist.append("PLANETS/FANIM1.PIC")  # Felszin animacio - Surface anim (earth-like)
        PIClist.append("PLANETS/FANIM5.PIC")  # Felszin animacio - Surface anim (rocky)
        PIClist.append("PLANETS/FANIM10.PIC")  # Felszin animacio - Surface anim (tropical)

        PIClist.append("GRAFIKA/CHARSET1.PIC")  # Karakterkeszlet - Charset

        PIClist.append("ICON/ICONMAIN.PIC")  # Ikonok keretei es egermutatok - Icon frames and mouse pointers

        PIClist.append("GRAFIKA/TEXT.PIC")  # Fokepernyo - gomb funkcioja, penz, datum - Main screen button function, money, date

        PIClist.append("GRAFIKA/MAIN.PIC")  # Fokepernyo - Main screen
        PIClist.append("GRAFIKA/HEROES.PIC")  # Heroes
        PIClist.append("GRAFIKA/MAINFACE.PIC")  # Commanders
        PIClist.append("GRAFIKA/MAINA1.PIC")  # Fokepernyo animacio 1 - Main screen anim 1
        PIClist.append("GRAFIKA/MAINA2.PIC")  # Fokepernyo animacio 2 - Main screen anim 2
        PIClist.append("GRAFIKA/MAINA3.PIC")  # Fokepernyo animacio 3 - Main screen anim 3
        PIClist.append("GRAFIKA/MAINA4.PIC")  # Fokepernyo animacio 4 - Main screen anim 4
        PIClist.append("GRAFIKA/MAINA5.PIC")  # Fokepernyo animacio 5 - Main screen anim 5

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

        PIClist.append("GRAFIKA/KOCSMA.PIC")  # Kocsma - Space local background
        PIClist.append("GRAFIKA/KOCSMAAN.PIC")  # Kocsma animaciok - Space local anims
        PIClist.append("GRAFIKA/PIRATES.PIC")  # Kocsmatoltelekek - Space local guests

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


    def load_allANIs(self):

        ANIlist = [ ]

        # ani file, pic file to use for paletta, colorkey, trim 1 pixel border
        ANIlist.append([ "ANIM/MAIN1.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #1 feny csillan 1
        ANIlist.append([ "ANIM/MAIN2.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #2 urhajo elsuhan 1
        ANIlist.append([ "ANIM/MAIN3.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #3 urhajo elsuhan 2
        ANIlist.append([ "ANIM/MAIN4.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #4 urhajo elsuhan 3
        ANIlist.append([ "ANIM/MAIN5.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #5 urhajo elsuhan 4
        ANIlist.append([ "ANIM/MAIN6.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: space local ajton at nezve #6 feny csillan 2

        ANIlist.append([ "ANIM/MAIN11.ANI", "GRAFIKA/MAIN.PIC", None, True ])          # control room: research-design kepernyo bekapcs
        ANIlist.append([ "ANIM/MAIN12.ANI", "GRAFIKA/MAIN.PIC", (0x17, 0, 0), True ])  # control room: messages kepernyo bekapcs

        ANIs = {}

        for ANIpath, palettefilename, ANIcolorkey, trimborder in ANIlist:
            [ ANIframes, ANIsize ] = self.loadANI(ANIpath, palettefilename)
            ANIname = ANIpath[:-4]
            ANIs[ANIname] = []
            for ANIframe in ANIframes:
                aniframe_pyimage = pygame.image.frombytes(ANIframe, ANIsize, 'RGB')
                if trimborder:
                    aniframe_pyimage = aniframe_pyimage.subsurface(pygame.Rect(1, 1, ANIsize[0] - 2, ANIsize[1] - 2))

                ANIs[ANIname].append(aniframe_pyimage)
                if ANIcolorkey != None:
                    ANIs[ANIname][-1].set_colorkey(pygame.Color(ANIcolorkey[0], ANIcolorkey[1], ANIcolorkey[2]))

        return ANIs


    def slice_picsequence(self, picsequence_def):

        frames_dict = {}

        for seqname in picsequence_def.keys():

            frames_dict[seqname] = []

            [ PICsurface, number_of_frames, number_of_frames_in_a_row, width, height, width_offset, height_offset, colspacer, rowspacer, colorkey ] = picsequence_def[seqname]
            colspace = width + colspacer
            rowspace = height + rowspacer

            for frameidx in range(number_of_frames):
                x = (frameidx % number_of_frames_in_a_row) * colspace + width_offset
                y = (frameidx // number_of_frames_in_a_row) * rowspace + height_offset
                frames_dict[seqname].append(PICsurface.subsurface(pygame.Rect(x, y, width, height)))
                if colorkey != None:
                    frames_dict[seqname][-1].set_colorkey(pygame.Color(colorkey))

        return frames_dict


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


    def prepare_controlroom_anims(self):

        self.controlroom_anims_pasteposes = {
            "rightdoor"        : (273,  8 + 49),
            "commanderdoor"    : (172,      49),
            "liftdoor"         : (202,  7 + 49),
            "liftlights"       : (205, 21 + 49),
            "liftlights_up"    : (205, 21 + 49),
            "liftlights_dn"    : (205, 21 + 49),
            "radarscreen"      : ( 37,      49),
            "liftpanel"        : (226, 32 + 49),
            "researchcomputer" : ( 40,      73),
            "messagescomputer" : ( 14,      73)
        }

        self.controlroom_anim_defs = {
            # name                  PICsurface       nf  fr   w   h   wo   ho cs rs  colorkey
            "rightdoor"     : [ self.PICs["MAINA1"],  6,  6, 47, 136,   0,   0, 0, 0, None ],
            "commanderdoor" : [ self.PICs["MAINA2"],  4,  4, 18,  89,   0,   0, 0, 0, None ],
            "liftdoor"      : [ self.PICs["MAINA3"],  4,  4, 21, 105,   0,   0, 0, 0, None ],
            "liftlights"    : [ self.PICs["MAINA4"], 16, 16, 16,  91,   0,   0, 0, 0, None ],
            "radarscreen"   : [ self.PICs["MAINA5"], 48, 16, 19,  21,   0,   1, 0, 1, None ],
            "liftpanel"     : [ self.PICs["MAINA5"], 10, 10, 12,  14, 115,  45, 1, 0, None ],
        }

        self.controlroom_anims = self.slice_picsequence(self.controlroom_anim_defs)

        self.controlroom_anims["liftlights_up"] = self.controlroom_anims["liftlights"][:7]
        self.controlroom_anims["liftlights_dn"] = self.controlroom_anims["liftlights"][-10:]
        self.controlroom_anims["liftlights_dn"].reverse()

        self.controlroom_anims["researchcomputer"] = self.ANIs["ANIM/MAIN11"]
        self.controlroom_anims["messagescomputer"] = self.ANIs["ANIM/MAIN12"]


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

        self.cd_anim_defs = {
            # name                PICsurface     nf  rf   w   h  wo   ho cs rs  colorkey
            "normaltray"   : [ self.PICs["CDS"], 10, 10, 32, 15,  0,   0, 0, 1, None ],
            "?starttray"   : [ self.PICs["CDS"], 10, 10, 32, 15,  0,  16, 0, 1, None ],
            "?nostarttray" : [ self.PICs["CDS"], 10, 10, 32, 15,  0,  32, 0, 1, None ],
            "emptytray"    : [ self.PICs["CDS"], 10, 10, 32, 15,  0,  48, 0, 1, None ],
            "spectrum"     : [ self.PICs["CDS"], 10, 10, 32, 15,  0,  64, 0, 1, None ]
        }

        self.cd_anims = self.slice_picsequence(self.cd_anim_defs)

        self.cd_animname_map = [
            "",
            "?starttray",
            "",
            "emptytray",
            "",
            "normaltray"
        ]

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

        self.planetmain_vert_lines  = [ self.PICs["DESIGNER"].subsurface(pygame.Rect(  94,  5,  2, 68)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect(  97,  5,  2, 68)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 100,  5,  2, 65)),
                                        self.PICs["DESIGNER"].subsurface(pygame.Rect( 103,  5,  2, 65)) ]

        self.planetmain_designer = self.PICs["DESIGNER"].copy()
        self.planetmain_designer.fill(pygame.Color(0, 0, 0), pygame.Rect(94, 5, 123, 77))

        self.planetmain_epulet_illust = []
        for epulet_no in range(1,27):
            self.planetmain_epulet_illust.append(self.PICs[f"EPULET{epulet_no}"].subsurface(pygame.Rect(  2,  2, 86, 68)))


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


    def prepare_mine_szamok(self):

        self.mine_szamok_defs = {
            # name            PICsurface       nf  rf   w   h   wo   ho  cs rs  colorkey
            "nagy"    : [ self.PICs["SZAMOK"], 10,  5, 50, 35,   0,   0, 14, 0, None ],
            "kozepes" : [ self.PICs["SZAMOK"], 10, 10, 14, 35,   1,  70,  2, 0, None ],
            "kicsi"   : [ self.PICs["SZAMOK"], 10, 10, 12,  9, 163,  71,  1, 0, None ],
        }

        self.mine_szamok = self.slice_picsequence(self.mine_szamok_defs)


    def prepare_kocsma_anims(self):

        self.kocsma_anims_pasteposes = {
            "greenlights"     : (166, 49 +  3),
            "lavalampa"       : ( 78, 49 + 28),
            "kartyazoszormok" : (210, 49 + 29),
            "hatsoatjaro"     : (210, 49 +  8),
            "kisasztal1"      : (161, 49 + 29),
#            "kisasztal2"      : (160, 49 + 28),
            "rosszlampa"      : (233, 49 +  0),
            "rossztv"         : (114, 49 +  0),
            "zagyva"          : (269, 49 +  7),
            "nagyasztal"      : (181, 49 + 33),
            "knightrider"     : (267, 49 + 39)
        }

        self.kocsma_anim_defs = {
            # name                     PICsurface        nf  rf   w   h  wo   ho cs rs  colorkey
            "greenlights"     : [ self.PICs["KOCSMAAN"], 21, 13, 23,  7,  0,   0, 0, 1,    None ],
            "lavalampa"       : [ self.PICs["KOCSMAAN"],  5,  5, 11, 13, 24,  54, 0, 0, (0,0,0) ],
            "kartyazoszormok" : [ self.PICs["KOCSMAAN"], 14, 13, 24, 25,  0,  16, 0, 1, (0,0,0) ],
            "hatsoatjaro"     : [ self.PICs["KOCSMAAN"], 13, 13, 22,  9, 24,  44, 0, 0,    None ],
            "kisasztal1"      : [ self.PICs["KOCSMAAN"], 14, 14, 16,  9, 90,  58, 0, 0,    None ],
            "kisasztal2"      : [ self.PICs["KOCSMAAN"], 15, 15, 15, 10, 22, 116, 0, 0,    None ],
            "rosszlampa"      : [ self.PICs["KOCSMAAN"], 12, 12,  4, 36,  0,  68, 0, 0,    None ],
            "rossztv"         : [ self.PICs["KOCSMAAN"],  5,  5, 22, 32, 48,  72, 0, 0, (0,0,0) ],
            "zagyva"          : [ self.PICs["KOCSMAAN"], 15, 14, 22, 10,  0, 105, 0, 1, (0,0,0) ],
            "nagyasztal"      : [ self.PICs["KOCSMAAN"], 32, 20, 16, 17,  0, 127, 0, 1,    None ],
            "knightrider"     : [ self.PICs["KOCSMAAN"], 18, 18,  9,  1,  0, 163, 0, 0,    None ]
        }

        self.kocsma_anims = self.slice_picsequence(self.kocsma_anim_defs)


    def prepare_kocsmatoltelekek(self):

        self.kocsmatoltelekek_pasteposes = {
            "undorling"    : (258, 49 + 12),
            "spy"          : (235, 49 + 41),
            "treasonable"  : (199, 49 +  0),
            "morgrul"      : (106, 49 +  5),
            "lenyzold"     : (144, 49 + 21),
            "bountyhunter" : (163, 49 + 32),
            "eran"         : ( 71, 49 + 81)
        }

        self.kocsmatoltelekek = {
            "bountyhunter" : self.PICs["PIRATES"].subsurface(pygame.Rect(  1,  1, 56, 118)),
            "lenyzold"     : self.PICs["PIRATES"].subsurface(pygame.Rect( 59,  1, 44, 107)),
            "undorling"    : self.PICs["PIRATES"].subsurface(pygame.Rect(105,  1, 28,  97)),
            "spy"          : self.PICs["PIRATES"].subsurface(pygame.Rect(135,  1, 45,  93)),
            "eran"         : self.PICs["PIRATES"].subsurface(pygame.Rect(182,  1, 92,  69)),
            "morgrul"      : self.PICs["PIRATES"].subsurface(pygame.Rect(182, 71, 69,  68)),
            "treasonable"  : self.PICs["PIRATES"].subsurface(pygame.Rect(276,  1, 40,  37))
        }

        for kocsmatoltelek in self.kocsmatoltelekek.keys():
            self.kocsmatoltelekek[kocsmatoltelek].set_colorkey(pygame.Color(0, 0, 0xFF))


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

        base_mapsurface = self.render_surface(planet, animstate).copy()  # copy() because it's coming from cache

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
        elif screenobj.screentype == "mine":
            return self.render_mine(screenobj)
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
        elif screenobj.screentype == "spacelocal":
            return self.render_spacelocal(screenobj)


    def __render_anims_helper(self, anims, animstates, pasteposes, blitscreen):

        for animname in pasteposes.keys():
            if animstates[animname].active > 0:
                frames = anims[animname]
                currframe_no = animstates[animname].currframe
                pastepos = pasteposes[animname]
                blitscreen.blit(frames[currframe_no], pastepos)


    # current_commanders <- gamedata_dynamic["commanders"]
    def render_controlroom(self, screenobj_controlroom):

        current_commanders = screenobj_controlroom.current_commanders

        self.screen_controlroom.blit(self.render_menu(screenobj_controlroom.menu_info), (0, 0))
        self.screen_controlroom.blit(self.render_infobar(screenobj_controlroom.menu_info), (0, 32))

        # control room background
        self.screen_controlroom.blit(self.PICs["MAIN"], (0, 49))

        self.__render_anims_helper(self.controlroom_anims, screenobj_controlroom.animstates, self.controlroom_anims_pasteposes, self.screen_controlroom)

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

        # TODO: space local door anim

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

        # main pic
        self.screen_buffer.blit(self.PICs["RESEARCH"], (0, 49))

        # CDs
        for invention_no in range(0,35):

            thisoneisselected = (screenobj_researchdesign.project_selected_cd_no == invention_no)
            research_state = screenobj_researchdesign.researchstates[invention_no]

            # research state 0 - unavailable (not shown) - no CD
            if research_state == 0:
                continue

            # research state 2 - tray with "?" CD - in research
            # research state 4 - tray without CD - in research
            elif research_state in [ 2, 4 ]:  # under analysis
                cd_to_blit = self.cd_anims["spectrum"][screenobj_researchdesign.animstates["spectrum"].currframe]

            # research state 1 - tray with "?" CD
            # research state 3 - tray without CD
            # research state 5 - done
            elif research_state in [ 1, 3, 5 ]:
                animname = self.cd_animname_map[research_state]

                if screenobj_researchdesign.animstates[animname + "open"].active > 0:
                    cdanimname = animname + "open"
                else:
                    cdanimname = animname + "close"

                if thisoneisselected:
                    frameno = screenobj_researchdesign.animstates[cdanimname].currframe
                else:
                    frameno = 0

                cd_to_blit = self.cd_anims[animname][frameno]

            else:
                print(f"Invalid research_state {research_state}! This should not happen!")
                exit(1)

            cd_pos = (0 + (invention_no % 5) * 32, 49 + 4 + int(invention_no // 5) * 16)
            self.screen_buffer.blit(cd_to_blit, cd_pos)

        # Project name / status
        if screenobj_researchdesign.project_selected != None:
            self.screen_buffer.blit(self.render_text("Project name :", textcolor = 1), (190, 76))
            self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_name, textcolor = 1), (200, 88))
            self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_status, textcolor = 1), (190, 100))
            if screenobj_researchdesign.project_selected_requiredskills != None:
                self.screen_buffer.blit(self.render_text("Math :", textcolor = 1), (189, 139))
                self.screen_buffer.blit(self.render_text("Elect:", textcolor = 1), (189, 149))
                self.screen_buffer.blit(self.render_text("Physics:", textcolor = 1), (235, 139))
                self.screen_buffer.blit(self.render_text("A.Int  :", textcolor = 1), (235, 149))
                self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_requiredskills[0], textcolor = 2), (224, 139))
                self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_requiredskills[2], textcolor = 2), (224, 149))
                self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_requiredskills[1], textcolor = 2), (282, 139))
                self.screen_buffer.blit(self.render_text(screenobj_researchdesign.project_selected_requiredskills[3], textcolor = 2), (282, 149))
            if screenobj_researchdesign.project_selected_completionratio != None:
                self.screen_buffer.blit(self.render_text(f"Completed: {screenobj_researchdesign.project_selected_completionratio}%", textcolor = 1), (190, 112))

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


        self.set_mousecursor(screenobj_starmap.mousecursor)


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

        if screenobj_ship.selected_group_no_current > 0:
            curgrp = screenobj_ship.current_shipgroup[screenobj_ship.selected_group_no_current]
            [ sysname, planetname, moonname ] = screenobj_ship.selected_group_location_names

            if curgrp.type in [1, 5]:
                shiplist = [ "Hunter", "Fighter", "Destroyer", "Cruiser" ]
#                vehiclelist = [ "Trooper", "Tank", "Aircraft", "Miss Tank" ]
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
        self.screen_buffer.blit(self.planetmain_designer, (0, 49))

        if screenobj_planetmain.planet.colony == 1:
            # build icon
            buildicon_state = screenobj_planetmain.animstates["builddemolish"].currframe and screenobj_planetmain.build_mode
            self.screen_buffer.blit(self.planetmain_buildicon[buildicon_state], (0, 1 + 49))
            # demolish icon
            demolishicon_state = screenobj_planetmain.animstates["builddemolish"].currframe and screenobj_planetmain.demolish_mode
            self.screen_buffer.blit(self.planetmain_demolishicon[demolishicon_state], (45, 1 + 49))
            # building - invention up
            self.screen_buffer.blit(self.planetmain_arrowup[int(screenobj_planetmain.selected_building_is_first)], (0, 15 + 49))
            # building - invention down
            self.screen_buffer.blit(self.planetmain_arrowdown[int(screenobj_planetmain.selected_building_is_last)], (0, 48 + 49))
            # building on surface illustration
            self.screen_buffer.blit(self.render_building(screenobj_planetmain.planet, self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]), (12, 15 + 49))
            # building name
            yellow_text_building_name = self.render_text(
                                            self.gamedata_static["buildings_info"][screenobj_planetmain.selected_building_type]["name"],
                                            textcolor = 1)
            self.screen_buffer.blit(yellow_text_building_name, (3, 81 + 49))

            # Invention Info mode (cannot be in this mode if there is no colony anyway)
            if screenobj_planetmain.screenmode_buildinginfo:
                self.screen_buffer.blit(yellow_text_building_name, (117, 59))
                statustext_offset_y = 70

                # building was selected on the map
                if screenobj_planetmain.screenmode_buildinginfo_specific:

                    curr_bldg = screenobj_planetmain.selected_building_on_map
                    self.screen_buffer.blit(self.render_text(f"Status     : {['Passive','Active'][curr_bldg.active]}", textcolor = 2), (98, statustext_offset_y))
                    if curr_bldg.building_data["building_typegroup?"] in [1, 8]:  # power plant/commandcentre
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Production : {curr_bldg.production} kwh", textcolor = 2), (98, statustext_offset_y))
                    if curr_bldg.workers != 0:
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Workers    : {curr_bldg.workers}/{curr_bldg.building_data['workers']}", textcolor = 2), (98, statustext_offset_y))
                    if curr_bldg.energy_use != 0:
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Energy     : {curr_bldg.energy_use} kwh", textcolor = 2), (98, statustext_offset_y))
                    statustext_offset_y += 9
                    self.screen_buffer.blit(self.render_text(f"Working    : {curr_bldg.working}%", textcolor = 2), (98, statustext_offset_y))
                    statustext_offset_y += 9
                    self.screen_buffer.blit(self.render_text(f"Performace : {curr_bldg.performance}%", textcolor = 2), (98, statustext_offset_y))

                else:  # general building info

                    bldg_info = screenobj_planetmain.selected_building_typeinfo
                    self.screen_buffer.blit(self.render_text(f"Cost       : {bldg_info['price']}", textcolor = 2), (98, statustext_offset_y))
                    if bldg_info["building_typegroup?"] in [1, 8]:  # power plant/commandcentre
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Production : {bldg_info['production']} kwh", textcolor = 2), (98, statustext_offset_y))
                    elif bldg_info["building_typegroup?"] in [2, 9]:  # mine / miner station
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text("Production : mine", textcolor = 2), (98, statustext_offset_y))
                    if bldg_info['workers'] != 0:
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Workers    : {bldg_info['workers']}", textcolor = 2), (98, statustext_offset_y))
                    if bldg_info['power_consumption'] != 0:
                        statustext_offset_y += 9
                        self.screen_buffer.blit(self.render_text(f"Energy     : {bldg_info['power_consumption']} kwh", textcolor = 2), (98, statustext_offset_y))

                self.screen_buffer.blit(self.planetmain_horiz_lines[0], (226,  54))
                self.screen_buffer.blit(self.planetmain_horiz_lines[1], (226, 124))
                self.screen_buffer.blit(self.planetmain_vert_lines[0],  (226,  56))
                self.screen_buffer.blit(self.planetmain_vert_lines[1],  (314,  56))

                self.screen_buffer.blit(self.planetmain_horiz_lines[2], ( 94, 127))
                self.screen_buffer.blit(self.planetmain_horiz_lines[3], (205, 127))
                self.screen_buffer.blit(self.planetmain_horiz_lines[4], ( 94, 194))
                self.screen_buffer.blit(self.planetmain_horiz_lines[5], (205, 194))
                self.screen_buffer.blit(self.planetmain_vert_lines[2],  ( 94, 129))
                self.screen_buffer.blit(self.planetmain_vert_lines[3],  (314, 129))

                self.screen_buffer.blit(self.planetmain_epulet_illust[screenobj_planetmain.selected_building_type - 1], (228, 56))

                selected_building_description = self.gamedata_static["buildings_desc"][screenobj_planetmain.selected_building_type-1]
                self.screen_buffer.blit(self.render_text(selected_building_description[0], textcolor = 2), (100, 134))
                for blgd_desc_index in range(len(selected_building_description)-1):
                    self.screen_buffer.blit(self.render_text(selected_building_description[blgd_desc_index + 1], textcolor = 1), (100, 148 + blgd_desc_index*9))

        if not screenobj_planetmain.screenmode_buildinginfo:  # Terrain mode
            # surface map
            planet_surface = self.render_surface_with_buildings(screenobj_planetmain.planet, screenobj_planetmain.animstates["surface"].currframe)
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


    # mine
    def render_mine(self, screenobj_mine):

        self.screen_buffer.blit(self.render_menu(screenobj_mine.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_mine.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["MINER"], (0, 49))

        # mineral production
        mineral_no = 0
        for mineral in screenobj_mine.mineral_production.keys():
            mineral_production = screenobj_mine.mineral_production[mineral]
            mineral_stock = screenobj_mine.mineral_storage[mineral]
            if mineral_production == 0:
                mineral_production_string = ' -'
            elif mineral_production == -1:
                mineral_production_string = '--'
            else:
                mineral_production_string = f"{mineral_production:2}"

            mineral_stock_string = f"{mineral_stock:6}"

            yellow_text_mineral_prod = self.render_text(mineral_production_string, textcolor = 1)
            yellow_text_mineral_stock = self.render_text(mineral_stock_string, textcolor = 1)
            self.screen_buffer.blit(yellow_text_mineral_prod, (113, 57 + 8 * mineral_no))
            self.screen_buffer.blit(yellow_text_mineral_stock, (59, 57 + 8 * mineral_no))
            mineral_no += 1

        # number of mines
        self.screen_buffer.blit(self.mine_szamok["kicsi"][screenobj_mine.num_of_mines // 10], (113, 113))
        self.screen_buffer.blit(self.mine_szamok["kicsi"][screenobj_mine.num_of_mines % 10], (126, 113))

        # number of active droids
        self.screen_buffer.blit(self.mine_szamok["nagy"][screenobj_mine.num_of_droids_active], (34, 144))

        # number of droids in stock
        self.screen_buffer.blit(self.mine_szamok["kozepes"][screenobj_mine.num_of_droids_stock // 10], (113, 144))
        self.screen_buffer.blit(self.mine_szamok["kozepes"][screenobj_mine.num_of_droids_stock % 10], (129, 144))

        return self.screen_buffer


    # messages
    def render_messages(self, screenobj_messages):

        self.screen_buffer.blit(self.render_menu(screenobj_messages.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_messages.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["UZENET"], (0, 49))

        # messages
        for msg_no in range(len(screenobj_messages.messages)):
            msgbitmap = self.render_text(screenobj_messages.messages[msg_no][0], textcolor = screenobj_messages.messages[msg_no][1])
            self.screen_buffer.blit(msgbitmap, (10, 57 + msg_no * 9))

        return self.screen_buffer


    # space local
    def render_spacelocal(self, screenobj_spacelocal):

        self.screen_buffer.blit(self.render_menu(screenobj_spacelocal.menu_info), (0, 0))
        self.screen_buffer.blit(self.render_infobar(screenobj_spacelocal.menu_info), (0, 32))

        # main pic
        self.screen_buffer.blit(self.PICs["KOCSMA"], (0, 49))

        self.__render_anims_helper(self.kocsma_anims, screenobj_spacelocal.animstates, self.kocsma_anims_pasteposes, self.screen_buffer)

        # kocsmatoltelekek
        ##################

        for kocsmatoltelek in self.kocsmatoltelekek_pasteposes.keys():
            self.screen_buffer.blit(self.kocsmatoltelekek[kocsmatoltelek], self.kocsmatoltelekek_pasteposes[kocsmatoltelek])


        return self.screen_buffer

