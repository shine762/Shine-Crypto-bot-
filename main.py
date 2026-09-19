import asyncio
import json
import random
from datetime import datetime, timezone
import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpotMartingaleBot:
    def __init__(self):
        self.is_paused = False
        self.live_price = 0.0
        self.usdt_balance = 10000.0
        self.sol_balance = 0.0
        self.invested_amount = 0.0
        self.avg_entry_price = 0.0
        self.ts_high = 0.0
        self.ts_low = 0.0
        self.active_phase = 1
        self.active_round = 6
        self.sub_trade_count = 0
        self.max_sub_trades = 3
        self.sub_trade_gap = 2.0
        self.round_range_size = 25.0
        self.round_base_price = 110.0
        self.realized_pnl = 0.0
        self.cooldown_remaining = 0
        self.active_positions = []
        self.trades_history = []
        self.round_allocations = {
            1: 0.01, 2: 0.02, 3: 0.04, 4: 0.06, 5: 0.10,
            6: 0.20, 7: 0.30, 8: 0.27
        }

    def get_state(self):
        total_cap = self.usdt_balance + (self.sol_balance * self.live_price)
        unrealized_pnl = 0.0
        pnl_pct = 0.0

        if self.sol_balance > 0 and self.avg_entry_price > 0:
            unrealized_pnl = (self.live_price - self.avg_entry_price) * self.sol_balance
            pnl_pct = ((self.live_price - self.avg_entry_price) / self.avg_entry_price) * 100.0

        alloc_pct = self.round_allocations.get(self.active_round, 0.20) * 100.0

        return {
            "price": self.live_price,
            "livePrice": self.live_price,
            "pnl": round(unrealized_pnl, 2),
            "pnlPct": round(pnl_pct, 2),
            "usdtBalance": round(self.usdt_balance, 2),
            "solBalance": round(self.sol_balance, 4),
            "avgEntryPrice": round(self.avg_entry_price, 2),
            "investedAmount": round(self.invested_amount, 2),
            "totalCapital": round(total_cap, 2),
            "tsHigh": round(self.ts_high, 2),
            "tsLow": round(self.ts_low, 2),
            "activePhase": self.active_phase,
            "activeRound": self.active_round,
            "allocationPct": str(alloc_pct),
            "realizedPnl": round(self.realized_pnl, 2),
            "cooldownRemaining": self.cooldown_remaining,
            "activePositions": self.active_positions,
            "tradesHistory": self.trades_history
        }

    def execute_buy(self, is_sub_trade=False):
        if self.usdt_balance <= 10 or self.live_price <= 0:
            return

        base_alloc = self.round_allocations.get(self.active_round, 0.20)
        sub_alloc = base_alloc / (self.max_sub_trades + 1)
        invest_target = 10000.0 * sub_alloc

        if invest_target > self.usdt_balance:
            invest_target = self.usdt_balance

        sol_bought = invest_target / self.live_price
        self.usdt_balance -= invest_target
        self.sol_balance += sol_bought
        self.invested_amount += invest_target

        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0

        if is_sub_trade:
            self.sub_trade_count += 1
        else:
            self.sub_trade_count = 0
            self.round_base_price = self.live_price

        pos_label = f"R{self.active_round} (Entry {self.sub_trade_count + 1})"
        pos = {
            "round": self.active_round,
            "subTrade": self.sub_trade_count,
            "label": pos_label,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4)
        }
        self.active_positions.append(pos)

        tx_hash = "5KqW" + str(len(self.trades_history) + 1) + "xP" + str(random.randint(1000, 9999)) + "DEX"
        self.trades_history.insert(0, {
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "round": self.active_round,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "txHash": tx_hash
        })

        self.ts_high = 0.0
        self.ts_low = 0.0

    def execute_sell_all_in_profit(self):
        if self.sol_balance <= 0 or self.live_price <= 0:
            return

        sold_value = self.sol_balance * self.live_price
        profit = sold_value - self.invested_amount

        if profit <= 0:
            return

        self.usdt_balance += sold_value
        self.realized_pnl += profit

        tx_hash = "5KqW" + str(len(self.trades_history) + 1) + "xP" + str(random.randint(1000, 9999)) + "DEX"
        self.trades_history.insert(0, {
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(self.sol_balance, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "txHash": tx_hash
        })

        self.sol_balance = 0.0
        self.invested_amount = 0.0
        self.avg_entry_price = 0.0
        self.ts_high = 0.0
        self.ts_low = 0.0
        self.sub_trade_count = 0
        self.active_positions = []
        self.cooldown_remaining = 60

    def update_price_tick(self, new_price):
        if new_price <= 0:
            return

        self.live_price = new_price

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            return

        if self.is_paused:
            return

        if len(self.active_positions) == 0:
            self.execute_buy(is_sub_trade=False)
            return

        last_entry = self.active_positions[-1]["entryPrice"]

        if self.live_price <= (last_entry - self.sub_trade_gap):
            if self.sub_trade_count < self.max_sub_trades:
                self.execute_buy(is_sub_trade=True)
                return
            elif self.live_price <= (self.round_base_price - self.round_range_size):
                if self.active_round < 8:
                    self.active_round += 1
                    self.execute_buy(is_sub_trade=False)
                    return

        profit_target_price = self.avg_entry_price * 1.012

        if self.live_price >= profit_target_price:
            if self.live_price > self.ts_high:
                self.ts_high = self.live_price
                self.ts_low = round(self.ts_high * 0.99, 2)

            if self.ts_low > self.avg_entry_price and self.live_price <= self.ts_low:
                self.execute_sell_all_in_profit()

bot = SpotMartingaleBot()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

async def binance_price_worker():
    urls = [
        "https://api.binance.us/api/v3/ticker/price?symbol=SOLUSDT",
        "https://api.coinbase.com/v2/prices/SOL-USD/spot",
        "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
    ]
    async with aiohttp.ClientSession() as session:
        while True:
            price = 0.0
            for url in urls:
                try:
                    async with session.get(url, timeout=3) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if "price" in data:
                                price = float(data["price"])
                            elif "data" in data and "amount" in data["data"]:
                                price = float(data["data"]["amount"])
                            if price > 0:
                                break
                except Exception:
                    continue

            if price > 0:
                bot.update_price_tick(price)
                state_payload = json.dumps(bot.get_state())
                await manager.broadcast(state_payload)

            await asyncio.sleep(1.5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(binance_price_worker())

@app.get("/")
def home():
    return {"status": "SHINE Dynamic DCA Engine Active"}

@app.get("/status")
def get_status():
    return bot.get_state()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_text(json.dumps(bot.get_state()))
        while True:
            data_text = await websocket.receive_text()
            try:
                msg = json.loads(data_text)
                if msg.get("action") == "PAUSE":
                    bot.is_paused = True
                elif msg.get("action") == "RESUME":
                    bot.is_paused = False
                await manager.broadcast(json.dumps(bot.get_state()))
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
