"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8
        self.pc = 0
        self.ram = [0]*256
        self.stop = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]
        filename = sys.argv[1]
        with open(filename) as program_file:  # opens file
            for line in program_file:  # reads file line by line
                # turns the line into int instead of string
                line = line.split('#')
                line = line[0].strip()  # list
                if line == '':
                    continue
                # turns the line into <int> instead of string store the address in memory
                self.ram[address] = int(line, base=2)
                address += 1  # add one and goes to the next

        # with open(filename) as program_file:
        #     for line in program_file:
        #         arr1 = line.split('#', 1)
        #         line = int(arr1[0].strip(), base2)
        #         if len(line)<1:
        #             continue
        #         self.ram[address] = line
        #         address += 1
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ALU Functions

    def ADD():
        print("ADD not implemented yet")
        pass

    def SUB():
        print("SUB not implemented yet")
        pass

    def MUL():
        # Eventually I will want to hook this up to the ALU
        # I will want to perform the operations in the ALU
        # using only && and ||. I would want ADD to use these
        # and multiply to preform this operation over and overagain

        # For MVP I will just multiply the two together here
        self.reg[self.ram_read(self.pc + 1)
                 ] *= self.reg[self.ram_read(self.pc+2)]
        self.pc += 3

    def DIV():
        print("DIV not implemented yet")
        pass

    def MOD():
        print("MOD not implemented yet")
        pass

    def INC():
        print("INC not implemented yet")
        pass

    def DEC():
        print("DEC not implemented yet")
        pass

    def CMP():
        print("CMP not implemented yet")
        pass

    def AND():
        print("AND not implemented yet")
        pass

    def NOT():
        print("NOT not implemented yet")
        pass

    def OR():
        print("OR not implemented yet")
        pass

    def XOR():
        print("XOR not implemented yet")
        pass

    def SHL():
        print("SHL not implemented yet")
        pass

    def SHR():
        print("SHR not implmented yet")
        pass

    # PC Mutators

    def CALL():
        print("CALL not implemented yet")
        pass

    def RET():
        print("RET not implemented yet")
        pass

    def INT():
        print("INT not implemented yet")
        pass

    def IRET():
        print("IRET not implemented yet")
        pass

    def JMP():
        print("JMP not implemented yet")
        pass

    def JEQ():
        print("JEQ not implemented yet")
        pass

    def JNE():
        print("JNE not implemented yet")
        pass

    def JGT():
        print("JGT not implemented yet")
        pass

    def JLT():
        print("JLT not implemented yet")
        pass

    def JLE():
        print("JLE not implemented yet")
        pass

    def JGE():
        print("JGE not implemented yet")
        pass

    # Other

    def NOP():
        """
            No operation. Do nothing for this instruction.
        """
        pass

    def HLT(self):
        """
            Halt: It terminates the cpu processes
        """
        self.stop = True

    def LDI(self):
        """
        LDI register immediate
        Set the value of a register to an integer.
        """
        # Register number/ Memory Location
        operand_a = self.ram_read(self.pc + 1)
        # Value to be stored
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def LD(self):
        print("LD not implemented yet")
        pass

    def ST(self):
        print("ST not implemented yet")
        pass

    def PUSH(self):
        print("PUSH not implemented yet")
        pass

    def POP(self):
        print("POP not implemented yet")
        pass

    def PRN(self):
        """
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        """
        # Register number/ Memory Location
        operand_a = self.ram_read(self.pc + 1)
        # Value to be stored
        operand_b = self.reg[operand_a]
        print(operand_b)
        self.pc += 2

    def PRA(self):
        print("PRA not yet implimented")
        pass

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        IR = self.ram_read(self.pc)  # Instruction register
        # Register number
        operand_a = self.ram_read(self.pc + 1)
        # Value
        operand_b = self.ram_read(self.pc + 2)
        branchTable = {
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100100: self.MOD,
            0b01100101: self.INC,
            0b01100110: self.DEC,
            0b10100111: self.CMP,
            0b10101000: self.AND,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b10101011: self.XOR,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b01010111: self.JGT,
            0b01011000: self.JLT,
            0b01011001: self.JLE,
            0b01011010: self.JGE,
            0b00000000: self.NOP,
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b10000011: self.LD,
            0b10000100: self.ST,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01000111: self.PRN,
            0b01001000: self.PRA
        }
        #  if else for various actions
        #  After running code for any particular instruction,
        #  the PC needs to be updated to point to the
        #  next instruction for the next iteration of the loop in run().
        #  The number of bytes an instruction uses can be determined
        #  from the two high bits (bits 6-7) of the instruction opcode.
        #  See the LS-8 spec for details.
        while not self.stop:
            # HLT
            # Halt the CPU (and exit the emulator).
            # Machine code: # 00000001
            if IR in branchTable:
                IR = self.ram_read(self.pc)  # Instruction register
                print(f"IR is {IR}")
                self.trace()
                branchTable[IR]()
            else:
                print(
                    "ERROR: PASSED WRONG ARG TO CPU")
