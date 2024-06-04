from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Import your game loop and other functions
from src.lifesim_lib.translation import _
from src.lifesim_lib.const import *
from src.menus.main import main_menu
from src.menus.start import start_menu
from src.lifesim_lib.lifesim_lib import PlayerDied, yes_no, choice_input, clear_screen

class LifeSimApp(App):
    def build(self):
        root = BoxLayout()
        # Add your UI elements here

        # Create an instance of your player
        self.player = start_menu()
        self.player.print_traits()

        # Schedule the game loop
        Clock.schedule_once(self.game_loop, 0)

        return root

    def game_loop(self, dt):
        try:
            while True:
                try:
                    main_menu(self.player)
                except Exception as e:
                    if type(e) == PlayerDied:
                        raise
                    clear_screen()
                    print(_("An error has occurred"))
                    import traceback
                    message = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    print(message)
                    try:
                        with open("error.log", "w") as f:
                            f.write(message)
                        print(_("The above error message has been written to error.log"))
                    except:
                        pass
                    print(_("Please report this bug on Github"))
                    print("https://github.com/fungamer2-2/Life-Simulator1/issues/new?template=bug_report.md")
                    exit(1)
                else:
                    self.player.save_game()
        except PlayerDied:
            pass

        # Handle player's age and game continuation
        print(_("Age {age}").format(age=self.player.age))
        if self.player.children and yes_no(_("Would you like to continue as one of your children?")):
            names = [c.name for c in self.player.children]
            print(_("Which child would you like to continue as?"))
            choice = choice_input(*names)
            c = self.player.children[choice - 1]
            self.player.convert_child_to_player(c)
            self.player.save_game()
        elif yes_no(_("Would you like to start a new life?")):
            self.player = start_menu()
            self.player.print_traits()
        else:
            print(_("Thanks for playing!"))
            return  # Exit the game loop

        # Schedule the next iteration of the game loop
        Clock.schedule_once(self.game_loop, 1/60)  # 60 FPS example

if __name__ == '__main__':
    LifeSimApp().run()