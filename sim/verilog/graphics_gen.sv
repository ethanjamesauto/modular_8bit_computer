module graphics_gen(
    input logic clk,
    input logic reset_n,
    input logic [9:0] SW,
    input logic [9:0] hcount, vcount,
    input logic [7:0] frame_count,
    output logic [7:0] red, green, blue,
	 
    input logic [9:0] player_hpos,
    input logic [8:0] player_vpos,
    input logic [9:0] background_pos,
    input logic [2:0] player_sprite_count,
    input logic player_sprite_reverse
);

/*
Driver logic for the ground texture ROM
*/
logic [3:0] tile;
assign tile = vcount[8:5];
logic [4:0] ground_pos;
assign ground_pos = hcount[4:0] - background_pos[4:0];

logic [2:0] ground_idx;
logic [23:0] rgb;
ground_tex_rom ground_tex0(clk, 1'b1, {vcount[4:1], ground_pos[4:1]}, ground_idx);

always_comb case (ground_idx)
0: rgb = 24'd2564148;1: rgb = 24'd2851379;2: rgb = 24'd3560573;3: rgb = 24'd3615827;4: rgb = 24'd6019404;5: rgb = 24'd8793146;6: rgb = 24'd12800060;7: rgb = 24'd15632965;
default: rgb = 24'bx;
endcase


/*
Driver logic for the character sprite ROM
*/
localparam PLAYER_SIZE = 64;

logic [23:0] character_rgb;
logic [3:0] character_idx;
logic [4:0] char_haddr, char_vaddr;

always_comb begin
    char_vaddr = vcount[5:1] - player_vpos[5:1];
    char_haddr = hcount[5:1] - player_hpos[5:1];
    if (player_sprite_reverse) char_haddr = PLAYER_SIZE - 1 - char_haddr;
end

character_rom character_rom0(clk, 1'b1, {1'b0, player_sprite_count, char_vaddr, char_haddr}, character_idx);

always_comb case (character_idx)
0: character_rgb = 24'd0; 1: character_rgb = 24'd2445881; 2: character_rgb = 24'd2564148; 3: character_rgb = 24'd2851379; 4: character_rgb = 24'd3560573; 5: character_rgb = 24'd3615827; 6: character_rgb = 24'd6019404; 7: character_rgb = 24'd6133901; 8: character_rgb = 24'd8793146; 9: character_rgb = 24'd12800060; 10: character_rgb = 24'd15632965; 11: character_rgb = 24'd16182332; 
default: character_rgb = 24'bx;
endcase

/*
Driver logic for tree (background) ROM
*/
localparam TREE_START = 7'd64;
localparam TREE_HEIGHT = 8'd128;
localparam TREE_WIDTH = 7'd73;
logic [7:0] tree_offset;
assign tree_offset = hcount[7:0] - background_pos[7:0];
logic tree_val;

background_rom background_rom0(clk, 1'b1, {tree_offset[7:1], vcount[7:1] - TREE_START}, tree_val);

/*
Main RGB output logic
*/
always_comb begin
    automatic logic [9:0] poop = background_pos + TREE_WIDTH*2;
    if (character_idx != 0 // see if the player is transparent as this location
		&& hcount >= player_hpos && hcount < player_hpos + PLAYER_SIZE // see if the player is at this horizontal location
		&& vcount >= player_vpos && vcount < player_vpos + PLAYER_SIZE) // see if the player is at this vertical location
	begin
        red = character_rgb[23:16];
        green = character_rgb[15:8];
        blue = character_rgb[7:0];
    end else if (tree_val && vcount >= TREE_START*2 && vcount < (TREE_START + TREE_HEIGHT)*2 // see if the tree is at this vertical location
            && (hcount >= background_pos || background_pos >= 1024-TREE_WIDTH*2) && hcount < poop) begin // see if the tree is at this horizontal location
        red = 54; green = 84; blue = 125; // draw the color of the tree
    end else if (tile == 12) begin // draw the ground tiles
        red = rgb[23:16];
        green = rgb[15:8];
        blue = rgb[7:0];
    end else if (tile > 12) begin // draw the area below the ground
        red = 39; green = 32; blue = 52;
    end else begin
        red = 0; green = 17; blue = 71; // draw the sky
    end
end

endmodule