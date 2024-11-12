import aiohttp
import asyncio
import time

async def get_balance(retries=3, delay=2):
    url = "https://india.1xbet.com/api/internal/user/balance"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
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

    timeout = aiohttp.ClientTimeout(total=30)  # Set timeout for the request

    while retries > 0:
        try:
            # Send the GET request asynchronously
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()  # Will raise an error for 4xx or 5xx HTTP statuses
                    
                    # Attempt to parse the response as JSON
                    data = await response.json()
                    
                    # Check if 'balance' exists and is structured correctly
                    if 'balance' in data and isinstance(data['balance'], list) and len(data['balance']) > 0:
                        money = data['balance'][0].get('money')
                        if money is not None:
                            print(f"Balance: {money}")
                            return float(money)
                        else:
                            print("Error: 'money' key is missing in the balance object.")
                            return None  # Return None if the 'money' key is missing
                    else:
                        print("Error: 'balance' key is missing or malformed.")
                        return None  # Return None if 'balance' is malformed

        except (asyncio.TimeoutError, aiohttp.ClientResponseError, aiohttp.ClientError) as e:
            print(f"Error occurred: {e}. Retrying... ({4 - retries}/{3})")
            retries -= 1
            time.sleep(delay)  # Wait before retrying
            delay *= 2  # Exponential backoff for next retry
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying... ({4 - retries}/{3})")
            retries -= 1
            time.sleep(delay)
            delay *= 2

    print("Max retries reached. Returning None.")
    return None  # Return None after all retries fail
