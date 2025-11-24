/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_traffic_gen (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Gán đầu vào từ chân chip
    wire [3:0] N_period = ui_in[3:0]; // 4 bit đầu làm chu kỳ N
    
    // Dây nối nội bộ
    wire [7:0] packet_id_internal;
    wire packet_type_internal;
    wire valid_internal;

    // Instance module Traffic Generator
    traffic_gen core (
        .clk(clk),
        .rst_n(rst_n),
        .N_period(N_period),
        .packet_id(packet_id_internal),
        .packet_type(packet_type_internal),
        .valid(valid_internal)
    );

    // Gán đầu ra
    assign uo_out = packet_id_internal;      // 8-bit Packet ID ra 8 chân output chính
    
    assign uio_out[0] = packet_type_internal; // Chân phụ 0: Loại gói (0: UL, 1: DL)
    assign uio_out[1] = valid_internal;       // Chân phụ 1: Valid
    assign uio_out[7:2] = 6'b0;               // Các chân còn lại gán 0
    
    // Cấu hình chiều: 1 là Output, 0 là Input
    assign uio_oe[1:0] = 2'b11; 
    assign uio_oe[7:2] = 6'b000000;
    
    // Xử lý biến không dùng để tránh warning
    wire _unused = &{ena, ui_in[7:4], uio_in, 1'b0};

endmodule

/* Module Traffic Generator (Logic chính) */
module traffic_gen (
    input wire clk,
    input wire rst_n,
    input wire [3:0] N_period,
    output reg [7:0] packet_id,
    output reg packet_type,
    output reg valid
);
    wire [7:0] ul_id, dl_id;
    reg ul_en, dl_en;
    
    // Hai bộ LFSR với Seed và Tap khác nhau
    lfsr_8bit #(.SEED(8'hAA), .TAPS(8'hB4)) lfsr_ul (.clk(clk), .rst_n(rst_n), .en(ul_en), .data_out(ul_id));
    lfsr_8bit #(.SEED(8'h55), .TAPS(8'hD8)) lfsr_dl (.clk(clk), .rst_n(rst_n), .en(dl_en), .data_out(dl_id));

    reg [3:0] counter;
    reg state; // 0: UL turn, 1: DL turn

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter <= 0; state <= 0; valid <= 0;
            ul_en <= 0; dl_en <= 0;
            packet_id <= 0; packet_type <= 0;
        end else begin
            ul_en <= 0; dl_en <= 0; valid <= 0;
            if (counter >= N_period) begin
                counter <= 0; valid <= 1;
                if (state == 0) begin 
                    packet_id <= ul_id; packet_type <= 0;
                    ul_en <= 1; state <= 1;
                end else begin 
                    packet_id <= dl_id; packet_type <= 1;
                    dl_en <= 1; state <= 0;
                end
            end else begin
                counter <= counter + 1;
            end
        end
    end
endmodule

/* Module LFSR 8-bit */
module lfsr_8bit #(parameter [7:0] SEED = 8'h1, parameter [7:0] TAPS = 8'hB4) (
    input wire clk, rst_n, en,
    output reg [7:0] data_out
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) data_out <= SEED;
        else if (en) begin
            wire feedback = ^(data_out & TAPS);
            data_out <= {data_out[6:0], feedback};
        end
    end
endmodule
