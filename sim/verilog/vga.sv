// this module just contains the PLL and vga driver
module vga(
	input logic CLOCK_50,
	input logic [9:0] SW,
	input logic [3:0] KEY_N,
	output logic VGA_SYNC_N, VGA_BLANK_N, VGA_HS, VGA_VS, VGA_CLK,
	output logic [7:0] VGA_R, VGA_G, VGA_B,
	output logic [9:0] hcount, vcount
);

logic reset_n;
assign reset_n = KEY_N[3];

pll vga_pll(.refclk(CLOCK_50), .rst(1'b0), .outclk_0(VGA_CLK));

vga_driver vga_driver0(
	.clk(VGA_CLK),
	.reset_n(reset_n),
	.sw(SW),
	.key(KEY_N),
	.vga_sync_n(VGA_SYNC_N), .vga_blank_n(VGA_BLANK_N), .vga_hs(VGA_HS), .vga_vs(VGA_VS),
	.vga_r(VGA_R), .vga_g(VGA_G), .vga_b(VGA_B),
	.hcount(hcount), .vcount(vcount)
);

endmodule