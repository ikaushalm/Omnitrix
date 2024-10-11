import requests

def get_balance():
    url = "https://india.1xbet.com/api/internal/user/balance"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "fast_coupon=true; v3fr=1; lng=en; flaglng=en; typeBetNames=full; coefview=0; platform_type=desktop; auid=mjmZBWcJdAWhPk3sFFxuAg==; tzo=5.5; ggru=153; completed_user_settings=true; _gid=GA1.2.1984229050.1728672777; hdt=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoib0FIU3JyUUEvdStPVGtHR2Y0bVN0MUdMeHdBUGl5TDFkRnVkZGhEMkFERGt3a1cwRGMva29vaFZGMWxGLysrZnpPaTZRd3ltcS9CdVRWb2NLZVViejZ2T1dIanVtL3VORUZJUHcrQUpNRWxybVlENzFtMHpFRUUzNFUxZXhLNHI0M3RTUEJRQjdxVXB1cnJzV2FTZTViT1lCMllwMU5uZ0dQTlIvZG5YVFNxQ1VJQXYxSTJIVWcxSjlUYzh0Nm53dGlHNDE3bGwyeWxSRTE1Rng5WmVFdDFqcFphRWIyYjQ4RUtCTDNza2FGYWhuMFY2MnVacUJHTlFkVnkrZzFsbG5Mb1NDYURtd1llVVFKbWRoWnZXMnNBNXJLbURNUGZzTWdXN1VENG40WCtuMmVhRFF1MD0iLCJleHAiOjE3Mjg2ODcxNzksImlhdCI6MTcyODY3Mjc3OX0.nVL-D_LNz6Q49CRM9b0e1moERPysp40ZOtr1itxaKmnUfVoWkj3n7v5OMSDn0OS173BdUylI9hDDVWs-ZN9ihQ; sh.session.id=d4498fbf-9b25-4393-9866-cb30bfd99c98; _grant_1728690548=_ud14op92; ua=835718469; uhash=1c3bc6e92570e21b3da6ea7c93379e5d; cur=INR; SESSION=d9e0be76723fa850aee9bef87c806262; game_cols_count=2; disallow_sport=; pushfree_status=canceled; visit=2-5f1fe244c0fd46407494e9541fdf1c6e; _ga=GA1.2.1205925352.1728672777; _glhf=1728690680; _ga_7V60YW2S5H=GS1.1.1728672776.1.1.1728673287.60.1.1947932387; _gat_gtag_UA_131019888_1=1; _gat_gtag_UA_43962315_51=1",
        "priority": "u=1, i",
        "referer": "https://india.1xbet.com/en/casino/game/72348/dragon-tiger",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    response = requests.get(url, headers=headers)
    data=response.json()
    print(f"Balance: {data['balance'][0]['money']}")
    return float(data['balance'][0]['money'])

