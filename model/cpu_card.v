module cpu_card(
	input wire VCC,
	input wire GND,
	input wire clk,				// generated by motherboard clock generator
	input wire rst_n,			// probably a button on the motherboard
	output reg we_n,			// active low
	output reg oe_n,			// active low
	inout wire [7:0] data,
	output reg [15:0] addr,	    // 64k address space is suppored by default. More address bits may be added later
	output wire int_n			// pulled up by motherboard; driven down by any peripheral (could be used for interrupts)
);

reg [7:0] dat_o;

reg [7:0] dat;
assign data = dat;
// "cpu card"
initial begin
	dat = 8'bz;
	addr = 16'h0;
	we_n = 1'b1;
	oe_n = 1'b1;
	delay(5);

	// write/read to simple card
	write(8'd25, 16'h4000);
	read(dat_o, 16'h4000);
	$display("Read: %h", dat_o);

	// write/read to alu card
	write(8'd50, 16'h5001);
	read(dat_o, 16'h5001);
	$display("Read: %h", dat_o);

	addr = 16'h0;
	$finish;
end

task write(input reg [7:0] dat_i, input reg [15:0] addr_i); begin
	dat = dat_i;
	addr = addr_i;
	we_n = 1'b0;
	delay(1);
	we_n = 1'b1;
end endtask

task read(output reg [7:0] dat_o, input reg [15:0] addr_i); begin
	dat = 8'bz;
	addr = addr_i;
	oe_n = 1'b0;
	delay(1);
	dat_o = data;
	oe_n = 1'b1;
end endtask

task delay(input integer cycles);
	repeat(cycles) @(posedge clk);
endtask

endmodule