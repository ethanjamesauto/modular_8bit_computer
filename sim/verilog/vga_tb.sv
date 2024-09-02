`timescale 1ns/1ns

module vga_tb;
logic clk = 0, reset_n = 1;

logic blank_n, hsync_n, vsync_n;
logic [9:0] hcount, vcount;
logic new_frame;
logic [7:0] frame_count;

bit [7:0] red, green, blue; // TODO: why does this not output correctly with logic?

vga_driver vga_driver0(
	.clk(clk),
	.reset_n(reset_n),
	.sw(10'b0),
	.key(4'b0),
	.vga_sync_n(blank_n), .vga_blank_n(), .vga_hs(hsync_n), .vga_vs(vsync_n),
	.vga_r(red), .vga_g(green), .vga_b(blue),
	.hcount(hcount), .vcount(vcount)
);


initial repeat(1000000) #10 clk = ~clk;

initial begin
	#20 reset_n = 0;
	#20 reset_n = 1;
end

// save a single frame output to a file
initial begin
	int fd;
	fd = $fopen("img.ppm", "wb");
	$fwrite(fd, "P6 640 480 255\n");
	while (1) begin
		@(negedge clk) begin
			if (vcount >= 480) break;
			if (hcount < 640) begin 
				// $display("%d\t%d\t%d", red, green, blue);
				$fwrite(fd, "%c%c%c", red, green, blue);
			end
		end
	end
	$fclose(fd);
	$stop;
end

endmodule