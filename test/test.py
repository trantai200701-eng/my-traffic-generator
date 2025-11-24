import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def test_traffic_gen(dut):
    dut._log.info("Bắt đầu test Traffic Generator")

    # 1. Khởi tạo Clock 100MHz
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 2. Giữ Reset trong 10 chu kỳ đầu để tránh trạng thái X
    dut._log.info("Đang Reset...")
    dut.rst_n.value = 0
    dut.ui_in.value = 2  # Cài đặt chu kỳ N = 2
    dut.uio_in.value = 0
    dut.ena.value = 1
    
    # Chờ 10 chu kỳ clock rồi mới thả Reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    dut._log.info("Reset xong. Bắt đầu chạy logic...")

    # 3. Chạy vòng lặp kiểm tra
    for i in range(50):
        await RisingEdge(dut.clk)
        
        # Đọc giá trị đầu ra an toàn
        # Dùng try-except để tránh crash nếu gặp tín hiệu 'X' (Unknown)
        try:
            pkt_id = int(dut.uo_out.value)
            
            # Xử lý uio_out (Packet Type và Valid)
            # uio_out là BinaryValue, cần chuyển sang int cẩn thận
            uio_val = dut.uio_out.value
            
            # Kiểm tra xem uio_val có phải là số hợp lệ không
            if not uio_val.is_resolvable:
                dut._log.info(f"Cycle {i}: Tín hiệu chưa ổn định (X)")
                continue

            packet_type = (uio_val >> 0) & 1
            valid = (uio_val >> 1) & 1
            
            if valid:
                loai = "DL (Downlink)" if packet_type else "UL (Uplink)"
                dut._log.info(f"Cycle {i}: [VALID] {loai} - ID: {hex(pkt_id)}")
            else:
                dut._log.info(f"Cycle {i}: ...đang chờ (Counter chạy)...")
                
        except ValueError:
            dut._log.error(f"Cycle {i}: Gặp lỗi khi đọc giá trị (có thể do tín hiệu X)")
