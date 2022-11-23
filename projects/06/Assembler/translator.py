class Translator:
    def __init__(self):
        self.dest_convert_rules = {
            '': '000', 'M': '001', 'D': '010', 'MD': '011', 
            'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111',
        }

        self.jump_convert_rules = {
            '': '000', 'JGT': '001', 'JEQ': '010', 'JGE' : '011',
            'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
        }

        self.comp_convert_rules_0 = {
            '0': '101010', '1': '111111', '-1': '111010', 'D': '001100',
            'A': '110000', '!D': '001101', '!A': '110001', '!D': '001101',
            '-D': '001111', '-A': '110011', 'D+1': '011111', 'A+1': '110111',
            'D-1': '001110', 'A-1': '110010', 'D+A': '000010', 'D-A': '010011',
            'A-D': '000111', 'D&A': '000000', 'D|A': '010101'
        }

        self.comp_convert_rules_1 = {
            'M': '110000', '!M': '110001', '-M': '110011', 'M+1': '110111', 
            'M-1': '110010', 'D+M': '000010', 'D-M': '010011', 'M-D': '000111', 
            'D&M': '000000', 'D|M': '010101'
        }



    def dest_translation(self, mnemonic):
        return self.dest_convert_rules[mnemonic]
    
    def jump_translation(self, mnemonic):
        return self.jump_convert_rules[mnemonic]
    
    def comp_translation_0(self, mnemonic):
        return self.comp_convert_rules_0[mnemonic]
    
    def comp_translation_1(self, mnemonic):
        return self.comp_convert_rules_1[mnemonic]

    def comp0_contains(self, key):
        return key in self.comp_convert_rules_0.keys()
    
    def comp1_contains(self, key):
        return key in self.comp_convert_rules_1.keys()

    



    