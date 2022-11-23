from parser import Parser
from symbol import SymbolTables, LabelTables
from translator import Translator
from command_type import CommandType
from utils import *
from glob import glob
import os.path as osp

class Assembler:
    def __init__(self, file_path):
        self.parser = Parser(file_path)
        self.symbols = SymbolTables()
        self.labels = LabelTables()
        self.translator = Translator()
        self.file_path = file_path
        self.binary_commands = []
        self.var_ptr = 16
        self.pc = 0


    def build_labels(self):
        while self.parser.hasMoreCommands():
            self.parser.advance()
            if self.parser.commandType() == CommandType.L_COMMAND:
                label = self.parser.label()
                self.labels.addEntry(label, self.pc)
            else:
                self.pc += 1
        self.pc = 0
        self.parser.reset()

    def parse_line(self):
        binary_command = ""
        dst, jmp, comp = "", "", ""
        if self.parser.commandType() == CommandType.A_COMMAND:
            symbol = self.parser.symbol()
            if symbol.isnumeric():
                return fill_zero_left(symbol)
            elif self.labels.contains(symbol):
                addr = self.labels.getAddress(symbol)
                return fill_zero_left(addr)
            elif self.symbols.contains(symbol):
                return fill_zero_left(self.symbols.getAddress(symbol))
            else:
                self.symbols.addEntry(symbol, self.var_ptr)
                binary_command = fill_zero_left(self.var_ptr)
                self.var_ptr += 1
        elif self.parser.commandType() == CommandType.C_COMMAND:
            equal_sign_index = self.parser.cur_command.find('=')
            semicolon_index = self.parser.cur_command.find(';')
            if equal_sign_index >= 0 and semicolon_index >= 0:
                dst = self.parser.cur_command[0: equal_sign_index]
                comp = self.parser.cur_command[equal_sign_index+1: semicolon_index]
                jmp = self.parser.cur_command[semicolon_index:]
            elif equal_sign_index == -1 and semicolon_index >= 0:
                comp = self.parser.cur_command[0: semicolon_index]
                jmp = self.parser.cur_command[semicolon_index+1:]
            elif equal_sign_index >= 0 and semicolon_index == -1:
                dst = self.parser.cur_command[0: equal_sign_index]
                comp = self.parser.cur_command[equal_sign_index+1:]
            else:
                dst = self.parser.cur_command
            if self.translator.comp0_contains(comp):
                a = '0'
                comp = self.translator.comp_translation_0(comp)
            else:
                a = '1'
                comp = self.translator.comp_translation_1(comp)

            binary_command = "111" + a + comp + self.translator.dest_translation(dst) + self.translator.jump_translation(jmp)
        return binary_command
   


    def assemble(self):
        binary_commands = []
        self.build_labels()
        while self.parser.hasMoreCommands():
            self.parser.advance()
            binary_command = self.parse_line()
            if binary_command != "":
                binary_commands.append(binary_command)
        return binary_commands
                


if __name__ == '__main__':
    root_path = '/Users/zenglezhu/code/mooc/Nand2Tetris/projects/06/'
    asm_paths = glob(osp.join(root_path, "**", "*.asm"), recursive=True)
    for asm_path in asm_paths:
        assembler = Assembler(asm_path)
        binary_commands = assembler.assemble()
        with open(asm_path.replace('asm', 'hack'), 'w') as f:
            for binary_command in binary_commands:
                f.write(binary_command + '\n')



    


    


    