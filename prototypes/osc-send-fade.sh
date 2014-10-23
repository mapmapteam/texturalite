#!/bin/bash

set -o verbose

# 0
osc-send -p 11111 /texturalite/sound/amp ,if 0 1
osc-send -p 11111 /texturalite/sound/amp ,if 1 0
osc-send -p 11111 /texturalite/sound/amp ,if 2 0
# 
# # 1
# osc-send -p 11111 /texturalite/sound/amp ,if 0 0
# osc-send -p 11111 /texturalite/sound/amp ,if 1 1
# osc-send -p 11111 /texturalite/sound/amp ,if 2 0

# # 2
# osc-send -p 11111 /texturalite/sound/amp ,if 0 0
# osc-send -p 11111 /texturalite/sound/amp ,if 1 0
# osc-send -p 11111 /texturalite/sound/amp ,if 2 1

