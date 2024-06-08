////////////////////////////// ALU //////////////////////

module ALU(
    input [31:0] Read_data1, ALU_in2, // ALU_in2<= Mux_Register_out
    input [3:0] ALUControl,
    output reg Zero,
    output reg [31:0] ALUResult
);
    always @(ALUControl or Read_data1 or ALU_in2 )
    begin
        case (ALUControl)
        4'b0000: begin Zero<=0; ALUResult<= Read_data1&ALU_in2; end
        4'b0001: begin Zero<=0; ALUResult<= Read_data1||ALU_in2; end
        4'b0010: begin Zero<=0; ALUResult<= Read_data1 + ALU_in2; end
        4'b0110: begin if(Read_data1==ALU_in2) Zero<=1;  
                        else  Zero<=0;
                        ALUResult<= Read_data1-ALU_in2; end
        default:  begin Zero<=0; ALUResult<= Read_data1&ALU_in2; end
        endcase
    end
endmodule