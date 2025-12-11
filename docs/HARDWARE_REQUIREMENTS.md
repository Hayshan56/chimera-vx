CHIMERA-VX HARDWARE REQUIREMENTS
## From Smartphone to Supercomputer

---

## 🎯 TIERED REQUIREMENTS SYSTEM

Chimera-VX is designed to be **hardware-agnostic** but **hardware-aware**. The challenge adapts to your available resources, but performance scales with capability.

### **Key Philosophy:**
> **"Any device can start, but epic hardware completes."**

---

## 📱 TIER 1: TERMUX (ANDROID SMARTPHONE)

### **Minimum Specifications:**
```

Device: Android 10+ smartphone
CPU:4+ cores @ 2.0GHz
RAM:6GB free (8GB total recommended)
Storage:32GB free space
Battery:4000mAh+ (or continuous power)
Cooling:Passive (avoid thermal throttling)

```

### **Recommended Add-ons:**
```

External Storage: 128GB microSD card
Cooling:Phone cooler/fan attachment
Power:Fast charger + power bank
Peripherals:Bluetooth keyboard/mouse
Display:External monitor via USB-C/HDMI

```

### **Performance Expectations:**
```

Quantum Simulation: 5-10 minutes per circuit
DNA Analysis:15-30 minutes processing
Radio DSP:Real-time for simple signals
Minecraft:Playable but laggy
Overall:2-3x longer solve times

```

### **Termux-Specific Setup:**
```bash
# Essential packages
pkg update && pkg upgrade
pkg install python git clang make cmake
pkg install rtl-sdr hackrf gnuroadio
pkg install sqlite mariadb nodejs
pkg install proot-distro  # For Ubuntu container

# Ubuntu container for heavier tools
proot-distro install ubuntu
proot-distro login ubuntu -- apt update
proot-distro login ubuntu -- apt install python3 python3-pip

# Storage optimization
termux-setup-storage
mkdir -p ~/storage/shared/chimera-vx
ln -s ~/storage/shared/chimera-vx ~/chimera
```

Phone-Specific Considerations:

1. Thermal Management: Phones throttle quickly
2. Battery Degradation: Continuous heavy use damages batteries
3. Storage Wear: Heavy I/O reduces flash memory lifespan
4. Screen Burn-in: Static UI elements can cause permanent damage
5. Network Stability: Mobile data may be unreliable

---

💻 TIER 2: LAPTOP (CONSUMER GRADE)

Minimum Specifications:

```
CPU: Intel i5-8300H / AMD Ryzen 5 3500U (4c/8t)
RAM: 16GB DDR4 (upgradable to 32GB)
Storage: 512GB NVMe SSD (SATA acceptable)
GPU: Integrated graphics (Intel UHD 630 / Vega 8)
Cooling: Active with adequate airflow
Power: 65W+ adapter for sustained performance
```

Recommended Specifications:

```
CPU: Intel i7-11800H / AMD Ryzen 7 5800H (8c/16t)
RAM: 32GB DDR4 @ 3200MHz
Storage: 1TB NVMe PCIe 4.0 SSD
GPU: NVIDIA RTX 3060 / AMD RX 6600M (for CUDA/OpenCL)
Cooling: Advanced thermal solution (vapor chamber)
Display: 1920x1080 minimum, 144Hz preferred
```

Performance Expectations:

```
Quantum Simulation: 1-2 minutes per circuit
DNA Analysis: 5-10 minutes processing
Radio DSP: Real-time for complex signals
Minecraft: Smooth 60+ FPS
FPGA Simulation: 2-5 minutes compile/simulate
Overall: Base expected solve times
```

Laptop-Specific Optimizations:

```bash
# Linux performance tuning
sudo cpupower frequency-set -g performance
sudo tuned-adm profile throughput-performance
sudo sysctl -w vm.swappiness=10
sudo sysctl -w vm.dirty_ratio=40
sudo sysctl -w vm.dirty_background_ratio=10

# Windows Subsystem for Linux (WSL2)
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04
# Configure .wslconfig for memory/CPU limits
```

Cooling Solutions:

```
Essential:
  ✓ Laptop cooling pad with fans
  ✓ Regular thermal paste replacement
  ✓ Undervolting (if supported)
  ✓ Elevated rear for airflow

Advanced:
  ✓ External water cooling (rare)
  ✓ Liquid metal thermal compound
  ✓ Custom fan curves
  ✓ Ambient temperature control
```

