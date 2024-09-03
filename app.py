from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from time import sleep
import requests
import json
import os
import random
import sys

class Fintopio:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'fintopio-tg.fintopio.com',
            'Origin': 'https://fintopio-tg.fintopio.com',
            'Pragma': 'no-cache',
            'Priority': 'u=3, i',
            'Referer': 'https://fintopio-tg.fintopio.com/',
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

    def referrals_data(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/referrals/data'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            referrals_data = response.json()
            if referrals_data is not None:
                return referrals_data
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Referrals Data ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")

    def daily_checkins(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/daily-checkins'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            daily_checkins = response.json()
            if daily_checkins is not None:
                self.print_timestamp(
                    f"{Fore.GREEN + Style.BRIGHT}[ Daily Checkins Claimed ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}[ Day {daily_checkins['totalDays']} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}[ Reward {daily_checkins['dailyReward']} ]{Style.RESET_ALL}"
                )
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Daily Checkins ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")

    def state_farming(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/farming/state'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            state_farming = response.json()
            if state_farming is not None:
                return state_farming
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Farm Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")

    def farm_farming(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/farming/farm'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            farm_farming = response.json()
            if farm_farming is not None:
                if farm_farming['state'] == 'farmed':
                    self.claim_farming(token=token)
                elif farm_farming['state'] == 'farming':
                    now = datetime.now().astimezone()
                    finish = datetime.fromtimestamp(farm_farming['timings']['finish'] / 1000).astimezone()
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Started ]{Style.RESET_ALL}")
                    if now >= finish:
                        self.claim_farming(token=token)
                    else:
                        formatted_finish = finish.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In Farm Farming Is {farm_farming['state']} ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Farm Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Has Been Already Started ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")

    def claim_farming(self, token: str, farmed: int):
        url = 'https://fintopio-tg.fintopio.com/api/farming/claim'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            claim_farming = response.json()
            if claim_farming is not None:
                if claim_farming['state'] == 'idling':
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Claimed {farmed} ]{Style.RESET_ALL}")
                    self.farm_farming(token=token)
                elif claim_farming['state'] == 'farming':
                    now = datetime.now().astimezone()
                    finish = datetime.fromtimestamp(claim_farming['timings']['finish'] / 1000).astimezone()
                    if now >= finish:
                        self.claim_farming(token=token)
                    else:
                        self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {claim_farming['farmed']} / {claim_farming['settings']['reward']} ]{Style.RESET_ALL}")
                        formatted_finish = finish.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No 'state' In Farm Farming ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Farm Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Is Not Finished Yet ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")

    def state_diamond(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/state'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            state_diamond = response.json()
            if state_diamond is not None:
                return state_diamond
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Farm Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")

    def complete_diamond(self, token: str, diamond_number: str, total_reward: str):
        url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/complete'
        data = json.dumps({'diamondNumber':diamond_number})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        try:
            response = self.session.post(url=url, headers=self.headers, data=data)
            response.raise_for_status()
            self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed {total_reward} From State Diamond ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_message_start = e.response.json()
            if e.response.status_code == 400 and error_message_start['message'] == 'Game is not available at the moment':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Game Is Not Available At The Moment ]{Style.RESET_ALL}")
            elif e.response.status_code == 400 and error_message_start['message'] == 'The diamond is outdated, reload the page and try again':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")

    def tasks(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/hold/tasks'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            tasks = response.json().get('tasks', [])
            for task in tasks:
                if task['status'] == 'available':
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting {task['slug']} ]{Style.RESET_ALL}")
                    self.start_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
                elif task['status'] == 'verified':
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming {task['slug']} ]{Style.RESET_ALL}")
                    self.claim_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    def start_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/start'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            start_tasks = response.json()
            if start_tasks is not None:
                if start_tasks['status'] == 'verifying':
                    sleep(random.choice([10, 20]))
                    self.claim_tasks(token=token, task_id=task_id, task_slug=task_slug, task_reward_amount=task_reward_amount)
                elif start_tasks['status'] == 'in-progress':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Please Try This Task By Itself ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'status' In Start Tasks Is {start_tasks['status']} ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Start Tasks ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_message_start = e.response.json()
            if e.response.status_code == 400 and error_message_start['message'] == 'Unable to update task status':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unable To Update Task Status. Please Try This Task By Itself ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")

    def claim_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/claim'
        self.headers.update({'Authorization': f'Bearer {token}'})
        while True:
            try:
                response = self.session.post(url=url, headers=self.headers)
                response.raise_for_status()
                claim_tasks = response.json()
                if claim_tasks is not None:
                    if claim_tasks['status'] == 'completed':
                        self.print_timestamp(
                            f"{Fore.GREEN + Style.BRIGHT}[ Claimed {task_slug} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Reward {task_reward_amount} ]{Style.RESET_ALL}"
                        )
                        break
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'status' In Claim Tasks Is {claim_tasks['status']} ]{Style.RESET_ALL}")
                        break
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Start Tasks ]{Style.RESET_ALL}")
                    break
            except requests.HTTPError as e:
                error_message_claim = e.response.json()
                if e.response.status_code == 400 and error_message_claim['message'] == 'Entity not found':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {task_slug} Not Found ]{Style.RESET_ALL}")
                    break
                elif e.response.status_code == 400 and error_message_claim['message'] == 'Unable to update task status':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Please Wait Until {task_slug} Is Claimed ]{Style.RESET_ALL}")
                    sleep(random.choice([5, 10]))
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                    break
            except requests.RequestException as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                break
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                break

    def main(self):
        while True:
            try:
                with open('tokens.txt', 'r') as file:
                    tokens = [line.strip() for line in file.readlines()]
                
                all_finish_times = []
                all_next_at_times = []
                
                for index, token in enumerate(tokens):
                    referrals_data = self.referrals_data(token=token)
                    if referrals_data['isDailyRewardClaimed']:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Balance {referrals_data['balance']} ]{Style.RESET_ALL}"
                        )
                    else:
                        self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                        self.daily_checkins(token=token)
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Farming ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    state_farming = self.state_farming(token=token)
                    if state_farming['state'] == 'farmed':
                        self.claim_farming(token=token, farmed=state_farming['farmed'])
                    elif state_farming['state'] == 'idling':
                        self.farm_farming(token=token)
                    elif state_farming['state'] == 'farming':
                        now = datetime.now().astimezone()
                        finish = datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone()
                        all_finish_times.append(finish)
                        if now >= finish:
                            self.claim_farming(token=token, farmed=state_farming['farmed'])
                        else:
                            self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {state_farming['farmed']} / {state_farming['settings']['reward']} ]{Style.RESET_ALL}")
                            formatted_finish = finish.strftime('%x %X %Z')
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In State Farming Is {state_farming['state']} ]{Style.RESET_ALL}")
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    self.tasks(token=token)
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Diamond ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    state_diamond = self.state_diamond(token=token)
                    if state_diamond['state'] == 'available':
                        self.complete_diamond(token=token, diamond_number=state_diamond['diamondNumber'], total_reward=state_diamond['settings']['totalReward'])
                    elif state_diamond['state'] == 'unavailable':
                        next_at = datetime.fromtimestamp(state_diamond['timings']['nextAt'] / 1000).astimezone()
                        all_next_at_times.append(next_at)
                        formatted_next_at = next_at.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Diamond Can Be Complete At {formatted_next_at} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In State Diamond Is {state_diamond['state']} ]{Style.RESET_ALL}")

                now = datetime.now().astimezone()
                next_sleep_time = None

                if all_finish_times:
                    next_sleep_time = min(all_finish_times)
                if all_next_at_times:
                    next_next_at_time = min(all_next_at_times)
                    if next_sleep_time is None or next_next_at_time < next_sleep_time:
                        next_sleep_time = next_next_at_time

                if next_sleep_time:
                    sleep_time = (next_sleep_time - now).total_seconds()
                    if sleep_time > 0:
                        sleep_timestamp = now + timedelta(seconds=sleep_time)
                        timestamp_sleep_time = sleep_timestamp.strftime('%X %Z')
                        self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {timestamp_sleep_time} ]{Style.RESET_ALL}")
                        sleep(sleep_time)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        fintopio = Fintopio()
        fintopio.main()
    except (Exception, requests.ConnectionError, requests.JSONDecodeError) as e:
        fintopio.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)