///////////////////////////// Add- PC //////////////////////
module Add_PC(
    input [31:0] PC_out,
    input [31:0] ImmExt,
    output [31:0] PCSum_out
);
    assign PCSum_out= PC_out+ImmExt;
endmodule