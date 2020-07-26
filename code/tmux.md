---
description: Frequently used for tmux
---

# tmux

## Recipes

**To create session**

`tmux new -s sess_name`

**To attach a session**

`tmux a -t sess_name`

**To create a session in detached mode**

`tmux new -d -s sess_name`

**To  send commands to a session to the pane 0**

`tmux send-keys -t sess_name.0 "pwd" ENTER`

**To split panes horizontally in detached mode 1(right) and 0(left)**

`tmux splitw -h -p 50 -t sess_name:1.0`

**To kill tmux server**

`tmux kill-server`

**To kill tmux session**

`tmux kill-session -t sess_name`

**To kill all other sessions from a session**

`tmux kill-session -a`

## Resources

- [tmux: Productive Mouse-Free Development](http://pragprog.com/book/bhtmux/tmux)
- [How to reorder windows](http://superuser.com/questions/343572/tmux-how-do-i-reorder-my-windows)
- [tmux Tutorial — Split Terminal Windows Easily - Lukasz Wrobel](https://lukaszwrobel.pl/blog/tmux-tutorial-split-terminal-windows-easily/) 