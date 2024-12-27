"""Module player."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
from datetime import datetime
from os import path
from random import randint

import pygame as pg

from codemaster.models.actors.actors import Actor
from codemaster.models.actors.items.files_disks import FilesDisk
from codemaster.tools.utils.colors import Color
from codemaster.models.actors.items import bullets
from codemaster.models.actors.items.bullets import Bullet
from codemaster.tools.logger.logger import log
from codemaster.config.settings import Settings
from codemaster.config.constants import (
    BITMAPS_FOLDER,
    BM_PC_PAC_FOLDER,
    SOUNDS_FOLDER,
    FILE_NAMES,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_RIP,
    NEAR_BOTTOM,
    MSG_PC_DURATION,
    MSG_PC_DUR_LONG,
    MSG_PC_DUR_SHORT,
    )
from codemaster import resources
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.items.platforms import MovingPlatform, SlidingBands
from codemaster.models.actors.items.bullets import BULLET_MAX_QTY
from codemaster.models.actors.actor_types import ActorType, ActorBaseType
from codemaster.models.actors.items import EnergyShieldA
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.actors.spells import (
    VortexOfDoomB,
    VortexOfDoomA,
    LightningBoltA,
    DoomBoltB,
    DoomBoltA,
    )

PL_X_SPEED = 6
PL_JUMP_SPEED = 11.5
PL_LIVES_DEFAULT = 5
PL_POWER_DEFAULT = 100
PL_HEALTH_DEFAULT = 100
PL_MAGIC_RESISTANCE = 70
PL_SPEED_DEFAULT = 8
PL_BULLETS_T01_DEFAULT = 140
PL_BULLETS_T02_DEFAULT = 75
PL_BULLETS_T03_DEFAULT = 24
PL_BULLETS_T04_DEFAULT = 8

PC_PAC_ID = 1
# PC types  (X, Y, width, height, id, type_en, type_name) of sprite
PC_PAC_01 = (1, 1, 54, 72, PC_PAC_ID, 'PC_Pac', 'Pac')


class Player(pg.sprite.Sprite):

    def file_name_im_get(self, folder, name, num):
        return path.join(folder, f"{FILE_NAMES[name][0]}_{num:02}.{FILE_NAMES[name][1]}")

    def file_name_im_rip_get(self):
        return path.join(BITMAPS_FOLDER, f"{FILE_NAMES['im_pj_rip'][0]}.{FILE_NAMES['im_pj_rip'][1]}")

    def file_name_sound_get(self, name_id):
        return path.join(SOUNDS_FOLDER, f"{FILE_NAMES[name_id][0]}.{FILE_NAMES[name_id][1]}")

    def __init__(self, name, game):
        super().__init__()
        self.name = name
        self.game = game
        self.is_a_player = True
        self.id = "player"
        self.base_type = ActorBaseType.PC
        self.type = ActorType.PLAYER
        self.health_total = PL_HEALTH_DEFAULT
        self.power_total = PL_POWER_DEFAULT
        self.sprite_sheet_data_id = PC_PAC_ID
        self.is_alive = True
        self.color = 1
        self.change_x = 0
        self.change_y = 0
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.rip_frames = []
        self.direction = DIRECTION_RIGHT
        self.debug = False
        self.start_time = False
        self.images_sprite_no = 6
        self.frame = 0
        self.rip_seconds = 0
        self.invulnerable = False
        self.bullet_start_position_delta_x = 0
        self.is_energy_shield_activated = False
        self.target_of_spells_count = Counter()
        self.auto_spell_target = None
        self.stats = {
            'level': 1,
            'levels_visited': set(),
            'score': 0,
            'lives': PL_LIVES_DEFAULT,
            'power': PL_POWER_DEFAULT,
            'health': PL_HEALTH_DEFAULT,
            'magic_resistance': PL_MAGIC_RESISTANCE,
            'magic_resistance_base': PL_MAGIC_RESISTANCE,
            'speed': PL_SPEED_DEFAULT,
            'magic_attack': None,
            'batteries': 0,
            'files_disks': 0,
            'files_disks_type': {'D': 0, 'C': 0, 'B': 0, 'A': 0},
            'bullets_t01': PL_BULLETS_T01_DEFAULT,
            'bullets_t01_shot': 0,
            'bullets_t02': PL_BULLETS_T02_DEFAULT,
            'bullets_t02_shot': 0,
            'bullets_t03': PL_BULLETS_T03_DEFAULT,
            'bullets_t03_shot': 0,
            'bullets_t04': PL_BULLETS_T04_DEFAULT,
            'bullets_t04_shot': 0,
            'potions_power': [],
            'potions_health': [],
            ActorType.POTION_POWER.name: 0,
            ActorType.POTION_HEALTH.name: 0,
            ActorType.FILES_DISK_D.name: 0,
            ActorType.FILES_DISK_C.name: 0,
            ActorType.FILES_DISK_B.name: 0,
            ActorType.FILES_DISK_A.name: 0,
            'apples': 0,
            'apples_stock': [],
            'apples_type': {'G': 0, 'Y': 0, 'R': 0},
            ActorType.APPLE_GREEN.name: 0,
            ActorType.APPLE_YELLOW.name: 0,
            ActorType.APPLE_RED.name: 0,
            'door_keys': 0,
            'door_keys_stock': [],
            'door_keys_type': {'G': 0, 'B': 0, 'A': 0, 'Y': 0, 'R': 0, 'M': 0},
            ActorType.DOOR_KEY_GREEN.name: 0,
            ActorType.DOOR_KEY_BLUE.name: 0,
            ActorType.DOOR_KEY_AQUA.name: 0,
            ActorType.DOOR_KEY_YELLOW.name: 0,
            ActorType.DOOR_KEY_RED.name: 0,
            ActorType.DOOR_KEY_MAGENTA.name: 0,
            'energy_shields_stock': [],
            'files_disks_stock': [],
            'magic_attack_spells': {},
            }
        self.stats_old = {
            'level': 1,
            'score': None,
            'lives': None,
            'power': None,
            'health': None,
            'magic_resistance': PL_MAGIC_RESISTANCE,
            'speed': None,
            'batteries': None,
            'files_disks': None,
            'files_disks_type': {},
            'bullets_t01': None,
            'bullets_t02': None,
            'bullets_t03': None,
            'bullets_t04': None,
            ActorType.POTION_POWER.name: None,
            ActorType.POTION_HEALTH.name: None,
            ActorType.FILES_DISK_D.name: None,
            ActorType.FILES_DISK_C.name: None,
            ActorType.FILES_DISK_B.name: None,
            ActorType.FILES_DISK_A.name: None,
            'apples': None,
            'door_keys': None,
            }
        self.stats_render = {
            'level': None,
            'score': None,
            'lives': None,
            'power': None,
            'health': None,
            'speed': None,
            'batteries': None,
            'files_disks': None,
            'files_disks_type': None,
            'level_no': None,
            'bullets_t01': None,
            'bullets_t02': None,
            'bullets_t03': None,
            'bullets_t04': None,
            ActorType.POTION_POWER.name: None,
            ActorType.POTION_HEALTH.name: None,
            ActorType.FILES_DISK_D.name: None,
            ActorType.FILES_DISK_C.name: None,
            ActorType.FILES_DISK_B.name: None,
            ActorType.FILES_DISK_A.name: None,
            'level_title': None,
            'score_title': None,
            'lives_title': None,
            'batteries_title': None,
            'power_title': None,
            'bullets_t01_title': None,
            'bullets_t02_title': None,
            'bullets_t03_title': None,
            'bullets_t04_title': None,
            'files_disk_t01_title': None,
            'files_disk_t02_title': None,
            'files_disk_t03_title': None,
            'files_disk_t04_title': None,
            'apples': None,
            'door_keys': None,
            }
        self.level = None
        self.sound_effects = True

        for i in range(self.images_sprite_no):
            image = pg.image.load(self.file_name_im_get(
                BM_PC_PAC_FOLDER, 'im_pc_pac', i + 1)).convert()
            image.set_colorkey(Color.BLACK)
            self.walking_frames_r.append(image)
        for i in range(self.images_sprite_no):
            image = pg.image.load(self.file_name_im_get(
                BM_PC_PAC_FOLDER, 'im_pc_pac', i + 1)).convert()
            image = pg.transform.flip(image, True, False)
            image.set_colorkey(Color.BLACK)
            self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()

        # RIP image
        image = pg.image.load(self.file_name_im_rip_get()).convert()
        image.set_colorkey(Color.BLACK)
        self.rip_frames.append(image)

        # sounds
        self.death_sound = pg.mixer.Sound(self.file_name_sound_get('snd_death_pl'))
        self.item_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.battery_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.files_disk_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.cartridge_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.rec_potion_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.life_rec_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.enemy_hit_sound = pg.mixer.Sound(self.file_name_sound_get('snd_en_hit'))
        self.door_key_found_sound = pg.mixer.Sound(self.file_name_sound_get('snd_pl_battery_found'))
        self.door_unlock_sound = pg.mixer.Sound(self.file_name_sound_get('snd_door_unlock'))
        self.npc_killed_sound = pg.mixer.Sound(self.file_name_sound_get('snd_npc_killed'))
        self.explosion_sound = pg.mixer.Sound(self.file_name_sound_get('snd_explosion'))
        self.magic_bolt_sound = pg.mixer.Sound(self.file_name_sound_get('magic_bolt'))

    @property
    def lives(self):
        return self.stats['lives']

    @lives.setter
    def lives(self, value):
        self.stats['lives'] = value

    @property
    def health(self):
        return self.stats['health']

    @health.setter
    def health(self, value):
        self.stats['health'] = value

    def get_health_rounded(self):
        return round(self.stats['health'])

    @property
    def magic_resistance(self):
        return self.stats['magic_resistance']

    @magic_resistance.setter
    def magic_resistance(self, value):
        self.stats['magic_resistance'] = value

    @property
    def power(self):
        return self.stats['power']

    @power.setter
    def power(self, value):
        self.stats['power'] = value

    def reset_stats_start_game(self):
        # Update PC stats for new game after leaving the tutorial
        for energy_shield in self.stats['energy_shields_stock']:
            energy_shield.kill_hook()
        for energy_shield in self.stats['files_disks_stock']:
            energy_shield.kill_hook()

        self.stats['lives'] -= PL_LIVES_DEFAULT
        self.stats.update({
            'level': 1,
            'score': 0,
            'lives': PL_LIVES_DEFAULT,
            'power': PL_POWER_DEFAULT,
            'health': PL_HEALTH_DEFAULT,
            'magic_resistance': PL_MAGIC_RESISTANCE,
            'magic_resistance_base': PL_MAGIC_RESISTANCE,
            'speed': PL_SPEED_DEFAULT,
            'bullets_t01': PL_BULLETS_T01_DEFAULT,
            'bullets_t02': PL_BULLETS_T02_DEFAULT,
            'bullets_t03': PL_BULLETS_T03_DEFAULT,
            'bullets_t04': PL_BULLETS_T04_DEFAULT,
            'batteries': 0,
            'files_disks': 0,
            'files_disks_type': {'D': 0, 'C': 0, 'B': 0, 'A': 0},
            ActorType.FILES_DISK_B.name: 0,
            'files_disks_stock': [],
            'magic_attack': None,
            'energy_shields_stock': [],
            'magic_attack_spells': {},
            })

    def get_power_rounded(self):
        return round(self.stats['power'])

    def acquire_energy_shield(self, msg_echo=True):
        if self.stats['energy_shields_stock']:
            return

        self.game.is_log_debug and log.debug("Create energy shield")
        energy_shield = EnergyShieldA(self.rect.x, self.rect.y, self.game)
        energy_shield.owner = self
        self.stats['energy_shields_stock'].append(energy_shield)
        msg_echo and log.info(f"You have acquired an {energy_shield.type.name}.")

    def set_magic_target(self, target_id):
        self.auto_spell_target = Actor.get_actor_if_exists(target_id)

    def update(self):
        # when RIP
        if self.direction == DIRECTION_RIP:
            if self.lives < 1:
                self.is_alive = False
            t = datetime.now().time()
            if ((t.hour * 60 + t.minute) * 60 + t.second) - self.rip_seconds >= 1:
                self.rip_seconds = 0
                if self.image != self.walking_frames_r[0]:
                    self.image = self.walking_frames_r[0]
                self.direction = DIRECTION_RIGHT
                self.change_x = 0
                self.change_y = 0
                self.reset_position()
            else:
                if self.image != self.rip_frames[0]:
                    self.image = self.rip_frames[0]
            return

        # Check this now and then, but skip the first four iterations
        if self.game.update_state_counter == 4:
            if self.is_ready_to_level_up():
                self.level_up()

        # Move left/right
        self.rect.x += self.change_x
        if self.direction == DIRECTION_RIGHT:
            if self.change_x:
                self.frame = int((pg.time.get_ticks() // 100 - self.start_time) *
                                 (Settings.fps // 10) % self.images_sprite_no)
            self.image = self.walking_frames_r[self.frame]
        else:
            if self.change_x:
                self.frame = int((pg.time.get_ticks() // 100 - self.start_time) *
                                 (Settings.fps // 10) % self.images_sprite_no)
            self.image = self.walking_frames_l[self.frame]

        # See if we hit any horizontal platform 
        block_hit_list = pg.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check if we hit any vertical platform 
        any_vertical_sliding_band = False
        block_hit_list = pg.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
                if block.change_y > 0:
                    any_vertical_sliding_band = True
                    self.change_y += block.change_y
            elif isinstance(block, SlidingBands):
                self.rect.x += block.velocity

        if not any_vertical_sliding_band:
            if self.rect.bottom <= NEAR_BOTTOM:
                self.calc_gravity()
            else:
                if self.direction != DIRECTION_RIP:
                    self.die_hard()

        # Check if we hit any battery
        battery_hit_list = pg.sprite.spritecollide(self, self.level.batteries, False)
        for battery in battery_hit_list:
            battery.kill()
            self.sound_effects and self.battery_found_sound.play()
            self.stats['batteries'] += 1
            self.stats['score'] += ExperiencePoints.xp_points[battery.type.name]

        # Check if we hit any apple
        apple_hit_list = pg.sprite.spritecollide(self, self.level.apples, False)
        for apple in apple_hit_list:
            apple.kill()
            self.sound_effects and self.battery_found_sound.play()
            self.stats['apples'] += 1
            self.stats['apples_type'][apple.apple_type] += 1
            self.stats['apples_stock'].append(apple)
            apple.is_location_in_inventory = True
            self.stats[apple.type.name] += 1

        # Check if we hit any potion
        potion_hit_list = pg.sprite.spritecollide(self, self.level.potions, False)
        for potion in potion_hit_list:
            potion.kill()
            self.stats[potion.type.name] += 1
            if potion.type.name == ActorType.POTION_POWER.name:
                self.stats['potions_power'].append(potion)
            elif potion.type.name == ActorType.POTION_HEALTH.name:
                self.stats['potions_health'].append(potion)
            potion.is_location_in_inventory = True
            self.sound_effects and self.rec_potion_found_sound.play()

        # Check if we hit any life recovery
        life_rec_hit_list = pg.sprite.spritecollide(self, self.level.life_recs, False)
        for life_rec in life_rec_hit_list:
            self.lives += 1
            if self.lives > 99:
                self.lives = 99
            life_rec.kill()
            self.sound_effects and self.life_rec_found_sound.play()

        # Check if we hit any files_disk
        files_disk_hit_list = pg.sprite.spritecollide(self, self.level.files_disks, False)
        for files_disk in files_disk_hit_list:
            files_disk.kill()
            self.sound_effects and self.files_disk_found_sound.play()
            self.stats['files_disks'] += 1
            self.stats['files_disks_type'][files_disk.disk_type] += 1
            self.stats['files_disks_stock'].append(files_disk)
            files_disk.is_location_in_inventory = True
            self.stats[files_disk.type.name] += 1
            self.stats['score'] += ExperiencePoints.xp_points[files_disk.type.name] // 2
        files_disk_hit_list and TextMsg.create(
            "Yeah!\nI've found\nanother disk!", self.game,
            time_in_secs=MSG_PC_DURATION)

        # Check if we hit any computer
        computers_hit_list = pg.sprite.spritecollide(self, self.level.computers, False)
        for computer in computers_hit_list:
            if not computer.visited:
                TextMsg.create(
                    "Hey!\nThis computer\nis a beauty!", self.game,
                    time_in_secs=MSG_PC_DURATION)
                computer.visited = True

        # Check if we hit any cartridge
        cartridge_hit_list = pg.sprite.spritecollide(self, self.level.cartridges, False)
        for cartridge in cartridge_hit_list:
            if cartridge.type == ActorType.CARTRIDGE_GREEN:
                self.stats['bullets_t01'] += 15 + randint(1, 12)
                if self.stats['bullets_t01'] > BULLET_MAX_QTY:
                    self.stats['bullets_t01'] = BULLET_MAX_QTY
            elif cartridge.type == ActorType.CARTRIDGE_BLUE:
                self.stats['bullets_t02'] += 10 + randint(1, 7)
                if self.stats['bullets_t02'] > BULLET_MAX_QTY:
                    self.stats['bullets_t02'] = BULLET_MAX_QTY
            elif cartridge.type == ActorType.CARTRIDGE_YELLOW:
                self.stats['bullets_t03'] += 4 + randint(1, 5)
                if self.stats['bullets_t03'] > BULLET_MAX_QTY:
                    self.stats['bullets_t03'] = BULLET_MAX_QTY
            else:
                self.stats['bullets_t04'] += 1 + randint(1, 4)
                if self.stats['bullets_t04'] > BULLET_MAX_QTY:
                    self.stats['bullets_t04'] = BULLET_MAX_QTY
            cartridge.kill()
            self.sound_effects and self.battery_found_sound.play()

        # Check if we hit any enemy
        if not self.invulnerable:
            enemy_hit_list = pg.sprite.spritecollide(self, self.level.npcs, False)
            has_been_hit = False
            for enemy in enemy_hit_list:
                if enemy.hostility_level == 0:
                    continue
                if (self.is_energy_shield_activated and self.direction == DIRECTION_RIGHT
                        and enemy.is_actor_on_the_left(self)):
                    continue
                if (self.is_energy_shield_activated and self.direction == DIRECTION_LEFT
                        and enemy.is_actor_on_the_right(self)):
                    continue
                has_been_hit = True
                self.health -= enemy.stats.power
            if has_been_hit:
                if self.health < 1:
                    self.die_hard()
                else:
                    self.sound_effects and self.enemy_hit_sound.play()

        # Check if we hit any snake body piece
        if not self.invulnerable:
            snake_bp_hit_list = pg.sprite.spritecollide(self, self.level.snakes_body_pieces, False)
            is_snake_bp_hit = False
            snakes_set = set()
            for snake_bp in snake_bp_hit_list:
                is_snake_bp_hit = True
                snakes_set.add(snake_bp.snake)
            for snake in snakes_set:
                self.health -= snake.stats.power // 5
            if is_snake_bp_hit:
                if self.health < 1:
                    self.die_hard()
                else:
                    self.sound_effects and self.enemy_hit_sound.play()

        # Check if we hit any dragon body piece
        if not self.invulnerable:
            dragon_bp_hit_list = pg.sprite.spritecollide(
                self, self.level.dragons_body_pieces, False)
            is_dragon_bp_hit = False
            dragons_set = set()
            for dragon_bp in dragon_bp_hit_list:
                is_dragon_bp_hit = True
                dragons_set.add(dragon_bp.dragon)
            for dragon in dragons_set:
                self.health -= dragon.stats.power // 6
            if is_dragon_bp_hit:
                if self.health < 1:
                    self.die_hard()
                else:
                    self.sound_effects and self.enemy_hit_sound.play()

        # Check if we hit any mine
        mines_hit_list = pg.sprite.spritecollide(self, self.level.mines, False)
        for mine in mines_hit_list:
            mine.explosion()

        # Check if we hit any door_key
        door_key_hit_list = pg.sprite.spritecollide(self, self.level.door_keys, False)
        for door_key in door_key_hit_list:
            door_key.kill()
            self.sound_effects and self.door_key_found_sound.play()
            self.stats['door_keys'] += 1
            self.stats['door_keys_type'][door_key.key_type] += 1
            self.stats['door_keys_stock'].append(door_key)
            door_key.is_location_in_inventory = True
            self.stats[door_key.type.name] += 1

        # Check if we hit any clock
        clocks_hit_list = pg.sprite.spritecollide(self, self.level.clocks, False)
        for clock in clocks_hit_list:
            self.sound_effects and self.item_found_sound.play()
            clock.set_on()

    def calc_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .37

    def jump(self):
        # move down a bit and see if there is a platform below.
        self.rect.y += 4
        platform_hit_list = pg.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 4
        if len(platform_hit_list) > 0:
            self.change_y = -PL_JUMP_SPEED

    def go_left(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = -PL_X_SPEED
        self.direction = DIRECTION_LEFT

    def go_left_slow(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = -PL_X_SPEED // 2
        self.direction = DIRECTION_LEFT

    def go_left_very_slow(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = -PL_X_SPEED // 4
        self.direction = DIRECTION_LEFT

    def go_right(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = PL_X_SPEED
        self.direction = DIRECTION_RIGHT

    def go_right_slow(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = PL_X_SPEED // 2
        self.direction = DIRECTION_RIGHT

    def go_right_very_slow(self):
        if self.direction == DIRECTION_RIP:
            return
        self.change_x = PL_X_SPEED // 4
        self.direction = DIRECTION_RIGHT

    def stop(self):
        self.change_x = 0

    def die_hard(self):
        if self.direction == DIRECTION_RIP:
            return
        self.stop()
        self.image = self.rip_frames[0]
        self.lives -= 1
        self.health = PL_HEALTH_DEFAULT
        self.enemy_hit_sound.stop()
        self.sound_effects and self.death_sound.play()
        self.image = self.rip_frames[0]
        self.rect.y -= 34
        self.direction = DIRECTION_RIP
        t = datetime.now().time()
        self.rip_seconds = (t.hour * 60 + t.minute) * 60 + t.second
        if self.stats['energy_shields_stock']:
            self.stats['energy_shields_stock'][0].deactivate()
        for clock in self.game.clock_sprites:
            clock.die_hard()
        for text_msg in self.game.text_msg_sprites:
            text_msg.die_hard()
        for spell in self.game.level.magic_sprites:
            if spell.target == self:
                spell.kill_hook()

    def self_destruction(self):
        if self.direction == DIRECTION_RIP:
            return
        self.die_hard()

    def reset_position(self):
        self.level.shift_world(
            self.level.door_previous_pos_world[0] - self.level.world_shift)
        self.level.shift_world_top(
            self.level.door_previous_pos_world[1] - self.level.world_shift_top)
        self.rect.x = self.level.door_previous_pos_player[0]
        self.rect.y = self.level.door_previous_pos_player[1]

    def shot_bullet(self, bullet_type):
        if self.direction == DIRECTION_RIP:
            return
        if (self.stats[bullet_type.value] < 1
                or self.power < Bullet.power_min_to_use[bullet_type.name]):
            # Not enough bullets or power for this kind of weapon
            self.game.sound_effects and resources.Resource.weapon_empty_sound.play()
            return
        self.stats[f'{bullet_type.value}_shot'] += 1
        self.stats[bullet_type.value] -= 1
        self.power -= Bullet.power_consumption[bullet_type.name]
        Bullet.shot(bullet_type=bullet_type, change_x=bullets.BULLET_STD_VELOCITY,
                    change_y=0, owner=self, game=self.game)

    def drink_potion_health(self):
        if self.direction == DIRECTION_RIP:
            return
        if self.health > 99:
            return
        if len(self.stats['potions_health']) > 0:
            self.stats[ActorType.POTION_HEALTH.name] -= 1
            self.stats['potions_health'].pop().drink()

    def drink_potion_power(self):
        if self.direction == DIRECTION_RIP:
            return
        if self.power > 99:
            return
        if len(self.stats['potions_power']) > 0:
            self.stats[ActorType.POTION_POWER.name] -= 1
            self.stats['potions_power'].pop().drink()

    def eat_apple(self):
        if self.direction == DIRECTION_RIP:
            return
        if self.health > 99:
            return
        if len(self.stats['apples_stock']) > 0:
            last_apple = self.stats['apples_stock'][-1]
            self.stats['apples'] -= 1
            self.stats['apples_type'][last_apple.apple_type] -= 1
            self.stats[last_apple.type.name] -= 1
            self.stats['apples_stock'].pop().eat()

    def is_ready_to_level_up(self):
        if self.stats['score'] > 4000 and self.stats['level'] < 2:
            return True
        if self.stats['score'] > 8500 and self.stats['level'] < 3:
            return True
        if self.stats['score'] > 11000 and self.stats['level'] < 4:
            return True
        return False

    def level_up(self, msg_echo=True):
        self.stats['level'] += 1
        if self.stats['level'] > 1:
            if not self.stats['energy_shields_stock']:
                self.acquire_energy_shield(msg_echo=msg_echo)

                self.stats['magic_attack_spells'].update({'1': VortexOfDoomB})
                self.stats['magic_attack'] = VortexOfDoomB
                msg_echo and log.info("You have acquired a Vortex of Doom B spell.")

                self.stats['magic_attack_spells'].update({'2': VortexOfDoomA})
                self.stats['magic_attack'] = VortexOfDoomA
                msg_echo and log.info("You have acquired a Vortex of Doom A spell.")

                self.stats['magic_attack_spells'].update({'3': LightningBoltA})
                self.stats['magic_attack'] = LightningBoltA
                msg_echo and log.info("You have acquired a Lightning Bolt A spell.")

                self.stats['magic_attack_spells'].update({'4': DoomBoltB})
                self.stats['magic_attack'] = DoomBoltB
                msg_echo and log.info("You have acquired a Doom Bolt B spell.")

                self.stats['magic_attack_spells'].update({'5': DoomBoltA})
                self.stats['magic_attack'] = DoomBoltA
                msg_echo and log.info("You have acquired a Doom Bolt A spell.")

                self.game.is_magic_on = True

                msg_echo and TextMsg.create(
                    "You have acquired the following skills:\n"
                    f"> Energy Shield A\n"
                    "You have acquired the following spells:\n"
                    "1. Vortex of Doom B\n"
                    "2. Vortex of Doom A\n"
                    "3. Lightning Bolt A\n"
                    "4. Doom Bolt B\n"
                    "5. Doom Bolt A\n"
                    "\n!! Do not forget that 'm' switch \n  the magic mode.",
                   self.game, time_in_secs=6)

    def switch_energy_shield(self):
        if self.direction == DIRECTION_RIP:
            return
        if self.power <= 0:
            return
        if not self.stats['energy_shields_stock']:
            return

        energy_shield = self.stats['energy_shields_stock'][0]
        if energy_shield.is_activated:
            energy_shield.deactivate()
            return
        energy_shield.activate()

    def use_door_key(self):
        if self.direction == DIRECTION_RIP:
            return
        if not self.stats['door_keys']:
            return
        door_hit_list = pg.sprite.spritecollide(self, self.level.doors, False)
        for door in door_hit_list:
            for door_key in self.stats['door_keys_stock']:
                if door_key.door is door:
                    self.stats['door_keys'] -= 1
                    self.stats['door_keys_type'][door_key.key_type] -= 1
                    self.stats['door_keys_stock'].remove(door_key)
                    self.stats[door_key.type.name] -= 1
                    door_key.use_key_in_door(door_key.door)
                    break

    def use_computer(self):
        if self.direction == DIRECTION_RIP:
            return
        if not self.stats['files_disks_stock']:
            return

        hit_list = pg.sprite.spritecollide(self, self.level.computers, False)
        if not hit_list:
            return

        msg_ids = []
        for files_disk in self.stats['files_disks_stock']:
            if not files_disk.is_msg_encrypted(files_disk.msg_id, self.game):
                continue
            if files_disk.msg_id.endswith('CORRUPTED_FILE'):
                continue
            msg_ids += [files_disk.msg_id]
            files_disk.set_msg_encrypted(
                files_disk.msg_id, is_encrypted=False, game=self.game)
            self.stats['score'] += ExperiencePoints.xp_points[files_disk.type.name]

        if msg_ids:
            text = (f"Files decrypted:\n"
                    f"{'\n'.join(msg_ids)}"
                    f"{'\n' if len(msg_ids) == 1 else ''}"
                    )
            TextMsg.create(text, self.game, time_in_secs=MSG_PC_DUR_LONG)
        else:
            text = "No files to decrypt"
            TextMsg.create(text, self.game, time_in_secs=MSG_PC_DUR_SHORT)

    def choose_spell(self, slot_number):
        if not slot_number:
            self.stats['magic_attack'] = None
            TextMsg.create("Set to NO spell.\n",
                           self.game, time_in_secs=MSG_PC_DUR_SHORT)
            return

        if self.stats['magic_attack_spells'].get(str(slot_number)):
            self.stats['magic_attack'] = self.stats['magic_attack_spells'][str(slot_number)]
            TextMsg.create(f"{self.stats['magic_attack'].__name__}\n",
                           self.game, time_in_secs=MSG_PC_DUR_SHORT)
        else:
            TextMsg.create(
                "You've got \nNO spell\nin this slot.", self.game, time_in_secs=MSG_PC_DUR_SHORT)

    def get_health_potion_ids(self):
        return [x.id for x in self.stats['potions_health']]

    def get_health_potion_powers(self):
        return [x.stats.power for x in self.stats['potions_health']]

    def get_health_potion_powers_sorted_str(self):
        return [str(x.stats.power)
                for x in sorted(self.stats['potions_health'], key=lambda x: x.power)]

    def get_health_potion_by_power(self, power):
        for potion in self.stats['potions_health']:
            if potion.stats.power == power:
                return potion

    def drink_health_potion(self, potion):
        if not potion:
            return
        potion.drink()
        self.stats['potions_health'] = [
            x for x in self.stats['potions_health'] if x.id != potion.id
            ]
        self.stats[ActorType.POTION_HEALTH.name] = len(self.stats['potions_health'])

    def get_power_potion_ids(self):
        return [x.id for x in self.stats['potions_power']]

    def get_power_potion_powers(self):
        return [x.stats.power for x in self.stats['potions_power']]

    def get_power_potion_powers_sorted_str(self):
        return [str(x.stats.power)
                for x in sorted(self.stats['potions_power'], key=lambda x: x.power)]

    def get_power_potion_by_power(self, power):
        for potion in self.stats['potions_power']:
            if potion.stats.power == power:
                return potion

    def drink_power_potion(self, potion):
        if not potion:
            return
        potion.drink()
        self.stats['potions_power'] = [
            x for x in self.stats['potions_power'] if x.id != potion.id
            ]
        self.stats[ActorType.POTION_POWER.name] = len(self.stats['potions_power'])

    def get_files_disks_str(self):
        return [str(x.msg_id)
                for x in sorted(self.stats['files_disks_stock'], key=lambda x: x.msg_id)]

    def get_files_disks_with_status_str(self):
        return [
            (f"{FilesDisk.get_msg(x.msg_id, self.game)['has_been_read'] and 'R' or '-'}"
             f"       {x.msg_id}")
            for x in sorted(self.stats['files_disks_stock'], key=lambda x: x.msg_id)
            ]

    def find_disks_for_msg_id(self, msg_id):
        return [x for x in self.stats['files_disks_stock']
                if x.msg_id == msg_id]

    def count_files_disks_not_decrypted(self):
        return sum(1 for disk in self.stats['files_disks_stock']
                if FilesDisk.get_msg(disk.msg_id, self.game)['is_encrypted']
                   and not FilesDisk.get_msg(disk.msg_id, self.game)['is_corrupted'])

    def count_files_disks_not_read(self):
        return sum(1 for disk in self.stats['files_disks_stock']
                if not FilesDisk.get_msg(disk.msg_id, self.game)['has_been_read']
                   and not FilesDisk.get_msg(disk.msg_id, self.game)['is_corrupted'])

    def levels_visited_names(self):
        return [str(x) for x in self.stats['levels_visited']]

    @staticmethod
    def create_starting_game_msg(game):
        TextMsg.create(
            "Ok. Let's go.\n"
            "- Are you ready?\n- I'm not ready!\n- Are you ready?\n- I'm not ready!",
            game, time_in_secs=3)

    @staticmethod
    def get_stats_to_persist(game):
        """Returns a dictionary with all the player's stats to persist."""
        res = {'player': {}}
        pc = game.player
        level = game.level
        res['player'] = {
            'direction': pc.direction,
            'level': pc.stats['level'],
            'score': pc.stats['score'],
            'lives': pc.stats['lives'],
            'health': pc.stats['health'],
            'power': round(pc.stats['power'], 3),
            'magic_resistance': pc.stats['magic_resistance'],
            'game_level': level.id,
            'previous_door_crossed': level.previous_door_crossed.id if level.previous_door_crossed else None,
            'door_previous_position': level.door_previous_position,
            'door_previous_pos_player': level.door_previous_pos_player,
            'door_previous_pos_world': level.door_previous_pos_world,
            'levels_visited': sorted(list(pc.stats['levels_visited'])),
            'levels_completed': sorted(level.levels_completed_ids(game)),
            'batteries': pc.stats['batteries'],
            'files_disks': pc.stats['files_disks'],
            'files_disks_type': pc.stats['files_disks_type'],
            'bullets_t01': pc.stats['bullets_t01'],
            'bullets_t01_shot': pc.stats['bullets_t01_shot'],
            'bullets_t02': pc.stats['bullets_t02'],
            'bullets_t02_shot': pc.stats['bullets_t02_shot'],
            'bullets_t03': pc.stats['bullets_t03'],
            'bullets_t03_shot': pc.stats['bullets_t03_shot'],
            'bullets_t04': pc.stats['bullets_t04'],
            'bullets_t04_shot': pc.stats['bullets_t04_shot'],
            'potions_power': [x.id for x in pc.stats['potions_power']],
            'potions_health': [x.id for x in pc.stats['potions_health']],
            ActorType.POTION_POWER.name: pc.stats[ActorType.POTION_POWER.name],
            ActorType.POTION_HEALTH.name: pc.stats[ActorType.POTION_HEALTH.name],
            ActorType.FILES_DISK_D.name: pc.stats[ActorType.FILES_DISK_D.name],
            ActorType.FILES_DISK_C.name: pc.stats[ActorType.FILES_DISK_C.name],
            ActorType.FILES_DISK_B.name: pc.stats[ActorType.FILES_DISK_B.name],
            ActorType.FILES_DISK_A.name: pc.stats[ActorType.FILES_DISK_A.name],
            'apples': pc.stats['apples'],
            'apples_stock': [x.id for x in pc.stats['apples_stock']],
            'apples_type': pc.stats['apples_type'],
            ActorType.APPLE_GREEN.name: pc.stats[ActorType.APPLE_GREEN.name],
            ActorType.APPLE_YELLOW.name: pc.stats[ActorType.APPLE_YELLOW.name],
            ActorType.APPLE_RED.name: pc.stats[ActorType.APPLE_RED.name],
            'door_keys': pc.stats['door_keys'],
            'door_keys_stock': [x.id for x in pc.stats['door_keys_stock']],
            'door_keys_type': pc.stats['door_keys_type'],
            ActorType.DOOR_KEY_GREEN.name: pc.stats[ActorType.DOOR_KEY_GREEN.name],
            ActorType.DOOR_KEY_BLUE.name: pc.stats[ActorType.DOOR_KEY_BLUE.name],
            ActorType.DOOR_KEY_AQUA.name: pc.stats[ActorType.DOOR_KEY_AQUA.name],
            ActorType.DOOR_KEY_YELLOW.name: pc.stats[ActorType.DOOR_KEY_YELLOW.name],
            ActorType.DOOR_KEY_RED.name: pc.stats[ActorType.DOOR_KEY_RED.name],
            ActorType.DOOR_KEY_MAGENTA.name: pc.stats[ActorType.DOOR_KEY_MAGENTA.name],
            'energy_shield_health': pc.stats['energy_shields_stock'][0].stats.health
                                    if pc.stats['energy_shields_stock'] else None,
            'files_disks_stock': [x.id for x in pc.stats['files_disks_stock']],
            'sound_effects': game.sound_effects,
            'is_music_paused': game.is_music_paused,
            }
        return res
