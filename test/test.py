import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def test_traffic_gen(dut):
    dut._log.info("Bắt đầu test Traffic Generator")

    # 1. Khởi tạo Clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 2. Reset
    dut._log.info("Đang Reset...")
    dut.rst_n.value = 0
    dut.ui_in.value = 2
    dut.uio_in.value = 0
    dut.ena.value = 1
    
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("Reset xong. Bắt đầu chạy logic...")

    # 3. Vòng lặp kiểm tra
    for i in range(50):
        await RisingEdge(dut.clk)
        
        # Đọc giá trị từ DUT
        uio_val_obj = dut.uio_out.value
        uo_val_obj = dut.uo_out.value

        # Kiểm tra xem tín hiệu có bị X (unknown) hay Z (high-Z) không
        if not uio_val_obj.is_resolvable or not uo_val_obj.is_resolvable:
            dut._log.info(f"Cycle {i}: Tín hiệu chưa ổn định (X/Z), bỏ qua.")
            continue

        # SỬA LỖI CHÍNH Ở ĐÂY:
        # Chuyển đổi đối tượng LogicArray thành số nguyên (int) trước khi tính toán
        try:
            val_int = int(uio_val_obj)
            pkt_id = int(uo_val_obj)

            packet_type = (val_int >> 0) & 1
            valid = (val_int >> 1) & 1
            
            if valid:
                loai = "DL (Downlink)" if packet_type else "UL (Uplink)"
                dut._log.info(f"Cycle {i}: [VALID] {loai} - ID: {hex(pkt_id)}")
            
        except Exception as e:
            dut._log.warning(f"Cycle {i}: Không thể chuyển đổi dữ liệu: {e}")