---

🖥️ TIER 3: DESKTOP (WORKSTATION GRADE)

Minimum Specifications:

```
CPU: Intel i7-12700K / AMD Ryzen 7 5700X (8c/16t)
RAM: 32GB DDR4 @ 3600MHz (4x8GB)
Storage: 1TB NVMe PCIe 4.0 + 2TB HDD
GPU: NVIDIA RTX 3070 / AMD RX 6700 XT
Cooling: 240mm AIO liquid cooler
PSU: 750W 80+ Gold certified
Motherboard: Z690 / B550 with good VRMs
```

Recommended Specifications:

```
CPU: Intel i9-13900K / AMD Ryzen 9 7950X (24c/32t)
RAM: 64GB DDR5 @ 6000MHz (2x32GB)
Storage: 2TB NVMe PCIe 5.0 + 4TB NVMe PCIe 4.0
GPU: NVIDIA RTX 4090 / AMD RX 7900 XTX
Cooling: Custom water cooling loop
PSU: 1000W 80+ Platinum certified
Motherboard: Z790 / X670E with PCIe 5.0
```

Performance Expectations:

```
Quantum Simulation: 10-30 seconds per circuit
DNA Analysis: 1-2 minutes processing
Radio DSP: Real-time for multiple signals
Minecraft: 200+ FPS with shaders
FPGA Simulation: 30-60 seconds compile/simulate
Overall: 2-3x faster than base times
```

Desktop-Specific Setup:

```bash
# Linux kernel tuning
sudo grubby --update-kernel=ALL --args="mitigations=off"
sudo sysctl -w kernel.sched_autogroup_enabled=1
sudo sysctl -w vm.zone_reclaim_mode=0
sudo sysctl -w vm.vfs_cache_pressure=50

# GPU acceleration
pip install cupy-cuda11x  # NVIDIA CUDA
pip install pyopencl     # OpenCL support
pip install tensorflow-gpu
```

Cooling Configuration:

```
Air Cooling:
  ✓ Noctua NH-D15 / be quiet! Dark Rock Pro 4
  ✓ 6+ case fans (positive pressure)
  ✓ Cable management for airflow
  ✓ Regular dust cleaning

Water Cooling:
  ✓ EKWB / Corsair custom loop
  ✓ 360mm+ radiator space
  ✓ High-static-pressure fans
  ✓ Coolant monitoring and maintenance
```

---

⚡ TIER 4: SERVER (ENTERPRISE GRADE)

Minimum Specifications:

```
CPU: Dual Intel Xeon Silver 4314 / AMD EPYC 7313 (32c/64t total)
RAM: 128GB DDR4 ECC @ 3200MHz (8x16GB)
Storage: RAID 10 with 4x2TB NVMe SSDs
GPU: Dual NVIDIA A100 40GB / AMD MI100
Cooling: 2U rackmount with redundant fans
PSU: Dual 1600W 80+ Platinum redundant
Network: Dual 10GbE SFP+ ports
```

Recommended Specifications:

```
CPU: Dual AMD EPYC 9654 (192c/384t total)
RAM: 1TB DDR5 ECC @ 4800MHz (16x64GB)
Storage: NVMe-oF array with 100TB raw
GPU: 8x NVIDIA H100 80GB / AMD MI300X
Cooling: Liquid immersion cooling system
PSU: Triple 2400W 80+ Titanium redundant
Network: 100GbE InfiniBand fabric
```

Performance Expectations:

```
Quantum Simulation: 1-5 seconds per circuit
DNA Analysis: 10-30 seconds processing
Radio DSP: Real-time for massive bandwidth
Minecraft: Server for 100+ simultaneous players
FPGA Simulation: 5-10 seconds compile/simulate
Overall: 10-100x faster than base times
```

Server-Specific Configuration:

```bash
# High-performance tuning
sudo tuned-adm profile latency-performance
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 134217728"

# NUMA optimization
numactl --cpunodebind=0 --membind=0 python script.py
numactl --interleave=all python script.py
```

Infrastructure Requirements:

```
Power: 240V 30A circuit minimum
Cooling: 20,000 BTU+ HVAC system
Network: Enterprise switch with QoS
Rack: 42U with proper cable management
Monitoring: IPMI/iDRAC/iLO remote management
Backup: SAN/NAS with snapshot capability
```

