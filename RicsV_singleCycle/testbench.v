module RicsV_singleCycle (
    input clk,
    input reset,
    output [31:0] writedata,
    output [31:0] dataadr,
    output memwrite
);

    // Wires to connect the modules
    wire [31:0] pc, instr, readdata;
    wire [31:0] alu_result, writedata;
    wire alusrc, regwrite, jump, memwrite, memread, branch;
    wire [1:0] memtoreg, imm_src;
    wire [2:0] alu_control;
    wire zero;

    // Instantiate the Program Counter (PC)
    PC pc_inst(
        .clk(clk),
        .reset(reset),
        .Mux_PC_out(Mux_PC_out),
        .PC_out(pc)
    );

    // Instantiate the Instruction Memory
    Instruction_Memory imem_inst(
        .clk(clk),
        .reset(reset),
        .read_address(pc),
        .Instruction_out(instr)
    );

    // Instantiate the PC Adder
    PCplus4 pcplus4_inst(
        .PCplus4_in(pc),
        .PCplus4_out(PCplus4_out)
    );

    // Instantiate the Register File
    Register_File regfile_inst(
        .clk(clk),
        .reset(reset),
        .RegWrite(regwrite),
        .Instruction_in(instr),
        .Write_data(Mux_Memory_out),
        .Read_data1(Read_data1),
        .Read_data2(Read_data2)
    );

    // Instantiate the Immediate Generator
    Immediate_Generator immgen_inst(
        .Opcode(instr[6:0]),
        .instruction(instr),
        .ImmExt(ImmExt)
    );

    // Instantiate the Control Unit
    Control_Unit control_inst(
        .Instruction(instr),
        .Branch(branch),
        .MemRead(memread),
        .MemtoReg(memToReg),
        .MemWrite(memwrite),
        .ALUSrc(alusrc),
        .RegWrite(regwrite),
        .ALUOp(ALUOp)
    );

    // Instantiate the ALU Control
    ALU_Control alucontrol_inst(
        .ALUOp(ALUOp),
        .Instruction(instr),
        .ALUControl(ALUControl)
    );

    // Instantiate the ALU
    ALU alu_inst(
        .Read_data1(Read_data1),
        .ALU_in2(Mux_Register_out),
        .ALUControl(ALUControl),
        .Zero(zero),
        .ALUResult(ALUResult)
    );

    // Instantiate the Data Memory
    Data_memory dmem_inst(
        .clk(clk),
        .reset(reset),
        .Address(ALUResult),
        .Write_data(Read_data2),
        .MemWrite(memwrite),
        .MemRead(memread),
        .Read_data(Read_data)
    );

    // Instantiate the Mux for Memory
    Mux_Memory mux_mem_inst(
        .Read_data(Read_data),
        .ALUResult(ALUResult),
        .MemtoReg(memToReg),
        .Mux_Memory_out(Mux_Memory_out)
    );

    // Instantiate the Mux for Register
    Mux_Register mux_reg_inst(
        .Read_data2(Read_data2),
        .ImmExt(ImmExt),
        .ALUSrc(alusrc),
        .Mux_Register_out(Mux_Register_out)
    );

    // Instantiate the Adder for PC + Imm
    Add_PC addpc_inst(
        .PC_out(pc),
        .ImmExt(ImmExt),
        .PCSum_out(PCSum_out)
    );

    // Instantiate the Mux for PC
    Mux_PC mux_pc_inst(
        .PCplus4_out(PCplus4_out),
        .PCSum_out(PCSum_out),
        .Zero(zero),
        .Branch(branch),
        .Mux_PC_out(Mux_PC_out)
    );

endmodule
