<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Explain how your project works

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

Explain how to use your project

1.  **Reset**: Apply a low pulse to `rst_n` to reset the LFSRs and counters.
2.  **Configuration**: Set `ui_in[3:0]` to define the period `N` (number of clock cycles between packets).
3.  **Observation**:
    * Monitor `uo_out[7:0]` to see the generated 8-bit Packet ID.
    * Monitor `uio_out[1]` (Valid Flag). When it goes HIGH, valid data is present.
    * Monitor `uio_out[0]` (Packet Type) to distinguish between Uplink (0) and Downlink (1).

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
