"""Module explosions."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import BM_EXPLOSIONS_FOLDER, DIRECTION_RIP
from codemaster.models.experience_points import ExperiencePoints
from codemaster.tools.logger.logger import log
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Explosion(ActorItem):
    """Represents an explosion.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_folder = BM_EXPLOSIONS_FOLDER
        self.file_name_key = 'explosions'
        self.images_sprite_no = 8
        self.category_type = ActorCategoryType.EXPLOSION
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.health = self.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        self.animation_speed = 0.4
        self.transparency_alpha = True
        super().__init__(x, y, game, name=name)
        self.player.sound_effects and self.player.explosion_sound.play()

    def update_after_inc_index_hook(self):
        if 1.99 <= round(self.frame_index, 2) <= 2:
            # Check if we hit any npc
            npcs_hit_list = pg.sprite.spritecollide(self, self.game.level.npcs, False)
            for npc in npcs_hit_list:
                if not npc.can_be_killed_normally:
                    continue
                # Manage npc damage
                attack_power_res = self.power
                if self.is_magic_item:
                    attack_power_res = self.power - npc.magic_resistance
                    self.game.is_log_debug and log.debug(
                        f"{npc.id} hit by {self.id}, npc_health: {str(round(npc.health, 2))}, "
                        f"explosion_power: {str(self.power)}, magic_res: {npc.magic_resistance}, "
                        f"owner: {self.owner.id}")
                else:
                    self.game.is_log_debug and log.debug(
                        f"{npc.id} hit by {self.id}, npc_health: {str(round(npc.health, 2))}, "
                        f"explosion_power: {str(self.power)}, owner: {self.owner.id}")
                if attack_power_res > 0:
                    npc.health -= attack_power_res

                if npc.health <= 0:
                    self.game.is_log_debug and log.debug(
                        f"{npc.id}, !!! Dead by {self.id}. Owner: {self.owner.type.name} !!!")
                    if self.is_a_player_shot:
                        self.player.stats['score'] += ExperiencePoints.xp_points[npc.type.name]
                    npc.drop_items()
                    npc.kill_hook()
                    self.player.sound_effects and self.player.enemy_hit_sound.play()

            # Check if we hit any mine
            mines_hit_list = pg.sprite.spritecollide(self, self.game.level.mines, False)
            for mine in mines_hit_list:
                mine.health -= self.power
                if mine.health <= 0:
                    mine.explosion()
                    mine.kill()

            # Check if we hit any player
            players_hit_list = pg.sprite.spritecollide(self, self.game.players, False)
            for pc in players_hit_list:
                if pc.direction == DIRECTION_RIP or pc.invulnerable:
                    continue

                # Manage player damage
                attack_power_res = self.power
                if self.is_magic_item:
                    attack_power_res = self.power - pc.magic_resistance
                    self.game.is_log_debug and log.debug(
                        f"{pc.id} hit by {self.id}, pc_health: {str(round(pc.health, 2))}, "
                        f"explosion_power: {str(self.power)}, magic_res: {pc.magic_resistance}, "
                        f"owner: {self.owner.id}")
                else:
                    self.game.is_log_debug and log.debug(
                        f"{pc.id} hit by {self.id}, pc_health: {str(round(pc.health, 2))}, "
                        f"explosion_power: {str(self.power)}, owner: {self.owner.id}")
                if attack_power_res > 0:
                    pc.health -= attack_power_res

                if pc.health <= 0:
                    self.game.is_log_debug and log.debug(
                        f"{pc.id}, !!! Dead by {self.id} Owner: {self.owner.id} !!!")
                    pc.die_hard()

        if self.frame_index >= self.images_sprite_no:
            self.kill()

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class ExplosionC(Explosion):
    """Represents an explosion of type C."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't1'
        self.type = ActorType.EXPLOSION_C
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 140


class ExplosionB(Explosion):
    """Represents an explosion of type B."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't1'
        self.type = ActorType.EXPLOSION_B
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 170


class ExplosionA(Explosion):
    """Represents an explosion of type A."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't1'
        self.type = ActorType.EXPLOSION_A
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 350


class ExplosionMagicC2(Explosion):
    """Represents an explosion of type C2."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't4'
        self.type = ActorType.EXPLOSION_MAGIC_C2
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 160
        self.is_magic_item = True


class ExplosionMagicC3(Explosion):
    """Represents an explosion of type C3."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't3'
        self.type = ActorType.EXPLOSION_MAGIC_C3
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 185
        self.is_magic_item = True


class ExplosionMagicC4(Explosion):
    """Represents an explosion of type C4."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't2'
        self.type = ActorType.EXPLOSION_MAGIC_C4
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 210
        self.is_magic_item = True


class ExplosionMagicC5(Explosion):
    """Represents an explosion of type C5."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't2'
        self.type = ActorType.EXPLOSION_MAGIC_C5
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 300
        self.is_magic_item = True
