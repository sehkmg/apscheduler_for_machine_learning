from copy import deepcopy

class cmd2deploy:
    def __init__(self):
        self.cmd_file = open('schedule_training/cmd2deploy.txt', 'r')
        self.gpu_str = 'CUDA_VISIBLE_DEVICES={} '
        self.command_lists = []

    def get_line(self):
        return self.cmd_file.readline()

    def arg_iteration(self, command):
        command = deepcopy(command)
        iteration_arg_list = [[]]

        while command[-1][0] == '*':
            iteration_arg = command.pop()
            arg_name = iteration_arg.split('=')[0][1:]
            start = int(iteration_arg.split('=')[1].split('~')[0])
            end = int(iteration_arg.split('=')[1].split('~')[1])

            cur_len = len(iteration_arg_list)
            for i in range(cur_len):
                base_arg = iteration_arg_list.pop(0)

                arg = deepcopy(base_arg)
                for option in range(start, end+1):
                    arg.append('{}={}'.format(arg_name, option))
                    iteration_arg_list.append(arg)
                    arg = deepcopy(base_arg)

        return command, iteration_arg_list
    
    def make_cmd_list(self):
        # see first line
        line = self.get_line()

        # if current line is gpu info, execute
        while line[:3] == 'gpu':
            # store gpu number
            gpu_num = int(line.strip().split(':')[1])
            # see next line
            line = self.get_line().split('#')[0]
            if line != '\n':
                line = line.strip()

            # if current line is not gpu info, repeat
            while line[:3] != 'gpu':

                # if current line is not newline and EOF or doc
                # repeat adding commands
                command_list = []
                while line != '\n' and line and line != 'doc':

                    # load command and extent iteration
                    command = line.strip().split(' ')
                    command, iteration_arg_list = self.arg_iteration(command)

                    # store command
                    for arg in iteration_arg_list:
                        command_list.append(self.gpu_str.format(gpu_num) + ' '.join(command + arg))

                    # see next line
                    line = self.get_line().split('#')[0]
                    if line != '\n':
                        line = line.strip()

                # if current line is newline or EOF, append command_list to command_lists
                if len(command_list) != 0:
                    self.command_lists.append(command_list)
                # if current line is EOF or doc, return command_lists
                if not line or line == 'doc':
                    self.cmd_file.close()
                    return self.command_lists

                # see next line
                line = self.get_line().split('#')[0]
                if line != '\n':
                    line = line.strip()

if __name__=='__main__':
    cmd2deploy = cmd2deploy()
    command_lists = cmd2deploy.make_cmd_list()

    for command_list in command_lists:
        for command in command_list:
            print(command)
        print('')
