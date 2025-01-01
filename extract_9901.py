import requests
import ipaddress

# 下载文件
url = 'https://raw.githubusercontent.com/yuanzl77/IPTV/refs/heads/main/live.m3u'
response = requests.get(url)
lines = response.text.splitlines()

# 中国移动的IP段列表
cmcc_ip_ranges = [
    "39.0.0.0/8",
    "117.136.0.0/13",
    "221.176.0.0/13",
    "183.128.0.0/11",
    "211.136.0.0/13"
]

def is_cmcc_ip(ip):
    for ip_range in cmcc_ip_ranges:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range):
            return True
    return False

# 提取特定地址和对应的#EXTINF行，同时去除IPV6地址
filtered_lines = []
seen_addresses = set()
for i in range(len(lines)):
    if lines[i].startswith("http://"):
        # 去除IPV6地址
        try:
            ip = lines[i].split("//")[1].split("/")[0].split(":")[0]
            if ":" in ip:  # 如果包含冒号，则为IPV6地址
                continue
            if is_cmcc_ip(ip) and lines[i] not in seen_addresses:
                seen_addresses.add(lines[i])
                filtered_lines.append(lines[i-1])
                filtered_lines.append(lines[i])
        except Exception as e:
            continue

# 写入新的文件
with open('live.m3u', 'w') as f:
    for line in filtered_lines:
        f.write(line + '\n')
