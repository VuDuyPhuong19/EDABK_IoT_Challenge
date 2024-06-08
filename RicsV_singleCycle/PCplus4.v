
////////////////////////////// PC Adder //////////////////////
module PCplus4(
    input [31:0] PCplus4_in, //PC_out
    output [31:0] PCplus4_out
);
    assign PCplus4_out= PCplus4_in + 32'h00000004;
endmodule