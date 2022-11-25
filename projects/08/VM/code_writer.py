class CodeWriter:
    def __init__(self):
        self.ptr = 0
        self.label_cnt = 0

    def arithmeticTemplate1(self, operator):
        return "@SP\nAM=M-1\nD=M\nA=A-1\n%s" % operator

    def arithmeticTemplate2(self, jmp_type):
        return f'@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE{self.ptr}\n' + \
            f'D;{jmp_type}\n@SP\nA=M-1\nM=-1\n@CONTINUE{self.ptr}\n' + \
            f'0;JMP\n(FALSE{self.ptr})\n@SP\nA=M-1\nM=0\n(CONTINUE{self.ptr})\n'
    

    def pushTemplate1(self, segment, value, is_direct):
        no_pointer_code = "" if is_direct else f'@{value}\nA=D+A\nD=M\n'
        return f"@{segment}\nD=M\n{no_pointer_code}@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def popTemplate1(self, segment, value, is_direct):
        no_pointer_code = "D=A\n" if is_direct else f'D=M\n@{value}\nD=D+A\n'
        return f"@{segment}\n{no_pointer_code}@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"

    def preFrameTemplate(self, position):
        return f"@R11\nD=M-1\nD=M-1\nAM=D\nD=M\n@{position}\nM=D\n"
 



    def returnTemplate(self):
        return f'@LCL\nD=M\n@R11\nM=D\n@5\nA=D-A\nD=M\n@R12\nM=D\n' + self.popTemplate1('ARG', 0, False) + \
            f'@ARG\nD=M\n@SP\nM=D+1\n' + self.preFrameTemplate("THAT") + self.preFrameTemplate("THIS") + \
            self.preFrameTemplate("ARG") + self.preFrameTemplate("LCL") + '@R12\nA=M\n0;JMP\n'
                


    def writeArithmetic(self, operator):
        asm_command = ''
        if operator == 'add':
            asm_command = self.arithmeticTemplate1('M=M+D\n')
        elif operator == 'sub':
            asm_command = self.arithmeticTemplate1('M=M-D\n')
        elif operator == 'and':
            asm_command = self.arithmeticTemplate1('M=M&D\n')
        elif operator == 'or':
            asm_command = self.arithmeticTemplate1('M=M|D\n')
        elif operator == 'gt':
            asm_command = self.arithmeticTemplate2('JLE')
            self.ptr += 1
        elif operator == 'lt':
            asm_command = self.arithmeticTemplate2('JRE')
            self.ptr += 1
        elif operator == 'eq':
            asm_command = self.arithmeticTemplate2('JNE')
            self.ptr += 1
        elif operator == 'not':
            asm_command = '@SP\nA=M-1\nM=!M\n'
        elif operator == 'neg':
            asm_command = 'D=0\n@SP\nA=M-1\nM=D-M\n'
        return asm_command
        

    def writePush(self, segment, value):
        asm_command = ''
        if segment == 'constant':
            asm_command = f'@{value}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        elif segment == 'local':
            asm_command = self.pushTemplate1("LCL", value, False)
        elif segment == 'argument':
            asm_command = self.pushTemplate1("ARG", value, False)
        elif segment == 'this':
            asm_command = self.pushTemplate1("THIS", value, False)
        elif segment == 'that':
            asm_command = self.pushTemplate1("THAT", value, False)
        elif segment == 'temp':
            asm_command = self.pushTemplate1("R5", int(value) + 5, False)
        elif segment == 'pointer':
            if value == 0:
                asm_command = self.pushTemplate1("THIS", value, True)
            elif value == 1:
                asm_command = self.pushTemplate1("THAT", value, True)
        elif segment == 'static':
            asm_command = self.pushTemplate1(str(int(value)+16), value, True)
        return asm_command
        

    def writePop(self, segment, value):
        asm_command = ''
        if segment == 'local':
            asm_command = self.popTemplate1("LCL", value, False)
        elif segment == 'argument':
            asm_command = self.popTemplate1("ARG", value, False)
        elif segment == 'this':
            asm_command = self.popTemplate1("THIS", value, False)
        elif segment == 'that':
            asm_command = self.popTemplate1("THAT", value, False)
        elif segment == 'temp':
            asm_command = self.popTemplate1("R5", int(value) + 5, False)
        elif segment == 'pointer':
            if value == 0:
                asm_command = self.popTemplate1("THIS", value, True)
            elif value == 1:
                asm_command = self.popTemplate1("THAT", value, True)
        elif segment == 'static':
            asm_command = self.popTemplate1(str(int(value)+16), value, True)
        return asm_command


    def writeLabel(self, label):
        return f'({label})\n'
    

    def writeGoto(self, label):
        return f'@{label}\n0;JMP\n'
    
    def writeIf(self, label):
        return self.arithmeticTemplate1('') + f'@{label}\nD;JNE\n'

    
    def writeInit(self):
        return f'@256\nD=A\n@SP\nM=D\n' + self.writeCall("Sys.init", 0)

    def writeCall(self, function_name, num_args):
        new_label = 'RETURN_LABEL' + str(self.label_cnt)
        self.label_cnt += 1
        label_cmd = f"@{new_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        LCL_cmd = self.pushTemplate1("LCL", 0, True)
        ARG_cmd = self.pushTemplate1("ARG", 0, True)
        THIS_cmd = self.pushTemplate1("THIS", 0, True)
        THAT_cmd = self.pushTemplate1("THAT", 0, True)
        return new_label + label_cmd + LCL_cmd + ARG_cmd + THIS_cmd + THAT_cmd + \
            f'@SP\nD=M\n@5\nD=D-A\n@{num_args}\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\n' + \
            f'M=D\n@{function_name}\n0;JMP\n({new_label})\n'
    
    def writeReturn(self):
        return self.returnTemplate()
    
    def writeFunction(self, function_name, num_locals):
        function_cmd = f'{function_name}\n'
        for _ in range(int(num_locals)):
            function_cmd += self.writePush('constant', 0)
        return function_cmd

