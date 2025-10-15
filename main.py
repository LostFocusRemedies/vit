"""
import vit.main as vit 
from importlib import reload
reload(vit)

vit.vit()
"""

import pyparsing as pp
import maya.cmds as cm



commands_dict = {
    "goto_cmd": "g",
    "goto_start_cmd": "gs",
    "goto_end_cmd": "ge",
    "set_range_cmd": "r",
    "move_cmd": "m",
    "yank_cmd": "y",
    "cut_cmd": "x",
    "paste_cmd": "p",
}
commands_str = " ".join(commands_dict.values())


#------------------------------------------------
# Command parsing
#------------------------------------------------

def parse_command(command_string):
    # Basic elements
    integer = pp.Word(pp.nums).setParseAction(lambda t: int(t[0]))
    
    # Frame specifiers
    dot = pp.Literal(".")
    at = pp.Suppress("@")
    minus = pp.Literal("-")
    
    # Frame types
    relative_frame = pp.Combine(pp.Optional(minus) + integer)
    current_frame = dot
    absolute_frame = at + integer
    
    frame = (absolute_frame | relative_frame | current_frame)
    
    # Range separator (: or ;)
    range_sep = pp.Suppress(pp.Literal(":") | pp.Literal(";"))
    frame_range = pp.Group(frame + range_sep + frame)("range")
    
    # Command definitions
    cmd = pp.oneOf(command_string)("command")
    
    # Arguments can be either a range or individual frames/integers
    arguments = pp.Optional(frame_range | frame)("args")
    
    # Full grammar
    grammar = cmd + arguments
    
    try:
        result = grammar.parseString(command_string, parseAll=True)
        return result
    except pp.ParseException as e:
        print(f"Parse error: {e}")
        return None



#------------------------------------------------
# TIMELINE OPERATIONS
#------------------------------------------------

def goto_frame(frame):
    cm.currentTime(frame)

def goto_start():
    start = cm.playbackOptions(q=True, min=True)
    cm.currentTime(start)

def goto_end():
    end = cm.playbackOptions(q=True, max=True)
    cm.currentTime(end)

def set_range(start, end):
    cm.playbackOptions(min=start, max=end)
    

#------------------------------------------------
# UI
#------------------------------------------------

def vit(*args):
    vit_dialog = cm.promptDialog(
        title='VIT',
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    if vit_dialog == 'Cancel': 
        return
    
    vit_input = cm.promptDialog(query=True, text=True)
    parsed = parse_command(vit_input)
    
    if not parsed: 
        print("Invalid command")
        return
    
    cmd = parsed.command
    
    if cmd == "gs":
        goto_start()
    elif cmd == "ge":
        goto_end()
    elif cmd == "g":
        if parsed.args:
            if parsed.args == ".":
                frame = cm.currentTime(q=True)
            if not parsed.args.startswith("@"):
                frame = int(parsed.args) + cm.playbackOptions(q=True, min=True)
            goto_frame(frame)
    elif cmd == "r":
        if parsed.range:
            start, end = parsed.range
            if start == ".":
                start = cm.currentTime(q=True)
            if end == ".":
                end = cm.currentTime(q=True)
            if start > end:
                start, end = end, start
            if start == end:
                print("Range start and end cannot be the same")
                return
            if not start.startswith("@"): 
                start = int(start) + cm.playbackOptions(q=True, min=True)
            if not end.startswith("@"): 
                end = int(end) + cm.playbackOptions(q=True, min=True)
                
            set_range(int(start), int(end))
    else:
        print(f"Command '{cmd}' not yet implemented")




#------------------------------------------------
# When running as a script
#------------------------------------------------


# if __name__ == "__main__":
#     vit()