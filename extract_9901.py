import requests

# 下载文件
url = 'https://raw.githubusercontent.com/yuanzl77/IPTV/refs/heads/main/live.m3u'
response = requests.get(url)
lines = response.text.splitlines()

# 提取特定地址和对应的#EXTINF行
filtered_lines = []
seen_addresses = set()
for i in range(len(lines)):
    if '120.76.' in lines[i]:
        address = lines[i]
        if address not in seen_addresses:
            seen_addresses.add(address)
            filtered_lines.append(lines[i-1])
            filtered_lines.append(lines[i])

# 写入新的文件
with open('live.m3u', 'w') as f:
    for line in filtered_lines:
        f.write(line + '\n')
