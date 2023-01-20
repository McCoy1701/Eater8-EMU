import time


class Computer:
    def __init__(self):
        self.reset()


    def reset(self):
        self.A = 0                                   #8-bits register a
        self.B = 0                                   #8-bits register b

        self.output = 0                              #8-bits output register

        self.instructionRegister = 0                 #8-bits
        self.programCounter = 0                      #4-bits
        self.carryFlag = False                       #1-bit
        self.zeroFlag = False                        #1-bit
        self.halt = False                            #1-bit

        self.ram = [0] * 16                          #16-bits of RAM


    def debug(self, level = 'ALL'):
        printList = {
            0: f'A: {hex(self.A)}, B: {hex(self.B)}, Output: {hex(self.output)}',
            1: f'Program Counter: {hex(self.programCounter)}, Instruction Register: {hex(self.instructionRegister)}',
            2: f'Carry: {bin(self.carryFlag)}, Zero: {bin(self.zeroFlag)}, HALT: {bin(self.halt)}',
            3: f'RAM: {[hex(i) for i in self.ram]} \n'
        }

        match level:
            case 'RAM':
                print(printList[3])

            case 'FLAGS':
                print(printList[2])

            case 'REGISTERS':
                for i in range(1):
                    print(printList[i])

            case 'ALL':
                for i in range(len(printList)):
                    print(printList[i])


    def load(self, filename):
        if filename == '':
            self.ram[0x00] = 0x1f         #LDA 0x0F
            self.ram[0x01] = 0x2e         #ADD 0x0E
            self.ram[0x02] = 0x79         #JC 0x09
            self.ram[0x03] = 0xe0         #OUT
            self.ram[0x04] = 0x4f         #STA 0x0F
            self.ram[0x05] = 0x1e         #LDA 0x0E
            self.ram[0x06] = 0x2d         #ADD 0x0D
            self.ram[0x07] = 0x4e         #STA 0x0E
            self.ram[0x08] = 0x60         #JMP 0x00
            self.ram[0x09] = 0x50         #LDI 0x00
            self.ram[0x0a] = 0x4f         #STA 0x0F
            self.ram[0x0b] = 0x1d         #LDA 0x0D
            self.ram[0x0c] = 0x4e         #STA 0x0E
            self.ram[0x0d] = 1
            self.ram[0x0e] = 1
            self.ram[0x0f] = 0

        else:
            try:
                with open(filename, 'rb') as file:
                    program = [int(i) for i in file.read()]


                    if len(program) != 16:
                        print('program size error')

                    else:
                        for i in range(len(self.ram)):
                            self.ram[i] = program[i]


            except FileNotFoundError:
                print(f'file not found: {filename}')


    def _step(self, speed):
        self.instructionRegister = self.ram[self.programCounter]

        self.execute()
        # self.debug()

        self.programCounter += 1

        time.sleep(float(speed))


    def execute(self):

        opcode = (self.instructionRegister & 0xf0) >> 4
        argument = self.instructionRegister & 0x0f

        # print(f'Opcode: {hex(opcode)} Argument: {hex(argument)} PC: {self.ProgramCounter}')

        match opcode:
            case 0x00:
                pass

            case 0x01:
                self.A = self.ram[argument]

            case 0x02:
                self.B = self.ram[argument]
                self.carryFlag = (self.A + self.B) > 0xff
                self.A = (self.A + self.B) & 0xff
                self.zeroFlag = self.A == 0

            case 0x03:
                self.B = self.ram[argument]
                self.carryFlag = (self.A - self.B) < 0x00
                self.A = (self.A - self.B) & 0xff
                self.zeroFlag = self.A == 0

            case 0x04:
                self.ram[argument] = self.A

            case 0x05:
                self.A = argument

            case 0x06:
                self.programCounter = argument - 1

            case 0x07:
                if self.carryFlag:
                    self.programCounter = argument - 1

            case 0x08:
                if self.zeroFlag:
                    self.programCounter = argument - 1

            case 0x0e:
                self.output = self.A
                print(f'Output: {hex(self.A)}, {self.A}')

            case 0x0f:
                self.halt = True


    def run(self, filename, speed):

        self.reset()
        self.load(filename)

        try:
            while not self.halt:
                self._step(speed)

        except IndexError:
            print('EOM')                          #End Of Memory