---

🛰️ SPECIALIZED HARDWARE

1. Software-Defined Radio (SDR):

```
Minimum: RTL-SDR v3 (~$30)
  ✓ Frequency: 24-1766 MHz
  ✓ Bandwidth: 2.4 MHz
  ✓ ADC: 8-bit
  ✓ Use: Basic signal reception

Recommended: HackRF One (~$300)
  ✓ Frequency: 1 MHz - 6 GHz
  ✓ Bandwidth: 20 MHz
  ✓ ADC: 8-bit
  ✓ Use: Full transmit/receive capability

Professional: USRP B210 (~$1,200)
  ✓ Frequency: 70 MHz - 6 GHz
  ✓ Bandwidth: 56 MHz
  ✓ ADC: 12-bit
  ✓ Use: Research and development

Elite: Ettus USRP X310 (~$7,000)
  ✓ Frequency: DC - 6 GHz
  ✓ Bandwidth: 160 MHz
  ✓ ADC: 14-bit
  ✓ Use: Advanced research and signals intelligence
```

2. FPGA Development:

```
Minimum: Digilent Basys 3 (~$200)
  ✓ FPGA: Artix-7 XC7A35T
  ✓ Logic Cells: 33,280
  ✓ Memory: 1,800 Kb
  ✓ I/O: Limited but sufficient

Recommended: Digilent Arty A7-100T (~$300)
  ✓ FPGA: Artix-7 XC7A100T
  ✓ Logic Cells: 101,440
  ✓ Memory: 4,860 Kb
  ✓ I/O: Good selection

Professional: Xilinx KCU105 (~$2,500)
  ✓ FPGA: Kintex UltraScale XCKU040
  ✓ Logic Cells: 478,000
  ✓ Memory: 21,150 Kb
  ✓ I/O: High-speed transceivers

Elite: Xilinx Alveo U280 (~$8,000)
  ✓ FPGA: Virtex UltraScale+ VU9P
  ✓ Logic Cells: 2,586,000
  ✓ Memory: 38,000 Kb
  ✓ I/O: PCIe 4.0, HBM2 memory
```

3. Quantum Computing Access:

```
Free: IBM Quantum Experience
  ✓ Qubits: 5-7 public devices
  ✓ Access: Free account
  ✓ Queue: Hours to days
  ✓ Use: Learning and small circuits

Paid: IBM Quantum Premium
  ✓ Qubits: 27-127 qubit devices
  ✓ Access: $?/month
  ✓ Queue: Priority access
  ✓ Use: Research and development

On-premise: SpinQ Gemini Mini (~$5,000)
  ✓ Qubits: 2 NMR qubits
  ✓ Control: Desktop unit
  ✓ Use: Education and prototyping

Cloud: Amazon Braket / Azure Quantum
  ✓ Qubits: Various technologies
  ✓ Access: Pay-per-use
  ✓ Providers: D-Wave, IonQ, Rigetti
  ✓ Use: Commercial applications
```

4. Specialized Peripherals:

```
Logic Analyzer:
  ✓ Saleae Logic 8 (~$400)
  ✓ 8 channels @ 100MHz
  ✓ Essential for hardware debugging

Oscilloscope:
  ✓ Rigol DS1054Z (~$400)
  ✓ 4 channels @ 50MHz
  ✓ Useful for signal analysis

Microcontroller Dev Kits:
  ✓ ESP32 DevKit (~$10)
  ✓ STM32 Nucleo (~$20)
  ✓ Raspberry Pi Pico (~$4)
  ✓ Useful for embedded puzzles

Hardware Security Modules:
  ✓ Yubikey 5 (~$50)
  ✓ OnlyKey (~$100)
  ✓ TPM 2.0 module (~$20)
  ✓ Useful for crypto puzzles
```

---

⚡ POWER REQUIREMENTS

Power Consumption Estimates:

```
Tier 1 (Phone): 5-10W continuous
Tier 2 (Laptop): 30-100W under load
Tier 3 (Desktop): 200-800W under load
Tier 4 (Server): 500-3000W under load

Monthly Energy Cost (at $0.15/kWh):
  Phone: $0.50 - $1.00
  Laptop: $3.00 - $10.00
  Desktop: $20.00 - $85.00
  Server: $50.00 - $300.00
```

