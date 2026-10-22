import subprocess
import re
import time

IP = "192.168.164.132"
COMMUNITY = "public"
INTERVAL = 2         
DURATION = 60        

TARGET_OIDS = {
    "Inbound": "1.3.6.1.2.1.2.2.1.10.2",
    "Outbound": "1.3.6.1.2.1.2.2.1.16.2"
}

def get_interface_traffic(ip, community, oid):
    command = ["snmpwalk", "-v2c", "-c", community, "-On", ip, oid]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        match = re.search(r'(?:Counter32|Counter64|INTEGER):\s*(\d+)', result.stdout)
        if match:
            return int(match.group(1))
    return None

print(f"Monitoring live bandwidth on {IP} every {INTERVAL} seconds for {DURATION} seconds...")

previous_poll = {}
for direction, oid in TARGET_OIDS.items():
    previous_poll[direction] = get_interface_traffic(IP, COMMUNITY, oid)

iterations = DURATION // INTERVAL

for _ in range(iterations):
    time.sleep(INTERVAL)
    
    for direction, oid in TARGET_OIDS.items():
        current_poll = get_interface_traffic(IP, COMMUNITY, oid)
        
        if previous_poll.get(direction) is not None and current_poll is not None:
            delta_bytes = current_poll - previous_poll[direction]
            
            if delta_bytes < 0:
                delta_bytes += 4294967296 
            
            bits_per_second = (delta_bytes * 8) / INTERVAL
            mbps = bits_per_second / 1_000_000
            
            print(f"{direction} Speed: {mbps:.2f} Mbps")
            
            previous_poll[direction] = current_poll
        else:
            print(f"Failed to retrieve {direction} data.")
    
    print("-" * 25)
