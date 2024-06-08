///////////////////////////// Mux-block- datamemory //////////////////////
module Mux_Memory(
    input [31:0] Read_data,
    input [31:0] ALUResult,
    input MemtoReg,
    output [31:0] Mux_Memory_out
);
    assign Mux_Memory_out= (MemtoReg)? Read_data: ALUResult;
endmodule