# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#

import pygame
from io import BytesIO


class ReReSFX:

    smpfile_names = [
            "SOUND/ABORT.SMP",    "SOUND/ADDROID.SMP",  "SOUND/ADDSTAT.SMP",  "SOUND/ATTACK.SMP",   "SOUND/ATTENTIO.SMP",
            "SOUND/BACK.SMP",     "SOUND/BASEEFF.SMP",  "SOUND/BUILDCOL.SMP", "SOUND/BUILDERS.SMP", "SOUND/BUILDIN.SMP",
            "SOUND/BUILD.SMP",    "SOUND/BUY.SMP",      "SOUND/CANCEL.SMP",   "SOUND/CHANGE.SMP",   "SOUND/CLICK-OK.SMP",
            "SOUND/COMMANDE.SMP", "SOUND/CONTROLL.SMP", "SOUND/CPANEL.SMP",   "SOUND/CREDITS.SMP",  "SOUND/DESIGNAB.SMP",
            "SOUND/DESIGNRE.SMP", "SOUND/DESTRUCT.SMP", "SOUND/DEVELOPE.SMP", "SOUND/DISK.SMP",     "SOUND/DOOR1.SMP",
            "SOUND/DOOR2.SMP",    "SOUND/DOOR3.SMP",    "SOUND/ENDBATTL.SMP", "SOUND/FIGHTERS.SMP", "SOUND/GROUPDIS.SMP",
            "SOUND/GROUPNEW.SMP", "SOUND/GROUP.SMP",    "SOUND/HIBA.SMP",     "SOUND/HIPER.SMP",    "SOUND/HOLO.SMP",
            "SOUND/ICON.SMP",     "SOUND/KIIRO.SMP",    "SOUND/LANDING.SMP",  "SOUND/LAUNCH.SMP",   "SOUND/LOAD.SMP",
            "SOUND/LOCAL1.SMP",   "SOUND/LOCAL2.SMP",   "SOUND/LOCAL3.SMP",   "SOUND/LOCAL4.SMP",   "SOUND/LOCAL5.SMP",
            "SOUND/LOCAL6.SMP",   "SOUND/LOCAL7.SMP",   "SOUND/LOCAL8.SMP",   "SOUND/LOCAL.SMP",    "SOUND/MAINCPU.SMP",
            "SOUND/MESSAGE.SMP",  "SOUND/MESSAGES.SMP", "SOUND/MINERSTA.SMP", "SOUND/MINE.SMP",     "SOUND/MOON.SMP",
            "SOUND/MOVESHIP.SMP", "SOUND/NOTHANKS.SMP", "SOUND/OKAY.SMP",     "SOUND/PILOTS.SMP",   "SOUND/PLALIEN.SMP",
            "SOUND/PLANETFO.SMP", "SOUND/PLANETIN.SMP", "SOUND/PLANET.SMP",   "SOUND/PLUSEFUL.SMP", "SOUND/PLYOUR.SMP",
            "SOUND/PRODUCTI.SMP", "SOUND/RESEARCH.SMP", "SOUND/RETREAT.SMP",  "SOUND/SAT1.SMP",     "SOUND/SAT2.SMP",
            "SOUND/SAT3.SMP",     "SOUND/SAT4.SMP",     "SOUND/SATROBB1.SMP", "SOUND/SATROBB2.SMP", "SOUND/SATROBB3.SMP",
            "SOUND/SAVE.SMP",     "SOUND/SELECT1.SMP",  "SOUND/SELECT2.SMP",  "SOUND/SELECT3.SMP",  "SOUND/SELECT.SMP",
            "SOUND/STARMAP.SMP",  "SOUND/STARTDES.SMP", "SOUND/SURFACE.SMP",  "SOUND/TALK.SMP",     "SOUND/TAXDEC.SMP",
            "SOUND/TAXINC.SMP",   "SOUND/TRACTOR.SMP",  "SOUND/TRANSFER.SMP", "SOUND/UNITADD.SMP",  "SOUND/WELCOME.SMP",
            "SOUND/X.SMP",        "SOUND/ZOOMOUT.SMP",

            "SOUND2/WARSND1.SMP",  "SOUND2/WARSND2.SMP",  "SOUND2/WARSND3.SMP",  "SOUND2/WARSND4.SMP",  "SOUND2/WARSND5.SMP",
            "SOUND2/WARSND6.SMP",  "SOUND2/WARSND7.SMP",  "SOUND2/WARSND8.SMP",  "SOUND2/WARSND9.SMP",  "SOUND2/WARSND10.SMP",
            "SOUND2/WARSND11.SMP", "SOUND2/WARSND12.SMP", "SOUND2/WARSND13.SMP", "SOUND2/WARSND14.SMP", "SOUND2/WARSND15.SMP",
            "SOUND2/WARSND16.SMP", "SOUND2/WARSND17.SMP", "SOUND2/WARSND18.SMP", "SOUND2/WARSND19.SMP", "SOUND2/WARSND20.SMP",
            "SOUND2/WARSND21.SMP", "SOUND2/WARSND22.SMP", "SOUND2/WARSND23.SMP", "SOUND2/WARSND24.SMP", "SOUND2/WARSND25.SMP",
            "SOUND2/WARSND26.SMP", "SOUND2/WARSND27.SMP", "SOUND2/WARSND28.SMP", "SOUND2/WARSND29.SMP", "SOUND2/WARSND30.SMP",
            "SOUND2/WARSND31.SMP", "SOUND2/WARSND32.SMP", "SOUND2/WARSND33.SMP", "SOUND2/WARSND34.SMP", "SOUND2/WARSND35.SMP",
            "SOUND2/WARSND36.SMP", "SOUND2/WARSND37.SMP", "SOUND2/WARSND38.SMP", "SOUND2/WARSND39.SMP", "SOUND2/WARSND40.SMP",
            "SOUND2/WARSND41.SMP", "SOUND2/WARSND42.SMP", "SOUND2/WARSND43.SMP", "SOUND2/WARSND44.SMP", "SOUND2/WARSND45.SMP",

            "SOUND3/GRSND1.SMP",  "SOUND3/GRSND2.SMP",  "SOUND3/GRSND3.SMP",  "SOUND3/GRSND4.SMP",  "SOUND3/GRSND5.SMP",
            "SOUND3/GRSND6.SMP",  "SOUND3/GRSND7.SMP",  "SOUND3/GRSND8.SMP",  "SOUND3/GRSND9.SMP",  "SOUND3/GRSND10.SMP",
            "SOUND3/GRSND11.SMP", "SOUND3/GRSND20.SMP", "SOUND3/GRSND21.SMP", "SOUND3/GRSND22.SMP", "SOUND3/GRSND30.SMP",
            "SOUND3/GRSND31.SMP", "SOUND3/GRSND32.SMP"

        ]

    def __init__(self):

        voc_head = b'Creative Voice File\x1a\x1a\x00\n\x01)\x11'

        self.effects = {}
        for smpfile_name in self.smpfile_names:
            smpfile = open(smpfile_name, "rb")
            smpdata = smpfile.read()
            smpfile.close()
            self.effects[smpfile_name.split('.')[0].split('/')[1]] = pygame.mixer.Sound(BytesIO(voc_head + smpdata))

#        # "SHIP" is recycled from "MOVESHIP"
#        smpfile = open("SOUND/MOVESHIP.SMP", "rb")
#        # 12270 - 4806 + 4 = 0x001d2c
#        smpheader = bytes([ 0x01, 0x2c, 0x1d, 0x00, 0xad, 0x00 ])
#        smpfile.seek(4806)
#        smpdata = smpfile.read()
#        smpfile.close()
#        self.effects["SHIP"] = pygame.mixer.Sound(BytesIO(voc_head + smpheader + smpdata))

        self.effects["SHIP"] = self.effects["BASEEFF"]


    def play_effect(self, effectname):
        self.effects[effectname].play()


    def stop(self):
        pygame.mixer.stop()

