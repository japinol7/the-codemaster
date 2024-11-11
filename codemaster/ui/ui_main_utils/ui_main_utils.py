"""Module ui_main_menu."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui


def create_text_dialog_msg(obj, text, title="Message", rect=None, visible=True):
    obj.items['text_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
        rect=rect or pg.Rect((406, 450), (350, 165)),
        manager=obj.manager,
        html_message=text,
        window_title=title,
        object_id=pgui.core.ObjectID(class_id='@dialog_msgs', object_id='#text_msg'),
        visible=visible,
        )


def create_error_dialog_msg(obj, text, rect=None, visible=True):
    obj.items['error_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
        rect=rect or pg.Rect((406, 450), (350, 165)),
        manager=obj.manager,
        html_message=text,
        window_title="ERROR",
        object_id=pgui.core.ObjectID(class_id='@dialog_msgs', object_id='#error_msg'),
        visible=visible,
        )


def create_confirmation_dialog_msg(obj, text, title, action_short_text, items_key, visible=True):
    obj.items[items_key] = pgui.windows.ui_confirmation_dialog.UIConfirmationDialog(
        rect=pg.Rect((406, 450), (350, 205)),
        manager=obj.manager,
        action_long_desc=text,
        window_title=title,
        action_short_name=action_short_text,
        blocking=True,
        visible=visible,
        )
