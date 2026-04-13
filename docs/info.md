## How it works

Example programs are available or you can write your own using the [nnaasm](https://github.com/Xgames123/nna/blob/main/spec/nnaasm.md) assembler.

An overview of the instructions and the processor can be found in the [nna github repo](https://github.com/Xgames123/nna/blob/main/spec/nna8v3.md)

Other versions of the `nna` architecture can also be found in the [nna github repo](https://github.com/Xgames123/nna)

## How to test

Load one of the test programs on the flash.

Reset the design as follows:

- Hold `rst_n` and clock low
- Put both the PSRAMs and the flash in QPI mode
- Configure the flash to use 4 dummy cycles.
- Clock once with `rst_n` still low
- Put `rst_n` high and clock normally

## External hardware

The design is intended to be used with this QSPI PMOD on the bidirectional PMOD. This has a 16MB flash and 2 8MB RAMs.

## Generating verilog code

The logic is made using [Hneemann's Digital](https://github.com/hneemann/digital).
To generate the `tinynna.v` file open the src/digital/soc.dig file and click export > verilog.
