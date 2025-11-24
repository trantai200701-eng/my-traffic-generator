## How it works

This project implements a traffic generator for Uplink (UL) and Downlink (DL) simulation using Linear Feedback Shift Registers (LFSRs).

The design consists of:
1.  **Two 8-bit LFSRs**:
    * **Uplink LFSR**: Generates pseudo-random packet IDs for UL traffic (Seed: 0xAA, Taps: 0xB4).
    * **Downlink LFSR**: Generates pseudo-random packet IDs for DL traffic (Seed: 0x55, Taps: 0xD8).
2.  **Scheduler**:
    * Uses an internal counter to switch between UL and DL packets based on the input period `N`.
    * When the counter reaches `N`, a packet is generated.
    * The system alternates between UL and DL transmission.

## How to test

1.  **Reset**: Apply a low pulse to `rst_n` to reset the LFSRs and counters.
2.  **Configuration**: Set `ui_in[3:0]` to define the period `N` (number of clock cycles between packets).
3.  **Observation**:
    * Monitor `uo_out[7:0]` to see the generated 8-bit Packet ID.
    * Monitor `uio_out[1]` (Valid Flag). When it goes HIGH, valid data is present.
    * Monitor `uio_out[0]` (Packet Type) to distinguish between Uplink (0) and Downlink (1).

## External hardware

No external hardware is required for the basic logic functionality. Just connect a clock source and logic analyzer to observe the outputs.
