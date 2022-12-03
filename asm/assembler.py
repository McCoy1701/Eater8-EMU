import sys


class Assembler:
    def __init__(self):
        self.programBin = []

        self.opcodes = {
            'NOP' : 0x00,
            'LDA' : 0x01,
            'ADD' : 0x02,
            'SUB' : 0x03,
            'STA' : 0x04,
            'LDI' : 0x05,
            'JMP' : 0x06,
            'JC'  : 0x07,
            'JZ'  : 0x08,
            'OUT' : 0x0e,
            'HLT' : 0x0f,
        }

        try: self.filename = sys.argv[1]
        except IndexError: print('No file given')

        self.binaryFile = self.filename.split('\\')[2].split('.')[0]

        self.parseLine()
        self.writeBinary()


    def readFile(self):
        instructions = []
        with open(self.filename, 'r') as file:
            for wholeLine in file.readlines():
                line = wholeLine.split(';')[0]
                line = line.split('\n')[0]
                instructions.append(line)

        return instructions


    def parseLine(self):
        instructions = self.readFile()

        for i in instructions:
            instr = i.split()

            try: opcode = self.opcodes[instr[0]] << 4
            except KeyError: opcode = int(instr[0], 16)

            if len(instr) == 2: argument = int(instr[1], 16)
            else: argument = 0

            programByte = opcode | argument

            self.programBin.append(programByte)


    def writeBinary(self):
        with open('.\\bin\\' + self.binaryFile + '.bin', 'wb') as file:
            file.write(bytes(self.programBin))


asm = Assembler()

