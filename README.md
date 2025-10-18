# Timeline Command Language
A recreational project, to create a DSL to speed up Timeline operations in Maya. 
It si inspired by modal editors like Vim, that, once learned, can speed up manipulation and navigation tremendously. 

The idea is to simulating entering a "timeline mode" in Maya by pressing a shortcut. 

## Tools used
Using Python 3.11, to run in Maya 2025. ~~For the parsing I'll use pyparsing for the moment, as it comes in with maya, and it should handle the project scope well. ~~ Actually using regex, as it keeps the code so much more readable than pyparsing!

## Ideal behaviour

### == Opt.1 ==
On the press of a shortcut, let's say `ALT + G` you invoke a very small promptDialog (probably written in cmds to keep compatibility to a maximum, at the cost of looks fo course).
On Pressing `ENTER` the command gets executed. Alternatively, similar to certain Vim's commands, some commands won't require pressing `ENTER` when CAPITALIZED. Obviously this behaviour will eb possible for commands that don't require an argument. 

For example: `g 100` will require `ENTER` cause it needs to know to which frame to bring you, but the command `ge` (goto range end bound) can simply be entered as `Ge` and it will execute wihtout the need to press `ENTER`. Otherwise, the DSL could maybe understand that if no explicit argument is needed, then also no `ENTER` is needed, and that could be interesting too. 

```bash
┌──────────────────────────────┐
│r 50:120                      │
└──────────────────────────────┘
```

### == Opt.2 ==

Another option could be to implement an actual `vit mode` in Maya. 
This can be done using [Event Filter](https://doc.qt.io/qt-6/eventsandfilters.html#event-filters).
That could be interesting, but it's something I'll have to study a bit before trying to implement it. 

And, on a second thought, the whole input system should actually be different. At the moment I'm designing vit to receive a string, and parse it, then with a switch chose the right command. 
But in a mode system, I'd imagine the commands to be parsed 'on the fly'. 
For example: in Blender, you press `g` to enter `grab mode` (move tool in blender lingo) then you press `5` and it'll move the object 5 units relative to the current view, then if you press `x` it'll constrain the movement to the x axys, and if you press `-` it'll adjust to a negative value. 

The way I'm designing vit right now would expects to receive `gx-5` as a string and then it'll execute the command at once.  


## Features

- [x] Lex imput commands 
- [ ] Parse Commands 
- [ ] Maya commands
- [ ] Maya GUI - 



## Core Concepts

- **Relative frames**: `100` means frame 100 relative to range start
- **Absolute frames**: `@100` means actual timeline frame 100
- **Current frame**  : `.` (like vim's current line)
- **Range bounds**   : `s` (start), `e` (end)

## Navigation Commands

### g - Go to frame
- `g 100`           - Go to frame 100 (relative to range)
- `g @100`          - Go to absolute frame 100
- `gs` or `g s`     - Go to range start
- `ge` or `g e`     - Go to range end
- `g .+10`          - Go to current frame +10
- `g .-10`          - Go to current frame -10 

## Range Commands

### r - Set range
- `r 100:200`       - Set range to [100, 200]
- `r :200`          - Set range max (keep current min)
- `r 100:`          - Set range min (keep current max)
- `r s:e`           - Will work with shortcuts too
- `rs` or `r .:`    - Set range min to current frame
- `re` or `r :.`    - Set range max to current frame

### ee - Extend range
- `ee`  - Extend range to full timeline bounds

### sh - Shrink range
- `sh`  - Shrink timeline bounds to current range bounds

### s - Scale range
- `s 0.5`   - Scale the selected range to 0.5
- `ss 0.5`  - Ripple Scale the selected range to 0.5  

### sl - Select range
- `sl 0:10`   - Select range 0:10
- `sl .`      - select the current frame
- `sl 10`     - select range 10:10 


==
## Editing Commands

### m - Move keyframes
- `m 5`     - Move current key +5 frames
- `m @100`  - Move current key to frame 100
- `ma 5`    - Move all keys after +5 frames
- `mm 5`    - Ripple move +5 (push subsequent keys)

### y - Yank (copy)
- `y`   - Yank current keyframe
- `ya`  - Yank all keyframes on selected objects
- `yr`  - Yank range

### p - Paste
- `p`   - Paste at current frame (overwrite)
- `pi`  - Paste insert (push keys after)
- `pm`  - Paste mirrored

### x - Cut
- `x`        - Cut current key (leave gap)
- `x 10`     - Cut key at 10 if available (leave gap)
- `x 10:e`   - Cut keyframes at 10 if available (leave gap)
- `xx`       - Cut and ripple (close gap)
- `xa`       - Cut all keys after and ripple
- `xo`       - Cut all keys outside range bounds

### sp - Space or Distribute
- `sp 3`         - Add 3 frames between keys in current range
- `sp 3 100:200` - Add 3 frames between keys in range
- `spa 3`        - Add 3 frames between ALL keys



==
## Ex Commands
These commands can run more complex actions, and they're called with the prefix `:` 

### Open Maya Editors
- `:graph`     - opens the Graph Editor
- `:clip`   - opens the Clip Editor
- `:dope`    - opens the Dope Sheet

### :save - save to file   ???? maybe 
### :load - load from file ???? maybe

### Utility Commands
- `:help`     - Show command reference
- `:help m`   - Show help for move command
- `:undo`     - Undo last operation (or just `u`)
- `:redo`     - Redo last operation (or just `ctrl+r`)
- `:info`     - Show current frame, range, selection info // through the ui
- `:clear`    - Clear command history // implying the implementation of the history