Power Supply Recommendations:

```
Phone: 25W+ fast charger + power bank
Laptop: 65W+ OEM charger
Desktop: 80+ Gold/Titanium certified
Server: Redundant PSUs with UPS backup

UPS Recommendations:
  Phone: Small portable charger
  Laptop: 300VA UPS (~$50)
  Desktop: 1000VA UPS (~$150)
  Server: 2000VA+ rackmount UPS (~$500+)
```
  
  🌡️ THERMAL MANAGEMENT

Temperature Limits:

```
Component   Safe Max   Throttle   Danger
---------- ---------- ---------- --------
Phone CPU     45°C       50°C      60°C
Laptop CPU    80°C       95°C      105°C
Desktop CPU   70°C       85°C      100°C
Server CPU    75°C       90°C      105°C
GPU           80°C       90°C      105°C
NVMe SSD      70°C       85°C      100°C
```

Cooling Solutions by Tier:

```
Tier 1 (Phone):
  ✓ Phone cooling fan attachment
  ✓ Air conditioning room
  ✓ Avoid direct sunlight
  ✓ Remove phone case during heavy use

Tier 2 (Laptop):
  ✓ Laptop cooling pad
  ✓ Regular dust cleaning
  ✓ Undervolting CPU/GPU
  ✓ Repaste thermal compound annually

Tier 3 (Desktop):
  ✓ High-performance air cooler or AIO
  ✓ Positive air pressure case
  ✓ Custom fan curves
  ✓ Regular maintenance

Tier 4 (Server):
  ✓ Data center cooling (20-24°C)
  ✓ Hot aisle/cold aisle containment
  ✓ Liquid cooling (immersion/direct)
  ✓ Environmental monitoring
```

---

💾 STORAGE REQUIREMENTS

Space Requirements by Puzzle:

```
Puzzle        Raw Data   Working   Total
----------- ---------- --------- -------
Quantum         10MB      100MB    110MB
DNA             100MB     1GB      1.1GB
Radio           500MB     2GB      2.5GB
FPGA            50MB      500MB    550MB
Minecraft       200MB     1GB      1.2GB
USB             50MB      200MB    250MB
Temporal        10MB      50MB     60MB
Crypto          10MB      100MB    110MB
Hardware        100MB     500MB    600MB
Forensic        2GB       4GB      6GB
Network         100MB     500MB    600MB
Meta            10MB      50MB     60MB

Total          3.13GB    10GB      13.13GB
```

Storage Recommendations:

```
Tier 1: 32GB free minimum (64GB recommended)
Tier 2: 100GB free minimum (200GB recommended)
Tier 3: 500GB free minimum (1TB recommended)
Tier 4: 2TB free minimum (10TB recommended)

Speed Requirements:
  Phone: UFS 3.1 / eMMC 5.1 minimum
  Laptop: NVMe PCIe 3.0 minimum
  Desktop: NVMe PCIe 4.0 recommended
  Server: NVMe RAID array
```

Backup Strategy:

```
Essential: Regular backups to external drive
Recommended: 3-2-1 backup rule
  3 copies of data
  2 different media types
  1 offsite copy

Cloud Options:
  Free: GitHub (code), Google Drive (data)
  Paid: Backblaze B2, AWS S3 Glacier
```

---

🌐 NETWORK REQUIREMENTS

Bandwidth Requirements:

```
Minimum: 10 Mbps download / 1 Mbps upload
Recommended: 100 Mbps symmetrical
Ideal: 1 Gbps symmetrical with low latency

Data Usage Estimates:
  Initial download: 3-5GB
  Per puzzle: 100MB-2GB each
  Total download: 10-20GB
  Upload: Minimal (solution hashes only)
```

Latency Sensitivity:

```
Not latency-sensitive for most puzzles
Exception: Temporal puzzles may require precise timing
Recommended: <100ms ping to challenge server
```

Network Security:

```
Essential: Firewall with default deny
Recommended: VPN for public networks
Advanced: Dedicated VLAN for challenge hardware

Port Requirements:
  Inbound: None (client initiates)
  Outbound: HTTPS (443), custom API ports
```

---

🔧 PERFORMANCE OPTIMIZATION

General Optimizations:

