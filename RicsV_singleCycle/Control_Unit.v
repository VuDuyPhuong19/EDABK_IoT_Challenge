////////////////////////////// Control_Unit //////////////////////
module Control_Unit (
    input [31:0] Instruction, 
    //input [6:0] Opcode,
    output reg Branch, MemRead, MemtoReg, MemWrite, ALUSrc, RegWrite,
    output reg [1:0] ALUOp
);
wire [6:0] Opcode;
assign Opcode = Instruction[6:0];
 always@(*)
    begin
        case (Opcode)
        7'b0110011: begin // R-type instr
        ALUSrc<=0; MemtoReg<=0;RegWrite<=1; MemRead<=0; MemWrite<=0;Branch<=0; 
        ALUOp<=2'b10;
        end
        7'b0000011: begin // Load Instruction LW
        ALUSrc<=1; MemtoReg<=1;RegWrite<=1; MemRead<=1; MemWrite<=0;Branch<=0; 
        ALUOp<=2'b00;
        end
        7'b0100011: begin // store Instr SW MetoReg<=X
        ALUSrc<=1; MemtoReg<=1;RegWrite<=0; MemRead<=0; MemWrite<=1;Branch<=0; 
        ALUOp<=2'b00;    
        end
        7'b0000011: begin // B-type MetoReg<=X
        ALUSrc<=0; MemtoReg<=0;RegWrite<=0; MemRead<=0; MemWrite<=1;Branch<=1; 
        ALUOp<=2'b01;    
        end
        7'b0010011: begin // I type
        ALUSrc<=1; MemtoReg<=0;RegWrite<=1; MemRead<=0; MemWrite<=0;Branch<=0; 
        ALUOp<=2'b00;
        end
        default: begin // same R-type instr
        ALUSrc<=0; MemtoReg<=0;RegWrite<=1; MemRead<=0; MemWrite<=0;Branch<=0; 
        ALUOp<=2'b10;
        end
        endcase
    end
endmodule