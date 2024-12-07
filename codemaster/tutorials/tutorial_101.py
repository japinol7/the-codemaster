"""Module tutorial_101."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    ClockTimerA,
    ComputerA,
    FilesDiskB,
    InvisibleHolderA,
    LifeRecoveryA,
    )
from codemaster.models.actors.npcs import (
    SkullYellow,
    )
from codemaster.models.actors.player import (
    PL_LIVES_DEFAULT,
    )
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.actors.text_msgs.text_msgs import TextMsgActorTop
from suiteoftests.config.constants import CLOCK_TIMER_IN_SECS
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
        self._init_clock_timer(time_in_secs=3)

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
        elif self.current_stat == 'kill_skull' \
                and not self.level.get_npcs_filtered_by_actor_type(ActorType.SKULL_YELLOW):
            self.lesson_last()

    def _init_clock_timer(self, time_in_secs=CLOCK_TIMER_IN_SECS):
        self.clock_timer = ClockTimerA(
            0, 26,
            self.game, time_in_secs,
            x_centered=False, y_on_top=False,
            owner=self.actor_tutorial_msg_holder)
        self.clock_timer.clock.trigger_method = self.lesson_get_a_battery
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
            "I have added a battery,\ntry to get it.")

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
            "Great!\n"
            "When you get a battery you get some XP,\n"
            "as you can see on the left side of the score bar.\n"
            "I have added a life recovery,\ntry to get it.")

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
            "Great!\n"
            "You can see that you got on more life \n"
            "on the left side of the score bar.\n"
            "I have added some bullet cartridges,\n"
            "try to get them.")

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
            "Great!\n"
            "You can see that you got some bullets \n"
            "on the left side of the score bar.\n"
            "I have added one files disk B,\n"
            "try to get it.")

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
            "Great!\n"
            "You can see that you got one files disk B \n"
            "on the right side of the score bar.\n"
            "I have added a computer.\nPress [r],\n"
            "on the computer to decrypt your file messages.")

        self.current_stat = 'computer'
        x = 2070 + self.level.world_shift
        y = 245 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            ComputerA(x, y, self.game),
            ])

    def lesson_read_msg(self):
        self._create_tutorial_msg_actor(
            "Great!\n"
            "Now, read the decrypted message from the Pause screen:\n"
            " 1. Press [Ctrl + p]\n"
            " 2. Press button [Info Files]\n"
            " 3. Read the message\n"
            " 4. Press [Ctrl + p] to leave the Pause screen.")

        self.current_stat = 'read_msg'

    def lesson_kill_skull_by_shooting(self):
        self._create_tutorial_msg_actor(
            "Great!\n"
            "You can shoot bullets pressing these keys:\n"
            "[u],  [i],  [j],  [k]\n"
            "Bullets are a limited commodity\n"
            "and you must spent power points to shoot them,\n"
            "I have added a Skull npc, try to Kill him.\n"
            "Don't get too close or he will kill you.")

        self.current_stat = 'kill_skull'
        x = 1560 + self.level.world_shift
        y = 290 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            SkullYellow(x, y, self.game),
            ])

    def lesson_kill_skull(self):
        self._create_tutorial_msg_actor(
            "Great!\n"
            "I have added a Skull npc, try to Kill him.\n"
            "Don't get too close or he will kill you.")

        self.current_stat = 'kill_skull'
        x = 1500 + self.level.world_shift
        y = 290 + self.level.get_scroll_shift_top_delta()
        self.level.add_actors([
            SkullYellow(x, y, self.game),
            ])

    def lesson_last(self):
        self._create_tutorial_msg_actor(
            "Great!\n"
            "")