```bash
# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
sudo systemctl disable avahi-daemon

# Tune filesystem
sudo tune2fs -o discard /dev/nvme0n1p2  # SSD trim
sudo mount -o noatime,nodiratime /  # Reduce writes

# Memory management
sudo sysctl -w vm.swappiness=1
sudo sysctl -w vm.vfs_cache_pressure=50
```

Puzzle-Specific Optimizations:

Quantum:

```python
# Use statevector simulator for small circuits
backend = Aer.get_backend('statevector_simulator')
# Use GPU acceleration if available
backend = Aer.get_backend('qasm_simulator', max_parallel_threads=0)
```

DNA:

```python
# Use memory-mapped files for large sequences
from Bio import SeqIO
handle = open("large.fasta")
for record in SeqIO.parse(handle, "fasta"):
    process(record)
handle.close()
```

Radio:

```python
# Process in chunks to avoid memory issues
chunk_size = 1024 * 1024  # 1MB chunks
with open('iq_data.bin', 'rb') as f:
    while chunk := f.read(chunk_size):
        process_chunk(chunk)
```

FPGA:

```bash
# Parallel compilation
make -j$(nproc) all
# Use incremental compilation
iverilog -g2012 -o output design.v testbench.v
```

---

🚨 HARDWARE FAILURE WARNINGS

Common Failure Modes:

```
1. Thermal Throttling: Performance drops under load
2. Battery Degradation: Reduced capacity over time
3. Storage Wear: SSD lifespan reduced by heavy writes
4. Fan Failure: Overheating and component damage
5. Power Surge: Component destruction

Warning Signs:
  ✓ Unusual fan noise
  ✓ High temperatures (>90°C)
  ✓ Performance degradation
  ✓ System instability
  ✓ Blue screens/crashes
```

Preventative Measures:

```
1. Regular maintenance (cleaning, repasting)
2. Surge protectors/UPS
3. Temperature monitoring software
4. Regular backups
5. Spare hardware available
```

---

📈 SCALING RECOMMENDATIONS

When to Upgrade:

```
Upgrade when:
  1. Puzzles take >2x estimated time
  2. System crashes during heavy computation
  3. Temperatures consistently >90°C
  4. RAM usage consistently >90%
  5. Storage consistently >80% full
```

Upgrade Priority Order:

```
1. RAM (cheapest performance boost)
2. Storage (NVMe SSD if on SATA/HDD)
3. Cooling (better thermals allow sustained boost)
4. CPU (most expensive, biggest impact)
5. GPU (only for specific puzzles)
```

---

🧪 TESTING YOUR HARDWARE

Benchmark Script:

```python
#!/usr/bin/env python3
# hardware_benchmark.py

import psutil
import platform
import cpuinfo
import GPUtil
import numpy as np
from datetime import datetime

def run_benchmarks():
    print("🧪 Chimera-VX Hardware Benchmark")
    print("=" * 50)
    
    # CPU Benchmark
    print("\n[1/5] CPU Benchmark...")
    start = datetime.now()
    # Matrix multiplication stress test
    size = 1000
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    result = np.dot(a, b)
    cpu_time = (datetime.now() - start).total_seconds()
    print(f"  CPU Score: {1000/cpu_time:.2f} points")
    
    # Memory Benchmark
    print("\n[2/5] Memory Benchmark...")
    start = datetime.now()
    # Large array operations
    arr = np.random.rand(1000, 1000, 10)
    arr = arr * 2 - 1
    arr = np.sin(arr) + np.cos(arr)
    mem_time = (datetime.now() - start).total_seconds()
    print(f"  Memory Score: {100/mem_time:.2f} points")
    
    # Storage Benchmark
    print("\n[3/5] Storage Benchmark...")
    import tempfile
    start = datetime.now()
    with tempfile.NamedTemporaryFile() as tmp:
        data = np.random.bytes(100 * 1024 * 1024)  # 100MB
        tmp.write(data)
        tmp.flush()
    storage_time = (datetime.now() - start).total_seconds()
    print(f"  Storage Score: {100/storage_time:.2f} points")
    
    # Overall Score
    total_score = (1000/cpu_time) * 0.4 + (100/mem_time) * 0.3 + (100/storage_time) * 0.3
    print(f"\n✅ Overall Hardware Score: {total_score:.2f}")
    
    # Recommendations
    print("\n📋 Recommendations:")
    if total_score < 50:
        print("  ⚠️  Your hardware may struggle with Chimera-VX")
        print("  💡 Consider upgrading RAM and storage first")
    elif total_score < 100:
        print("  ✅ Your hardware meets minimum requirements")
        print("  💡 Expect moderate performance")
    else:
        print("  🎉 Your hardware is excellent for Chimera-VX!")
        print("  💡 You should have a smooth experience")

if __name__ == "__main__":
    run_benchmarks()
```

