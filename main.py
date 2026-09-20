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
        self.max_sub_trades = 3
        self.sub_trade_gap_pct = 0.010
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
        self.round_allocations = {
            1: 0.01, 2: 0.02, 3: 0.04, 4: 0.06, 5: 0.10,
            6: 0.20, 7: 0.30, 8: 0.27, 9: 0.00, 10: 0.00
        }
        self.round_risk_profile = {
            1: {"risk": 90, "gap": 0.0020, "bounce": 1.0006, "min_profit": 0.25},
            2: {"risk": 80, "gap": 0.0030, "bounce": 1.0008, "min_profit": 0.50},
            3: {"risk": 70, "gap": 0.0040, "bounce": 1.0010, "min_profit": 0.75},
            4: {"risk": 60, "gap": 0.0055, "bounce": 1.0012, "min_profit": 1.00},
            5: {"risk": 50, "gap": 0.0070, "bounce": 1.0015, "min_profit": 1.25},
            6: {"risk": 40, "gap": 0.0090, "bounce": 1.0018, "min_profit": 1.50},
            7: {"risk": 30, "gap": 0.0110, "bounce": 1.0022, "min_profit": 2.00},
            8: {"risk": 20, "gap": 0.0140, "bounce": 1.0028, "min_profit": 2.50},
            9: {"risk": 10, "gap": 0.0180, "bounce": 1.0035, "min_profit": 3.00},
            10: {"risk": 0, "gap": 0.0250, "bounce": 1.0050, "min_profit": 5.00}
        }
        self.sub_ts_high = 0.0
        self.sub_ts_low = 0.0

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
            if trade_val >= 8000.0:
                if not is_buyer_maker:
                    recent_buy_vol += trade_val
                else:
                    recent_sell_vol += trade_val
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
            "activePositions": self.active_positions,
            "tradesHistory": self.trades_history,
            "botThought": ai_thoughts
        }

    def execute_buy(self, is_sub_trade=False, escalate_round=False):
        if self.usdt_balance <= 10 or self.live_price <= 0:
            return

        if not is_sub_trade and not escalate_round:
            self.sync_phase_and_round()

        base_alloc = self.round_allocations.get(self.active_round, 0.20)
        sub_alloc = base_alloc / (self.max_sub_trades + 1)
        all_sol = self.sol_balance + self.macro_vault_sol
        total_account_val = self.usdt_balance + (all_sol * self.live_price)
        vol_multiplier = 1.25 if self.whale_sentiment == "BULLISH" else (0.85 if self.whale_sentiment == "BEARISH" else 1.0)
        invest_target = max(10.0, total_account_val * sub_alloc * vol_multiplier)

        if invest_target > self.usdt_balance:
            invest_target = self.usdt_balance

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_bought = net_invest / self.live_price
        self.usdt_balance -= invest_target

        if is_sub_trade:
            self.sub_trade_count += 1
        else:
            self.sub_trade_count = 0
            self.round_base_price = self.live_price

        pos_id = str(uuid.uuid4())[:8]

        if self.active_round == 8:
            self.macro_vault_sol += sol_bought
            self.macro_vault_invested += invest_target
            self.macro_vault_entry = self.macro_vault_invested / self.macro_vault_sol if self.macro_vault_sol > 0 else 0.0
            self.macro_target_price = round(self.macro_vault_entry * 2.0, 2)
            pos_label = f"R8 27% MACRO VAULT (Entry {self.sub_trade_count + 1})"
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
            target_exit = round(self.live_price * 1.05, 2)
            pos_label = f"R{self.active_round} (Entry {self.sub_trade_count + 1})"
            pos = {
                "id": pos_id,
                "round": self.active_round,
                "subTrade": self.sub_trade_count,
                "label": pos_label,
                "entryPrice": round(self.live_price, 2),
                "solAmount": round(sol_bought, 4),
                "invested": round(invest_target, 2),
                "isMacro": False,
                "isSubTrade": is_sub_trade,
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
def execute_sub_trade_sell(self, pos_id):
        target_pos = None
        target_idx = -1
        for idx, p in enumerate(self.active_positions):
            if p.get("id") == pos_id:
                target_pos = p
                target_idx = idx
                break

        if not target_pos:
            return

        sol_to_sell = target_pos["solAmount"]
        invested = target_pos["invested"]
        sold_value = sol_to_sell * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - invested

        if profit <= 0:
            return

        self.usdt_balance += net_return
        self.sol_balance -= sol_to_sell
        self.invested_amount -= invested
        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0
        self.realized_pnl += profit

        self.trades_history.insert(0, {
            "orderId": str(uuid.uuid4())[:8],
            "side": "SELL_SUB",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_to_sell, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": self.active_round,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self.active_positions.pop(target_idx)
        if self.sub_trade_count > 0:
            self.sub_trade_count -= 1
        self.sub_ts_high = 0.0
        self.sub_ts_low = 0.0
        self.tb_active = False

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

        if profit <= 0:
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

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            return

        if self.is_paused:
            return

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]

        if len(regular_positions) == 0:
            if not self.initial_tb_active:
                self.initial_tb_active = True
                self.initial_tb_peak = self.live_price
                self.initial_tb_lowest = self.live_price
                return

            if self.live_price >= self.initial_tb_peak:
                self.initial_tb_peak = self.live_price
                self.initial_tb_lowest = self.live_price
                return

            if self.live_price < self.initial_tb_lowest:
                self.initial_tb_lowest = self.live_price

            drop_from_peak = (self.initial_tb_peak - self.initial_tb_lowest) / self.initial_tb_peak if self.initial_tb_peak > 0 else 0.0
            is_buyer_ready = self.check_market_exhaustion(mode="BUY")

            if drop_from_peak >= 0.002:
                bounce_factor = 1.0008 if (is_buyer_ready or self.whale_sentiment == "BULLISH") else 1.0012
                required_bounce_price = self.initial_tb_lowest * bounce_factor
                if self.live_price >= required_bounce_price:
                    self.execute_buy(is_sub_trade=False, escalate_round=False)
            elif len(self.price_history) >= 12 and not is_buyer_ready:
                self.execute_buy(is_sub_trade=False, escalate_round=False)
            return

        active_sub_trades = [p for p in regular_positions if p.get("isSubTrade", False)]
        risk_cfg = self.round_risk_profile.get(self.active_round, {"gap": 0.005, "bounce": 1.0015, "min_profit": 0.50})

        if len(active_sub_trades) > 0:
            latest_sub = active_sub_trades[-1]
            sub_entry = latest_sub["entryPrice"]
            sub_invested = latest_sub["invested"]
            sub_sol = latest_sub["solAmount"]

            est_return = (sub_sol * self.live_price) * (1.0 - self.taker_fee_pct)
            net_profit_est = est_return - sub_invested

            if net_profit_est >= risk_cfg["min_profit"]:
                if self.live_price > self.sub_ts_high:
                    self.sub_ts_high = self.live_price

                if net_profit_est >= (risk_cfg["min_profit"] * 2.5):
                    sub_trail_pct = 0.9988
                elif net_profit_est >= (risk_cfg["min_profit"] * 1.5):
                    sub_trail_pct = 0.9980
                else:
                    sub_trail_pct = 0.9972

                calc_sub_stop = round(self.sub_ts_high * sub_trail_pct, 2)
                if calc_sub_stop > self.sub_ts_low:
                    self.sub_ts_low = calc_sub_stop

                if self.live_price <= self.sub_ts_low and self.sub_ts_low > sub_entry:
                    self.execute_sub_trade_sell(latest_sub["id"])
                    return
            else:
                self.sub_ts_high = self.live_price
                self.sub_ts_low = 0.0

        if self.sub_trade_count < self.max_sub_trades:
            last_entry = regular_positions[-1]["entryPrice"]
            dynamic_gap = max(0.20, last_entry * risk_cfg["gap"])

            if not self.tb_active:
                if self.live_price <= (last_entry - dynamic_gap):
                    self.tb_active = True
                    self.tb_lowest_price = self.live_price
            else:
                if self.live_price < self.tb_lowest_price:
                    self.tb_lowest_price = self.live_price

                if self.live_price > (last_entry + dynamic_gap):
                    self.tb_active = False
                else:
                    bounce_target = self.tb_lowest_price * risk_cfg["bounce"]
                    allow_sub_buy = True if risk_cfg["risk"] >= 70 else (self.whale_sentiment != "BEARISH")
                    
                    if self.live_price >= bounce_target and allow_sub_buy:
                        self.tb_active = False
                        self.execute_buy(is_sub_trade=True)
                        return
        elif self.active_round < 8:
            last_entry = regular_positions[-1]["entryPrice"]
            if self.live_price <= (last_entry * 0.985):
                self.active_round += 1
                self.execute_buy(is_sub_trade=False, escalate_round=True)
                return

        if self.macro_vault_sol > 0 and self.live_price >= self.macro_target_price:
            if self.live_price > self.macro_ts_high:
                self.macro_ts_high = round(self.live_price, 2)

            calculated_macro_stop = round(self.macro_ts_high * 0.992, 2)
            if calculated_macro_stop > self.macro_ts_low:
                self.macro_ts_low = calculated_macro_stop

            if self.live_price <= self.macro_ts_low:
                self.execute_macro_sell()

        if self.avg_entry_price > 0:
            if self.live_price > self.ts_high:
                self.ts_high = round(self.live_price, 2)

            peak_gain_pct = (self.ts_high - self.avg_entry_price) / self.avg_entry_price
            is_seller_exhausted = self.check_market_exhaustion(mode="SELL")

            if self.active_round >= 5:
                min_profit_target = 0.035
            elif self.active_round >= 3:
                min_profit_target = 0.018
            elif self.active_round == 2:
                min_profit_target = 0.010
            else:
                min_profit_target = 0.006

            if peak_gain_pct >= min_profit_target:
                if peak_gain_pct >= 0.04 or is_seller_exhausted:
                    trail_factor = 0.9980
                    self.ts_stage = "0.20%"
                elif peak_gain_pct >= 0.02:
                    trail_factor = 0.9965
                    self.ts_stage = "0.35%"
                elif peak_gain_pct >= 0.01:
                    trail_factor = 0.9975
                    self.ts_stage = "0.25%"
                else:
                    trail_factor = 0.9982
                    self.ts_stage = "0.18%"

                calculated_stop = round(self.ts_high * trail_factor, 2)
                if calculated_stop > self.ts_low:
                    self.ts_low = calculated_stop

                if self.ts_low > self.avg_entry_price and self.live_price <= self.ts_low and self.live_price > self.avg_entry_price:
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

async def binance_price_worker():
    price_urls = [
        "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
        "https://api.binance.us/api/v3/ticker/price?symbol=SOLUSDT",
        "https://api.coinbase.com/v2/prices/SOL-USD/spot"
    ]
    whale_url = "https://api.binance.com/api/v3/aggTrades?symbol=SOLUSDT&limit=60"

    async with aiohttp.ClientSession() as session:
        while True:
            price = 0.0
            for url in price_urls:
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
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

            try:
                async with session.get(whale_url, timeout=aiohttp.ClientTimeout(total=3)) as whale_resp:
                    if whale_resp.status == 200:
                        trades_data = await whale_resp.json()
                        if isinstance(trades_data, list):
                            bot.process_market_trades(trades_data)
            except Exception:
                pass

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
                await manager.broadcast(json.dumps(bot.get_state()))
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
