"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Registers
        self.reg = [0]*8
        # program counter
        self.pc = 0
        # flag
        self.fl = 0
        # self.e_fl = 0
        # self.l_fl = 0
        # self.g_fl = 0
        self.ram = [0]*256
        self.stop = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "CMP":
            # Flag example
            # `AA B C DDDD`
            #  00 0 0 0LGE
            #  10 1 0 0111
            reg_a_value = self.reg[reg_a]
            reg_b_value = self.reg[reg_b]
            if reg_a_value > reg_b_value:
                self.fl = 0b00000010
            elif reg_a_value == reg_b_value:
                self.fl = 0b00000001
            elif reg_a_value < reg_b_value:
                self.fl = 0b00000100
        elif op == "MOD":
            self.reg[reg_a]

        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         # self.fl,
    #         # self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')
    def trace(self, LABEL=str()):

        print(f"{LABEL} TRACE --> PC: %02i | RAM: %03i %03i %03i | Register: " % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02i" % self.reg[i], end='')
        print(" | Stack:", end='')

        for i in range(240, 244):
            print(" %02i" % self.ram_read(i), end='')
        print()

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ALU Functions

    def ADD(self):
        """Add the value in two registers and store the result in registerA."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('ADD', reg_a, reg_b)
        self.pc += 3

    def SUB(self):
        """Subtract the value in the second register from the first, storing the result in registerA."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('SUB', reg_a, reg_b)
        self.pc += 3

    def MUL(self):
        """Multiply the values in two registers together and store the result in registerA."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def DIV(self):
        """Divide the value in the first register
        by the value in the second,
        storing the result in registerA.
        If the value in the second register is 0,
        the system should print an error message and halt."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('DIV', reg_a, reg_b)
        self.pc += 3

    def MOD(self):
        """Divide the value in the first register by the value in the second, 
        storing the remainder of the result in registerA.
        If the value in the second register is 0, 
        the system should print an error message and halt."""
        print("MOD not implemented yet")
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+1)
        self.alu("MOD", reg_a, reg_b)
        self.pc += 2

    def INC(self):
        """Increment (add 1 to) the value in the given register."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = None
        self.alu("INC", reg_a, reg_b)
        self.pc += 2

    def DEC(self):
        """Decrement (subtract 1 from) the value in the given register."""
        reg_a = self.ram_read(self.pc+1)
        reg_b = None
        self.alu("DEC", reg_a, reg_b)
        self.pc += 2

    def CMP(self):
        # print("Compare Ran")
        """
        Compare the values in two registers.
        If they are equal, set the Equal E flag to 1, otherwise set it to 0.
        If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
        If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
        """
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    def AND(self):
        print("AND not implemented yet")
        pass

    def NOT(self):
        """Perform a bitwise-NOT on the value in a register,
        storing the result in the register."""
        print("NOT not implemented yet")
        pass

    def OR(self):
        """Perform a bitwise-OR between the values in registerA and registerB,
        storing the result in registerA."""
        print("OR not implemented yet")
        pass

    def XOR(self):
        """Perform a bitwise-XOR between the values in registerA and registerB,
        storing the result in registerA."""
        print("XOR not implemented yet")
        pass

    def SHL(self):
        """Shift the value in registerA left by the number
        of bits specified in registerB,
        filling the low bits with 0."""
        print("SHL not implemented yet")
        pass

    def SHR(self):
        """Shift the value in registerA right by the number of bits specified in registerB,
        filling the high bits with 0."""
        print("SHR not implemented yet")
        pass

    # PC Mutator

    def CALL(self):
        print("Call Ran")
        """1. The address of the ***instruction*** _directly after_ `CALL`
        is pushed onto the stack.
        This allows us to return to where we left off when the subroutine finishes executing.
        2. The PC is set to the address stored in the given register.
        We jump to that location in RAM and execute the first instruction in the subroutine.
        The PC can move forward or backwards from its current location."""
        # push the address of pc+1 onto the stack
        # Set the PC to the value stored at the given register
        # Jump to that register specified
        return_addr = self.pc+2

        # Push on the stack
        self.reg[7] -= 1
        self.ram[self.reg[7]] = return_addr

        # Get the address for the call
        reg_num = self.ram[self.pc+1]
        subroutine_addr = self.reg[reg_num]
        # Call it
        self.pc = subroutine_addr

    def RET(self):
        """ 
            Return from subroutine.
            Pop the value from the top of the stack and store it in the PC.
        """

        # Copy the value from memory at the address pointed to by SP
        top_of_stack = self.reg[7]
        return_addr = self.ram[top_of_stack]
        self.pc = return_addr
        self.reg[7] += 1

    def INT(self):
        print("INT not implemented yet")
        pass

    def IRET(self):
        print("IRET not implemented yet")
        pass

    def JMP(self):
        # print("JMP Ran")
        """Jump to the address stored in the given register.
        Set the PC to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        self.pc = self.reg[location]

    def JEQ(self):
        # print("JEQ Ran")
        """JEQ register
        If equal flag is set (true), jump to the address stored in the given register. """
        # if reg_a_value > reg_b_value:
        #         self.fl = 0b00000010
        #     elif reg_a_value == reg_b_value:
        #         self.fl = 0b00000001
        #     elif reg_a_value < reg_b_value:
        #         self.fl = 0b00000100
        location = self.ram_read(self.pc + 1)
        if self.fl == 0b00000001:
            self.pc = self.reg[location]
        else:
            self.pc += 2

    def JNE(self):
        # print("JNE Ran")
        """If E flag is clear (false, 0),
        jump to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        if self.fl != 0b00000001:
            # print(self.pc+1)
            self.pc = self.reg[location]
        else:
            self.pc += 2

    def JGT(self):
        # print("JGT Ran")
        """If greater-than flag is set (true),
        jump to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        if self.fl == 0b00000010:
            self.pc = self.reg[location]
        else:
            self.pc += 2

    def JLT(self):
        # print("JLT Ran")
        """If less-than flag is set (true), jump to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        if self.fl == 0b00000100:
            self.pc = self.reg[location]
        else:
            self.pc += 2

    def JLE(self):
        # print("JLE Ran")
        """If less-than flag or equal flag is set (true),
        jump to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        if self.fl == 0b00000100 or self.fl == 0b00000001:
            self.pc = self.reg[location]
        else:
            self.pc += 2

    def JGE(self):
        # print("JGE Ran")
        """If greater-than flag or equal flag is set (true),
        jump to the address stored in the given register."""
        location = self.ram_read(self.pc + 1)
        if self.fl == 0b00000010 or self.fl == 0b00000001:
            self.pc = self.reg[location]
        else:
            self.pc += 2

    # Other

    def NOP(self):
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
        # print("LDI Ran")
        # Register number/ Memory Location
        operand_a = self.ram_read(self.pc + 1)
        # Value to be stored
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def LD(self):
        """Loads registerA with the value at the memory address stored in registerB."""
        print("LD not implemented yet")
        pass

    def ST(self):
        """Store value in registerB in the address stored in registerA."""
        print("ST not implemented yet")
        pass

    def PUSH(self):
        """Places something on the stack, stored in Ram"""
        # print("Push ran")
        # Decrement the sp (R7)
        self.reg[7] -= 1
        # Copy the value given to the address pointed by SP
        reg_num = self.ram[self.pc+1]
        value = self.reg[reg_num]
        # Figure where to put it
        top_of_stack_addr = self.reg[7]
        # put it there
        self.ram[top_of_stack_addr] = value
        self.pc += 2

    def POP(self):
        # print("POP ran")
        # Copy the value from memory at the address pointed to by SP
        address = self.reg[7]
        value = self.ram[address]
        reg_num = self.ram[self.pc+1]
        self.reg[reg_num] = value
        # Increment the SP
        self.reg[7] += 1
        self.pc += 2

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
        """Print alpha character value stored in the given register.
        Print to the console the ASCII character corresponding to the value in the register."""
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
        # operand_a = self.ram_read(self.pc + 1)
        # # Value
        # operand_b = self.ram_read(self.pc + 2)
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
            0b01000101: self.PUSH,  # implemented
            0b01000110: self.POP,  # implemented
            0b01000111: self.PRN,  # implemented
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
                # print(f"IR is {IR}")
                # self.trace()
                branchTable[IR]()
            else:
                print(
                    "ERROR: PASSED WRONG ARG TO CPU")
