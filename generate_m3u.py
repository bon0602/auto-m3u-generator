import requests
import base64
from Crypto.Cipher import AES
import json

url = "https://quartz12.orbitalrift.org/quartz12/file/livelist/22_zh_TW.txt"
key = b"44BBF7451673B288"

response = requests.get(url)
encrypted = base64.b64decode(response.text)

cipher = AES.new(key, AES.MODE_ECB)
decrypted = cipher.decrypt(encrypted)

pad_len = decrypted[-1]
decrypted = decrypted[:-pad_len]

data = json.loads(decrypted.decode("utf-8"))
m3u = "#EXTM3U\n"

for group in data.get("data", []):
    group_title = group.get("classify", "")
    for channel in group.get("list", []):
        name = channel.get("dname", "")
        logo = channel.get("icon", "")
        url_list = json.loads(channel.get("url", "[]"))
        if url_list and "path" in url_list[0]:
            stream_url = url_list[0]["path"]
            m3u += f'#EXTINF:-1 group-title="{group_title}" tvg-logo="{logo}",{name}\n'
            m3u += f"{stream_url}\n"

with open("playlist.txt", "w", encoding="utf-8") as f:
    f.write(m3u)