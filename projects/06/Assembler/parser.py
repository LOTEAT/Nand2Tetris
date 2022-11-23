from command_type import CommandType



class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.commands = f.readlines()
        self.commands = [command[:command.find('//')].strip() for command in self.commands]
        self.commands = list(filter(lambda x: x, self.commands))
        self.cur_command_line = 0
        self.commands_length = len(self.commands)
        self.cur_command = None
    
    def hasMoreCommands(self):
        return self.cur_command_line < self.commands_length

    def advance(self):
        if self.hasMoreCommands():
            self.cur_command = self.commands[self.cur_command_line]
            self.cur_command_line += 1

    def commandType(self):
        if '@' in self.cur_command:
            return CommandType.A_COMMAND
        elif '(' in self.cur_command:
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def label(self):
        return self.cur_command[1:-1]

    def symbol(self):
        return self.cur_command[1:]

    def dest(self):
        # if self.commandType() == CommandType.C_COMMAND:
        return self.cur_command.split('=')[0]
            

    def comp(self):
        # if self.commandType() == CommandType.C_COMMAND:
        return self.cur_command.split('=')[1]

    def jump(self):
        # if self.commandType() == CommandType.C_COMMAND:
        return self.cur_command.split(';')[1]
    
    def reset(self):
        self.cur_command_line = 0
        self.cur_command = None
    




