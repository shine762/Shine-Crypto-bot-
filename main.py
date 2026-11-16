import asyncio
import json
import uuid
import os
from datetime import datetime, timezone, timedelta
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
    "Prefer": "resolution=merge-duplicates"
}

class UltraQuantSpotBot:
    def __init__(self):
        self.is_paused = False
        self.live_price = 0.0
        self.usdt_balance = 0.0
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
        self.max_sub_trades = 24
        self.round_trades_done = {r: 0 for r in range(1, 11)}
        self.realized_pnl = 0.0
        self.cooldown_remaining = 0
        self.active_positions = []
        self.trades_history = []
        self.spot_trades_history = []
        self.micro_trades_history = []
        self.killer2_trades_history = []
        self.killer3_trades_history = []
        self.hyper_trades_history = []
        self.singularity_trades_history = []
        self.scalp_trades_history = []
        self.manual_trades_history = []
        self.price_history = []
        self.latest_signal = {"action": "HOLD", "price": 0.0, "text": "Scanning market for high-probability signals..."}
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
        self.whale_boost_multiplier = 1.0
        self.whale_dump_alert = False
        self.cvd_net_volume = 0.0
        self.taker_fee_pct = 0.001
        self.min_net_profit_usdt = 0.02
        self.solana_dex_mode = "PANCAKESWAP_BSC_TESTNET"
        self.bsc_usdt_address = "0xEC09EBf252cc6d0FE4DaCAF8CeC5F7A66b0aaf12"
        self.shine_vault_address = "0x204e8c521aCa3621DB585829667759433aBb70d3"
        self.shine_core_address = "0xEEe011D9d6Cb0C5A382C5baffE8E05c384631159"
        self.root_owner_address = "0x99b23c8039e98a119eaed74e4f3fe5d68ff1abba"
        self.bsc_pancake_router = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
        self.dex_last_quote_price = 0.0
        self.round8_hold_pct = 0.07
        self.round8_trade_pct = 0.20
        self.round8_hold_sol = 0.0
        self.round8_hold_invested = 0.0
        self.round8_hold_usdt = 0.0
        self.round_allocations = {
            1: 0.01, 2: 0.02, 3: 0.04, 4: 0.06, 5: 0.10,
            6: 0.20, 7: 0.30, 8: 0.27, 9: 0.0, 10: 0.0
        }
        self.home_pool_users = 1
        self.home_round_spent = {r: 0.0 for r in range(1, 11)}
        self.home_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.macro_profit_vault = 0.0
        self.hyper_pool_active = True
        self.hyper_pool_users = 1
        self.hyper_pool_balance = 0.0
        self.hyper_user_investment = 0.0
        self.hyper_trade_size = 10.0
        self.hyper_positions = []
        self.hyper_round_trades_done = {r: 0 for r in range(1, 11)}
        self.hyper_round_spent = {r: 0.0 for r in range(1, 11)}
        self.hyper_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.hyper_macro_profit_vault = 0.0
        self.singularity_macro_profit_vault = 0.0
        self.hyper_tb_active = False
        self.hyper_tb_lowest = 0.0
        self.hyper_last_ref_price = 0.0
        self.hyper_realized_pnl = 0.0
        self.hyper_total_trades = 0
        self.micro_pool_users = 1
        self.micro_positions = []
        self.micro_round_trades_done = {r: 0 for r in range(1, 11)}
        self.micro_round_spent = {r: 0.0 for r in range(1, 11)}
        self.micro_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.micro_macro_profit_vault = 0.0
        self.micro_tb_active = False
        self.micro_tb_lowest = 0.0
        self.micro_last_ref_price = 0.0
        self.micro_realized_pnl = 0.0
        self.micro_total_trades = 0
        self.killer2_pool_users = 1
        self.killer2_positions = []
        self.killer2_round_trades_done = {r: 0 for r in range(1, 11)}
        self.killer2_round_spent = {r: 0.0 for r in range(1, 11)}
        self.killer2_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.killer2_macro_profit_vault = 0.0
        self.killer2_tb_active = False
        self.killer2_tb_lowest = 0.0
        self.killer2_last_ref_price = 0.0
        self.killer2_realized_pnl = 0.0
        self.killer2_total_trades = 0
        self.killer3_pool_users = 1
        self.killer3_positions = []
        self.killer3_round_trades_done = {r: 0 for r in range(1, 11)}
        self.killer3_round_spent = {r: 0.0 for r in range(1, 11)}
        self.killer3_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.killer3_macro_profit_vault = 0.0
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
        self.manual_test_balance = 100.0
        self.manual_realized_pnl = 0.0
        self.wallet_active_positions = []
        self.wallet_open_orders = []
        self.auto_loops = []
        self.spot_realized_pnl = 0.0
        self.db_loaded = False
        self.total_user_capital = 0.0
        self.singularity_active = True
        self.singularity_users = 1
        self.singularity_pool_balance = 0.0
        self.singularity_user_investment = 0.0
        self.singularity_positions = []
        self.singularity_round_trades_done = {r: 0 for r in range(1, 11)}
        self.singularity_realized_pnl = 0.0
        self.singularity_total_trades = 0
        self.singularity_macro_sol = 0.0
        self.singularity_macro_invested = 0.0
        self.singularity_macro_target = 0.0
        self.singularity_macro_ts_high = 0.0
        self.singularity_macro_ts_low = 0.0
        self.singularity_round_spent = {r: 0.0 for r in range(1, 11)}
        self.singularity_round_borrowed = {r: 0.0 for r in range(1, 11)}
        self.singularity_tb_active = False
        self.singularity_tb_lowest = 0.0
        self.singularity_last_ref_price = 0.0
        self.owner_real_capital = 0.0
        self.showcase_capital = 80000.0
        self.showcase_usdt = 80000.0
        self.showcase_positions = []
        self.showcase_trades_history = []
        self.showcase_realized_pnl = 0.0
        self.showcase_ts_high = 0.0
        self.showcase_ts_low = 0.0
        self.showcase_tb_active = False
        self.showcase_tb_lowest = 0.0
        self.showcase_macro_sol = 0.0
        self.showcase_macro_invested = 0.0
        self.showcase_macro_target = 0.0
        self.showcase_macro_ts_high = 0.0
        self.showcase_macro_ts_low = 0.0
        self.showcase_round_spent = {r: 0.0 for r in range(1, 11)}
        self.showcase_round_borrowed = {r: 0.0 for r in range(1, 11)}

    def verify_user_slot_onchain(self, wallet_addr, prog_code="V1", level_num=1):
        if not w3_deploy or not wallet_addr:
            return True
        prog_map = {"V1": 1, "Q2": 2, "T3": 3, "S4": 4, "G5": 5, "N6": 6, "A7": 7, "C8": 8, "S9": 9, "Q10": 10}
        p_idx = prog_map.get(str(prog_code).upper(), 1)
        l_idx = max(0, int(level_num) - 1)
        try:
            abi = [{"inputs": [{"internalType": "address", "name": "_user", "type": "address"}, {"internalType": "uint8", "name": "_program", "type": "uint8"}, {"internalType": "uint8", "name": "_level", "type": "uint8"}], "name": "isUserLevelActive", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}]
            contract = w3_deploy.eth.contract(address=Web3.to_checksum_address(self.shine_core_address), abi=abi)
            return bool(contract.functions.isUserLevelActive(Web3.to_checksum_address(wallet_addr), p_idx, l_idx).call())
        except Exception:
            return True

    async def db_save_showcase_state(self):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                state_row = {
                    "id": "ID1_STATE",
                    "round": 0,
                    "sub_trade": 0,
                    "label": "ID1_STATE",
                    "entry_price": round(self.showcase_capital, 2),
                    "sol_amount": round(self.showcase_macro_sol, 4),
                    "invested": round(self.showcase_realized_pnl, 4),
                    "is_macro": False,
                    "target_price": round(self.showcase_macro_target, 2)
                }
                await session.post(f"{SUPABASE_URL}/rest/v1/active_positions?on_conflict=id", json=state_row)
        except Exception:
            pass

    def execute_showcase_buy(self, cur_rnd, trade_amt, borrowed_donor=0, is_macro=False):
        cur_p = float(self.live_price)
        if cur_p <= 0 or trade_amt < 10.0 or self.showcase_usdt < trade_amt:
            return
        fee = trade_amt * self.taker_fee_pct
        sol_qty = (trade_amt - fee) / cur_p
        self.showcase_usdt = round(self.showcase_usdt - trade_amt, 2)
        p_id = "ID1_" + str(uuid.uuid4())[:6]
        if is_macro:
            lbl = "ID1 R8 HOLD VAULT"
            self.showcase_macro_sol = round(self.showcase_macro_sol + sol_qty, 4)
            self.showcase_macro_invested = round(self.showcase_macro_invested + trade_amt, 2)
            m_entry = self.showcase_macro_invested / self.showcase_macro_sol if self.showcase_macro_sol > 0 else cur_p
            self.showcase_macro_target = round(max(200.0, m_entry * 2.0), 2)
            t_price = self.showcase_macro_target
        elif borrowed_donor > 0:
            lbl = f"R{cur_rnd} (LOAN R{borrowed_donor} #{len(self.showcase_positions) + 1})"
            t_price = round(cur_p + 0.40, 2)
        else:
            lbl = f"R{cur_rnd} (ID1 #{len(self.showcase_positions) + 1})"
            t_price = round(cur_p + 0.40, 2)
        pos = {
            "id": p_id,
            "round": cur_rnd,
            "subTrade": len(self.showcase_positions) + 1,
            "label": lbl,
            "entryPrice": round(cur_p, 2),
            "solAmount": round(sol_qty, 4),
            "invested": round(trade_amt, 2),
            "isMacro": is_macro,
            "borrowedFrom": borrowed_donor,
            "targetPrice": t_price,
            "ts_high": round(cur_p, 2),
            "ts_low": 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.showcase_positions.append(pos)
        t_rec = {
            "orderId": p_id + "_B",
            "side": "BUY",
            "price": round(cur_p, 2),
            "solAmount": round(sol_qty, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": cur_rnd,
            "execType": "ID1_SHOWCASE_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.showcase_trades_history.insert(0, t_rec)
        self.showcase_trades_history = self.showcase_trades_history[:200]
        self.showcase_ts_high = round(cur_p, 2)
        self.showcase_ts_low = 0.0
        asyncio.create_task(self.db_save_buy(pos, t_rec))
        asyncio.create_task(self.db_save_showcase_state())

    def execute_showcase_sell(self, pos, force=False):
        cur_p = float(self.live_price)
        if cur_p <= 0:
            return
        sol_amt = float(pos["solAmount"])
        inv = float(pos["invested"])
        gross = sol_amt * cur_p
        fee = gross * self.taker_fee_pct
        net_ret = gross - fee
        profit = round(net_ret - inv, 4)
        if not force and profit < self.min_net_profit_usdt:
            return
        r_num = pos.get("round", 1)
        b_donor = pos.get("borrowedFrom", 0)
        if b_donor > 0:
            self.showcase_round_spent[b_donor] = max(0.0, round(self.showcase_round_spent.get(b_donor, 0.0) - inv, 2))
            self.showcase_round_borrowed[r_num] = max(0.0, round(self.showcase_round_borrowed.get(r_num, 0.0) - inv, 2))
        else:
            self.showcase_round_spent[r_num] = max(0.0, round(self.showcase_round_spent.get(r_num, 0.0) - inv, 2))
        if pos.get("isMacro", False):
            self.showcase_macro_sol = max(0.0, round(self.showcase_macro_sol - sol_amt, 4))
            self.showcase_macro_invested = max(0.0, round(self.showcase_macro_invested - inv, 2))
        self.showcase_usdt = round(self.showcase_usdt + net_ret, 2)
        self.showcase_realized_pnl = round(self.showcase_realized_pnl + profit, 4)
        if pos in self.showcase_positions:
            self.showcase_positions.remove(pos)
        t_rec = {
            "orderId": pos["id"] + "_S",
            "side": "SELL",
            "price": round(cur_p, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": profit,
            "realizedPnl": profit,
            "round": r_num,
            "execType": "ID1_SHOWCASE_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.showcase_trades_history.insert(0, t_rec)
        self.showcase_trades_history = self.showcase_trades_history[:200]
        asyncio.create_task(self.db_save_sell_individual(pos["id"], t_rec))
        asyncio.create_task(self.db_save_showcase_state())

    def run_showcase_tick(self):
        if self.live_price <= 0 or not getattr(self, "db_loaded", False):
            return
        cur_p = float(self.live_price)
        self.sync_phase_and_round()
        cur_rnd = self.active_round
        if cur_rnd in [9, 10]:
            return

        for r_chk in [8, 7, 6, 5]:
            r_top = self.get_round_top_price(r_chk)
            if cur_p >= (r_top - 1.0) or cur_rnd < r_chk:
                for p in list(self.showcase_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_showcase_sell(p)
                if r_chk == 8:
                    for p in list(self.showcase_positions):
                        if p.get("round") == 8 and p.get("borrowedFrom", 0) == 0 and not p.get("isMacro", False):
                            p["isMacro"] = True
                            p["label"] = "ID1 R8 HOLD VAULT"
                            self.showcase_macro_sol = round(self.showcase_macro_sol + float(p["solAmount"]), 4)
                            self.showcase_macro_invested = round(self.showcase_macro_invested + float(p["invested"]), 2)
                            m_ent = self.showcase_macro_invested / self.showcase_macro_sol if self.showcase_macro_sol > 0 else cur_p
                            self.showcase_macro_target = round(max(200.0, m_ent * 2.0), 2)
                            p["targetPrice"] = self.showcase_macro_target
                            asyncio.create_task(self.db_save_buy(p, {
                                "order_id": p["id"] + "_HOLD",
                                "side": "HOLD",
                                "price": round(cur_p, 2),
                                "sol_amount": 0.0,
                                "fee": 0.0,
                                "profit": 0.0,
                                "round": 8,
                                "exec_type": "ID1_SHOWCASE_HOLD"
                            }))
                    r8_own_max = round(self.round_allocations.get(8, 0.27) * self.showcase_capital, 2)
                    r8_own_active = sum(float(p["invested"]) for p in self.showcase_positions if p.get("round") == 8 and p.get("borrowedFrom", 0) == 0)
                    r8_own_rem = round(r8_own_max - r8_own_active, 2)
                    if r8_own_rem >= 100.0 and self.showcase_usdt >= 100.0:
                        buy_amt = min(self.showcase_usdt, r8_own_rem)
                        self.showcase_round_spent[8] = round(self.showcase_round_spent.get(8, 0.0) + buy_amt, 2)
                        self.execute_showcase_buy(8, buy_amt, borrowed_donor=0, is_macro=True)

        if self.showcase_macro_sol > 0 and self.showcase_macro_target > 0 and cur_p >= self.showcase_macro_target:
            if cur_p > self.showcase_macro_ts_high:
                self.showcase_macro_ts_high = round(cur_p, 2)
            calc_m_stop = round(self.showcase_macro_ts_high * 0.99, 2)
            if calc_m_stop > self.showcase_macro_ts_low:
                self.showcase_macro_ts_low = calc_m_stop
            if cur_p <= self.showcase_macro_ts_low:
                for p in list(self.showcase_positions):
                    if p.get("isMacro", False):
                        self.execute_showcase_sell(p)

        reg_showcase = [p for p in self.showcase_positions if not p.get("isMacro", False)]
        if len(reg_showcase) == 0:
            trade_amt = 400.0
            if self.showcase_usdt >= trade_amt:
                allowed, b_donor = self.allocate_round_budget(self.showcase_round_spent, self.showcase_round_borrowed, cur_rnd, trade_amt, self.showcase_capital)
                if allowed:
                    self.execute_showcase_buy(cur_rnd, trade_amt, borrowed_donor=b_donor, is_macro=False)
            return

        for pos in list(reg_showcase):
            ent = float(pos["entryPrice"])
            if cur_p > ent:
                if cur_p > float(pos.get("ts_high", ent)):
                    pos["ts_high"] = round(cur_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - ent
                pullback = 0.20 if gain >= 1.50 else (0.15 if gain >= 0.80 else (0.10 if gain >= 0.40 else 0.0))
                if pullback > 0.0:
                    stop_lvl = max(round(ent + 0.15, 2), round(peak - pullback, 2))
                    if stop_lvl > float(pos.get("ts_low", 0.0)):
                        pos["ts_low"] = stop_lvl
                        self.showcase_ts_high = peak
                        self.showcase_ts_low = stop_lvl
                    if cur_p <= pos["ts_low"]:
                        self.execute_showcase_sell(pos)
                        return

        last_ent = float(reg_showcase[-1]["entryPrice"])
        if (last_ent - cur_p) >= 1.20 and len(reg_showcase) < 24 and self.showcase_usdt >= 400.0:
            if not self.showcase_tb_active:
                self.showcase_tb_active = True
                self.showcase_tb_lowest = cur_p
            else:
                if cur_p < self.showcase_tb_lowest:
                    self.showcase_tb_lowest = cur_p
                if cur_p >= (self.showcase_tb_lowest * 1.0025):
                    self.showcase_tb_active = False
                    self.showcase_tb_lowest = 0.0
                    trade_amt = 400.0
                    allowed, b_donor = self.allocate_round_budget(self.showcase_round_spent, self.showcase_round_borrowed, cur_rnd, trade_amt, self.showcase_capital)
                    if allowed:
                        self.execute_showcase_buy(cur_rnd, trade_amt, borrowed_donor=b_donor, is_macro=False)
        else:
            self.showcase_tb_active = False

    def get_showcase_state(self):
        s_sol = sum(float(p.get("solAmount", 0.0)) for p in self.showcase_positions)
        s_inv = sum(float(p.get("invested", 0.0)) for p in self.showcase_positions)
        s_avg = round(s_inv / s_sol, 2) if s_sol > 0 else 0.0
        s_unreal = round((s_sol * self.live_price) - s_inv, 2) if s_sol > 0 and self.live_price > 0 else 0.0
        s_pct = round((s_unreal / s_inv) * 100.0, 2) if s_inv > 0 else 0.0
        return {
            "mode": "REAL" if self.owner_real_capital > 0 else "SHOWCASE",
            "totalCapital": round(self.showcase_usdt + s_inv, 2),
            "usdtBalance": round(self.showcase_usdt, 2),
            "solBalance": round(s_sol, 4),
            "investedAmount": round(s_inv, 2),
            "avgEntryPrice": s_avg,
            "pnl": s_unreal,
            "pnlPct": s_pct,
            "realizedPnl": round(self.showcase_realized_pnl, 4),
            "macroSol": round(self.showcase_macro_sol, 4),
            "macroInvested": round(self.showcase_macro_invested, 2),
            "tsHigh": round(self.showcase_ts_high, 2),
            "tsLow": round(self.showcase_ts_low, 2),
            "activePositions": self.showcase_positions,
            "tradesHistory": self.showcase_trades_history
        }

    def get_tier_config(self, capital=None):
        cap = capital if capital is not None else self.total_user_capital
        net_fund = cap
        if net_fund <= 300.0:
            trade_size = 10.0
        else:
            trade_size = round(net_fund / 24.0, 2)
        return {"slots": 24, "size": max(10.0, trade_size), "net_fund": net_fund}

    def check_and_trigger_fund_tiers(self):
        if self.is_paused or self.live_price <= 0:
            return
        fund = self.total_user_capital
        if fund >= 10.0 and len(self.micro_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_micro_buy()
        if fund >= 40.0 and len(self.active_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_buy(is_sub_trade=False)
        if fund >= 60.0 and len(self.killer2_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_killer2_buy()
        if fund >= 80.0 and len(self.killer3_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_killer3_buy()
        if fund >= 500.0 and len(self.hyper_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_hyper_buy()
        if fund >= 1000.0 and len(self.singularity_positions) == 0 and self.usdt_balance >= 10.0:
            self.execute_singularity_buy()

    def get_hyper_slots(self, cap=None):
        return 24

    def get_singularity_tier_config(self, cap=None, target_round=None):
        cfg = self.get_tier_config(cap)
        return {"slots": 24, "trade_size": cfg["size"], "round_fund": cfg["net_fund"]}

    async def fetch_real_vault_capital_from_slots(self, session):
        root_owner_lower = "0x99b23c8039e98a119eaed74e4f3fe5d68ff1abba"
        try:
            async with session.get(f"{SUPABASE_URL}/rest/v1/user_activated_slots?select=wallet_address,program,level,cost") as s_resp:
                if s_resp.status == 200:
                    slot_rows = await s_resp.json()
                    if isinstance(slot_rows, list):
                        unique_slots = {}
                        for s in slot_rows:
                            w_addr = str(s.get("wallet_address") or "").lower().strip()
                            if not w_addr or w_addr == root_owner_lower:
                                continue
                            s_key = f"{w_addr}_{s.get('program')}_{s.get('level')}"
                            unique_slots[s_key] = float(s.get("cost") or 0.0)
                        total_slot_cost = sum(unique_slots.values())
                        return round(total_slot_cost * 0.80, 2)
        except Exception:
            pass
        return None

    async def load_from_database(self):
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                real_slots_cap = await self.fetch_real_vault_capital_from_slots(session)
                async with session.get(f"{SUPABASE_URL}/rest/v1/bot_state?id=eq.1") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data and len(data) > 0:
                            row = data[0]
                            self.realized_pnl = float(row.get("realized_pnl", 0.0))
                            if "spot_realized_pnl" in row and row.get("spot_realized_pnl") is not None:
                                self.spot_realized_pnl = float(row.get("spot_realized_pnl"))
                            if real_slots_cap is not None:
                                self.total_user_capital = real_slots_cap
                            elif "total_user_capital" in row and row.get("total_user_capital") is not None:
                                self.total_user_capital = float(row.get("total_user_capital"))
                            if "wallet_balance" in row and row.get("wallet_balance") is not None:
                                self.manual_test_balance = float(row.get("wallet_balance"))
                            if "manual_realized_pnl" in row and row.get("manual_realized_pnl") is not None:
                                self.manual_realized_pnl = float(row.get("manual_realized_pnl"))
                            if "micro_realized_pnl" in row and row.get("micro_realized_pnl") is not None:
                                self.micro_realized_pnl = float(row.get("micro_realized_pnl"))
                            if "killer2_realized_pnl" in row and row.get("killer2_realized_pnl") is not None:
                                self.killer2_realized_pnl = float(row.get("killer2_realized_pnl"))
                            if "killer3_realized_pnl" in row and row.get("killer3_realized_pnl") is not None:
                                self.killer3_realized_pnl = float(row.get("killer3_realized_pnl"))
                            if "hyper_realized_pnl" in row and row.get("hyper_realized_pnl") is not None:
                                self.hyper_realized_pnl = float(row.get("hyper_realized_pnl"))
                            if "singularity_realized_pnl" in row and row.get("singularity_realized_pnl") is not None:
                                self.singularity_realized_pnl = float(row.get("singularity_realized_pnl"))

                async with session.get(f"{SUPABASE_URL}/rest/v1/active_positions?order=created_at.asc") as resp:
                    if resp.status == 200:
                        pos_data = await resp.json()
                        if isinstance(pos_data, list):
                            loaded_positions = []
                            self.hyper_positions = []
                            self.micro_positions = []
                            self.killer2_positions = []
                            self.killer3_positions = []
                            self.singularity_positions = []
                            self.showcase_positions = []
                            self.showcase_macro_sol = 0.0
                            self.showcase_macro_invested = 0.0
                            self.showcase_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.showcase_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.hyper_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.hyper_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.micro_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.micro_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.killer2_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.killer2_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.killer3_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.killer3_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.singularity_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.singularity_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            self.wallet_active_positions = []
                            self.wallet_open_orders = []
                            self.auto_loops = []

                            for p in pos_data:
                                p_id = str(p.get("id", ""))
                                lbl_raw = str(p.get("label") or "")
                                parsed_donor = 0
                                if "LOAN R" in lbl_raw:
                                    try:
                                        parsed_donor = int(lbl_raw.split("LOAN R")[1].split()[0].strip())
                                    except Exception:
                                        parsed_donor = 0
                                pos_obj = {
                                    "id": p_id,
                                    "round": int(p.get("round") or 1),
                                    "subTrade": int(p.get("sub_trade") or 1),
                                    "label": lbl_raw,
                                    "entryPrice": float(p.get("entry_price") or 0.0),
                                    "solAmount": float(p.get("sol_amount") or 0.0),
                                    "invested": float(p.get("invested") or 0.0),
                                    "isMacro": bool(p.get("is_macro") or False),
                                    "borrowedFrom": parsed_donor,
                                    "targetPrice": float(p.get("target_price") or 0.0),
                                    "ts_high": float(p.get("entry_price") or 0.0),
                                    "timestamp": p.get("created_at") or datetime.now(timezone.utc).isoformat()
                                }

                                if p_id == "ID1_STATE":
                                    self.showcase_realized_pnl = float(p.get("invested") or 0.0)
                                    self.showcase_macro_target = float(p.get("target_price") or 0.0)
                                elif p_id.startswith("ID1_"):
                                    self.showcase_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    if parsed_donor > 0:
                                        self.showcase_round_spent[parsed_donor] = round(self.showcase_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.showcase_round_borrowed[r_idx] = round(self.showcase_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.showcase_round_spent[r_idx] = round(self.showcase_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    if pos_obj.get("isMacro", False):
                                        self.showcase_macro_sol += pos_obj["solAmount"]
                                        self.showcase_macro_invested += pos_obj["invested"]
                                elif p_id.startswith("SNG_"):
                                    self.singularity_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    self.singularity_round_trades_done[r_idx] = self.singularity_round_trades_done.get(r_idx, 0) + 1
                                    if parsed_donor > 0:
                                        self.singularity_round_spent[parsed_donor] = round(self.singularity_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.singularity_round_borrowed[r_idx] = round(self.singularity_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.singularity_round_spent[r_idx] = round(self.singularity_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    if pos_obj.get("isMacro", False):
                                        self.singularity_macro_sol += pos_obj["solAmount"]
                                        self.singularity_macro_invested += pos_obj["invested"]
                                elif p_id.startswith("HYPER_"):
                                    self.hyper_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    self.hyper_round_trades_done[r_idx] = self.hyper_round_trades_done.get(r_idx, 0) + 1
                                    if parsed_donor > 0:
                                        self.hyper_round_spent[parsed_donor] = round(self.hyper_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.hyper_round_borrowed[r_idx] = round(self.hyper_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.hyper_round_spent[r_idx] = round(self.hyper_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                elif p_id.startswith("M_"):
                                    self.micro_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    self.micro_round_trades_done[r_idx] = self.micro_round_trades_done.get(r_idx, 0) + 1
                                    if parsed_donor > 0:
                                        self.micro_round_spent[parsed_donor] = round(self.micro_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.micro_round_borrowed[r_idx] = round(self.micro_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.micro_round_spent[r_idx] = round(self.micro_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                elif p_id.startswith("K2_"):
                                    self.killer2_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    self.killer2_round_trades_done[r_idx] = self.killer2_round_trades_done.get(r_idx, 0) + 1
                                    if parsed_donor > 0:
                                        self.killer2_round_spent[parsed_donor] = round(self.killer2_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.killer2_round_borrowed[r_idx] = round(self.killer2_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.killer2_round_spent[r_idx] = round(self.killer2_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                elif p_id.startswith("K3_"):
                                    self.killer3_positions.append(pos_obj)
                                    r_idx = pos_obj["round"]
                                    self.killer3_round_trades_done[r_idx] = self.killer3_round_trades_done.get(r_idx, 0) + 1
                                    if parsed_donor > 0:
                                        self.killer3_round_spent[parsed_donor] = round(self.killer3_round_spent.get(parsed_donor, 0.0) + pos_obj["invested"], 2)
                                        self.killer3_round_borrowed[r_idx] = round(self.killer3_round_borrowed.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                    else:
                                        self.killer3_round_spent[r_idx] = round(self.killer3_round_spent.get(r_idx, 0.0) + pos_obj["invested"], 2)
                                elif p_id.startswith("MAN_"):
                                    lbl_str = str(pos_obj.get("label", "")).upper()
                                    if "TP_SL" in lbl_str or "TP/SL" in lbl_str or "OCO" in lbl_str:
                                        pos_obj["orderType"] = "TP_SL"
                                    elif "TRAILING" in lbl_str:
                                        pos_obj["orderType"] = "TRAILING_STOP"
                                    elif "LIMIT" in lbl_str:
                                        pos_obj["orderType"] = "LIMIT"
                                    elif "TRIGGER" in lbl_str:
                                        pos_obj["orderType"] = "TRIGGER"
                                    elif "AUTO_LOOP" in lbl_str or "LOOP" in lbl_str:
                                        pos_obj["orderType"] = "AUTO_LOOP"
                                    else:
                                        pos_obj["orderType"] = "MARKET"
                                    self.wallet_active_positions.append(pos_obj)
                                elif p_id.startswith("ORD_"):
                                    lbl_meta = str(p.get("label", "")).split("|")
                                    o_type = lbl_meta[1] if len(lbl_meta) > 1 else "LIMIT"
                                    o_side = lbl_meta[2] if len(lbl_meta) > 2 else "BUY"
                                    cb_val = float(lbl_meta[3]) if len(lbl_meta) > 3 else 1.0
                                    act_p = float(lbl_meta[4]) if len(lbl_meta) > 4 else float(p.get("entry_price", 0.0))
                                    trig_p = float(lbl_meta[5]) if len(lbl_meta) > 5 else float(p.get("target_price", 0.0))
                                    o_price = float(p.get("entry_price", 0.0))
                                    o_invested = float(p.get("invested", 0.0))
                                    o_sol = float(p.get("sol_amount", 0.0))
                                    if o_sol <= 0 and o_price > 0 and o_invested > 0:
                                        o_sol = round(o_invested / o_price, 4)
                                    ord_obj = {
                                        "id": p_id,
                                        "orderId": p_id,
                                        "orderType": o_type,
                                        "side": o_side,
                                        "amount": o_invested if o_side == "BUY" else o_sol,
                                        "solAmount": o_sol,
                                        "invested": o_invested,
                                        "price": o_price,
                                        "entryPrice": o_price,
                                        "activationPrice": act_p,
                                        "isActivated": False,
                                        "stopPrice": trig_p,
                                        "limitPrice": o_price,
                                        "triggerDirection": "BELOW" if trig_p <= act_p else "ABOVE",
                                        "callbackPct": cb_val,
                                        "peakTracked": act_p,
                                        "lowestTracked": act_p,
                                        "status": "OPEN",
                                        "statusText": f"{o_type} {o_side} @ ${round(o_price, 2)}",
                                        "timestamp": p.get("created_at", datetime.now(timezone.utc).isoformat())
                                    }
                                    self.wallet_open_orders.append(ord_obj)
                                elif p_id.startswith("BOT_"):
                                    if not hasattr(self, "copy_subscribers"):
                                        self.copy_subscribers = []
                                    lbl_parts = str(pos_obj.get("label", "")).split("|")
                                    b_type = lbl_parts[1] if len(lbl_parts) > 1 else "VELOCITY_DCA"
                                    s_allowed = int(lbl_parts[2]) if len(lbl_parts) > 2 else 1
                                    b_amt = float(pos_obj.get("invested", 10.0))
                                    pnl_saved = float(lbl_parts[3]) if len(lbl_parts) > 3 else 0.0
                                    self.copy_subscribers.append({
                                        "id": p_id,
                                        "botType": b_type,
                                        "totalCapital": b_amt,
                                        "availableReserve": b_amt,
                                        "slotSize": round(b_amt / max(1, s_allowed), 2),
                                        "slotsAllowed": s_allowed,
                                        "activeSlots": 0,
                                        "realizedPnl": pnl_saved,
                                        "activePositions": [],
                                        "entryPrice": float(pos_obj.get("entryPrice", self.live_price)),
                                        "timestamp": p.get("created_at", datetime.now(timezone.utc).isoformat())
                                    })
                                elif p_id.startswith("CPOS_"):
                                    lbl_parts = str(pos_obj.get("label", "")).split("|")
                                    parent_sub_id = lbl_parts[1] if len(lbl_parts) > 1 else ""
                                    if hasattr(self, "copy_subscribers"):
                                        for sub in self.copy_subscribers:
                                            if sub.get("id") == parent_sub_id:
                                                c_entry = float(pos_obj.get("entryPrice", 0.0)) or float(p.get("entry_price", 0.0))
                                                c_inv = float(pos_obj.get("invested", 0.0)) or float(p.get("invested", 0.0))
                                                c_sol = float(pos_obj.get("solAmount", 0.0)) or float(p.get("sol_amount", 0.0))
                                                sub["activePositions"].append({
                                                    "posId": p_id,
                                                    "entryPrice": c_entry,
                                                    "invested": c_inv,
                                                    "solAmount": c_sol,
                                                    "timestamp": p.get("created_at", datetime.now(timezone.utc).isoformat())
                                                })
                                                sub["activeSlots"] = len(sub["activePositions"])
                                                sub["availableReserve"] = max(0.0, float(sub.get("availableReserve", 0.0)) - c_inv)
                                elif p_id.startswith("ATL_"):
                                    lbl_parts = str(p.get("label", "")).split("|")
                                    b_cb = float(lbl_parts[1]) if len(lbl_parts) > 1 else 0.01
                                    s_cb = float(lbl_parts[2]) if len(lbl_parts) > 2 else 0.01
                                    a_rep = (lbl_parts[3] == "1") if len(lbl_parts) > 3 else True
                                    stg = lbl_parts[4] if len(lbl_parts) > 4 else ("WAITING_SELL_TRIGGER" if float(p.get("sol_amount", 0.0)) > 0 else "WAITING_BUY_TRIGGER")
                                    b_trig = float(lbl_parts[5]) if len(lbl_parts) > 5 else float(p.get("entry_price", 0.0))
                                    s_trig = float(p.get("target_price", 0.0))
                                    cur_peak = float(lbl_parts[6]) if len(lbl_parts) > 6 else s_trig
                                    cur_low = float(lbl_parts[7]) if len(lbl_parts) > 7 else 0.0
                                    sol_qty = float(p.get("sol_amount", 0.0))
                                    inv_amt = float(p.get("invested", 10.0))
                                    exec_p = float(p.get("entry_price", 0.0)) if sol_qty > 0 else 0.0
                                    loop_obj = {
                                        "id": p_id,
                                        "usdtAmount": inv_amt,
                                        "buyTrigger": b_trig,
                                        "buyCallbackPct": b_cb,
                                        "sellTrigger": s_trig,
                                        "sellCallbackPct": s_cb,
                                        "autoRepeat": a_rep,
                                        "stage": stg,
                                        "solBought": sol_qty,
                                        "buyExecutedPrice": exec_p,
                                        "lowestTracked": cur_low,
                                        "peakTracked": cur_peak,
                                        "profitRealized": 0.0,
                                        "status": f"ARMED (TARGET ${s_trig})" if sol_qty > 0 else f"WAITING BUY (${b_trig})"
                                    }
                                    self.auto_loops.append(loop_obj)
                                else:
                                    loaded_positions.append(pos_obj)

                            if self.total_user_capital < 500.0:
                                self.hyper_positions = []
                                self.hyper_round_trades_done = {r: 0 for r in range(1, 11)}
                            if self.total_user_capital < 1000.0:
                                self.singularity_positions = []
                                self.singularity_round_trades_done = {r: 0 for r in range(1, 11)}
                                self.singularity_round_spent = {r: 0.0 for r in range(1, 11)}
                                self.singularity_macro_sol = 0.0
                                self.singularity_macro_invested = 0.0

                            self.active_positions = loaded_positions
                            regular_pos = [p for p in self.active_positions if not p.get("isMacro", False)]
                            macro_pos = [p for p in self.active_positions if p.get("isMacro", False)]

                            all_scalp_sol = (
                                sum(p["solAmount"] for p in self.micro_positions)
                                + sum(p["solAmount"] for p in self.killer2_positions)
                                + sum(p["solAmount"] for p in self.killer3_positions)
                                + sum(p["solAmount"] for p in self.hyper_positions)
                                + sum(p["solAmount"] for p in self.singularity_positions)
                            )
                            all_scalp_inv = (
                                sum(p["invested"] for p in self.micro_positions)
                                + sum(p["invested"] for p in self.killer2_positions)
                                + sum(p["invested"] for p in self.killer3_positions)
                                + sum(p["invested"] for p in self.hyper_positions)
                                + sum(p["invested"] for p in self.singularity_positions)
                            )
                            self.sol_balance = sum(p["solAmount"] for p in regular_pos) + all_scalp_sol
                            self.invested_amount = sum(p["invested"] for p in regular_pos) + all_scalp_inv
                            self.macro_vault_sol = sum(p["solAmount"] for p in macro_pos)
                            self.macro_vault_invested = sum(p["invested"] for p in macro_pos)
                            self.avg_entry_price = round(self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0, 2)
                            self.sub_trade_count = len(regular_pos)
                            self.round_trades_done = {r: 0 for r in range(1, 11)}
                            self.home_round_spent = {r: 0.0 for r in range(1, 11)}
                            self.home_round_borrowed = {r: 0.0 for r in range(1, 11)}
                            for p in regular_pos + macro_pos:
                                r_idx = p.get("round", 1)
                                b_don = p.get("borrowedFrom", 0)
                                if not p.get("isMacro", False):
                                    self.round_trades_done[r_idx] = self.round_trades_done.get(r_idx, 0) + 1
                                if b_don > 0:
                                    self.home_round_spent[b_don] = round(self.home_round_spent.get(b_don, 0.0) + float(p.get("invested", 0.0)), 2)
                                    self.home_round_borrowed[r_idx] = round(self.home_round_borrowed.get(r_idx, 0.0) + float(p.get("invested", 0.0)), 2)
                                else:
                                    self.home_round_spent[r_idx] = round(self.home_round_spent.get(r_idx, 0.0) + float(p.get("invested", 0.0)), 2)

                            sc_inv_total = sum(float(p.get("invested", 0.0)) for p in self.showcase_positions)
                            self.showcase_usdt = max(0.0, round(self.showcase_capital + self.showcase_realized_pnl - sc_inv_total, 2))

                async with session.get(f"{SUPABASE_URL}/rest/v1/trades_history?order=created_at.desc&limit=500") as resp:
                    if resp.status == 200:
                        t_data = await resp.json()
                        if isinstance(t_data, list):
                            bot_logs = []
                            wallet_logs = []
                            scalp_logs = []
                            all_logs = []
                            self.showcase_trades_history = []
                            seen_trade_keys = set()
                            m_pnl = 0.0
                            m_count = 0
                            k2_pnl = 0.0
                            k2_count = 0
                            k3_pnl = 0.0
                            k3_count = 0
                            h_pnl = 0.0
                            sng_pnl = 0.0
                            spot_closed_profit = 0.0
                            wallet_pnl = 0.0

                            micro_logs = []
                            killer2_logs = []
                            killer3_logs = []
                            hyper_logs = []
                            sng_logs = []

                            for t in t_data:
                                e_type = str(t.get("exec_type", "")).upper()
                                ord_id = str(t.get("order_id", "")).upper()
                                side_raw = str(t.get("side") or "BUY").upper()
                                p_val = float(t.get("profit", 0.0))
                                s_qty_val = float(t.get("sol_amount") or 0.0)
                                if "CANCEL" in e_type:
                                    continue
                                dedup_key = f"{ord_id}_{side_raw}_{t.get('created_at')}"
                                if dedup_key in seen_trade_keys:
                                    continue
                                seen_trade_keys.add(dedup_key)

                                formatted_t = {
                                    "orderId": ord_id,
                                    "side": t.get("side") or "BUY",
                                    "price": float(t.get("price") or 0.0),
                                    "solAmount": s_qty_val,
                                    "fee": float(t.get("fee") or 0.0),
                                    "profit": p_val,
                                    "realizedPnl": p_val,
                                    "round": int(t.get("round") or 1),
                                    "execType": e_type,
                                    "timestamp": t.get("created_at") or datetime.now(timezone.utc).isoformat()
                                }
                                if ord_id.startswith("ID1_") or "ID1_SHOWCASE" in e_type:
                                    self.showcase_trades_history.append(formatted_t)
                                    continue
                                all_logs.append(formatted_t)
                                is_sell_trade = (t.get("side") in ["SELL", "AUTO_LOOP_SELL"] or "SELL" in e_type or "EXIT" in e_type or "PROFIT" in e_type)

                                if ord_id.startswith(("MAN_", "ATL_", "ORD_", "COPY_", "CPOS_", "BOT_")) or any(k in e_type for k in ["BUY_FILLED", "SELL_FILLED", "AUTO_TRAILING_LOOP", "MANUAL", "COPY"]):
                                    wallet_logs.append(formatted_t)
                                    if is_sell_trade:
                                        wallet_pnl += p_val
                                elif ord_id.startswith("SNG_") or "SINGULARITY" in e_type:
                                    sng_logs.append(formatted_t)
                                    if is_sell_trade:
                                        sng_pnl += p_val
                                elif ord_id.startswith("HYPER_") or (("HYPER" in e_type or "TITAN_POOL" in e_type) and not ord_id.startswith("SNG_")):
                                    hyper_logs.append(formatted_t)
                                    if is_sell_trade:
                                        h_pnl += p_val
                                elif ord_id.startswith("M_") or (("MICRO" in e_type or "APEX" in e_type) and not ord_id.startswith("SNG_")):
                                    micro_logs.append(formatted_t)
                                    scalp_logs.append(formatted_t)
                                    if is_sell_trade:
                                        m_count += 1
                                        m_pnl += p_val
                                elif ord_id.startswith("K2_") or (("KILLER2" in e_type or "QUANTUM" in e_type) and not ord_id.startswith("SNG_")):
                                    killer2_logs.append(formatted_t)
                                    scalp_logs.append(formatted_t)
                                    if is_sell_trade:
                                        k2_count += 1
                                        k2_pnl += p_val
                                elif ord_id.startswith("K3_") or (("KILLER3" in e_type or "ABYSS" in e_type) and not ord_id.startswith("SNG_")):
                                    killer3_logs.append(formatted_t)
                                    scalp_logs.append(formatted_t)
                                    if is_sell_trade:
                                        k3_count += 1
                                        k3_pnl += p_val
                                else:
                                    bot_logs.append(formatted_t)
                                    if is_sell_trade:
                                        spot_closed_profit += p_val

                            self.trades_history = all_logs
                            self.spot_trades_history = bot_logs
                            self.micro_trades_history = micro_logs
                            self.killer2_trades_history = killer2_logs
                            self.killer3_trades_history = killer3_logs
                            self.hyper_trades_history = hyper_logs
                            self.singularity_trades_history = sng_logs
                            self.scalp_trades_history = scalp_logs
                            self.manual_trades_history = wallet_logs

                            if self.micro_realized_pnl == 0.0 and m_pnl != 0.0:
                                self.micro_realized_pnl = round(m_pnl, 4)
                            self.micro_total_trades = m_count
                            if self.killer2_realized_pnl == 0.0 and k2_pnl != 0.0:
                                self.killer2_realized_pnl = round(k2_pnl, 4)
                            self.killer2_total_trades = k2_count
                            if self.killer3_realized_pnl == 0.0 and k3_pnl != 0.0:
                                self.killer3_realized_pnl = round(k3_pnl, 4)
                            self.killer3_total_trades = k3_count
                            if self.hyper_realized_pnl == 0.0 and h_pnl != 0.0:
                                self.hyper_realized_pnl = round(h_pnl, 4)
                            self.hyper_total_trades = len([t for t in hyper_logs if str(t.get("side","")).upper() == "SELL"])
                            if self.singularity_realized_pnl == 0.0 and sng_pnl != 0.0:
                                self.singularity_realized_pnl = round(sng_pnl, 4)
                            self.singularity_total_trades = len([t for t in sng_logs if str(t.get("side","")).upper() == "SELL"])
                            if self.spot_realized_pnl == 0.0 and spot_closed_profit != 0.0:
                                self.spot_realized_pnl = round(spot_closed_profit, 4)
                            if self.manual_realized_pnl == 0.0 and wallet_pnl != 0.0:
                                self.manual_realized_pnl = round(wallet_pnl, 4)
                            summed_all = round(self.spot_realized_pnl + self.micro_realized_pnl + self.killer2_realized_pnl + self.killer3_realized_pnl + self.hyper_realized_pnl + self.singularity_realized_pnl, 4)
                            if summed_all != 0.0 or self.realized_pnl == 0.0:
                                self.realized_pnl = summed_all

                            total_active_cost = self.invested_amount + self.macro_vault_invested + self.round8_hold_invested
                            if self.total_user_capital <= 0:
                                self.usdt_balance = 0.0
                            else:
                                self.usdt_balance = max(0.0, round(self.total_user_capital + self.realized_pnl - total_active_cost, 2))

                            self.hyper_pool_balance = self.usdt_balance
                            self.singularity_pool_balance = self.usdt_balance

                            w_pos_inv = sum(float(p.get("invested", 0.0)) for p in self.wallet_active_positions)
                            w_ord_inv = sum(float(o.get("invested", o.get("amount", 0.0))) for o in self.wallet_open_orders if o.get("side") == "BUY")
                            copy_locked_inv = sum(float(s.get("totalCapital", s.get("invested", 0.0))) for s in getattr(self, "copy_subscribers", []))
                            atl_locked_inv = sum(float(a.get("usdtAmount", 0.0)) for a in self.auto_loops)
                            self.manual_test_balance = max(0.0, round(100.0 + self.manual_realized_pnl - w_pos_inv - w_ord_inv - copy_locked_inv - atl_locked_inv, 2))
                            self.db_loaded = True
                            asyncio.create_task(self.db_sync_state())
        except Exception as e:
            print(f"DATABASE LOAD ERROR: {e}")
            return

    async def db_sync_state(self):
        if not getattr(self, "db_loaded", False) or self.live_price <= 0:
            return
        try:
            payload = {
                "total_user_capital": round(self.total_user_capital, 2),
                "usdt_balance": round(self.usdt_balance, 2),
                "wallet_balance": round(self.manual_test_balance, 2),
                "manual_realized_pnl": round(self.manual_realized_pnl, 4),
                "sol_balance": round(self.sol_balance, 4),
                "invested_amount": round(self.invested_amount, 2),
                "avg_entry_price": round(self.avg_entry_price, 2),
                "realized_pnl": round(self.realized_pnl, 4),
                "spot_realized_pnl": round(self.spot_realized_pnl, 4),
                "micro_realized_pnl": round(self.micro_realized_pnl, 4),
                "killer2_realized_pnl": round(self.killer2_realized_pnl, 4),
                "killer3_realized_pnl": round(self.killer3_realized_pnl, 4),
                "hyper_realized_pnl": round(self.hyper_realized_pnl, 4),
                "hyper_pool_balance": round(self.hyper_pool_balance, 2),
                "singularity_realized_pnl": round(self.singularity_realized_pnl, 4),
                "singularity_pool_balance": round(self.singularity_pool_balance, 2),
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
                    "is_macro": pos.get("isMacro", False),
                    "target_price": pos.get("targetPrice", 0.0)
                }
                db_trade_row = {
                    "order_id": str(trade_data.get("order_id") or trade_data.get("orderId")),
                    "side": str(trade_data.get("side", "BUY")),
                    "price": float(trade_data.get("price", 0.0)),
                    "sol_amount": float(trade_data.get("sol_amount") or trade_data.get("solAmount", 0.0)),
                    "fee": float(trade_data.get("fee", 0.0)),
                    "profit": float(trade_data.get("profit", 0.0)),
                    "round": int(trade_data.get("round", 0)),
                    "exec_type": str(trade_data.get("exec_type") or trade_data.get("execType", "BUY")),
                    "created_at": trade_data.get("created_at") or trade_data.get("timestamp") or datetime.now(timezone.utc).isoformat()
                }
                await session.post(f"{SUPABASE_URL}/rest/v1/active_positions?on_conflict=id", json=pos_row)
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=db_trade_row)
            await self.db_sync_state()
        except Exception:
            pass

    async def db_save_sell_individual(self, pos_id, trade_data):
        try:
            db_row = {
                "order_id": str(trade_data.get("order_id") or trade_data.get("orderId")),
                "side": str(trade_data.get("side")),
                "price": float(trade_data.get("price", 0.0)),
                "sol_amount": float(trade_data.get("sol_amount") or trade_data.get("solAmount", 0.0)),
                "fee": float(trade_data.get("fee", 0.0)),
                "profit": float(trade_data.get("profit", 0.0)),
                "round": int(trade_data.get("round", 0)),
                "exec_type": str(trade_data.get("exec_type") or trade_data.get("execType", "SELL")),
                "created_at": trade_data.get("timestamp") or datetime.now(timezone.utc).isoformat()
            }
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.delete(f"{SUPABASE_URL}/rest/v1/active_positions?id=eq.{pos_id}")
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=db_row)
            await self.db_sync_state()
        except Exception:
            pass

    async def db_save_engine_trade(self, trade_data):
        try:
            db_row = {
                "order_id": str(trade_data.get("order_id") or trade_data.get("orderId")),
                "side": str(trade_data.get("side")),
                "price": float(trade_data.get("price", 0.0)),
                "sol_amount": float(trade_data.get("sol_amount") or trade_data.get("solAmount", 0.0)),
                "fee": float(trade_data.get("fee", 0.0)),
                "profit": float(trade_data.get("profit", 0.0)),
                "round": int(trade_data.get("round", 0)),
                "exec_type": str(trade_data.get("exec_type") or trade_data.get("execType", "ENGINE")),
                "created_at": trade_data.get("timestamp") or datetime.now(timezone.utc).isoformat()
            }
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.post(f"{SUPABASE_URL}/rest/v1/trades_history", json=db_row)
            await self.db_sync_state()
        except Exception:
            pass

    def process_market_trades(self, trades):
        if not trades:
            return
        if not hasattr(self, "whale_trades_window"):
            self.whale_trades_window = []

        now_ts = datetime.now(timezone.utc).timestamp()
        for t in trades:
            price = float(t.get("p", 0.0))
            qty = float(t.get("q", 0.0))
            is_buyer_maker = t.get("m", False)
            trade_val = price * qty
            if trade_val >= 250.0:
                is_aggressive_buy = not is_buyer_maker
                weight = 3.0 if trade_val >= 10000.0 else (2.0 if trade_val >= 2500.0 else 1.0)
                self.whale_trades_window.append({
                    "val": trade_val * weight,
                    "rawVal": trade_val,
                    "isBuy": is_aggressive_buy,
                    "time": now_ts
                })

        self.whale_trades_window = [x for x in self.whale_trades_window if (now_ts - x["time"]) <= 120.0]

        if len(self.whale_trades_window) > 0:
            buy_vol = sum(x["val"] for x in self.whale_trades_window if x["isBuy"])
            sell_vol = sum(x["val"] for x in self.whale_trades_window if not x["isBuy"])
            total_vol = buy_vol + sell_vol
            self.cvd_net_volume = round(buy_vol - sell_vol, 2)
            if total_vol > 0:
                ratio = round((buy_vol / total_vol) * 100.0, 1)
                self.whale_orderflow_ratio = ratio
                if ratio >= 60.0 and self.cvd_net_volume > 5000.0:
                    self.whale_sentiment = "BULLISH"
                    self.whale_boost_multiplier = 1.30
                    self.whale_dump_alert = False
                elif ratio <= 38.0 and self.cvd_net_volume < -5000.0:
                    self.whale_sentiment = "BEARISH"
                    self.whale_boost_multiplier = 0.80
                    self.whale_dump_alert = True
                else:
                    self.whale_sentiment = "NEUTRAL"
                    self.whale_boost_multiplier = 1.0
                    self.whale_dump_alert = False

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
        scalp_sol = (
            sum(p.get("solAmount", 0.0) for p in self.micro_positions)
            + sum(p.get("solAmount", 0.0) for p in self.killer2_positions)
            + sum(p.get("solAmount", 0.0) for p in self.killer3_positions)
            + sum(p.get("solAmount", 0.0) for p in self.hyper_positions)
            + sum(p.get("solAmount", 0.0) for p in self.singularity_positions)
        )
        scalp_inv = (
            sum(p.get("invested", 0.0) for p in self.micro_positions)
            + sum(p.get("invested", 0.0) for p in self.killer2_positions)
            + sum(p.get("invested", 0.0) for p in self.killer3_positions)
            + sum(p.get("invested", 0.0) for p in self.hyper_positions)
            + sum(p.get("invested", 0.0) for p in self.singularity_positions)
        )
        reg_sol = sum(p.get("solAmount", 0.0) for p in self.active_positions if not p.get("isMacro", False))
        reg_inv = sum(p.get("invested", 0.0) for p in self.active_positions if not p.get("isMacro", False))
        all_sol = reg_sol + scalp_sol + self.macro_vault_sol
        all_invested = reg_inv + scalp_inv + self.macro_vault_invested
        total_cap = self.usdt_balance + all_invested
        unrealized_pnl = 0.0
        pnl_pct = 0.0

        if all_sol > 0 and all_invested > 0:
            current_val = all_sol * self.live_price
            unrealized_pnl = current_val - all_invested
            pnl_pct = (unrealized_pnl / all_invested) * 100.0

        alloc_pct = self.round_allocations.get(self.active_round, 0.20) * 100.0
        combined_entry = (all_invested / all_sol) if all_sol > 0 else 0.0

        def calc_bot_ts_state(pos_list, rules):
            if not pos_list or self.live_price <= 0:
                return 0.0, 0.0, "IDLE"
            p_peak = max(float(p.get("ts_high", p.get("entryPrice", self.live_price))) for p in pos_list)
            p_peak = max(p_peak, self.live_price)
            p_entry = min(float(p.get("entryPrice", self.live_price)) for p in pos_list)
            diff = p_peak - p_entry
            pullback = 0.0
            stg = "IDLE"
            for g_req, pb_val, s_title in rules:
                if diff >= g_req:
                    pullback = pb_val
                    stg = s_title
                    break
            stop_val = round(p_peak - pullback, 2) if pullback > 0.0 else 0.0
            return round(p_peak, 2), stop_val, stg

        h_ts_h, h_ts_l, h_stg = calc_bot_ts_state(self.hyper_positions, [(0.70, 0.12, "STAGE_3"), (0.40, 0.08, "STAGE_2"), (0.20, 0.05, "STAGE_1")])
        m_ts_h, m_ts_l, m_stg = calc_bot_ts_state(self.micro_positions, [(0.80, 0.15, "STAGE_3"), (0.55, 0.12, "STAGE_2"), (0.35, 0.08, "STAGE_1")])
        k2_ts_h, k2_ts_l, k2_stg = calc_bot_ts_state(self.killer2_positions, [(1.20, 0.25, "STAGE_3"), (0.80, 0.20, "STAGE_2"), (0.50, 0.15, "STAGE_1")])
        k3_ts_h, k3_ts_l, k3_stg = calc_bot_ts_state(self.killer3_positions, [(1.50, 0.03, "STAGE_3"), (1.00, round(self.live_price * 0.005, 2), "STAGE_2"), (0.60, round(self.live_price * 0.010, 2), "STAGE_1")])
        sng_ts_h, sng_ts_l, sng_stg = calc_bot_ts_state(self.singularity_positions, [(1.50, 0.20, "STAGE_3"), (0.80, 0.15, "STAGE_2"), (0.40, 0.10, "STAGE_1")])

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

        positions_list = []
        for p in self.wallet_active_positions:
            p_sol = float(p.get("solAmount", 0.0))
            p_inv = float(p.get("invested", 0.0))
            p_ent = float(p.get("entryPrice", self.live_price))
            positions_list.append({
                "id": p.get("id"),
                "orderId": p.get("id"),
                "round": 0,
                "subTrade": 0,
                "label": p.get("label", "MANUAL POSITION"),
                "side": p.get("side", "BUY"),
                "entryPrice": round(p_ent, 2),
                "solAmount": round(p_sol, 4),
                "invested": round(p_inv, 2),
                "orderType": p.get("orderType", "MARKET"),
                "isManualWallet": True,
                "status": "HOLDING",
                "timestamp": p.get("timestamp", datetime.now(timezone.utc).strftime("%H:%M:%S"))
            })

        open_orders_list = []
        for o in self.wallet_open_orders:
            o_price = float(o.get("price", self.live_price))
            o_sol = float(o.get("solAmount", 0.0))
            o_inv = float(o.get("invested", o.get("amount", 0.0)))
            o_type = o.get("orderType", "LIMIT")
            open_orders_list.append({
                "id": o.get("id"),
                "orderId": o.get("id"),
                "orderType": o_type,
                "side": o.get("side", "BUY"),
                "amount": round(o_inv, 2) if o.get("side") == "BUY" else round(o_sol, 4),
                "solAmount": round(o_sol, 4),
                "invested": round(o_inv, 2),
                "price": round(o_price, 2),
                "entryPrice": round(o_price, 2),
                "stopPrice": round(float(o.get("stopPrice", 0.0)), 2),
                "limitPrice": round(float(o.get("limitPrice", o_price)), 2),
                "callbackPct": float(o.get("callbackPct", 1.0)),
                "status": o.get("status", "OPEN"),
                "statusText": o.get("statusText", f"{o_type} {o.get('side', 'BUY')} @ ${round(o_price, 2)}"),
                "timestamp": o.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            })
        atl_sol_total = 0.0
        atl_inv_total = 0.0
        for atl in self.auto_loops:
            s_bought = float(atl.get("solBought", 0.0))
            if s_bought > 0:
                atl_sol_total += s_bought
                atl_inv_total += float(atl.get("usdtAmount", 0.0))
                positions_list.insert(0, {
                    "id": atl.get("id"),
                    "round": 0,
                    "subTrade": 0,
                    "label": f"LOOP HOLDING ({atl.get('id')})",
                    "side": "BUY",
                    "entryPrice": round(float(atl.get("buyExecutedPrice", self.live_price)), 2),
                    "solAmount": round(s_bought, 4),
                    "invested": round(float(atl.get("usdtAmount", 0.0)), 2),
                    "orderType": "AUTO_LOOP",
                    "isManualWallet": True,
                    "status": "HOLDING",
                    "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                })
            else:
                open_orders_list.insert(0, {
                    "id": atl.get("id"),
                    "orderId": atl.get("id"),
                    "orderType": "Auto Trailing Loop",
                    "side": "BUY",
                    "amount": atl.get("usdtAmount", 0.0),
                    "solAmount": 0.0,
                    "invested": round(atl.get("usdtAmount", 0.0), 2),
                    "price": round(atl.get("buyTrigger", 0.0), 2),
                    "entryPrice": 0.0,
                    "stopPrice": round(atl.get("buyTrigger", 0.0), 2),
                    "limitPrice": round(atl.get("sellTrigger", 0.0), 2),
                    "callbackPct": atl.get("buyCallbackPct", 0.01),
                    "status": "OPEN",
                    "statusText": atl.get("status", "OPEN"),
                    "label": "Auto Trailing Loop",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

        w_sol_total = sum(p.get("solAmount", 0.0) for p in getattr(self, "wallet_active_positions", [])) + atl_sol_total
        w_invested_total = sum(p.get("invested", 0.0) for p in getattr(self, "wallet_active_positions", [])) + atl_inv_total
        w_avg_entry = round(w_invested_total / w_sol_total, 2) if w_sol_total > 0 else 0.0
        
        w_unreal_pnl = round((self.live_price - w_avg_entry) * w_sol_total, 2) if w_sol_total > 0 else 0.0
        w_unreal_pct = round(((self.live_price - w_avg_entry) / w_avg_entry) * 100.0, 2) if w_avg_entry > 0 else 0.0

        w_locked_usdt = sum(o.get("invested", o.get("amount", 0.0)) for o in open_orders_list if o.get("side") == "BUY")
        w_total_usdt = round(self.manual_test_balance + w_locked_usdt, 2)

        return {
            "isPaused": self.is_paused,
            "price": self.live_price,
            "livePrice": self.live_price,
            "manualTestBalance": round(self.manual_test_balance, 2),
            "walletLockedUsdt": round(w_locked_usdt, 2),
            "walletTotalUsdt": w_total_usdt,
            "walletSol": round(w_sol_total, 4),
            "walletInvested": round(w_invested_total, 2),
            "walletAvgEntry": w_avg_entry,
            "walletUnrealizedPnl": w_unreal_pnl,
            "walletUnrealizedPct": w_unreal_pct,
            "walletRealizedPnl": round(self.manual_realized_pnl, 2),
            "walletActivePositions": positions_list,
            "walletOpenOrders": open_orders_list,
            "openOrders": open_orders_list,
            "orders": open_orders_list,
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
            "spotRealizedPnl": round(self.spot_realized_pnl, 2),
            "realizedPnl": round(self.realized_pnl, 2),
            "cooldownRemaining": self.cooldown_remaining,
            "macroVaultSol": round(self.macro_vault_sol, 4),
            "macroVaultInvested": round(self.macro_vault_invested, 2),
            "whaleOrderflow": self.whale_orderflow_ratio,
            "whaleSentiment": self.whale_sentiment,
            "whaleBoost": getattr(self, "whale_boost_multiplier", 1.0),
            "whaleDumpAlert": getattr(self, "whale_dump_alert", False),
            "cvdNetVolume": getattr(self, "cvd_net_volume", 0.0),
            "solanaDexMode": getattr(self, "solana_dex_mode", "MAINNET"),
            "canManualTrade": True,
            "subTradeCount": self.sub_trade_count,
            "maxSubTrades": self.max_sub_trades,
            "activePositions": self.active_positions,
            "tradesHistory": self.trades_history,
            "spotTradesHistory": [{
                "orderId": p["id"],
                "side": "BUY",
                "price": float(p.get("entryPrice", 0.0)),
                "solAmount": float(p.get("solAmount", 0.0)),
                "fee": 0.0,
                "profit": 0.0,
                "isOpen": True,
                "round": p.get("round", 1),
                "execType": "ACTIVE_POSITION",
                "timestamp": p.get("timestamp", datetime.now(timezone.utc).isoformat())
            } for p in self.active_positions] + self.spot_trades_history,
            "microTradesHistory": self.micro_trades_history,
            "killer2TradesHistory": self.killer2_trades_history,
            "killer3TradesHistory": self.killer3_trades_history,
            "scalpTradesHistory": self.scalp_trades_history,
            "manualTradesHistory": self.manual_trades_history,
            "latestSignal": self.latest_signal,
            "botThought": ai_thoughts,
            "hyperPoolActive": self.total_user_capital >= 500.0,
            "hyperPoolUsers": 1,
            "hyperPoolBalance": round(self.usdt_balance + sum(p.get("invested", 0.0) for p in self.hyper_positions), 2),
            "hyperUserInvestment": round(self.total_user_capital, 2),
            "hyperTradeSize": round(self.get_tier_config()["size"], 2),
            "hyperPositions": self.hyper_positions,
            "hyperRealizedPnl": round(self.hyper_realized_pnl, 4),
            "hyperTotalTrades": self.hyper_total_trades,
            "hyperTradesHistory": getattr(self, "hyper_trades_history", []),
            "hyperUserDailyPnl": round(self.hyper_realized_pnl, 4),
            "hyperTsHigh": h_ts_h,
            "hyperTsLow": h_ts_l,
            "hyperTrailingStage": h_stg,
            "microTsHigh": m_ts_h,
            "microTsLow": m_ts_l,
            "microTrailingStage": m_stg,
            "killer2TsHigh": k2_ts_h,
            "killer2TsLow": k2_ts_l,
            "killer2TrailingStage": k2_stg,
            "killer3TsHigh": k3_ts_h,
            "killer3TsLow": k3_ts_l,
            "killer3TrailingStage": k3_stg,
            "singularityTsHigh": sng_ts_h,
            "singularityTsLow": sng_ts_l,
            "singularityTrailingStage": sng_stg,
            "microPoolUsers": getattr(self, "micro_pool_users", 1),
            "microPoolBalance": round(self.usdt_balance + sum(p.get("invested", 0.0) for p in self.micro_positions), 2),
            "microUserInvestment": 10.0,
            "microUserDailyPnl": round(self.micro_realized_pnl / max(1, getattr(self, "micro_pool_users", 1)), 4),
            "microPositions": self.micro_positions,
            "microRealizedPnl": round(self.micro_realized_pnl, 4),
            "microTotalTrades": self.micro_total_trades,
            "microIdleFundAvail": round(self.get_scavenged_idle_fund(), 2),
            "microTbLowest": round(self.micro_tb_lowest, 2),
            "killer2TbLowest": round(self.killer2_tb_lowest, 2),
            "killer3TbLowest": round(self.killer3_tb_lowest, 2),
            "hyperTbLowest": round(self.hyper_tb_lowest, 2),
            "killer2PoolUsers": getattr(self, "killer2_pool_users", 1),
            "killer2PoolBalance": round(self.usdt_balance + sum(p.get("invested", 0.0) for p in self.killer2_positions), 2),
            "killer2UserInvestment": 10.0,
            "killer2UserDailyPnl": round(self.killer2_realized_pnl / max(1, getattr(self, "killer2_pool_users", 1)), 4),
            "killer2Positions": self.killer2_positions,
            "killer2RealizedPnl": round(self.killer2_realized_pnl, 4),
            "killer2TotalTrades": self.killer2_total_trades,
            "killer2IdleFundAvail": round(self.get_killer2_idle_fund(), 2),
            "killer3PoolUsers": getattr(self, "killer3_pool_users", 1),
            "killer3PoolBalance": round(self.usdt_balance + sum(p.get("invested", 0.0) for p in self.killer3_positions), 2),
            "killer3UserInvestment": 10.0,
            "killer3UserDailyPnl": round(self.killer3_realized_pnl / max(1, getattr(self, "killer3_pool_users", 1)), 4),
            "killer3Positions": self.killer3_positions,
            "killer3RealizedPnl": round(self.killer3_realized_pnl, 4),
            "killer3TotalTrades": self.killer3_total_trades,
            "killer3IdleFundAvail": round(self.get_killer3_idle_fund(), 2),
            "singularityActive": self.total_user_capital >= 1000.0,
            "singularityUsers": 1,
            "singularityPoolBalance": round(self.usdt_balance + sum(p.get("invested", 0.0) for p in self.singularity_positions), 2),
            "singularityUserInvestment": round(self.total_user_capital, 2),
            "singularityTradeSize": round(self.get_tier_config()["size"], 2),
            "singularityPositions": self.singularity_positions,
            "singularityRealizedPnl": round(self.singularity_realized_pnl, 4),
            "singularityTotalTrades": self.singularity_total_trades,
            "singularityTradesHistory": getattr(self, "singularity_trades_history", []),
            "singularityUserDailyPnl": round(self.singularity_realized_pnl, 4),
            "singularityMacroSol": round(self.singularity_macro_sol, 4),
            "singularityMacroInvested": round(self.singularity_macro_invested, 2),
            "singularityTbLowest": round(self.singularity_tb_lowest, 2),
            "autoLoops": self.auto_loops,
            "copySubscribers": getattr(self, "copy_subscribers", []),
            "harvesterActive": self.harvester_active,
            "harvesterSol": round(self.harvester_vault_sol, 4),
            "harvesterInvested": round(self.harvester_vault_invested, 2),
            "harvesterCash": round(self.harvester_vault_cash, 2),
            "harvesterBorrowed": round(self.harvester_borrowed_r8, 2),
            "harvesterRealizedPnl": round(self.harvester_realized_pnl, 4),
            "harvesterStatus": self.harvester_status,
            "harvesterCycle": self.harvester_cycle_count,
            "round8HoldSol": round(self.round8_hold_sol, 4),
            "round8HoldInvested": round(self.round8_hold_invested, 2),
            "ownerShowcase": self.get_showcase_state()
        }

    def get_round_top_price(self, round_num):
        step = 250.0
        phase = max(1, min(10, self.active_phase))
        phase_max = phase * step
        round_step = step / 10.0
        return phase_max - ((round_num - 1) * round_step)

    def get_eligible_donor_rounds(self, cur_rnd):
        if cur_rnd in [5, 6, 7, 8]:
            return list(range(1, cur_rnd))
        return []

    def allocate_round_budget(self, spent_dict, borrowed_dict, cur_rnd, target_size, total_pool_budget):
        if cur_rnd in [9, 10] or total_pool_budget <= 0:
            return False, 0
        round_max = self.round_allocations.get(cur_rnd, 0.10) * total_pool_budget
        round_spent = spent_dict.get(cur_rnd, 0.0)
        if (round_max - round_spent) >= target_size:
            spent_dict[cur_rnd] = round(round_spent + target_size, 2)
            return True, 0
        donors = self.get_eligible_donor_rounds(cur_rnd)
        if not donors:
            return False, 0
        for r_donor in donors:
            d_alloc = self.round_allocations.get(r_donor, 0.10) * total_pool_budget
            d_spent = spent_dict.get(r_donor, 0.0)
            if (d_alloc - d_spent) >= target_size:
                spent_dict[r_donor] = round(d_spent + target_size, 2)
                borrowed_dict[cur_rnd] = round(borrowed_dict.get(cur_rnd, 0.0) + target_size, 2)
                return True, r_donor
        best_donor = 0
        best_free = 0.0
        total_free = max(0.0, round_max - round_spent)
        for r_donor in donors:
            d_alloc = self.round_allocations.get(r_donor, 0.10) * total_pool_budget
            d_free = max(0.0, d_alloc - spent_dict.get(r_donor, 0.0))
            total_free += d_free
            if d_free > best_free:
                best_free = d_free
                best_donor = r_donor
        if total_free >= target_size and best_donor > 0:
            spent_dict[best_donor] = round(spent_dict.get(best_donor, 0.0) + target_size, 2)
            borrowed_dict[cur_rnd] = round(borrowed_dict.get(cur_rnd, 0.0) + target_size, 2)
            return True, best_donor
        return False, 0

    def process_round_transitions(self):
        if self.is_paused or self.live_price <= 0:
            return
        cur_p = float(self.live_price)
        cur_rnd = self.active_round

        for r_chk in [8, 7, 6, 5]:
            r_top = self.get_round_top_price(r_chk)
            if cur_p >= (r_top - 1.0) or cur_rnd < r_chk:
                for p in list(self.active_positions):
                    if not p.get("isMacro", False) and p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_sell_individual(p)
                for p in list(self.micro_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_micro_sell(p)
                for p in list(self.killer2_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_killer2_sell(p)
                for p in list(self.killer3_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_killer3_sell(p)
                for p in list(self.hyper_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_hyper_sell(p)
                for p in list(self.singularity_positions):
                    if p.get("round") == r_chk and p.get("borrowedFrom", 0) > 0:
                        est_p = (float(p["solAmount"]) * cur_p * (1.0 - self.taker_fee_pct)) - float(p["invested"])
                        if est_p >= self.min_net_profit_usdt:
                            self.execute_singularity_sell(p)

                if r_chk == 8:
                    for p in list(self.active_positions):
                        if p.get("round") == 8 and p.get("borrowedFrom", 0) == 0 and not p.get("isMacro", False):
                            p["isMacro"] = True
                            p["label"] = "R8 HOLD VAULT"
                            p_sol = float(p["solAmount"])
                            p_inv = float(p["invested"])
                            self.sol_balance = max(0.0, self.sol_balance - p_sol)
                            self.invested_amount = max(0.0, self.invested_amount - p_inv)
                            self.macro_vault_sol += p_sol
                            self.macro_vault_invested += p_inv
                            self.macro_vault_entry = self.macro_vault_invested / self.macro_vault_sol if self.macro_vault_sol > 0 else cur_p
                            self.macro_target_price = round(max(200.0, self.macro_vault_entry * 2.0), 2)
                            p["targetPrice"] = self.macro_target_price
                            self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0
                            asyncio.create_task(self.db_save_buy(p, {
                                "order_id": p["id"] + "_HOLD",
                                "side": "HOLD",
                                "price": round(cur_p, 2),
                                "sol_amount": 0.0,
                                "fee": 0.0,
                                "profit": 0.0,
                                "round": 8,
                                "exec_type": "R8_TRANSITION_HOLD"
                            }))
                    if self.total_user_capital >= 40.0 and self.usdt_balance >= 10.0:
                        r8_own_max = round(self.round_allocations.get(8, 0.27) * self.total_user_capital, 2)
                        r8_own_active = sum(float(p["invested"]) for p in self.active_positions if p.get("round") == 8 and p.get("borrowedFrom", 0) == 0)
                        r8_own_rem = round(r8_own_max - r8_own_active, 2)
                        if r8_own_rem >= 10.0:
                            invest_target = min(self.usdt_balance, r8_own_rem)
                            fee = invest_target * self.taker_fee_pct
                            net_invest = invest_target - fee
                            sol_bought = net_invest / cur_p
                            self.usdt_balance = round(self.usdt_balance - invest_target, 2)
                            self.home_round_spent[8] = round(self.home_round_spent.get(8, 0.0) + invest_target, 2)
                            self.macro_vault_sol += sol_bought
                            self.macro_vault_invested += invest_target
                            self.macro_vault_entry = self.macro_vault_invested / self.macro_vault_sol if self.macro_vault_sol > 0 else cur_p
                            self.macro_target_price = round(max(200.0, self.macro_vault_entry * 2.0), 2)
                            pos_id = str(uuid.uuid4())[:8].upper()
                            hold_pos = {
                                "id": pos_id,
                                "round": 8,
                                "subTrade": 1,
                                "label": "R8 HOLD VAULT",
                                "entryPrice": round(cur_p, 2),
                                "solAmount": round(sol_bought, 4),
                                "invested": round(invest_target, 2),
                                "isMacro": True,
                                "borrowedFrom": 0,
                                "targetPrice": self.macro_target_price,
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            self.active_positions.append(hold_pos)
                            asyncio.create_task(self.db_save_buy(hold_pos, {
                                "order_id": pos_id + "_B",
                                "side": "BUY",
                                "price": round(cur_p, 2),
                                "sol_amount": round(sol_bought, 4),
                                "fee": round(fee, 4),
                                "profit": 0.0,
                                "round": 8,
                                "exec_type": "R8_END_SOL_HOLD"
                            }))

    def execute_buy(self, is_sub_trade=False, escalate_round=False):
        if self.is_paused or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return

        self.sync_phase_and_round()
        if self.total_user_capital < 40.0:
            return
        cur_rnd = self.active_round
        cfg = self.get_tier_config()
        max_allowed_slots = cfg["slots"]

        current_done = self.round_trades_done.get(cur_rnd, 0)
        if current_done >= max_allowed_slots:
            return

        target_size = min(self.usdt_balance, 10.0)
        allowed, borrowed_donor = self.allocate_round_budget(self.home_round_spent, self.home_round_borrowed, cur_rnd, target_size, self.total_user_capital)
        if not allowed:
            return
        is_macro_hold = False
        invest_target = target_size

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_bought = net_invest / self.live_price
        self.usdt_balance = round(self.usdt_balance - invest_target, 2)
        self.round_trades_done[cur_rnd] = self.round_trades_done.get(cur_rnd, 0) + 1
        self.sub_trade_count = self.round_trades_done[cur_rnd]
        pos_id = str(uuid.uuid4())[:8].upper()

        self.sol_balance += sol_bought
        self.invested_amount += invest_target
        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0
        target_exit = round(self.live_price + 0.40, 2)
        if borrowed_donor > 0:
            pos_label = f"R{cur_rnd} (LOAN R{borrowed_donor} #{self.sub_trade_count})"
        else:
            pos_label = f"R{cur_rnd} (Trade {self.sub_trade_count}/24)"
        pos = {
            "id": pos_id,
            "round": cur_rnd,
            "subTrade": self.sub_trade_count,
            "label": pos_label,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(invest_target, 2),
            "isMacro": False,
            "borrowedFrom": borrowed_donor,
            "targetPrice": target_exit,
            "ts_high": round(self.live_price, 2),
            "ts_low": 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.active_positions.append(pos)
        self.trigger_copy_buy("VELOCITY_DCA", self.live_price)
        t_record = {
            "orderId": pos_id,
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_bought, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": cur_rnd,
            "execType": "WHALE_MAKER_MATCHED",
            "orderflowRatio": self.whale_orderflow_ratio,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.spot_trades_history.insert(0, t_record)
        self.latest_signal = {
            "action": "BUY",
            "price": round(self.live_price, 2),
            "text": f"BUY SOL NOW @ ${round(self.live_price, 2)} (Whale Rebound Confirmed)"
        }
        asyncio.create_task(self.db_save_buy(pos, {
            "order_id": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_bought, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": cur_rnd,
            "exec_type": "WHALE_MAKER_MATCHED"
        }))
        self.ts_high = round(self.live_price, 2)
        self.ts_low = 0.0
        self.ts_stage = "1.0%"
        self.tb_active = False
        self.initial_tb_active = False

    def execute_manual_buy(self, amount_usdt=50.0, order_type="MARKET", limit_price=0.0):
        target_price = self.live_price if order_type == "MARKET" or limit_price <= 0 else limit_price
        if amount_usdt <= 0 or target_price <= 0:
            return
        if self.manual_test_balance < amount_usdt:
            amount_usdt = self.manual_test_balance
        if amount_usdt <= 0:
            return
        fee = amount_usdt * self.taker_fee_pct
        net_invest = amount_usdt - fee
        sol_bought = net_invest / target_price
        self.manual_test_balance -= amount_usdt
        pos_id = "MAN_" + str(uuid.uuid4())[:6]
        manual_pos = {
            "id": pos_id,
            "round": 0,
            "subTrade": 0,
            "label": f"WALLET {order_type} BUY",
            "side": "BUY",
            "entryPrice": round(target_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(amount_usdt, 2),
            "orderType": order_type,
            "isManualWallet": True,
            "status": "FILLED",
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.wallet_active_positions.insert(0, manual_pos)
        t_record = {
            "orderId": pos_id,
            "side": "BUY",
            "price": round(target_price, 2),
            "solAmount": round(sol_bought, 4),
            "invested": round(amount_usdt, 2),
            "fee": round(fee, 4),
            "profit": 0.0,
            "execType": f"{order_type}_BUY_FILLED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.manual_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(manual_pos, t_record))
        asyncio.create_task(self.db_sync_state())
        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

    def trigger_copy_buy(self, bot_type, buy_price):
        if not hasattr(self, "copy_subscribers") or not self.copy_subscribers or buy_price <= 0:
            return
        for sub in list(self.copy_subscribers):
            if sub.get("botType") == bot_type:
                slot_size = float(sub.get("slotSize", 0.0))
                reserve = float(sub.get("availableReserve", 0.0))
                positions = sub.get("activePositions", [])
                max_slots = int(sub.get("slotsAllowed", 10))
                if slot_size >= 10.0 and reserve >= slot_size and len(positions) < max_slots:
                    fee = slot_size * self.taker_fee_pct
                    sol_qty = (slot_size - fee) / buy_price
                    pos_id = "CPOS_" + str(uuid.uuid4())[:6]
                    pos_item = {
                        "posId": pos_id,
                        "entryPrice": round(buy_price, 2),
                        "invested": round(slot_size, 2),
                        "solAmount": round(sol_qty, 4),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    positions.append(pos_item)
                    sub["activePositions"] = positions
                    sub["availableReserve"] = round(reserve - slot_size, 2)
                    sub["activeSlots"] = len(positions)
                    t_buy = {
                        "orderId": pos_id,
                        "side": "BUY",
                        "price": round(buy_price, 2),
                        "solAmount": round(sol_qty, 4),
                        "invested": round(slot_size, 2),
                        "fee": round(fee, 4),
                        "profit": 0.0,
                        "execType": f"COPY_{bot_type}_DIP_BUY",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.manual_trades_history.insert(0, t_buy)
                    c_pos_record = {
                        "id": pos_id,
                        "round": 0,
                        "subTrade": 0,
                        "label": f"CPOS|{sub.get('id')}|{bot_type}",
                        "entryPrice": round(buy_price, 2),
                        "solAmount": round(sol_qty, 4),
                        "invested": round(slot_size, 2),
                        "isMacro": False,
                        "targetPrice": 0.0
                    }
                    asyncio.create_task(self.db_save_buy(c_pos_record, t_buy))
                    asyncio.create_task(self.db_sync_state())

    def distribute_copy_profit(self, bot_type, profit_pct, exit_price):
        if not hasattr(self, "copy_subscribers") or not self.copy_subscribers or exit_price <= 0:
            return
        for sub in list(self.copy_subscribers):
            if sub.get("botType") == bot_type:
                positions = sub.get("activePositions", [])
                if not positions:
                    continue
                pos_to_close = positions.pop(0)
                sub["activePositions"] = positions
                sub["activeSlots"] = len(positions)
                invested = float(pos_to_close.get("invested", 10.0))
                sol_amt = float(pos_to_close.get("solAmount", 0.0))
                gross = sol_amt * exit_price
                fee = gross * self.taker_fee_pct
                net_ret = gross - fee
                profit = round(net_ret - invested, 4)
                sub["availableReserve"] = round(float(sub.get("availableReserve", 0.0)) + invested, 2)
                sub["realizedPnl"] = round(float(sub.get("realizedPnl", 0.0)) + profit, 4)
                self.manual_test_balance = round(self.manual_test_balance + profit, 2)
                self.manual_realized_pnl = round(self.manual_realized_pnl + profit, 4)
                t_rec = {
                    "orderId": "COPY_EXIT_" + str(uuid.uuid4())[:6],
                    "side": "SELL",
                    "price": round(exit_price, 2),
                    "solAmount": round(sol_amt, 4),
                    "fee": round(fee, 4),
                    "profit": profit,
                    "realizedPnl": profit,
                    "execType": f"COPY_{bot_type}_PROFIT",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                self.manual_trades_history.insert(0, t_rec)
                upd_label = f"COPY|{bot_type}|{sub.get('slotsAllowed', 1)}|{sub['realizedPnl']}"
                asyncio.create_task(self.db_save_buy({
                    "id": sub.get("id"),
                    "round": 0,
                    "subTrade": 0,
                    "label": upd_label,
                    "entryPrice": float(sub.get("entryPrice", exit_price)),
                    "solAmount": 0.0,
                    "invested": float(sub.get("totalCapital", 10.0)),
                    "isMacro": False,
                    "targetPrice": 0.0
                }, t_rec))
                if pos_to_close.get("posId"):
                    asyncio.create_task(self.db_save_sell_individual(pos_to_close.get("posId"), t_rec))
                else:
                    asyncio.create_task(self.db_save_engine_trade(t_rec))
                asyncio.create_task(self.db_sync_state())

    def execute_manual_sell(self, pos_id=None, sell_amount_sol=0.0):
        if len(self.wallet_active_positions) == 0 or self.live_price <= 0:
            return

        target_positions = []
        if pos_id:
            for p in list(self.wallet_active_positions):
                if p.get("id") == pos_id:
                    target_positions.append(p)
                    break
        else:
            target_positions = [p for p in list(self.wallet_active_positions) if p.get("solAmount", 0) > 0]

        if len(target_positions) == 0:
            return

        total_sol = sum(p.get("solAmount", 0.0) for p in target_positions)
        total_invested = sum(p.get("invested", 0.0) for p in target_positions)

        if sell_amount_sol > 0 and sell_amount_sol < total_sol:
            sold_sol = sell_amount_sol
            cost_basis = total_invested * (sold_sol / total_sol)
        else:
            sold_sol = total_sol
            cost_basis = total_invested

        if sold_sol <= 0:
            return

        gross_value = sold_sol * self.live_price
        fee = gross_value * self.taker_fee_pct
        net_value = gross_value - fee
        user_net_profit = round(net_value - cost_basis, 4)

        self.manual_realized_pnl = round(self.manual_realized_pnl + user_net_profit, 4)
        w_pos_inv = sum(float(p.get("invested", 0.0)) for p in self.wallet_active_positions if p.get("id") != pos_id)
        w_ord_inv = sum(float(o.get("invested", o.get("amount", 0.0))) for o in self.wallet_open_orders if o.get("side") == "BUY")
        self.manual_test_balance = max(0.0, round(100.0 + self.manual_realized_pnl - w_pos_inv - w_ord_inv, 2))

        if pos_id:
            self.wallet_active_positions = [p for p in self.wallet_active_positions if p.get("id") != pos_id]
        elif sold_sol >= total_sol:
            self.wallet_active_positions.clear()
        else:
            rem_sol = round(total_sol - sold_sol, 4)
            rem_inv = round(total_invested - cost_basis, 2)
            self.wallet_active_positions.clear()
            if rem_sol > 0:
                self.wallet_active_positions.append({
                    "id": "MAN_" + str(uuid.uuid4())[:6],
                    "round": 0,
                    "subTrade": 0,
                    "label": "WALLET REMAINING HOLDING",
                    "side": "BUY",
                    "entryPrice": round(rem_inv / rem_sol, 2) if rem_sol > 0 else round(self.live_price, 2),
                    "solAmount": rem_sol,
                    "invested": rem_inv,
                    "orderType": "MARKET",
                    "isManualWallet": True,
                    "status": "FILLED",
                    "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                })

        t_record = {
            "orderId": "MAN_S_" + (str(pos_id) if pos_id else str(uuid.uuid4())[:6]),
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sold_sol, 4),
            "fee": round(fee, 4),
            "profit": round(user_net_profit, 4),
            "realizedPnl": round(user_net_profit, 4),
            "execType": "MARKET_SELL_FILLED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.manual_trades_history.insert(0, t_record)
        if pos_id:
            asyncio.create_task(self.db_save_sell_individual(pos_id, t_record))
        else:
            for p in target_positions:
                asyncio.create_task(self.db_save_sell_individual(p.get("id"), t_record))
        asyncio.create_task(self.db_sync_state())
        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

    async def create_advanced_order(self, ord_data):
        pos_id = ord_data.get("posId") or ord_data.get("id")
        action = ord_data.get("action", "")

        if action == "CANCEL_ORDER" or ord_data.get("cancel"):
            if pos_id and str(pos_id).startswith("ATL_"):
                self.cancel_auto_loop_slot(pos_id)
                return
            if pos_id == "ALL":
                self.cancel_auto_loop_slot("ALL")
                for p in self.wallet_open_orders:
                    if p.get("side") == "BUY":
                        self.manual_test_balance += p.get("invested", p.get("amount", 0.0))
                self.wallet_open_orders.clear()
                return
            for p in list(self.wallet_open_orders):
                if p.get("id") == pos_id:
                    if p.get("side") == "BUY":
                        self.manual_test_balance += p.get("invested", p.get("amount", 0.0))
                    else:
                        r_sol = float(p.get("solAmount", 0.0))
                        r_inv = float(p.get("invested", 0.0))
                        if r_sol > 0:
                            revert_pos = {
                                "id": "MAN_" + str(uuid.uuid4())[:6],
                                "round": 0,
                                "subTrade": 0,
                                "label": "WALLET REVERTED HOLDING",
                                "side": "BUY",
                                "entryPrice": round(r_inv / r_sol, 2) if r_sol > 0 else round(self.live_price, 2),
                                "solAmount": r_sol,
                                "invested": r_inv,
                                "orderType": "MARKET",
                                "isManualWallet": True,
                                "status": "FILLED",
                                "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                            }
                            self.wallet_active_positions.append(revert_pos)
                            asyncio.create_task(self.db_save_buy(revert_pos, {"order_id": revert_pos["id"], "side": "BUY", "price": revert_pos["entryPrice"], "sol_amount": r_sol, "fee": 0.0, "profit": 0.0, "exec_type": "CANCEL_REVERT"}))
                    self.wallet_open_orders.remove(p)
                    asyncio.create_task(self.db_save_sell_individual(pos_id, {"order_id": pos_id + "_CANCEL", "side": "CANCEL", "price": 0.0, "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "CANCELLED"}))
                    asyncio.create_task(self.db_sync_state())
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                    return
            return

        if pos_id:
            if str(pos_id).startswith("ATL_"):
                for loop in list(self.auto_loops):
                    if loop.get("id") == pos_id:
                        sold_sol = float(loop.get("solBought", 0.0))
                        inv_amt = float(loop.get("usdtAmount", 0.0))
                        if sold_sol > 0:
                            gross = sold_sol * self.live_price
                            fee = gross * self.taker_fee_pct
                            net_ret = gross - fee
                            pnl = round(net_ret - inv_amt, 4)
                            self.manual_test_balance = round(self.manual_test_balance + net_ret, 2)
                            self.manual_realized_pnl = round(self.manual_realized_pnl + pnl, 4)
                            t_rec = {
                                "orderId": str(pos_id) + "_MC",
                                "side": "SELL",
                                "price": round(self.live_price, 2),
                                "solAmount": round(sold_sol, 4),
                                "fee": round(fee, 4),
                                "profit": pnl,
                                "realizedPnl": pnl,
                                "execType": "AUTO_LOOP_MARKET_CLOSE",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            self.manual_trades_history.insert(0, t_rec)
                            asyncio.create_task(self.db_save_sell_individual(pos_id, t_rec))
                        else:
                            self.manual_test_balance = round(self.manual_test_balance + inv_amt, 2)
                            asyncio.create_task(self.db_save_sell_individual(pos_id, {
                                "order_id": str(pos_id) + "_CANCEL",
                                "side": "CANCEL",
                                "price": round(self.live_price, 2),
                                "sol_amount": 0.0,
                                "fee": 0.0,
                                "profit": 0.0,
                                "round": 0,
                                "exec_type": "AUTO_LOOP_CANCELED"
                            }))
                        self.auto_loops.remove(loop)
                        await self.db_sync_state()
                        await manager.broadcast(json.dumps(self.get_state()))
                        return
            for p in list(self.wallet_active_positions):
                if p.get("id") == pos_id:
                    self.execute_manual_sell(pos_id=pos_id)
                    return
            for p in list(self.wallet_open_orders):
                if p.get("id") == pos_id:
                    self.wallet_open_orders.remove(p)
                    return
            return

        o_type = str(ord_data.get("orderType", "MARKET")).upper().replace(" ", "_")
        side = str(ord_data.get("side", "BUY")).upper()
        amt = float(ord_data.get("amount", 0.0))
        price = float(ord_data.get("price", 0.0))
        cb_pct = float(ord_data.get("callbackPct", 1.0))
        o_id = ord_data.get("orderId") or ("ORD_" + str(uuid.uuid4())[:6])

        if o_type == "MARKET":
            if side == "BUY":
                self.execute_manual_buy(amt, "MARKET", self.live_price)
            else:
                self.execute_manual_sell(pos_id=None, sell_amount_sol=amt)
            return

        exact_order_price = round(price, 2)
        if side == "BUY":
            if self.manual_test_balance < amt or amt <= 0 or exact_order_price <= 0:
                return
            self.manual_test_balance = round(self.manual_test_balance - amt, 2)
            sol_qty = round(amt / exact_order_price, 4)
            inv_amt = amt
        else:
            sol_qty = float(ord_data.get("solQuantity", 0.0))
            if sol_qty <= 0:
                sol_qty = amt
            total_avail_sol = sum(float(p.get("solAmount", 0.0)) for p in self.wallet_active_positions)
            if sol_qty <= 0 or total_avail_sol <= 0:
                return
            if round(sol_qty, 4) > round(total_avail_sol, 4):
                sol_qty = round(total_avail_sol, 4)
            rem_to_lock = sol_qty
            actual_cost_basis = 0.0
            for p in list(self.wallet_active_positions):
                p_sol = float(p.get("solAmount", 0.0))
                p_inv = float(p.get("invested", 0.0))
                if p_sol <= rem_to_lock:
                    rem_to_lock -= p_sol
                    actual_cost_basis += p_inv
                    self.wallet_active_positions.remove(p)
                    asyncio.create_task(self.db_save_sell_individual(p.get("id"), {"order_id": o_id, "side": "LOCK", "price": exact_order_price, "sol_amount": p_sol, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "LOCKED_FOR_SELL"}))
                else:
                    ratio = rem_to_lock / p_sol
                    part_inv = round(p_inv * ratio, 2)
                    actual_cost_basis += part_inv
                    p["solAmount"] = round(p_sol - rem_to_lock, 4)
                    p["invested"] = round(p_inv - part_inv, 2)
                    rem_to_lock = 0.0
                if rem_to_lock <= 0:
                    break
            inv_amt = round(actual_cost_basis, 2)

        initial_cur_p = round(self.live_price, 2)
        user_target_p = float(ord_data.get("price", exact_order_price))
        trig_target_p = float(ord_data.get("stopPrice", 0.0))
        exec_limit_p = float(ord_data.get("limitPrice", exact_order_price))
        trig_dir = "BELOW" if trig_target_p <= initial_cur_p else "ABOVE"

        order_obj = {
            "id": o_id,
            "orderId": o_id,
            "orderType": o_type,
            "side": side,
            "amount": float(inv_amt) if side == "BUY" else float(sol_qty),
            "solAmount": round(float(sol_qty), 4),
            "invested": round(float(inv_amt), 2),
            "price": exact_order_price,
            "entryPrice": exact_order_price,
            "activationPrice": user_target_p if o_type in ["TRAILING_STOP", "TRAILING"] else initial_cur_p,
            "isActivated": False,
            "stopPrice": trig_target_p,
            "limitPrice": exec_limit_p,
            "triggerDirection": trig_dir,
            "callbackPct": cb_pct,
            "peakTracked": user_target_p,
            "lowestTracked": user_target_p,
            "status": "OPEN",
            "statusText": f"{o_type} {side} @ ${exact_order_price}",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }

        self.wallet_open_orders.insert(0, order_obj)
        lbl_meta = f"ORD|{o_type}|{side}|{cb_pct}|{user_target_p}|{trig_target_p}"
        pos_ord_record = {
            "id": o_id,
            "round": 0,
            "subTrade": 0,
            "label": lbl_meta,
            "entryPrice": exact_order_price,
            "solAmount": float(sol_qty),
            "invested": float(inv_amt),
            "isMacro": False,
            "targetPrice": trig_target_p if trig_target_p > 0 else exact_order_price
        }
        asyncio.create_task(self.db_save_buy(pos_ord_record, {
            "order_id": o_id,
            "side": side,
            "price": exact_order_price,
            "sol_amount": float(sol_qty),
            "fee": 0.0,
            "profit": 0.0,
            "round": 0,
            "exec_type": f"OPEN_{o_type}"
        }))
        await self.db_sync_state()
        await manager.broadcast(json.dumps(self.get_state()))

    def create_auto_loop_order(self, usdt_amt, buy_trigger, buy_cb, sell_trigger, sell_cb, auto_repeat=True, slot_id=None):
        if usdt_amt <= 0 or buy_trigger <= 0 or sell_trigger <= 0:
            return
        if len(self.auto_loops) >= 10 and not slot_id:
            return

        if slot_id:
            for loop in self.auto_loops:
                if loop["id"] == slot_id:
                    loop["buyTrigger"] = float(buy_trigger)
                    loop["buyCallbackPct"] = float(buy_cb)
                    loop["sellTrigger"] = float(sell_trigger)
                    loop["sellCallbackPct"] = float(sell_cb)
                    loop["autoRepeat"] = bool(auto_repeat)
                    return

        if round(self.manual_test_balance, 2) < round(usdt_amt, 2):
            return

        usdt_amt = round(min(self.manual_test_balance, usdt_amt), 2)
        self.manual_test_balance = round(self.manual_test_balance - usdt_amt, 2)
        loop_id = str(slot_id) if slot_id else ("ATL_" + str(uuid.uuid4())[:6])
        rep_val = "1" if auto_repeat else "0"
        lbl_meta = f"ATL|{buy_cb}|{sell_cb}|{rep_val}|WAITING_BUY_TRIGGER|{buy_trigger}|{sell_trigger}|0.0"
        new_loop = {
            "id": loop_id,
            "usdtAmount": float(usdt_amt),
            "buyTrigger": float(buy_trigger),
            "buyCallbackPct": float(buy_cb),
            "sellTrigger": float(sell_trigger),
            "sellCallbackPct": float(sell_cb),
            "autoRepeat": bool(auto_repeat),
            "stage": "WAITING_BUY_TRIGGER",
            "solBought": 0.0,
            "buyExecutedPrice": 0.0,
            "lowestTracked": 0.0,
            "peakTracked": float(sell_trigger),
            "profitRealized": 0.0,
            "status": "ARMED (WAITING BUY)"
        }
        self.auto_loops.append(new_loop)
        pos_record = {
            "id": loop_id,
            "round": 0,
            "subTrade": 0,
            "label": lbl_meta,
            "entryPrice": float(buy_trigger),
            "solAmount": 0.0,
            "invested": float(usdt_amt),
            "isMacro": False,
            "targetPrice": float(sell_trigger)
        }
        asyncio.create_task(self.db_save_buy(pos_record, {
            "order_id": loop_id,
            "side": "AUTO_LOOP_OPEN",
            "price": buy_trigger,
            "sol_amount": 0.0,
            "fee": 0.0,
            "profit": 0.0,
            "round": 0,
            "exec_type": "OPEN_LOOP_PENDING"
        }))
        asyncio.create_task(self.db_sync_state())
        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
        asyncio.create_task(self.db_sync_state())

    def cancel_auto_loop_slot(self, slot_id):
        for loop in list(self.auto_loops):
            if loop["id"] == slot_id or slot_id == "ALL":
                target_id = loop["id"]
                if loop.get("solBought", 0.0) <= 0:
                    self.manual_test_balance += loop.get("usdtAmount", 0.0)
                else:
                    gross = loop["solBought"] * self.live_price
                    self.manual_test_balance += gross
                self.auto_loops.remove(loop)
                asyncio.create_task(self.db_save_sell_individual(target_id, {
                    "order_id": target_id + "_CANCEL",
                    "side": "CANCEL",
                    "price": round(self.live_price, 2),
                    "sol_amount": 0.0,
                    "fee": 0.0,
                    "profit": 0.0,
                    "round": 0,
                    "exec_type": "AUTO_LOOP_CANCELED"
                }))
        asyncio.create_task(self.db_sync_state())

    def run_auto_trailing_loop_tick(self):
        if not self.auto_loops or self.live_price <= 0:
            return

        for ord in list(self.auto_loops):
            stg = ord.get("stage", "WAITING_BUY_TRIGGER")

            if stg == "WAITING_BUY_TRIGGER":
                if self.live_price <= ord["buyTrigger"]:
                    ord["stage"] = "TRAILING_BUY"
                    ord["lowestTracked"] = self.live_price
                    ord["status"] = f"TRAILING DIP (LOW: ${round(self.live_price, 2)})"
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

            elif stg == "TRAILING_BUY":
                if "lowestTracked" not in ord or ord["lowestTracked"] <= 0 or self.live_price < ord["lowestTracked"]:
                    ord["lowestTracked"] = self.live_price
                if self.live_price > ord["buyTrigger"]:
                    ord["stage"] = "WAITING_BUY_TRIGGER"
                    ord["lowestTracked"] = 0.0
                    ord["status"] = f"ARMED (WAITING BUY @ ${round(ord['buyTrigger'], 2)})"
                    continue
                cb_pct = float(ord.get("buyCallbackPct", 0.01))
                cb_target = ord["lowestTracked"] * (1.0 + (cb_pct / 100.0))
                if self.live_price >= cb_target and self.live_price <= ord["buyTrigger"]:
                    invest_amt = float(ord["usdtAmount"])
                    fee = invest_amt * self.taker_fee_pct
                    sol_qty = (invest_amt - fee) / self.live_price
                    ord["solBought"] = sol_qty
                    ord["buyExecutedPrice"] = self.live_price
                    ord["stage"] = "WAITING_SELL_TRIGGER"
                    ord["peakTracked"] = float(ord["sellTrigger"])
                    ord["status"] = f"BOUGHT @ ${round(self.live_price, 2)} - TARGET ${round(ord['sellTrigger'], 2)}"
                    rep_flag = "1" if ord.get("autoRepeat", True) else "0"
                    upd_label = f"ATL|{ord['buyCallbackPct']}|{ord['sellCallbackPct']}|{rep_flag}|WAITING_SELL_TRIGGER|{ord['buyTrigger']}|{ord['sellTrigger']}|0.0"
                    t_rec = {
                        "orderId": ord["id"] + "_B",
                        "side": "AUTO_LOOP_BUY",
                        "price": round(self.live_price, 2),
                        "solAmount": round(sol_qty, 4),
                        "fee": round(fee, 4),
                        "profit": 0.0,
                        "execType": "AUTO_TRAILING_LOOP",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.manual_trades_history.insert(0, t_rec)
                    asyncio.create_task(self.db_save_buy({
                        "id": ord["id"],
                        "round": 0,
                        "subTrade": 0,
                        "label": upd_label,
                        "entryPrice": round(self.live_price, 2),
                        "solAmount": round(sol_qty, 4),
                        "invested": round(invest_amt, 2),
                        "isMacro": False,
                        "targetPrice": float(ord["sellTrigger"])
                    }, t_rec))
                    asyncio.create_task(self.db_sync_state())
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

            elif stg == "WAITING_SELL_TRIGGER":
                if self.live_price >= ord["sellTrigger"]:
                    ord["stage"] = "TRAILING_SELL"
                    ord["peakTracked"] = self.live_price
                    ord["status"] = f"TRAILING PROFIT (HIGH: ${round(self.live_price, 2)})"
                    rep_flag = "1" if ord.get("autoRepeat", True) else "0"
                    upd_label = f"ATL|{ord['buyCallbackPct']}|{ord['sellCallbackPct']}|{rep_flag}|TRAILING_SELL|{ord['buyTrigger']}|{ord['sellTrigger']}|{self.live_price}"
                    asyncio.create_task(self.db_save_buy({
                        "id": ord["id"],
                        "round": 0,
                        "subTrade": 0,
                        "label": upd_label,
                        "entryPrice": float(ord.get("buyExecutedPrice", ord["sellTrigger"])),
                        "solAmount": float(ord.get("solBought", 0.0)),
                        "invested": float(ord.get("usdtAmount", 0.0)),
                        "isMacro": False,
                        "targetPrice": float(ord["sellTrigger"])
                    }, {"order_id": ord["id"] + "_TRL", "side": "TRAIL", "price": round(self.live_price, 2), "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "TRAIL"}))
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

            elif stg == "TRAILING_SELL":
                if self.live_price > ord.get("peakTracked", self.live_price):
                    ord["peakTracked"] = self.live_price

                s_cb_pct = float(ord.get("sellCallbackPct", 0.01))
                pullback_trigger = ord["peakTracked"] * (1.0 - (s_cb_pct / 100.0))

                if self.live_price <= pullback_trigger and self.live_price >= (ord["sellTrigger"] * 0.998):
                    sold_sol = float(ord["solBought"])
                    if sold_sol <= 0:
                        continue
                    gross = sold_sol * self.live_price
                    fee = gross * self.taker_fee_pct
                    net_ret = gross - fee
                    profit = round(net_ret - ord["usdtAmount"], 4)
                    self.manual_realized_pnl = round(self.manual_realized_pnl + profit, 4)
                    self.manual_test_balance = round(self.manual_test_balance + net_ret, 2)
                    ord["profitRealized"] = profit

                    t_rec = {
                        "orderId": ord["id"] + "_S",
                        "side": "SELL",
                        "price": round(self.live_price, 2),
                        "solAmount": round(sold_sol, 4),
                        "fee": round(fee, 4),
                        "profit": profit,
                        "realizedPnl": profit,
                        "execType": "AUTO_TRAILING_LOOP_EXIT",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.manual_trades_history.insert(0, t_rec)
                    if not ord.get("autoRepeat", True):
                        asyncio.create_task(self.db_save_sell_individual(ord["id"], t_rec))
                    else:
                        asyncio.create_task(self.db_save_engine_trade(t_rec))

                    if ord.get("autoRepeat", True):
                        rearm_amt = min(float(ord["usdtAmount"]), float(self.manual_test_balance))
                        if rearm_amt >= 5.0:
                            ord["usdtAmount"] = round(rearm_amt, 2)
                            self.manual_test_balance = round(self.manual_test_balance - rearm_amt, 2)
                            ord["stage"] = "WAITING_BUY_TRIGGER"
                            ord["solBought"] = 0.0
                            ord["buyExecutedPrice"] = 0.0
                            ord["lowestTracked"] = 0.0
                            ord["peakTracked"] = float(ord["sellTrigger"])
                            ord["status"] = f"LOOP REARMED (WAITING BUY @ ${round(ord['buyTrigger'], 2)})"
                            rep_flag = "1"
                            upd_label = f"ATL|{ord['buyCallbackPct']}|{ord['sellCallbackPct']}|{rep_flag}|WAITING_BUY_TRIGGER|{ord['buyTrigger']}|{ord['sellTrigger']}|0.0"
                            asyncio.create_task(self.db_save_buy({
                                "id": ord["id"],
                                "round": 0,
                                "subTrade": 0,
                                "label": upd_label,
                                "entryPrice": float(ord["buyTrigger"]),
                                "solAmount": 0.0,
                                "invested": float(ord["usdtAmount"]),
                                "isMacro": False,
                                "targetPrice": float(ord["sellTrigger"])
                            }, {
                                "order_id": ord["id"] + "_REARM",
                                "side": "REARM",
                                "price": float(ord["buyTrigger"]),
                                "sol_amount": 0.0,
                                "fee": 0.0,
                                "profit": 0.0,
                                "round": 0,
                                "exec_type": "LOOP_REARMED"
                            }))
                            asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                        else:
                            if ord in self.auto_loops:
                                self.auto_loops.remove(ord)
                            asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                    else:
                        if ord in self.auto_loops:
                            self.auto_loops.remove(ord)
                        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

                    asyncio.create_task(self.db_sync_state())

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
        t_record = {
            "orderId": str(uuid.uuid4())[:8],
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(self.macro_vault_sol, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.active_positions = [p for p in self.active_positions if not p.get("isMacro", False)]
        self.macro_vault_sol = 0.0
        self.macro_vault_invested = 0.0
        self.macro_vault_entry = 0.0
        self.macro_ts_high = 0.0
        self.macro_ts_low = 0.0
        asyncio.create_task(self.db_sync_state())

    def execute_sell_individual(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        sold_value = sol_amt * self.live_price
        fee = sold_value * self.taker_fee_pct
        net_return = sold_value - fee
        profit = net_return - invested
        if not force and profit < self.min_net_profit_usdt:
            return

        r_num = pos.get("round", self.active_round)
        borrowed_donor = pos.get("borrowedFrom", 0)

        if borrowed_donor > 0:
            self.home_round_spent[borrowed_donor] = max(0.0, round(self.home_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.home_round_borrowed[r_num] = max(0.0, round(self.home_round_borrowed.get(r_num, 0.0) - invested, 2))
        else:
            self.home_round_spent[r_num] = max(0.0, round(self.home_round_spent.get(r_num, 0.0) - invested, 2))

        if r_num == 8 and borrowed_donor > 0:
            self.macro_profit_vault = round(self.macro_profit_vault + profit, 4)

        self.usdt_balance += net_return
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.spot_realized_pnl = round(self.spot_realized_pnl + profit, 4)
        self.sol_balance = max(0.0, self.sol_balance - sol_amt)
        self.invested_amount = max(0.0, self.invested_amount - invested)
        self.avg_entry_price = self.invested_amount / self.sol_balance if self.sol_balance > 0 else 0.0

        if self.round_trades_done.get(r_num, 0) > 0:
            self.round_trades_done[r_num] -= 1
        self.sub_trade_count = len([p for p in self.active_positions if not p.get("isMacro", False) and p["id"] != pos_id])
        self.active_positions = [p for p in self.active_positions if p["id"] != pos_id]

        trade_record = {
            "orderId": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": r_num,
            "execType": "SPOT_DCA_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        self.spot_trades_history.insert(0, trade_record)
        p_pct = (profit / invested) * 100.0 if invested > 0 else 0.0
        self.distribute_copy_profit("VELOCITY_DCA", p_pct, self.live_price)
        asyncio.create_task(self.db_save_sell_individual(pos_id, {
            "order_id": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": r_num,
            "exec_type": "INDIVIDUAL_PROFIT_EXIT"
        }))
        asyncio.create_task(self.db_sync_state())
        if not self.is_paused and len(self.active_positions) == 0 and self.total_user_capital >= 40.0 and self.usdt_balance >= 10.0:
            self.execute_buy(is_sub_trade=False)

    def execute_hyper_buy(self):
        if self.is_paused or self.total_user_capital < 500.0 or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return

        self.sync_phase_and_round()
        h_round = self.active_round
        cfg = self.get_tier_config()
        max_allowed_slots = cfg["slots"]

        if self.hyper_round_trades_done.get(h_round, 0) >= max_allowed_slots:
            return

        total_pool_budget = cfg["net_fund"]
        target_size = min(self.usdt_balance, max(10.0, cfg["size"]))
        borrowed_donor = 0
        is_macro_hold = False
        allowed, borrowed_donor = self.allocate_round_budget(self.hyper_round_spent, self.hyper_round_borrowed, h_round, target_size, total_pool_budget)
        if not allowed:
            return

        fee = target_size * self.taker_fee_pct
        net_invest = target_size - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance = round(self.usdt_balance - target_size, 2)
        self.hyper_pool_balance = self.usdt_balance
        self.hyper_round_trades_done[h_round] = self.hyper_round_trades_done.get(h_round, 0) + 1
        pos_id = "HYPER_" + str(uuid.uuid4())[:6]

        if borrowed_donor > 0:
            lbl_text = f"HYPER TITAN R{h_round} (LOAN R{borrowed_donor} #{self.hyper_round_trades_done[h_round]})"
        else:
            lbl_text = f"HYPER TITAN R{h_round} (#{self.hyper_round_trades_done[h_round]})"

        pos = {
            "id": pos_id,
            "round": h_round,
            "subTrade": self.hyper_round_trades_done[h_round],
            "label": lbl_text,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(target_size, 2),
            "isMacro": is_macro_hold,
            "borrowedFrom": borrowed_donor,
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.hyper_positions.append(pos)
        self.hyper_last_ref_price = self.live_price
        self.hyper_tb_active = False
        self.hyper_tb_lowest = 0.0
        t_record = {
            "orderId": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": h_round,
            "execType": "HYPER_TITAN_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.hyper_trades_history.insert(0, t_record)
        self.scalp_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(pos, t_record))

    def execute_hyper_sell(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = float(pos["solAmount"])
        invested = float(pos["invested"])
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = round(net_return - invested, 4)
        if not force and profit < self.min_net_profit_usdt:
            return

        h_round = pos.get("round", 1)
        borrowed_donor = pos.get("borrowedFrom", 0)

        if borrowed_donor > 0:
            self.hyper_round_spent[borrowed_donor] = max(0.0, round(self.hyper_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.hyper_round_borrowed[h_round] = max(0.0, round(self.hyper_round_borrowed.get(h_round, 0.0) - invested, 2))
        else:
            self.hyper_round_spent[h_round] = max(0.0, round(self.hyper_round_spent.get(h_round, 0.0) - invested, 2))

        if h_round == 8 and borrowed_donor > 0:
            self.hyper_macro_profit_vault = round(self.hyper_macro_profit_vault + profit, 4)

        self.usdt_balance = round(self.usdt_balance + net_return, 2)
        self.hyper_pool_balance = self.usdt_balance
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.hyper_realized_pnl = round(self.hyper_realized_pnl + profit, 4)
        self.hyper_total_trades += 1

        if self.hyper_round_trades_done.get(h_round, 0) > 0:
            self.hyper_round_trades_done[h_round] -= 1
        self.hyper_positions = [p for p in self.hyper_positions if p["id"] != pos_id]
        self.hyper_last_ref_price = self.live_price
        trade_record = {
            "orderId": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": h_round,
            "execType": "HYPER_TITAN_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        self.hyper_trades_history.insert(0, trade_record)
        self.scalp_trades_history.insert(0, trade_record)
        asyncio.create_task(self.db_save_sell_individual(pos_id, trade_record))
        asyncio.create_task(self.db_sync_state())

    def run_hyper_titan_tick(self):
        if self.is_paused or self.total_user_capital < 500.0 or self.live_price <= 0:
            return

        if len(self.hyper_positions) == 0:
            if self.usdt_balance >= 10.0:
                self.execute_hyper_buy()
            return

        for pos in list(self.hyper_positions):
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_hyper_sell(pos)
                    continue

                if gain >= 0.70:
                    pullback = 0.12
                elif gain >= 0.40:
                    pullback = 0.08
                elif gain >= 0.20:
                    pullback = 0.05
                else:
                    pullback = 0.0
                if pullback > 0.0 and current_p <= (peak - pullback):
                    self.execute_hyper_sell(pos)

        if self.usdt_balance < 10.0 or len(self.hyper_positions) >= 24:
            self.hyper_tb_active = False
            return

        ref_p = min(float(p["entryPrice"]) for p in self.hyper_positions)
        self.hyper_last_ref_price = ref_p
        current_dip = ref_p - self.live_price
        req_h_dip = 1.20

        if current_dip >= req_h_dip:
            if not self.hyper_tb_active:
                self.hyper_tb_active = True
                self.hyper_tb_lowest = self.live_price
            else:
                if self.live_price < self.hyper_tb_lowest:
                    self.hyper_tb_lowest = self.live_price
                bounce_gap = 0.02
                if self.live_price >= (self.hyper_tb_lowest + bounce_gap):
                    self.hyper_tb_active = False
                    self.hyper_tb_lowest = 0.0
                    self.execute_hyper_buy()
        else:
            self.hyper_tb_active = False

    

    def get_scavenged_idle_fund(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return self.usdt_balance

    def get_micro_trade_size(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return round(self.usdt_balance / 10.0, 2)

    def execute_micro_buy(self):
        if self.is_paused or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return
        self.sync_phase_and_round()
        m_round = self.active_round
        cfg = self.get_tier_config()
        if self.total_user_capital < 10.0:
            return
        max_allowed_slots = cfg["slots"]

        if self.micro_round_trades_done.get(m_round, 0) >= max_allowed_slots:
            return

        total_pool_budget = cfg["net_fund"]
        target_size = min(self.usdt_balance, max(10.0, cfg["size"]))
        borrowed_donor = 0
        is_macro_hold = False
        allowed, borrowed_donor = self.allocate_round_budget(self.micro_round_spent, self.micro_round_borrowed, m_round, target_size, total_pool_budget)
        if not allowed:
            return

        invest_target = target_size

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance = round(self.usdt_balance - invest_target, 2)
        self.micro_round_trades_done[m_round] = self.micro_round_trades_done.get(m_round, 0) + 1
        pos_id = "M_" + str(uuid.uuid4())[:6]

        if borrowed_donor > 0:
            lbl_text = f"APEX VELOCITY R{m_round} (LOAN R{borrowed_donor} #{self.micro_round_trades_done[m_round]})"
        else:
            lbl_text = f"APEX VELOCITY R{m_round} (#{self.micro_round_trades_done[m_round]})"

        pos = {
            "id": pos_id,
            "round": m_round,
            "subTrade": self.micro_round_trades_done[m_round],
            "label": lbl_text,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(invest_target, 2),
            "isMacro": is_macro_hold,
            "borrowedFrom": borrowed_donor,
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.micro_positions.append(pos)
        self.trigger_copy_buy("APEX_SCALPER", self.live_price)
        self.micro_last_ref_price = self.live_price
        self.micro_tb_active = False
        self.micro_tb_lowest = 0.0
        t_record = {
            "orderId": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": m_round,
            "execType": "MICRO_SCALP_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.micro_trades_history.insert(0, t_record)
        self.scalp_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(pos, t_record))

    def execute_micro_sell(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if not force and profit < self.min_net_profit_usdt:
            return

        m_round = pos.get("round", 1)
        borrowed_donor = pos.get("borrowedFrom", 0)

        if borrowed_donor > 0:
            self.micro_round_spent[borrowed_donor] = max(0.0, round(self.micro_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.micro_round_borrowed[m_round] = max(0.0, round(self.micro_round_borrowed.get(m_round, 0.0) - invested, 2))
        else:
            self.micro_round_spent[m_round] = max(0.0, round(self.micro_round_spent.get(m_round, 0.0) - invested, 2))

        if m_round == 8 and borrowed_donor > 0:
            self.micro_macro_profit_vault = round(self.micro_macro_profit_vault + profit, 4)

        self.usdt_balance = round(self.usdt_balance + net_return, 2)
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.micro_realized_pnl = round(self.micro_realized_pnl + profit, 4)
        self.micro_total_trades += 1

        if self.micro_round_trades_done.get(m_round, 0) > 0:
            self.micro_round_trades_done[m_round] -= 1
        self.micro_positions = [p for p in self.micro_positions if p["id"] != pos_id]
        self.micro_last_ref_price = self.live_price
        m_pct = (profit / invested) * 100.0 if invested > 0 else 0.0
        self.distribute_copy_profit("APEX_SCALPER", m_pct, self.live_price)
        trade_record = {
            "orderId": pos_id + "_S",
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
        self.micro_trades_history.insert(0, trade_record)
        self.scalp_trades_history.insert(0, trade_record)
        asyncio.create_task(self.db_save_sell_individual(pos_id, {
            "order_id": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": m_round,
            "exec_type": "MICRO_SCALP_EXIT"
        }))
        asyncio.create_task(self.db_sync_state())

    def run_micro_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return

        if len(self.micro_positions) == 0:
            if self.usdt_balance >= 10.0:
                self.execute_micro_buy()
            return

        for pos in list(self.micro_positions):
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_micro_sell(pos)
                    continue

                if gain >= 0.80:
                    pullback = 0.15
                elif gain >= 0.55:
                    pullback = 0.12
                elif gain >= 0.35:
                    pullback = 0.08
                else:
                    pullback = 0.0
                if pullback > 0.0 and current_p <= (peak - pullback):
                    self.execute_micro_sell(pos)

        idle_fund = self.get_scavenged_idle_fund()
        fund = self.total_user_capital
        max_m_trades = 1 if fund < 20.0 else (2 if fund < 30.0 else (3 if fund < 80.0 else 24))
        if idle_fund < 10.0 or self.usdt_balance < 10.0 or len(self.micro_positions) >= max_m_trades:
            self.micro_tb_active = False
            return

        ref_p = min(float(p["entryPrice"]) for p in self.micro_positions)
        self.micro_last_ref_price = ref_p
        current_dip = ref_p - self.live_price
        req_m_dip = 0.15 if self.active_round == 7 else (0.20 if self.active_round == 6 else 0.30)

        if current_dip >= req_m_dip:
            if not self.micro_tb_active:
                self.micro_tb_active = True
                self.micro_tb_lowest = self.live_price
            else:
                if self.live_price < self.micro_tb_lowest:
                    self.micro_tb_lowest = self.live_price
                bounce_gap = 0.01
                if self.live_price >= (self.micro_tb_lowest + bounce_gap):
                    self.micro_tb_active = False
                    self.micro_tb_lowest = 0.0
                    self.execute_micro_buy()
        else:
            self.micro_tb_active = False

    def get_killer2_idle_fund(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return self.usdt_balance

    def get_killer2_trade_size(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return 10.0

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
        if self.is_paused or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return
        self.sync_phase_and_round()
        k_round = self.active_round
        cfg = self.get_tier_config()
        if self.total_user_capital < 60.0:
            return
        max_allowed_slots = cfg["slots"]

        if self.killer2_round_trades_done.get(k_round, 0) >= max_allowed_slots:
            return

        total_pool_budget = cfg["net_fund"]
        target_size = min(self.usdt_balance, max(10.0, cfg["size"]))
        borrowed_donor = 0
        is_macro_hold = False
        allowed, borrowed_donor = self.allocate_round_budget(self.killer2_round_spent, self.killer2_round_borrowed, k_round, target_size, total_pool_budget)
        if not allowed:
            return

        invest_target = target_size

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance = round(self.usdt_balance - invest_target, 2)
        self.killer2_round_trades_done[k_round] = self.killer2_round_trades_done.get(k_round, 0) + 1
        pos_id = "K2_" + str(uuid.uuid4())[:6]

        if borrowed_donor > 0:
            lbl_text = f"QUANTUM PULSE R{k_round} (LOAN R{borrowed_donor} #{self.killer2_round_trades_done[k_round]})"
        else:
            lbl_text = f"QUANTUM PULSE R{k_round} (#{self.killer2_round_trades_done[k_round]})"

        pos = {
            "id": pos_id,
            "round": k_round,
            "subTrade": self.killer2_round_trades_done[k_round],
            "label": lbl_text,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(invest_target, 2),
            "isMacro": is_macro_hold,
            "borrowedFrom": borrowed_donor,
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.killer2_positions.append(pos)
        self.trigger_copy_buy("QUANTUM_PULSE", self.live_price)
        self.killer2_last_ref_price = self.live_price
        self.killer2_tb_active = False
        self.killer2_tb_lowest = 0.0
        t_record = {
            "orderId": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": k_round,
            "execType": "KILLER2_SCALP_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.killer2_trades_history.insert(0, t_record)
        self.scalp_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(pos, t_record))

    def execute_killer2_sell(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if not force and profit < self.min_net_profit_usdt:
            return

        k_round = pos.get("round", 1)
        borrowed_donor = pos.get("borrowedFrom", 0)

        if borrowed_donor > 0:
            self.killer2_round_spent[borrowed_donor] = max(0.0, round(self.killer2_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.killer2_round_borrowed[k_round] = max(0.0, round(self.killer2_round_borrowed.get(k_round, 0.0) - invested, 2))
        else:
            self.killer2_round_spent[k_round] = max(0.0, round(self.killer2_round_spent.get(k_round, 0.0) - invested, 2))

        if k_round == 8 and borrowed_donor > 0:
            self.killer2_macro_profit_vault = round(self.killer2_macro_profit_vault + profit, 4)

        self.usdt_balance = round(self.usdt_balance + net_return, 2)
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.killer2_realized_pnl = round(self.killer2_realized_pnl + profit, 4)
        self.killer2_total_trades += 1

        if self.killer2_round_trades_done.get(k_round, 0) > 0:
            self.killer2_round_trades_done[k_round] -= 1
        self.killer2_positions = [p for p in self.killer2_positions if p["id"] != pos_id]
        self.killer2_last_ref_price = self.live_price
        k2_pct = (profit / invested) * 100.0 if invested > 0 else 0.0
        self.distribute_copy_profit("QUANTUM_PULSE", k2_pct, self.live_price)
        trade_record = {
            "orderId": pos_id + "_S",
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
        self.killer2_trades_history.insert(0, trade_record)
        self.scalp_trades_history.insert(0, trade_record)
        asyncio.create_task(self.db_save_sell_individual(pos_id, {
            "order_id": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": k_round,
            "exec_type": "KILLER2_SCALP_EXIT"
        }))
        asyncio.create_task(self.db_sync_state())

    def run_killer2_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return

        if len(self.killer2_positions) == 0:
            if self.usdt_balance >= 10.0:
                self.execute_killer2_buy()
            return

        for pos in list(self.killer2_positions):
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_killer2_sell(pos)
                    continue

                if gain >= 1.20:
                    pullback = 0.25
                elif gain >= 0.80:
                    pullback = 0.20
                elif gain >= 0.50:
                    pullback = 0.15
                else:
                    pullback = 0.0
                if pullback > 0.0 and current_p <= (peak - pullback):
                    self.execute_killer2_sell(pos)

        fund = self.total_user_capital
        max_k2_trades = 1 if fund < 70.0 else (2 if fund < 80.0 else 24)
        if self.usdt_balance < 10.0 or len(self.killer2_positions) >= max_k2_trades:
            self.killer2_tb_active = False
            return

        ref_p = min(float(p["entryPrice"]) for p in self.killer2_positions)
        self.killer2_last_ref_price = ref_p
        current_dip = ref_p - self.live_price
        req_k2_dip = 0.30 if self.active_round == 7 else (0.45 if self.active_round == 6 else 0.60)

        if current_dip >= req_k2_dip:
            if not self.killer2_tb_active:
                self.killer2_tb_active = True
                self.killer2_tb_lowest = self.live_price
            else:
                if self.live_price < self.killer2_tb_lowest:
                    self.killer2_tb_lowest = self.live_price
                bounce_gap = 0.02
                if self.live_price >= (self.killer2_tb_lowest + bounce_gap) or current_dip >= (req_k2_dip + 0.05):
                    self.killer2_tb_active = False
                    self.killer2_tb_lowest = 0.0
                    self.execute_killer2_buy()
        else:
            self.killer2_tb_active = False

    def get_killer3_idle_fund(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return self.usdt_balance

    def get_killer3_trade_size(self):
        if self.usdt_balance < 10.0:
            return 0.0
        return 10.0

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
        if self.is_paused or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return
        self.sync_phase_and_round()
        k_round = self.active_round
        cfg = self.get_tier_config()
        if self.total_user_capital < 80.0:
            return
        max_allowed_slots = cfg["slots"]

        if self.killer3_round_trades_done.get(k_round, 0) >= max_allowed_slots:
            return

        total_pool_budget = cfg["net_fund"]
        target_size = min(self.usdt_balance, max(10.0, cfg["size"]))
        borrowed_donor = 0
        is_macro_hold = False
        allowed, borrowed_donor = self.allocate_round_budget(self.killer3_round_spent, self.killer3_round_borrowed, k_round, target_size, total_pool_budget)
        if not allowed:
            return

        invest_target = target_size

        fee = invest_target * self.taker_fee_pct
        net_invest = invest_target - fee
        sol_amt = net_invest / self.live_price
        self.usdt_balance = round(self.usdt_balance - invest_target, 2)
        self.killer3_round_trades_done[k_round] = self.killer3_round_trades_done.get(k_round, 0) + 1
        pos_id = "K3_" + str(uuid.uuid4())[:6]

        if borrowed_donor > 0:
            lbl_text = f"TITAN ABYSS R{k_round} (LOAN R{borrowed_donor} #{self.killer3_round_trades_done[k_round]})"
        else:
            lbl_text = f"TITAN ABYSS R{k_round} (#{self.killer3_round_trades_done[k_round]})"

        pos = {
            "id": pos_id,
            "round": k_round,
            "subTrade": self.killer3_round_trades_done[k_round],
            "label": lbl_text,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(invest_target, 2),
            "isMacro": is_macro_hold,
            "borrowedFrom": borrowed_donor,
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }
        self.killer3_positions.append(pos)
        self.trigger_copy_buy("TITAN_ABYSS", self.live_price)
        self.killer3_last_ref_price = self.live_price
        self.killer3_tb_active = False
        self.killer3_tb_lowest = 0.0
        t_record = {
            "orderId": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": k_round,
            "execType": "KILLER3_SCALP_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.killer3_trades_history.insert(0, t_record)
        self.scalp_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(pos, t_record))

    def execute_killer3_sell(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = pos["solAmount"]
        invested = pos["invested"]
        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = net_return - invested
        if not force and profit < self.min_net_profit_usdt:
            return

        k_round = pos.get("round", 1)
        borrowed_donor = pos.get("borrowedFrom", 0)

        if borrowed_donor > 0:
            self.killer3_round_spent[borrowed_donor] = max(0.0, round(self.killer3_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.killer3_round_borrowed[k_round] = max(0.0, round(self.killer3_round_borrowed.get(k_round, 0.0) - invested, 2))
        else:
            self.killer3_round_spent[k_round] = max(0.0, round(self.killer3_round_spent.get(k_round, 0.0) - invested, 2))

        if k_round == 8 and borrowed_donor > 0:
            self.killer3_macro_profit_vault = round(self.killer3_macro_profit_vault + profit, 4)

        self.usdt_balance = round(self.usdt_balance + net_return, 2)
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.killer3_realized_pnl = round(self.killer3_realized_pnl + profit, 4)
        self.killer3_total_trades += 1

        if self.killer3_round_trades_done.get(k_round, 0) > 0:
            self.killer3_round_trades_done[k_round] -= 1
        self.killer3_positions = [p for p in self.killer3_positions if p["id"] != pos_id]
        self.killer3_last_ref_price = self.live_price
        k3_pct = (profit / invested) * 100.0 if invested > 0 else 0.0
        self.distribute_copy_profit("TITAN_ABYSS", k3_pct, self.live_price)
        trade_record = {
            "orderId": pos_id + "_S",
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
        self.killer3_trades_history.insert(0, trade_record)
        self.scalp_trades_history.insert(0, trade_record)
        asyncio.create_task(self.db_save_sell_individual(pos_id, {
            "order_id": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "sol_amount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "round": k_round,
            "exec_type": "KILLER3_SCALP_EXIT"
        }))
        asyncio.create_task(self.db_sync_state())

    def run_killer3_scalper_tick(self):
        if self.is_paused or self.live_price <= 0:
            return

        if len(self.killer3_positions) == 0:
            if self.usdt_balance >= 10.0:
                self.execute_killer3_buy()
            return

        for pos in list(self.killer3_positions):
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_killer3_sell(pos)
                    continue

                if gain >= 1.50:
                    pullback = 0.03
                elif gain >= 1.00:
                    pullback = round(peak * 0.005, 2)
                elif gain >= 0.60:
                    pullback = round(peak * 0.010, 2)
                else:
                    pullback = 0.0
                if pullback > 0.0 and current_p <= (peak - pullback):
                    self.execute_killer3_sell(pos)

        fund = self.total_user_capital
        max_k3_trades = 24 if fund >= 80.0 else 0
        if self.usdt_balance < 10.0 or len(self.killer3_positions) >= max_k3_trades:
            self.killer3_tb_active = False
            return

        ref_p = min(float(p["entryPrice"]) for p in self.killer3_positions)
        self.killer3_last_ref_price = ref_p
        current_dip = ref_p - self.live_price
        req_k3_dip = 0.50 if self.active_round == 7 else (0.70 if self.active_round == 6 else 0.90)

        if current_dip >= req_k3_dip:
            if not self.killer3_tb_active:
                self.killer3_tb_active = True
                self.killer3_tb_lowest = self.live_price
            else:
                if self.live_price < self.killer3_tb_lowest:
                    self.killer3_tb_lowest = self.live_price
                bounce_gap = 0.02
                if self.live_price >= (self.killer3_tb_lowest + bounce_gap) or current_dip >= (req_k3_dip + 0.05):
                    self.killer3_tb_active = False
                    self.killer3_tb_lowest = 0.0
                    self.execute_killer3_buy()
        else:
            self.killer3_tb_active = False

    def execute_singularity_buy(self, engine_idx=1):
        if self.is_paused or self.total_user_capital < 1000.0 or self.usdt_balance < 10.0 or self.live_price <= 0:
            return
        if self.active_round in [9, 10]:
            return

        self.sync_phase_and_round()
        cur_rnd = self.active_round
        cfg = self.get_tier_config()
        allowed_slots = cfg["slots"]

        if self.singularity_round_trades_done.get(cur_rnd, 0) >= allowed_slots:
            return

        total_pool_budget = cfg["net_fund"]
        target_size = min(self.usdt_balance, max(10.0, cfg["size"]))
        borrowed_donor_round = 0
        is_macro_vault_hold = False
        allowed, borrowed_donor_round = self.allocate_round_budget(self.singularity_round_spent, self.singularity_round_borrowed, cur_rnd, target_size, total_pool_budget)
        if not allowed:
            return

        fee = target_size * self.taker_fee_pct
        net_invest = target_size - fee
        sol_amt = net_invest / self.live_price

        self.usdt_balance = round(self.usdt_balance - target_size, 2)
        self.singularity_pool_balance = self.usdt_balance
        self.singularity_round_trades_done[cur_rnd] = self.singularity_round_trades_done.get(cur_rnd, 0) + 1
        trade_num = self.singularity_round_trades_done[cur_rnd]
        pos_id = "SNG_" + str(uuid.uuid4())[:6]

        if borrowed_donor_round > 0:
            pos_label = f"TITAN SINGULARITY R{cur_rnd} (LOAN R{borrowed_donor_round} #{trade_num})"
        else:
            pos_label = f"TITAN SINGULARITY R{cur_rnd} (#{trade_num})"

        pos = {
            "id": pos_id,
            "round": cur_rnd,
            "subTrade": trade_num,
            "label": pos_label,
            "entryPrice": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "invested": round(target_size, 2),
            "isMacro": is_macro_vault_hold,
            "targetPrice": 0.0,
            "borrowedFrom": borrowed_donor_round,
            "ts_high": round(self.live_price, 2),
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }

        self.singularity_positions.append(pos)
        self.singularity_last_ref_price = self.live_price
        self.singularity_tb_active = False
        self.singularity_tb_lowest = 0.0

        t_record = {
            "orderId": pos_id + "_B",
            "side": "BUY",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": 0.0,
            "round": cur_rnd,
            "execType": "SINGULARITY_SCALP_ENTRY",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, t_record)
        self.singularity_trades_history.insert(0, t_record)
        self.scalp_trades_history.insert(0, t_record)
        asyncio.create_task(self.db_save_buy(pos, t_record))

    def execute_singularity_sell(self, pos, force=False):
        pos_id = pos["id"]
        sol_amt = float(pos["solAmount"])
        invested = float(pos["invested"])
        r_num = pos.get("round", 1)
        borrowed_donor = pos.get("borrowedFrom", 0)

        gross_val = sol_amt * self.live_price
        fee = gross_val * self.taker_fee_pct
        net_return = gross_val - fee
        profit = round(net_return - invested, 4)
        if not force and profit < self.min_net_profit_usdt:
            return

        self.usdt_balance = round(self.usdt_balance + net_return, 2)
        self.singularity_pool_balance = self.usdt_balance
        self.realized_pnl = round(self.realized_pnl + profit, 4)
        self.singularity_realized_pnl = round(self.singularity_realized_pnl + profit, 4)
        self.singularity_total_trades += 1

        if self.singularity_round_trades_done.get(r_num, 0) > 0:
            self.singularity_round_trades_done[r_num] -= 1

        if borrowed_donor > 0:
            self.singularity_round_spent[borrowed_donor] = max(0.0, round(self.singularity_round_spent.get(borrowed_donor, 0.0) - invested, 2))
            self.singularity_round_borrowed[r_num] = max(0.0, round(self.singularity_round_borrowed.get(r_num, 0.0) - invested, 2))
        else:
            self.singularity_round_spent[r_num] = max(0.0, round(self.singularity_round_spent.get(r_num, 0.0) - invested, 2))

        if r_num == 8 and borrowed_donor > 0:
            self.singularity_macro_profit_vault = round(self.singularity_macro_profit_vault + profit, 4)

        self.singularity_positions = [p for p in self.singularity_positions if p["id"] != pos_id]
        self.singularity_last_ref_price = self.live_price

        trade_record = {
            "orderId": pos_id + "_S",
            "side": "SELL",
            "price": round(self.live_price, 2),
            "solAmount": round(sol_amt, 4),
            "fee": round(fee, 4),
            "profit": round(profit, 4),
            "realizedPnl": round(profit, 4),
            "round": r_num,
            "execType": "SINGULARITY_SCALP_EXIT",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.trades_history.insert(0, trade_record)
        self.singularity_trades_history.insert(0, trade_record)
        self.scalp_trades_history.insert(0, trade_record)
        asyncio.create_task(self.db_save_sell_individual(pos_id, trade_record))
        asyncio.create_task(self.db_sync_state())

    def run_singularity_tick(self):
        if self.is_paused or self.total_user_capital < 1000.0 or self.live_price <= 0:
            return

        if len(self.singularity_positions) == 0:
            if self.usdt_balance >= 10.0:
                self.execute_singularity_buy()
            return

        for pos in list(self.singularity_positions):
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)
                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_singularity_sell(pos)
                    continue

                if gain >= 1.50:
                    pullback = 0.20
                elif gain >= 0.80:
                    pullback = 0.15
                elif gain >= 0.40:
                    pullback = 0.10
                else:
                    pullback = 0.0
                if pullback > 0.0 and current_p <= (peak - pullback):
                    self.execute_singularity_sell(pos)

        if self.usdt_balance < 10.0 or len(self.singularity_positions) >= 24:
            self.singularity_tb_active = False
            return

        ref_p = min(float(p["entryPrice"]) for p in self.singularity_positions)
        self.singularity_last_ref_price = ref_p
        current_dip = ref_p - self.live_price
        dip_req = 1.50

        if current_dip >= dip_req:
            if not self.singularity_tb_active:
                self.singularity_tb_active = True
                self.singularity_tb_lowest = self.live_price
            else:
                if self.live_price < self.singularity_tb_lowest:
                    self.singularity_tb_lowest = self.live_price
                bounce_gap = 0.02
                if self.live_price >= (self.singularity_tb_lowest + bounce_gap):
                    self.singularity_tb_active = False
                    self.singularity_tb_lowest = 0.0
                    self.execute_singularity_buy()
        else:
            self.singularity_tb_active = False

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
        self.run_showcase_tick()
        if self.is_paused:
            return

        self.check_and_trigger_fund_tiers()
        self.process_round_transitions()
        self.run_hyper_titan_tick()
        self.run_micro_scalper_tick()
        self.run_killer2_scalper_tick()
        self.run_killer3_scalper_tick()
        self.run_singularity_tick()
        self.run_auto_trailing_loop_tick()

        if self.live_price <= 0:
            return

        for ord in list(self.wallet_open_orders):
            o_type = ord.get("orderType", "")
            side = ord.get("side", "BUY")
            amt = ord.get("amount", 0.0)
            target_p = ord.get("price", self.live_price)

            now_ts = datetime.now(timezone.utc).timestamp()
            norm_type = str(o_type).upper().replace(" ", "_")
            fixed_price = float(ord.get("price", target_p))
            side_str = str(side).upper()

            cur_p = round(self.live_price, 2)
            lim_p = round(fixed_price, 2)
            if norm_type == "LIMIT":
                if side_str == "BUY" and cur_p > 0 and lim_p > 0 and cur_p <= lim_p:
                    if ord in self.wallet_open_orders:
                        self.wallet_open_orders.remove(ord)
                    exact_invest = round(float(ord.get("invested", amt)), 2)
                    fee = round(exact_invest * self.taker_fee_pct, 4)
                    net_invest = exact_invest - fee
                    sol_bought = round(net_invest / lim_p, 4)
                    pos_id = "MAN_" + str(uuid.uuid4())[:6]
                    manual_pos = {
                        "id": pos_id,
                        "round": 0,
                        "subTrade": 0,
                        "label": f"WALLET LIMIT BUY ({pos_id})",
                        "side": "BUY",
                        "entryPrice": lim_p,
                        "solAmount": sol_bought,
                        "invested": exact_invest,
                        "orderType": "LIMIT",
                        "isManualWallet": True,
                        "status": "HOLDING",
                        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                    }
                    self.wallet_active_positions.insert(0, manual_pos)
                    t_record = {
                        "orderId": str(ord.get("id")),
                        "side": "BUY",
                        "price": lim_p,
                        "solAmount": sol_bought,
                        "invested": exact_invest,
                        "fee": fee,
                        "profit": 0.0,
                        "realizedPnl": 0.0,
                        "round": 0,
                        "execType": "LIMIT_BUY_FILLED",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.manual_trades_history.insert(0, t_record)
                    asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), {"order_id": str(ord.get("id")) + "_CLOSED", "side": "FILL", "price": lim_p, "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "LIMIT_FILLED"}))
                    asyncio.create_task(self.db_save_buy(manual_pos, t_record))
                    asyncio.create_task(self.db_sync_state())
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                elif side_str == "SELL" and cur_p > 0 and lim_p > 0 and cur_p >= lim_p:
                    if ord in self.wallet_open_orders:
                        self.wallet_open_orders.remove(ord)
                    sold_sol = round(float(ord.get("solAmount", 0.0)), 4)
                    cost_basis = round(float(ord.get("invested", 0.0)), 2)
                    gross_val = round(sold_sol * lim_p, 2)
                    fee = round(gross_val * self.taker_fee_pct, 4)
                    net_val = round(gross_val - fee, 2)
                    net_profit = round(net_val - cost_basis, 4)
                    self.manual_test_balance = round(self.manual_test_balance + net_val, 2)
                    self.manual_realized_pnl = round(self.manual_realized_pnl + net_profit, 4)
                    t_record = {
                        "orderId": str(ord.get("id")),
                        "side": "SELL",
                        "price": lim_p,
                        "solAmount": sold_sol,
                        "invested": cost_basis,
                        "fee": fee,
                        "profit": net_profit,
                        "realizedPnl": net_profit,
                        "round": 0,
                        "execType": "LIMIT_SELL_FILLED",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    self.manual_trades_history.insert(0, t_record)
                    asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), t_record))
                    asyncio.create_task(self.db_sync_state())
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
            elif norm_type in ["TRAILING_STOP", "TRAILING"]:
                cb = float(ord.get("callbackPct", 1.0))
                act_p = float(ord.get("activationPrice", 0.0))
                if side_str == "SELL":
                    if not ord.get("isActivated", False):
                        if cur_p >= act_p and act_p > 0:
                            ord["isActivated"] = True
                            ord["peakTracked"] = cur_p
                    else:
                        current_peak = float(ord.get("peakTracked", cur_p))
                        if cur_p > current_peak:
                            ord["peakTracked"] = cur_p
                            current_peak = cur_p
                        floor_trigger = round(current_peak * (1.0 - (cb / 100.0)), 2)
                        if cur_p <= floor_trigger:
                            if ord in self.wallet_open_orders:
                                self.wallet_open_orders.remove(ord)
                            sold_sol = round(float(ord.get("solAmount", 0.0)), 4)
                            cost_basis = round(float(ord.get("invested", 0.0)), 2)
                            gross_val = round(sold_sol * cur_p, 2)
                            fee = round(gross_val * self.taker_fee_pct, 4)
                            net_val = round(gross_val - fee, 2)
                            net_profit = round(net_val - cost_basis, 4)
                            self.manual_test_balance = round(self.manual_test_balance + net_val, 2)
                            self.manual_realized_pnl = round(self.manual_realized_pnl + net_profit, 4)
                            t_record = {
                                "orderId": str(ord.get("id")),
                                "side": "SELL",
                                "price": cur_p,
                                "solAmount": sold_sol,
                                "invested": cost_basis,
                                "fee": fee,
                                "profit": net_profit,
                                "realizedPnl": net_profit,
                                "round": 0,
                                "execType": "TRAILING_SELL_FILLED",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            self.manual_trades_history.insert(0, t_record)
                            asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), t_record))
                            asyncio.create_task(self.db_sync_state())
                            asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                elif side_str == "BUY":
                    if cur_p <= 1.0 or act_p <= 1.0:
                        pass
                    if not ord.get("isActivated", False):
                        if cur_p <= act_p:
                            ord["isActivated"] = True
                            ord["lowestTracked"] = cur_p
                    else:
                        current_low = float(ord.get("lowestTracked", cur_p))
                        if cur_p < current_low:
                            ord["lowestTracked"] = cur_p
                            current_low = cur_p
                        ceil_trigger = round(current_low * (1.0 + (cb / 100.0)), 2)
                        if cur_p >= ceil_trigger:
                            if ord in self.wallet_open_orders:
                                self.wallet_open_orders.remove(ord)
                            exact_invest = round(float(ord.get("invested", amt)), 2)
                            fee = round(exact_invest * self.taker_fee_pct, 4)
                            net_invest = exact_invest - fee
                            sol_bought = round(net_invest / cur_p, 4)
                            pos_id = "MAN_" + str(uuid.uuid4())[:6]
                            manual_pos = {
                                "id": pos_id,
                                "round": 0,
                                "subTrade": 0,
                                "label": "WALLET TRAILING BUY",
                                "side": "BUY",
                                "entryPrice": cur_p,
                                "solAmount": sol_bought,
                                "invested": exact_invest,
                                "orderType": "TRAILING_STOP",
                                "isManualWallet": True,
                                "status": "FILLED",
                                "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                            }
                            self.wallet_active_positions.insert(0, manual_pos)
                            t_record = {
                                "orderId": str(ord.get("id")),
                                "side": "BUY",
                                "price": cur_p,
                                "solAmount": sol_bought,
                                "invested": exact_invest,
                                "fee": fee,
                                "profit": 0.0,
                                "realizedPnl": 0.0,
                                "round": 0,
                                "execType": "TRAILING_BUY_FILLED",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            self.manual_trades_history.insert(0, t_record)
                            asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), {"order_id": str(ord.get("id")) + "_CLOSED", "side": "FILL", "price": cur_p, "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "TRAILING_FILLED"}))
                            asyncio.create_task(self.db_save_buy(manual_pos, t_record))
                            asyncio.create_task(self.db_sync_state())
                            asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
            elif norm_type == "TRIGGER":
                trig_p = round(float(ord.get("stopPrice", 0.0) or ord.get("price", 0.0)), 2)
                t_dir = ord.get("triggerDirection", "BELOW" if trig_p <= float(ord.get("activationPrice", cur_p)) else "ABOVE")
                should_exec = False
                if cur_p > 1.0 and trig_p > 1.0:
                    if t_dir == "BELOW" and cur_p <= trig_p:
                        should_exec = True
                    elif t_dir == "ABOVE" and cur_p >= trig_p:
                        should_exec = True

                if should_exec:
                    if ord in self.wallet_open_orders:
                        self.wallet_open_orders.remove(ord)
                    exec_fill_p = round(float(ord.get("limitPrice") or ord.get("price") or cur_p), 2)
                    if side_str == "SELL":
                        sold_sol = round(float(ord.get("solAmount", 0.0)), 4)
                        cost_basis = round(float(ord.get("invested", 0.0)), 2)
                        gross_val = round(sold_sol * exec_fill_p, 2)
                        fee = round(gross_val * self.taker_fee_pct, 4)
                        net_val = round(gross_val - fee, 2)
                        net_profit = round(net_val - cost_basis, 4)
                        self.manual_test_balance = round(self.manual_test_balance + net_val, 2)
                        self.manual_realized_pnl = round(self.manual_realized_pnl + net_profit, 4)
                        t_record = {
                            "orderId": str(ord.get("id")),
                            "side": "SELL",
                            "price": exec_fill_p,
                            "solAmount": sold_sol,
                            "invested": cost_basis,
                            "fee": fee,
                            "profit": net_profit,
                            "realizedPnl": net_profit,
                            "round": 0,
                            "execType": "TRIGGER_SELL_FILLED",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        self.manual_trades_history.insert(0, t_record)
                        asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), t_record))
                    else:
                        exact_invest = round(float(ord.get("invested", amt)), 2)
                        fee = round(exact_invest * self.taker_fee_pct, 4)
                        net_invest = exact_invest - fee
                        sol_bought = round(net_invest / exec_fill_p, 4)
                        pos_id = "MAN_" + str(uuid.uuid4())[:6]
                        manual_pos = {
                            "id": pos_id,
                            "round": 0,
                            "subTrade": 0,
                            "label": "WALLET TRIGGER BUY",
                            "side": "BUY",
                            "entryPrice": exec_fill_p,
                            "solAmount": sol_bought,
                            "invested": exact_invest,
                            "orderType": "TRIGGER",
                            "isManualWallet": True,
                            "status": "FILLED",
                            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                        }
                        self.wallet_active_positions.insert(0, manual_pos)
                        t_record = {
                            "orderId": str(ord.get("id")),
                            "side": "BUY",
                            "price": exec_fill_p,
                            "solAmount": sol_bought,
                            "invested": exact_invest,
                            "fee": fee,
                            "profit": 0.0,
                            "realizedPnl": 0.0,
                            "round": 0,
                            "execType": "TRIGGER_BUY_FILLED",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        self.manual_trades_history.insert(0, t_record)
                        asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), {"order_id": str(ord.get("id")) + "_CLOSED", "side": "FILL", "price": exec_fill_p, "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "TRIGGER_FILLED"}))
                        asyncio.create_task(self.db_save_buy(manual_pos, t_record))
                    asyncio.create_task(self.db_sync_state())
                    asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
            elif norm_type in ["TP_SL", "TP/SL", "OCO"]:
                p1 = round(float(ord.get("limitPrice", 0.0)), 2)
                p2 = round(float(ord.get("stopPrice", 0.0)), 2)
                init_p = round(float(ord.get("activationPrice", cur_p)), 2)
                should_exec = False
                exec_label = "OCO_FILLED"
                fill_target_p = cur_p

                if side_str == "SELL":
                    tp_p = max(p1, p2)
                    sl_p = min(p1, p2) if min(p1, p2) > 0 else 0.0
                    if tp_p > 0 and cur_p >= tp_p and init_p <= tp_p:
                        should_exec = True
                        exec_label = "TP_FILLED"
                        fill_target_p = tp_p
                    elif sl_p > 0 and cur_p <= sl_p and init_p >= sl_p:
                        should_exec = True
                        exec_label = "SL_FILLED"
                        fill_target_p = sl_p

                    if should_exec:
                        if ord in self.wallet_open_orders:
                            self.wallet_open_orders.remove(ord)
                        sold_sol = round(float(ord.get("solAmount", 0.0)), 4)
                        cost_basis = round(float(ord.get("invested", 0.0)), 2)
                        gross_val = round(sold_sol * cur_p, 2)
                        fee = round(gross_val * self.taker_fee_pct, 4)
                        net_val = round(gross_val - fee, 2)
                        net_profit = round(net_val - cost_basis, 4)
                        self.manual_test_balance = round(self.manual_test_balance + net_val, 2)
                        self.manual_realized_pnl = round(self.manual_realized_pnl + net_profit, 4)
                        t_record = {
                            "orderId": str(ord.get("id")),
                            "side": "SELL",
                            "price": cur_p,
                            "solAmount": sold_sol,
                            "invested": cost_basis,
                            "fee": fee,
                            "profit": net_profit,
                            "realizedPnl": net_profit,
                            "round": 0,
                            "execType": f"OCO_{exec_label}",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        self.manual_trades_history.insert(0, t_record)
                        asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), t_record))
                        asyncio.create_task(self.db_sync_state())
                        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))
                elif side_str == "BUY":
                    targets = [x for x in [p1, p2] if x > 0]
                    lower_target = min(targets) if targets else 0.0
                    upper_target = max(targets) if targets else 0.0

                    if lower_target > 0 and lower_target < init_p and cur_p <= lower_target:
                        should_exec = True
                        exec_label = "DIP_BUY_FILLED"
                        fill_target_p = lower_target
                    elif upper_target > 0 and upper_target > init_p and cur_p >= upper_target:
                        should_exec = True
                        exec_label = "BREAKOUT_BUY_FILLED"
                        fill_target_p = upper_target

                    if should_exec:
                        if ord in self.wallet_open_orders:
                            self.wallet_open_orders.remove(ord)
                        exact_invest = round(float(ord.get("invested", amt)), 2)
                        fee = round(exact_invest * self.taker_fee_pct, 4)
                        net_invest = exact_invest - fee
                        sol_bought = round(net_invest / fill_target_p, 4)
                        pos_id = "MAN_" + str(uuid.uuid4())[:6]
                        manual_pos = {
                            "id": pos_id,
                            "round": 0,
                            "subTrade": 0,
                            "label": "WALLET OCO BUY",
                            "side": "BUY",
                            "entryPrice": fill_target_p,
                            "solAmount": sol_bought,
                            "invested": exact_invest,
                            "orderType": "OCO",
                            "isManualWallet": True,
                            "status": "FILLED",
                            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S")
                        }
                        self.wallet_active_positions.insert(0, manual_pos)
                        t_record = {
                            "orderId": str(ord.get("id")),
                            "side": "BUY",
                            "price": cur_p,
                            "solAmount": sol_bought,
                            "invested": exact_invest,
                            "fee": fee,
                            "profit": 0.0,
                            "realizedPnl": 0.0,
                            "round": 0,
                            "execType": f"OCO_{exec_label}",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        self.manual_trades_history.insert(0, t_record)
                        asyncio.create_task(self.db_save_sell_individual(str(ord.get("id")), {"order_id": str(ord.get("id")) + "_CLOSED", "side": "FILL", "price": fill_target_p, "sol_amount": 0.0, "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "OCO_FILLED"}))
                        asyncio.create_task(self.db_save_buy(manual_pos, t_record))
                        asyncio.create_task(self.db_sync_state())
                        asyncio.create_task(manager.broadcast(json.dumps(self.get_state())))

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            return

        regular_positions = [p for p in self.active_positions if not p.get("isMacro", False)]
        macro_positions = [p for p in self.active_positions if p.get("isMacro", False)]

        if len(self.active_positions) == 0:
            if self.total_user_capital >= 40.0 and self.usdt_balance >= 10.0:
                self.execute_buy(is_sub_trade=False, escalate_round=False)
            return

        if len(regular_positions) == 0 and len(macro_positions) > 0:
            last_macro_entry = macro_positions[-1]["entryPrice"]
            if (last_macro_entry - self.live_price) >= 1.20 and self.total_user_capital >= 40.0 and self.usdt_balance >= 10.0:
                if len(macro_positions) < 24:
                    self.execute_buy(is_sub_trade=True, escalate_round=False)
            return

        last_entry = regular_positions[-1]["entryPrice"]
        current_dip = last_entry - self.live_price

        if current_dip < 1.20:
            self.tb_active = False
            self.tb_stage = "IDLE"
        else:
            if not self.tb_active:
                self.tb_active = True
                self.tb_lowest_price = self.live_price

            if self.tb_active:
                if self.live_price < self.tb_lowest_price:
                    self.tb_lowest_price = self.live_price

                required_bounce_pct = 0.0025
                self.tb_stage = "FAST_DIP"
                bounce_target = self.tb_lowest_price * (1.0 + required_bounce_pct)
                if self.live_price >= bounce_target:
                    self.tb_active = False
                    self.tb_stage = "IDLE"
                    active_count = len(regular_positions)
                    fund = self.total_user_capital
                    max_home_trades = 1 if fund < 50.0 else (2 if fund < 80.0 else 24)
                    if active_count < max_home_trades:
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
            entry_p = float(pos["entryPrice"])
            current_p = float(self.live_price)
            if current_p > entry_p:
                if "ts_high" not in pos or current_p > float(pos.get("ts_high", entry_p)):
                    pos["ts_high"] = round(current_p, 2)

                peak = float(pos["ts_high"])
                gain = peak - entry_p

                if self.usdt_balance < 10.0 and (current_p * float(pos["solAmount"]) * (1.0 - self.taker_fee_pct) - float(pos["invested"])) >= self.min_net_profit_usdt:
                    self.execute_sell_individual(pos)
                    break

                if gain >= 1.50:
                    pullback = 0.20
                    self.ts_stage = "STAGE_3"
                elif gain >= 0.80:
                    pullback = 0.15
                    self.ts_stage = "STAGE_2"
                elif gain >= 0.40:
                    pullback = 0.10
                    self.ts_stage = "STAGE_1"
                else:
                    pullback = 0.0

                if pullback > 0.0:
                    calc_stop = round(peak - pullback, 2)
                    min_allowed_stop = round(entry_p + 0.15, 2)
                    if calc_stop < min_allowed_stop:
                        calc_stop = min_allowed_stop
                    if "ts_low" not in pos or calc_stop > float(pos.get("ts_low", 0.0)):
                        pos["ts_low"] = calc_stop
                        self.ts_low = calc_stop
                    self.ts_high = peak

                    if current_p <= pos["ts_low"]:
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



@app.get("/")
def home():
    return {"status": "SHINE DEX BSC Quant Engine", "network": "BNB Smart Chain", "active": True}

@app.get("/health")
def health():
    return {"status": "ok"}

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
                elif action in ["UPGRADE_CAPITAL", "USER_LEVEL_UP"]:
                    slot_cost = float(msg.get("slotCost", 0.0))
                    sender_wallet = str(msg.get("walletAddress") or "").lower().strip()
                    prog_code = str(msg.get("program") or "V1").upper()
                    lvl_num = int(msg.get("level") or 1)
                    if sender_wallet and sender_wallet != bot.root_owner_address:
                        if bot.verify_user_slot_onchain(sender_wallet, prog_code, lvl_num):
                            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                                real_slots_cap = await bot.fetch_real_vault_capital_from_slots(session)
                            if real_slots_cap is not None and real_slots_cap > 0.0:
                                bot.total_user_capital = real_slots_cap
                            elif slot_cost > 0.0:
                                bot.total_user_capital = round(bot.total_user_capital + (slot_cost * 0.80), 2)
                            scalp_active_cost = (
                                sum(float(p.get("invested", 0.0)) for p in bot.micro_positions)
                                + sum(float(p.get("invested", 0.0)) for p in bot.killer2_positions)
                                + sum(float(p.get("invested", 0.0)) for p in bot.killer3_positions)
                                + sum(float(p.get("invested", 0.0)) for p in bot.hyper_positions)
                                + sum(float(p.get("invested", 0.0)) for p in bot.singularity_positions)
                            )
                            reg_active_cost = sum(float(p.get("invested", 0.0)) for p in bot.active_positions if not p.get("isMacro", False))
                            total_active_cost = reg_active_cost + scalp_active_cost + bot.macro_vault_invested + bot.round8_hold_invested
                            bot.usdt_balance = max(0.0, round(bot.total_user_capital + bot.realized_pnl - total_active_cost, 2))
                            bot.hyper_pool_balance = bot.usdt_balance
                            bot.singularity_pool_balance = bot.usdt_balance
                            asyncio.create_task(bot.db_sync_state())
                            bot.check_and_trigger_fund_tiers()
                elif action == "ADMIN_BOT_BUY":
                    b_target = str(msg.get("bot", "HOME")).upper()
                    if b_target == "HOME":
                        bot.execute_buy(is_sub_trade=True)
                    elif b_target == "HYPER":
                        bot.execute_hyper_buy()
                    elif b_target == "MICRO":
                        bot.execute_micro_buy()
                    elif b_target == "KILLER2":
                        bot.execute_killer2_buy()
                    elif b_target == "KILLER3":
                        bot.execute_killer3_buy()
                    elif b_target == "SINGULARITY":
                        e_idx = int(msg.get("engineIdx", 1))
                        bot.execute_singularity_buy(engine_idx=e_idx)
                elif action == "ADMIN_BOT_SELL":
                    b_target = str(msg.get("bot", "HOME")).upper()
                    t_pos_id = str(msg.get("posId", "")).upper()
                    if b_target == "HOME":
                        for p in list(bot.active_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_sell_individual(p, force=True)
                                break
                    elif b_target == "HYPER":
                        for p in list(bot.hyper_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_hyper_sell(p, force=True)
                                break
                    elif b_target == "MICRO":
                        for p in list(bot.micro_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_micro_sell(p, force=True)
                                break
                    elif b_target == "KILLER2":
                        for p in list(bot.killer2_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_killer2_sell(p, force=True)
                                break
                    elif b_target == "KILLER3":
                        for p in list(bot.killer3_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_killer3_sell(p, force=True)
                                break
                    elif b_target == "SINGULARITY":
                        for p in list(bot.singularity_positions):
                            if str(p.get("id", "")).upper() == t_pos_id:
                                bot.execute_singularity_sell(p, force=True)
                                break
                elif action == "ADMIN_BOT_SELL_ALL":
                    b_target = str(msg.get("bot", "HOME")).upper()
                    if b_target == "HOME":
                        for p in list(bot.active_positions):
                            bot.execute_sell_individual(p, force=True)
                    elif b_target == "HYPER":
                        for p in list(bot.hyper_positions):
                            bot.execute_hyper_sell(p, force=True)
                    elif b_target == "MICRO":
                        for p in list(bot.micro_positions):
                            bot.execute_micro_sell(p, force=True)
                    elif b_target == "KILLER2":
                        for p in list(bot.killer2_positions):
                            bot.execute_killer2_sell(p, force=True)
                    elif b_target == "KILLER3":
                        for p in list(bot.killer3_positions):
                            bot.execute_killer3_sell(p, force=True)
                    elif b_target == "SINGULARITY":
                        for p in list(bot.singularity_positions):
                            bot.execute_singularity_sell(p, force=True)
                elif action in ["MANUAL_BUY", "MANUAL_SELL", "CREATE_ORDER", "PLACE_ORDER", "ADVANCED_ORDER", "CANCEL_ORDER"]:
                    await bot.create_advanced_order(msg)
                elif action == "CLIENT_PRICE_TICK":
                    c_p = float(msg.get("price", 0.0))
                    if c_p > 0:
                        bot.update_price_tick(c_p)
                elif action in ["CANCEL_AUTO_LOOP", "STOP_AUTO_LOOP"]:
                    s_id = msg.get("slotId", "ALL")
                    bot.cancel_auto_loop_slot(s_id)
                elif action in ["CREATE_AUTO_LOOP", "EDIT_AUTO_LOOP"]:
                    u_amt = float(msg.get("amount", 10.0))
                    b_trig = float(msg.get("buyTrigger", 100.0))
                    b_cb = float(msg.get("buyCallback", 0.01))
                    s_trig = float(msg.get("sellTrigger", 105.0))
                    s_cb = float(msg.get("sellCallback", 0.01))
                    a_rep = bool(msg.get("autoRepeat", True))
                    s_id = msg.get("slotId", None)
                    bot.create_auto_loop_order(u_amt, b_trig, b_cb, s_trig, s_cb, a_rep, s_id)
                elif action == "START_COPY_TRADE":
                    c_amt = float(msg.get("amount", 10.0))
                    c_type = str(msg.get("botType", "VELOCITY_DCA"))
                    c_slots = min(10, max(1, int(msg.get("slotsAllowed", 1))))
                    if bot.manual_test_balance < c_amt or c_amt <= 0:
                        continue
                    if not hasattr(bot, "copy_subscribers"):
                        bot.copy_subscribers = []
                    bot.manual_test_balance -= c_amt
                    sub_id = "BOT_" + str(uuid.uuid4())[:6]
                    per_slot_amt = round(c_amt / max(1, c_slots), 2)
                    bot.copy_subscribers.append({
                        "id": sub_id,
                        "botType": c_type,
                        "totalCapital": c_amt,
                        "availableReserve": c_amt,
                        "slotSize": per_slot_amt,
                        "slotsAllowed": c_slots,
                        "activeSlots": 0,
                        "realizedPnl": 0.0,
                        "activePositions": [],
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    copy_pos = {
                        "id": sub_id,
                        "round": 0,
                        "subTrade": 0,
                        "label": f"COPY|{c_type}|{c_slots}",
                        "entryPrice": round(bot.live_price, 2),
                        "solAmount": 0.0,
                        "invested": round(c_amt, 2),
                        "isMacro": False,
                        "targetPrice": 0.0
                    }
                    asyncio.create_task(bot.db_save_buy(copy_pos, {
                        "order_id": sub_id,
                        "side": "COPY_START",
                        "price": round(bot.live_price, 2),
                        "sol_amount": 0.0,
                        "fee": 0.0,
                        "profit": 0.0,
                        "round": 0,
                        "exec_type": f"COPY_{c_type}_RESERVED"
                    }))
                    asyncio.create_task(bot.db_sync_state())
                elif action == "CLOSE_COPY_TRADE":
                    s_id = str(msg.get("subId", ""))
                    if hasattr(bot, "copy_subscribers"):
                        for sub in list(bot.copy_subscribers):
                            if sub.get("id") == s_id:
                                reserve = float(sub.get("availableReserve", 0.0))
                                positions = sub.get("activePositions", [])
                                active_sol = sum(float(p.get("solAmount", 0.0)) for p in positions)
                                active_invested = sum(float(p.get("invested", 0.0)) for p in positions)
                                gross_sold = active_sol * bot.live_price
                                fee = gross_sold * bot.taker_fee_pct
                                net_sold = gross_sold - fee
                                pos_pnl = net_sold - active_invested if active_sol > 0 else 0.0
                                total_refund = round(reserve + net_sold, 2)
                                bot.manual_test_balance = round(bot.manual_test_balance + total_refund, 2)
                                bot.manual_realized_pnl = round(bot.manual_realized_pnl + pos_pnl, 4)
                                bot.copy_subscribers.remove(sub)
                                for p_item in positions:
                                    if p_item.get("posId"):
                                        asyncio.create_task(bot.db_save_sell_individual(p_item.get("posId"), {"order_id": p_item.get("posId") + "_SUB_CLOSED", "side": "SELL", "price": round(bot.live_price, 2), "sol_amount": float(p_item.get("solAmount", 0.0)), "fee": 0.0, "profit": 0.0, "round": 0, "exec_type": "COPY_SUB_CLOSED"}))
                                t_rec = {
                                    "orderId": s_id + "_CLOSED",
                                    "side": "SELL",
                                    "price": round(bot.live_price, 2),
                                    "solAmount": round(active_sol, 4),
                                    "fee": round(fee, 4),
                                    "profit": round(pos_pnl, 4),
                                    "realizedPnl": round(pos_pnl, 4),
                                    "execType": "COPY_BOT_UNSUBSCRIBED",
                                    "timestamp": datetime.now(timezone.utc).isoformat()
                                }
                                bot.manual_trades_history.insert(0, t_rec)
                                asyncio.create_task(bot.db_save_sell_individual(s_id, t_rec))
                                asyncio.create_task(bot.db_sync_state())
                                break
                await manager.broadcast(json.dumps(bot.get_state()))
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

async def run_backend_price_feed():
    endpoints = [
        "wss://stream.binance.com:9443/ws/solusdt@trade",
        "wss://data-stream.binance.vision/ws/solusdt@trade"
    ]
    ep_idx = 0
    last_broadcast_ts = 0.0
    while True:
        url = endpoints[ep_idx % len(endpoints)]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(url, timeout=10.0) as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            p = 0.0
                            if "p" in data:
                                p = float(data["p"])
                                bot.process_market_trades([data])
                            elif "price" in data:
                                p = float(data["price"])
                            if p > 0:
                                bot.update_price_tick(p)
                                now_ts = datetime.now(timezone.utc).timestamp()
                                if (now_ts - last_broadcast_ts) >= 0.4:
                                    last_broadcast_ts = now_ts
                                    await manager.broadcast(json.dumps(bot.get_state()))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
        except Exception:
            pass
        ep_idx += 1
        await asyncio.sleep(1)

async def cleanup_all_bots_24h_history():
    pkt_zone = timezone(timedelta(hours=5))
    while True:
        now_pkt = datetime.now(pkt_zone)
        target_midnight = (now_pkt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (target_midnight - now_pkt).total_seconds()
        await asyncio.sleep(wait_seconds)
        try:
            now_iso = datetime.now(timezone.utc).isoformat()
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS) as session:
                await session.delete(f"{SUPABASE_URL}/rest/v1/trades_history?created_at=lte.{now_iso}")
            if hasattr(bot, "trades_history"):
                bot.trades_history.clear()
            if hasattr(bot, "spot_trades_history"):
                bot.spot_trades_history.clear()
            if hasattr(bot, "micro_trades_history"):
                bot.micro_trades_history.clear()
            if hasattr(bot, "killer2_trades_history"):
                bot.killer2_trades_history.clear()
            if hasattr(bot, "killer3_trades_history"):
                bot.killer3_trades_history.clear()
            if hasattr(bot, "scalp_trades_history"):
                bot.scalp_trades_history.clear()
            if hasattr(bot, "hyper_trades_history"):
                bot.hyper_trades_history.clear()
            if hasattr(bot, "singularity_trades_history"):
                bot.singularity_trades_history.clear()
            if hasattr(bot, "showcase_trades_history"):
                bot.showcase_trades_history.clear()
            await bot.db_save_showcase_state()
            await bot.db_sync_state()
            await manager.broadcast(json.dumps(bot.get_state()))
        except Exception:
            pass

async def self_keep_alive_ping():
    await asyncio.sleep(5)
    ping_urls = [
        "https://shine-crypto-bot.onrender.com/status",
        "https://shine-crypto-bot.fastapicloud.dev/status"
    ]
    timeout = aiohttp.ClientTimeout(total=8)
    while True:
        try:
            async with aiohttp.ClientSession(headers=SUPABASE_HEADERS, timeout=timeout) as session:
                real_slots_cap = await bot.fetch_real_vault_capital_from_slots(session)
                if real_slots_cap is not None and abs(real_slots_cap - bot.total_user_capital) >= 0.01:
                    bot.total_user_capital = real_slots_cap
                    scalp_cost = (
                        sum(float(p.get("invested", 0.0)) for p in bot.micro_positions)
                        + sum(float(p.get("invested", 0.0)) for p in bot.killer2_positions)
                        + sum(float(p.get("invested", 0.0)) for p in bot.killer3_positions)
                        + sum(float(p.get("invested", 0.0)) for p in bot.hyper_positions)
                        + sum(float(p.get("invested", 0.0)) for p in bot.singularity_positions)
                    )
                    reg_cost = sum(float(p.get("invested", 0.0)) for p in bot.active_positions if not p.get("isMacro", False))
                    total_active = reg_cost + scalp_cost + bot.macro_vault_invested + bot.round8_hold_invested
                    bot.usdt_balance = max(0.0, round(bot.total_user_capital + bot.realized_pnl - total_active, 2))
                    bot.hyper_pool_balance = bot.usdt_balance
                    bot.singularity_pool_balance = bot.usdt_balance
                    await bot.db_sync_state()
                    bot.check_and_trigger_fund_tiers()
        except Exception:
            pass
        for u in ping_urls:
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(u) as resp:
                        pass
            except Exception:
                pass
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.load_from_database())
    asyncio.create_task(self_keep_alive_ping())
    asyncio.create_task(run_backend_price_feed())
    asyncio.create_task(cleanup_all_bots_24h_history())

try:
    from web3 import Web3
    import solcx
    BSC_TESTNET_RPC = os.environ.get("BSC_RPC_URL", "https://bsc-testnet-rpc.publicnode.com")
    w3_deploy = Web3(Web3.HTTPProvider(BSC_TESTNET_RPC))
    w3_deploy.eth.account.enable_unaudited_hdwallet_features()
except Exception:
    w3_deploy = None

MNEMONIC_PHRASE = os.environ.get("MNEMONIC_PHRASE", "").strip()
BOT_EXECUTOR_KEY = os.environ.get("BOT_EXECUTOR_KEY", "").strip()

GITHUB_BASE = "https://raw.githubusercontent.com/shine762/Shine.Core.sol/main"

def send_signed_tx(tx_dict, priv_key):
    signed_tx = w3_deploy.eth.account.sign_transaction(tx_dict, private_key=priv_key)
    raw_tx = getattr(signed_tx, "raw_transaction", getattr(signed_tx, "rawTransaction", None))
    tx_hash = w3_deploy.eth.send_raw_transaction(raw_tx)
    receipt = w3_deploy.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    return tx_hash.hex(), receipt

@app.get("/deploy-all-contracts")
async def deploy_all_system(admin_key: str = ""):
    expected_key = os.environ.get("ADMIN_DEPLOY_KEY", "")
    if not expected_key or admin_key != expected_key or not MNEMONIC_PHRASE:
        return {"status": "ERROR", "message": "Unauthorized or MNEMONIC_PHRASE env missing"}
    account = w3_deploy.eth.account.from_mnemonic(MNEMONIC_PHRASE)
    deployer_key = account.key.hex()
    sender = account.address

    balance = w3_deploy.eth.get_balance(sender)
    if balance < w3_deploy.to_wei(0.005, 'ether'):
        return {"status": "ERROR", "message": f"Wallet {sender} mein kam az kam 0.005 tBNB hona zaroori hai!"}

    try:
        solcx.install_solc('0.8.20')
        solcx.set_solc_version('0.8.20')
    except Exception:
        pass

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{GITHUB_BASE}/MockUSDT.sol") as r:
            mock_code = await r.text()
        async with session.get(f"{GITHUB_BASE}/ShineCore.sol") as r:
            core_code = await r.text()
        async with session.get(f"{GITHUB_BASE}/ShineVault.sol") as r:
            vault_code = await r.text()

    with open("MockUSDT.sol", "w") as f:
        f.write(mock_code)
    with open("ShineCore.sol", "w") as f:
        f.write(core_code)
    with open("ShineVault.sol", "w") as f:
        f.write(vault_code)

    compiled = solcx.compile_files(["MockUSDT.sol", "ShineCore.sol", "ShineVault.sol"], solc_version='0.8.20')

    mock_interface = next(v for k, v in compiled.items() if k.endswith(":MockUSDT"))
    core_interface = next(v for k, v in compiled.items() if k.endswith(":ShineCore"))
    vault_interface = next(v for k, v in compiled.items() if k.endswith(":ShineVault"))

    gas_price = max(w3_deploy.eth.gas_price, w3_deploy.to_wei('5', 'gwei'))

    mock_contract = w3_deploy.eth.contract(abi=mock_interface['abi'], bytecode=mock_interface['bin'])
    nonce = w3_deploy.eth.get_transaction_count(sender, 'pending')
    tx_mock = mock_contract.constructor().build_transaction({
        'from': sender,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': gas_price
    })
    _, receipt_mock = send_signed_tx(tx_mock, deployer_key)
    mock_usdt_address = receipt_mock.contractAddress

    core_contract = w3_deploy.eth.contract(abi=core_interface['abi'], bytecode=core_interface['bin'])
    nonce = w3_deploy.eth.get_transaction_count(sender, 'pending')
    tx_core = core_contract.constructor(mock_usdt_address).build_transaction({
        'from': sender,
        'nonce': nonce,
        'gas': 5000000,
        'gasPrice': gas_price
    })
    _, receipt_core = send_signed_tx(tx_core, deployer_key)
    shine_core_address = receipt_core.contractAddress

    vault_contract = w3_deploy.eth.contract(abi=vault_interface['abi'], bytecode=vault_interface['bin'])
    nonce = w3_deploy.eth.get_transaction_count(sender, 'pending')
    tx_vault = vault_contract.constructor(mock_usdt_address, shine_core_address, sender).build_transaction({
        'from': sender,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': gas_price
    })
    _, receipt_vault = send_signed_tx(tx_vault, deployer_key)
    shine_vault_address = receipt_vault.contractAddress

    core_deployed = w3_deploy.eth.contract(address=shine_core_address, abi=core_interface['abi'])
    nonce = w3_deploy.eth.get_transaction_count(sender, 'pending')
    tx_link = core_deployed.functions.setVaults(
        sender,
        shine_vault_address,
        sender,
        sender,
        sender
    ).build_transaction({
        'from': sender,
        'nonce': nonce,
        'gas': 500000,
        'gasPrice': gas_price
    })
    send_signed_tx(tx_link, deployer_key)

    bot.bsc_usdt_address = mock_usdt_address
    bot.shine_vault_address = shine_vault_address
    bot.shine_core_address = shine_core_address

    return {
        "status": "SUCCESS",
        "message": "Teeno contracts deploy ho gaye aur aapas mein link ho gaye!",
        "deployedBy": sender,
        "contracts": {
            "MockUSDT": mock_usdt_address,
            "ShineCore": shine_core_address,
            "ShineVault": shine_vault_address
        },
        "links": {
            "MockUSDT_BscScan": f"https://testnet.bscscan.com/address/{mock_usdt_address}",
            "ShineCore_BscScan": f"https://testnet.bscscan.com/address/{shine_core_address}",
            "ShineVault_BscScan": f"https://testnet.bscscan.com/address/{shine_vault_address}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
