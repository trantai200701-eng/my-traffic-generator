import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def test_traffic_gen(dut):
    dut._log.info("Bắt đầu test Traffic Gen")

    # Tạo xung clock 100MHz (10ns)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset hệ thống
    dut._log.info("Resetting...")
    dut.rst_n.value = 0
    dut.ui_in.value = 3  # Giả sử đặt N = 3 chu kỳ
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Hệ thống bắt đầu chạy...")

    # Chạy mô phỏng trong 100 chu kỳ clock
    for i in range(100):
        await RisingEdge(dut.clk)
        
        # Đọc giá trị
        pkt_id = int(dut.uo_out.value)
        
        # Đọc bit Valid và Type từ uio_out
        # Lưu ý: cần chuyển đổi nhị phân cẩn thận
        uio_val = dut.uio_out.value
        packet_type = (uio_val >> 0) & 1
        valid = (uio_val >> 1) & 1

        if valid == 1:
            loai_goi = "DOWNLINK" if packet_type else "UPLINK"
            dut._log.info(f"Time {cocotb.utils.get_sim_time(units='ns')}: Có gói tin! Loại: {loai_goi}, ID: {hex(pkt_id)}")
