from copy import deepcopy
from math import pow

'''if there is no such arguments,
please specify empty list. i.e.
onoff_args = []
args_info = []
iteration_args_info = []'''

'''Modify here'''
# base command
base_command = 'python train.py'

# arguments
onoff_args = ['--clip_gradient']

args_info = [{'arg': '--hidden_dim', 'option': [256,512]},
             {'arg': '--dropout_rate', 'option': [0.3, 0.5]}]

iteration_args_info = [{'arg': '--seed', 'start': 1, 'end': 2},
                 {'arg': '--num_layers', 'start': 1, 'end': 2}]
'''Modify here'''

# informations for handling onoff argument
onoff_args_num = len(onoff_args)
onoff_args_cases = int(pow(2, onoff_args_num))

# add onoff argument info to base command
command_list = []
command = [base_command]

# if onoff_args is empty
if onoff_args_num==0:
    command_list.append(command)

else:
    for i in range(onoff_args_cases):
        case = ('{:0' + str(onoff_args_num) + '}').format(int(bin(i)[2:]))

        for idx in range(onoff_args_num):
            if case[idx] == '1':
                command.append(onoff_args[idx])

        command_list.append(command)
        command = [base_command]

# prepare argument info
arg_list = [[]]

for arg_info in args_info:
    cur_len = len(arg_list)
    for i in range(cur_len):
        base_arg = arg_list.pop(0)

        arg = deepcopy(base_arg)
        for option in arg_info['option']:
            arg.append('{}={}'.format(arg_info['arg'], option))
            arg_list.append(arg)
            arg = deepcopy(base_arg)

# prepare iteration argument info
iteration_arg_list = []

for iteration_arg_info in iteration_args_info:
    iteration_arg_list.append('*{}={}~{}'.format(iteration_arg_info['arg'], iteration_arg_info['start'], iteration_arg_info['end']))

# combine three types of arguments
with open('cmd2exec.txt', 'w') as cmd:
    for command in command_list:
        for arg in arg_list:
            cmd.write(' '.join(command + arg + iteration_arg_list))
            cmd.write('\n')
