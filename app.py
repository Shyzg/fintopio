import asyncio
import aiohttp
from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from time import sleep
from aiohttp import (
    ClientSession,
    ClientResponseError,
    ClientTimeout
)
import json
import os
import random
import sys

class Fintopio:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'fintopio-tg.fintopio.com',
            'Pragma': 'no-cache',
            'Referer': 'https://fintopio-tg.fintopio.com/hold?reflink=l5bYPIC8FtjMColV',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random,
            'webapp': 'true'
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

    async def get_token(self, queries: str):
        if not queries:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Empty Query Found ]{Style.RESET_ALL}")
        tokens = []
        async with ClientSession(timeout=ClientTimeout(total=20)) as session:
            for query in queries:
                url = f'https://fintopio-tg.fintopio.com/api/auth/telegram?{query}'
                try:
                    async with session.get(url=url, headers=self.headers) as response:
                        response.raise_for_status()
                        get_token = await response.json()
                        token = get_token['token']
                        tokens.append(token)
                except ClientResponseError as e:
                    self.print_timestamp(
                        f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ {str(e.message)} ]{Style.RESET_ALL}"
                    )
            return tokens

    async def init_fast(self, token: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/fast/init'
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}'
                }
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Init Fast: {str(e.message)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Init Fast: {str(e)} ]{Style.RESET_ALL}")

    async def activate_referrals(self, token: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/referrals/activate'
                data = json.dumps({'code':'l5bYPIC8FtjMColV'})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Content-Type': 'application/json',
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return True
        except ClientResponseError:
            return False
        except Exception:
            return False

    async def init_fast_hold(self, token: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/hold/fast/init'
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}'
                }
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Init Fast Hold: {str(e.message)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Init Fast Hold: {str(e)} ]{Style.RESET_ALL}")

    async def daily_checkins(self, token: str, first_name: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/daily-checkins'
                data = json.dumps({})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Content-Type': 'application/json',
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    daily_checkins = await response.json()
                    if daily_checkins['claimed']:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Checkins Already Claimed ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Reward {daily_checkins['dailyReward']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Day {daily_checkins['totalDays']} ]{Style.RESET_ALL}"
                        )
                    else:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ Daily Checkins Claimed ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Reward {daily_checkins['dailyReward']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Day {daily_checkins['totalDays']} ]{Style.RESET_ALL}"
                        )
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Daily Checkins: {str(e.message)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")

    async def complete_diamond(self, token: str, first_name: str, diamond_number: str, total_reward: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/complete'
                data = json.dumps({'diamondNumber':diamond_number})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Content-Type': 'application/json',
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    if response.status == 200:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ Claimed {total_reward} From State Diamond ]{Style.RESET_ALL}"
                        )
                    elif response.status == 400:
                        complete_diamond = await response.json()
                        if complete_diamond['message'] == 'Game is not available at the moment':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Game Is Not Available At The Moment ]{Style.RESET_ALL}")
                        elif complete_diamond['message'] == 'The diamond is outdated, reload the page and try again':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
                        elif complete_diamond['message'] == 'Game is already finished, please wait until the next one is available':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
                        elif complete_diamond['message']['diamondNumber']['isNumberString'] == 'diamondNumber must be a number string':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Diamond Number Must Be A Number String ]{Style.RESET_ALL}")
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Diamond: {str(response.reason)} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Diamond: {str(response.reason)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")

    async def state_farming(self, token: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/farming/state'
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}'
                }
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e.message)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")

    async def farm_farming(self, token: str, farmed: int, first_name: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/farming/farm'
                data = json.dumps({})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    if response.status == 200:
                        farm_farming = await response.json()
                        if farm_farming['state'] == 'farmed':
                            await self.claim_farming(token=token, farmed=farmed, first_name=first_name)
                        elif farm_farming['state'] == 'farming':
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}[ Farming Started ]{Style.RESET_ALL}"
                            )
                            if datetime.now().astimezone() >= datetime.fromtimestamp(farm_farming['timings']['finish'] / 1000).astimezone():
                                await self.claim_farming(token=token, farmed=farmed, first_name=first_name)
                            else:
                                formatted_finish = datetime.fromtimestamp(farm_farming['timings']['finish'] / 1000).astimezone().strftime('%x %X %Z')
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}"
                                )
                    elif response.status == 400:
                        error_farm_farming = await response.json()
                        if error_farm_farming['message'] == 'Farming has been already started':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Has Been Already Started ]{Style.RESET_ALL}")
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farm Farming: {str(response.reason)} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farm Farming: {str(response.reason)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")

    async def claim_farming(self, token: str, farmed: int, first_name: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/farming/claim'
                data = json.dumps({})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    if response.status == 200:
                        claim_farming = await response.json()
                        if claim_farming['state'] == 'idling':
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}[ Farming Claimed {farmed} ]{Style.RESET_ALL}"
                            )
                            await self.farm_farming(token=token, farmed=farmed, first_name=first_name)
                        elif claim_farming['state'] == 'farming':
                            if datetime.now().astimezone() >= datetime.fromtimestamp(claim_farming['timings']['finish'] / 1000).astimezone():
                                await self.claim_farming(token=token, farmed=farmed, first_name=first_name)
                            else:
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {claim_farming['farmed']} / {claim_farming['settings']['reward']} ]{Style.RESET_ALL}"
                                )
                                formatted_finish = datetime.fromtimestamp(claim_farming['timings']['finish'] / 1000).astimezone().strftime('%x %X %Z')
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}"
                                )
                    elif response.status == 400:
                        error_claim_farming = await response.json()
                        if error_claim_farming['message'] == 'Farming is not finished yet':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Is Not Finished Yet ]{Style.RESET_ALL}")
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Farming: {str(response.reason)} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Farming: {str(response.reason)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")

    async def tasks(self, token: str, first_name: str):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = 'https://fintopio-tg.fintopio.com/api/hold/tasks'
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}'
                }
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    tasks = await response.json()
                    for task in tasks['tasks']:
                        if task['status'] == 'available':
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Starting {task['slug']} ]{Style.RESET_ALL}"
                            )
                            await self.start_tasks(token=token, first_name=first_name, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
                        elif task['status'] == 'verified':
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Claiming {task['slug']} ]{Style.RESET_ALL}"
                            )
                            await self.claim_tasks(token=token, first_name=first_name, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
        except ClientResponseError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Tasks: {str(e.message)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def start_tasks(self, token: str, first_name: str, task_id: int, task_slug: str, task_reward_amount: int):
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/start'
                data = json.dumps({})
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {token}',
                    'Content-Length': str(len(data)),
                    'Origin': 'https://fintopio-tg.fintopio.com'
                }
                async with session.post(url=url, headers=headers, data=data) as response:
                    if response.status == 201:
                        start_tasks = await response.json()
                        if start_tasks['status'] == 'verifying':
                            sleep(random.choice([10, 20]))
                            await self.claim_tasks(token=token, first_name=first_name, task_id=task_id, task_slug=task_slug, task_reward_amount=task_reward_amount)
                        elif start_tasks['status'] == 'in-progress':
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}[ Finish This {task_slug} By Itself ]{Style.RESET_ALL}"
                            )
                    elif response.status == 400:
                        error_start_tasks = await response.json()
                        if error_start_tasks['message'] == 'Unable to update task status':
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unable To Update Task Status. Please Try This Task By Itself ]{Style.RESET_ALL}")
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Tasks: {str(response.reason)} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Tasks: {str(response.reason)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def claim_tasks(self, token: str, first_name: str, task_id: int, task_slug: str, task_reward_amount: int):
        while True:
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/claim'
                    data = json.dumps({})
                    headers = {
                        **self.headers,
                        'Authorization': f'Bearer {token}',
                        'Content-Length': str(len(data)),
                        'Origin': 'https://fintopio-tg.fintopio.com'
                    }
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 201:
                            claim_tasks = await response.json()
                            if claim_tasks['status'] == 'completed':
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ Claimed {task_slug} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.BLUE + Style.BRIGHT}[ Reward {task_reward_amount} ]{Style.RESET_ALL}"
                                )
                                break
                        elif response.status == 400:
                            error_claim_tasks = await response.json()
                            if error_claim_tasks['message'] == 'Entity not found':
                                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {task_slug} Not Found ]{Style.RESET_ALL}")
                                break
                            elif error_claim_tasks['message'] == 'Unable to update task status':
                                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Please Wait Until {task_slug} Is Claimed ]{Style.RESET_ALL}")
                                sleep(random.choice([5, 10]))
                            else:
                                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Tasks: {str(response.reason)} ]{Style.RESET_ALL}")
                                break
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Tasks: {str(response.reason)} ]{Style.RESET_ALL}")
                            break
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                break

    async def main(self):
        while True:
            try:
                queries = [line.strip() for line in open('queries.txt') if line.strip()]
                tokens = await self.get_token(queries=queries)
                restart_times = []

                for token in tokens:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Home/Gem ]{Style.RESET_ALL}")

                    init_fast = await self.init_fast(token=token)
                    first_name = init_fast['profile']['firstName'] if init_fast else Faker().first_name()

                    await self.activate_referrals(token=token)

                    init_fast_hold = await self.init_fast_hold(token=token)
                    self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}[ Balance {init_fast_hold['referralData']['balance']} ]{Style.RESET_ALL}"
                    )

                    await self.daily_checkins(token=token, first_name=first_name)

                    if init_fast_hold['clickerDiamondState']['state'] == 'available':
                        await self.complete_diamond(token=token, first_name=first_name, diamond_number=init_fast_hold['clickerDiamondState']['diamondNumber'], total_reward=init_fast_hold['clickerDiamondState']['settings']['totalReward'])
                    else:
                        formatted_next_at = datetime.fromtimestamp(init_fast_hold['clickerDiamondState']['timings']['nextAt'] / 1000).astimezone().strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Diamond Can Be Complete At {formatted_next_at} ]{Style.RESET_ALL}")

                    restart_times.append(datetime.fromtimestamp(init_fast_hold['clickerDiamondState']['timings']['nextAt'] / 1000).astimezone().timestamp())
                for token in tokens:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Tasks/Farming ]{Style.RESET_ALL}")

                    init_fast = await self.init_fast(token=token)
                    first_name = init_fast['profile']['firstName'] if init_fast else Faker().first_name()

                    state_farming = await self.state_farming(token=token)
                    if state_farming['state'] == 'farmed':
                        await self.claim_farming(token=token, farmed=state_farming['farmed'], first_name=first_name)
                    elif state_farming['state'] == 'idling':
                        await self.farm_farming(token=token, farmed=state_farming['farmed'], first_name=first_name)
                    elif state_farming['state'] == 'farming':
                        if datetime.now().astimezone() >= datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone():
                            await self.claim_farming(token=token, farmed=state_farming['farmed'], first_name=first_name)
                        else:
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {state_farming['farmed']} / {state_farming['settings']['reward']} ]{Style.RESET_ALL}"
                            )
                            formatted_finish = datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone().strftime('%x %X %Z')
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}"
                            )
                    restart_times.append(datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone().timestamp())
                for token in tokens:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}")
                    
                    init_fast = await self.init_fast(token=token)
                    first_name = init_fast['profile']['firstName'] if init_fast else Faker().first_name()

                    await self.tasks(token=token, first_name=first_name)

                if restart_times:
                    now = datetime.now().astimezone().timestamp()
                    wait_times = [restart_time_end - now for restart_time_end in restart_times if restart_time_end > now]
                    if wait_times:
                        sleep_time = min(wait_times) + 30
                    else:
                        sleep_time = 15 * 60
                else:
                    sleep_time = 15 * 60

                sleep_timestamp = datetime.now().astimezone() + timedelta(seconds=sleep_time)
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {sleep_timestamp.strftime('%X %Z')} ]{Style.RESET_ALL}")
                sleep(sleep_time)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        fintopio = Fintopio()
        asyncio.run(fintopio.main())
    except KeyboardInterrupt:
        sys.exit(0)