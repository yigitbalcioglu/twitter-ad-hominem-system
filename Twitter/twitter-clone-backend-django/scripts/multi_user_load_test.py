from __future__ import annotations

import argparse
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class UserRunResult:
    username: str
    register_ok: bool
    login_ok: bool
    tweet_success_count: int
    error: str = ""


def random_suffix(length: int = 8) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def register_user(base_url: str, email: str, username: str, password: str, timeout: int) -> None:
    response = requests.post(
        f"{base_url}/auth/register/",
        json={"email": email, "username": username, "password": password},
        timeout=timeout,
    )
    if response.status_code != 201:
        raise RuntimeError(f"register failed ({response.status_code}): {response.text}")


def login_user(base_url: str, email: str, password: str, timeout: int) -> str:
    response = requests.post(
        f"{base_url}/auth/token/",
        json={"email": email, "password": password},
        timeout=timeout,
    )
    if response.status_code != 200:
        raise RuntimeError(f"login failed ({response.status_code}): {response.text}")

    data = response.json()
    access = data.get("access")
    if not access:
        raise RuntimeError("login response has no access token")
    return access


def create_tweet(base_url: str, token: str, content: str, timeout: int) -> None:
    response = requests.post(
        f"{base_url}/tweets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": content},
        timeout=timeout,
    )
    if response.status_code != 201:
        raise RuntimeError(f"tweet failed ({response.status_code}): {response.text}")


def run_single_user(base_url: str, password: str, tweets_per_user: int, timeout: int) -> UserRunResult:
    suffix = random_suffix()
    username = f"load_{suffix}"
    email = f"{username}@example.com"

    try:
        register_user(base_url, email, username, password, timeout)
    except Exception as exc:
        return UserRunResult(username=username, register_ok=False, login_ok=False, tweet_success_count=0, error=str(exc))

    try:
        token = login_user(base_url, email, password, timeout)
    except Exception as exc:
        return UserRunResult(username=username, register_ok=True, login_ok=False, tweet_success_count=0, error=str(exc))

    success_count = 0
    for index in range(1, tweets_per_user + 1):
        try:
            create_tweet(
                base_url,
                token,
                content=f"[{username}] parallel test tweet #{index}",
                timeout=timeout,
            )
            success_count += 1
        except Exception as exc:
            return UserRunResult(
                username=username,
                register_ok=True,
                login_ok=True,
                tweet_success_count=success_count,
                error=str(exc),
            )

    return UserRunResult(
        username=username,
        register_ok=True,
        login_ok=True,
        tweet_success_count=success_count,
    )


def summarize(results: List[UserRunResult], tweets_per_user: int, elapsed_seconds: float) -> None:
    total_users = len(results)
    register_ok = sum(1 for result in results if result.register_ok)
    login_ok = sum(1 for result in results if result.login_ok)
    total_tweets = sum(result.tweet_success_count for result in results)
    expected_tweets = total_users * tweets_per_user

    print("\n=== Multi-User Load Test Summary ===")
    print(f"Total users:           {total_users}")
    print(f"Register success:      {register_ok}/{total_users}")
    print(f"Login success:         {login_ok}/{total_users}")
    print(f"Tweet success:         {total_tweets}/{expected_tweets}")
    print(f"Elapsed time:          {elapsed_seconds:.2f}s")
    print(f"Throughput (tweets/s): {(total_tweets / elapsed_seconds) if elapsed_seconds > 0 else 0:.2f}")

    failures = [result for result in results if result.error]
    if failures:
        print("\nSample failures:")
        for result in failures[:10]:
            print(f"- {result.username}: {result.error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel multi-user register/login/tweet load test")
    parser.add_argument("--base-url", default="http://localhost:8000/api/v1", help="Backend base URL")
    parser.add_argument("--users", type=int, default=30, help="Number of users to simulate")
    parser.add_argument("--tweets-per-user", type=int, default=2, help="Tweets per user")
    parser.add_argument("--workers", type=int, default=10, help="Parallel worker count")
    parser.add_argument("--password", default="strong-pass-123", help="Password to use for all test users")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout seconds")
    args = parser.parse_args()

    start = time.perf_counter()
    results: List[UserRunResult] = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                run_single_user,
                args.base_url,
                args.password,
                args.tweets_per_user,
                args.timeout,
            )
            for _ in range(args.users)
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "OK" if not result.error else "FAIL"
            print(
                f"[{status}] {result.username} | reg={result.register_ok} login={result.login_ok} tweets={result.tweet_success_count}/{args.tweets_per_user}"
            )

    elapsed = time.perf_counter() - start
    summarize(results, args.tweets_per_user, elapsed)


if __name__ == "__main__":
    main()
