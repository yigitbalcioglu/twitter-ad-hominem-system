import asyncio
import uuid

import requests
import websockets

BASE = "http://localhost:8000/api/v1"
WS_BASE = "ws://localhost:8000"


def setup_users():
    uid = uuid.uuid4().hex[:8]
    u1 = {
        "email": f"ws_{uid}_a@example.com",
        "username": f"ws_{uid}_a",
        "password": "strong-pass-123",
    }
    u2 = {
        "email": f"ws_{uid}_b@example.com",
        "username": f"ws_{uid}_b",
        "password": "strong-pass-123",
    }

    for payload in (u1, u2):
        response = requests.post(f"{BASE}/auth/register/", json=payload, timeout=10)
        print("register", payload["username"], response.status_code)

    t1 = requests.post(
        f"{BASE}/auth/token/",
        json={"email": u1["email"], "password": u1["password"]},
        timeout=10,
    )
    t2 = requests.post(
        f"{BASE}/auth/token/",
        json={"email": u2["email"], "password": u2["password"]},
        timeout=10,
    )
    print("token", t1.status_code, t2.status_code)

    a1 = t1.json()["access"]
    a2 = t2.json()["access"]

    h1 = {"Authorization": f"Bearer {a1}"}
    h2 = {"Authorization": f"Bearer {a2}"}

    me1 = requests.get(f"{BASE}/auth/me/", headers=h1, timeout=10).json()
    me2 = requests.get(f"{BASE}/auth/me/", headers=h2, timeout=10).json()
    print("users", me1["username"], me1["id"], me2["username"], me2["id"])

    f1 = requests.post(f"{BASE}/auth/follows/{me2['id']}/toggle/", headers=h1, timeout=10)
    f2 = requests.post(f"{BASE}/auth/follows/{me1['id']}/toggle/", headers=h2, timeout=10)
    print("follow", f1.status_code, f1.json(), f2.status_code, f2.json())

    send = requests.post(
        f"{BASE}/auth/messages/{me2['id']}/",
        headers={**h1, "Content-Type": "application/json"},
        json={"text": "e2e http message"},
        timeout=10,
    )
    print("send_http", send.status_code, send.json().get("text"))

    return me1, me2, a1, a2


async def websocket_flow(me1, me2, a1, a2):
    url_for_user1 = f"{WS_BASE}/ws/messages/{me2['id']}/?token={a1}"
    url_for_user2 = f"{WS_BASE}/ws/messages/{me1['id']}/?token={a2}"

    async with websockets.connect(url_for_user1) as ws1, websockets.connect(url_for_user2) as ws2:
        await ws1.send('{"text":"e2e websocket message"}')

        received_1 = await asyncio.wait_for(ws1.recv(), timeout=10)
        received_2 = await asyncio.wait_for(ws2.recv(), timeout=10)

        print("ws_recv_user1", received_1)
        print("ws_recv_user2", received_2)


if __name__ == "__main__":
    me1, me2, a1, a2 = setup_users()
    asyncio.run(websocket_flow(me1, me2, a1, a2))
    print("E2E_WS_OK")
