![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# Uplink/Downlink Traffic Generator (LFSR-based)

This project implements a hardware-based **Traffic Generator** intended for testing network systems or simulation environments. It is designed for the **SkyWater 130nm** process technology via the **Tiny Tapeout** platform.

The core logic generates pseudo-random 8-bit Packet IDs using Linear Feedback Shift Registers (LFSRs), simulating interleaved Uplink (UL) and Downlink (DL) traffic.

## Features

* **Dual Independent LFSRs:**
    * **Uplink (UL):** Generates random IDs using Seed `0xAA` and Polynomial `0xB4`.
    * **Downlink (DL):** Generates random IDs using Seed `0x55` and Polynomial `0xD8`.
* **Configurable Scheduler:**
    * The period $N$ between packets is configurable via input pins (`ui_in`).
    * A packet is generated every $N$ clock cycles.
* **Round-Robin Arbitration:**
    * The system strictly alternates between Uplink and Downlink packets.

## How it works

1.  **Inputs:** The system takes a 4-bit value `N_period` from the input pins.
2.  **Processing:** An internal counter runs continuously. When the counter reaches `N_period`:
    * The Logic determines whose turn it is (UL or DL).
    * The corresponding LFSR advances to the next random number.
    * The `Valid` flag is raised.
3.  **Outputs:** The 8-bit Packet ID is sent to the output pins, along with a `Packet Type` flag (0 for UL, 1 for DL).

## Pinout

| Pin | Direction | Name | Description |
| --- | --- | --- | --- |
| **ui_in[3:0]** | Input | N_period | Sets the generation period (Cycles between packets) |
| **ui_in[7:4]** | Input | Unused | Tied to 0 |
| **uo_out[7:0]** | Output | Packet ID | The generated 8-bit pseudo-random ID |
| **uio_out[0]** | Output | Packet Type | `0`: Uplink (UL), `1`: Downlink (DL) |
| **uio_out[1]** | Output | Valid | `1` when data is valid, `0` otherwise |
| **clk** | Input | Clock | System Clock |
| **rst_n** | Input | Reset | Active Low Reset |

## Verification

The project has been verified using:
* **RTL Simulation:** Cocotb (Python) testbench verifying the logic and scheduler timing.
* **Gate Level Simulation (GLS):** Verified post-synthesis netlist behavior.
* **Physical Verification:** Passed Tiny Tapeout Precheck (DRC/LVS clean).

## 3D Render

## 3D Viewer

View the 3D GDSII of this chip here:
👉 **[Click to Open 3D Viewer](https://gds-viewer.tinytapeout.com/?pdk=sky130A&model=https%3A%2F%2Ftrantai200701-eng.github.io%2Fmy-traffic-generator%2Ftinytapeout.oas)**
---
*Project by: Tran Tan Tai*
*Built for Tiny Tapeout*
