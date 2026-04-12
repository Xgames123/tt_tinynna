# Wiring docs

Information of buses and wires

# soc.dig

Main file

# memory_controller.dig

Uses QPI protocol to talk to the PSRAMs and flash on the QSPI PMOD.

## Configuration

- Flash turn on QPI mode (0x38) and use 4 dummy cycles and 64 byte wrap (0xC0 followed by 0x8C)
- PSRAM's turn on QPI mode (0x35) (note: different opcodes than the flash)

## Timings

- PSRAM ^tACLK `5ns`

# nna8v2_mpu_mux.dig

Version of the processor without tri-state logic

## Instruction

- `curop` The opcode of current instruction.
- `arg` The combined arguments of the current instruction.
- `arg0` First argument of the current instruction
- `arg1` Second argument of the current instruction
- `xcycle` Indicates that the current clock cycle is the second cycle of a two cycle instruction. During a second cycle the databus is released by _pc_.
- `xcycle_next` Indicates that the next clock cycle will be an xcycle

### cal

Related to the cal instruction

- `cal_rslt` The answer of the calculation in `co` applied between `regout_arg0` and `regout_arg1`
- `co_add` high when the `co` register contains the add instruction

## Data

- `data_in` Data at the memory location specified by `addr_out`;
- `addr_out` Contains the memory location were `data_out` will written or where data will be read into `data_in`.
- `bank` Contains the currently selected bank.
- `addr_out` Combined `addr` and `bank` in big endian format.
- `data_w` Data write. Signals that current instruction wants to write the data on `addr_out` to the location in `addr_out`.
- `data_r` Data read. Signals that current instruction wants to read the data on location `addr_out` (passed via `data_in`).
- `data_rw` Indicates that the processor wants to read or write data.

### Registries

- `selreg` Selected register, value is based on arg0 and extra logic to handle lil and lih
- `regin` Data that will be written to the selected register
- `reg_we` Indicates that data on regin will be written to the selected register
