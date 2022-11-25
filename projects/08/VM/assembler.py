from parser import Parser
from code_writer import CodeWriter
from command_type import CommandType
from glob import glob
import os.path as osp

class Assembler:
    def __init__(self, file_path):
        self.parser = Parser(file_path)
        self.file_path = file_path
        self.writer = CodeWriter()
        self.asm_commands = []




    def parse_line(self):
        if self.parser.commandType() == CommandType.C_ARITHMETIC:
            return self.writer.writeArithmetic(self.parser.cur_command)
        elif self.parser.commandType() == CommandType.C_PUSH:
            _, segment, value = self.parser.cur_command.split(' ')
            return self.writer.writePush(segment, value)
        elif self.parser.commandType() == CommandType.C_POP:
            _, segment, value = self.parser.cur_command.split(' ')
            return self.writer.writePush(segment, value)
        elif self.parser.commandType() == CommandType.C_LABEL:
            return self.writer.writeLabel(self.parser.cur_command)
        elif self.parser.commandType() == CommandType.C_GOTO:
            _, label = self.parser.cur_command.split(' ')
            return self.writer.writeGoto(label)
        elif self.parser.commandType() == CommandType.C_IF:
            return self.writer.writeIf(self.parser.cur_command)
        elif self.parser.commandType() == CommandType.C_RETURN:
            return self.writer.writeReturn()
        elif self.parser.commandType() == CommandType.C_FUNCTION:
            _, segment, value = self.parser.cur_command.split(' ')
            return self.writer.writeFunction(segment, value)
        elif self.parser.commandType() == CommandType.C_CALL:
            _, segment, value = self.parser.cur_command.split(' ')
            return self.writer.writeCall(segment, value)





    def assemble(self):
        while self.parser.hasMoreCommands():
            self.parser.advance()
            asm_command = self.parse_line()
            if asm_command != "":
                self.asm_commands.append(asm_command)
        return self.asm_commands
                


if __name__ == '__main__':
    root_path = '/Users/zenglezhu/code/mooc/Nand2Tetris/projects/08/'
    asm_paths = glob(osp.join(root_path, "**", "*.vm"), recursive=True)
    for asm_path in asm_paths:
        assembler = Assembler(asm_path)
        asm_commands = assembler.assemble()
        with open(asm_path.replace('vm', 'asm'), 'w') as f:
            for asm_command in asm_commands:        
                f.write(asm_command + '\n')



    


    


    