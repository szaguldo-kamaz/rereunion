# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_commanders(screen):

    def __init__(self, gamedata_static, gamedata_dynamic):

        self.screentype = "commanders"
        self.all_sfx    = [ "BACK", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPE", "WELCOME" ]

        self.menu_icons = [ "BACK TO M.SCREEN", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS", "HIRE MAN" ]
        self.menu_text  = [ "BACK TO M.SCREEN", "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS", "HIRE MAN" ]
        self.menu_sfx   = [ "BACK", None, "BUILDERS", "FIGHTERS", "DEVELOPE", "WELCOME" ]
        super().__init__(gamedata_dynamic, [ self.menu_icons, self.menu_text, self.menu_sfx ])

        self.gamedata_static = gamedata_static

        self.anim_exists = False

        self.commander_names = gamedata_static["commander_names"]
        self.commandertypes = [ "PILOTS", "BUILDERS", "FIGHTERS", "DEVELOPERS" ]
        self.name_to_idno_map = dict(zip(self.commandertypes, range(len(self.commandertypes))))
        self.shown_commander_type = 'PILOTS'
        self.shown_commander_type_id = 0
        self.selected_commander_no = None
        self.commander_says = None
        self.canbehired = None
        self.selected_commander_level = None
        self.hired_commander_level = None


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        [ menuaction, _ ] = self.get_action()
        if menuaction != None:

            if menuaction in self.commandertypes:
                if self.shown_commander_type != menuaction:
                    self.shown_commander_type = menuaction
                    self.shown_commander_type_id = self.name_to_idno_map[self.shown_commander_type]
                    self.commander_says = None
                    self.selected_commander_no = None
                    self.canbehired = False
                    self.menu_sfx = self.all_sfx[:]
                    self.menu_sfx[self.shown_commander_type_id + 1] = None
                    self.define_menu([ self.menu_icons, self.menu_text, self.menu_sfx ])
                    self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)
                    self.sfx_to_play = self.all_sfx[self.shown_commander_type_id + 1]

            elif menuaction == "HIRE MAN":

                if self.canbehired:
                    choosen_commander_salary = self.gamedata_static["commander_salaries"][self.shown_commander_type_id][self.selected_commander_no]
                    if choosen_commander_salary <= self.gamedata_dynamic["money"]:
                        #hire man
                        self.gamedata_dynamic["money"] -= choosen_commander_salary
                        self.gamedata_dynamic["commanders"][self.shown_commander_type_id] = self.selected_commander_no + 1
                        self.hired_commander_level = self.gamedata_dynamic["commanders"][self.shown_commander_type_id]

                        if self.shown_commander_type_id == 3:
                            self.gamedata_dynamic['developer_skills'] = self.gamedata_dynamic['developers_skills'][self.selected_commander_no]
                        else:
                            self.gamedata_dynamic['commander_level'][self.shown_commander_type_id] = self.gamedata_dynamic['commanders_levels'][self.shown_commander_type_id][self.selected_commander_no]

                        self.canbehired = False
                        self.commander_says = [ self.gamedata_static["commander_hire_txt"]["ok"] ]
                        self.sfx_to_play = "WELCOME"
                    else:
                        self.commander_says = [ self.gamedata_static["commander_hire_txt"]["nomoney"] ]
                        self.sfx_to_play = "HIBA"

                elif self.selected_commander_no == None:
                    self.sfx_to_play = "X"

                else:
                    # we cannot get here if there's no commander selected, so ok to use these vars
                    if self.selected_commander_level < self.hired_commander_level:
                        self.commander_says = [ self.gamedata_static["commander_hire_txt"]["noskill"] ]
                    elif self.selected_commander_level == self.hired_commander_level:
                        self.commander_says = [ self.gamedata_static["commander_hire_txt"]["already"] ]
                    else:
                        print(f"Unexpected state in screen_commanders ({self.selected_commander_level}:{self.hired_commander_level:})")
                        exit(1)

                    self.sfx_to_play = "HIBA"

            else:
                self.action = menuaction

        self.current_commanders = gamedata_dynamic["commanders"]

        # p b f d
        mouse_over_commander_no = None

        # Level 1-2-3 commander
        if   49 <= mouse_pos[1] <= 49+110 and   4 <= mouse_pos[0] <= 104:
            mouse_over_commander_no = 0
        elif 49 <= mouse_pos[1] <= 49+110 and 109 <= mouse_pos[0] <= 209:
            mouse_over_commander_no = 1
        elif 49 <= mouse_pos[1] <= 49+110 and 215 <= mouse_pos[0] <= 315:
            mouse_over_commander_no = 2

        if mouse_over_commander_no != None:
            self.menu_info["actiontext"] = self.commander_names[self.shown_commander_type_id][mouse_over_commander_no]
            if mouse_buttonevent[0]:  # mouse button pressed
                self.selected_commander_no = mouse_over_commander_no
                self.commander_says = self.gamedata_static["commanders_desc"][self.shown_commander_type_id*3 + self.selected_commander_no][:2]
                self.selected_commander_level = self.selected_commander_no + 1
                self.hired_commander_level = self.gamedata_dynamic["commanders"][self.shown_commander_type_id]

                if self.selected_commander_level == self.hired_commander_level:
                    if self.shown_commander_type_id == 3:
                        sk = self.gamedata_dynamic['developer_skills']
                        self.commander_says.append(f"Level:  Math: {sk[0]}  Physics: {sk[1]}  Elect: {sk[2]}  A.Int: {sk[3]}")
                    else:
                        sl = self.gamedata_dynamic['commander_level'][self.shown_commander_type_id]
                        self.commander_says.append(f"My scholarly level: {sl:3}")
                    self.commander_says.append("I work for you")
                    self.canbehired = False

                else:
                    if self.shown_commander_type_id == 3:
                        sk = self.gamedata_dynamic['developers_skills'][self.selected_commander_no]
                        self.commander_says.append(f"Level:  Math: {sk[0]}  Physics: {sk[1]}  Elect: {sk[2]}  A.Int: {sk[3]}")
                    else:
                        sl = self.gamedata_dynamic['commanders_levels'][self.shown_commander_type_id][mouse_over_commander_no]
                        self.commander_says.append(f"My scholarly level: {sl:3}")

                    if self.selected_commander_level < self.hired_commander_level:
                        self.commander_says.append("I'm no better than your advisor")
                        self.canbehired = False
                    else:  # Salary
                        self.commander_says.append(self.gamedata_static["commanders_desc"][self.shown_commander_type_id*3 + self.selected_commander_no][2])
                        self.canbehired = True