System Monitoring:

```bash
# Real-time monitoring
sudo apt install htop iotop nvtop
htop  # CPU/RAM
iotop # Disk I/O
nvtop # GPU (if available)
sensors # Temperatures

# Logging for analysis
sudo dmesg -w  # Kernel messages
journalctl -f  # System logs
```

  🆘 TROUBLESHOOTING COMMON ISSUES

Issue: System Overheating

```
Symptoms: Performance drops, crashes, loud fans
Solution:
  1. Clean dust from vents/fans
  2. Improve airflow (elevate laptop)
  3. Reduce ambient temperature
  4. Undervolt CPU/GPU
  5. Replace thermal paste
```

Issue: Out of Memory

```
Symptoms: Sluggish performance, swapping, crashes
Solution:
  1. Close unnecessary applications
  2. Increase swap space
  3. Add more RAM
  4. Use 64-bit OS if on 32-bit
```

Issue: Storage Full

```
Symptoms: Can't save files, system warnings
Solution:
  1. Clean temporary files
  2. Move data to external storage
  3. Uninstall unused applications
  4. Upgrade storage capacity
```

Issue: Network Problems

```
Symptoms: Can't connect, slow downloads
Solution:
  1. Check firewall settings
  2. Restart router/modem
  3. Use wired connection if possible
  4. Contact ISP if persistent
```

---

🌟 OPTIMAL HARDWARE CONFIGURATION

The "Sweet Spot" Configuration:

```
CPU: AMD Ryzen 7 5800X3D / Intel i7-13700K
RAM: 32GB DDR4 @ 3600MHz CL16
Storage: 1TB NVMe PCIe 4.0 SSD
GPU: NVIDIA RTX 4060 Ti / AMD RX 7600
Cooling: 240mm AIO or high-end air cooler
PSU: 750W 80+ Gold
Motherboard: B550 / B760 with good VRMs
Total Cost: $1,200 - $1,800
```

Budget Configuration:

```
CPU: AMD Ryzen 5 5600 / Intel i5-12400F
RAM: 16GB DDR4 @ 3200MHz
Storage: 512GB NVMe SSD
GPU: Integrated graphics (or used GTX 1660)
Cooling: Stock cooler
PSU: 550W 80+ Bronze
Motherboard: A520 / B660
Total Cost: $600 - $800
```

No-Compromise Configuration:

```
CPU: AMD Threadripper 7970X / Intel i9-14900K
RAM: 128GB DDR5 @ 6000MHz
Storage: 2TB NVMe PCIe 5.0 + 4TB NVMe PCIe 4.0
GPU: NVIDIA RTX 4090
Cooling: Custom water loop
PSU: 1200W 80+ Titanium
Motherboard: TRX50 / Z790
Total Cost: $4,000 - $6,000
```

---

🏁 CONCLUSION

Chimera-VX is designed to be challenging, not impossible. While better hardware provides advantages, the most important component is your brain.

Remember: Many of history's greatest hackers started with limited resources. What you lack in hardware, you can compensate for with creativity, persistence, and clever problem-solving.

"It's not the hardware in your hands, but the software in your heart."

---

📞 SUPPORT AND RESOURCES
  Recommended Retailers:

· US: Micro Center, Newegg, Amazon
· EU: Caseking, Alternate, Amazon
· Asia: Taobao, Lazada, Shopee
· Global: eBay (for used parts)

Further Reading:

· "Building a Cybersecurity Lab" by David Bombal
· "The Hardware Hacker" by Andrew Huang
· PC Part Picker: https://pcpartpicker.com
· Logical Increments: https://www.logicalincrements.com

---

Last Updated: 11/12/2025
Maintainer: Hayshan56
Contact: hayshanwow@gmail.com

This document will be updated as hardware evolves and new requirements emerge.
