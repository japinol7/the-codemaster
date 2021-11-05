"""Module help info."""
__author__ = 'Joan A. Pinol  (japinol)'


class HelpInfo:
    """Manages information used for help purposes."""

    @staticmethod
    def print_help_keys():
        print('  F1: \t show a help screen while playing the game'
              '   t: \t stats on/off\n'
              '  L_Ctrl + R_Alt + g:  grid\n'
              '   p: \t pause\n'
              ' ESC: exit game\n'
              '  ^m: \t pause/resume music\n'
              '  ^s: \t sound effects on/off\n'
              '  L_Alt + R_Alt + Enter: change full screen / normal screen mode\n'
              '  ^h: \t shows this help\n'
              '     \t hold b to kill your current life\n'
              '     \t drink health potion,  insert\n'
              '     \t drink power potion,  delete\n'
              '     \t eat health apple,  home\n'
              '   t: \t try unlocking door using each key in your inventory\n'
              '   h: \t switch energy field if available\n'
              '   m: \t switch magic and magic NPC selector  (via mouse clicks)\n'
              ' 1-5  \t choose between numbered magic attack spells. You have to acquire them.\n'
              '  0   \t no current spell  selected.\n'
              '  L_mouse_button \t cast current spell  (if magic is on and the PC has enough level)\n'
              '     \t left,   a, (or arrow)\n'
              '     \t right,  d, (or arrow)\n'
              '     \t jump,   w, (or arrow)\n'
              '     \t fire light,   u, (or 4)\n'
              '     \t fire medium,  i, (or 5)\n'
              '     \t fire strong,  j, (or 1)\n'
              '     \t fire heavy,   k, (or 2)\n'
              )
