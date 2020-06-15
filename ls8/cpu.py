"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8
        self.pc = 0
        self.ram = []

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

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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

    def run(self):
        """Run the CPU."""
        ir = self.pc
        operand_a = ram_read(self.pc + 1)
        operand_b = ram_read(self.pc + 2)
        #  if else for various actions
        #  After running code for any particular instruction,
        #  the PC needs to be updated to point to the
        #  next instruction for the next iteration of the loop in run().
        #  The number of bytes an instruction uses can be determined
        #  from the two high bits (bits 6-7) of the instruction opcode.
        #  See the LS-8 spec for details.

# HLT
# HLT

# Halt the CPU (and exit the emulator).

# Machine code:

# 00000001
# 01


#         LDI
# LDI register immediate

# Set the value of a register to an integer.

# Machine code:

# 10000010 00000rrr iiiiiiii
# 82 0r ii

        pass

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
