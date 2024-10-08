from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from urllib.parse import parse_qs
import asyncio, json, os, re, sys

class Fintopio:
    def __init__(self) -> None:
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'fintopio-tg.fintopio.com',
            'Pragma': 'no-cache',
            'Priority': 'u=3, i',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    def process_queries(self, lines_per_file: int):
        if not os.path.exists('queries.txt'):
            raise FileNotFoundError(f"File 'queries.txt' not found. Please ensure it exists.")

        with open('queries.txt', 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
        if not queries:
            raise ValueError("File 'queries.txt' is empty.")

        existing_queries = set()
        for file in os.listdir():
            if file.startswith('queries-') and file.endswith('.txt'):
                with open(file, 'r') as qf:
                    existing_queries.update(line.strip() for line in qf if line.strip())

        new_queries = [query for query in queries if query not in existing_queries]
        if not new_queries:
            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ No New Queries To Add ]{Style.RESET_ALL}")
            return

        files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
        files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

        last_file_number = int(re.findall(r'\d+', files[-1])[0]) if files else 0

        for i in range(0, len(new_queries), lines_per_file):
            chunk = new_queries[i:i + lines_per_file]
            if files and len(open(files[-1], 'r').readlines()) < lines_per_file:
                with open(files[-1], 'a') as outfile:
                    outfile.write('\n'.join(chunk) + '\n')
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Updated '{files[-1]}' ]{Style.RESET_ALL}")
            else:
                last_file_number += 1
                queries_file = f"queries-{last_file_number}.txt"
                with open(queries_file, 'w') as outfile:
                    outfile.write('\n'.join(chunk) + '\n')
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Generated '{queries_file}' ]{Style.RESET_ALL}")

    def load_queries(self, file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    async def generate_token(self, query: str):
        url = f'https://fintopio-tg.fintopio.com/api/auth/telegram?{query}'
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=self.headers) as response:
                    response.raise_for_status()
                    generate_token = await response.json()
                    user_data = json.loads(parse_qs(query)['user'][0])
                    first_name = user_data.get('first_name', self.faker.first_name())
                    return (generate_token['token'], first_name)
        except (Exception, ClientResponseError) as e:
            self.print_timestamp(
                f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}"
            )
            return None

    async def generate_tokens(self, queries):
        tasks = [self.generate_token(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def init_fast(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/fast/init'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError):
            return False

    async def activate_referrals(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/referrals/activate'
        data = json.dumps({'code':'l5bYPIC8FtjMColV'})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError):
            return False

    async def init_fast_hold(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/hold/fast/init'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Init Fast Hold: {str(e)} ]{Style.RESET_ALL}")
            return None
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Init Fast Hold: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def daily_checkins(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/daily-checkins'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'Origin': 'https://fintopio-tg.fintopio.com'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    response.raise_for_status()
                    daily_checkins = await response.json()
                    if daily_checkins['claimed']:
                        return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You\'ve Already Claim Daily Checkins ]{Style.RESET_ALL}")
                    return self.print_timestamp(
                        f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {daily_checkins['dailyReward']} From Daily Checkins ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}[ Day {daily_checkins['totalDays']} ]{Style.RESET_ALL}"
                    )
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")

    async def complete_diamond(self, token: str, diamond_number: str, total_reward: str):
        url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/complete'
        data = json.dumps({'diamondNumber':diamond_number})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    if response.status == 400:
                        error_complete_diamond = await response.json()
                        if error_complete_diamond['message'] == 'Game is not available at the moment':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Game Is Not Available At The Moment ]{Style.RESET_ALL}")
                        elif error_complete_diamond['message'] == 'The diamond is outdated, reload the page and try again':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
                        elif error_complete_diamond['message'] == 'Game is already finished, please wait until the next one is available':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
                        elif error_complete_diamond['message']['diamondNumber']['isNumberString'] == 'diamondNumber must be a number string':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Diamond Number Must Be A Number String ]{Style.RESET_ALL}")
                    response.raise_for_status()
                    return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {total_reward} From State Diamond ]{Style.RESET_ALL}")
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")

    async def state_farming(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/farming/state'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
            return None
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def farm_farming(self, token: str, farmed: int):
        url = 'https://fintopio-tg.fintopio.com/api/farming/farm'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    if response.status == 400:
                        error_farm_farming = await response.json()
                        if error_farm_farming['message'] == 'Farming has been already started':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Has Been Already Started ]{Style.RESET_ALL}")
                    response.raise_for_status()
                    farm_farming = await response.json()
                    if farm_farming['state'] == 'farmed':
                        return await self.claim_farming(token=token, farmed=farmed)
                    elif farm_farming['state'] == 'farming':
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Started And Can Be Claim At {datetime.fromtimestamp(farm_farming['timings']['finish'] / 1000).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")

    async def claim_farming(self, token: str, farmed: int):
        url = 'https://fintopio-tg.fintopio.com/api/farming/claim'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    if response.status == 400:
                        error_claim_farming = await response.json()
                        if error_claim_farming['message'] == 'Farming is not finished yet':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Is Not Finished Yet ]{Style.RESET_ALL}")
                    response.raise_for_status()
                    claim_farming = await response.json()
                    if claim_farming['state'] == 'idling':
                        self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {farmed} From Farming ]{Style.RESET_ALL}")
                        return await self.farm_farming(token=token, farmed=farmed)
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")

    async def tasks(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/hold/tasks'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    tasks = await response.json()
                    for task in tasks['tasks']:
                        if task['status'] == 'available':
                            await self.start_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
                        elif task['status'] == 'verified':
                            await self.claim_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def start_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/start'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    if response.status == 400:
                        error_start_tasks = await response.json()
                        if error_start_tasks['message'] == 'Unable to update task status':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unable To Update Task Status. Please Try This Task By Itself ]{Style.RESET_ALL}")
                    response.raise_for_status()
                    start_tasks = await response.json()
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ {task_slug} Started ]{Style.RESET_ALL}")
                    if start_tasks['status'] == 'verifying':
                        return await self.claim_tasks(token=token, task_id=task_id, task_slug=task_slug, task_reward_amount=task_reward_amount)
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def claim_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/claim'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json'
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    if response.status == 400:
                        error_claim_tasks = await response.json()
                        if error_claim_tasks['message'] == 'Entity not found':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {task_slug} Not Found ]{Style.RESET_ALL}")
                        elif error_claim_tasks['message'] == 'Unable to update task status':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unable To Update {task_slug} Status ]{Style.RESET_ALL}")
                    response.raise_for_status()
                    claim_tasks = await response.json()
                    if claim_tasks['status'] == 'completed':
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {task_reward_amount} From {task_slug} ]{Style.RESET_ALL}")
        except ClientResponseError as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def main(self, queries: str):
        while True:
            try:
                accounts = await self.generate_tokens(queries=queries)
                restart_times = []
                total_balance = 0

                for (token, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home/Gem ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.init_fast(token=token)
                    await self.activate_referrals(token=token)
                    init_fast_hold = await self.init_fast_hold(token=token)
                    if init_fast_hold is not None:
                        total_balance += int(float(init_fast_hold['referralData']['balance']))
                        await self.daily_checkins(token=token)

                        if init_fast_hold['clickerDiamondState']['state'] == 'available':
                            await self.complete_diamond(token=token, diamond_number=init_fast_hold['clickerDiamondState']['diamondNumber'], total_reward=init_fast_hold['clickerDiamondState']['settings']['totalReward'])
                        else:
                            restart_times.append(datetime.fromtimestamp(init_fast_hold['clickerDiamondState']['timings']['nextAt'] / 1000).astimezone().timestamp())
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Diamond Can Be Complete At {datetime.fromtimestamp(init_fast_hold['clickerDiamondState']['timings']['nextAt'] / 1000).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")

                for (token, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Tasks/Farming ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    state_farming = await self.state_farming(token=token)
                    if state_farming is not None:
                        if state_farming['state'] == 'farmed':
                            await self.claim_farming(token=token, farmed=state_farming['farmed'])
                        elif state_farming['state'] == 'idling':
                            await self.farm_farming(token=token, farmed=state_farming['farmed'])
                        elif state_farming['state'] == 'farming':
                            if datetime.now().astimezone() >= datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone():
                                await self.claim_farming(token=token, farmed=state_farming['farmed'])
                            else:
                                restart_times.append(datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone().timestamp())
                                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")

                for (token, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.tasks(token=token)

                self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ Total Account {len(accounts)} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Total Balance {total_balance} ]{Style.RESET_ALL}"
                )

                if restart_times:
                    wait_times = [restart_time_end - datetime.now().astimezone().timestamp() for restart_time_end in restart_times if restart_time_end > datetime.now().astimezone().timestamp()]
                    if wait_times:
                        sleep_time = min(wait_times) + 30
                    else:
                        sleep_time = 15 * 60
                else:
                    sleep_time = 15 * 60

                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {(datetime.now().astimezone() + timedelta(seconds=sleep_time)).strftime('%X %Z')} ]{Style.RESET_ALL}")
                await asyncio.sleep(sleep_time)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        init(autoreset=True)
        fintopio = Fintopio()
        
        queries_files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
        queries_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

        fintopio.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 1 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Split Queries ]{Style.RESET_ALL}"
        )
        fintopio.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 2 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Use Existing 'queries-*.txt' ]{Style.RESET_ALL}"
        )
        fintopio.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 3 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Use 'queries.txt' Without Splitting ]{Style.RESET_ALL}"
        )

        initial_choice = int(input(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}[ Select An Option ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
        ))
        if initial_choice == 1:
            accounts = int(input(
                f"{Fore.YELLOW + Style.BRIGHT}[ How Much Account That You Want To Process Each Terminal ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            ))
            fintopio.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Processing Queries To Generate Files ]{Style.RESET_ALL}")
            fintopio.process_queries(lines_per_file=accounts)

            queries_files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
            queries_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

            if not queries_files:
                raise FileNotFoundError("No 'queries-*.txt' Files Found")
        elif initial_choice == 2:
            if not queries_files:
                raise FileNotFoundError("No 'queries-*.txt' Files Found")
        elif initial_choice == 3:
            queries = [line.strip() for line in open('queries.txt') if line.strip()]
        else:
            raise ValueError("Invalid Initial Choice. Please Run The Script Again And Choose A Valid Option")

        if initial_choice in [1, 2]:
            fintopio.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Select The Queries File To Use ]{Style.RESET_ALL}")
            for i, queries_file in enumerate(queries_files, start=1):
                fintopio.print_timestamp(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ {i} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}[ {queries_file} ]{Style.RESET_ALL}"
                )

            choice = int(input(
                f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}[ Select 'queries-*.txt' File ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            )) - 1
            if choice < 0 or choice >= len(queries_files):
                raise ValueError("Invalid Choice. Please Run The Script Again And Choose A Valid Option")

            selected_file = queries_files[choice]
            queries = fintopio.load_queries(selected_file)
        asyncio.run(fintopio.main(queries=queries))
    except (ValueError, IndexError, FileNotFoundError) as e:
        fintopio.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)