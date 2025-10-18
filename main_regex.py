import re
from enum import Enum

class COMMANDS(str, Enum):
    GOTO         = "g"
    GOTO_START   = "gs" 
    GOTO_END     = "ge"
    RANGE_SET    = "r"
    RANGE_EXTEND = "rr" 
    RANGE_SHRINK = "rs"
    MOVE         = "m"
    YANK         = "y"
    YANK_ALL     = "ya"
    YANK_NEXT    = "yn"
    YANK_PREV    = "yp"
    CUT          = "x"
    CUT_ALL      = "xa"
    CUT_NEXT     = "xn"
    CUT_PREV     = "xp"
    PASTE        = "p" # will paste insert at current frame


# Frame components
RELATIVE       = r"[0-9]+"
ABSOLUTE       = rf"@-?{RELATIVE}"      # @100, @-10 (allow negative absolute)
CURRENT_OFFSET = rf"\.?[+-]{RELATIVE}"  # .+5, .-10, +5, -10
CURRENT        = r"\."
BOUND          = r"[se]"

# combining the Frame pattern
FRAME = rf"(?:{ABSOLUTE}|{CURRENT_OFFSET}|{CURRENT}|{BOUND}|{RELATIVE})"
RANGE = rf"(?:{FRAME})?[:;](?:{FRAME})?"

# sorting the commands by length to avoid partial matches
commands_sorted = sorted(COMMANDS, key=lambda c: len(c.value), reverse=True)
COMMAND = "|".join(re.escape(cmd.value) for cmd in commands_sorted)

#  finally the full grammar
GRAMMAR_PATTERN = rf"^(?P<cmd>{COMMAND})?(?:\s*(?P<arg>(?:{RANGE})|(?:{FRAME})))?$"



def main():
    vit_pattern = re.compile(GRAMMAR_PATTERN)

    test_commands = [
        "g@10",
        "gs",
        "ge",
        "r@5:@15",
        "m-3",        
        "mm",
        "y",
        "x @12:@18",
        "p",
        "rr",
        "100",        # Implicit goto
        "10:20",      # Implicit range
    ]
    
    for cmd in test_commands:
        match = vit_pattern.match(cmd)
        if not match:
            print(f"Invalid command: {cmd}")
            continue

        match_dict = match.groupdict()

        if not match_dict["cmd"] and match_dict["arg"]:
            if ":" in match_dict["arg"] or ";" in match_dict["arg"]:
                match_dict["cmd"] = COMMANDS.RANGE_SET.value
            else:
                match_dict["cmd"] = COMMANDS.GOTO.value

        print(f"{cmd:15} => cmd:'{match_dict['cmd']}' arg: '{match_dict['arg']}'")








if __name__ == "__main__":
    main()
