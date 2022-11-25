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
        self.arithmetics_keyword = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']


    def hasMoreCommands(self):
        return self.cur_command_line < self.commands_length

    def advance(self):
        if self.hasMoreCommands():
            self.cur_command = self.commands[self.cur_command_line]
            self.cur_command_line += 1
    
    def commandType(self):
        if any([keyword in self.cur_command for keyword in self.arithmetics_keyword]):
            return CommandType.C_ARITHMETIC
        elif 'push' in self.cur_command:
            return CommandType.C_PUSH
        elif 'pop' in self.cur_command:
            return CommandType.C_POP
        elif 'label' in self.cur_command:
            return CommandType.C_LABEL
        elif 'if' in self.cur_command:
            return CommandType.C_IF
        elif 'function' in self.cur_command:
            return CommandType.C_FUNCTION
        elif 'return' in self.cur_command:
            return CommandType.C_RETURN
        elif 'call' in self.cur_command:
            return CommandType.C_CALL
        elif 'goto' in self.cur_command:
            return CommandType.C_GOTO
    

    




