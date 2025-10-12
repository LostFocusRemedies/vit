import pyparsing as pp


def main(command):
    define_grammar()
    parse_command(command)
    
def parse_command(command):
    print("Parsing command:", command)
    try:
        result = pp.OneOrMore(pp.Word(pp.alphanums + "-_./:")).parseString(command)
        print("Parsed result:", result)
    except pp.ParseException as pe:
        print("Parse error:", pe)

def define_grammar():
    integer = pp.Word(pp.nums)
    minus = pp.Literal("-")
    dot = pp.Literal(".")
    range_start = pp.Literal("s")
    range_end   = pp.Literal("e")
    colon = pp.Literal(":")
    at = pp.Literal("@")
    
    relative_frame = (pp.Optional(minus) + integer)
    current_frame = dot
    absolute_frame = at + integer
    frame = (relative_frame | current_frame | absolute_frame)
    # 0:10
    frame_range = frame + colon + frame


if __name__ == "__main__":
    command = input("Enter command: ")
    main(command)