`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  // QSPI PMOD mappings
  wire spi_sck = uio_out[3];

  wire spi_ce_flash = uio_out[0];
  wire spi_ce_rama = uio_out[6];
  wire spi_ce_ramb = uio_out[7];
  
  wire spi_sd3 = uio_oe[5] ? uio_out[5] : 'z;
  wire spi_sd2 = uio_oe[4] ? uio_out[4] : 'z;
  wire spi_sd1 = uio_oe[2] ? uio_out[2] : 'z;
  wire spi_sd0 = uio_oe[1] ? uio_out[1] : 'z;

  wire [3:0] spi_sd;
  assign spi_sd = {spi_sd0, spi_sd1, spi_sd2, spi_sd3};

  assign uio_in = {uio_out[7:6], spi_sd3, spi_sd2, uio_out[3], spi_sd1, spi_sd0, uio_out[0]};

  // uio[0] CS0 (Flash)
  // uio[1] SD0/MOSI
  // uio[2] SD1/MISO
  // uio[3] SCK
  // uio[4] SD2
  // uio[5] SD3
  // uio[6] CS1 (RAM A)
  // uio[7] CS2 (RAM B)

  tt_um_xgames123_tinynna user_project (
    // include power ports for the Gate Level test
  `ifdef GL_TEST
      .VPWR( 1'b1),
      .VGND( 1'b0),
  `endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );

endmodule
