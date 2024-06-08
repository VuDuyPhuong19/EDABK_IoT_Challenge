////////////////////////////// immediate generator //////////////////////
// tao gia tri immidiate tu 12bit thanh 32bit
module Immediate_Generator (
    input [6:0] Opcode, 
    input [31:0] instruction,  
    output reg [31:0] ImmExt // imm 32bit
);
    always @(Opcode or instruction) begin
        case (Opcode)
            7'b0010011: ImmExt= {{20{instruction[31]}}, instruction[31:20]}; // I instruction
            7'b0100011: ImmExt= {{20{instruction[31]}}, instruction[31:25], instruction[11:7]}; // S instruction
            7'b1100011: ImmExt= {{20{instruction[31]}},instruction[31], instruction[7], instruction[30:25],instruction[11:8]}; // B instruction
            default:  ImmExt= {{20{instruction[31]}},instruction[31:20]}; //  instruction
        endcase
    end
endmodule 