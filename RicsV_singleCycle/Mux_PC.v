///////////////////////////// Mux-block- PC //////////////////////
module Mux_PC(
    input [31:0] PCplus4_out,
    input [31:0] PCSum_out,
    input Zero,
    input Branch,
    output [31:0] Mux_PC_out
);
    assign Mux_PC_out= (Zero&Branch)? PCSum_out: PCplus4_out;
endmodule