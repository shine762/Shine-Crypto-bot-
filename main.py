import asyncio
import json
import uuid
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

class UltraQuantSpotBot:
    def __init__(self):
        self.is_paused = False
        self.live_price = 0.0
        self.usdt_balance = 10000.0
        self.sol_balance = 0.0
        self.invested_amount = 0.0
        self.avg_entry_price = 0.0
        self.ts_high = 0.0
        self.ts_low = 0.0
        self.ts_stage = "1.0%"
        self.tb_active = False
        self.tb_lowest_price = 0.0
        self.active_phase = 1
        self.active_round = 1
        self.sub_trade_count = 0
        self.max_sub_trades = 10
        self.sub_trade_gap_pct = 0.008
        self.round_range_size = 25.0
        self.round_base_price = 0.0
        self.realized_pnl = 0.0
        self.cooldown_remaining = 0
        self.active_positions = []
        self.trades_history = []
        self.price_history = []
        self.initial_tb_active = False
        self.initial_tb_peak = 0.0
        self.initial_tb_lowest = 0.0
        self.initial_capital = 10000.0
        self.macro_vault_sol = 0.0
        self.macro_vault_invested = 0.0
        self.macro_vault_entry = 0.0
        self.macro_target_price = 0.0
        self.macro_ts_high = 0.0
        self.macro_ts_low = 0.0
        self.whale_buy_vol = 0.0
        self.whale_sell_vol = 0.0
        self.whale_orderflow_ratio = 50.0
        self.whale_sentiment = "NEUTRAL"
        self.taker_fee_pct = 0.001
        self.min_net_profit_usdt = 0.1
        self.round_allocations = {
            1: 0.01, 2: 0.02, 3: 0.04, 4: 0.06, 5: 0.10,
            6: 0.20, 7: 0.30, 8: 0.27, 9: 0.0, 10: 0.0
        }

    def process_market_trades(self, trades):
        if not trades:
            return
        recent_buy_vol = 0.0
        recent_sell_vol = 0.0
        for t in trades:
            price = float(t.get("p", 0.0))
            qty = float(t.get("q", 0.0))
            is_buyer_maker = t.get("m", False)
            trade_val = price * qty
            # Sirf $25,000 se $50,000+ ki institutional trades count hongi
            if trade_val >= 25000.0:
                # $50,000+ wali super-whale trade ko extra weightage milega
                multiplier = 1.5 if trade_val >= 50000.0 else 1.0
                weighted_val = trade_val * multiplier
                if not is_buyer_maker:
                    recent_buy_vol += weighted_val
                else:
                    recent_sell_vol += weighted_val
        total_whale_vol = recent_buy_vol + recent_sell_vol
        if total_whale_vol > 0:
            self.whale_buy_vol = recent_buy_vol
            self.whale_sell_vol = recent_sell_vol
            self.whale_orderflow_ratio = round((recent_buy_vol / total_whale_vol) * 100.0, 1)
            if self.whale_orderflow_ratio >= 60.0:
                self.whale_sentiment = "BULLISH"
            elif self.whale_orderflow_ratio <= 40.0:
                self.whale_sentiment = "BEARISH"
            else:
                self.whale_sentiment = "NEUTRAL"

    def sync_phase_and_round(self):
        if self.live_price <= 0:
            return
        step = 250.0
        phase = int(self.live_price / step) + 1
        if phase > 10:
            phase = 10
        if phase < 1:
            phase = 1
        self.active_phase = phase
        phase_max = phase * step
        round_step = step / 10.0
        calculated_round = int((phase_max - self.live_price) / round_step) + 1
        if calculated_round < 1:
            calculated_round = 1
        if calculated_round > 10:
            calculated_round = 10
        if len([p for p in self.active_positions if not p.get("isMacro", False)]) == 0:
            self.active_round = calculated_round

    def get_state(self):
        all_sol = self.sol_balance + self.macro_vault_sol
        all_invested = self.invested_amount + self.macro_vault_invested
        total_cap = self.usdt_balance + (all_sol * self.live_price)
        unrealized_pnl = 0.0
        pnl_pct = 0.0

        if all_sol > 0 and all_invested > 0:
            current_val = all_sol * self.live_price
            unrealized_pnl = current_val - all_invested
            pnl_pct = (unrealized_pnl / all_invested) * 100.0

        alloc_pct = self.round_allocations.get(self.active_round, 0.20) * 100.0
        combined_entry = (all_invested / all_sol) if all_sol > 0 else 0.0

        ai_thoughts = ""
        regular_pos = [p for p in self.active_positions if not p.get("isMacro", False)]
        if self.is_paused:
            ai_thoughts = "Main abhi paused hoon. Aap jab chaho RUNNING button daba kar mujhe market scan karne ki ijazat de sakte ho."
        elif self.cooldown_remaining > 0:
            ai_thoughts = f"Pichla profit kamyabi se book ho gaya hai! Main abhi {self.cooldown_remaining} seconds ke cool-down par hoon taake jaldbaazi mein galat trade na le loon."
        elif len(regular_pos) == 0:
            if self.whale_sentiment == "BEARISH":
                ai_thoughts = f"Market mein barhay sellers (Whales) dabao daal rahay hain ({self.whale_orderflow_ratio}% sell volume). Is liye main safe side par baith kar entry roak raha hoon."
            else:
                target_dip_val = round(self.live_price * 0.982, 2)
                ai_thoughts = f"Scanning orderbook: Current price is ${round(self.live_price, 2)} with {self.whale_orderflow_ratio}% Buy Volume. Waiting for dip confirmation near ${target_dip_val} to trigger safety buy."
        else:
            last_entry = regular_pos[-1]["entryPrice"]
            if self.live_price > self.avg_entry_price:
                ai_thoughts = f"Zabardast! Trade munafay mein hai. Entry ${round(self.avg_entry_price, 2)} thi aur ab price ${round(self.live_price, 2)} hai. Trailing Stop active hai taake zyada se zyada faida lock kiya ja sakay."
            else:
                ai_thoughts = f"Market meri entry price (${last_entry}) se thora neechay chal rahi hai. Main panic nahi kar raha, mera DCA Trailing buy order tayyar hai jaise hi bounce confirm hoga agla level execute ho jaye ga."

        return {
            "isPaused": self.is_paused,
            "price": self.live_price,
            "livePrice": self.live_price,
            "pnl": round(unrealized_pnl, 2),
            "pnlPct": round(pnl_pct, 2),
            "usdtBalance": round(self.usdt_balance, 2),
            "solBalance": round(all_sol, 4),
            "avgEntryPrice": round(combined_entry, 2),
            "investedAmount": round(all_invested, 2),
            "totalCapital": round(total_cap, 2),
            "tsHigh": round(self.ts_high, 2),
            "tsLow": round(self.ts_low, 2),
            "trailingStage": self.ts_stage,
            "activePhase": self.active_phase,
            "activeRound": self.active_round,
            "allocationPct": str(alloc_pct),
            "realizedPnl": round(self.realized_pnl, 2),
            "cooldownRemaining": self.cooldown_remaining,
            "macroVaultSol": round(self.macro_vault_sol, 4),
            "macroVaultInvested": round(self.macro_vault_invested, 2),
            "whaleOrderflow": self.whale_orderflow_ratio,
            "whaleSentiment": self.whale_sentiment,
            "canManualTrade": self.active_round in [9, 10],
            "subTradeCount": self.sub_trade_count,
            "maxSubTrades": self.max_sub_trades,
            "activePositions": self.active_positions,
            "tradesHistory": self.trades_history,
            "botThought": ai_thoughts
        }

    def execute_buy(self, is_sub_trade=False, escalate_round=False):
        if self.usdt_balance <= 5 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return

        if not is_sub_trade and not escalate_round:
            self.sync_phase_and_round()

        base_alloc = self.round_allocations.get(self.active_round, 0.01)
        sub_alloc = base_alloc / float(self.max_sub_trades)
        all_sol = self.sol_balance + self.macro_vault_sol
        total_account_val = self.usdt_balance + (all_sol * self.live_price)
        vol_multiplier = 1.2 if self.whale_sentiment == "BULLISH" else (0.9 if self.whale_sentiment == "BEARISH" else 1.0)
        invest_target = max(5.0, total_account_val * sub_alloc * vol_multiplier)

        if invest_target > self.usdt_balance:
            invest_target = self.usdt_balance

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_bought = net_invest / self.live_price
        self.usdt_balance -= invest_target

        if is_sub_trade:
            self.sub_trade_count += 1
        else:
            self.sub_trade_count = 1
            self.round_base_price = self.live_price

        pos_id = str(uuid.uuid4())[:8]

        if self.active_round == 8:
            self.macro_vault_sol += sol_bought
            self.macro_vault_invested += invest_target
            self.macro_vault_entry = self.macro_vault_invested / self.macro_vault_sol if self.macro_vault_sol > 0 else 0.0
            self.macro_target_price = round(max(200.0, self.macro_vault_entry * 2.0), 2)
            pos_label = f"R8 27% HOLD (Trade {self.sub_trade_count}/10)"
            pos = {
                "id": pos_id,
                "round": 8,
                "subTrade": self.sub_trade_count,
                "label": pos_label,
                "entryPrice": round(self.live_price, 2),
                "solAmount": round(sol_bought, 4),
                "invested": round(invest_target, 2),
                "isMacro": True,
                "targetPrice": self.macro_target_price
            }
        else:
            self.sol_balance += sol_bought
            self.invested_amount += invest_target
            self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0
            target_exit = round(self.avg_entry_price * 1.5, 2)
            pos_label = f"R{self.active_round} (Trade {self.sub_trade_count}/10)"
            pos = {
                "id": pos_id,
                "round": self.active_round,
                "subTrade": self.sub_trade_count,
                "label": pos_label,
                "entryPrice": round(self.live_price, 2),
                "solAmount": round(sol_bought, 4),
                "invested": round(invest_target, 2),
                "isMacro": False,
                "targetPrice": target_exit
            }

        self.active_positions.append(pos)
        self.trades_history.insert(0, {
            "orderId": pos_id,
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "fee": round(fee, 4),
            "round": self.active_round,
            "execType": "WHALE_MAKER_MATCHED",
            "orderflowRatio": self.whale_orderflow_ratio,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self.ts_high = round(self.live_price, 2)
        self.ts_low = round(self.live_price * 0.99, 2)
        self.ts_stage = "1.0%"
        self.tb_active = False
        self.initial_tb_active = False

    def execute_manual_buy(self, amount_usdt=50.0):
        if self.usdt_balance < amount_usdt or self.live_price <= 0:
            return
        fee = amount_usdt * self.taker_fee_pct
        net_invest = amount_usdt - fee
        sol_bought = net_invest / self.live_price
        self.usdt_balance -= amount_usdt
        self.sol_balance += sol_bought
        self.invested_amount += amount_usdt
        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0
        pos_id = str(uuid.uuid4())[:8]
        self.active_positions.append({
            "id": pos_id,
            "round": self.active_round,
            "subTrade": 99,
            "label": f"MANUAL BUY (R{self.active_round})",
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(amount_usdt, 2),
            "isMacro": False,
            "targetPrice": round(self.live_price * 2.0, 2)
        })
        self.trades_history.insert(0, {
            "orderId": pos_id,
            "side": "MANUAL_BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "fee": round(fee, 4),
            "round": self.active_round,
            "execType": "USER_MANUAL",
            "orderflowRatio": self.whale_orderflow_ratio,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def execute_manual_sell(self):
        if self.sol_balance <= 0 or self.live_price <= 0:
            return
        sold_value = self.sol_balance * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - self.invested_amount
        self.usdt_balance += net_return
        self.realized_pnl += profit
        self.trades_history.insert(0, {
            "orderId": str(uuid.uuid4())[:8],
            "side": "MANUAL_SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(self.sol_balance, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.sol_balance = 0.0
        self.invested_amount = 0.0
        self.avg_entry_price = 0.0
        self.active_positions = [p for p in self.active_positions if p.get("isMacro", False)]

    def execute_macro_sell(self):
        if self.macro_vault_sol <= 0 or self.live_price < self.macro_target_price:
            return

        sold_value = self.macro_vault_sol * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - self.macro_vault_invested

        if profit <= 0:
            return

        self.usdt_balance += net_return
        self.realized_pnl += profit

        self.trades_history.insert(0, {
            "orderId": str(uuid.uuid4())[:8],
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(self.macro_vault_sol, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self.active_positions = [p for p in self.active_positions if not p.get("isMacro", False)]
        self.macro_vault_sol = 0.0
        self.macro_vault_invested = 0.0
        self.macro_vault_entry = 0.0
        self.macro_ts_high = 0.0
        self.macro_ts_low = 0.0

    def execute_sell_all_in_profit(self):
        if self.sol_balance <= 0 or self.live_price <= 0:
            return

        sold_value = self.sol_balance * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - self.invested_amount

        if profit < self.min_net_profit_usdt:
            return

        self.usdt_balance += net_return
        self.realized_pnl += profit

        self.trades_history.insert(0, {
            "orderId": str(uuid.uuid4())[:8],
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(self.sol_balance, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self.sol_balance = 0.0
        self.invested_amount = 0.0
        self.avg_entry_price = 0.0
        self.ts_high = 0.0
        self.ts_low = 0.0
        self.ts_stage = "IDLE"
        self.sub_trade_count = 0
        self.active_round = 1
        self.active_positions = [p for p in self.active_positions if p.get("isMacro", False)]
        self.cooldown_remaining = 40
        self.tb_active = False
        self.initial_tb_active = False
        self.initial_tb_peak = 0.0
        self.initial_tb_lowest = 0.0

    def check_market_exhaustion(self, mode="SELL"):
        if len(self.price_history) < 6:
            return False
        recent = self.price_history[-6:]
        deltas = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
        up_momentum = sum(d for d in deltas if d > 0)
        down_momentum = abs(sum(d for d in deltas if d < 0))
        if mode == "SELL":
            return down_momentum > (up_momentum * 1.5)
        elif mode == "BUY":
            return (up_momentum > down_momentum) and (down_momentum > 0)
        return False

    def update_price_tick(self, new_price):
        if new_price <= 0:
            return

        self.live_price = new_price
        self.price_history.append(new_price)
        if len(self.price_history) > 50:
            self.price_history.pop(0)

        # 1. Round 6 Fix: Live price aate hi foran Round aur Phase sync hoga
        if len([p for p in self.active_positions if not p.get("isMacro", False)]) == 0:
            self.sync_phase_and_round()

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            return

        if self.is_paused:
            return

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]

        # 2. Intezar Khatam: Agar position nahi hai to BINA INTEZAR seedha BUY execute karo
        if len(regular_positions) == 0:
            self.execute_buy(is_sub_trade=False, escalate_round=False)
            return

        # 3. Har $2.00 drop par foran agli DCA trade (Whale ka intezar band)
        last_entry = regular_positions[-1]["entryPrice"]
        if (last_entry - self.live_price) >= 2.0:
            if self.sub_trade_count < self.max_sub_trades:
                self.execute_buy(is_sub_trade=True)
                return
            elif self.active_round < 8:
                self.active_round += 1
                self.sub_trade_count = 0
                self.execute_buy(is_sub_trade=False, escalate_round=True)
                return
            elif self.active_round < 10:
                self.active_round += 1
                self.sub_trade_count = 0
                return
        if self.macro_vault_sol > 0 and self.live_price >= self.macro_target_price:
            if self.live_price > self.macro_ts_high:
                self.macro_ts_high = round(self.live_price, 2)

            calculated_macro_stop = round(self.macro_ts_high * 0.99, 2)
            if calculated_macro_stop > self.macro_ts_low:
                self.macro_ts_low = calculated_macro_stop

            if self.live_price <= self.macro_ts_low:
                self.execute_macro_sell()

        if self.avg_entry_price > 0 and self.sol_balance > 0:
            projected_profit = (self.sol_balance * self.live_price * (1 - self.taker_fee_pct)) - self.invested_amount
            if self.live_price > self.ts_high:
                self.ts_high = round(self.live_price, 2)

            peak_gain_pct = (self.ts_high - self.avg_entry_price) / self.avg_entry_price

            if projected_profit >= self.min_net_profit_usdt:
                if peak_gain_pct >= 0.02:
                    trail_factor = 0.9975
                    self.ts_stage = "0.25%"
                elif peak_gain_pct >= 0.01:
                    trail_factor = 0.9950
                    self.ts_stage = "0.50%"
                else:
                    trail_factor = 0.9900
                    self.ts_stage = "1.0%"

                calculated_stop = round(self.ts_high * trail_factor, 2)
                if calculated_stop > self.ts_low:
                    self.ts_low = calculated_stop

                if self.live_price <= self.ts_low:
                    self.execute_sell_all_in_profit()
bot = UltraQuantSpotBot()

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

async def binance_ws_worker():
    # Direct millisecond live stream from Binance
    ws_url = "wss://stream.binance.com:9443/ws/solusdt@aggTrade"
    
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(ws_url, heartbeat=20.0) as ws:
                    last_broadcast = 0.0
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            price = float(data.get("p", 0.0))
                            qty = float(data.get("q", 0.0))
                            is_buyer_maker = data.get("m", False)

                            if price > 0:
                                # Har millisecond trade par whale check
                                bot.process_market_trades([{"p": price, "q": qty, "m": is_buyer_maker}])
                                
                                # Zero delay price update
                                bot.update_price_tick(price)

                                # Frontend par broadcast (har 150ms baad taake lag na ho)
                                now = asyncio.get_event_loop().time()
                                if now - last_broadcast >= 0.15:
                                    last_broadcast = now
                                    await manager.broadcast(json.dumps(bot.get_state()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
        except Exception:
            await asyncio.sleep(2.0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(binance_ws_worker())

@app.get("/")
def home():
    return {"status": "SHINE Ultra", "active": True}

@app.get("/status")
def get_bot_status():
    return bot.get_state()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_text(json.dumps(bot.get_state()))
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                action = msg.get("action")
                if action == "PAUSE":
                    bot.is_paused = True
                elif action == "RESUME":
                    bot.is_paused = False
                elif action == "MANUAL_BUY":
                    buy_amt = float(msg.get("amount", 50.0))
                    bot.execute_manual_buy(buy_amt)
                elif action == "MANUAL_SELL":
                    bot.execute_manual_sell()
                await manager.broadcast(json.dumps(bot.get_state()))
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
