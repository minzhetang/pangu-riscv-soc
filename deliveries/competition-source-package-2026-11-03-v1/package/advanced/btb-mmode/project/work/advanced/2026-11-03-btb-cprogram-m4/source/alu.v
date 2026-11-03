module alu (
    input wire [31:0] a,
    input wire [31:0] b,
    input wire [4:0]  ctrl,
    output reg [31:0] result,
    output wire       zero
);
    localparam ADD = 5'b00000, SUB = 5'b00001, AND = 5'b00010,
               OR  = 5'b00011, XOR = 5'b00100, SLL = 5'b00101,
               SRL = 5'b00110, SRA = 5'b00111, SLT = 5'b01000, SLTU = 5'b01001, PASS_B = 5'b01010;
    always @(*) begin
        case (ctrl)
            ADD: result = a + b;
            SUB: result = a - b;
            AND: result = a & b;
            OR:  result = a | b;
            XOR: result = a ^ b;
            SLL: result = a << b[4:0];
            SRL: result = a >> b[4:0];
            SRA: result = $signed(a) >>> b[4:0];
            SLT: result = ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
            SLTU: result = ($unsigned(a) < $unsigned(b)) ? 32'd1 : 32'd0;
            PASS_B: result = b;
            default: result = 32'd0;
        endcase
    end
    assign zero = (result == 32'd0);
endmodule
