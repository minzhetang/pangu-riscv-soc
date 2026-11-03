# AI-ISOLATED-M0 frozen v1 — synthetic operator only

No trained model or legally verified third-party weights were supplied/selected.
This milestone deliberately uses original deterministic synthetic 16-input x
8-output fully connected layers, no activation. These are operator test tensors,
not a trained model, real-model port, recognition task or complete edge AI system.
Weights, inputs and biases are generated here; no third-party license dependency.
Original deliverable code/tensors are provided for this project's use/modification;
this statement does not relicense pre-existing project/tool code.

Architecture: 16 signed8 inputs, 128 signed8 weights and 8 signed32 biases loaded
via explicit configuration handshake. 1 MAC/cycle reused by a complete 8-row
controller. Inputs/weights scale 1/64 (signed8 integer divided by 64); bias and
40-bit accumulator scale 1/4096. Exact bias + sum of 16 products, no accumulator
wrap reachable for the supported dimensions even with int32-extreme bias. Output
signed8 scale 1/64, nearest rounding with ties away from zero then saturation
[-128,127]. Raw signed40 accumulator accompanies each output for exact comparison.

Config valid/ready with kind0=input addr0..15; kind1=row-major weight addr0..127;
kind2=bias addr0..7. Out-of-range/kind3 ignored, no initialized bit set.
Start valid/ready accepted only idle and config valid low. Busy blocks config/start.
Missing initialization produces one error/last response, no MAC. Normal result
stream has row index0..7, last on row7, valid/raw/y/index/error held under stalls.
Reset synchronous: cancels busy/result, clears initialization flags, requires reload;
does not promise physical array clearing. No external memory/bus/CPU integration.

Freeze software integer oracle, floating original tensor results, quantized vectors
and exact expected arrays before RTL. Finite cases: 3 non-grid bounded float sets
(positive/negative/mixed), zero, signed extrema, positive/negative int32 bias limits,
rounding ties +/-32 and +/-96, saturation boundaries. Software quantization uses
nearest ties away zero and clipping. Compare RTL raw sums exactly to Python unbounded
integer dot product and every y to separate scalar rounding/saturation; report float
reference error before/after saturation, explicitly separate out-of-range cases.

Run all finite cases with no output stalls and row-index-dependent 0..3 stalls.
Baseline start-to-last-handshake = 8*(16 MAC + 1 response) = 136 clock cycles;
with deterministic stalls = 136 + 12 = 148. Config traffic overhead counted separately,
not CPU speedup. Test repeated starts with retained weights, invalid config/missing
init, start/config backpressure, reset mid-MAC and pending output, no ghost output.
Output mismatch negative control must reject an altered expected value.
No synthesis/frequency/power/accuracy claims; stop at bounded independent simulation.
