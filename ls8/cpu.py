"""CPU functionality."""

import sys

OP1 = 0b10000010 # LDI
OP2 = 0b01000111 # PRN
OP3 = 0b10100010 # MUL
OP4 = 0b01000101 # PUSH
OP5 = 0b01000110 # POP
OP6 = 0b00000001 # HALT
OP7 = 0b01010000 # CALL
OP8 = 0b00010001 # RET
OP9 = 0b10100000 # ADD

class CPU:
    """Main CPU class."""

    def __init__(self, reg = [0] * 8, ram = [0] * 256, pc = 0):
        """Construct a new CPU."""
        self.reg = reg
        self.ram = ram
        self.pc = pc
        self.sp = 244
        self.running = True 

    def load(self):
        """Load a program into memory."""

        program = []
        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                l = line.split('#')
                operation = l[0].strip()
                try:
                    program.append(int(operation, 2))
                except ValueError:
                    pass

        for operation in program:
            self.ram[address] = operation
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, register):
        return self.ram[register]

    def ram_write(self, register, address):
        self.ram[address] = register

    def hlt(self):
        self.running = False

    def ldi(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value

    def prn(self):
        address = self.ram[self.pc + 1]
        print(self.reg[address])

    def mul(self):
        value_1 = self.ram[self.pc + 1]
        value_2 = self.ram[self.pc + 2]
        self.alu("MUL", value_1, value_2)

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.pc
            operation = self.ram[ir]
            # Perform operation here

