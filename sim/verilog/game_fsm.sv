module game_fsm(
    input logic clk,
    input logic reset_n,
    input logic [9:0] sw,
    input logic [3:0] key,
    input logic [9:0] hcount, vcount,
    input logic new_frame,
    output logic [7:0] frame_count,
    output logic [9:0] player_hpos,
    output logic [8:0] player_vpos,
    output logic [9:0] background_pos,

    output logic [2:0] player_sprite_count,
    output logic player_sprite_reverse
);

localparam START_POS = 200-32;      // player start position
localparam MIN_POS = 160-32;        // minimum player position
localparam MAX_POS = 320+160-32;    // maximum player position
localparam GROUND = 320;            // ground level (y)

logic signed [7:0] player_velocity; // the player's vertical velocity

enum logic [3:0] {IDLE, RIGHT, LEFT} player_state;
logic [5:0] move_count;

always_comb begin
    if (player_velocity < 0)
        player_sprite_count = 3'd5;
    else if (player_velocity > 0)
        player_sprite_count = 3'd6;
    else
        player_sprite_count = move_count[5:3];
end

always_ff @(posedge clk or negedge reset_n) begin
    if (~reset_n) begin
        move_count <= 6'b0;
    end else begin
        if (new_frame && (player_state != IDLE || move_count != 6'b0))
            move_count <= move_count + 6'b1;
    end
end

always_ff @(posedge clk or negedge reset_n) begin
    if (~reset_n) begin
        background_pos <= 10'd350;
        player_hpos <= START_POS;
        frame_count <= 8'b0;
        player_state <= IDLE;
        player_vpos <= GROUND;
        player_sprite_reverse <= 1'b0;
        player_velocity <= 8'sd0;
    end else begin
        if (new_frame) begin
            frame_count <= frame_count + 8'b1; // used for some animations

            if (~key[2] && player_vpos == GROUND) begin // jump
                player_velocity <= -8'sd14;
                player_vpos <= $signed({1'b0, player_vpos}) + player_velocity;
            end else begin
                if ($signed({1'b0, player_vpos}) + player_velocity >= GROUND) begin
                    player_vpos <= GROUND;
                    player_velocity <= 8'sd0;
                end else begin
                    player_vpos <= $signed({1'b0, player_vpos}) + player_velocity;
                    player_velocity <= player_velocity + 8'sd1;
                end
            end

            if (~key[0] && ~key[1]) begin // no movement

            end else if (~key[0]) begin // move right
                player_state <= RIGHT;
                player_sprite_reverse <= 1'b0;
                if (player_hpos < MAX_POS) 
                    player_hpos <= player_hpos + 10'd2; // move player
                else
                    background_pos <= background_pos - 10'd2; // move background
            end else if (~key[1]) begin // move left
                player_state <= LEFT;
                player_sprite_reverse <= 1'b1;
                if (player_hpos > MIN_POS)
                    player_hpos <= player_hpos - 10'd2; // move player
                else
                    background_pos <= background_pos + 10'd2; // move background
            end else begin
                player_state <= IDLE;
            end
        end
    end
end

endmodule