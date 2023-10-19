# ReReunion
#
# Author: David Vincze <vincze.david@webcode.hu>
#
# github.com/szaguldo-kamaz/rereunion
#


from rere_screen import screen


class screen_messages(screen):

    def __init__(self, gamedata_dynamic):

        self.screentype = "messages"

        menu_icons = [ "BACK TO M.SCREEN" ]
        menu_text  = [ "BACK TO M.SCREEN" ]
        menu_sfx   = [ "BACK" ]

        super().__init__(gamedata_dynamic, [ menu_icons, menu_text, menu_sfx ])

        self.anim_exists = False


    def update(self, gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent):

        self.update_menu(gamedata_dynamic, mouse_pos, mouse_buttonstate, mouse_buttonevent)

        self.messages = []
        for msg_no in range (gamedata_dynamic["message_count"]):
            msg = gamedata_dynamic["messages"][msg_no].decode('ascii')
            if msg.find('arrived to') != -1:
                msgtextcolor = 1
            else:
                msgtextcolor = 2
            self.messages.append([msg, msgtextcolor])
