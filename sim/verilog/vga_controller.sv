module vga_controller(
	input  logic vga_clk,
	input  logic reset_n,
	output logic blank_n,
	output logic hsync_n,
	output logic vsync_n,
	output logic [9:0] hcount,
	output logic [9:0] vcount,
	output logic new_frame
);

localparam active_h = 0;
localparam front_porch_h = active_h+640;
localparam sync_pulse_h = front_porch_h+16;
localparam back_porch_h = sync_pulse_h+96; 
localparam total_h = back_porch_h+48;

localparam active_v = 0;
localparam front_porch_v = active_v+480;
localparam sync_pulse_v = front_porch_v+10;
localparam back_porch_v = sync_pulse_v+2;
localparam total_v = back_porch_v+33;

// sync and blanking signal logic
always_comb begin
	hsync_n = !(hcount >= sync_pulse_h && hcount < back_porch_h);
	vsync_n = !(vcount >= sync_pulse_v && vcount < back_porch_v);
	blank_n = !(hcount >= front_porch_h || vcount >= front_porch_v);
end

// horizontal and vertical counter logic
always_ff @(posedge vga_clk or negedge reset_n) begin
	if (~reset_n) begin
		hcount <= 10'd0;
		vcount <= 10'd0;
		new_frame <= 1'b0;
	end else
	begin
		new_frame <= 1'b0;
		if (hcount == total_h-1) begin // TODO: will >= use less LUTs?
			if (vcount == total_v-1) begin
				vcount <= 10'd0;
				new_frame <= 1'b1;
			end else begin
				vcount <= vcount + 10'd1;
			end
			hcount <= 10'd0;
		end else begin
			hcount <= hcount + 10'd1;
		end
	end
end

endmodule