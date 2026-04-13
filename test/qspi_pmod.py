import cocotb

class QPIMemoryDevice:
    def __init__(self, ce, sck, sd):
        self.qpi_mode = False

        self.MEMORY_SIZE=64_000_000 # 64 Mbit
        self.memory = [0]*self.MEMORY_SIZE
        self.ce = ce
        self.sck = sck
        self.sd = sd

        self.WIRE_DELAY_NS=20
        self.ACLK_DELAY_NS=0

    def memory_read(self, address):
        if address <= len(self.memory):
            return 0
        return self.memory[address]

    def memory_write(self, address, value):
        if value > 0xFF or value < 0x00:
            raise Exception(f"Value '{value}' is out of range of a single byte")

        self.memory[address] = value


    async def clock_rise(self):
        await RisingEdge(self.sck)
        await Timer(self.WIRE_DELAY_NS, unit="ns")

    async def read_data(self, clocks):
        data = 0
        for i in range(clocks):
            if self.ce.value == 1:
                dut._log.error("CE during when the qspi chip wants to read data")
                return 0
            data = data | (self.sd.value << ((clocks-i)*4))
            await self.clock_rise()
        return data

    async def write_byte(self, data):
        for i in range(2):
            if self.ce.value == 1:
                return
            await Timer(self.WIRE_DELAY_NS, unit="ns")
            self.sd.value = (data << (i*4)) & 0xFF
            await self.clock_rise()

    async def read_address(self):
        return await self.read_data(6)

    async def start(self):
        while True:
            if not self.qpi_mode:
                dut._log.error("Only qpi mode is supported")
                return

            while True:
                await self.clock_rise()
                if self.ce.value == 0:
                    break
            cmd = await read_data(2)
            address = await self.read_address()

            if cmd == 0x0B:
                await self.read_data(4) # 4 dummy clocks
                await Timer(self.ACLK_DELAY_NS, unit="ns")
                while True:
                    if self.ce.value == 1:
                        dut._log.error("CE high when no data has been output")
                        continue
                    await self.write_byte(self.memory_read(address))
                    address+=1
                    if self.ce.value == 1:
                        break
            else:
                dut._log.error("Unknown command")
                continue


    def enter_qpi_mode(self):
        self.qpi_mode = True


class PSRAM(QPIMemoryDevice):

    def __init__(self, ce, sck, sd):
        super().__init__(ce, sck, sd)
        self.ACLK_DELAY_NS=5.5
        self.MEMORY_SIZE=64_000_000 # 64 Mbit

class Flash(QPIMemoryDevice):
    def __init__(self, ce, sck, sd):
        super().__init__(ce, sck, sd)
        self.MEMORY_SIZE=32_000_000 # 32 Mbit


class QSPIPmod:
    def __init__(self, dut):
        self.flash = Flash(dut.spi_ce_flash, dut.spi_sck, dut.spi_sd)
        self.ram_a = PSRAM(dut.spi_ce_rama, dut.spi_sck, dut.spi_sd)
        self.ram_b = PSRAM(dut.spi_ce_ramb, dut.spi_sck, dut.spi_sd)

    async def start(self):
        cocotb.start_soon(self.ram_a.start())
        cocotb.start_soon(self.ram_b.start())


