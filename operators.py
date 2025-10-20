import maya.cmds as cm
import maya.mel as mel



# ------------------------------------------------
# NAVIGATION OPS

def goto(frame):
    cm.currentTime(frame)


def goto_start():
    start_frame = cm.playbackOptions(q=True, min=True)
    goto(start_frame)


def goto_end():
    end_frame = cm.playbackOptions(q=True, max=True)
    goto(end_frame)


def range_set(start, end):
    cm.playbackOptions(min=start, max=end)


def range_extend():
    ast = cm.playbackOptions(q=True, ast=True)
    aet = cm.playbackOptions(q=True, aet=True)
    cm.playbackOptions(min=ast, max=aet)


def range_shrink(start, end):
    if start < end:
        cm.playbackOptions(min=start + 1, max=end - 1)




# ------------------------------------------------
# MOVE KEYFRAMES OPS

def move(frame, offset):
    if isinstance(frame, list):
        range_start = frame[0]
        range_end = frame[1]

    sel = cm.ls(selection=True)
    cm.keyframe(
        sel,
        edit=True,
    )




# ------------------------------------------------
# CLIPBOARD OPS

def yank_keyframe(frame=cm.currentTime(q=True)):
    time_control = cm.lsUI(type="timeControl")[0]
    start_frame, end_frame = cm.timeControl(time_control, q=True, rangeArray=True)
    end_frame -= 1
    if start_frame == end_frame:
        start_frame = end_frame = cm.currentTime(q=True)

    cm.copyKey(time=(start_frame, end_frame))
    print(f"Yanked keyframes within range: {start_frame} to {end_frame}")


def yank_all_keyframes():
    pass


def cut_keyframe(frame=cm.currentTime(q=True)):
    pass


def cut_all_keyframes():
    pass


def paste_keyframes():
    current_time = int(cm.currentTime(q=True))
    cm.pasteKey(time=(current_time, current_time), option="insert")




# ------------------------------------------------
# Utility Functions
# ------------------------------------------------

def get_selected_time_range():
    playbackSlider = get_active_playback_slider()

    selectedRange = cm.timeControl(playbackSlider, q=True, rangeArray=True)
    rangeFramesFirst, rangeFramesLast = selectedRange[0], selectedRange[1]

    if (rangeFramesLast - rangeFramesFirst) == 1:
        rangeFramesFirst = cm.playbackOptions(q=True, min=True)
        rangeFramesLast = cm.playbackOptions(q=True, max=True)
        selectedRange = [rangeFramesFirst, rangeFramesLast]

    return selectedRange


def get_active_audio_node():
    playbackSlider = get_active_playback_slider()
    audioNode = cm.timeControl(playbackSlider, q=True, s=True)
    return audioNode


def get_active_playback_slider():
    return mel.eval("$tmp = $gPlayBackSlider")
