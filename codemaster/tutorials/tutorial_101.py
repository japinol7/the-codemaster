"""Module tutorial_101."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DIRECTION_LEFT,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    ClockA,
    ClockTimerA,
    ComputerA,
    FilesDiskB,
    InvisibleHolderA,
    LifeRecoveryA,
    PotionPower,
    PotionHealth,
    )
from codemaster.models.actors.npcs import (
    SkullYellow,
    SkullRed,
    TerminatorEyeYellow,
    )
from codemaster.models.actors.player import (
    PL_LIVES_DEFAULT,
    )
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.actors.text_msgs.text_msgs import TextMsgActorTop
from codemaster.tools.logger.logger import log


class Tutorial101:

    def __init__(self, level, game):
        self.id = 101
        self.game = game
        self.player = game.player
        self.level = level
        self.clock_timer = None
        self.current_stat = ''
        self.actor_tutorial_msg_holder = None

        level.door_previous_pos_player = level.player_start_pos_left
        level.door_previous_pos_world = level.world_start_pos_left

    def update_pc_enter_level(self):
        log.info("Initialize tutorial level")

        self.game.ui_manager.ui_ingame.items['save_game_button'].disable()
        self.game.ui_manager.ui_ingame.items['watch_cutscene'].disable()

        # Update PC stats for tutorial
        self.player.stats['lives'] -= 1
        self.player.stats.update({
            'bullets_t01': 0,
            'bullets_t02': 0,
            'bullets_t03': 0,
            'bullets_t04': 0,
            })

        # Add an actor that will hold tutorial msgs
        self.actor_tutorial_msg_holder = InvisibleHolderA(5, 390, self.game)
        self.level.add_actors([self.actor_tutorial_msg_holder])

        self.player.create_starting_game_msg(self.game)
        self._create_clock_timer_msg(time_in_secs=3, trigger=self.lesson_get_a_battery)

    def update(self):
        # Update the tutorial states only now and then
        if self.game.update_state_counter != 4:
            return

        if self.current_stat == 'batteries' and self.player.stats['batteries'] == 1:
            self.clock_timer.die_hard()
            self.lesson_get_a_life_recovery()
        elif self.current_stat == 'lives' \
                and self.player.stats['lives'] == PL_LIVES_DEFAULT:
            self.lesson_get_some_cartridges()
        elif self.current_stat == 'cartridges' \
                and self.player.stats['bullets_t01'] > 0 \
                and self.player.stats['bullets_t02'] > 0 \
                and self.player.stats['bullets_t03'] > 0 \
                and self.player.stats['bullets_t04'] > 0:
            self.lesson_get_one_files_disk_b()
        elif self.current_stat == 'files_disks' \
                and self.player.stats['files_disks'] > 0:
            self.lesson_use_computer_to_decrypt_msg()
        elif self.current_stat == 'computer' \
                and self.player.stats['files_disks_stock'] \
                and not FilesDiskB.is_msg_encrypted(
                    self.player.stats['files_disks_stock'][0].msg_id, self.game):
            self.lesson_read_msg()
        elif self.current_stat == 'read_msg' \
                and self.player.stats['files_disks_stock'] \
                and FilesDiskB.has_msg_been_read(
                    self.player.stats['files_disks_stock'][0].msg_id, self.game):
            self.lesson_kill_skull_by_shooting()
        elif self.current_stat == 'kill_skull_by_shooting' \
                and not self.level.get_npcs_filtered_by_actor_type(ActorType.SKULL_YELLOW):
            self.lesson_kill_skull_by_casting_spells()
        elif self.current_stat == 'kill_skull_by_casting_spells' \
                and not self.level.get_npcs_filtered_by_actor_type(ActorType.SKULL_RED):
            self.lesson_drink_power_potion()
        elif self.current_stat == 'drink_power_potion' \
                and not self.level.get_items_filtered_by_actor_type(ActorType.POTION_POWER) \
                and self.player.power >= self.player.power_total:
            self.lesson_kill_terminator_eye_by_casting_spells()
        elif self.current_stat == 'kill_terminator_eye_by_casting_spells' \
                and not self.level.get_npcs_filtered_by_actor_type(ActorType.TERMINATOR_EYE_YELLOW):
            self.lesson_drink_health_potion()
        elif self.current_stat == 'drink_health_potion' \
                and not self.level.get_items_filtered_by_actor_type(ActorType.POTION_HEALTH) \
                and self.player.health >= self.player.health_total:
            self.lesson_get_clock()
        elif self.current_stat == 'get_clock' \
                and not self.level.get_items_filtered_by_actor_type(ActorType.CLOCK_A):
            self.lesson_get_door_key()
        elif self.current_stat == 'get_door_key' \
                and not self.level.get_items_filtered_by_actor_type(ActorType.DOOR_KEY_BLUE):
            self.lesson_last()

    def _create_clock_timer_msg(self, time_in_secs=5, trigger=None):
        self.clock_timer = ClockTimerA(
            0, 26,
            self.game, time_in_secs,
            x_centered=False, y_on_top=False,
            owner=self.actor_tutorial_msg_holder)
        if trigger:
            self.clock_timer.clock.trigger_method = trigger
        self.game.active_sprites.add(self.clock_timer)
        self.clock_sprites = pg.sprite.Group()
        self.clock_sprites.add(self.clock_timer)

    def _create_tutorial_msg_actor(self, msg, time_in_secs=6000):
        TextMsg.create(
            "Tutorial-Chan:\n"
            f"{msg}",
            game=self.game,
            owner=self.actor_tutorial_msg_holder,
            delta_x=0, delta_y=-30,
            time_in_secs=time_in_secs,
            msg_class=TextMsgActorTop)

    def lesson_get_a_battery(self):
        self.clock_timer.die_hard()
        self._create_tutorial_msg_actor(
            "Hi! My name is Tutorial-Chan. \n"
            "Nice to meet ya!\n"
            "Here are some basic control keys:\n"
            " > Press [a] / [d] to move left / right.\n"
            " > Press [w] to jump.\n"
            " > Press [F1] to open/close the help screen.\n"
            "I've added a battery. Try to collect it.")

        self.current_stat = 'batteries'
        self.level.add_actors([
            BatteryA(
                580 + self.level.world_shift,
                550 + self.level.get_scroll_shift_top_delta(),
                self.game
                ),
            ])

    def lesson_get_a_life_recovery(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "Collecting a battery grants you XP,\n"
            "which is displayed on the left side of the score bar.\n"
            "Remember that you can exit the tutorial and start the main game\n"
            "by getting the key, and unlocking and enter the door\n"
            "on the right of this level.\n"
            "I've added a life recovery item.\nTry to collect it.")

        self.current_stat = 'lives'
        self.level.add_actors([
            LifeRecoveryA(
                705 + self.level.world_shift,
                380 + self.level.get_scroll_shift_top_delta(),
                self.game
                ),
            ])

    def lesson_get_some_cartridges(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can see that you have got on more life \n"
            "on the left side of the score bar.\n"
            "I've added some bullet cartridges.\n"
            "Try to collect them.")

        self.current_stat = 'cartridges'
        x = 960 + self.level.world_shift
        y = 312 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            CartridgeGreen(x + 70, y, self.game),
            CartridgeBlue(x + 140, y, self.game),
            CartridgeYellow(x + 210, y, self.game),
            CartridgeRed(x + 280, y, self.game),
            ])

    def lesson_get_one_files_disk_b(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can see that you have got some bullets \n"
            "on the left side of the score bar.\n"
            "I've added one files disk B.\n"
            "Try to collect it.")

        self.current_stat = 'files_disks'
        x = 1560 + self.level.world_shift
        y = 312 + self.level.get_scroll_shift_top_delta()
        files_disk = FilesDiskB(x, y, self.game)
        self.level.add_actors([
            files_disk,
            ])
        files_disk.msg_id = 'B_09'

    def lesson_use_computer_to_decrypt_msg(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can see that you have got one files disk B \n"
            "on the right side of the score bar.\n"
            "I have added a computer.\n"
            "Press [r] on the computer\n"
            "to decrypt your file messages.")

        self.current_stat = 'computer'
        x = 2070 + self.level.world_shift
        y = 245 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            ComputerA(x, y, self.game),
            ])

    def lesson_read_msg(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "Now, read the decrypted message from the Pause screen:\n"
            " 1. Press [Ctrl + p]\n"
            " 2. Press button [Info Files]\n"
            " 3. Read the message\n"
            " 4. Press [Ctrl + p] to leave the Pause screen.")

        self.current_stat = 'read_msg'

    def lesson_kill_skull_by_shooting(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can shoot bullets pressing these keys:\n"
            "[u],  [i],  [j],  [k]\n"
            "Bullets are a limited commodity\n"
            "and you must spent power points to shoot them,\n"
            "I have added a Skull NPC, try to Kill him.\n"
            "Don't get too close or he will kill you.")

        self.current_stat = 'kill_skull_by_shooting'
        x = 1560 + self.level.world_shift
        y = 290 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            SkullYellow(x, y, self.game),
            ])

    def lesson_kill_skull_by_casting_spells(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "I have temporarily leveled you up one level,\n"
            "so you can cast magic and use energy shields.\n"
            "Press [m] to activate/deactivate magic capabilities.\n"
            "Press one of these keys to choose your next spell:\n"
            "[1], [2], [3], [4], [5].\n"
            "Then use the mouse to click on the NPC target.\n"
            "I've added a Skull NPC. Try to kill him using a spell.")

        self.player.stats.update({
            'bullets_t01': 0,
            'bullets_t02': 0,
            'bullets_t03': 0,
            'bullets_t04': 0,
            })
        self.player.level_up(msg_echo=False)
        self.player.choose_spell(3)
        for bullet in self.level.bullets:
            bullet.kill_hook()

        self.current_stat = 'kill_skull_by_casting_spells'
        x = 1500 + self.level.world_shift
        y = 290 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            SkullRed(x, y, self.game),
            ])

    def lesson_drink_power_potion(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can press [delete] to quick drink a power potion.\n"
            "You can also choose a potion to drink from the pause menu.\n"
            "I've added a power potion.\n"
            "Try to collect it and drink it.")

        self.current_stat = 'drink_power_potion'
        x = 2370 + self.level.world_shift
        y = 315 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            PotionPower(x, y, self.game, random_min=100, random_max=100),
            ])

    def lesson_kill_terminator_eye_by_casting_spells(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "Press [h] to activate/deactivate your energy shield.\n"
            "This energy shield can protect you from bullets.\n"
            "I have added a Terminator Eye NPC, try to Kill him.\n"
            "Use you shield and magic to fight him.")

        self.current_stat = 'kill_terminator_eye_by_casting_spells'
        self.player.switch_energy_shield()
        x = 2700 + self.level.world_shift
        y = 270 + self.level.get_scroll_shift_top_delta()
        terminator_eye = TerminatorEyeYellow(x, y, self.game)
        terminator_eye.direction = DIRECTION_LEFT
        self.level.add_actors([terminator_eye])

    def lesson_drink_health_potion(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can press [insert] to quick drink a health potion.\n"
            "You can also choose a potion to drink from the pause menu.\n"
            "I've added a health potion.\n"
            "Try to collect it and drink it.")

        self.current_stat = 'drink_health_potion'
        if self.player.health >= self.player.health_total:
            self.player.health = self.player.health_total - 5

        x = 2610 + self.level.world_shift
        y = 315 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            PotionHealth(x, y, self.game, random_min=100, random_max=100),
            ])

    def lesson_get_clock(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can find some clocks in the game.\n"
            "These clocks display a countdown over your avatar.\n"
            "They currently have no other effect,\n"
            "but aren't they cool?\n"
            "I've added a clock. Try to fetch it.")

        self.current_stat = 'get_clock'
        x = 2290 + self.level.world_shift
        y = 308 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            ClockA(x, y, self.game, time_in_secs=6),
            ])

    def lesson_get_door_key(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "Just one more thing; to beat this game demo you must:\n"
            " > Get all the batteries.\n"
            " > Get all the files disks.\n"
            " > Decrypt and read all the files disks that are not corrupted.\n"
            "Fetch the key located near the door.")

        if self.player.stats['door_keys_stock']:
            self._create_clock_timer_msg(time_in_secs=6, trigger=self.lesson_last)
            self.current_stat = 'lesson_last_alt'
        else:
            self.current_stat = 'get_door_key'

    def lesson_last(self):
        self._create_tutorial_msg_actor(
            "Great job!\n"
            "You can now exit the tutorial and start the main game.\n"
            "To do this, head to the door on the right side of this level.\n"
            "Press [r] at the door to unlock it using the key you fetched.\n"
            "Have a wonderful gaming time!\n"
            ";)")
