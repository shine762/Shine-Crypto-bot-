import asyncio
import json
import uuid
import os
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

SUPABASE_URL = "https://awlaziaxapoixbhiqcpq.supabase.co"
SUPABASE_KEY = "sb_publishable_PgY6nJ0OeM4OIoJS3GVG8A_MZb--nVp"
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

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
        self.tb_stage = "IDLE"
        self.active_phase = 1
        self.active_round = 1
        self.sub_trade_count = 0
        self.max_sub_trades = 10
        self.round_trades_done = {r: 0 for r in range(1, 11)}
        self.realized_pnl = 0.0
        self.cooldown_remaining = 0
        self.active_positions = []
        self.trades_history = []
        self.manual_trades_history = []
        self.price_history = []
        self.latest_signal = {"action": "HOLD", "price": 0.0, "text": "Scanning market for high-probability signals..."}
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
        self.micro_positions = []
        self.micro_round_trades_done = {r: 0 for r in range(1, 11)}
        self.micro_tb_active = False
        self.micro_tb_lowest = 0.0
        self.micro_last_ref_price = 0.0
        self.micro_realized_pnl = 0.0
        self.micro_total_trades = 0
        self.killer2_positions = []
        self.killer2_round_trades_done = {r: 0 for r in range(1, 11)}
        self.killer2_tb_active = False
        self.killer2_tb_lowest = 0.0
        self.killer2_last_ref_price = 0.0
        self.killer2_realized_pnl = 0.0
        self.killer2_total_trades = 0
        self.killer3_positions = []
        self.killer3_round_trades_done = {r: 0 for r in range(1, 11)}
        self.killer3_tb_active = False
        self.killer3_tb_lowest = 0.0
        self.killer3_last_ref_price = 0.0
        self.killer3_realized_pnl = 0.0
        self.killer3_total_trades = 0
        self.harvester_active = False
        self.harvester_vault_sol = 0.0
        self.harvester_vault_invested = 0.0
        self.harvester_vault_cash = 0.0
        self.harvester_borrowed_r8 = 0.0
        self.harvester_last_action_price = 0.0
        self.harvester_realized_pnl = 0.0
        self.harvester_cycle_count = 0
        self.harvester_status = "IDLE (WAITING R6-R8)"

    
    async def load_from_database(self):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                async with session.get(f"{SUPABASE_URL}/rest/v1/bot_state?id=eq.1") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data and len(data) > 0:
                            row = data[0]
                            self.realized_pnl = float(row.get("realized_pnl", 0.0))
                            

                async with session.get(f"{SUPABASE_URL}/rest/v1/active_positions?order=created_at.asc") as resp:
                    if resp.status == 200:
                        pos_data = await resp.json()
                        if isinstance(pos_data, list):
                            self.active_positions = [{
                                "id": p.get("id"),
                                "round": p.get("round"),
                                "subTrade": p.get("sub_trade"),
                                "label": p.get("label"),
                                "entryPrice": float(p.get("entry_price", 0)),
                                "solAmount": float(p.get("sol_amount", 0)),
                                "invested": float(p.get("invested", 0)),
                                "isMacro": p.get("is_macro", False),
                                "targetPrice": float(p.get("target_price", 0))
                            } for p in pos_data]

                            regular_pos = [p for p in self.active_positions if not p.get("isMacro", False)]
                            macro_pos = [p for p in self.active_positions if p.get("isMacro", False)]

                            if len(regular_pos) > 0 or len(macro_pos) > 0:
                                self.sol_balance = sum(p["solAmount"] for p in regular_pos)
                                self.invested_amount = sum(p["invested"] for p in regular_pos)
                                self.macro_vault_sol = sum(p["solAmount"] for p in macro_pos)
                                self.macro_vault_invested = sum(p["invested"] for p in macro_pos)
                                total_spent = self.invested_amount + self.macro_vault_invested
                                self.usdt_balance = max(0.0, round(self.initial_capital + self.realized_pnl - total_spent, 2))
                                self.avg_entry_price = round(self.invested_amount / self.sol_balance, 2) if self.sol_balance > 0 else 0.0
                                self.sub_trade_count = len(regular_pos)
                                self.round_trades_done = {r: 0 for r in range(1, 11)}
                                for p in regular_pos:
                                    r_idx = p.get("round", 1)
                                    self.round_trades_done[r_idx] = self.round_trades_done.get(r_idx, 0) + 1
                            else:
                                self.sol_balance = 0.0
                                self.invested_amount = 0.0
                                self.avg_entry_price = 0.0
                                self.macro_vault_sol = 0.0
                                self.macro_vault_invested = 0.0
                                self.sub_trade_count = 0
                                self.round_trades_done = {r: 0 for r in range(1, 11)}
                                self.usdt_balance = round(self.initial_capital + self.realized_pnl, 2)

                            asyncio.create_task(self.db_sync_state())

                async with session.get(f"{SUPABASE_URL}/rest/v1/trades_history?order=created_at.desc&limit=100") as resp:
                    if resp.status == 200:
                        t_data = await resp.json()
                        if isinstance(t_data, list):
                            self.trades_history = [{
                                "orderId": t.get("order_id"),
                                "side": t.get("side"),
                                "price": float(t.get("price", 0)),
                                "solAmount": float(t.get("sol_amount", 0)),
                                "fee": float(t.get("fee", 0)),
                                "profit": float(t.get("profit", 0)),
                                "realizedPnl": float(t.get("profit", 0)),
                                "round": t.get("round"),
                                "execType": t.get("exec_type"),
                                "timestamp": t.get("created_at")
                            } for t in t_data]

                            self.micro_realized_pnl = 0.0
                            self.micro_total_trades = 0
                            self.killer2_realized_pnl = 0.0
                            self.killer2_total_trades = 0
                            spot_closed_profit = 0.0
                            for t in t_data:
                                if t.get("exec_type") == "MICRO_SCALP_EXIT":
                                    self.micro_total_trades += 1
                                    self.micro_realized_pnl += float(t.get("profit", 0.0))
                                elif t.get("exec_type") == "KILLER2_SCALP_EXIT":
                                    self.killer2_total_trades += 1
                                    self.killer2_realized_pnl += float(t.get("profit", 0.0))
                                elif t.get("side") == "SELL":
                                    spot_closed_profit += float(t.get("profit", 0.0))
                            self.killer3_realized_pnl = 0.0
                            self.killer3_total_trades = 0
                            for t in t_data:
                                if t.get("exec_type") == "KILLER3_SCALP_EXIT":
                                    self.killer3_total_trades += 1
                                    self.killer3_realized_pnl += float(t.get("profit", 0.0))
                            self.harvester_realized_pnl = 0.0
                            for t in t_data:
                                if t.get("exec_type") in ["HARVESTER_SWING_EXIT", "HARVESTER_GRAND_ATH_EXIT"]:
                                    self.harvester_realized_pnl += float(t.get("profit", 0.0))
                            self.realized_pnl = round(spot_closed_profit + self.micro_realized_pnl + self.killer2_realized_pnl + self.killer3_realized_pnl + self.harvester_realized_pnl, 2)

                
        except Exception:
            pass

    async def db_sync_state(self):
        try:
            payload = {
                "usdt_balance": round(self.usdt_balance, 2),
                "sol_balance": round(self.sol_balance, 4),
                "invested_amount": round(self.invested_amount, 2),
                "avg_entry_price": round(self.avg_entry_price, 2),
                "realized_pnl": round(self.realized_pnl, 2),
                "active_phase": self.active_phase,
                "active_round": self.active_round,
                "sub_trade_count": self.sub_trade_count,
                
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.patch(f"{SUPABASE_URL}/rest/v1/bot_state?id=eq.1", json=payload)
        except Exception:
            pass

    async def db_save_buy(self, pos, trade_data):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                pos_row = {
                    "id": pos["id"],
                    "round": pos["round"],
                    "sub_trade": pos["subTrade"],
                    "label": pos["label"],
                    "entry_price": pos["entryPrice"],
                    "sol_amount": pos["solAmount"],
                    "invested": pos["invested"],
                    "is_macro": pos["isMacro"],
                    "target_price": pos["targetPrice"]
                }
                await session.post(f"{SUPABASE_URL}/rest/v1/active_positions", json=pos_row)
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=trade_data)
            await self.db_sync_state()
        except Exception:
            pass

    async def db_save_sell_individual(self, pos_id, trade_data):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.delete(f"{SUPABASE_URL}/rest/v1/active_positions?id=eq.{pos_id}")
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=trade_data)
            await self.db_sync_state()
        except Exception:
            pass

    

    async def db_save_micro_trade(self, trade_data):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=trade_data)
            await self.db_sync_state()
        except Exception:
            pass

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
            if trade_val >= 1500.0:
                multiplier = 2.0 if trade_val >= 10000.0 else 1.0
                weighted_val = trade_val * multiplier
                if not is_buyer_maker:
                    recent_buy_vol += weighted_val
                else:
                    recent_sell_vol += weighted_val
        total_whale_vol = recent_buy_vol + recent_sell_vol
        if total_whale_vol > 0:
            self.whale_buy_vol = recent_buy_vol
            self.whale_sell_vol = recent_sell_vol
            ratio = round((recent_buy_vol / total_whale_vol) * 100.0, 1)
            self.whale_orderflow_ratio = max(38.0, min(72.0, ratio))
            if self.whale_orderflow_ratio >= 55.0:
                self.whale_sentiment = "BULLISH"
            elif self.whale_orderflow_ratio <= 45.0:
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
        self.active_round = calculated_round
        self.sub_trade_count = self.round_trades_done.get(self.active_round, 0)

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

        wallet_positions = getattr(self, 'wallet_active_positions', [])
        w_sol_total = sum(p["solAmount"] for p in wallet_positions)
        w_invested_total = sum(p["invested"] for p in wallet_positions)
        w_avg_entry = (w_invested_total / w_sol_total) if w_sol_total > 0 else 0.0

        return {
            "isPaused": self.is_paused,
            "price": self.live_price,
            "livePrice": self.live_price,
            "walletSol": round(w_sol_total, 4),
            "walletInvested": round(w_invested_total, 2),
            "walletAvgEntry": round(w_avg_entry, 2),
            "walletActivePositions": wallet_positions,
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
            "tbActive": self.tb_active,
            "tbStage": self.tb_stage,
            "tbLowest": round(self.tb_lowest_price, 2),
            "activePhase": self.active_phase,
            "activeRound": self.active_round,
            "allocationPct": str(alloc_pct),
            "realizedPnl": round(self.realized_pnl, 2),
            "cooldownRemaining": self.cooldown_remaining,
            "macroVaultSol": round(self.macro_vault_sol, 4),
            "macroVaultInvested": round(self.macro_vault_invested, 2),
            "whaleOrderflow": self.whale_orderflow_ratio,
            "whaleSentiment": self.whale_sentiment,
            "canManualTrade": True,
            "subTradeCount": self.sub_trade_count,
            "maxSubTrades": self.max_sub_trades,
            "activePositions": self.active_positions,
            "tradesHistory": self.trades_history,
            "manualTradesHistory": self.manual_trades_history,
            "latestSignal": self.latest_signal,
            "botThought": ai_thoughts,
            
            "microPositions": self.micro_positions,
            "microRealizedPnl": round(self.micro_realized_pnl, 4),
            "microTotalTrades": self.micro_total_trades,
            "microIdleFundAvail": round(self.get_scavenged_idle_fund(), 2),
            "killer2Positions": self.killer2_positions,
            "killer2RealizedPnl": round(self.killer2_realized_pnl, 4),
            "killer2TotalTrades": self.killer2_total_trades,
            "killer2IdleFundAvail": round(self.get_killer2_idle_fund(), 2),
            "killer3Positions": self.killer3_positions,
            "killer3RealizedPnl": round(self.killer3_realized_pnl, 4),
            "killer3TotalTrades": self.killer3_total_trades,
            "killer3IdleFundAvail": round(self.get_killer3_idle_fund(), 2),
            "harvesterActive": self.harvester_active,
            "harvesterSol": round(self.harvester_vault_sol, 4),
            "harvesterInvested": round(self.harvester_vault_invested, 2),
            "harvesterCash": round(self.harvester_vault_cash, 2),
            "harvesterBorrowed": round(self.harvester_borrowed_r8, 2),
            "harvesterRealizedPnl": round(self.harvester_realized_pnl, 4),
            "harvesterStatus": self.harvester_status,
            "harvesterCycle": self.harvester_cycle_count
        }

    def execute_buy(self, is_sub_trade=False, escalate_round=False):
        if self.usdt_balance <= 5 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return

        self.sync_phase_and_round()

        all_sol = self.sol_balance + self.macro_vault_sol
        total_account_val = self.usdt_balance + (all_sol * self.live_price)
        vol_multiplier = 1.2 if self.whale_sentiment == "BULLISH" else (0.9 if self.whale_sentiment == "BEARISH" else 1.0)

        if self.active_round == 8:
            leftover_trades = sum(max(0, 10 - self.round_trades_done.get(r, 0)) for r in range(1, 8))
            total_r8_trades = 10 + leftover_trades
            current_r8_done = self.round_trades_done.get(8, 0)
            if current_r8_done >= total_r8_trades:
                return
            trades_remaining = max(1, total_r8_trades - current_r8_done)
            invest_target = max(5.0, (self.usdt_balance / trades_remaining) * vol_multiplier)
        else:
            current_done = self.round_trades_done.get(self.active_round, 0)
            if current_done >= 10:
                return
            base_alloc = self.round_allocations.get(self.active_round, 0.01)
            sub_alloc = base_alloc / 10.0
            invest_target = max(5.0, total_account_val * sub_alloc * vol_multiplier)

        if invest_target > self.usdt_balance:
            invest_target = self.usdt_balance

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_bought = net_invest / self.live_price
        self.usdt_balance -= invest_target

        self.round_trades_done[self.active_round] = self.round_trades_done.get(self.active_round, 0) + 1
        self.sub_trade_count = self.round_trades_done[self.active_round]

        pos_id = str(uuid.uuid4())[:8]

        if self.active_round == 8:
            self.macro_vault_sol += sol_bought
            self.macro_vault_invested += invest_target
            self.macro_vault_entry = self.macro_vault_invested / self.macro_vault_sol if self.macro_vault_sol > 0 else 0.0
            self.macro_target_price = round(max(200.0, self.macro_vault_entry * 2.0), 2)
            pos_label = f"R8 Aggressive Vault (Trade {self.sub_trade_count})"
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
            target_exit = round(self.live_price + 0.40, 2)
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
                "targetPrice": target_exit,
                "ts_high": round(self.live_price, 2),
                "ts_low": 0.0
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

        self.latest_signal = {
            "action": "BUY",
            "price": round(self.live_price, 2),
            "text": f"BUY SOL NOW @ ${round(self.live_price, 2)} (Whale Rebound Confirmed)"
        }
        print(f">>> [TRADE SUCCESS] BUY Order Executed! Price: ${round(self.live_price, 2)} | Bought: {round(sol_bought, 4)} SOL | Round: {self.active_round}")

        asyncio.create_task(self.db_save_buy(pos, {
            "order_id": pos_id,
            "side": "BUY",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_bought, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": self.active_round,
            "exec_type": "WHALE_MAKER_MATCHED"
        }))

        self.ts_high = round(self.live_price, 2)
        self.ts_low = 0.0
        self.ts_stage = "1.0%"
        self.tb_active = False
        self.initial_tb_active = False

    def execute_manual_buy(self, amount_usdt=50.0):
        if amount_usdt <= 0 or self.live_price <= 0:
            return
        fee = amount_usdt * self.taker_fee_pct
        net_invest = amount_usdt - fee
        sol_bought = net_invest / self.live_price
        pos_id = str(uuid.uuid4())[:8]
        
        manual_pos = {
            "id": pos_id,
            "round": 0,
            "subTrade": 0,
            "label": "WALLET SPOT BUY",
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(amount_usdt, 2),
            "isManualWallet": True,
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        
        if not hasattr(self, 'wallet_active_positions'):
            self.wallet_active_positions = []
        self.wallet_active_positions.append(manual_pos)
        
        self.manual_trades_history.insert(0, {
            "orderId": pos_id,
            "side": "MANUAL_BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(amount_usdt, 2),
            "fee": round(fee, 4),
            "execType": "NON_CUSTODIAL_DEX",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        print(f">>> [WALLET MANUAL BUY] Bought {round(sol_bought, 4)} SOL @ ${round(self.live_price, 2)} directly into User Self-Custody Wallet.")

    def execute_manual_sell(self):
        if not hasattr(self, 'wallet_active_positions') or len(self.wallet_active_positions) == 0:
            return
        if self.live_price <= 0:
            return
            
        total_sol = sum(p["solAmount"] for p in self.wallet_active_positions)
        total_invested = sum(p["invested"] for p in self.wallet_active_positions)
        
        if total_sol <= 0:
            return
            
        gross_value = total_sol * self.live_price
        fee = gross_value * self.taker_fee_pct
        net_value = gross_value - fee
        gross_profit = net_value - total_invested
        
        owner_cut = 0.0
        user_net_profit = gross_profit
        if gross_profit > 0:
            owner_cut = round(gross_profit * 0.10, 4)
            user_net_profit = round(gross_profit - owner_cut, 4)
            
        self.manual_trades_history.insert(0, {
            "orderId": str(uuid.uuid4())[:8],
            "side": "MANUAL_SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(total_sol, 4),
            "fee": round(fee, 4),
            "profit": round(user_net_profit, 4),
            "ownerCut": owner_cut,
            "realizedPnl": round(user_net_profit, 4),
            "execType": "NON_CUSTODIAL_DEX",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        self.wallet_active_positions = []
        print(f">>> [WALLET MANUAL SELL] Sold {round(total_sol, 4)} SOL @ ${round(self.live_price, 2)}. User Net Profit: +${user_net_profit} | Owner 10% Fee: +${owner_cut}")

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

    def execute_sell_individual(self, pos):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        sold_value = sol_amt * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - invested

        if profit < self.min_net_profit_usdt:
            return

        self.usdt_balance += net_return
        self.realized_pnl += profit
        self.sol_balance = max(0.0, self.sol_balance - sol_amt)
        self.invested_amount = max(0.0, self.invested_amount - invested)
        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0

        r_num = pos.get("round", self.active_round)
        if self.round_trades_done.get(r_num, 0) > 0:
            self.round_trades_done[r_num] -= 1
        self.sub_trade_count = len([p for p in self.active_positions if not p.get("isMacro", False) and p["id"] != pos_id])

        self.active_positions = [p for p in self.active_positions if p["id"] != pos_id]

        trade_record = {
            "orderId": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": r_num,
            "execType": "INDIVIDUAL_PROFIT_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        print(f">>> [INDIVIDUAL SELL SUCCESS] Order {pos_id} exited! Profit: +${round(profit, 4)} USDT | Entry: ${pos['entryPrice']} | Exit: ${round(self.live_price, 2)}")

        asyncio.create_task(self.db_save_sell_individual(pos_id, trade_record))

    def get_scavenged_idle_fund(self):
        if self.usdt_balance <= 5.0:
            return 0.0
        total_account = self.usdt_balance + (self.sol_balance * self.live_price)
        scavenged_pool = 0.0
        for r in range(1, 9):
            if r != self.active_round:
                allocated = total_account * self.round_allocations.get(r, 0.0)
                used_ratio = min(1.0, self.round_trades_done.get(r, 0) / 10.0)
                unspent = allocated * (1.0 - used_ratio)
                scavenged_pool += unspent
        return max(0.0, min(self.usdt_balance, scavenged_pool))

    def execute_micro_buy(self):
        idle_fund = self.get_scavenged_idle_fund()
        if idle_fund < 5.0 or self.live_price <= 0:
            return
        m_round = self.active_round
        if self.micro_round_trades_done.get(m_round, 0) >= 10:
            return
        base_alloc = self.round_allocations.get(m_round, 0.01)
        target_size = max(5.0, min(self.usdt_balance, (idle_fund * base_alloc) / 10.0))
        if target_size > self.usdt_balance:
            target_size = self.usdt_balance
        if target_size < 5.0:
            return
        fee = target_size * self.taker_fee_pct
        net_invest = target_size - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance -= target_size
        self.micro_round_trades_done[m_round] = self.micro_round_trades_done.get(m_round, 0) + 1
        pos_id = "M_" + str(uuid.uuid4())[:6]
        pos = {
            "id": pos_id,
            "round": m_round,
            "subTrade": self.micro_round_trades_done[m_round],
            "label": f"MICRO R{m_round} (#{self.micro_round_trades_done[m_round]})",
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(target_size, 2),
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.micro_positions.append(pos)
        self.micro_last_ref_price = self.live_price
        self.micro_tb_active = False
        self.micro_tb_lowest = 0.0
        asyncio.create_task(self.db_sync_state())
        print(f">>> [MICRO SCALP BUY] Active Market Round R{m_round} | Price: ${round(self.live_price, 2)} | Sol: {round(sol_amt, 4)} | Fund: ${round(target_size, 2)} from Idle Pool")

    def execute_micro_sell(self, pos):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if profit <= 0:
            return
        self.usdt_balance += net_return
        self.realized_pnl += profit
        self.micro_realized_pnl += profit
        self.micro_total_trades += 1
        m_round = pos.get("round", 1)
        if self.micro_round_trades_done.get(m_round, 0) > 0:
            self.micro_round_trades_done[m_round] -= 1
        self.micro_positions = [p for p in self.micro_positions if p["id"] != pos_id]
        self.micro_last_ref_price = self.live_price
        trade_record = {
            "orderId": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": m_round,
            "execType": "MICRO_SCALP_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        db_payload = {
            "order_id": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": m_round,
            "exec_type": "MICRO_SCALP_EXIT"
        }
        asyncio.create_task(self.db_save_micro_trade(db_payload))
        print(f">>> [MICRO SCALP PROFIT] Pos: {pos_id} Sold @ ${round(self.live_price, 2)} | Profit: +${round(profit, 4)} USDT")

        if not self.is_paused and len(self.micro_positions) == 0 and self.get_scavenged_idle_fund() >= 5.0:
            print(f">>> [PERPETUAL LOOP] Profit booked! Instantly re-entering runner trade @ ${round(self.live_price, 2)}")
            self.execute_micro_buy()

    def run_micro_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return

        if len(self.micro_positions) == 0 and self.get_scavenged_idle_fund() >= 5.0:
            self.execute_micro_buy()
            return

        if self.micro_last_ref_price <= 0:
            self.micro_last_ref_price = self.live_price

        current_dip = self.micro_last_ref_price - self.live_price
        if current_dip >= 0.30 and len(self.micro_positions) < 10:
            if not self.micro_tb_active:
                self.micro_tb_active = True
                self.micro_tb_lowest = self.live_price
            else:
                if self.live_price < self.micro_tb_lowest:
                    self.micro_tb_lowest = self.live_price
                drop_distance = self.micro_last_ref_price - self.micro_tb_lowest
                if drop_distance >= 1.20:
                    callback = 0.03
                elif drop_distance >= 0.80:
                    callback = 0.02
                else:
                    callback = 0.01
                if self.live_price >= (self.micro_tb_lowest + callback):
                    self.execute_micro_buy()

        for pos in list(self.micro_positions):
            entry_p = pos["entryPrice"]
            if self.live_price > entry_p:
                if "ts_high" not in pos or self.live_price > pos["ts_high"]:
                    pos["ts_high"] = round(self.live_price, 2)
                gain = pos["ts_high"] - entry_p
                if gain >= 0.28:
                    if gain >= 1.20:
                        pullback = 0.03
                    elif gain >= 0.80:
                        pullback = 0.02
                    else:
                        pullback = 0.01
                    if self.live_price <= (pos["ts_high"] - pullback) and (self.live_price - entry_p) >= 0.20:
                        self.execute_micro_sell(pos)
    def get_killer2_idle_fund(self):
        if self.usdt_balance <= 5.0:
            return 0.0
        total_account = self.usdt_balance + ((self.sol_balance + self.macro_vault_sol) * self.live_price)
        scavenged_pool = 0.0
        for r in range(1, 9):
            if r != self.active_round:
                allocated = total_account * self.round_allocations.get(r, 0.0)
                used_ratio = min(1.0, self.round_trades_done.get(r, 0) / 10.0)
                unspent = allocated * (1.0 - used_ratio)
                scavenged_pool += unspent
        return max(0.0, min(self.usdt_balance, scavenged_pool))

    def get_killer2_trade_size(self):
        total_account = self.usdt_balance + ((self.sol_balance + self.macro_vault_sol) * self.live_price)
        base_size = max(100.0, (total_account / 50.0))
        idle_fund = self.get_killer2_idle_fund()
        return min(self.usdt_balance, min(idle_fund, base_size))

    def get_killer2_step_trail(self, mode="BUY"):
        flow = self.whale_orderflow_ratio
        if mode == "BUY":
            if flow <= 40.0:
                return 0.06
            elif flow <= 50.0:
                return 0.05
            else:
                return 0.04
        else:
            if flow >= 60.0:
                return 0.06
            elif flow >= 50.0:
                return 0.05
            else:
                return 0.04

    def execute_killer2_buy(self):
        idle_fund = self.get_killer2_idle_fund()
        if idle_fund < 10.0 or self.live_price <= 0:
            return
        k_round = self.active_round
        if self.killer2_round_trades_done.get(k_round, 0) >= 10:
            return
        target_size = self.get_killer2_trade_size()
        if target_size < 10.0 or target_size > self.usdt_balance:
            return
        fee = target_size * self.taker_fee_pct
        net_invest = target_size - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance -= target_size
        self.killer2_round_trades_done[k_round] = self.killer2_round_trades_done.get(k_round, 0) + 1
        pos_id = "K2_" + str(uuid.uuid4())[:6]
        pos = {
            "id": pos_id,
            "round": k_round,
            "subTrade": self.killer2_round_trades_done[k_round],
            "label": f"KILLER2 R{k_round} (#{self.killer2_round_trades_done[k_round]})",
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(target_size, 2),
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.killer2_positions.append(pos)
        self.killer2_last_ref_price = self.live_price
        self.killer2_tb_active = False
        self.killer2_tb_lowest = 0.0
        asyncio.create_task(self.db_sync_state())

    def execute_killer2_sell(self, pos):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if profit <= 0:
            return
        self.usdt_balance += net_return
        self.realized_pnl += profit
        self.killer2_realized_pnl += profit
        self.killer2_total_trades += 1
        k_round = pos.get("round", 1)
        if self.killer2_round_trades_done.get(k_round, 0) > 0:
            self.killer2_round_trades_done[k_round] -= 1
        self.killer2_positions = [p for p in self.killer2_positions if p["id"] != pos_id]
        self.killer2_last_ref_price = self.live_price
        trade_record = {
            "orderId": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": k_round,
            "execType": "KILLER2_SCALP_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        db_payload = {
            "order_id": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": k_round,
            "exec_type": "KILLER2_SCALP_EXIT"
        }
        asyncio.create_task(self.db_save_micro_trade(db_payload))
        if not self.is_paused and len(self.killer2_positions) == 0 and self.get_killer2_idle_fund() >= 10.0:
            self.execute_killer2_buy()

    def run_killer2_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return
        if len(self.killer2_positions) == 0 and self.get_killer2_idle_fund() >= 10.0:
            self.execute_killer2_buy()
            return
        if self.killer2_last_ref_price <= 0:
            self.killer2_last_ref_price = self.live_price
        current_dip = self.killer2_last_ref_price - self.live_price
        if current_dip >= 0.60 and len(self.killer2_positions) < 10:
            if not self.killer2_tb_active:
                self.killer2_tb_active = True
                self.killer2_tb_lowest = self.live_price
            else:
                if self.live_price < self.killer2_tb_lowest:
                    self.killer2_tb_lowest = self.live_price
                callback = self.get_killer2_step_trail(mode="BUY")
                if self.live_price >= (self.killer2_tb_lowest + callback):
                    self.execute_killer2_buy()
        for pos in list(self.killer2_positions):
            entry_p = pos["entryPrice"]
            if self.live_price > entry_p:
                if "ts_high" not in pos or self.live_price > pos["ts_high"]:
                    pos["ts_high"] = round(self.live_price, 2)
                gain = pos["ts_high"] - entry_p
                if gain >= 0.60:
                    pullback = self.get_killer2_step_trail(mode="SELL")
                    if self.live_price <= (pos["ts_high"] - pullback) and (self.live_price - entry_p) >= 0.45:
                        self.execute_killer2_sell(pos)

    def get_killer3_idle_fund(self):
        if self.usdt_balance <= 5.0:
            return 0.0
        total_account = self.usdt_balance + ((self.sol_balance + self.macro_vault_sol) * self.live_price)
        scavenged_pool = 0.0
        eligible_rounds = [r for r in range(1, 9) if abs(r - self.active_round) >= 2]
        if not eligible_rounds:
            eligible_rounds = [r for r in range(1, 9) if r != self.active_round]
        for r in eligible_rounds:
            allocated = total_account * self.round_allocations.get(r, 0.0)
            used_ratio = min(1.0, self.round_trades_done.get(r, 0) / 10.0)
            unspent = allocated * (1.0 - used_ratio)
            scavenged_pool += unspent
        return max(0.0, min(self.usdt_balance, scavenged_pool))

    def get_killer3_trade_size(self):
        total_account = self.usdt_balance + ((self.sol_balance + self.macro_vault_sol) * self.live_price)
        base_size = max(100.0, (total_account / 50.0))
        idle_fund = self.get_killer3_idle_fund()
        return min(self.usdt_balance, min(idle_fund, base_size))

    def get_killer3_step_trail(self, mode="BUY"):
        flow = self.whale_orderflow_ratio
        if mode == "BUY":
            if flow <= 40.0:
                return 0.09
            elif flow <= 50.0:
                return 0.08
            else:
                return 0.07
        else:
            if flow >= 60.0:
                return 0.09
            elif flow >= 50.0:
                return 0.08
            else:
                return 0.07

    def execute_killer3_buy(self):
        idle_fund = self.get_killer3_idle_fund()
        if idle_fund < 10.0 or self.live_price <= 0:
            return
        k_round = self.active_round
        if self.killer3_round_trades_done.get(k_round, 0) >= 10:
            return
        target_size = self.get_killer3_trade_size()
        if target_size < 10.0 or target_size > self.usdt_balance:
            return
        fee = target_size * self.taker_fee_pct
        net_invest = target_size - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance -= target_size
        self.killer3_round_trades_done[k_round] = self.killer3_round_trades_done.get(k_round, 0) + 1
        pos_id = "K3_" + str(uuid.uuid4())[:6]
        pos = {
            "id": pos_id,
            "round": k_round,
            "subTrade": self.killer3_round_trades_done[k_round],
            "label": f"KILLER3 R{k_round} (#{self.killer3_round_trades_done[k_round]})",
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(target_size, 2),
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.killer3_positions.append(pos)
        self.killer3_last_ref_price = self.live_price
        self.killer3_tb_active = False
        self.killer3_tb_lowest = 0.0
        asyncio.create_task(self.db_sync_state())

    def execute_killer3_sell(self, pos):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if profit <= 0:
            return
        self.usdt_balance += net_return
        self.realized_pnl += profit
        self.killer3_realized_pnl += profit
        self.killer3_total_trades += 1
        k_round = pos.get("round", 1)
        if self.killer3_round_trades_done.get(k_round, 0) > 0:
            self.killer3_round_trades_done[k_round] -= 1
        self.killer3_positions = [p for p in self.killer3_positions if p["id"] != pos_id]
        self.killer3_last_ref_price = self.live_price
        trade_record = {
            "orderId": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": k_round,
            "execType": "KILLER3_SCALP_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        db_payload = {
            "order_id": pos_id,
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": k_round,
            "exec_type": "KILLER3_SCALP_EXIT"
        }
        asyncio.create_task(self.db_save_micro_trade(db_payload))
        if not self.is_paused and len(self.killer3_positions) == 0 and self.get_killer3_idle_fund() >= 10.0:
            self.execute_killer3_buy()

    def run_killer3_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return
        if len(self.killer3_positions) == 0 and self.get_killer3_idle_fund() >= 10.0:
            self.execute_killer3_buy()
            return
        if self.killer3_last_ref_price <= 0:
            self.killer3_last_ref_price = self.live_price
        current_dip = self.killer3_last_ref_price - self.live_price
        if current_dip >= 0.90 and len(self.killer3_positions) < 10:
            if not self.killer3_tb_active:
                self.killer3_tb_active = True
                self.killer3_tb_lowest = self.live_price
            else:
                if self.live_price < self.killer3_tb_lowest:
                    self.killer3_tb_lowest = self.live_price
                callback = self.get_killer3_step_trail(mode="BUY")
                if self.live_price >= (self.killer3_tb_lowest + callback):
                    self.execute_killer3_buy()
        for pos in list(self.killer3_positions):
            entry_p = pos["entryPrice"]
            if self.live_price > entry_p:
                if "ts_high" not in pos or self.live_price > pos["ts_high"]:
                    pos["ts_high"] = round(self.live_price, 2)
                gain = pos["ts_high"] - entry_p
                if gain >= 0.90:
                    pullback = self.get_killer3_step_trail(mode="SELL")
                    if self.live_price <= (pos["ts_high"] - pullback) and (self.live_price - entry_p) >= 0.70:
                        self.execute_killer3_sell(pos)

    def run_harvester_infinity_tick(self):
        if self.is_paused or self.live_price <= 0:
            return
        total_account = self.usdt_balance + ((self.sol_balance + self.macro_vault_sol) * self.live_price)

        if not self.harvester_active:
            if self.active_round in [6, 7, 8] and self.live_price < 240.0:
                r8_total_alloc = total_account * self.round_allocations.get(8, 0.27)
                borrow_budget = max(50.0, min(self.usdt_balance, r8_total_alloc))
                if borrow_budget >= 50.0:
                    half_budget = borrow_budget / 2.0
                    fee = half_budget * self.taker_fee_pct
                    sol_bought = (half_budget - fee) / self.live_price
                    self.usdt_balance -= half_budget
                    self.harvester_borrowed_r8 = borrow_budget
                    self.harvester_vault_invested = half_budget
                    self.harvester_vault_cash = half_budget
                    self.harvester_vault_sol = sol_bought
                    self.harvester_last_action_price = self.live_price
                    self.harvester_active = True
                    self.harvester_status = "50/50 RUNNING"
                    pos_id = "HRV_INIT_" + str(uuid.uuid4())[:4]
                    t_record = {
                        "orderId": pos_id,
                        "side": "BUY",
                        "price": round(self.live_price, 2),
                        "solAmount": round(sol_bought, 4),
                        "fee": round(fee, 4),
                        "profit": 0.0,
                        "round": self.active_round,
                        "execType": "HARVESTER_VAULT_INIT",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.trades_history.insert(0, t_record)
                    asyncio.create_task(self.db_sync_state())
            return

        if self.live_price >= 250.0 and self.harvester_vault_sol > 0:
            gross_val = self.harvester_vault_sol * self.live_price
            fee = gross_val * self.taker_fee_pct
            net_return = gross_val - fee
            profit = (net_return + self.harvester_vault_cash) - self.harvester_borrowed_r8
            self.usdt_balance += net_return
            if profit > 0:
                self.realized_pnl += profit
                self.harvester_realized_pnl += profit
            self.harvester_cycle_count += 1
            self.harvester_active = False
            self.harvester_vault_sol = 0.0
            self.harvester_vault_invested = 0.0
            self.harvester_vault_cash = 0.0
            self.harvester_borrowed_r8 = 0.0
            self.harvester_status = "ATH HARVESTED ($250) - WAITING R6-R8"
            t_record = {
                "orderId": "HRV_ATH_" + str(uuid.uuid4())[:4],
                "side": "SELL",
                "price": round(self.live_price, 2),
                "solAmount": round(self.harvester_vault_sol, 4),
                "fee": round(fee, 4),
                "profit": round(profit, 4),
                "realizedPnl": round(profit, 4),
                "round": 1,
                "execType": "HARVESTER_GRAND_ATH_EXIT",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.trades_history.insert(0, t_record)
            asyncio.create_task(self.db_save_micro_trade({
                "order_id": t_record["orderId"],
                "side": "SELL",
                "price": t_record["price"],
                "sol_amount": t_record["solAmount"],
                "fee": t_record["fee"],
                "profit": t_record["profit"],
                "round": 1,
                "exec_type": "HARVESTER_GRAND_ATH_EXIT"
            }))
            return

        if self.harvester_last_action_price <= 0:
            self.harvester_last_action_price = self.live_price
        price_diff = self.live_price - self.harvester_last_action_price

        if price_diff >= 0.80 and self.harvester_vault_sol > 0.05:
            portion_sol = self.harvester_vault_sol * 0.10
            gross_val = portion_sol * self.live_price
            fee = gross_val * self.taker_fee_pct
            net_val = gross_val - fee
            cost = portion_sol * (self.harvester_vault_invested / self.harvester_vault_sol)
            profit = net_val - cost
            self.harvester_vault_sol -= portion_sol
            self.harvester_vault_invested = max(0.0, self.harvester_vault_invested - cost)
            self.harvester_vault_cash += net_val
            if profit > 0:
                self.realized_pnl += profit
                self.harvester_realized_pnl += profit
            self.harvester_last_action_price = self.live_price
            self.harvester_status = f"SWING SELL (+${round(profit,2)})"
            t_record = {
                "orderId": "HRV_S_" + str(uuid.uuid4())[:4],
                "side": "SELL",
                "price": round(self.live_price, 2),
                "solAmount": round(portion_sol, 4),
                "fee": round(fee, 4),
                "profit": round(profit, 4),
                "realizedPnl": round(profit, 4),
                "round": self.active_round,
                "execType": "HARVESTER_SWING_EXIT",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.trades_history.insert(0, t_record)
            asyncio.create_task(self.db_save_micro_trade({
                "order_id": t_record["orderId"],
                "side": "SELL",
                "price": t_record["price"],
                "sol_amount": t_record["solAmount"],
                "fee": t_record["fee"],
                "profit": t_record["profit"],
                "round": self.active_round,
                "exec_type": "HARVESTER_SWING_EXIT"
            }))

        elif price_diff <= -0.80 and self.harvester_vault_cash >= 15.0:
            reinvest_size = min(self.harvester_vault_cash, self.harvester_borrowed_r8 * 0.10)
            if reinvest_size >= 10.0:
                fee = reinvest_size * self.taker_fee_pct
                sol_bought = (reinvest_size - fee) / self.live_price
                self.harvester_vault_cash -= reinvest_size
                self.harvester_vault_invested += reinvest_size
                self.harvester_vault_sol += sol_bought
                self.harvester_last_action_price = self.live_price
                self.harvester_status = "REBUY RE-BALANCE"
                t_record = {
                    "orderId": "HRV_B_" + str(uuid.uuid4())[:4],
                    "side": "BUY",
                    "price": round(self.live_price, 2),
                    "solAmount": round(sol_bought, 4),
                    "fee": round(fee, 4),
                    "profit": 0.0,
                    "round": self.active_round,
                    "execType": "HARVESTER_SWING_BUY",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                self.trades_history.insert(0, t_record)
                asyncio.create_task(self.db_sync_state())

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

        self.sync_phase_and_round()

        

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]
        if self.cooldown_remaining > 0:
            self.latest_signal = {
                "action": "COOLDOWN",
                "price": round(self.live_price, 2),
                "text": f"COOLING DOWN ({self.cooldown_remaining}s) - Securing Realized Profits"
            }
        elif len(regular_positions) == 0:
            if self.whale_sentiment == "BULLISH":
                self.latest_signal = {
                    "action": "BUY",
                    "price": round(self.live_price, 2),
                    "text": f"BUY SOL NOW @ ${round(self.live_price, 2)} (Whale Inflow: {self.whale_orderflow_ratio}%)"
                }
            elif self.whale_sentiment == "BEARISH":
                self.latest_signal = {
                    "action": "WAIT",
                    "price": round(self.live_price, 2),
                    "text": f"WAIT / DO NOT BUY @ ${round(self.live_price, 2)} (Heavy Whale Selling Pressure)"
                }
            else:
                self.latest_signal = {
                    "action": "HOLD",
                    "price": round(self.live_price, 2),
                    "text": f"SCANNING MARKET @ ${round(self.live_price, 2)} (Orderflow Neutral)"
                }
        else:
            current_net = (self.sol_balance * self.live_price * (1 - self.taker_fee_pct)) - self.invested_amount
            if current_net >= self.min_net_profit_usdt:
                if self.ts_low > 0 and self.live_price <= (self.ts_low + 0.15):
                    self.latest_signal = {
                        "action": "SELL",
                        "price": round(self.live_price, 2),
                        "text": f"SELL / TAKE PROFIT NOW @ ${round(self.live_price, 2)} (+${round(current_net, 2)} USDT Secured)"
                    }
                elif self.whale_sentiment == "BULLISH":
                    self.latest_signal = {
                        "action": "HOLD",
                        "price": round(self.live_price, 2),
                        "text": f"HOLD / RIDE TREND @ ${round(self.live_price, 2)} (+${round(current_net, 2)} USDT, Whales Buying)"
                    }
                else:
                    self.latest_signal = {
                        "action": "SELL",
                        "price": round(self.live_price, 2),
                        "text": f"TAKE PROFIT READY @ ${round(self.live_price, 2)} (Trailing Floor Active: ${round(self.ts_low, 2)})"
                    }
            else:
                if self.whale_sentiment == "BEARISH":
                    self.latest_signal = {
                        "action": "HOLD",
                        "price": round(self.live_price, 2),
                        "text": f"HOLDING DIP @ ${round(self.live_price, 2)} (Whale Volume Low, Trailing Buy Armed)"
                    }
                else:
                    self.latest_signal = {
                        "action": "HOLD",
                        "price": round(self.live_price, 2),
                        "text": f"HOLDING SOL @ ${round(self.live_price, 2)} (Avg Entry: ${round(self.avg_entry_price, 2)}, Whales Re-accumulating)"
                    }

        self.run_micro_scalper_tick()
        self.run_killer2_scalper_tick()
        self.run_killer3_scalper_tick()
        self.run_harvester_infinity_tick()

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            return

        if self.is_paused:
            return

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]

        if len(regular_positions) == 0:
            if self.whale_sentiment != "BEARISH" and self.round_trades_done.get(self.active_round, 0) < 10:
                self.execute_buy(is_sub_trade=False, escalate_round=False)
            return

        last_entry = regular_positions[-1]["entryPrice"]
        current_dip = last_entry - self.live_price

        if current_dip < 0.45:
            self.tb_active = False
            self.tb_stage = "IDLE"
        else:
            if not self.tb_active and current_dip >= 0.60:
                self.tb_active = True
                self.tb_lowest_price = self.live_price

            if self.tb_active:
                if self.live_price < self.tb_lowest_price:
                    self.tb_lowest_price = self.live_price

                total_drop = last_entry - self.tb_lowest_price

                if total_drop >= 1.20:
                    self.tb_stage = "1.20$"
                    required_bounce = 0.35
                elif total_drop >= 0.90:
                    self.tb_stage = "0.90$"
                    required_bounce = 0.25
                else:
                    self.tb_stage = "0.60$"
                    required_bounce = 0.15

                if self.whale_orderflow_ratio >= 65.0:
                    required_bounce = max(0.10, round(required_bounce - 0.05, 2))

                if self.live_price >= (self.tb_lowest_price + required_bounce):
                    self.tb_active = False
                    self.tb_stage = "IDLE"
                    active_count = len([p for p in regular_positions if p.get("round") == self.active_round])
                    if active_count < 10:
                        self.execute_buy(is_sub_trade=True)
                        return
        if self.macro_vault_sol > 0 and self.live_price >= self.macro_target_price:
            if self.live_price > self.macro_ts_high:
                self.macro_ts_high = round(self.live_price, 2)

            calculated_macro_stop = round(self.macro_ts_high * 0.99, 2)
            if calculated_macro_stop > self.macro_ts_low:
                self.macro_ts_low = calculated_macro_stop

            if self.live_price <= self.macro_ts_low:
                self.execute_macro_sell()

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]
        for pos in list(regular_positions):
            entry_p = pos["entryPrice"]
            if self.live_price > entry_p:
                if "ts_high" not in pos or self.live_price > pos["ts_high"]:
                    pos["ts_high"] = round(self.live_price, 2)

                peak_gain = pos["ts_high"] - entry_p
                projected_p = (pos["solAmount"] * self.live_price * (1 - self.taker_fee_pct)) - pos["invested"]

                if projected_p >= self.min_net_profit_usdt:
                    trail_gap = 0.15 if peak_gain >= 0.60 else 0.10
                    calc_stop = round(pos["ts_high"] - trail_gap, 2)
                    if "ts_low" not in pos or calc_stop > pos["ts_low"]:
                        pos["ts_low"] = calc_stop

                    if pos.get("ts_low", 0) > 0 and self.live_price <= pos["ts_low"]:
                        self.execute_sell_individual(pos)
                        break
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
    ws_url = "wss://stream.binance.com:9443/ws/solusdt@trade"
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(ws_url) as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            price = float(data.get("p", 0.0))
                            if price > 0:
                                bot.process_market_trades([data])
                                bot.update_price_tick(price)
                                await manager.broadcast(json.dumps(bot.get_state()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
        except Exception:
            await asyncio.sleep(2)
async def price_feed_fallback_worker():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT", timeout=3) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            p = float(data.get("price", 0.0))
                            if p > 0:
                                bot.update_price_tick(p)
                                await manager.broadcast(json.dumps(bot.get_state()))
                                await asyncio.sleep(2)
                                continue
                except Exception:
                    pass
                try:
                    async with session.get("https://api.coinbase.com/v2/prices/SOL-USD/spot", timeout=3) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            p = float(data.get("data", {}).get("amount", 0.0))
                            if p > 0:
                                bot.update_price_tick(p)
                                await manager.broadcast(json.dumps(bot.get_state()))
                except Exception:
                    pass
        except Exception:
            pass
        await asyncio.sleep(2)
@app.on_event("startup")
async def startup_event():
    await bot.load_from_database()
    asyncio.create_task(binance_ws_worker())
    asyncio.create_task(price_feed_fallback_worker())

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
