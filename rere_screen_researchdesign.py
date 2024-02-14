# ReReunionc
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
        self.anim_states["vumeter"] = { "currframe" : 0, "frames" : 9, "currtick": 0, "ticks": 2, "loop" : 1, "backwards": False }
        self.anim_states["cdtray"]  = { "currframe" : 0, "frames" : 9, "currtick": 0, "ticks": 5, "loop" : 0, "backwards": False }

        self.developer_names = gamedata_static["commander_names"][3]
        self.reset(gamedata_dynamic)


    def reset(self, gamedata_dynamic):
        self.project_selected = None
        self.project_running = None
        self.project_selected_name = ''
        self.project_selected_status = ''
        self.project_selected_requiredskills = None
        self.project_selected_completionratio = None
        self.project_selected_requiredtime = None
        self.update(gamedata_dynamic, (0,0), [0,0,0], [0,0,0])


    def __map_states_to_icons(self, gamedata_dynamic):

        resstate_to_icon_map = [ -1, 1, 4, 3, 4, 0, 2 ]

#        resstate_to_icon_map = [ 0, 2, 5, 4, 5, 1, 3 ]
#            0 -> 0
#            1 -> 2
#            2 -> 5
#            3 -> 4
#            4 -> 5
#            5 -> 1
#            6 -> 3 TODO ?? # hyperdrive?
#            TODO 3  # development stalled ?

        iconstates = []
        for invention_no in range(1,36):
            iconstates.append(resstate_to_icon_map[gamedata_dynamic["inventions"][invention_no]["research_state"]])

            # research state 0 - unavailable (not shown)
            # research state 1 - tray with "?" CD
            # research state 2 - tray with "?" CD - in research
            # research state 3 - tray without CD
            # research state 4 - tray without CD - in research
            # research state 5 - done

        return iconstates


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.iconstates = self.__map_states_to_icons(gamedata_dynamic)

        if gamedata_dynamic["commanders"][3] > 0:
            self.computer_state = 1  # on
            self.developer_level = gamedata_dynamic["developer_level"]  # name, math, phys, elect, AI
            self.developer_name = self.developer_names[gamedata_dynamic["commanders"][3] - 1]
        else:
            self.computer_state = 0  # off

        # Inventions
        if (53 <= mouse_pos[1] <= 162) and (0 <= mouse_pos[0] <= 157):

            mouse_on_invmap_pos = ( int((mouse_pos[0] + 1)/32), int((mouse_pos[1] - 52)/16) )
            invention_no = mouse_on_invmap_pos[0] + mouse_on_invmap_pos[1] * 5 + 1

            if gamedata_dynamic["inventions"][invention_no]["research_state"] != 0:
                self.menu_info["actiontext"] = gamedata_dynamic["inventions"][invention_no]["name"]

                # Select invention from optical disc drive array
                if mouse_buttonevent[0] and mouse_buttonstate[0]:  # left mouse button was pressed
                    self.project_selected = gamedata_dynamic["inventions"][invention_no]
                    self.project_selected_name = self.project_selected["name"]
                    self.project_selected_requiredskills = list(map(str,self.project_selected["requiredskills"]))
#                    self.project_selected_requiredtime = self.project_selected["research_requiredtime"]
                    self.project_selected_completionratio = str(int(self.project_selected["research_remaining"] / 100))
                    if self.project_selected["research_state"] == 5:
                        self.project_selected_status = "Done"
                        self.project_selected_requiredskills = None
                        self.project_selected_completionratio = None
                        self.sfx_to_play = "DESIGNRE"
                    elif self.project_selected["research_state"] in [2, 4]:
                        self.project_selected_status = "Under analysis"
                    else:
                        self.project_selected_status = "Can be analysed"

