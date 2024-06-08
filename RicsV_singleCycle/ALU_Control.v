///////////////////////////// ALU-control //////////////////////

module ALU_Control(
    input [1:0] ALUOp,
    input [31:0] Instruction,
    //input [6:0]func7,
    //input func7,
    //input [2:0] func3,
    output reg [3:0] ALUControl
);
    wire func7;
    wire[2:0] func3;
    assign func7=Instruction[30];
    assign func3=Instruction[14:12];
    
    always @(ALUOp or func7 or func3 )
    begin
        case ({ALUOp,func7,func3})
        6'b000000: begin ALUControl<=4'b0010; end 
        6'b010000: begin ALUControl<=4'b0110; end
        6'b100000: begin ALUControl<=4'b0010; end
        6'b101000: begin ALUControl<=4'b0110; end
        6'b100111: begin ALUControl<=4'b0000; end
        6'b100110: begin ALUControl<=4'b0001; end

        default  : begin ALUControl<=4'b0001; end
        endcase
    end
endmodule