# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_researchdesign(screen):

    def __init__(self, gamedata_static, gamedata_dynamic):

        self.screentype = "researchdesign"

        menu_icons = [ "BACK TO M.SCREEN", "INFO-BUY" ]
        menu_text  = [ "BACK TO M.SCREEN", "INFO-BUY" ]
        menu_sfx   = [ "BACK", "PRODUCTI" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = True
        self.add_anim("spectrum",        9, 2, 1)
        self.add_anim("normaltrayclose", 9, 1, 0)
        self.add_anim("normaltrayopen",  9, 1, 0, backwards = True)
        self.add_anim("?starttrayclose", 9, 1, 0)
        self.add_anim("?starttrayopen",  9, 1, 0, backwards = True)
        self.add_anim("emptytrayclose",  9, 1, 0)
        self.add_anim("emptytrayopen",   9, 1, 0, backwards = True)

        self.developer_names = gamedata_static["commander_names"][3]
        self.reset(gamedata_dynamic)


    def reset(self, gamedata_dynamic):

        self.project_selected_cd_no = None
        self.project_selected = None
        self.project_running = None
        self.project_selected_name = ''
        self.project_selected_status = ''
        self.project_selected_requiredskills = None
        self.project_selected_completionratio = None
        self.project_selected_requiredtime = None
        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def __rearrange_researchstates(self, gamedata_dynamic):

        # research state 0 - unavailable (not shown)
        # research state 1 - tray with "?" CD
        # research state 2 - tray with "?" CD - in research
        # research state 3 - tray without CD
        # research state 4 - tray without CD - in research
        # research state 5 - done

        researchstates = []

        for invention_no in range(1,36):
            researchstates.append(gamedata_dynamic["inventions"][invention_no]["research_state"])

        return researchstates


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        if mouse_pos == None:
            if self.last_mouse_pos == None:
                mouse_pos = (0,0)
            else:
                mouse_pos = self.last_mouse_pos
        else:
            self.last_mouse_pos = mouse_pos

        if gamedata_dynamic["commanders"][3] > 0:
            self.computer_state = 1  # on
            self.developer_level = gamedata_dynamic["developer_level"]  # name, math, phys, elect, AI
            self.developer_name = self.developer_names[gamedata_dynamic["commanders"][3] - 1]
        else:
            self.computer_state = 0  # off
            self.developer_name = "No developer"
            self.developer_level = [ '-', '-', '-', '-' ]

        if self.waitingforanim != None:

            if self.animstates[self.waitingforanim].active == 2:

                self.animstates[self.waitingforanim].activate(0)

                if self.waitingforanim == "normaltrayclose":
                    self.waitingforanim = "normaltrayopen"
                    self.animstates["normaltrayopen"].activate(1)

                elif self.waitingforanim == "normaltrayopen":
                    self.waitingforanim = None

                elif self.waitingforanim == "?starttrayclose":
                    self.waitingforanim = None
                    self.project_selected["research_state"] = 2
                    self.project_selected_status = "Under development"

                elif self.waitingforanim == "?starttrayopen":
                    self.waitingforanim = None
                    self.project_selected_status = "Can be analysed"

                elif self.waitingforanim == "emptytrayclose":
                    self.waitingforanim = None
                    self.project_selected["research_state"] = 4
                    self.project_selected_status = "Under analysis"

                elif self.waitingforanim == "emptytrayopen":
                    self.waitingforanim = None
                    self.project_selected_status = "Can be analysed"

            mouse_buttonevent = [0,0,0]

        self.researchstates = self.__rearrange_researchstates(gamedata_dynamic)

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        # Inventions
        if (53 <= mouse_pos[1] <= 162) and (0 <= mouse_pos[0] <= 157):

            mouse_on_invmap_pos = ( int((mouse_pos[0] + 1)/32), int((mouse_pos[1] - 52)/16) )
            invention_no = mouse_on_invmap_pos[0] + mouse_on_invmap_pos[1] * 5 + 1

            if gamedata_dynamic["inventions"][invention_no]["research_state"] != 0:
                self.menu_info["actiontext"] = gamedata_dynamic["inventions"][invention_no]["name"]

                # Select invention from optical disc drive array
                if mouse_buttonevent[0] and mouse_buttonstate[0]:  # left mouse button was pressed
                    self.project_selected_cd_no = invention_no - 1
                    self.project_selected = gamedata_dynamic["inventions"][invention_no]
                    self.project_selected_name = self.project_selected["name"]
                    self.project_selected_requiredskills = list(map(str,self.project_selected["requiredskills"]))
                    self.project_selected_completionratio = str(int(self.project_selected["research_remaining"] / 100))

                    if self.project_selected["research_state"] == 5:
                        self.project_selected_status = "Done"
                        self.project_selected_requiredskills = None
                        self.project_selected_completionratio = None
                        self.waitingforanim = "normaltrayclose"
                        self.sfx_to_play = "DESIGNRE"

                    elif self.project_selected["research_state"] == 2:
                        self.project_selected["research_state"] = 1
                        self.waitingforanim = "?starttrayopen"
                        self.sfx_to_play = "DESIGNAB"

                    elif self.project_selected["research_state"] == 4:
                        self.project_selected["research_state"] = 3
                        self.waitingforanim = "emptytrayopen"
                        self.sfx_to_play = "DESIGNAB"

                    elif self.project_selected["research_state"] in [1, 3]:
                        self.project_selected_status = "Can be analysed"
                        if self.project_selected["research_state"] == 1:
                            self.waitingforanim = "?starttrayclose"
                        elif self.project_selected["research_state"] == 3:
                            self.waitingforanim = "emptytrayclose"
                        self.sfx_to_play = "STARTDES"

                    else:
                        print(f"ERR: Unknown research state {self.project_selected_name}/{self.project_selected['research_state']}! Should not happen!")
                        exit(1)

                    self.animstates[self.waitingforanim].activate(1)
