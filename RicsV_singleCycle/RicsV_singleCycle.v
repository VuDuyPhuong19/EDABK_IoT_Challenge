module RicsV_singleCycle (
    input clk,
    input reset,
    //input [319:0] Instruction_in,
    output [31:0] PC_cur,
    output [31:0] Instruction_cur
);

    // Wires to connect the modules
    wire [31:0] PC_out, Instr, PCplus4_out, PCSum_out, Mux_PC_out;
    wire [31:0] Read_data1, Read_data2, ImmExt, ALUResult, Read_data, Write_data;
    wire [31:0] Mux_Register_out, Mux_Memory_out;
    wire [3:0] ALUControl;
    wire [1:0] ALUOp;
    wire Zero, Branch, MemRead, MemtoReg, MemWrite, ALUSrc, RegWrite;

    assign PC_cur = PC_out;
    assign Instruction_cur = Instr;

    // Instantiate the Program Counter (PC)
    PC pc_inst(
        .clk(clk),
        .reset(reset),
        .Mux_PC_out(Mux_PC_out),
        .PC_out(PC_out)
    );

    // Instantiate the Instruction Memory
    Instruction_Memory imem_inst(
        .clk(clk),
        .reset(reset),
        //.Instruction_in(Instruction_in),
        .read_address(PC_out),
        .Instruction_out(Instr)
    );

    // Instantiate the PC Adder
    PCplus4 pcplus4_inst(
        .PCplus4_in(PC_out),
        .PCplus4_out(PCplus4_out)
    );

    // Instantiate the Register File
    Register_File regfile_inst(
        .clk(clk),
        .reset(reset),
        .RegWrite(RegWrite),
        .Instruction_in(Instr),
        .Write_data(Mux_Memory_out),
        .Read_data1(Read_data1),
        .Read_data2(Read_data2)
    );

    // Instantiate the Immediate Generator
    Immediate_Generator immgen_inst(
        .Opcode(Instr[6:0]),
        .instruction(Instr),
        .ImmExt(ImmExt)
    );

    // Instantiate the Control Unit
    Control_Unit control_inst(
        .Instruction(Instr),
        .Branch(Branch),
        .MemRead(MemRead),
        .MemtoReg(MemtoReg),
        .MemWrite(MemWrite),
        .ALUSrc(ALUSrc),
        .RegWrite(RegWrite),
        .ALUOp(ALUOp)
    );

    // Instantiate the ALU Control
    ALU_Control alucontrol_inst(
        .ALUOp(ALUOp),
        .Instruction(Instr),
        .ALUControl(ALUControl)
    );

    // Instantiate the ALU
    ALU alu_inst(
        .Read_data1(Read_data1),
        .ALU_in2(Mux_Register_out),
        .ALUControl(ALUControl),
        .Zero(Zero),
        .ALUResult(ALUResult)
    );

    // Instantiate the Data Memory
    Data_memory dmem_inst(
        .clk(clk),
        .reset(reset),
        .Address(ALUResult),
        .Write_data(Read_data2),
        .MemWrite(MemWrite),
        .MemRead(MemRead),
        .Read_data(Read_data)
    );

    // Instantiate the Mux for Memory
    Mux_Memory mux_mem_inst(
        .Read_data(Read_data),
        .ALUResult(ALUResult),
        .MemtoReg(MemtoReg),
        .Mux_Memory_out(Mux_Memory_out)
    );

    // Instantiate the Mux for Register
    Mux_Register mux_reg_inst(
        .Read_data2(Read_data2),
        .ImmExt(ImmExt),
        .ALUSrc(ALUSrc),
        .Mux_Register_out(Mux_Register_out)
    );

    // Instantiate the Adder for PC + Imm
    Add_PC addpc_inst(
        .PC_out(PC_out),
        .ImmExt(ImmExt),
        .PCSum_out(PCSum_out)
    );

    // Instantiate the Mux for PC
    Mux_PC mux_pc_inst(
        .PCplus4_out(PCplus4_out),
        .PCSum_out(PCSum_out),
        .Zero(Zero),
        .Branch(Branch),
        .Mux_PC_out(Mux_PC_out)
    );

endmodule
