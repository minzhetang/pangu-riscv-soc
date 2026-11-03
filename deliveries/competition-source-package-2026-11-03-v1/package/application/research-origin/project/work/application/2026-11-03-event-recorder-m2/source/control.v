module control (
    input wire [6:0] opcode,
    input wire [2:0] funct3,
    input wire [6:0] funct7,
    output reg       reg_write,
    output reg       mem_write,
    output reg       branch,
    output reg       mem_to_reg,
    output reg       alu_src,
    output reg [4:0] alu_ctrl,
    output reg       jump
);
    localparam ALU_ADD = 5'b00000, ALU_SUB = 5'b00001, ALU_AND = 5'b00010,
               ALU_OR  = 5'b00011, ALU_XOR = 5'b00100, ALU_SLL = 5'b00101,
               ALU_SRL = 5'b00110, ALU_SRA = 5'b00111, ALU_SLT = 5'b01000, ALU_SLTU = 5'b01001, ALU_PASS_B = 5'b01010;
    always @(*) begin
        reg_write = 0; mem_write = 0; branch = 0; mem_to_reg = 0;
        alu_src = 0; jump = 0; alu_ctrl = ALU_ADD;
        case (opcode)
            7'b0110011: begin
                reg_write = 1; alu_src = 0;
                case (funct3)
                    3'b000: alu_ctrl = (funct7 == 7'b0000000) ? ALU_ADD : ALU_SUB;
                    3'b111: alu_ctrl = ALU_AND;
                    3'b110: alu_ctrl = ALU_OR;
                    3'b100: alu_ctrl = ALU_XOR;
                    3'b001: alu_ctrl = ALU_SLL;
                    3'b010: if (funct7 == 7'b0000000) alu_ctrl = ALU_SLT;
                    3'b011: if (funct7 == 7'b0000000) alu_ctrl = ALU_SLTU;
                    3'b101: alu_ctrl = (funct7 == 7'b0000000) ? ALU_SRL : ALU_SRA;
                endcase
            end
            7'b0010011: begin
                reg_write = 1; alu_src = 1;
                case (funct3)
                    3'b000: alu_ctrl = ALU_ADD;
                    3'b001: if (funct7 == 7'b0000000) alu_ctrl = ALU_SLL;
                    3'b010: alu_ctrl = ALU_SLT;
                    3'b011: alu_ctrl = ALU_SLTU;
                    3'b100: alu_ctrl = ALU_XOR;
                    3'b101: begin
                        if (funct7 == 7'b0000000) alu_ctrl = ALU_SRL;
                        else if (funct7 == 7'b0100000) alu_ctrl = ALU_SRA;
                    end
                    3'b110: alu_ctrl = ALU_OR;
                    3'b111: alu_ctrl = ALU_AND;
                endcase
            end
            7'b0110111: begin
                reg_write = 1; alu_src = 1; alu_ctrl = ALU_PASS_B;
            end
            7'b0010111: begin
                reg_write = 1; alu_src = 1; alu_ctrl = ALU_ADD;
            end
            7'b0000011: begin
                reg_write = 1; mem_to_reg = 1; alu_src = 1; alu_ctrl = ALU_ADD;
            end
            7'b0100011: begin
                mem_write = 1; alu_src = 1; alu_ctrl = ALU_ADD;
            end
            7'b1100011: begin
                branch = 1; alu_src = 0; alu_ctrl = ALU_SUB;
            end
            7'b1101111: begin
                reg_write = 1; jump = 1;
            end
            7'b1100111: begin
                reg_write = 1; jump = 1; alu_src = 1; alu_ctrl = ALU_ADD;
            end
        endcase
    end
endmodule
