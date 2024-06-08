///////////////////////////// Data_memory //////////////////////
module Data_memory(
    input clk, reset,
    input [31:0] Address, // dia chi cua o nho
    input [31:0] Write_data, // du lieu ghi vao ney co
    input [31:0] MemWrite,MemRead,   // cho phep ghi/doc vao thanh ghi hay khong
    //output reg [31:0] Dmemory [63:0],
	 output [31:0] Read_data // ma lenh dau ra
    
    

);
    reg [31:0] Dmemory [63:0]; // 64 thanh ghi chua du lieu , moi o nho 32bit
    
    assign Read_data= (MemRead)?  Dmemory[Address]: 32'b0;


    integer k;
    always @( posedge clk or negedge reset ) begin
        if(! reset==1) begin
            for(k=0; k<64; k=k+1) begin 
                Dmemory[k]<=32'h0;
            end
        end
        else begin
            if(MemWrite==1)   Dmemory[Address]<= Write_data;
            //else Read_data<= Dmemory[Address];
        
        end
    end
endmodule