#coding=utf-8
# =================
# author: zhouxin
# start_date： 171126
# description: some basic settings for the projects
#
# =================

# colors 
# numbers in sorting have two states
# in comparation or out
# so 'IN' or 'OUT' stand for the two states
COLOR_MAPPING = {
    'IN1': '#e74c3c',
    'IN2': '#1abc9c',
    'IN3': '#2ecc71',
    'IN4': '#6959CD',
    'OUT1': '#95a5a6',
    'OUT2': '#2c3e50',
    'OUT3': '#7f8c8d'

}

AUDIO_MAPPING = [
    65.406, 73.416, 82.407, 87.307, 97.999, 110.00, 123.47,
    130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94,
    261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88,
    523.25, 587.33, 659.26, 698.46, 783.99, 880.00, 987.77,
    1046.5, 1174.7, 1318.5, 1396.9, 1568.0, 1760.0, 1975.5,
    2093.0, 2349.3, 2637.0, 2793.8, 3136.0, 3520.0, 3951.1
]


# ending animation
from collections import OrderedDict

FINISHED = []
for i in range(1, 42):
    tem = []
    for j in range(1, 41):
        if i == j:
            tem.append((j, COLOR_MAPPING.get('IN1')))
        else:
            tem.append((j, COLOR_MAPPING.get('OUT1')))
    FINISHED.append(OrderedDict(tem))


