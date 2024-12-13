"""Module sign_message."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_MISC_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class SignMessage(ActorItem):
    """Represents a sign message.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_MISC_FOLDER
        self.file_name_key = 'im_sign_messages'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.SIGN_MESSAGE
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1

        super().__init__(x, y, game, name=name)

        self.hostility_level = 0
        self.magic_resistance = 990

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class SignMessageTutorialStartGame(SignMessage):
    """Represents a sign message for tutorial msg to start the game."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = 'goto_start_game_01'
        self.type = ActorType.SIGN_MESSAGE_TUTORIAL_START_GAME
        super().__init__(x, y, game, name=name)


class SignMessageTutorialLeave(SignMessage):
    """Represents a sign message for tutorial msg post to leave."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = 'leave_tutorial_01'
        self.type = ActorType.SIGN_MESSAGE_TUTORIAL_LEAVE
        super().__init__(x, y, game, name=name)
