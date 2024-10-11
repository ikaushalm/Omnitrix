import requests

# Define the URL
url = "https://india.1xbet.com/api/internal/user/balance"

# Define headers based on the curl command
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "fast_coupon=true; v3fr=1; lng=en; flaglng=en; typeBetNames=full; platform_type=desktop; auid=mjmZBWcC3hYDHgI2Euy5Ag==; tzo=5.5; completed_user_settings=true; _gid=GA1.2.263389482.1728241176; sh.session.id=447382d6-ebdf-45e8-aa57-5c96ee7ba7a3; pushfree_status=canceled; game_cols_count=2; spinOfThronesTwoModal_casino=true; spinOfThronesTwoModal_slots=true; application_locale=en; bettingView=0; visit=3-3622948242f982abb5e21d9ac15d1870; spinOfThronesTwoModalCounter=2; hdt=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoiMjgvRjJxR1ljQkFNKzJpMm5QNGg5bVpxUnUvb1FENXVNNmQ2OWJocUVYekR3Nm5kcmpnWThxb0VQOUhFVG1SbldINFp2cVIzL2xHWFpqb2lFUmJLUlN1ME1wMXNrNkZ5dW1JdU1tdE53YUZXbEFnYWR1L1dibWd4WStXUitid2wyYnF5MGNwbFdUaFVua3ZlZnAwOTVkTFpMcE9GN2NiNFRMMnhPek03bU9Ea0g0QU15bHQ2dG1wZzlxSUdqbndjdFlXWmdJRnBENW5VQ3kxU1loMmxQVU5vcnNZNkxoY1RpM1MySzBmb1NDbHNHOEVZcndmSWw2ZnhTTWhjczE3eG5jQmhQeThaOVRUVlBYU1hPREpJanVzUU0wbG1QRDRUYWVIQWdYMFZjc3VIZ0xIMHliWT0iLCJleHAiOjE3MjgyNjk5ODgsImlhdCI6MTcyODI1NTU4OH0.rP28ktEJ5g6eSTTmrm_sgRlSVdZd_C4-Oynmhbke4gKA0qcGUSRZLbjh5odExWm4eOGcYayacNouEkjw57uc2A; dnb=1; _glhf=1728274912; ggru=146; _ga=GA1.2.331155337.1728241176; _grant_1728274912=_ud71op89; ua=835718469; uhash=1c3bc6e92570e21b3da6ea7c93379e5d; cur=INR; SESSION=73e26accb807a21967f316966c6e2718; disallow_sport=; _gat_gtag_UA_43962315_51=1; _ga_7V60YW2S5H=GS1.1.1728241176.1.1.1728257192.60.1.889205518; _gat_gtag_UA_131019888_1=1",
    "priority": "u=1, i",
    "referer": "https://india.1xbet.com/en/casino/game/72348/dragon-tiger",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# Send the GET request with the specified headers
response = requests.get(url, headers=headers)

# Print the response status and data
print("Status Code:", response.status_code)
print("Response Data:", response.text)
data = response.json()
print(f' print {data['balance'][0]['money']}')
