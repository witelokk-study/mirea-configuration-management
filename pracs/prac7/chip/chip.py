import os
import sys
from random import randint
from pathlib import Path


class Chip:
    def __init__(self, font, rom):
        self.mem = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 512
        self.sp = 0
        self.stack = [0] * 16
        self.scr = [0] * (64 * 32)
        self.key = [0] * 16
        self.delay_timer = 0
        self.sound_timer = 0
        for i in range(80):
            self.mem[i] = font[i]
        for i in range(len(rom)):
            self.mem[i + 512] = rom[i]


def step(chip):
    mem, V, stack, scr, key = chip.mem, chip.V, chip.stack, chip.scr, chip.key
    npc = chip.pc + 2
    opc = mem[chip.pc] << 8 | mem[chip.pc + 1]
    op1 = opc & 0xf000
    op2 = opc & 0xf00f
    op3 = opc & 0xf0ff
    if opc == 0x00e0:
        #TODO
        pass
    elif opc == 0x00ee:
        chip.sp -= 1
        npc = stack[chip.sp]
        npc += 2
    elif op1 == 0x1000:
        npc = opc & 0x0fff
    elif op1 == 0x2000:
        stack[chip.sp] = chip.pc
        chip.sp += 1
        npc = opc & 0x0fff
    elif op1 == 0x3000:
        if V[(opc & 0x0f00) >> 8] == (opc & 0x00ff):
            npc = chip.pc + 4
    elif op1 == 0x4000:
        if V[(opc & 0x0f00) >> 8] != (opc & 0x00ff):
            npc = chip.pc + 4
    elif op1 == 0x5000:
        if V[(opc & 0x0f00) >> 8] == V[(opc & 0x00f0) >> 4]:
            npc = chip.pc + 4
    elif op1 == 0x7000:
        #TODO
        V[(opc & 0x0f00) >> 8] += (opc & 0x00ff)
    elif op2 == 0x8000:
        V[(opc & 0x0F00) >> 8] = V[(opc & 0x00F0) >> 4]
    elif op2 == 0x8001:
        V[(opc & 0x0F00) >> 8] |= V[(opc & 0x00F0) >> 4]
    elif op2 == 0x8002:
        V[(opc & 0x0F00) >> 8] &= V[(opc & 0x00F0) >> 4]
    elif op2 == 0x8003:
        V[(opc & 0x0F00) >> 8] ^= V[(opc & 0x00F0) >> 4]
    elif op2 == 0x8004:
        V[(opc & 0x0F00) >> 8] += V[(opc & 0x00F0) >> 4]
        if V[(opc & 0x00F0) >> 4] > (0xFF - V[(opc & 0x0F00) >> 8]):
            V[0xF] = 1
        else:
            V[0xF] = 0
    elif op2 == 0x8005:
        #TODO
        if V[(opc & 0x00F0) >> 4] > V[(opc & 0x0F00) >> 8]:
            V[0xF] = 0
        else:
            V[0xF] = 1
        V[(opc & 0x0F00) >> 8] -= V[(opc & 0x00F0) >> 4]
    elif op2 == 0x8006:
        V[0xF] = V[(opc & 0x0F00) >> 8] & 0x1
        V[(opc & 0x0F00) >> 8] >>= 1
    elif op2 == 0x8007:
        #TODO
        if V[(opc & 0x0F00) >> 8] > V[(opc & 0x00F0) >> 4]:
            V[0xF] = 0
        else:
            V[0xF] = 1
        V[(opc & 0x0F00) >> 8] = V[(opc & 0x00F0) >> 4] - V[(opc & 0x0F00) >> 8]
    elif op2 == 0x800e:
        #TODO
        V[0xF] = V[(opc & 0x0F00) >> 8] >> 7
        V[(opc & 0x0F00) >> 8] <<= 1
    elif op1 == 0x9000:
        if V[(opc & 0x0F00) >> 8] != V[(opc & 0x00F0) >> 4]:
            npc = chip.pc + 4
    elif op1 == 0xa000:
        chip.I = opc & 0x0FFF
    elif op1 == 0xb000:
        npc = (opc & 0x0FFF) + V[0]
    elif op1 == 0xc000:
        V[(opc & 0x0F00) >> 8] = randint(0, 255) & (opc & 0x00FF)
    elif op1 == 0xd000:
        #TODO
        x = V[(opc & 0x0F00) >> 8]
        y = V[(opc & 0x00F0) >> 4]
        height = opc & 0x000F
        V[0xF] = 0
        for yline in range(height):
            pixel = mem[chip.I + yline]
            for xline in range(8):
                if (pixel & (0x80 >> xline)) != 0:
                    if scr[(x + xline + ((y + yline) * 64))] == 1:
                        V[0xF] = 1
                    scr[x + xline + ((y + yline) * 64)] ^= 1
    elif op3 == 0xe09e:
        if key[V[(opc & 0x0F00) >> 8]] != 0:
            npc = chip.pc + 4
    elif op3 == 0xe0a1:
        if key[V[(opc & 0x0F00) >> 8]] == 0:
            npc = chip.pc + 4
    elif op3 == 0xf007:
        V[(opc & 0x0F00) >> 8] = chip.delay_timer
    elif op3 == 0xf00a:
        #TODO
        pass
    elif op3 == 0xf015:
        chip.delay_timer = V[(opc & 0x0F00) >> 8]
    elif op3 == 0xf018:
        chip.sound_timer = V[(opc & 0x0F00) >> 8]
    elif op3 == 0xf01e:
        if chip.I + V[(opc & 0x0F00) >> 8] > 0xFFF:
            V[0xF] = 1
        else:
            V[0xF] = 0
        chip.I += V[(opc & 0x0F00) >> 8]
    elif op3 == 0xf029:
        chip.I = V[(opc & 0x0F00) >> 8] * 0x5
    elif op3 == 0xf033:
        mem[chip.I] = V[(opc & 0x0F00) >> 8] // 100
        mem[chip.I + 1] = (V[(opc & 0x0F00) >> 8] // 10) % 10
        mem[chip.I + 2] = V[(opc & 0x0F00) >> 8] % 10
    elif op3 == 0xf055:
        for i in range(((opc & 0x0F00) >> 8) + 1):
            mem[chip.I + i] = V[i]
        chip.I += ((opc & 0x0F00) >> 8) + 1
    elif op3 == 0xf065:
        for i in range(((opc & 0x0F00) >> 8) + 1):
            V[i] = mem[chip.I + i]
        chip.I += ((opc & 0x0F00) >> 8) + 1
    else:
        print("invalid opcode 0x%x at 0x%x" % (opc, chip.pc))
        sys.exit(1)
    if chip.delay_timer > 0:
        chip.delay_timer -= 1
    if chip.sound_timer > 0:
        chip.sound_timer -= 1
    chip.pc = npc


font = Path("font.bin").read_bytes()
rom = Path("roms/pong2.rom").read_bytes()
chip = Chip(font, rom)
while True:
    step(chip)
