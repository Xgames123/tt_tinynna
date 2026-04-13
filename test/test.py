# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles,FallingEdge,RisingEdge
from qspi_pmod import QSPIPmod


async def reset(dut):
    await FallingEdge(dut.clk)
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


@cocotb.test()
async def memory_controller_test(dut):
    memory_controller = dut.user_project.soc.memory_controller_i1

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset(dut)
    dut._log.info("Memory controller test")

    pmod = QSPIPmod(dut)
    pmod.flash.memory_write(0, 0x1D)
    pmod.start()

    dut._log.info(dut.spi_ce_rama)
    assert dut.spi_ce_rama.value == 1
    assert dut.spi_ce_ramb.value == 1
    assert dut.spi_ce_flash.value == 1

    await FallingEdge(dut.spi_ce_flash)
    assert memory_controller.addr_in.value == 0 # read address 0
    assert memory_controller.data_ready.value == 0
    await RisingEdge(memory_controller.data_ready)
    assert memory_controller.data_out.value == 0x1D


# @cocotb.test()
# async def test_project(dut):
#     dut._log.info("Start")
#
#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, unit="us")
#     cocotb.start_soon(clock.start())
#
#     reset(dut)

    # dut._log.info("Test project behavior")
    #
    # # Set the input values you want to test
    # dut.ui_in.value = 20
    # dut.uio_in.value = 30
    #
    # # Wait for one clock cycle to see the output values
    # await ClockCycles(dut.clk, 1)
    #
    # # The following assersion is just an example of how to check the output values.
    # # Change it to match the actual expected output of your module:
    # assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
