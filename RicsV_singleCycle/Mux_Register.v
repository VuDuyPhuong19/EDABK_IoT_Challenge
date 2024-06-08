module Mux_Register(
    input [31:0] Read_data2,
    input [31:0] ImmExt,
    input ALUSrc,
    output [31:0] Mux_Register_out
);
assign Mux_Register_out= (ALUSrc)? ImmExt: Read_data2;
endmodule