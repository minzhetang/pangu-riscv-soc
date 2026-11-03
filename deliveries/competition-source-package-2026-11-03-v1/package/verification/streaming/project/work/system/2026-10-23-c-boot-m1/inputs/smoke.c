/* Toolchain/link smoke only. Not executed on CPU or FPGA in this phase. */
typedef unsigned int u32;
_Static_assert(sizeof(u32) == 4, "RV32 unsigned word required");
_Static_assert(sizeof(void *) == 4, "ILP32 pointer required");
volatile u32 input_a = 1234567u;
volatile u32 input_b = 97u;
volatile u32 results[4];
volatile u32 signature;
int main(void)
{
    u32 a = input_a;
    u32 b = input_b;
    results[0] = a * b;
    results[1] = a / b;
    results[2] = a % b;
    results[3] = a + b;
    /* Hand-derived before compilation, not obtained from the target. */
    signature = (results[0] == 119752999u && results[1] == 12727u &&
                 results[2] == 48u && results[3] == 1234664u)
        ? 0x50524f42u : 0x4641494cu;
    return signature == 0x50524f42u ? 0 : 1;
}
