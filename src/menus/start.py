from src.people.classes.player import Player
from src.people.classes.sibling import Sibling
from src.lifesim_lib.translation import _
from src.lifesim_lib.const import SAVE_PATH
import os, random, pickle
from random import randint
from src.lifesim_lib.lifesim_lib import *


def start_menu():
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    saves = get_save_files()
    if saves:
        choice = choice_input(_("Load Game"), _("New Game"))
        if choice == 1:
            players = get_saves(saves)
            choices = [p["name"] for p in players]
            choice = choice_input(*choices)
            d = players[choice - 1]
            return Player.load(d)
    choice = choice_input(_("Random Life"), _("Custom Life"))

    if choice == 2:
        print(_("Choose your gender:"))
        choice = choice_input(_("Male"), _("Female"))
        gender = Gender.Male if choice == 1 else Gender.Female
        first = input(_("Enter your first name (or leave blank for random): ")).strip()
        first = first or random_name(gender)
        last = input(_("Enter your last name (or leave blank for random): ")).strip()
        last = last or random_last_name()
        print()
        print()
        player = Player(first, last, gender)
        print(_("Would you like to Randomize or Customize your traits?"))
        choice = choice_input(_("Randomize"), _("Customize"))
        if choice == 1:
            player.randomize_traits()
        else:
            player.traits = {}
            all_traits = list(ALL_TRAITS_DICT)
            while True:
                clear_screen()
                print(_("Enter a number to select or deselect a trait"))
                print(_('Select "Done" when finished'))
                print()
                print(_("Traits:"))
                if player.traits:
                    print(player.get_traits_str())
                else:
                    print(_("None"))
                print()
                can_choose = lambda t: not any(
                    ALL_TRAITS_DICT[t].conflicts_with(other) for other in player.traits
                )
                options = [trait for trait in all_traits if can_choose(trait)]
                choices = list(
                    map(
                        lambda t: get_colored(t.name, t.get_color()),
                        map(ALL_TRAITS_DICT.__getitem__, options),
                    )
                )
                choices.append(_("Done"))
                choice = choice_input(*choices)
                if choice == len(choices):
                    if yes_no(_("Would you like to start with these traits?")):
                        break
                else:
                    trait = options[choice - 1]
                    if trait in player.traits:
                        del player.traits[trait]
                    else:
                        player.traits[trait] = ALL_TRAITS_DICT[trait]
            clear_screen()
        player.after_trait_select()
        return player
    else:
        player = Player()
    mother = player.parents["Mother"]
    father = player.parents["Father"]
    print(
        _("Your mother is {name}, age {age}.").format(name=mother.name, age=mother.age)
    )
    print(
        _("Your father is {name}, age {age}.").format(name=father.name, age=father.age)
    )
    sibling_age = randint(2, 10)
    if (
        mother.age >= randint(16, 20) + sibling_age
        and father.age >= randint(16, 18) + sibling_age
        and randint(1, 6) < 6
    ):
        whichlast = random.choice(
            (player.parents["Mother"].lastname, player.parents["Father"].lastname)
        )
        theirsmarts = round_stochastic((randint(0, 100) + player.smarts) / 2)
        theirlooks = round_stochastic((randint(0, 100) + player.looks) / 2)
        sibling = Sibling(
            whichlast, sibling_age, Gender.random(), theirsmarts, theirlooks
        )
        player.relations.append(sibling)
        print(
            _("You have a {siblingtype} named {name}, age {age}.").format(
                siblingtype=sibling.get_translated_type().lower(),
                name=sibling.name,
                age=sibling.age,
            )
        )
    player.randomize_traits()
    player.after_trait_select()
    return player
