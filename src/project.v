/*
 * Copyright (c) 2026 Xgames123
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none
`include "./nna8v2.v"

module tt_um_xgames123_nna8v2 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  wire brk;
  wire r;
  wire w;
  wire [15:0] addr_out = 0;

  nna8v2_mpu cpu(
    .clk(clk),
    .data_in( uio_in ),
    .data_out( uio_out ),
    .addr_out( addr_out ),
    .w( uo_out[0] ),
    .r( uo_out[1] ),
    .brk( uo_out[2] ),
    .rst(rst_n)
  );
endmodule
