module vga_driver(
	input logic clk, reset_n,
	input logic [9:0] sw,
    input logic [3:0] key,
	output logic vga_sync_n, vga_blank_n, vga_hs, vga_vs,
	output logic [7:0] vga_r, vga_g, vga_b,
    output logic [9:0] hcount, vcount
);

logic new_frame;
logic [7:0] frame_count;
logic [9:0] player_hpos;
logic [8:0] player_vpos;
logic [9:0] background_pos;
logic [2:0] player_sprite_count;
logic player_sprite_reverse;

logic [7:0] vga_r_a, vga_g_a, vga_b_a;
logic vga_blank_n_a, vga_hs_a, vga_vs_a;

// this signal isn't used
assign vga_sync_n = 1'b0;

// I originally thought that there might be a need to delay/synchronize these signals,
// but this ended up not being the case. This just passes the signals through.
always_comb begin
    vga_r = vga_r_a;
    vga_g = vga_g_a;
    vga_b = vga_b_a;
end

// delay these signals by a clock cycle to match the ROM read latency
always_ff @(posedge clk) begin
    vga_blank_n <= vga_blank_n_a;
    vga_hs <= vga_hs_a;
    vga_vs <= vga_vs_a;
end

vga_controller vga0(
	.vga_clk(clk),
	.reset_n(reset_n),
	.blank_n(vga_blank_n_a),
	.hsync_n(vga_hs_a),
	.vsync_n(vga_vs_a),
	.hcount(hcount),
	.vcount(vcount),
	.new_frame(new_frame)
);

graphics_gen gen0(
    .clk(clk),
    .reset_n(reset_n),
    .SW(sw),
    .hcount(hcount),
    .vcount(vcount),
    .frame_count(frame_count),
    .red(vga_r_a),
    .green(vga_g_a),
    .blue(vga_b_a),
    .player_hpos(player_hpos),
    .player_vpos(player_vpos),
    .background_pos(background_pos),
    .player_sprite_count(player_sprite_count),
    .player_sprite_reverse(player_sprite_reverse)
);

game_fsm game_fsm0(
    .clk(clk),
    .reset_n(reset_n),
    .sw(sw),
    .key(key),
    .hcount(hcount),
    .vcount(vcount),
    .new_frame(new_frame),
    .frame_count(frame_count),
    .player_hpos(player_hpos),
    .player_vpos(player_vpos),
    .background_pos(background_pos),
    .player_sprite_count(player_sprite_count),
    .player_sprite_reverse(player_sprite_reverse)
);

endmodule