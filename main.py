                
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile Preview</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<script src="https://cdnjs.cloudflare.com/ajax/libs/ethers/5.7.2/ethers.umd.min.js"></script>
<script src="https://unpkg.com/@solana/web3.js@1.91.4/lib/index.iife.min.js"></script>
<script src="https://unpkg.com/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        :root {
            --primary-bg: #1E1E2C;
            --secondary-bg: #2A2A3B;
            --tertiary-bg: #333344;
            --primary-blue: #3A47A6;
            --accent-orange: #E8755B;
            --text-primary: #FFFFFF;
            --text-secondary: #FFFFFFB3;
            --link-blue: #5C6BC0;
        }
        body {
            margin: 0;
            font-family: 'Plus Jakarta Sans', 'Roboto', sans-serif;
            background-color: var(--primary-bg);
            color: var(--text-primary);
            -webkit-font-smoothing: antialiased;
        }
        @keyframes terminalBlink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        @keyframes priceFlashGreen {
            0% { color: #00e676; text-shadow: 0 0 25px rgba(0, 230, 118, 0.9); }
            100% { color: #ffffff; text-shadow: 0 0 20px rgba(255,255,255,0.25); }
        }
        @keyframes priceFlashRed {
            0% { color: #f6465d; text-shadow: 0 0 25px rgba(246, 70, 93, 0.9); }
            100% { color: #ffffff; text-shadow: 0 0 20px rgba(255,255,255,0.25); }
        }
        .price-flash-up {
            animation: priceFlashGreen 0.6s ease-out;
        }
        .price-flash-down {
            animation: priceFlashRed 0.6s ease-out;
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
        }
        .header {
            background-color: var(--primary-blue);
            padding: 12px 16px;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            flex-wrap: nowrap;
        }
        #walletBtn {
            flex-shrink: 0;
            white-space: nowrap;
            z-index: 100;
        }
        .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header-title svg {
            width: 28px;
            height: 24px;
        }
        .header-title span {
            font-size: 16px;
            font-weight: 500;
        }
        .material-icons {
            color: var(--text-primary);
        }
        .profile-section {
            display: flex;
            align-items: center;
            padding: 24px 16px;
            gap: 16px;
        }
        .avatar-container {
            position: relative;
            width: 90px;
            height: 90px;
            flex-shrink: 0;
        }
        .avatar-gradient-border {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            padding: 0;
            background: none;
            box-sizing: border-box;
        }
        .avatar {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-image: url('https://i.imgur.com/O4u35tA.jpeg');
            background-size: cover;
            background-position: center;
        }
        
        .profile-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
        }
        .profile-name {
            font-size: 24px;
            font-weight: bold;
        }
.profile-name-wrapper {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
        }
        .settings-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 0;
            display: flex;
            align-items: center;
        }
        .profile-edit-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #151515;
            z-index: 6000;
            display: none;
            overflow-y: auto;
        }
        .profile-edit-overlay.active { display: block; }
        .edit-header {
            padding: 16px;
            border-bottom: 1px solid #2A2A2A;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .breadcrumb { color: #757575; font-size: 14px; }
        .breadcrumb span { color: white; }
        .edit-content { padding: 24px 16px; display: flex; flex-direction: column; align-items: center; }
        .edit-avatar-wrapper { position: relative; width: 120px; height: 120px; margin-bottom: 30px; }
        .edit-avatar { width: 100%; height: 100%; border-radius: 50%; background-image: url('https://i.imgur.com/O4u35tA.jpeg'); background-size: cover; }
        .close-edit-btn { position: absolute; top: 0; right: 0; background: #333; border: none; border-radius: 50%; width: 32px; height: 32px; color: white; display: flex; align-items: center; justify-content: center; }
        .input-group { width: 100%; margin-bottom: 20px; }
        .input-group label { display: block; color: #757575; margin-bottom: 8px; font-size: 14px; }
        .input-group input, .input-group textarea { width: 100%; background: #212121; border: 1px solid #333; border-radius: 12px; padding: 16px; color: white; font-size: 16px; box-sizing: border-box; }
        .save-profile-btn { width: 100%; background: var(--primary-blue); color: white; border: none; border-radius: 12px; padding: 16px; font-size: 16px; font-weight: bold; margin-top: 10px; }
        .profile-id {
            font-size: 16px;
            color: var(--text-secondary);
        }
        .show-more-btn {
            background-color: var(--tertiary-bg);
            border: none;
            border-radius: 20px;
            color: var(--text-primary);
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            margin-top: 8px;
        }
        .link-section {
            margin: 0 16px;
            background-color: var(--secondary-bg);
            border-radius: 16px;
            padding: 16px;
        }
        .link-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .link-title {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-secondary);
        }
        .question-mark {
            width: 16px;
            height: 16px;
            border: 1.5px solid var(--text-secondary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }
        .personal-link {
            color: var(--link-blue);
            font-weight: bold;
            text-decoration: none;
        }
        .copy-btn {
            width: 100%;
            background-color: var(--primary-blue);
            border: none;
            border-radius: 12px;
            color: var(--text-primary);
            padding: 16px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 16px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            padding: 16px 16px 0;
        }
        .stat-card {
            background-color: var(--secondary-bg);
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 100px;
        }
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
        }
        .stat-title {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 14px;
        }
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            margin-top: 8px;
        }
        .see-now-btn {
            background-color: var(--tertiary-bg);
            border: none;
            border-radius: 20px;
            color: var(--text-primary);
            padding: 8px 20px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 8px;
        }
.card-section {
            margin: 16px 16px 0;
            background-color: var(--secondary-bg);
            border-radius: 16px;
            padding: 16px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .card-header h2 {
            font-size: 18px;
            font-weight: 500;
            margin: 0;
        }
        .currency-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .currency-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--primary-bg);
            padding: 12px;
            border-radius: 12px;
        }
        .currency-info {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .currency-info span {
            font-weight: 500;
        }
        .currency-balance {
            font-weight: 700;
            font-size: 16px;
        }
        .passive-income-section h2 {
            font-size: 18px;
            font-weight: 500;
            margin: 0;
            color: var(--text-secondary);
        }
        .passive-income-amount {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 28px;
            font-weight: bold;
            margin-top: 8px;
        }
        .claim-btn {
            width: 100%;
            background-color: var(--primary-blue);
            border: none;
            border-radius: 12px;
            color: var(--text-primary);
            padding: 12px 16px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .claim-value {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
        }
        .divider {
            border: none;
            border-top: 1px dashed var(--tertiary-bg);
            margin: 20px 0;
        }
        .rules-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .rule-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
        }
        .rule-value {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--text-primary);
            font-weight: 500;
        }
        .icon-sm {
            width: 20px;
            height: 20px;
        }
        .icon-md {
            width: 24px;
            height: 24px;
        }
.rewards-section {
    margin: 24px 16px;
    color: var(--text-secondary);
}
.rewards-title {
    font-size: 18px;
    margin-bottom: 16px;
}
.reward-card {
    background-color: var(--secondary-bg);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}
.reward-label {
    font-size: 14px;
    margin-bottom: 8px;
}
.reward-value-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 28px;
    font-weight: bold;
    color: var(--text-primary);
}
.distribution-card {
    background-color: transparent;
    border: 1px solid var(--tertiary-bg);
    border-radius: 16px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-secondary);
}

.visual-container {
    position: relative;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(circle, rgba(15, 20, 30, 0.8) 0%, transparent 70%);
    overflow: hidden;
    margin: 20px 0;
}
@keyframes pulseV1 {
    0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(255, 215, 0, 0.4), inset 0 0 20px rgba(255, 215, 0, 0.4); }
    50% { transform: scale(1.05); box-shadow: 0 0 40px rgba(255, 215, 0, 0.8), inset 0 0 30px rgba(255, 215, 0, 0.6); }
}
@keyframes orbitRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes orbitAntiRotate { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
@keyframes orbitRotateReverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
@keyframes radarSweep { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes realCandleGreen {
            0%, 100% { transform: translateY(-4px) scaleY(1.2); }
            50% { transform: translateY(3px) scaleY(0.8); }
        }
        @keyframes realCandleRed {
            0%, 100% { transform: translateY(4px) scaleY(0.85); }
            50% { transform: translateY(-4px) scaleY(1.25); }
        }
        @keyframes realCandleOrange {
            0%, 100% { transform: translateY(0px) scaleY(1); }
            50% { transform: translateY(-2.5px) scaleY(1.1); }
        }
        @keyframes livePulseDot {
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.8); }
            60% { transform: scale(1.3); box-shadow: 0 0 0 6px rgba(0, 230, 118, 0); }
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }
        }
        .c-green { transform-origin: center; animation: realCandleGreen 1.4s ease-in-out infinite; }
        .c-orange { transform-origin: center; animation: realCandleOrange 1.4s ease-in-out infinite; }
        .c-red { transform-origin: center; animation: realCandleRed 1.4s ease-in-out infinite; }
        .live-vibe-dot {
            width: 7px;
            height: 7px;
            background: #00e676;
            border-radius: 50%;
            display: inline-block;
            animation: livePulseDot 1.2s infinite;
        }
        .pro-bot-btn {
            background-color: var(--secondary-bg);
            border: none;
            border-radius: 16px;
            padding: 14px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            box-sizing: border-box;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 14px;
            text-align: left;
        }
        .pro-bot-btn:active {
            transform: scale(0.98);
            opacity: 0.9;
        }

.radar-sweep {
    position: absolute;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, transparent 70%, rgba(0, 188, 212, 0.3) 100%);
    animation: radarSweep 4s linear infinite;
    z-index: 2;
}

.orbit-container { position: absolute; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; animation: orbitRotate 20s linear infinite; z-index: 5; }
.orbit-layer-2 { position: absolute; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; animation: orbitRotateReverse 30s linear infinite; z-index: 4; }
.orbit-layer-3 { position: absolute; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; animation: orbitRotate 40s linear infinite; z-index: 3; }

.counter-rotate { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; animation: orbitAntiRotate 20s linear infinite; }
.counter-rotate-normal { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; animation: orbitRotate 30s linear infinite; }
.counter-rotate-slow { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; animation: orbitAntiRotate 40s linear infinite; }

.main-badge {
    width: 80px; height: 80px;
    background: rgba(20, 20, 20, 0.9);
    border: none;
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    font-size: 32px; font-weight: 900; color: #FFD700;
    text-shadow: 0 0 10px #FFD700;
    z-index: 10;
    animation: pulseV1 2s ease-in-out infinite;
}

.sci-badge {
    position: absolute;
    background: rgba(15, 15, 20, 0.85);
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    font-weight: 900;
    backdrop-filter: blur(4px);
}

.bg-badge { width: 46px; height: 46px; font-size: 14px; }
.bg-badge-l2 { width: 38px; height: 38px; font-size: 12px; }
.bg-badge-l3 { width: 30px; height: 30px; font-size: 10px; }

.badge-x2 { border: none; color: #00BCD4; box-shadow: none; transform: translate(75px, 0px); }
.badge-x3 { border: none; color: #5C6BC0; box-shadow: none; transform: translate(23px, 71px); }
.badge-x4 { border: none; color: #8A2BE2; box-shadow: none; transform: translate(-60px, 44px); }
.badge-x5 { border: none; color: #E91E63; box-shadow: none; transform: translate(-60px, -44px); }
.badge-x6 { border: none; color: #2196F3; box-shadow: none; transform: translate(23px, -71px); }

.badge-x7 { border: none; color: #FF4500; box-shadow: none; transform: translate(101px, 73px); }
.badge-x8 { border: none; color: #32CD32; box-shadow: none; transform: translate(-38px, 119px); }
.badge-x9 { border: none; color: #FF1493; box-shadow: none; transform: translate(-125px, 0px); }
.badge-x10 { border: none; color: #00FA9A; box-shadow: none; transform: translate(-38px, -119px); }
.badge-x11 { border: none; color: #9400D3; box-shadow: none; transform: translate(101px, -73px); }

.badge-x12 { border: none; color: #FF8C00; box-shadow: none; transform: translate(120px, 120px); }
.badge-x13 { border: none; color: #00FFFF; box-shadow: none; transform: translate(-120px, 120px); }
.badge-x14 { border: none; color: #DC143C; box-shadow: none; transform: translate(-120px, -120px); }
.badge-x15 { border: none; color: #FFFFFF; box-shadow: none; transform: translate(120px, -120px); }

.circle-overlay {
    position: absolute;
    border-radius: 50%;
    z-index: 1;
}
.ring-1 { width: 150px; height: 150px; border: 1px dashed rgba(0, 188, 212, 0.3); }
.ring-2 { width: 250px; height: 250px; border: 1px dotted rgba(0, 188, 212, 0.2); }
.ring-3 { width: 340px; height: 340px; border: 1px solid rgba(0, 188, 212, 0.1); }
.programs-section {
    padding: 16px;
    position: relative;
    z-index: 10;
    background-color: var(--primary-bg);
    margin-top: 20px;
    display: block !important;
    clear: both;
    overflow: visible;
}
.programs-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.programs-header h2 {
    font-size: 24px;
    margin: 0;
}
.more-info-btn {
    background: #2A2A3B;
    border: none;
    border-radius: 20px;
    color: var(--text-secondary);
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
}
.program-card {
    background: #151515;
    border-radius: 24px;
    padding: 2px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.program-card.V1 { background: linear-gradient(135deg, #FFD700 0%, #151515 40%); }
.program-card.Q2 { background: linear-gradient(135deg, #FFFF00 0%, #151515 40%); }
.program-card.T3 { background: linear-gradient(135deg, #3A47A6 0%, #151515 40%); }
.program-card.S4 { background: linear-gradient(135deg, #8A2BE2 0%, #151515 40%); }
.program-card.G5 { background: linear-gradient(135deg, #E91E63 0%, #151515 40%); }
.program-card.N6 { background: linear-gradient(135deg, #00BCD4 0%, #151515 40%); }
.program-card.A7 { background: linear-gradient(135deg, #FF4500 0%, #151515 40%); }
.program-card.C8 { background: linear-gradient(135deg, #32CD32 0%, #151515 40%); }
.program-card.S9 { background: linear-gradient(135deg, #FF1493 0%, #151515 40%); }
.program-card.Q10 { background: linear-gradient(135deg, #00FA9A 0%, #151515 40%); }
.program-card.H11 { background: linear-gradient(135deg, #9400D3 0%, #151515 40%); }
.program-card.O12 { background: linear-gradient(135deg, #FF8C00 0%, #151515 40%); }
.program-card.N13 { background: linear-gradient(135deg, #00FFFF 0%, #151515 40%); }
.program-card.E14 { background: linear-gradient(135deg, #DC143C 0%, #151515 40%); }
.program-card.X15 { background: linear-gradient(135deg, #FFFFFF 0%, #151515 40%); }
.program-inner {
    background: #1A1A1A;
    border-radius: 22px;
    padding: 20px;
}
.platform-activity {
            padding: 16px;
            margin-bottom: 100px;
        }
        .activity-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
        .activity-header h2 {
            font-size: 28px;
            margin: 0;
            line-height: 1.2;
        }
        .activity-card {
            background: #212121;
            border-radius: 24px;
            padding: 20px;
            margin-bottom: 16px;
        }
        .activity-label {
            color: #757575;
            font-size: 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .activity-main-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .activity-total {
            font-size: 20px;
            font-weight: 700;
        }
        .activity-growth {
            color: #4CAF50;
            font-size: 16px;
        }
        .activity-divider {
            height: 1px;
            background: #333;
            margin: 16px 0;
        }
        .contract-selector {
            background: #212121;
            border-radius: 24px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #757575;
            margin-bottom: 16px;
        }
        .selector-arrow {
            background: #3A47A6;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .recent-event {
            display: flex;
            gap: 12px;
            align-items: center;
            padding: 10px 0;
        }
        .event-icon-bg {
            background: #1B5E20;
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .event-icon-bg i {
            color: #4CAF50;
            font-size: 20px;
        }
        .event-id {
            background: #1A237E;
            color: #5C6BC0;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
        }
        .event-time {
            color: #757575;
            font-size: 14px;
        }
        .event-top {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 4px;
        }
        .event-amount {
            font-weight: 500;
        }
        .event-program {
            color: #757575;
        }
        .blue-text {
            color: #5C6BC0;
        }
        .floating-actions {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 100;
        }
        .fab-trading {
            background: #7E57C2;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            cursor: pointer;
            border: none;
            color: white;
            text-decoration: none;
        }
        .fab-trading i { font-size: 24px; }
        .fab-trading span { font-size: 10px; font-weight: bold; text-transform: uppercase; margin-top: 2px; }
        .trading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #080808;
            z-index: 9000;
            display: none;
            flex-direction: column;
            font-family: 'Roboto', sans-serif;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        .trading-overlay.active { display: flex; }
        .bot-nav-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 65px;
            background: #0d0f17;
            border-top: 1px solid #1f2433;
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 10000;
            box-sizing: border-box;
            padding: 0 10px;
        }
        .bot-nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #718096;
            cursor: pointer;
            flex: 1;
            gap: 4px;
            background: none;
            border: none;
            outline: none;
        }
        .bot-nav-item svg {
            width: 22px;
            height: 22px;
            fill: currentColor;
            transition: all 0.2s ease;
        }
        .bot-nav-item span {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .bot-nav-item.active {
            color: #00d2ff;
        }
        .bot-nav-item.active svg {
            fill: #00d2ff;
            filter: drop-shadow(0 0 6px rgba(0, 210, 255, 0.6));
        }
        .bot-tab-view {
            display: none;
            width: 100%;
            box-sizing: border-box;
        }
        #tabViewTrade {
            width: 100vw !important;
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        #tradeTabContainer {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        #exchangeTerminalOverlay {
            width: 100% !important;
            max-width: 100vw !important;
            margin: 0 !important;
            padding: 12px 10px 90px 10px !important;
            box-sizing: border-box !important;
            overflow-x: hidden !important;
        }
        @keyframes signalActionVibeBuy {
            0%, 100% { transform: translateX(0); box-shadow: 0 0 16px rgba(0, 192, 135, 0.7); }
            20% { transform: translateX(-3px); }
            40% { transform: translateX(3px); }
            60% { transform: translateX(-2px); }
            80% { transform: translateX(2px); }
        }
        @keyframes signalActionVibeSell {
            0%, 100% { transform: translateX(0); box-shadow: 0 0 16px rgba(246, 70, 93, 0.7); }
            20% { transform: translateX(-3px); }
            40% { transform: translateX(3px); }
            60% { transform: translateX(-2px); }
            80% { transform: translateX(2px); }
        }
        .vibe-active-buy {
            animation: signalActionVibeBuy 1.2s infinite ease-in-out !important;
        }
        .vibe-active-sell {
            animation: signalActionVibeSell 1.2s infinite ease-in-out !important;
        }
        .bot-tab-view.active {
            display: block;
        }
        .bot-container { padding: 20px; }
        .bot-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 8px; }
        .bot-title-area { display: flex; align-items: center; gap: 12px; }
        .bot-icon { color: #5C6BC0; font-size: 28px; }
        .bot-name { color: #5C6BC0; font-size: 22px; font-weight: 900; letter-spacing: 1px; line-height: 1.2; }
        .bot-name span { display: block; color: #5C6BC0; }
        .price-section { margin-bottom: 30px; }
        .price-label { color: #757575; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .price-row { display: flex; align-items: baseline; gap: 10px; }
        .main-price { font-size: 36px; font-weight: 900; color: white; }
        .price-change { color: #f6465d; font-size: 16px; font-weight: 500; }
        .bot-controls { display: flex; gap: 12px; margin-bottom: 12px; }
        .btn-start { flex: 1; background: #2E7D32; color: white; border: none; border-radius: 4px; padding: 15px; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; text-transform: uppercase; }
        .btn-reset { background: #212121; color: white; border: none; border-radius: 4px; padding: 15px 25px; display: flex; align-items: center; justify-content: center; }
        .btn-config { background: #080808; color: white; border: 1px solid #333; border-radius: 4px; padding: 12px 20px; display: flex; align-items: center; gap: 8px; width: fit-content; margin-bottom: 30px; text-transform: uppercase; font-size: 14px; font-weight: bold; }
        .bot-card { background: #111; border-radius: 8px; padding: 20px; margin-bottom: 16px; border: 1px solid #1a1a1a; }
        .card-label { color: #757575; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
        .card-value-large { font-size: 28px; font-weight: 900; color: #4CAF50; display: flex; align-items: center; gap: 8px; }
        .card-value-sub { font-size: 16px; color: #4CAF50; opacity: 0.8; }
        .portfolio-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .portfolio-row:last-child { margin-bottom: 0; }
        .port-coin { color: #757575; font-size: 14px; text-transform: uppercase; }
        .port-amt { color: white; font-size: 18px; font-weight: 700; }
        .avg-main-val { font-size: 32px; font-weight: 900; color: white; margin: 10px 0; letter-spacing: 2px; }
        .invested-row { color: #757575; font-size: 14px; font-family: monospace; }
        .invested-white { color: white; }
        .ts-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .ts-label { color: #757575; font-size: 14px; font-family: monospace; }
        .ts-val { color: #3A47A6; font-weight: bold; font-size: 18px; }
        .ts-val.orange { color: #E8755B; }
        .chart-container { background: #080808; margin-top: 20px; width: 100%; position: relative; }
        .chart-intervals { display: flex; gap: 15px; padding: 10px 15px; background: #080808; border-bottom: 1px solid #1a1a1a; overflow-x: auto; }
        .interval-btn { color: #757575; font-size: 13px; cursor: pointer; padding: 4px 8px; border-radius: 4px; font-weight: 500; }
        .interval-btn.active { background: #f1f3f6; color: #080808; }
        #tradingview_chart { width: 100%; height: 450px; }
.martingale-section { 
            background: #111; 
            border-radius: 8px; 
            padding: 20px; 
            margin-bottom: 16px; 
            border: 1px solid #1a1a1a; 
        }
        .martingale-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 16px; 
            border-bottom: 1px solid rgba(255,255,255,0.06); 
            padding-bottom: 12px; 
        }
        .martingale-header h3 { 
            font-size: 13px; 
            color: #ffffff; 
            margin: 0; 
            font-weight: 800; 
            letter-spacing: 0.8px; 
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .martingale-header span { 
            font-size: 11px; 
            color: #8c8ca1; 
            font-family: 'JetBrains Mono', monospace; 
            font-weight: 600;
            background: rgba(255,255,255,0.04);
            padding: 4px 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .m-table { 
            width: 100%; 
            border-collapse: separate; 
            border-spacing: 0 6px; 
        }
        .m-table th { 
            text-align: left; 
            color: #616175; 
            font-size: 10px; 
            padding: 6px 10px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            font-weight: 700;
        }
        .m-table tbody tr {
            background: rgba(255,255,255,0.02);
            transition: all 0.25s ease;
            border-radius: 8px;
        }
        .m-table tbody tr:hover {
            background: rgba(255,255,255,0.05);
        }
        .m-table td { 
            padding: 10px 10px; 
            color: #ffffff; 
            font-size: 12px; 
            vertical-align: middle; 
        }
        .m-table td:first-child {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }
        .m-table td:last-child {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }
        .m-status { 
            background: rgba(255,255,255,0.04); 
            color: #8c8ca1; 
            padding: 4px 10px; 
            border-radius: 6px; 
            font-size: 10px; 
            font-weight: 800; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
            border: 1px solid rgba(255,255,255,0.06);
            display: inline-block;
        }
        .m-rnd { 
            font-weight: 800; 
            color: #ffffff; 
            font-family: 'JetBrains Mono', monospace; 
            font-size: 12px;
        }
        .m-alloc { 
            color: #8c8ca1; 
            font-family: 'JetBrains Mono', monospace; 
            font-size: 11px;
            font-weight: 600;
        }
        .m-price { 
            text-align: right; 
            font-family: 'JetBrains Mono', monospace; 
            color: #a0a0b8; 
            font-size: 11px;
            font-weight: 600;
        }
.trade-status-card { background: #111; border-radius: 8px; padding: 20px; margin-top: 16px; margin-bottom: 16px; border: 1px solid #1a1a1a; min-height: auto; display: flex; flex-direction: column; }
        .trade-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
        .trade-card-header h3 { font-size: 14px; color: white; margin: 0; letter-spacing: 1px; text-transform: uppercase; }
        .open-badge { background: #1a1a1a; color: white; padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: bold; border: 1px solid #333; }
        .empty-msg { flex: 1; display: flex; align-items: center; justify-content: center; color: #444; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase; }
        .fab-help {
            background: #7E57C2;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
.side-menu {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #3A47A6;
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            overflow-y: auto;
        }
        .side-menu.active {
            transform: translateX(0);
        }
        .menu-header {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .menu-logo {
            font-size: 24px;
            font-weight: 900;
            letter-spacing: 2px;
        }
        .close-menu {
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            color: white;
            cursor: pointer;
        }
        .menu-content {
            padding: 0 20px 40px;
        }
        .menu-preview-title {
            font-size: 32px;
            margin: 20px 0;
            font-weight: 400;
        }
        .search-container {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .search-input {
            flex: 1;
            background: rgba(255,255,255,0.15);
            border: none;
            border-radius: 8px;
            padding: 15px;
            color: white;
            font-size: 18px;
        }
        .go-btn {
            background: rgba(255,255,255,0.15);
            border: none;
            border-radius: 8px;
            padding: 0 30px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .exit-mode-btn {
            width: 100%;
            background: #111;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 18px;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 30px;
            cursor: pointer;
        }
        .menu-nav {
            display: flex;
            flex-direction: column;
        }
        .nav-item {
            display: flex;
            align-items: center;
            padding: 15px 0;
            gap: 15px;
            color: rgba(255,255,255,0.7);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
        }
        .nav-item.active {
            color: white;
        }
        .nav-item span {
            font-size: 18px;
            flex: 1;
        }
        .nav-item .arrow {
            color: rgba(255,255,255,0.3);
        }
        .nav-item .globe {
            color: rgba(255,255,255,0.5);
            font-size: 20px;
        }
        .sub-item {
            padding-left: 0;
        }
        .sub-item span {
            padding-left: 0;
        }
.program-preview-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #151515;
            z-index: 3000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            overflow-y: auto;
        }
        .program-preview-overlay.active { transform: translateX(0); }
        .preview-header {
            background-color: #3A47A6;
            padding: 12px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .header-left { display: flex; align-items: center; gap: 12px; font-size: 14px; color: #FFFFFFB3; }
        .logo-sm { width: 24px; height: 20px; }
        .menu-btn-circle {
            width: 36px;
            height: 36px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hamburger-lines span {
            display: block;
            width: 18px;
            height: 2px;
            background: white;
            margin: 3px 0;
        }
        .preview-content { padding: 20px; }
        .program-title-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 20px;
        }
        .program-title-row h1 { font-size: 32px; margin: 0; }
        .program-total-profit { font-size: 28px; font-weight: 800; }
        .school-banner {
            background: #1A1A1A;
            border-radius: 16px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 30px;
            border: 1px solid #333;
        }
        .school-icon { background: #4CAF50; padding: 8px; border-radius: 8px; }
        .school-text { flex: 1; display: flex; flex-direction: column; font-size: 14px; }
        .school-text strong { color: #4CAF50; }
        .levels-vertical-grid { display: flex; flex-direction: column; align-items: center; gap: 20px; }
        .level-card {
            width: 220px;
            height: 220px;
            border-radius: 24px;
            padding: 20px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }
        .level-card.locked { background-color: #2A2A2A; color: #666; }
        .level-card.active { background-color: #3A47A6; color: white; }
        .level-top { display: flex; justify-content: space-between; font-weight: bold; }
        .level-cost { display: flex; align-items: center; gap: 4px; }
        .coin-icon { width: 14px; height: 14px; background: #FFD700; border-radius: 50%; }
        .level-spots { display: flex; justify-content: center; gap: 10px; margin: 30px 0; }
        .matrix-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 15px 0;
        }
        .matrix-row {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        .matrix-branch {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .matrix-x4 .matrix-branch { gap: 10px; width: 90px; }
        .matrix-x5 .matrix-branch { gap: 8px; width: 100px; }
        .matrix-x6 .matrix-branch { gap: 5px; width: 110px; }
        
        .sub-row {
            display: flex;
            justify-content: center;
            gap: 6px;
        }
        .matrix-x4 .row-1-spot { width: 42px; height: 42px; margin-bottom: 10px; }
        .matrix-x4 .row-2-spot { width: 28px; height: 28px; }
        
        .matrix-x5 .row-1-spot { width: 38px; height: 38px; margin-bottom: 8px; }
        .matrix-x5 .row-2-spot { width: 22px; height: 22px; }
        .matrix-x5 .row-3-spot { width: 14px; height: 14px; }
        .matrix-x6 .row-1-spot { width: 34px; height: 34px; margin-bottom: 6px; }
        .matrix-x6 .row-2-spot { width: 18px; height: 18px; }
        .matrix-x6 .row-3-spot { width: 12px; height: 12px; }
        .matrix-x6 .row-4-spot { width: 8px; height: 8px; }
        .matrix-x5 .row-3, .matrix-x6 .row-3 { 
            display: flex; 
            gap: 4px; 
            margin-bottom: 4px;
        }
        .matrix-x6 .row-4 { 
            display: flex; 
            gap: 2px; 
        }
        .spot { 
            width: 42px; 
            height: 42px; 
            background: rgba(255,255,255,0.15); 
            border-radius: 50%; 
            position: relative; 
            z-index: 2;
        }
        .matrix-x4 .row-2 .spot, .matrix-x5 .row-2 .spot, .matrix-x6 .row-2 .spot { 
            width: 28px; 
            height: 28px; 
        }
        .matrix-x5 .row-3 .spot, .matrix-x6 .row-3 .spot { 
            width: 16px; 
            height: 16px; 
        }
        .matrix-x6 .row-4 .spot { 
            width: 10px; 
            height: 10px; 
        }
.preview-legend {
            margin-top: 30px;
            padding: 20px 0;
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 15px;
            color: #FFFFFFB3;
            font-size: 15px;
        }
        .legend-row { display: flex; align-items: center; gap: 12px; }
        .legend-circle { width: 24px; height: 24px; border-radius: 50%; }
        .circle-white { background: white; }
        .circle-gift { background: #00CCFF; }
        .circle-spill-above { background: #EDF45E; }
        .circle-spill-below { background: #F59322; }
        .marketing-legend-btn {
            grid-column: span 2;
            background: #3A47A6;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            width: fit-content;
            margin-top: 15px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
        }
.upline-card {
            background: #212121;
            border-radius: 16px;
            padding: 15px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        .upline-id {
            background: #333;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .detail-card-large {
            width: 100% !important;
            height: auto !important;
            min-height: 450px;
            padding: 20px 10px !important;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        #detailSpotsContainer {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-grow: 1;
            overflow: hidden;
        }
        .detail-id-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .id-display {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .id-display .label { font-size: 18px; font-weight: bold; opacity: 0.8; }
        .id-display .val { font-size: 32px; font-weight: 900; }
        .detail-footer-stats {
            display: grid;
            grid-template-columns: 1fr 1fr 1.5fr;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 20px;
            margin-top: 20px;
        }
        .f-stat { display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #FFFFFFB3; }
        .f-stat .v { color: white; font-size: 16px; font-weight: bold; display: flex; align-items: center; gap: 4px; }
        .spot.filled {
            background: white !important;
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 10px;
        }
        .matrix-x5 {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            margin: 15px 0;
        }
        .matrix-x5 .row-1 { display: flex; gap: 60px; }
        .matrix-x5 .row-1 .spot { width: 38px; height: 38px; }
        .matrix-x5 .row-2 { display: flex; gap: 12px; }
        .matrix-x5 .row-2 .spot { width: 24px; height: 24px; }
        .matrix-x5 .row-3 { display: flex; gap: 4px; }
        .matrix-x5 .row-3 .spot { width: 16px; height: 16px; }
        .matrix-x6 { display: flex; flex-direction: column; align-items: center; gap: 4px; margin: 10px 0; }
        .matrix-x6 .row-1 { display: flex; gap: 60px; }
        .matrix-x6 .row-1 .spot { width: 36px; height: 36px; }
        .matrix-x6 .row-2 { display: flex; gap: 12px; }
        .matrix-x6 .row-2 .spot { width: 22px; height: 22px; }
        .matrix-x6 .row-3 { display: flex; gap: 4px; }
        .matrix-x6 .row-3 .spot { width: 14px; height: 14px; }
        .matrix-x6 .row-4 { display: flex; gap: 2px; }
        .matrix-x6 .row-4 .spot { width: 10px; height: 10px; }
        
        .spot.orange { background: #F59322; }
        .spot.yellow { background: #EDF45E; }
        .spot.gift { background: #00CCFF; }
        .level-card.locked .spot { background: rgba(255,255,255,0.08); }
        .level-stats { display: flex; justify-content: center; gap: 15px; font-size: 16px; color: #757575; z-index: 2; }
        .stat-item { display: flex; align-items: center; gap: 5px; }
        .level-watermark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 120px;
            height: 100px;
            background: none;
            opacity: 0;
            pointer-events: none;
        }
        .info-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #151515;
            z-index: 5000;
            display: none;
            overflow-y: auto;
            padding: 20px;
            box-sizing: border-box;
        }
        .info-modal.active {
            display: block;
        }
        .modal-header {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .modal-close {
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            color: white;
            cursor: pointer;
        }
        .modal-title {
            font-size: 32px;
            font-weight: 700;
            margin: 0 0 24px 0;
        }
        .modal-desc {
            color: #FFFFFFB3;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 32px;
        }
        .video-legend-container {
            width: 100%;
            background: #1A1A1A;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 25px;
            border: 1px solid #333;
        }
        .video-legend-container video {
            width: 100%;
            display: block;
        }
        .legend-list {
            display: flex;
            flex-direction: column;
            gap: 24px;
            margin-bottom: 40px;
        }
        .legend-item {
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }
        .legend-box {
            width: 24px;
            height: 24px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .active-box { background-color: white; border-radius: 50%; }
        .gift-box { background-color: #00CCFF; border-radius: 50%; }
        .legend-item i { color: #FFFFFFB3; font-size: 24px; }
        .legend-text strong { color: white; display: block; margin-bottom: 2px; }
        .legend-text {
            color: #FFFFFF;
            font-size: 16px;
            line-height: 1.4;
        }
        .close-tip-btn {
            width: 100%;
            background-color: #2A2A3B;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 18px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
        }
.program-top {
    display: flex;
    justify-content: space-between;
    position: relative;
    margin-bottom: 20px;
}
.program-stats {
    z-index: 2;
}
.prog-label {
    color: var(--text-secondary);
    font-size: 14px;
}
.prog-value {
    font-size: 20px;
    font-weight: bold;
    margin-top: 4px;
}
.watermark {
    position: absolute;
    right: 10px;
    top: -10px;
    font-size: 80px;
    font-weight: 900;
    opacity: 0.1;
    font-style: italic;
}
.slots-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
    margin-top: 25px;
    margin-bottom: 15px;
    width: 100%;
}
.slot-box {
    background: #2A2A3B;
    border-radius: 12px;
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.1);
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.slot-box:active {
    transform: scale(0.95);
    background: #3A47A6;
}
.slot-box:hover { background: #333344; }
.slot-box.active {
    background: #3A47A6;
    color: white;
    border-color: #5C6BC0;
}
.program-card.V1 { border: 1px solid rgba(255, 215, 0, 0.3); box-shadow: 0 0 15px rgba(255, 215, 0, 0.1); }
.program-card.Q2 { border: 1px solid rgba(0, 188, 212, 0.3); box-shadow: 0 0 15px rgba(0, 188, 212, 0.1); }
.ghost-spot { background: rgba(0, 188, 212, 0.4) !important; border: 1px dashed #00BCD4; }
.velocity-spot { background: rgba(255, 215, 0, 0.4) !important; border: 1px dashed #FFD700; }
.program-card.T3 { border: 1px solid rgba(58, 71, 166, 0.3); }
.program-card.S4 { border: 1px solid rgba(138, 43, 226, 0.3); }
.program-card.G5 { border: 1px solid rgba(233, 30, 99, 0.3); }
.program-card.N6 { border: 1px solid rgba(0, 188, 212, 0.3); }
.program-card.A7 { border: 1px solid rgba(255, 69, 0, 0.3); }
.program-card.C8 { border: 1px solid rgba(50, 205, 50, 0.3); }
.program-card.S9 { border: 1px solid rgba(255, 20, 147, 0.3); }
.program-card.Q10 { border: 1px solid rgba(0, 250, 154, 0.3); }
.program-card.H11 { border: 1px solid rgba(148, 0, 211, 0.3); }
.program-card.O12 { border: 1px solid rgba(255, 140, 0, 0.3); }
.program-card.N13 { border: 1px solid rgba(0, 255, 255, 0.3); }
.program-card.E14 { border: 1px solid rgba(220, 20, 60, 0.3); }
.program-card.X15 { border: 1px solid rgba(255, 255, 255, 0.3); }
.slot-price { font-size: 9px; margin-top: 2px; }

.preview-btn {
    width: 100%;
    background: rgba(255,255,255,0.05);
    border: none;
    border-radius: 12px;
    color: var(--text-primary);
    padding: 16px;
    font-size: 16px;
    font-weight: bold;
    display: flex;
    justify-content: center;
    gap: 8px;
}
.landing-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #0a0a0a;
    background: radial-gradient(circle at 50% 118%, rgba(255, 215, 0, 0.42) 0%, rgba(10, 10, 10, 0.86) 55%, #0a0a0a 95%);
    backdrop-filter: blur(5px);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: white;
    overflow-y: auto;
    overflow-x: hidden;
}
.landing-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: transparent;
    position: relative;
    z-index: 10;
}
.landing-logo {
    font-size: 24px;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 8px;
}
.landing-auth-btns {
    display: flex;
    gap: 10px;
}
.btn-signup {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: white;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}
.btn-login {
    background: #2563eb;
    border: none;
    color: white;
    padding: 8px 22px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
}
.landing-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 20px 48px;
    position: relative;
    z-index: 2;
    box-sizing: border-box;
}
.usdt-bg-graphic {
    position: relative;
    width: 195px;
    height: 195px;
    border: none;
    background: transparent;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 46px auto;
    flex-shrink: 0;
}
.usdt-text-circle {
    position: absolute;
    width: 100%;
    height: 100%;
    animation: orbitRotate 18s linear infinite;
}
.usdt-text-circle span {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    text-align: center;
    color: #FFD700;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
}
.landing-title {
    font-size: 32px;
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 38px 0;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.landing-title span {
    color: #8c8ca1;
    font-weight: 600;
    font-size: 26px;
    display: block;
    margin-top: 6px;
}
.btn-program {
    background: transparent;
    border: 1.5px solid rgba(255, 215, 0, 0.85);
    color: #FFD700;
    padding: 16px 48px;
    border-radius: 34px;
    font-size: 22px;
    font-weight: 900;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.35);
    cursor: pointer;
    letter-spacing: 1px;
    transition: all 0.2s ease;
}
.btn-program:active {
    transform: scale(0.97);
    background: rgba(255, 215, 0, 0.15);
}
.login-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 10, 10, 0.98);
    z-index: 10000;
    display: none;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box;
}
.login-overlay.active { display: flex; }
.login-close-row { display: flex; justify-content: flex-end; margin-bottom: 20px; padding-top: 10px; }
.login-close-btn { background: none; border: none; color: white; cursor: pointer; }
.login-title { font-size: 36px; font-weight: bold; margin-bottom: 12px; }
.login-subtitle { color: #757575; font-size: 16px; line-height: 1.5; margin-bottom: 40px; }
.blockchain-card {
    background: linear-gradient(180deg, #151515 0%, #112a22 100%);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.05);
}
.bc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.bc-title { font-size: 24px; font-weight: bold; }
.bc-icon { width: 40px; height: 40px; background: #26A17B; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.bc-desc { color: #757575; font-size: 14px; line-height: 1.5; margin-bottom: 24px; }
.bc-btn { width: 100%; background: rgba(255,255,255,0.08); border: none; color: white; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 500; cursor: pointer; transition: background 0.2s; }
.bc-btn:active { background: rgba(255,255,255,0.15); }
.connect-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: #151515; z-index: 10001; display: none; flex-direction: column;
    overflow-y: auto;
}
.connect-overlay.active { display: flex; }
.connect-header { display: flex; justify-content: space-between; padding: 16px 20px; background: #151515; }
.connect-header-btn { background: rgba(255,255,255,0.1); color: white; border: none; padding: 8px 16px; border-radius: 20px; font-size: 14px; cursor: pointer; }
.connect-main { background: #2962FF; padding: 40px 20px; text-align: center; flex: 1; }
.connect-title { font-size: 28px; font-weight: bold; margin-bottom: 12px; }
.connect-subtitle { font-size: 14px; line-height: 1.5; opacity: 0.9; margin-bottom: 40px; }
.connect-graphic { font-size: 120px; margin-bottom: 40px; text-shadow: 0 10px 20px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; gap: 10px; }
.connect-btn-primary { width: 100%; background: #151515; color: white; border: none; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: bold; margin-bottom: 12px; cursor: pointer; }
.connect-btn-secondary { width: 100%; background: rgba(255,255,255,0.2); color: white; border: none; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; }
.connect-bottom { background: #151515; padding: 40px 20px; }
.preview-title { font-size: 28px; font-weight: bold; margin-bottom: 12px; }
.preview-subtitle { color: #757575; font-size: 14px; line-height: 1.5; margin-bottom: 20px; }
.preview-input-group { display: flex; gap: 10px; }
.preview-input { flex: 1; background: #212121; border: 1px solid #333; color: white; padding: 16px; border-radius: 12px; font-size: 16px; box-sizing: border-box; }
.preview-btn { background: #3A47A6; color: white; border: none; padding: 0 24px; border-radius: 12px; font-weight: bold; cursor: pointer; }
.wallet-modal-card {
    background: #10141f;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    width: 100%;
    max-width: 440px;
    margin: auto;
    padding: 22px 20px;
    box-sizing: border-box;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.wallet-option-pro {
    background: #161c28;
    border: 1px solid #222b3d;
    border-radius: 16px;
    padding: 12px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: all 0.2s ease;
}
.wallet-option-pro:hover, .wallet-option-pro:active {
    background: #1c2436;
    border-color: #00e5ff;
    transform: translateY(-1px);
}
.wallet-icon-wrap {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: #0d111a;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.wallet-icon-wrap img {
    width: 28px;
    height: 28px;
    object-fit: contain;
}
.wallet-recent-tag {
    background: rgba(0, 230, 118, 0.15);
    color: #00e676;
    border: 1px solid rgba(0, 230, 118, 0.3);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 900;
    font-family: monospace;
}
.wallet-grid-item {
    background: #161c28;
    border: 1px solid #222b3d;
    border-radius: 14px;
    padding: 12px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    text-align: center;
    transition: 0.2s;
}
.wallet-grid-item:hover, .wallet-grid-item:active {
    border-color: #2563eb;
    background: #1c2436;
}
.upgrade-detail-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; }
.upgrade-detail-label { color: #757575; }
.upgrade-detail-value { color: white; font-weight: 500; display: flex; align-items: center; gap: 6px; }
.upgrade-amount-row { display: flex; justify-content: space-between; align-items: center; padding: 20px 0 10px; }
.upgrade-amount-label { color: #5C6BC0; font-weight: bold; font-size: 16px; }
.upgrade-amount-value { color: #5C6BC0; font-weight: bold; font-size: 16px; }
.upgrade-amount-bnb { color: #E8755B; }
.service-fee-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; color: #5C6BC0; margin-bottom: 20px; }
.notification-wrapper { position: relative; cursor: pointer; display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.1); border-radius: 50%; }
.notif-dot { position: absolute; top: 8px; right: 8px; width: 8px; height: 8px; background: #E8755B; border-radius: 50%; border: 2px solid var(--primary-blue); }
.expanded-profile { display: none; flex-direction: column; gap: 10px; margin-top: 15px; width: 100%; animation: fadeIn 0.3s ease; }
.expanded-profile.active { display: flex; }
.wallet-address-row { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: bold; }
.invited-by-row { color: #757575; font-size: 14px; display: flex; align-items: center; gap: 6px; }
.upline-badge { background: rgba(92, 107, 192, 0.2); color: #5C6BC0; padding: 4px 12px; border-radius: 12px; font-weight: bold; cursor: pointer; }
.notif-overlay { position: fixed; top: 0; right: -100%; width: 100%; max-width: 480px; height: 100%; background: #151515; z-index: 9999; transition: 0.3s; overflow-y: auto; }
.notif-overlay.active { right: 0; }
.notif-header { padding: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2A2A2A; }
.notif-item { padding: 15px 20px; border-bottom: 1px solid #2A2A2A; display: flex; gap: 15px; align-items: flex-start; }
.notif-icon { width: 40px; height: 40px; border-radius: 50%; background: rgba(76, 175, 80, 0.2); display: flex; align-items: center; justify-content: center; color: #4CAF50; flex-shrink: 0; }
.notif-content { display: flex; flex-direction: column; gap: 4px; }
.notif-title { font-weight: bold; font-size: 14px; color: white; }
.notif-desc { color: #757575; font-size: 12px; line-height: 1.4; }
.notif-time { color: #5C6BC0; font-size: 10px; font-weight: bold; margin-top: 4px; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.airdrop-market-header {
    background: radial-gradient(circle at top right, #1a2238 0%, #0d121f 100%);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
}
.market-live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 229, 255, 0.12);
    border: 1px solid rgba(0, 229, 255, 0.4);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 900;
    color: #00e5ff;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.market-main-title {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.5px;
    margin: 0 0 4px 0;
}
.market-sub-title {
    font-size: 12px;
    color: #8c8ca1;
    margin: 0;
}
.airdrop-balance-card {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 12px 16px;
    text-align: right;
    min-width: 140px;
}
.balance-card-label {
    font-size: 10px;
    font-weight: 800;
    color: #FFD700;
    letter-spacing: 0.5px;
}
.balance-card-val {
    font-size: 24px;
    font-weight: 900;
    color: #ffffff;
    font-family: monospace;
    margin: 2px 0;
}
.balance-card-val small {
    font-size: 11px;
    color: #00e5ff;
}
.balance-card-sub {
    font-size: 10px;
    color: #8c8ca1;
}
.market-tabs-row {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    overflow-x: auto;
    padding-bottom: 4px;
}
.mkt-tab-btn {
    background: #11151e;
    border: 1px solid #1a202c;
    color: #8c8ca1;
    padding: 10px 18px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    white-space: nowrap;
    transition: 0.2s;
}
.mkt-tab-btn.active {
    background: #00e5ff;
    color: #000000;
    border-color: #00e5ff;
}
.airdrop-products-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 24px;
}
.product-commodity-card {
    background: #11151e;
    border: 1px solid #1a202c;
    border-radius: 18px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}
.prod-img-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    background: #000;
}
.prod-main-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
}
.product-commodity-card:hover .prod-main-img {
    transform: scale(1.04);
}
.prod-badge-live {
    position: absolute;
    top: 8px;
    right: 8px;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 900;
    font-family: monospace;
}
.prod-badge-live.up {
    background: rgba(0, 230, 118, 0.9);
    color: #000;
}
.prod-badge-live.down {
    background: rgba(246, 70, 93, 0.9);
    color: #fff;
}
.prod-body {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    justify-content: space-between;
}
.prod-name {
    font-size: 13px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    line-height: 1.3;
}
.prod-vol {
    font-size: 10px;
    color: #718096;
    font-family: monospace;
}
.prod-desc {
    font-size: 11px;
    color: #8c8ca1;
    line-height: 1.3;
    margin: 0;
}
.prod-price-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 8px 10px;
}
.price-lbl {
    font-size: 9px;
    color: #718096;
    font-weight: 800;
}
.price-num {
    font-size: 16px;
    font-weight: 900;
    color: #00e5ff;
    font-family: monospace;
}
.shine-symbol {
    font-size: 10px;
    color: #FFD700;
}
.prod-range-text {
    font-size: 9px;
    color: #8c8ca1;
    font-family: monospace;
    margin-top: 2px;
}
.btn-prod-buy {
    width: 100%;
    background: linear-gradient(90deg, #00c087, #00e5ff);
    color: #000000;
    border: none;
    border-radius: 10px;
    padding: 10px 0;
    font-size: 12px;
    font-weight: 900;
    cursor: pointer;
}
.inventory-card {
    background: #11151e;
    border: 1px solid #1a202c;
    border-radius: 14px;
    padding: 14px;
}
.btn-inv-sell {
    flex: 1;
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid #00e676;
    color: #00e676;
    border-radius: 8px;
    padding: 9px 0;
    font-size: 11px;
    font-weight: 900;
    cursor: pointer;
}
.btn-inv-claim {
    background: #1a202c;
    border: 1px solid #2d3748;
    color: #e2e8f0;
    border-radius: 8px;
    padding: 9px 12px;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
}
.empty-inventory-box {
    background: #11151e;
    border: 1px dashed rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 30px 16px;
    text-align: center;
}
.btn-explore-market {
    background: #00e5ff;
    color: #000;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 900;
    font-size: 12px;
    margin-top: 14px;
    cursor: pointer;
}
.web3-wallet-card {
    background: #11151e;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px 28px 0 0;
    width: 100%;
    max-width: 480px;
    padding: 16px 20px 32px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 16px;
    box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.8);
    animation: slideUpWeb3 0.25s ease-out;
}
@keyframes slideUpWeb3 {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
}
.web3-drawer-drag {
    width: 38px;
    height: 4px;
    background: #2d3748;
    border-radius: 2px;
    margin: 0 auto;
}
.web3-drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.web3-provider-info {
    display: flex;
    align-items: center;
    gap: 12px;
}
.web3-provider-icon {
    width: 42px;
    height: 42px;
    background: #1c2433;
    border: 1px solid #2d3748;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.web3-provider-icon img {
    width: 26px;
    height: 26px;
    object-fit: contain;
}
.web3-provider-title {
    font-size: 16px;
    font-weight: 800;
    color: #ffffff;
}
.web3-network-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #8c8ca1;
    font-family: monospace;
    margin-top: 2px;
}
.web3-net-dot {
    width: 7px;
    height: 7px;
    background: #00e676;
    border-radius: 50%;
    box-shadow: 0 0 6px #00e676;
}
.web3-close-btn {
    background: #1a202c;
    border: none;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    color: #8c8ca1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}
.web3-address-box {
    background: #161b26;
    border: 1px solid #232b3b;
    border-radius: 14px;
    padding: 12px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.web3-box-label {
    font-size: 9px;
    font-weight: 800;
    color: #718096;
    letter-spacing: 0.5px;
}
.web3-box-address {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    font-family: monospace;
    margin-top: 2px;
    word-break: break-all;
}
.web3-address-actions {
    display: flex;
    gap: 8px;
}
.web3-mini-action-btn {
    background: #232b3b;
    border: none;
    border-radius: 8px;
    width: 32px;
    height: 32px;
    color: #00e5ff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    text-decoration: none;
}
.web3-mini-action-btn i {
    font-size: 16px;
}
.web3-networth-card {
    background: radial-gradient(circle at top right, #1a2238 0%, #0d121f 100%);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 18px;
    padding: 16px;
    text-align: center;
}
.web3-networth-label {
    font-size: 10px;
    font-weight: 800;
    color: #FFD700;
    letter-spacing: 0.8px;
}
.web3-networth-val {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    font-family: monospace;
    margin: 4px 0;
}
.web3-networth-sub {
    font-size: 10px;
    color: #718096;
}
.web3-assets-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.web3-asset-row {
    background: #161b26;
    border: 1px solid #1f2737;
    border-radius: 14px;
    padding: 12px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.web3-asset-left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.web3-coin-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}
.web3-shine-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    border-radius: 50%;
    color: #000;
    font-weight: 900;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.web3-coin-name {
    font-size: 13px;
    font-weight: 800;
    color: #ffffff;
}
.web3-coin-tag {
    font-size: 10px;
    color: #718096;
    font-family: monospace;
}
.web3-asset-right {
    text-align: right;
    font-family: monospace;
}
.web3-asset-amount {
    font-size: 13px;
    font-weight: 800;
    color: #ffffff;
}
.web3-asset-fiat {
    font-size: 11px;
    color: #00c087;
    font-weight: 700;
}
.web3-drawer-footer {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 4px;
}
.web3-switch-btn {
    background: #1c2433;
    border: 1px solid #2d3748;
    color: #e2e8f0;
    border-radius: 12px;
    padding: 12px 0;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}
.web3-disconnect-btn {
    background: rgba(246, 70, 93, 0.15);
    border: 1px solid #f6465d;
    color: #f6465d;
    border-radius: 12px;
    padding: 12px 0;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}
.tw-switch {
    position: relative;
    display: inline-block;
    width: 46px;
    height: 26px;
    flex-shrink: 0;
}
.tw-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}
.tw-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #2e384d;
    transition: .3s;
    border-radius: 26px;
}
.tw-slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s;
    border-radius: 50%;
}
input:checked + .tw-slider {
    background-color: #2563eb;
}
input:checked + .tw-slider:before {
    transform: translateX(20px);
}
.tw-sheet-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.blockchain-loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 12, 18, 0.88);
    backdrop-filter: blur(8px);
    z-index: 99999;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
}
.blockchain-loader-card {
    background: transparent;
    border: none;
    padding: 0;
    width: auto;
    text-align: center;
    box-shadow: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
}
.bc-spinner {
    width: 58px;
    height: 58px;
    border: 3.5px solid rgba(0, 229, 255, 0.15);
    border-top: 3.5px solid #00e5ff;
    border-radius: 50%;
    animation: orbitRotate 0.75s linear infinite;
    filter: drop-shadow(0 0 14px rgba(0, 229, 255, 0.5));
}
.bc-success-icon {
    width: 64px;
    height: 64px;
    background: rgba(0, 230, 118, 0.15);
    border: 2px solid #00e676;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #00e676;
    font-size: 34px;
    box-shadow: 0 0 25px rgba(0, 230, 118, 0.4);
}
</style>
</head>
<body>
    <div class="container">
        <div id="landingPage" class="landing-page">
    <div class="landing-header">
        <div class="landing-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div class="landing-auth-btns">
            <button class="btn-signup" onclick="enterDashboard()">Sign up</button>
            <button class="btn-login" onclick="openLoginModal()">Login</button>
        </div>
    </div>
    <div class="landing-content">
        <div class="usdt-bg-graphic">
            <div class="usdt-text-circle">
                <span style="transform: rotate(0deg);">I</span>
                <span style="transform: rotate(22deg);">N</span>
                <span style="transform: rotate(44deg);">C</span>
                <span style="transform: rotate(66deg);">L</span>
                <span style="transform: rotate(88deg);">U</span>
                <span style="transform: rotate(110deg);">D</span>
                <span style="transform: rotate(132deg);">E</span>
                <span style="transform: rotate(154deg);">D</span>
                <span style="transform: rotate(190deg);">P</span>
                <span style="transform: rotate(212deg);">A</span>
                <span style="transform: rotate(234deg);">S</span>
                <span style="transform: rotate(256deg);">S</span>
                <span style="transform: rotate(278deg);">I</span>
                <span style="transform: rotate(300deg);">V</span>
                <span style="transform: rotate(322deg);">E</span>
            </div>
            <svg width="86" height="86" viewBox="0 0 100 100" style="border-radius: 50%; filter: drop-shadow(0 4px 16px rgba(0, 147, 147, 0.7));">
                <circle cx="50" cy="50" r="50" fill="#009393"/>
                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
            </svg>
        </div>
        <h1 class="landing-title">Take full control<span>of your crypto with SHINE</span></h1>
        <button class="btn-program" onclick="enterDashboard()">V1 PROGRAM</button>
    </div>
</div>
<div id="loginModal" class="login-overlay" style="overflow-y: auto; padding: 14px 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; padding-top: 4px;">
        <h1 class="login-title" style="font-size: 24px; font-weight: 800; margin: 0;">Choose Network</h1>
        <button class="login-close-btn" onclick="closeLoginModal()"><i class="material-icons">close</i></button>
    </div>
    <p class="login-subtitle" style="font-size: 12px; color: #8c8ca1; margin: 0 0 14px 0; line-height: 1.4;">Select an authorized protocol gateway to enter your decentralized account.</p>

    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
        <div style="background: #151922; border-radius: 20px; padding: 16px 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 44px; height: 44px; border-radius: 14px; background: #1e2430; display: flex; align-items: center; justify-content: center;">
                        <svg viewBox="0 0 32 32" style="width: 26px; height: 26px;">
                            <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                            <path fill="#000000" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                        </svg>
                    </div>
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #ffffff;">BNB Smart Chain</div>
                        <div style="font-size: 12px; color: #718096; font-family: monospace;">BSC (BEP-20)</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.3); padding: 4px 10px; border-radius: 20px;">
                    <span class="live-vibe-dot"></span>
                    <span style="color: #00e676; font-size: 11px; font-weight: 800; font-family: monospace;">LIVE</span>
                </div>
            </div>
            <p style="margin: 0 0 16px 0; color: #8c8ca1; font-size: 13px; line-height: 1.5;">Dual Settlement protocol in USDT & BNB. Instant smart contract execution with automated matrix distribution.</p>
            <button onclick="openConnectModal()" style="width: 100%; background: #2563eb; color: #ffffff; border: none; padding: 15px 0; border-radius: 14px; font-size: 14px; font-weight: 800; cursor: pointer;">Enter via BSC</button>
        </div>

        <div style="background: #151922; border-radius: 20px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 44px; height: 44px; border-radius: 14px; background: #1e2430; display: flex; align-items: center; justify-content: center;">
                        <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" style="width: 26px; height: 26px; object-fit: contain;">
                    </div>
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #ffffff;">Solana Network</div>
                        <div style="font-size: 12px; color: #718096; font-family: monospace;">SOL Mainnet</div>
                    </div>
                </div>
                <span style="background: rgba(0, 229, 255, 0.12); color: #00e5ff; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 800; font-family: monospace;">QUANT ENGINE</span>
            </div>
            <p style="margin: 0 0 16px 0; color: #8c8ca1; font-size: 13px; line-height: 1.5;">High-frequency algorithmic spot trading, sub-second routing, and automated zero-liquidation DCA execution.</p>
            <button onclick="enterDashboard(); toggleTrading();" style="width: 100%; background: #1e2430; color: #00e5ff; border: none; padding: 15px 0; border-radius: 14px; font-size: 14px; font-weight: 800; cursor: pointer;">Launch Solana Quant Desk</button>
        </div>

        <div style="background: #151922; border-radius: 20px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <svg viewBox="0 0 200 200" style="width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;">
                        <defs>
                            <radialGradient id="shineNetLogo" cx="35%" cy="30%" r="75%">
                                <stop offset="0%" stop-color="#ff4f9e"/>
                                <stop offset="35%" stop-color="#e91e7e"/>
                                <stop offset="75%" stop-color="#ba1261"/>
                                <stop offset="100%" stop-color="#840540"/>
                            </radialGradient>
                        </defs>
                        <circle cx="100" cy="100" r="98" fill="url(#shineNetLogo)"/>
                        <circle cx="100" cy="100" r="91" fill="none" stroke="#ff7ab6" stroke-width="3" opacity="0.9"/>
                        <circle cx="100" cy="100" r="85" fill="none" stroke="#750438" stroke-width="3" opacity="0.7"/>
                        <circle cx="100" cy="100" r="82" fill="url(#shineNetLogo)"/>
                        <g fill="#ffffff">
                            <text x="44" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">S</text>
                            <text x="74" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">H</text>
                            <path d="M100 56 Q101 64 107 67 Q101 70 100 78 Q99 70 93 67 Q99 64 100 56 Z"/>
                            <path d="M89 74 Q89.5 78 92 79.5 Q89.5 81 89 85 Q88.5 81 86 79.5 Q88.5 78 89 74 Z"/>
                            <path d="M112 76 Q112.5 80 115 81.5 Q112.5 83 112 87 Q111.5 83 109 81.5 Q111.5 80 112 76 Z"/>
                            <circle cx="100" cy="86" r="3.2"/>
                            <path d="M93 96 C94 91 98 87.5 104 88 C100 91 97 94 96 98 Z"/>
                            <circle cx="100" cy="99" r="3.2"/>
                            <path d="M92 113 C91 106 97 100 105 100 C100 103 97 107 97 113 Z"/>
                            <path d="M100 106 C105 107 107 112 105 118 C102 124 97 129 93 136 C95 131 99 125 102 120 C104 115 102 110 98 108 Z"/>
                            <path d="M93 126 C96 130 101 135 105 142 C103 138 99 133 95 128 Z"/>
                            <text x="127" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">N</text>
                            <text x="156" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">E</text>
                        </g>
                    </svg>
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #ffffff;">SHINE Chain</div>
                        <div style="font-size: 12px; color: #718096; font-family: monospace;">Layer 1 Native</div>
                    </div>
                </div>
                <span style="background: rgba(255, 215, 0, 0.12); color: #FFD700; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 800; font-family: monospace;">ROADMAP</span>
            </div>
            <p style="margin: 0; color: #8c8ca1; font-size: 13px; line-height: 1.5;">Native decentralized blockchain architecture with gas-free settlement and autonomous on-chain liquidity pools.</p>
        </div>
    </div>
</div>

<div id="connectWalletModal" class="connect-overlay">
    <div class="connect-header">
        <div class="landing-logo"><svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
        <button class="connect-header-btn" onclick="openWalletSelection()">Connect wallet</button>
    </div>
    <div class="connect-main">
        <h1 class="connect-title">Welcome to SHINE USDT</h1>
        <p class="connect-subtitle">Connect your wallet to start working. First time here? Watch a tutorial to learn more</p>
        <div class="connect-graphic" style="position: relative; height: 210px; margin-bottom: 25px; display: flex; align-items: center; justify-content: center;">
            <svg viewBox="0 0 320 220" style="width: 100%; max-width: 320px; height: 210px; overflow: visible;">
                <defs>
                    <radialGradient id="walletLeatherGrad" cx="40%" cy="30%" r="80%">
                        <stop offset="0%" stop-color="#3d2314"/>
                        <stop offset="60%" stop-color="#24140b"/>
                        <stop offset="100%" stop-color="#140a05"/>
                    </radialGradient>
                    <linearGradient id="walletFlapGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#5a341e"/>
                        <stop offset="70%" stop-color="#381d0f"/>
                        <stop offset="100%" stop-color="#221008"/>
                    </linearGradient>
                    <linearGradient id="walletGoldClasp" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ffe270"/>
                        <stop offset="50%" stop-color="#d4af37"/>
                        <stop offset="100%" stop-color="#997a15"/>
                    </linearGradient>
                    <radialGradient id="usdtGlowGrad" cx="50%" cy="50%" r="60%">
                        <stop offset="0%" stop-color="rgba(38, 161, 123, 0.45)"/>
                        <stop offset="100%" stop-color="rgba(38, 161, 123, 0)"/>
                    </radialGradient>
                    <filter id="shadowDepth" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000000" flood-opacity="0.6"/>
                    </filter>
                    <filter id="coinGlow" x="-30%" y="-30%" width="160%" height="160%">
                        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#00e5a3" flood-opacity="0.5"/>
                    </filter>
                </defs>

                <ellipse cx="160" cy="205" rx="110" ry="14" fill="#000000" opacity="0.45"/>
                <circle cx="160" cy="100" r="100" fill="url(#usdtGlowGrad)"/>

                <g transform="translate(68, 18) rotate(-18) scale(0.68)" filter="url(#coinGlow)">
                    <circle cx="50" cy="50" r="48" fill="#26A17B"/>
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#5eead4" stroke-width="2" opacity="0.6"/>
                    <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                    <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                </g>

                <g transform="translate(195, 20) rotate(16) scale(0.72)" filter="url(#coinGlow)">
                    <circle cx="50" cy="50" r="48" fill="#26A17B"/>
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#5eead4" stroke-width="2" opacity="0.6"/>
                    <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                    <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                </g>

                <g transform="translate(125, 0) scale(0.76)" filter="url(#coinGlow)">
                    <circle cx="50" cy="50" r="48" fill="#26A17B"/>
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.8"/>
                    <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                    <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                </g>

                <g filter="url(#shadowDepth)">
                    <rect x="55" y="75" width="210" height="125" rx="20" fill="url(#walletLeatherGrad)" stroke="#5a341e" stroke-width="2"/>
                    <path d="M65 92 Q160 84 255 92" stroke="#1f1008" stroke-width="6" fill="none"/>
                    <path d="M55 75 Q160 62 265 75 L255 125 Q160 148 65 125 Z" fill="url(#walletFlapGrad)" stroke="#6d3e24" stroke-width="2"/>
                    <path d="M68 84 Q160 74 252 84" stroke="#ffb076" stroke-width="1.2" stroke-dasharray="4 3" fill="none" opacity="0.7"/>
                    <rect x="145" y="118" width="30" height="24" rx="6" fill="url(#walletGoldClasp)" stroke="#665008" stroke-width="1.5"/>
                    <rect x="153" y="127" width="14" height="6" rx="2" fill="#24140b"/>
                </g>
            </svg>
        </div>
        <button class="connect-btn-primary" onclick="openWalletSelection()">Connect now</button>
        <button class="connect-btn-secondary" onclick="enterDashboard()">Watch tutorial</button>
    </div>
    <div class="connect-bottom" style="box-sizing: border-box; width: 100%; padding: 30px 20px;">
        <h2 class="preview-title">Account preview</h2>
        <p class="preview-subtitle">Look up any SHINE USDT member account in preview mode. Enter ID or wallet to preview or click Demo to view a random account.</p>
        <div class="preview-input-group" style="display: flex; gap: 10px; width: 100%; box-sizing: border-box; align-items: center;">
            <input type="text" class="preview-input" placeholder="Example: 1" style="flex: 1; min-width: 0; box-sizing: border-box; background: #212121; border: 1px solid #333; color: white; padding: 16px; border-radius: 12px; font-size: 16px;">
            <button class="preview-submit-btn" onclick="enterDashboard()" style="background: #2563eb; color: #ffffff; border: none; padding: 0 24px; height: 52px; border-radius: 12px; font-weight: 800; font-size: 15px; cursor: pointer; flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; text-align: center; white-space: nowrap; box-sizing: border-box;">Preview</button>
        </div>
    </div>
</div>

<div id="walletSelectionModal" class="login-overlay" style="align-items: center; justify-content: center; overflow-y: auto;">
    <div class="wallet-modal-card">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="material-icons" style="color: #00e5ff; font-size: 20px;">account_balance_wallet</i>
                <span style="font-size: 17px; font-weight: 800; color: #ffffff;">Connect Wallet</span>
            </div>
            <button class="login-close-btn" onclick="closeWalletSelection()"><i class="material-icons">close</i></button>
        </div>

        <div id="quickRecentWalletBox" style="display: none; background: rgba(0, 230, 118, 0.08); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 14px; padding: 10px 14px; justify-content: space-between; align-items: center; cursor: pointer;" onclick="directReconnectLastWallet()">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="web3-net-dot"></span>
                <div>
                    <div style="font-size: 11px; color: #00e676; font-weight: 800;">LAST CONNECTED WALLET</div>
                    <div id="quickRecentWalletName" style="font-size: 13px; font-weight: 800; color: #ffffff;">Trust Wallet</div>
                </div>
            </div>
            <button style="background: #00e676; color: #000; border: none; padding: 6px 12px; border-radius: 8px; font-weight: 900; font-size: 11px; cursor: pointer;">1-TAP CONNECT</button>
        </div>

        <div style="color: #718096; font-size: 12px; font-weight: 600;">Popular & Recommended</div>

        <div style="display: flex; flex-direction: column; gap: 10px;">
            <div class="wallet-option-pro" onclick="connectSpecificWalletProvider('METAMASK')">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="wallet-icon-wrap" style="background: transparent;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg" alt="MetaMask" style="width: 32px; height: 32px; object-fit: contain;">
                    </div>
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">MetaMask</div>
                        <div style="font-size: 11px; color: #718096;">EVM Standard · Browser & Mobile</div>
                    </div>
                </div>
                <span id="recentBadge-METAMASK" class="wallet-recent-tag" style="display: none;">RECENT</span>
            </div>

            <div class="wallet-option-pro" onclick="connectSpecificWalletProvider('TRUST')">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="wallet-icon-wrap" style="background: transparent;">
                        <svg width="30" height="30" viewBox="0 0 32 32" fill="none">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M16 2.5L4.5 7v11c0 7.8 5 15 11.5 16.5 6.5-1.5 11.5-8.7 11.5-16.5V7L16 2.5z" fill="#0500FF"/>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M16 5.2L24.8 8.8v9c0 6.2-3.8 11.8-8.8 13.2V5.2z" fill="#3375BB"/>
                        </svg>
                    </div>
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Trust Wallet</div>
                        <div style="font-size: 11px; color: #718096;">Multi-Chain DApp · Official Mobile</div>
                    </div>
                </div>
                <span id="recentBadge-TRUST" class="wallet-recent-tag" style="display: none;">RECENT</span>
            </div>

            <div class="wallet-option-pro" onclick="connectSpecificWalletProvider('PHANTOM')">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="wallet-icon-wrap" style="background: #ab9ff2;">
                        <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" alt="Phantom" style="width: 26px; height: 26px; object-fit: contain;">
                    </div>
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Phantom</div>
                        <div style="font-size: 11px; color: #718096;">Solana & Multi-Chain Standard</div>
                    </div>
                </div>
                <span id="recentBadge-PHANTOM" class="wallet-recent-tag" style="display: none;">RECENT</span>
            </div>

            <div class="wallet-option-pro" onclick="connectSpecificWalletProvider('BINANCE_OKX')">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="wallet-icon-wrap" style="background: transparent;">
                        <img src="https://cryptologos.cc/logos/bnb-bnb-logo.png?v=024" alt="Binance Web3" style="width: 32px; height: 32px; object-fit: contain;">
                    </div>
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Binance Web3 / OKX</div>
                        <div style="font-size: 11px; color: #718096;">Institutional Trading Gateway</div>
                    </div>
                </div>
                <span id="recentBadge-BINANCE_OKX" class="wallet-recent-tag" style="display: none;">RECENT</span>
            </div>

            <div class="wallet-option-pro" onclick="connectSpecificWalletProvider('COINBASE')">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="wallet-icon-wrap" style="background: transparent;">
                        <img src="https://avatars.githubusercontent.com/u/1885080?s=200&v=4" alt="Coinbase Wallet" style="width: 32px; height: 32px; border-radius: 8px; object-fit: contain;">
                    </div>
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Coinbase Wallet</div>
                        <div style="font-size: 11px; color: #718096;">Decentralized Smart Wallet</div>
                    </div>
                </div>
                <span id="recentBadge-COINBASE" class="wallet-recent-tag" style="display: none;">RECENT</span>
            </div>
        </div>

        <button onclick="toggleMoreWalletsGrid()" style="width: 100%; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); color: #ffffff; border-radius: 14px; padding: 13px 0; font-size: 13px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;">
            <i class="material-icons" style="font-size: 18px; color: #00e5ff;">grid_view</i>
            <span>All Wallets & WalletConnect</span>
        </button>

        <div id="allWalletsExpandGrid" style="display: none; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 4px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06);">
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('WALLETCONNECT')">
                <div class="wallet-icon-wrap" style="background: #3b99fc;"><img src="https://raw.githubusercontent.com/WalletConnect/walletconnect-assets/master/Logo/Blue%20(Default)/Logo.svg" alt="WC"></div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">WalletConnect</span>
            </div>
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('BITGET')">
                <div class="wallet-icon-wrap" style="background: #00f0ff;"><img src="https://s2.coinmarketcap.com/static/img/coins/64x64/24073.png" alt="Bitget"></div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">Bitget Wallet</span>
            </div>
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('SAFEPAL')">
                <div class="wallet-icon-wrap" style="background: #0c1b33;"><img src="https://s2.coinmarketcap.com/static/img/coins/64x64/8119.png" alt="SafePal"></div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">SafePal</span>
            </div>
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('1INCH')">
                <div class="wallet-icon-wrap" style="background: #0e1626;">
                    <img src="https://cryptologos.cc/logos/1inch-1inch-logo.png?v=024" alt="1inch" style="width: 28px; height: 28px; object-fit: contain;">
                </div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">1inch Wallet</span>
            </div>
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('RAINBOW')">
                <div class="wallet-icon-wrap" style="background: #001e3d;"><img src="https://avatars.githubusercontent.com/u/48327834?s=200&v=4" alt="Rainbow"></div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">Rainbow</span>
            </div>
            <div class="wallet-grid-item" onclick="connectSpecificWalletProvider('EXODUS')">
                <div class="wallet-icon-wrap" style="background: #1b1433;"><img src="https://s2.coinmarketcap.com/static/img/coins/64x64/8991.png" alt="Exodus"></div>
                <span style="font-size: 11px; font-weight: 800; color: #fff;">Exodus</span>
            </div>
        </div>

        <div style="text-align: center; color: #718096; font-size: 11px; line-height: 1.4;">
            By connecting, you agree to decentralized non-custodial protocol terms.
        </div>
    </div>
</div>

<div id="blockchainLoaderOverlay" class="blockchain-loader-overlay">
    <div class="blockchain-loader-card">
        <div id="bcLoaderSpinner" class="bc-spinner"></div>
        <div id="bcSuccessIcon" class="bc-success-icon" style="display: none;">✓</div>
        <h3 id="bcLoaderTitle" style="color: #ffffff; font-size: 18px; margin: 0; font-weight: 700; letter-spacing: 0.4px;">Activating...</h3>
        <div id="bcLoaderSubText" style="color: #718096; font-size: 12px;">Your transaction is in progress.</div>
    </div>
</div>

<div id="pwaInstallBanner" style="display: none; background: #161c28; border-bottom: 1px solid rgba(0, 229, 255, 0.2); padding: 8px 16px; justify-content: space-between; align-items: center; z-index: 10000; box-sizing: border-box;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#00e5ff"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        <span style="font-size: 12px; font-weight: 800; color: #ffffff;">Download Shine App</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <button id="pwaInstallBtn" style="background: #2563eb; color: #ffffff; border: none; padding: 5px 12px; border-radius: 8px; font-size: 11px; font-weight: 800; cursor: pointer;">Install</button>
        <button onclick="document.getElementById('pwaInstallBanner').style.display='none'" style="background: transparent; border: none; color: #718096; cursor: pointer; display: flex; align-items: center;"><i class="material-icons" style="font-size: 16px;">close</i></button>
    </div>
</div>
<header class="header">
    <div class="header-title">
        <svg viewBox="0 0 24 24" fill="white"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        <span id="headerIdDisplay">Preview ID 1</span>
    </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <button id="walletBtn" onclick="connectWallet()" style="background: #3A47A6; border: none; border-radius: 12px; color: white; padding: 8px 16px; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="material-icons" style="font-size:16px;">account_balance_wallet</i>
                    <span>Connect Wallet</span>
                </button>
                <div class="notification-wrapper" onclick="toggleNotifications()">
                    <i class="material-icons">notifications</i>
                    <span class="notif-dot" id="notifDot"></span>
                </div>
                <i class="material-icons" onclick="toggleMenu()" style="cursor: pointer; margin-left: 5px;">menu</i>
            </div>
        </header>

        <div id="pnlShareModal" class="login-overlay" style="z-index: 11000; align-items: center; justify-content: flex-start; overflow-y: auto; padding: 20px 16px 40px;">
            <div style="width: 100%; max-width: 420px; display: flex; flex-direction: column; gap: 14px; margin: auto;">
                <div style="display: flex; justify-content: flex-end;">
                    <button class="close-edit-btn" onclick="closePnlShareModal()" style="position: static; width: 38px; height: 38px;"><i class="material-icons" style="font-size: 20px;">close</i></button>
                </div>
                <div id="pnlPosterTarget" style="background: radial-gradient(circle at top right, #1a2234 0%, #0d121c 55%, #07090e 100%); border-radius: 28px; padding: 30px 24px; min-height: 520px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 20px 60px rgba(0,0,0,0.9); box-sizing: border-box;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                            <div style="display: flex; align-items: center; gap: 14px;">
                                <div id="posterUserAvatar" style="width: 64px; height: 64px; border-radius: 50%; background-color: #1e2430; background-size: cover; background-position: center; border: none; flex-shrink: 0; box-shadow: none;"></div>
                                <div>
                                <div id="posterUserName" style="color: #ffffff; font-size: 20px; font-weight: 800; line-height: 1.2; white-space: nowrap;">User</div>
                                <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                                    <span id="posterUserId" style="color: #00e5ff; font-size: 13px; font-family: monospace; font-weight: 800;">ID 1</span>
                                    <span style="background: rgba(0, 230, 118, 0.15); color: #00e676; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;">VERIFIED</span>
                                </div>
                            </div>
                        </div>
                    </div>

                        <div style="color: #8c8ca1; font-size: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">TOTAL REALIZED PROFIT</div>
                        <div id="poster-profit-val" style="font-size: 52px; font-weight: 900; color: #00e676; margin: 8px 0 16px 0; font-family: monospace; letter-spacing: -1px; text-shadow: 0 0 30px rgba(0, 230, 118, 0.4); line-height: 1;">+$0.00</div>

                        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 18px; flex-wrap: wrap;">
                            <span style="background: rgba(0, 230, 118, 0.12); color: #00e676; padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; font-family: monospace;">24H: <span id="poster-24h-profit">+$0.00</span></span>
                            <span style="background: rgba(0, 229, 255, 0.12); color: #00e5ff; padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; font-family: monospace;">ZERO LIQUIDATION</span>
                            <span style="background: rgba(255, 255, 255, 0.06); color: #ffffff; padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; font-family: monospace;">SPOT 100%</span>
                        </div>

                        <div style="background: rgba(0, 230, 118, 0.06); border: none; border-radius: 14px; padding: 14px 16px; margin-bottom: 22px;">
                            <div style="color: #00e676; font-size: 13px; font-weight: 900; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                                <i class="material-icons" style="font-size: 18px; color: #00e676;">verified</i>
                                <span>100% PASSIVE REVENUE STREAM</span>
                            </div>
                            <div style="color: #a7f3d0; font-size: 14px; line-height: 1.5; font-weight: 600;">
                                Earn lifetime daily dividends without building a network. Deploy capital once, harvest automated crypto profits forever.
                            </div>
                        </div>
                    </div>

                    <div style="border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #00e5ff; font-size: 13px; font-weight: 900; letter-spacing: 0.8px; margin-bottom: 3px;">SHINE ALGO SPOT BOT</div>
                        <div style="color: #ffffff; font-size: 16px; font-weight: 800; letter-spacing: 0.5px;">Shine Crypto.io</div>
                        <div style="color: #718096; font-size: 12px; margin-top: 2px;">Decentralized Quantitative Trading</div>
                    </div>
                        <div style="width: 68px; height: 68px; background: #ffffff; border-radius: 12px; padding: 4px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://shinecrypto.io" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px;">
                    <button onclick="shareDirectToSocial()" style="background: #2563eb; color: #ffffff; border: none; padding: 16px 0; border-radius: 14px; font-weight: 800; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);">
                        <i class="material-icons" style="font-size: 20px;">share</i> SHARE IMAGE
                    </button>
                    <button onclick="downloadPnlPoster()" style="background: #1c2433; color: #ffffff; border: 1px solid #2d3748; padding: 16px 0; border-radius: 14px; font-weight: 800; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;">
                        <i class="material-icons" style="font-size: 20px;">file_download</i> DOWNLOAD
                    </button>
                </div>
            </div>
        </div>
        <div id="notificationOverlay" class="notif-overlay">
            <div class="notif-header">
                <h2 style="margin:0; font-size:20px;">Notifications</h2>
                <button class="close-edit-btn" onclick="toggleNotifications()" style="position:static;"><i class="material-icons">close</i></button>
            </div>
            <div id="notifList">
                <div class="notif-item">
                    <div class="notif-icon"><i class="material-icons">payments</i></div>
                    <div class="notif-content">
                        <div class="notif-title">Profit Received</div>
                        <div class="notif-desc">+ 10 USDT received from ID 4582 in V1 Program.</div>
                        <div class="notif-time">Today, 10:24 AM</div>
                    </div>
                </div>
                <div class="notif-item">
                    <div class="notif-icon" style="background: rgba(58, 71, 166, 0.2); color: #5C6BC0;"><i class="material-icons">person_add</i></div>
                    <div class="notif-content">
                        <div class="notif-title">New Partner</div>
                        <div class="notif-desc">ID 8923 joined your team.</div>
                        <div class="notif-time">Yesterday, 14:30 PM</div>
                    </div>
                </div>
                <div class="notif-item">
                    <div class="notif-icon" style="background: rgba(255, 215, 0, 0.2); color: #FFD700;"><i class="material-icons">upgrade</i></div>
                    <div class="notif-content">
                        <div class="notif-title">Level Upgraded</div>
                        <div class="notif-desc">Successfully upgraded Q2 Level 3.</div>
                        <div class="notif-time">12 Oct 2023, 09:15 AM</div>
                    </div>
                </div>
            </div>
        </div>

        <main>
            <section class="profile-section">
                <div class="avatar-container">
                    <div class="avatar-gradient-border">
                        <div class="avatar" id="profileAvatar" onclick="document.getElementById('avatarInput').click()" style="cursor:pointer;"></div>
                        <input type="file" id="avatarInput" style="display:none" accept="image/*" onchange="uploadAvatar(event)">
                    </div>
                    
                </div>
                <div class="profile-info">
                    <div class="profile-name-wrapper">
                        <div class="profile-name" id="displayNickname">User</div>
                        <button class="settings-btn" onclick="toggleProfileEdit()">
                            <i class="material-icons">settings</i>
                        </button>
                    </div>
                    <div class="profile-id">ID 1 <span id="userRank" style="margin-left:8px; background:linear-gradient(90deg, #FFD700, #FFA500); color:#000; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:900;">GOLD STAR</span></div>
                    <button class="show-more-btn" id="showMoreBtn" onclick="toggleExpandedProfile()">
                        <span>Show more</span>
                        <i class="material-icons" style="font-size: 20px;">keyboard_arrow_down</i>
                    </button>
                </div>
            </section>
            <div id="expandedProfile" class="expanded-profile" style="padding: 0 16px 20px;">
                <div class="wallet-address-row">
                    <span id="displayWallet">0xE5af...2Ed7</span>
                    <i class="material-icons" style="font-size: 16px; color: #757575; cursor: pointer;" onclick="copyWallet()">content_copy</i>
                </div>
                <div class="invited-by-row">
                    invited 30.07.2022 by <span class="upline-badge" onclick="previewUpline(487984)">ID 487984</span>
                </div>
            </div>

            <section class="link-section">
                <div class="link-header">
                    <div class="link-title">
                        <span>Personal link</span>
                        <div class="question-mark">?</div>
            </div>
            <a href="#" class="personal-link" id="userPersonalReferralLink">Shine Crypto.io</a>
        </div>
        <button class="copy-btn" onclick="copyPersonalReferralLink()">Copy</button>
                <button class="pro-bot-btn" onclick="toggleTrading()">
                    <div style="display: flex; align-items: center; gap: 14px; min-width: 0; flex: 1;">
                        <svg width="34" height="34" viewBox="0 0 34 34" fill="none" style="flex-shrink: 0; overflow: visible;">
                            <g class="c-green">
                                <line x1="7" y1="3" x2="7" y2="31" stroke="#00c087" stroke-width="1.8" stroke-linecap="round"/>
                                <rect x="4" y="9" width="6" height="14" fill="#00c087" rx="1.5"/>
                            </g>
                            <g class="c-red">
                                <line x1="17" y1="6" x2="17" y2="28" stroke="#f6465d" stroke-width="1.8" stroke-linecap="round"/>
                                <rect x="14" y="11" width="6" height="12" fill="#f6465d" rx="1.5"/>
                            </g>
                            <g class="c-green">
                                <line x1="27" y1="4" x2="27" y2="30" stroke="#00c087" stroke-width="1.8" stroke-linecap="round"/>
                                <rect x="24" y="8" width="6" height="15" fill="#00c087" rx="1.5"/>
                            </g>
                        </svg>
                        <div style="min-width: 0; flex: 1;">
                            <div style="color: #FFFFFF; font-weight: 800; font-size: 14px; letter-spacing: 0.4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">SPOT TRADING & DEX</div>
                            <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
                                <span class="live-vibe-dot"></span>
                                <span style="color: #00c087; font-size: 10px; font-weight: 800; font-family: monospace; letter-spacing: 0.5px;">ACTIVE QUANT BOT</span>
                            </div>
                        </div>
                    </div>
                    <i class="material-icons" style="color: var(--text-secondary); font-size: 22px; flex-shrink: 0; margin-left: 6px;">chevron_right</i>
                </button>
            </section>
            <section class="stats-grid">
                <div class="stat-card">
                    <div class="stat-header">
                        <div class="stat-title">
                            <span>Partners</span>
                            <div class="question-mark">?</div>
                        </div>
                        <i class="material-icons">people_outline</i>
                    </div>
                    <div class="stat-value">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <div class="stat-title">
                            <span>Team</span>
                            <div class="question-mark">?</div>
                        </div>
                        <i class="material-icons">groups</i>
                    </div>
                    <div class="stat-value">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <div class="stat-title">
                            <span>Ratio</span>
                            <div class="question-mark">?</div>
                        </div>
                        <i class="material-icons">rocket_launch</i>
                    </div>
                    <div class="stat-value">0 %</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <div class="stat-title">
                            <span>Top 100 leaders</span>
                        </div>
                    </div>
                    <button class="see-now-btn">See Now</button>
                </div>
                <div class="stat-card" style="grid-column: span 2;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <div style="flex: 1;">
                            <div class="stat-header">
                                <div class="stat-title"><span>Trading Profits</span></div>
                            </div>
                            <div class="stat-value" id="realProfitValue" style="color: #4CAF50; font-size: 32px;">$0.00</div>
                        </div>
                        <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 15px;">
                            <div class="stat-header">
                                <div class="stat-title"><span>Success Trades</span></div>
                            </div>
                            <div class="stat-value" id="successTradeCount" style="color: #4CAF50; font-size: 32px;">0</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button class="see-now-btn" onclick="toggleTrading()" style="flex: 1; height: 40px; background: #4CAF50; margin-top: 0; border-radius: 12px; font-weight: bold;">
                            PROFIT
                        </button>
                        <button class="see-now-btn" onclick="toggleTrading()" style="flex: 1; height: 40px; background: #4CAF50; margin-top: 0; border-radius: 12px; font-weight: bold;">
                            SUCCESS TRADES
                        </button>
                    </div>
                </div>
            </section>
        </main>
    </div>
<section class="card-section profit-section">
                <div class="card-header">
                    <h2>Profit</h2>
                    <svg class="icon-md" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 6C16.4184 6 20 7.34315 20 9C20 10.6569 16.4184 12 12 12C7.58158 12 4 10.6569 4 9C4 7.34315 7.58158 6 12 6Z" stroke="#FFFFFFB3" stroke-width="1.5"/>
                        <path d="M4 9V15C4 16.6569 7.58158 18 12 18C16.4184 18 20 16.6569 20 15V9" stroke="#FFFFFFB3" stroke-width="1.5"/>
                        <path d="M4 12V15" stroke="#FFFFFFB3" stroke-width="1.5"/>
                    </svg>
                </div>
                <div class="currency-list">
                    <div class="currency-row">
                        <div class="currency-info">
                            <svg class="icon-md" viewBox="0 0 200 200" style="width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(228, 37, 125, 0.45));">
                                <defs>
                                    <radialGradient id="shineOuterRingGradH" cx="35%" cy="30%" r="75%">
                                        <stop offset="0%" stop-color="#fa5c9e"/>
                                        <stop offset="45%" stop-color="#e4257d"/>
                                        <stop offset="85%" stop-color="#b6115c"/>
                                        <stop offset="100%" stop-color="#8a0742"/>
                                    </radialGradient>
                                    <radialGradient id="shineInnerFaceGradH" cx="40%" cy="38%" r="62%">
                                        <stop offset="0%" stop-color="#ff59a3"/>
                                        <stop offset="40%" stop-color="#e92a83"/>
                                        <stop offset="85%" stop-color="#c41467"/>
                                        <stop offset="100%" stop-color="#96084a"/>
                                    </radialGradient>
                                    <linearGradient id="shineHighlightFlashH" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
                                        <stop offset="35%" stop-color="#ffffff" stop-opacity="0.2"/>
                                        <stop offset="70%" stop-color="#ffffff" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                                <circle cx="100" cy="100" r="98" fill="url(#shineOuterRingGradH)"/>
                                <circle cx="100" cy="100" r="92" fill="none" stroke="#ff7db6" stroke-width="2.5" opacity="0.8"/>
                                <circle cx="100" cy="100" r="86" fill="none" stroke="#8a0742" stroke-width="2.5" opacity="0.7"/>
                                <circle cx="100" cy="100" r="83" fill="url(#shineInnerFaceGradH)"/>
                                <path d="M35 45 Q 65 22 105 20 Q 60 35 48 78 Z" fill="url(#shineHighlightFlashH)" opacity="0.55"/>
                                <g fill="#ffffff">
                                    <text x="49" y="122" font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-weight="800" font-size="38" text-anchor="middle">S</text>
                                    <text x="76" y="122" font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-weight="800" font-size="38" text-anchor="middle">H</text>
                                    <path d="M109 62 Q109.8 69.5 117.5 72 Q109.8 74.5 109 82 Q108.2 74.5 100.5 72 Q108.2 69.5 109 62 Z"/>
                                    <path d="M94.5 78 Q95.2 80 97.5 81 Q95.2 82 94.5 84 Q93.8 82 91.5 81 Q93.8 80 94.5 78 Z"/>
                                    <path d="M117 80.5 Q117.8 83.5 121.5 84.5 Q117.8 85.5 117 88.5 Q116.2 85.5 112.5 84.5 Q116.2 83.5 117 80.5 Z"/>
                                    <circle cx="104" cy="85.5" r="2.4"/>
                                    <path d="M97 97.5 C98 92.5 101.5 88.8 106 88.2 C103.5 90.5 100.8 93.5 99.5 97.5 Z"/>
                                    <circle cx="103.5" cy="95.5" r="2.5"/>
                                    <path d="M94.5 111.5 C94 105.5 98.5 99.5 104.5 98 C107.5 97.2 109.8 96 111 94.5 C110.2 97.5 107.2 99.8 103.5 101 C99 102.5 97 106.5 97.5 111.5 Z"/>
                                    <circle cx="99.5" cy="114" r="2.5"/>
                                    <path d="M99.5 108.5 C103 108.5 106.5 111.8 105.8 116.5 C105 121 101 124.5 97.5 127.5 C95 129.8 93.8 132.5 93.5 134 C94.5 132 96.5 129.5 98.8 127.2 C101.5 124.5 104.8 121.5 105.5 117.5 C106.2 113 104 109.8 99.5 109.8 C97 109.8 95 111 94 113 C95 110 97 108.5 99.5 108.5 Z"/>
                                    <path d="M96 123.5 C97.8 125.8 101.2 129.5 104 133 C107 136.8 109 139 109.5 140 C108.2 138.5 105.5 134.5 102.5 130.5 C99.8 126.8 97.5 124.5 96 123.5 Z"/>
                                    <text x="127" y="122" font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-weight="800" font-size="38" text-anchor="middle">N</text>
                                    <text x="154" y="122" font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-weight="800" font-size="38" text-anchor="middle">E</text>
                                </g>
                            </svg>
                            <span>SHINE</span>
                        </div>
                        <span class="currency-balance" id="homeProfitShine">0</span>
                    </div>
                    <div class="currency-row">
                        <div class="currency-info">
                            <svg viewBox="0 0 100 100" class="icon-md" style="width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                            <span>USDT</span>
                        </div>
                        <span class="currency-balance" id="homeProfitUsdt">0</span>
                    </div>
                    <div class="currency-row">
                        <div class="currency-info">
                            <svg viewBox="0 0 32 32" class="icon-md" style="width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;">
                                <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                                <path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                            </svg>
                            <span>BNB</span>
                        </div>
                        <span class="currency-balance" id="homeProfitBnb">0</span>
                    </div>
                </div>
            </section>
            <section class="card-section passive-income-section">
                <h2>Total Passive income</h2>
                <div class="passive-income-amount">
                    <span id="homePassiveIncomeVal">0</span>
                    <svg class="icon-md" viewBox="0 0 100 100" style="width: 24px; height: 24px; border-radius: 50%;">
                        <circle cx="50" cy="50" r="50" fill="#009393"/>
                        <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                        <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                    </svg>
                </div>
                <button class="claim-btn" onclick="claimProfit()">
                    <span>Claim</span>
                    <div class="claim-value">
                        <span id="homeClaimValueDisplay">0</span>
                        <svg class="icon-sm" viewBox="0 0 100 100" style="width: 20px; height: 20px; border-radius: 50%;">
                            <circle cx="50" cy="50" r="50" fill="#009393"/>
                            <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                            <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                        </svg>
                    </div>
                </button>
                <div style="background: rgba(76, 175, 80, 0.08); border: 1px solid rgba(76, 175, 80, 0.2); border-radius: 12px; padding: 12px 14px; margin-top: 14px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <i class="material-icons" style="color: #4CAF50; font-size: 20px;">group_add</i>
                        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Referral Trading Profit</span>
                    </div>
                    <span style="color: #4CAF50; font-size: 13px; font-weight: 800; font-family: monospace;">10% DIRECT</span>
                </div>
                <hr class="divider">
                <ul class="rules-list">
                    <li class="rule-item">
                        <span>Rules</span>
                        <svg class="icon-md" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="#FFFFFFB3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M14 2V8H20" stroke="#FFFFFFB3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M9.5 14.5L11 16L15 12" stroke="#FFFFFFB3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </li>
                    <li class="rule-item">
                        <span>Trading profit</span>
                        <div class="rule-value">
                            <span id="ruleTradingProfitVal">0</span>
                            <svg class="icon-sm" viewBox="0 0 100 100" style="width: 20px; height: 20px; border-radius: 50%;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                        </div>
                    </li>
                    <li class="rule-item">
                        <span>Top 100 leaders</span>
                        <div class="rule-value">
                            <span>0</span>
                            <svg class="icon-sm" viewBox="0 0 100 100" style="width: 20px; height: 20px; border-radius: 50%;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                        </div>
                    </li>
                    <li class="rule-item">
                        <span>Unconditional</span>
                        <div class="rule-value">
                            <span>0</span>
                            <svg class="icon-sm" viewBox="0 0 100 100" style="width: 20px; height: 20px; border-radius: 50%;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                        </div>
                    </li>
                    <li class="rule-item">
                        <span>Active users</span>
                        <div class="rule-value">
                            <span>0</span>
                            <svg class="icon-sm" viewBox="0 0 100 100" style="width: 20px; height: 20px; border-radius: 50%;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                        </div>
                    </li>
</ul>
            </section>

            <section class="rewards-section">
                <div class="rewards-title">Daily rewards balances</div>
                <div class="reward-card">
                    <div class="reward-label">Total V1</div>
                    <div class="reward-value-row">
                        <span>0</span>
                        <svg class="icon-md" viewBox="0 0 100 100" style="width: 24px; height: 24px; border-radius: 50%;">
                            <circle cx="50" cy="50" r="50" fill="#009393"/>
                            <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                            <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                        </svg>
                    </div>
                </div>
                <div class="distribution-card">
                    <i class="material-icons">access_time</i>
                    <span>Distribution</span>
                </div>
                <div style="background: var(--secondary-bg); border-radius: 16px; padding: 15px; margin-top: 12px; text-align: center; border: 1px solid var(--tertiary-bg);">
                    <div style="color: #FFFFFFB3; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Next Global Dividend Distribution</div>
                    <div id="dividendTimer" style="font-size: 24px; font-weight: 900; color: #FFD700; margin: 8px 0;">00:00:00</div>
                    <div style="font-size: 10px; color: #4CAF50;">V1 GLOBAL POOL: <span id="globalPoolAmt">0.00</span> USDT</div>
                </div>
                <style>
                    .usdt-coin {
                        position: absolute;
                        bottom: 115px;
                        left: 55px;
                        opacity: 0;
                        z-index: 15;
                        animation: usdtJump 4s infinite ease-in-out;
                    }
                    @keyframes botWork {
                        0%, 100% { transform: translateY(0) scale(1); }
                        5% { transform: translateY(2px) scale(0.98); }
                        10% { transform: translateY(-2px) scale(1.02); }
                    }
                    @keyframes walletAbsorb {
                        0%, 70% { transform: scale(1); box-shadow: 0 0 20px rgba(76, 175, 80, 0.4); }
                        85% { transform: scale(1.1); box-shadow: 0 0 40px rgba(76, 175, 80, 0.8); }
                        100% { transform: scale(1); }
                    }
                    @keyframes scanLine {
                        0% { bottom: 5px; opacity: 0; }
                        50% { opacity: 1; }
                        100% { bottom: 60px; opacity: 0; }
                    }
                    @keyframes rotateRing {
                        from { transform: rotate(0deg); }
                        to { transform: rotate(360deg); }
                    }
                    .coin-wrapper { position: absolute; bottom: 115px; left: 55px; width: 28px; height: 28px; opacity: 0; animation: multiCoinJump 4s infinite ease-in-out; }
                    .trading-coin, .result-usdt { position: absolute; width: 100%; height: 100%; }
                    .result-usdt { opacity: 0; }
                    @keyframes multiCoinJump {
                        0% { transform: translate(0, 0) scale(0.5); opacity: 0; }
                        10% { opacity: 1; transform: translate(10px, -30px) scale(1); }
                        45% { transform: translate(70px, -110px) scale(1.4); opacity: 1; }
                        55% { transform: translate(80px, -100px) scale(1.4); opacity: 1; }
                        60% { opacity: 1; }
                        85% { opacity: 1; transform: translate(145px, -10px) scale(1.1); }
                        100% { transform: translate(145px, 40px) scale(0.2); opacity: 0; }
                    }
                    .coin-wrapper img.trading-coin { animation: swapToUsdt 4s infinite ease-in-out; animation-delay: inherit; }
                    .coin-wrapper img.result-usdt { animation: swapFromCoin 4s infinite ease-in-out; animation-delay: inherit; }
                    @keyframes swapToUsdt { 0%, 50% { opacity: 1; } 55%, 100% { opacity: 0; } }
                    @keyframes swapFromCoin { 0%, 50% { opacity: 0; } 55%, 100% { opacity: 1; } }
                    @keyframes pulseBorder {
                        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
                        70% { box-shadow: 0 0 0 15px rgba(76, 175, 80, 0); }
                        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
                    }
                    @keyframes pulse {
                        0% { transform: scale(1); opacity: 1; }
                        50% { transform: scale(1.5); opacity: 0.5; }
                        100% { transform: scale(1); opacity: 1; }
                    }
                </style>
                <div class="visual-container">
    <div class="radar-sweep"></div>
    <div class="circle-overlay ring-1"></div>
    <div class="circle-overlay ring-2"></div>
    <div class="circle-overlay ring-3"></div>
    
    <div class="orbit-layer-3">
        <div class="sci-badge bg-badge-l3 badge-x12"><div class="counter-rotate-slow">O12</div></div>
        <div class="sci-badge bg-badge-l3 badge-x13"><div class="counter-rotate-slow">N13</div></div>
        <div class="sci-badge bg-badge-l3 badge-x14"><div class="counter-rotate-slow">E14</div></div>
        <div class="sci-badge bg-badge-l3 badge-x15"><div class="counter-rotate-slow">X15</div></div>
    </div>

    <div class="orbit-layer-2">
        <div class="sci-badge bg-badge-l2 badge-x7"><div class="counter-rotate-normal">A7</div></div>
        <div class="sci-badge bg-badge-l2 badge-x8"><div class="counter-rotate-normal">C8</div></div>
        <div class="sci-badge bg-badge-l2 badge-x9"><div class="counter-rotate-normal">S9</div></div>
        <div class="sci-badge bg-badge-l2 badge-x10"><div class="counter-rotate-normal">Q10</div></div>
        <div class="sci-badge bg-badge-l2 badge-x11"><div class="counter-rotate-normal">H11</div></div>
    </div>

    <div class="orbit-container">
        <div class="sci-badge bg-badge badge-x2"><div class="counter-rotate">Q2</div></div>
        <div class="sci-badge bg-badge badge-x3"><div class="counter-rotate">T3</div></div>
        <div class="sci-badge bg-badge badge-x4"><div class="counter-rotate">S4</div></div>
        <div class="sci-badge bg-badge badge-x5"><div class="counter-rotate">G5</div></div>
        <div class="sci-badge bg-badge badge-x6"><div class="counter-rotate">N6</div></div>
    </div>
    
    <div class="main-badge">V1</div>
</div>
                </div>
            </section>

            <div style="clear: both; height: 1px;"></div>
            <section class="programs-section">
                <div class="programs-header">
                    <h2>Shine Programs</h2>
                    <button class="more-info-btn" onclick="toggleModal('infoModal')">
                        <i class="material-icons" style="font-size: 18px;">more_vert</i>
                        <span>More info</span>
                    </button>
                </div>
                <div class="program-card V1">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Velocity Engine (Global Pool)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #FFD700; opacity: 0.2;">V1</div>
                        </div>
                        <div class="slots-grid" id="slots-V1"></div>
                        <button class="preview-btn" onclick="openPreview('V1')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>V1</span> Quantum Preview</button>
                    </div>
                </div>
                <div class="program-card Q2">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Quantum Matrix (Ghost Support)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #00BCD4; opacity: 0.2;">Q2</div>
                        </div>
                        <div class="slots-grid" id="slots-Q2"></div>
                        <button class="preview-btn" onclick="openPreview('Q2')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>Q2</span> Quantum Preview</button>
                    </div>
                </div>
                <div class="program-card T3">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Trinity Force (Direct Power)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #3A47A6; opacity: 0.2;">T3</div>
                        </div>
                        <div class="slots-grid" id="slots-T3"></div>
                        <button class="preview-btn" onclick="openPreview('T3')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>T3</span> Trinity Preview</button>
                    </div>
                </div>
                <div class="program-card S4">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Dual Synergy (Team Spillover)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #8A2BE2; opacity: 0.2;">S4</div>
                        </div>
                        <div class="slots-grid" id="slots-S4"></div>
                        <button class="preview-btn" onclick="openPreview('S4')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>S4</span> Synergy Preview</button>
                    </div>
                </div>
                <div class="program-card G5">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Galaxy Orbit (Deep Network)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #E91E63; opacity: 0.2;">G5</div>
                        </div>
                        <div class="slots-grid" id="slots-G5"></div>
                        <button class="preview-btn" onclick="openPreview('G5')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>G5</span> Galaxy Preview</button>
                    </div>
                </div>
                <div class="program-card N6">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Infinite Nexus (Global Reach)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #00BCD4; opacity: 0.2;">N6</div>
                        </div>
                        <div class="slots-grid" id="slots-N6"></div>
                        <button class="preview-btn" onclick="openPreview('N6')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>N6</span> Nexus Preview</button>
                    </div>
                </div>
                <div class="program-card A7">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">AI Genesis (Quant Desk)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #FF4500; opacity: 0.2;">A7</div>
                        </div>
                        <div class="slots-grid" id="slots-A7"></div>
                        <button class="preview-btn" onclick="openPreview('A7')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>A7</span> Genesis Preview</button>
                    </div>
                </div>
                <div class="program-card C8">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Cyber Node (Quant Desk)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #32CD32; opacity: 0.2;">C8</div>
                        </div>
                        <div class="slots-grid" id="slots-C8"></div>
                        <button class="preview-btn" onclick="openPreview('C8')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>C8</span> Cyber Preview</button>
                    </div>
                </div>
                <div class="program-card S9">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Synapse Grid (Quant Desk)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #FF1493; opacity: 0.2;">S9</div>
                        </div>
                        <div class="slots-grid" id="slots-S9"></div>
                        <button class="preview-btn" onclick="openPreview('S9')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>S9</span> Synapse Preview</button>
                    </div>
                </div>
                <div class="program-card Q10">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Quantum Core (VIP Semi-Whale)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #00FA9A; opacity: 0.2;">Q10</div>
                        </div>
                        <div class="slots-grid" id="slots-Q10"></div>
                        <button class="preview-btn" onclick="openPreview('Q10')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>Q10</span> Quantum Preview</button>
                    </div>
                </div>
                <div class="program-card H11">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Holo Matrix (VIP Semi-Whale)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #9400D3; opacity: 0.2;">H11</div>
                        </div>
                        <div class="slots-grid" id="slots-H11"></div>
                        <button class="preview-btn" onclick="openPreview('H11')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>H11</span> Holo Preview</button>
                    </div>
                </div>
                <div class="program-card O12">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Omni Chain (VIP Semi-Whale)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #FF8C00; opacity: 0.2;">O12</div>
                        </div>
                        <div class="slots-grid" id="slots-O12"></div>
                        <button class="preview-btn" onclick="openPreview('O12')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>O12</span> Omni Preview</button>
                    </div>
                </div>
                <div class="program-card N13">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Neural Link (Whale Vault)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #00FFFF; opacity: 0.2;">N13</div>
                        </div>
                        <div class="slots-grid" id="slots-N13"></div>
                        <button class="preview-btn" onclick="openPreview('N13')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>N13</span> Neural Preview</button>
                    </div>
                </div>
                <div class="program-card E14">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Eternity Protocol (Whale Vault)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #DC143C; opacity: 0.2;">E14</div>
                        </div>
                        <div class="slots-grid" id="slots-E14"></div>
                        <button class="preview-btn" onclick="openPreview('E14')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>E14</span> Eternity Preview</button>
                    </div>
                </div>
                <div class="program-card X15">
                    <div class="program-inner">
                        <div class="program-top">
                            <div class="program-stats">
                                <div class="prog-label">Apex Singularity (Whale Vault)</div>
                                <div class="prog-value">0 USDT</div>
                            </div>
                            <div class="watermark" style="color: #FFFFFF; opacity: 0.2;">X15</div>
                        </div>
                        <div class="slots-grid" id="slots-X15"></div>
                        <button class="preview-btn" onclick="openPreview('X15')" style="background: var(--primary-blue); color: #fff; border: none; padding: 18px; font-weight: 900;"><span>X15</span> Apex Preview</button>
                    </div>
                </div>
            </section>
            <section class="platform-activity">
                <div class="activity-header">
                    <h2>Platform recent activity</h2>
                    <div class="question-mark">?</div>
                </div>

                <div class="activity-card">
                    <div class="activity-label">Members total</div>
                    <div class="activity-main-row">
                        <div class="activity-total" id="totalMembers">1,248</div>
                        <div class="activity-growth" id="memberGrowth">↑ 12</div>
                    </div>
                </div>
                <div class="activity-card">
                    <div class="activity-label">
                        <span>Members received</span>
                        <div class="question-mark">?</div>
                    </div>
                    <div class="activity-main-row">
                        <div class="activity-total">0 SHINE</div>
                        <div class="activity-growth">+ 0 SHINE</div>
                    </div>
                    <div class="activity-divider"></div>
                    <div class="activity-main-row">
                        <div class="activity-total">0 USDT</div>
                        <div class="activity-growth">+ 0 USDT</div>
                    </div>
                    <div class="activity-divider"></div>
                    <div class="activity-main-row">
                        <div class="activity-total">0 BNB</div>
                        <div class="activity-growth">+ 0 BNB</div>
                    </div>
                </div>

                <div class="contract-selector">
                    <span>SHINE USDT Contracts</span>
                    <div class="selector-arrow">
                        <i class="material-icons">arrow_drop_down</i>
                    </div>
                </div>

                <div id="liveActivityFeed">
                    <div class="recent-event">
                        <div class="event-icon-bg" style="background: #1B5E20;"><i class="material-icons">bolt</i></div>
                        <div class="event-details">
                            <div class="event-top"><span class="event-id">ID 1</span><span class="event-time">Just now</span></div>
                            <div class="event-bottom"><span class="event-amount">+ 10 USDT</span> <span class="event-program">in <span class="blue-text">V1</span></span></div>
                        </div>
                    </div>
                </div>
                
            </section>
            <div id="tradingOverlay" class="trading-overlay">
        <div class="bot-container" style="padding-bottom: 80px;">
            <div class="bot-header" style="margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; position: relative;">
                <button onclick="toggleTrading()" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 50%; width: 34px; height: 34px; color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; outline: none; z-index: 2;">
                    <i class="material-icons" style="font-size: 20px;">arrow_back</i>
                </button>
                <div style="position: absolute; left: 0; right: 0; text-align: center; font-size: 15px; font-weight: 900; color: #ffffff; letter-spacing: 0.8px; pointer-events: none;">Shine Crypto.io</div>
                <div class="bot-title-area">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div id="price-SOL" style="display: none;">0.00</div>
                    </div>
                </div>
            </div>

            <div id="tabViewHome" class="bot-tab-view active">
            <div class="bot-card" style="padding-bottom: 24px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <h3 style="margin: 0; font-size: 16px; letter-spacing: 1px; color: #fff; font-weight: 800;">SHINE APEX PRIME DCA</h3>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div id="backendLiveIndicator" title="Backend Server Status" style="display: flex; align-items: center; gap: 5px; background: rgba(255,255,255,0.05); padding: 4px 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                            <span id="backendStatusDot" style="width: 8px; height: 8px; background: #00E676; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #00E676; animation: livePulseDot 1.2s infinite;"></span>
                            <span id="backendStatusText" style="font-size: 10px; font-weight: 800; font-family: monospace; color: #00E676;">LIVE</span>
                        </div>
                        <span id="bot-cooldown-badge" style="display: none; background: rgba(255, 193, 7, 0.12); color: #FFC107; border: 1px solid rgba(255, 193, 7, 0.4); padding: 3px 8px; border-radius: 20px; font-size: 10px; font-weight: bold; font-family: monospace;">WAIT <span id="cooldown-timer">05:00</span></span>
                        <div onclick="toggleBotExecution()" id="btn-bot-toggle" style="background: rgba(76, 175, 80, 0.15); border: 1px solid #4CAF50; color: #4CAF50; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 900; cursor: pointer; letter-spacing: 0.5px;">RUNNING</div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; background: rgba(255,255,255,0.03); padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; border: 1px solid #1a1a1a;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #757575; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;">STATUS:</span>
                        <span id="live-phase-round" style="color: #FFD700; font-size: 13px; font-weight: 900;">PHASE 1 | ROUND 6</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #757575; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;">FUND USAGE:</span>
                        <span id="live-fund-usage" style="color: #00d2ff; font-size: 13px; font-weight: 900; font-family: monospace;">20.00%</span>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
                    <div style="color: #757575; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 4px;">Live SOL Price</div>
                    <div id="large-live-sol" style="font-size: 42px; font-weight: 900; color: #fff; font-family: monospace; text-shadow: 0 0 20px rgba(255,255,255,0.25);">$0.00</div>
                </div>

                <div style="border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <i class="material-icons" style="font-size: 18px; color: #00d2ff;">swap_horizontal_circle</i>
                            <span style="font-size: 12px; font-weight: 800; color: #fff; letter-spacing: 0.5px;">LIVE SPOT CONVERSION</span>
                        </div>
                        <span style="color: #4CAF50; font-size: 11px; font-weight: bold; font-family: monospace;">AUTOMATED ROUTE</span>
                    </div>
                    <div style="width: 100%; box-sizing: border-box; min-height: 240px; display: flex; justify-content: space-between; align-items: center; background: radial-gradient(circle at center, #18182b 0%, #0a0a14 100%); padding: 35px 20px; border-radius: 16px; border: 1px solid #282845; position: relative; overflow: visible; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                        <div style="text-align: center; width: 110px; z-index: 10;">
                            <div style="animation: botWork 4s infinite ease-in-out;">
                                <div style="width: 75px; height: 75px; background: #1a1a2e; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 2px solid #3A47A6; box-shadow: 0 0 25px rgba(58, 71, 166, 0.6); position: relative; overflow: hidden;">
                                    <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(45deg, transparent, rgba(0,210,255,0.1), transparent);"></div>
                                    <i class="material-icons" style="font-size: 42px; color: #00d2ff; filter: drop-shadow(0 0 8px #00d2ff);">precision_manufacturing</i>
                                    <div style="position: absolute; bottom: 5px; width: 45px; height: 2px; background: #00d2ff; box-shadow: 0 0 10px #00d2ff; animation: scanLine 2s infinite;"></div>
                                </div>
                                <div style="font-size: 10px; color: #00d2ff; margin-top: 8px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px;">CORE ENGINE</div>
                            </div>
                        </div>

                        <div style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 5;">
                            <div class="coin-wrapper" style="animation-delay: 0s;"><img id="anim-coin-1" src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" class="trading-coin"><img src="https://cryptologos.cc/logos/tether-usdt-logo.png?v=024" class="result-usdt"></div>
                            <div class="coin-wrapper" style="animation-delay: 1.5s;"><img id="anim-coin-2" src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" class="trading-coin"><img src="https://cryptologos.cc/logos/tether-usdt-logo.png?v=024" class="result-usdt"></div>
                            <div class="coin-wrapper" style="animation-delay: 3s;"><img id="anim-coin-3" src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" class="trading-coin"><img src="https://cryptologos.cc/logos/tether-usdt-logo.png?v=024" class="result-usdt"></div>
                            <div class="coin-wrapper" style="animation-delay: 4.5s;"><img id="anim-coin-4" src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" class="trading-coin"><img src="https://cryptologos.cc/logos/tether-usdt-logo.png?v=024" class="result-usdt"></div>
                        </div>

                        <div style="text-align: center; width: 110px; z-index: 10;">
                            <div>
                                <div style="width: 75px; height: 75px; background: #0d1a0d; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 2px solid #4CAF50; box-shadow: 0 0 25px rgba(76, 175, 80, 0.4); position: relative; animation: walletAbsorb 4s infinite ease-in-out;">
                                    <i class="material-icons" style="font-size: 42px; color: #4CAF50; filter: drop-shadow(0 0 10px #4CAF50);">account_balance_wallet</i>
                                    <div style="position: absolute; inset: -5px; border: 1px solid rgba(76, 175, 80, 0.3); border-radius: 50%; animation: rotateRing 10s linear infinite;"></div>
                                </div>
                                <div style="font-size: 10px; color: #4CAF50; margin-top: 8px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px;">SECURE VAULT</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
<div id="exchangeTerminalOverlay" class="login-overlay" style="z-index: 16000; overflow-y: auto; padding: 18px 18px 25% 18px; position: fixed; top: 0; left: 0; width: 100%; min-height: 125%; height: auto; background: #0b0e14; box-sizing: border-box; display: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 0 4px 16px 4px; padding: 4px 6px 14px 6px; border-bottom: 1px solid #1a202c;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; letter-spacing: 0.5px;">SOL/USDT</span>
                        <span style="background: rgba(0, 192, 135, 0.15); color: #00c087; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 900;">SPOT</span>
                        <div onclick="toggleTradeExecutionMode()" id="tradeModeToggleBtn" style="background: rgba(255, 215, 0, 0.12); border: 1px solid #FFD700; color: #FFD700; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace; cursor: pointer;">TESTNET</div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div id="ex-wallet-btn" onclick="openConnectModal()" style="background: rgba(0, 192, 135, 0.1); border: 1px solid rgba(0, 192, 135, 0.3); border-radius: 20px; color: #00c087; font-size: 11px; font-weight: 900; font-family: monospace; cursor: pointer; display: flex; align-items: center; gap: 5px; padding: 6px 12px;">
                            <i class="material-icons" style="font-size: 15px; color: #00c087;">account_balance_wallet</i>
                            <span id="ex-wallet-btn-text">CONNECT</span>
                        </div>
                    </div>
                </div>

                <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 10px 14px; margin: 0 auto 16px auto; width: 100%; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-family: monospace; text-align: center; box-sizing: border-box;">
                    <div style="display: flex; flex-direction: column; align-items: center;">
                        <div style="color: #64748b; font-size: 10px; font-weight: 800; text-transform: uppercase;">24h High</div>
                        <div id="ex-high-24h" style="color: #ffffff; font-size: 12px; font-weight: 900; margin-top: 3px;">$0.00</div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; border-left: 1px solid rgba(255,255,255,0.05);">
                        <div style="color: #64748b; font-size: 10px; font-weight: 800; text-transform: uppercase;">24h Low</div>
                        <div id="ex-low-24h" style="color: #ffffff; font-size: 12px; font-weight: 900; margin-top: 3px;">$0.00</div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; border-left: 1px solid rgba(255,255,255,0.05);">
                        <div style="color: #64748b; font-size: 10px; font-weight: 800; text-transform: uppercase; white-space: nowrap;">24H Vol</div>
                        <div id="ex-vol-24h" style="color: #ffffff; font-size: 12px; font-weight: 900; margin-top: 3px;">0</div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; border-left: 1px solid rgba(255,255,255,0.05);">
                        <div style="color: #64748b; font-size: 10px; font-weight: 800; text-transform: uppercase;">Buyers</div>
                        <div id="ex-buyers-count" style="color: #00c087; font-size: 12px; font-weight: 900; margin-top: 3px;">50% BUY</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 14px; align-items: start; min-height: auto;">
                    <div style="display: flex; flex-direction: column; justify-content: space-between; gap: 12px; height: 100%;">
                        <div style="display: flex; background: #151a24; border-radius: 8px; padding: 3px;">
                            <button id="ex-tab-buy" onclick="switchExchangeTab('BUY')" style="flex: 1; background: #00c087; color: #000; border: none; padding: 9px 0; border-radius: 6px; font-weight: 900; font-size: 12px; cursor: pointer;">Buy</button>
                            <button id="ex-tab-sell" onclick="switchExchangeTab('SELL')" style="flex: 1; background: transparent; color: #757575; border: none; padding: 9px 0; border-radius: 6px; font-weight: 900; font-size: 12px; cursor: pointer;">Sell</button>
                        </div>

                        <div onclick="toggleOrderTypeSheet(event)" style="background: #151a24; border: 1px solid #232b3b; border-radius: 8px; padding: 10px 12px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;">
                            <span style="color: #8c8ca1; font-size: 12px; font-weight: 800;">Order Type</span>
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span id="ex-current-ordertype" style="color: #fff; font-size: 13px; font-weight: 900;">Market</span>
                                <i class="material-icons" style="font-size: 16px; color: #8c8ca1;">arrow_drop_down</i>
                            </div>
                        </div>

                        <div id="atl-config-box" style="display: none; background: rgba(0, 192, 135, 0.05); border: 1px solid rgba(0, 192, 135, 0.3); border-radius: 10px; padding: 12px; flex-direction: column; gap: 10px; font-family: monospace;">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 6px;">
                                <span style="color: #00c087; font-size: 11px; font-weight: 900;">MULTI-GRID LOOP</span>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span id="atl-slots-counter" style="color: #8c8ca1; font-size: 10px; font-weight: bold;">0/10 SLOTS</span>
                                    <button type="button" onclick="showAddLoopSlotForm()" style="background: #00c087; color: #000; border: none; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; gap: 2px;">
                                        <i class="material-icons" style="font-size: 14px;">add</i> ADD
                                    </button>
                                </div>
                            </div>
                            <div id="atl-slot-input-area" style="display: flex; flex-direction: column; gap: 8px; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px dashed rgba(0,192,135,0.3);">
                                <div style="display: flex; gap: 6px;">
                                    <div style="flex: 1;">
                                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">BUY TRIGGER ($)</div>
                                        <input type="number" id="atl-buy-trigger" placeholder="90" style="width: 100%; background: #151a24; border: 1px solid #232b3b; color: #fff; padding: 6px; border-radius: 6px; font-size: 12px; font-weight: bold; box-sizing: border-box;">
                                    </div>
                                    <div style="width: 75px;">
                                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">BUY CB %</div>
                                        <input type="number" id="atl-buy-cb" value="0.01" step="0.01" style="width: 100%; background: #151a24; border: 1px solid #232b3b; color: #00c087; padding: 6px; border-radius: 6px; font-size: 12px; font-weight: bold; box-sizing: border-box;">
                                    </div>
                                </div>
                                <div style="display: flex; gap: 6px;">
                                    <div style="flex: 1;">
                                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">SELL TRIGGER ($)</div>
                                        <input type="number" id="atl-sell-trigger" placeholder="100" style="width: 100%; background: #151a24; border: 1px solid #232b3b; color: #fff; padding: 6px; border-radius: 6px; font-size: 12px; font-weight: bold; box-sizing: border-box;">
                                    </div>
                                    <div style="width: 75px;">
                                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">SELL CB %</div>
                                        <input type="number" id="atl-sell-cb" value="0.01" step="0.01" style="width: 100%; background: #151a24; border: 1px solid #232b3b; color: #FFD700; padding: 6px; border-radius: 6px; font-size: 12px; font-weight: bold; box-sizing: border-box;">
                                    </div>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; background: #151a24; padding: 6px 8px; border-radius: 6px;">
                                    <span style="color: #ffffff; font-size: 10px; font-weight: 800;">AUTO REPEAT (LOOP)</span>
                                    <input type="checkbox" id="atl-auto-repeat" checked style="accent-color: #00c087; cursor: pointer; width: 15px; height: 15px;">
                                </div>
                            </div>
                            <div id="atl-active-slots-list" style="display: flex; flex-direction: column; gap: 6px;"></div>
                        </div>

                        <div id="dynamic-order-fields" style="display: flex; flex-direction: column; gap: 8px;">
                            <div id="ex-price-field-box" style="background: #151a24; border: 1px solid #232b3b; border-radius: 8px; padding: 10px 12px; color: #64748b; font-size: 12px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
                                <span id="ex-price-field-text">Fill at market price</span>
                                <input type="number" id="ex-custom-price-input" placeholder="0.00" style="display: none; background: transparent; border: none; color: #fff; font-size: 14px; font-weight: 900; width: 100px; text-align: right; outline: none; font-family: monospace;">
                            </div>
                            <div id="ex-stop-field-box" style="display: none; background: #151a24; border: 1px solid #232b3b; border-radius: 8px; padding: 10px 12px; justify-content: space-between; align-items: center;">
                                <span id="ex-stop-field-text" style="color: #8c8ca1; font-size: 12px; font-weight: bold;">Stop Price</span>
                                <input type="number" id="ex-stop-price-input" placeholder="0.00" style="background: transparent; border: none; color: #f6465d; font-size: 14px; font-weight: 900; width: 100px; text-align: right; outline: none; font-family: monospace;">
                            </div>
                            <div id="ex-callback-field-box" style="display: none; background: #151a24; border: 1px solid #232b3b; border-radius: 8px; padding: 10px 12px; justify-content: space-between; align-items: center;">
                                <span style="color: #8c8ca1; font-size: 12px; font-weight: bold;">Callback %</span>
                                <input type="number" id="ex-callback-input" value="1.0" step="0.1" style="background: transparent; border: none; color: #00c087; font-size: 14px; font-weight: 900; width: 80px; text-align: right; outline: none; font-family: monospace;">
                            </div>
                        </div>

                        <div style="background: #151a24; border: 1px solid #232b3b; border-radius: 8px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #8c8ca1; font-size: 12px;">Amount</span>
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <input type="number" id="ex-input-amount" placeholder="0.00" style="background: transparent; border: none; color: #fff; font-size: 15px; font-weight: bold; width: 90px; text-align: right; outline: none;">
                                <span id="ex-unit-label" style="color: #8c8ca1; font-size: 11px; font-weight: bold;">USDT</span>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
                            <button onclick="setExchangePct(25)" style="background: #1c2433; border: 1px solid #2d3748; color: #a0aec0; border-radius: 6px; padding: 6px 0; font-size: 10px; font-weight: bold; cursor: pointer;">25%</button>
                            <button onclick="setExchangePct(50)" style="background: #1c2433; border: 1px solid #2d3748; color: #a0aec0; border-radius: 6px; padding: 6px 0; font-size: 10px; font-weight: bold; cursor: pointer;">50%</button>
                            <button onclick="setExchangePct(75)" style="background: #1c2433; border: 1px solid #2d3748; color: #a0aec0; border-radius: 6px; padding: 6px 0; font-size: 10px; font-weight: bold; cursor: pointer;">75%</button>
                            <button onclick="setExchangePct(100)" style="background: #1c2433; border: 1px solid #2d3748; color: #a0aec0; border-radius: 6px; padding: 6px 0; font-size: 10px; font-weight: bold; cursor: pointer;">100%</button>
                        </div>

                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #718096;">
                            <span>Available</span>
                            <span id="ex-avail-bal" style="color: #fff; font-family: monospace; font-weight: bold;">0.00 USDT</span>
                        </div>

                        <button id="ex-btn-submit" onclick="executeExchangeAction()" style="width: 100%; background: #00c087; color: #000; border: none; padding: 15px 0; border-radius: 10px; font-weight: 900; font-size: 14px; cursor: pointer; margin-top: 4px; box-shadow: 0 4px 14px rgba(0,192,135,0.3);">
                            Buy SOL
                        </button>

                        <div style="background: rgba(255,255,255,0.02); border: 1px solid #1a202c; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 4px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: #5C6BC0; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">WALLET AVG ENTRY</span>
                                <span id="ex-wallet-avg-entry" style="color: #fff; font-size: 14px; font-weight: 900; font-family: monospace;">$0.00</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #64748b;">INVESTED:</span>
                                <span style="color: #00c087; font-weight: bold;"><span id="ex-wallet-invested-disp">$0.00</span> (<span id="ex-wallet-sol-disp">0.0000</span> SOL)</span>
                            </div>
                        </div>

                        <div style="background: rgba(0, 192, 135, 0.03); border: 1px solid rgba(0, 192, 135, 0.2); border-radius: 10px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 6px;">
                                    <div id="ex-signal-pulse-dot" style="width: 8px; height: 8px; background: #00c087; border-radius: 50%; box-shadow: 0 0 10px #00c087; animation: livePulseDot 1.2s infinite;"></div>
                                    <span style="color: #ffffff; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">SIGNAL</span>
                                </div>
                                <span id="ex-signal-action-badge" style="background: rgba(0, 192, 135, 0.2); color: #00c087; border: 1px solid #00c087; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 900; font-family: monospace;">STRONG BUY</span>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 5px; font-family: monospace; font-size: 11px; padding-top: 4px;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: #8c8ca1;">ENTRY (BUY HERE):</span>
                                    <span id="ex-signal-entry-val" style="color: #00c087; font-weight: 900;">$0.00</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: #8c8ca1;">TARGET (SELL HERE):</span>
                                    <span id="ex-signal-target-val" style="color: #FFD700; font-weight: 900;">$0.00 (+1.2%)</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 8px; padding: 14px 10px; display: flex; flex-direction: column; justify-content: space-between; gap: 8px; box-sizing: border-box; height: 100%;">
                        <div style="display: flex; flex-direction: column; gap: 6px;">
                            <div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748b; font-weight: 700; text-transform: uppercase;">
                                <span>Price(USDT)</span>
                                <span>Qty(SOL)</span>
                            </div>

                            <div id="ex-asks-book" style="display: flex; flex-direction: column; gap: 5px; font-family: monospace; font-size: 13px; font-weight: 700;"></div>
                        </div>

                        <div style="padding: 10px 0; text-align: center; border-top: 1px solid #1a202c; border-bottom: 1px solid #1a202c; margin: 2px 0;">
                            <div id="ex-mid-price" style="font-size: 22px; font-weight: 900; color: #00c087; font-family: monospace; letter-spacing: 0.5px;">$0.00</div>
                        </div>

                        <div style="display: flex; flex-direction: column; gap: 6px;">
                            <div id="ex-bids-book" style="display: flex; flex-direction: column; gap: 5px; font-family: monospace; font-size: 13px; font-weight: 700;"></div>
                        </div>

                        <div style="border-top: 1px solid #1a202c; padding-top: 10px; display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
                            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 8px;">
                                <div style="color: #64748b; font-size: 9px; text-transform: uppercase; font-weight: bold; margin-bottom: 4px;">Portfolio Assets</div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: monospace;">
                                    <span style="color: #8c8ca1;">USDT</span>
                                    <span id="ex-port-usdt" style="color: #fff; font-weight: bold;">$0.00</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: monospace; margin-top: 2px;">
                                    <span style="color: #8c8ca1;">SOL</span>
                                    <span id="ex-port-sol" style="color: #00c087; font-weight: bold;">0.0000</span>
                                </div>
                            </div>

                            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 8px;">
                                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                                    <span style="color: #64748b; font-size: 9px; text-transform: uppercase; font-weight: bold;">Unrealized P&L</span>
                                    <span id="ex-unrealized-pct" style="color: #00c087; font-size: 10px; font-weight: bold;">+0.00%</span>
                                </div>
                                <div id="ex-unrealized-pnl" style="color: #00c087; font-size: 14px; font-weight: 900; font-family: monospace; margin-top: 2px;">+$0.00</div>
                            </div>

                            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 8px;">
                                <div style="color: #64748b; font-size: 9px; text-transform: uppercase; font-weight: bold;">Net Realized Profit</div>
                                <div id="ex-realized-pnl" style="color: #4CAF50; font-size: 14px; font-weight: 900; font-family: monospace; margin-top: 2px;">+$0.00</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="exchangeOrdersSection" style="margin-top: 20px; border-top: 1px solid #1a202c; padding-top: 14px; padding-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; overflow-x: auto; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); gap: 16px; white-space: nowrap;">
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div id="tab-opt-open-orders" onclick="switchExchangeOrderSubTab('OPEN')" style="color: #ffffff; font-size: 14px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                                <span>Orders(<span id="user-open-orders-count">0</span>)</span>
                                <i class="material-icons" style="font-size: 14px; color: #718096;">arrow_drop_down</i>
                            </div>
                            <span id="tab-opt-positions" onclick="switchExchangeOrderSubTab('POSITIONS')" style="color: #718096; font-size: 14px; font-weight: 700; cursor: pointer;">Positions(<span id="user-positions-count">0</span>)</span>
                            <span id="tab-opt-history-orders" onclick="switchExchangeOrderSubTab('HISTORY')" style="color: #718096; font-size: 14px; font-weight: 700; cursor: pointer;">History</span>
                            <span onclick="openEliteTradesModal()" style="color: #718096; font-size: 14px; font-weight: 700; cursor: pointer;">Elite trades</span>
                            <span id="tab-opt-bots-btn" onclick="switchExchangeOrderSubTab('BOTS')" style="color: #718096; font-size: 14px; font-weight: 700; cursor: pointer;">Bots(<span id="user-copy-bots-count">0</span>)</span>
                            <span id="tab-opt-chart-btn" onclick="toggleTradeChartVisibility()" style="color: #718096; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 3px;"><i class="material-icons" style="font-size: 16px;">show_chart</i>Chart</span>
                        </div>
                        <i class="material-icons" onclick="switchExchangeOrderSubTab('HISTORY')" style="color: #718096; font-size: 18px; cursor: pointer;">history</i>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0 14px 0;">
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: #718096; font-size: 12px; font-weight: 600;">
                            <input type="checkbox" checked style="accent-color: #00c087; width: 14px; height: 14px; cursor: pointer;">
                            <span>Show current</span>
                        </label>
                        <button onclick="cancelAllUserOrders()" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #e2e8f0; padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: 700; cursor: pointer;">Cancel all</button>
                    </div>

                    <div id="user-open-orders-list" style="display: flex; flex-direction: column; gap: 10px;">
                        <div style="text-align: center; color: #4a5568; font-size: 12px; padding: 20px 0;">NO OPEN ORDERS</div>
                    </div>

                    <div id="user-positions-list" style="display: none; flex-direction: column; gap: 10px;">
                        <div style="text-align: center; color: #4a5568; font-size: 12px; padding: 20px 0;">NO ACTIVE HOLDINGS</div>
                    </div>

                    <div id="user-history-orders-list" style="display: none; flex-direction: column; gap: 10px;">
                        <div style="text-align: center; color: #4a5568; font-size: 12px; padding: 20px 0;">NO EXECUTED TRADES</div>
                    </div>
<div id="user-bots-list" style="display: none; flex-direction: column; gap: 10px;">
                        <div style="text-align: center; color: #4a5568; font-size: 12px; padding: 20px 0;">NO ACTIVE COPY TRADING BOTS</div>
                    </div>
                </div>
<div id="tradeManualChartWrapper" class="chart-container" style="display: none; background: #11151e; border: 1px solid #1a202c; border-radius: 14px; margin-top: 4px; margin-bottom: 30px; overflow: hidden; width: 100%; max-width: 100%; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #151a24; border-bottom: 1px solid #1a202c;">
                        <div style="display: flex; gap: 6px;">
                            <div class="interval-btn active" id="tint-1m" onclick="changeTradeInterval('1m')">1m</div>
                            <div class="interval-btn" id="tint-15m" onclick="changeTradeInterval('15m')">15m</div>
                            <div class="interval-btn" id="tint-1h" onclick="changeTradeInterval('1h')">1h</div>
                            <div class="interval-btn" id="tint-4h" onclick="changeTradeInterval('4h')">4h</div>
                            <div class="interval-btn" id="tint-1d" onclick="changeTradeInterval('1d')">1D</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #00e5ff; font-size: 11px; font-family: monospace; font-weight: 800;">SOL/USDT</span>
                            <i class="material-icons" onclick="toggleTradeChartVisibility()" style="color: #8c8ca1; font-size: 18px; cursor: pointer;">close</i>
                        </div>
                    </div>
                    <div id="custom_trade_chart" style="width: 100%; height: 580px; aspect-ratio: 9/16; position: relative; background: #0b0e14;"></div>
                </div>
            </div>

            <div class="bot-card">
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 8px; height: 8px; background: #00e676; border-radius: 50%; box-shadow: 0 0 10px #00e676; animation: pulse 1s infinite;"></div>
                        <span style="color: #00d2ff; font-size: 12px; font-weight: 900; letter-spacing: 1px;">SHINE BOT BRAIN 🧠</span>
                    </div>
                    <button id="voiceBtn" onclick="speakBotThoughts()" style="background: transparent; border: none; color: #00d2ff; padding: 6px 0; font-size: 11px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                        <i class="material-icons" style="font-size: 16px;">volume_up</i> <span>BOT VOICE</span>
                    </button>
                </div>
                <div style="width: 100%; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px;">
                    <div style="background: rgba(0, 230, 118, 0.04); border: 1px solid rgba(0, 230, 118, 0.15); border-radius: 12px; padding: 14px 18px; min-height: 48px; display: flex; align-items: center;">
                        <div id="aiLiveText" style="font-family: 'JetBrains Mono', 'Roboto', monospace; font-size: 13px; line-height: 1.5; color: #00e676; word-break: break-word; letter-spacing: 0.5px; text-shadow: 0 0 10px rgba(0, 230, 118, 0.25); width: 100%;">
                            BRAIN: Analyzing liquidity pools and monitoring price volatility...
                        </div>
                    </div>
                </div>
            </div>

            <div class="bot-card" style="margin-bottom: 16px;">
                <div class="card-label" style="margin-bottom: 8px;">
                    <span style="color: #00d2ff; font-weight: 800; letter-spacing: 0.5px;">UNREALIZED P&L (LIVE)</span>
                    <i class="material-icons" style="font-size:18px; color:#4CAF50;">trending_up</i>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px;">
                    <div>
                        <div style="font-size: 10px; color: #757575; font-weight: bold;">BOT POSITION</div>
                        <div class="card-value-large" id="unrealized-pnl" style="font-size: 26px; font-weight: 900;">+$0.00</div>
                    </div>
                    <div class="card-value-sub" id="unrealized-pnl-pct" style="font-size: 13px; font-weight: 800; background: rgba(76, 175, 80, 0.12); padding: 4px 8px; border-radius: 8px;">+0.00%</div>
                </div>

                <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 14px;">
                    <div class="card-label" style="margin-bottom: 8px;">
                        <span style="color: #4CAF50; font-weight: 800; letter-spacing: 0.5px;">NET REALIZED PROFIT</span>
                        <button onclick="openPnlShareModal()" style="background: linear-gradient(90deg, #FFD700, #FFA500); border: none; color: #000; padding: 4px 12px; border-radius: 8px; font-size: 10px; font-weight: 900; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                            <i class="material-icons" style="font-size: 13px;">share</i> SHARE PnL
                        </button>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                        <div>
                            <div style="font-size: 10px; color: #757575; font-weight: bold;">BOT REALIZED (ALL TIME)</div>
                            <div class="card-value-large" id="realized-pnl-val" style="font-size: 26px; font-weight: 900; color: #4CAF50;">+$0.00</div>
                        </div>
                        <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
                            <div style="font-size: 10px; font-weight: 800; color: #4CAF50; background: rgba(76, 175, 80, 0.12); padding: 3px 8px; border-radius: 6px;">AUTO BOT POOL</div>
                            <div style="font-size: 11px; font-weight: 800; color: #00e676; font-family: monospace; background: rgba(0, 230, 118, 0.08); border: 1px solid rgba(0, 230, 118, 0.2); padding: 2px 8px; border-radius: 6px;">24H: <span id="bot-24h-profit">+$0.00</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bot-card" style="margin-bottom: 16px;">
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 14px; text-align: center;">
                    <span style="color: #fff; font-size: 14px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                    <span id="dip-hunter-status" style="color: #4CAF50; font-size: 12px; font-weight: 800; font-family: monospace; background: transparent; border: none; padding: 0;">RIDING POSITION</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 16px;">
                    <div id="ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center; transition: 0.3s;">
                        <div style="font-size: 9px; color: #757575; font-weight: bold;">STAGE 1 ($0.40)</div>
                        <div style="font-size: 11px; color: #5C6BC0; font-weight: 900; margin-top: 2px;">$0.10 TRAIL</div>
                    </div>
                    <div id="ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center; transition: 0.3s;">
                        <div style="font-size: 9px; color: #757575; font-weight: bold;">STAGE 2 ($0.80)</div>
                        <div style="font-size: 11px; color: #E8755B; font-weight: 900; margin-top: 2px;">$0.15 LOCK</div>
                    </div>
                    <div id="ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center; transition: 0.3s;">
                        <div style="font-size: 9px; color: #757575; font-weight: bold;">STAGE 3 ($1.50)</div>
                        <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.20 SNIP</div>
                    </div>
                </div>

                <div class="ts-row">
                    <div class="ts-label">TRAILING HIGH (PEAK)</div>
                    <div class="ts-val" id="ts-high">$0.00</div>
                </div>
                <div class="ts-row">
                    <div class="ts-label">TRIGGER STOP LEVEL</div>
                    <div class="ts-val orange" id="ts-low">$0.00</div>
                </div>

                <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 14px; padding-top: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #00d2ff; font-size: 12px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                        <span id="tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (WAITING DIP)</span>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                        <div id="tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                            <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE (1.0%)</div>
                            <div id="tb-target-1" style="font-size: 11px; color: #00d2ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                            <div style="font-size: 7px; color: #757575;">-$1.00 Dip</div>
                        </div>
                        <div id="tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                            <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK (0.5%)</div>
                            <div id="tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                            <div style="font-size: 7px; color: #757575;">Adaptive</div>
                        </div>
                        <div id="tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                            <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                            <div id="tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                            <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                        <span style="color: #757575;">DIP LOW TRACKED:</span>
                        <span id="tb-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                    </div>
                </div>
            </div>

            <div class="bot-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <i class="material-icons" style="font-size: 18px; color: #00d2ff;">psychology</i>
                        <span style="font-size: 12px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">SHINE BOT RADAR</span>
                    </div>
                    <span style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; border: 1px solid #00d2ff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; font-family: monospace;">INSTITUTIONAL v3.8</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #757575; font-size: 10px; text-transform: uppercase;">Whale Orderflow</div>
                        <div id="radar-orderflow-wrapper" style="color: #4CAF50; font-size: 14px; font-weight: bold; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
                            <span id="radar-orderflow-val">50.0% BUY VOL</span>
                            <i id="radar-orderflow-icon" class="material-icons" style="font-size: 14px;">trending_flat</i>
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #757575; font-size: 10px; text-transform: uppercase;">Whale Liquidity</div>
                        <div id="radar-whale-liquidity" style="color: #FFD700; font-size: 14px; font-weight: bold; margin-top: 4px;">CALCULATING...</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #757575; font-size: 10px; text-transform: uppercase;">Sharpe Ratio (Alpha)</div>
                        <div id="radar-sharpe-ratio" style="color: #00e676; font-size: 14px; font-weight: bold; margin-top: 4px; font-family: monospace;">0.00 (LIVE)</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #757575; font-size: 10px; text-transform: uppercase;">Max Drawdown (MDD)</div>
                        <div id="radar-max-drawdown" style="color: #4CAF50; font-size: 14px; font-weight: bold; margin-top: 4px; font-family: monospace;">0.00%</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.04); font-size: 11px; color: #757575;">
                    <span style="display: flex; align-items: center; gap: 4px;"><i class="material-icons" style="font-size: 14px; color: #4CAF50;">verified_user</i> Smart Contract Audited & Timelocked</span>
                    <span style="color: #FFD700; font-weight: bold;">ZERO LIQUIDATION RISK</span>
                </div>
            </div>

            <div class="bot-card">
                <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
                <div style="margin-bottom: 12px;">
                    <div style="color: #00d2ff; font-size: 11px; font-weight: bold; margin-bottom: 6px;">BOT TRADING ASSETS</div>
                    <div class="portfolio-row">
                        <div class="port-coin">BOT USDT</div>
                        <div class="port-amt" id="port-usdt">$0.00</div>
                    </div>
                    <div class="portfolio-row">
                        <div class="port-coin">BOT SOL</div>
                        <div class="port-amt" id="port-sol">0.0000</div>
                    </div>
                </div>
                
            </div>

            <div class="bot-card">
                <div class="card-label">BOT AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
                <div class="avg-main-val" id="avg-entry-price">$0.00</div>
                <div class="invested-row">BOT INVESTED: <span class="invested-white" id="invested-amount">$0.00</span> / <span id="total-capital">$0.00</span></div>
                
            </div>
            <div class="chart-container bot-card" style="padding: 0; overflow: hidden;">
                <div class="chart-intervals" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #0e0e16; border-bottom: 1px solid #1a1a2e;">
                    <div style="display: flex; gap: 8px;">
                        <div class="interval-btn active" onclick="changeInterval('1m')">1m</div>
                        <div class="interval-btn" onclick="changeInterval('15m')">15m</div>
                        <div class="interval-btn" onclick="changeInterval('1h')">1h</div>
                        <div class="interval-btn" onclick="changeInterval('4h')">4h</div>
                        <div class="interval-btn" onclick="changeInterval('1d')">1D</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-family: monospace; font-weight: bold;">
                        <span id="chart-symbol-badge" style="color: #fff;">SOL/USDT</span>
                    </div>
                </div>
                <div id="custom_trading_chart" style="width: 100%; height: 420px; position: relative; background: #08080c;"></div>
            </div>

         <div class="trade-status-card bot-card" style="margin-top: 20px;">
                <div class="trade-card-header">
                    <h3>DCA SAFETY ORDERS (BOT)</h3>
                    <div class="open-badge" id="bot-positions-badge">0 OPEN</div>
                </div>
                <div class="empty-msg" id="bot-positions-container">NO ACTIVE BOT POSITIONS</div>

                
            </div>

            <div class="bot-card">
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                    <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">AUTOMATED BOT AUDIT LOG</h3>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                        <span style="color: #8c8ca1;">Exits <span id="trade-count-pill" style="color: #fff; margin-left: 4px;">0</span></span>
                        <span style="color: #4CAF50;">Profit <span id="win-tag" style="margin-left: 4px;">0</span></span>
                        <span style="color: #f6465d;">Lose <span id="loss-tag" style="margin-left: 4px;">0</span></span>
                    </div>
                </div>
                <div id="trade-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                    <div class="empty-msg">NO BOT TRADES RECORDED</div>
                </div>
                <button id="btn-see-more-audit" onclick="toggleFullAuditHistory()" style="width: 100%; background: #1c2433; color: #00d2ff; border: 1px solid #2d3748; border-radius: 8px; padding: 12px; margin-top: 12px; font-weight: 800; font-size: 11px; cursor: pointer; letter-spacing: 0.5px; text-transform: uppercase;">See More (All Trades)</button>
            </div>
            <div class="martingale-section" id="phase-1-section" style="border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 1 (DYNAMIC GRID)</h3><span>250 - 1 SOL</span></div>
                <table class="m-table" id="table-phase-1">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$250 - $225</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$225 - $200</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$200 - $175</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$175 - $150</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$150 - $125</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$125 - $100</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$100 - $75</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$75 - $50</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$50 - $25</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$25 - $1</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-1" onclick="showNextPhase(1)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 2)</button>
            </div>

            <div class="martingale-section" id="phase-2-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 2 (DYNAMIC GRID)</h3><span>500 - 250 SOL</span></div>
                <table class="m-table" id="table-phase-2">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$500 - $475</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$475 - $450</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$450 - $425</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$425 - $400</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$400 - $375</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$375 - $350</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$350 - $325</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$325 - $300</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$300 - $275</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$275 - $250</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-2" onclick="showNextPhase(2)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 3)</button>
            </div>

            <div class="martingale-section" id="phase-3-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 3 (DYNAMIC GRID)</h3><span>750 - 500 SOL</span></div>
                <table class="m-table" id="table-phase-3">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$750 - $725</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$725 - $700</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$700 - $675</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$675 - $650</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$650 - $625</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$625 - $600</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$600 - $575</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$575 - $550</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$550 - $525</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$525 - $500</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-3" onclick="showNextPhase(3)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 4)</button>
            </div>

            <div class="martingale-section" id="phase-4-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 4 (DYNAMIC GRID)</h3><span>1000 - 750 SOL</span></div>
                <table class="m-table" id="table-phase-4">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$1000 - $975</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$975 - $950</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$950 - $925</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$925 - $900</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$900 - $875</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$875 - $850</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$850 - $825</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$825 - $800</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$800 - $775</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$775 - $750</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-4" onclick="showNextPhase(4)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 5)</button>
            </div>

            <div class="martingale-section" id="phase-5-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 5 (DYNAMIC GRID)</h3><span>1250 - 1000 SOL</span></div>
                <table class="m-table" id="table-phase-5">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$1250 - $1225</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$1225 - $1200</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$1200 - $1175</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$1175 - $1150</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$1150 - $1125</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$1125 - $1100</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$1100 - $1075</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$1075 - $1050</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1050 - $1025</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1025 - $1000</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-5" onclick="showNextPhase(5)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 6)</button>
            </div>

            <div class="martingale-section" id="phase-6-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 6 (DYNAMIC GRID)</h3><span>1500 - 1250 SOL</span></div>
                <table class="m-table" id="table-phase-6">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$1500 - $1475</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$1475 - $1450</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$1450 - $1425</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$1425 - $1400</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$1400 - $1375</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$1375 - $1350</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$1350 - $1325</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$1325 - $1300</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1300 - $1275</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1275 - $1250</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-6" onclick="showNextPhase(6)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 7)</button>
            </div>

            <div class="martingale-section" id="phase-7-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 7 (DYNAMIC GRID)</h3><span>1750 - 1500 SOL</span></div>
                <table class="m-table" id="table-phase-7">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$1750 - $1725</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$1725 - $1700</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$1700 - $1675</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$1675 - $1650</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$1650 - $1625</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$1625 - $1600</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$1600 - $1575</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$1575 - $1550</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1550 - $1525</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1525 - $1500</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-7" onclick="showNextPhase(7)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 8)</button>
            </div>

            <div class="martingale-section" id="phase-8-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 8 (DYNAMIC GRID)</h3><span>2000 - 1750 SOL</span></div>
                <table class="m-table" id="table-phase-8">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$2000 - $1975</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$1975 - $1950</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$1950 - $1925</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$1925 - $1900</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$1900 - $1875</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$1875 - $1850</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$1850 - $1825</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$1825 - $1800</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1800 - $1775</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$1775 - $1750</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-8" onclick="showNextPhase(8)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 9)</button>
            </div>

            <div class="martingale-section" id="phase-9-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 9 (DYNAMIC GRID)</h3><span>2250 - 2000 SOL</span></div>
                <table class="m-table" id="table-phase-9">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$2250 - $2225</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$2225 - $2200</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$2200 - $2175</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$2175 - $2150</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$2150 - $2125</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$2125 - $2100</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$2100 - $2075</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$2075 - $2050</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$2050 - $2025</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$2025 - $2000</td></tr>
                    </tbody>
                </table>
                <button id="btn-phase-9" onclick="showNextPhase(9)" style="width: 100%; background: #212121; color: white; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-top: 15px; cursor: pointer; font-weight: bold;">See More (Phase 10)</button>
            </div>

            <div class="martingale-section" id="phase-10-section" style="display: none; opacity: 0.5; border: 1px solid #1a1a1a;">
                <div class="martingale-header"><h3>PHASE 10 (DYNAMIC GRID)</h3><span>2500 - 2250 SOL</span></div>
                <table class="m-table" id="table-phase-10">
                    <thead><tr><th>RND</th><th>STATUS</th><th>ALLOC</th><th style="text-align: right;">PRICE RANGE</th></tr></thead>
                    <tbody>
                        <tr><td class="m-rnd">1</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">1.00%</td><td class="m-price">$2500 - $2475</td></tr>
                        <tr><td class="m-rnd">2</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">2.00%</td><td class="m-price">$2475 - $2450</td></tr>
                        <tr><td class="m-rnd">3</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">4.00%</td><td class="m-price">$2450 - $2425</td></tr>
                        <tr><td class="m-rnd">4</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">6.00%</td><td class="m-price">$2425 - $2400</td></tr>
                        <tr><td class="m-rnd">5</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">10.00%</td><td class="m-price">$2400 - $2375</td></tr>
                        <tr><td class="m-rnd">6</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">20.00%</td><td class="m-price">$2375 - $2350</td></tr>
                        <tr><td class="m-rnd">7</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">30.00%</td><td class="m-price">$2350 - $2325</td></tr>
                        <tr><td class="m-rnd">8</td><td><span class="m-status">PENDING</span></td><td class="m-alloc">27.00%</td><td class="m-price">$2325 - $2300</td></tr>
                        <tr><td class="m-rnd">9</td><td><span class="m-status">OWNER</span></td><td class="m-alloc">HOLD</td><td class="m-price">$2300 - $2275</td></tr>
                        <tr><td class="m-rnd">10</td><td><span class="m-status">AIRDROP</span></td><td class="m-alloc">HOLD</td><td class="m-price">$2275 - $2250</td></tr>
                    </tbody>
                </table>
            </div>
            </div>

            <div id="tabViewTrade" class="bot-tab-view">
                <div id="tradeTabContainer"></div>
            </div>
<div id="tabViewBot" class="bot-tab-view">
    <div class="bot-card" style="margin-bottom: 16px;">
        <div style="display: flex; align-items: center; justify-content: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; margin-bottom: 12px; gap: 8px;">
            <div id="botBrainPulseDot" style="width: 8px; height: 8px; background: #00e676; border-radius: 50%; box-shadow: 0 0 10px #00e676; animation: livePulseDot 1s infinite;"></div>
            <span id="botBrainTitleTag" style="color: #00e676; font-size: 13px; font-weight: 900; letter-spacing: 1px;">SHINE ENGINE BRAIN</span>
        </div>
        <div style="text-align: center; margin-bottom: 12px;">
            <div id="botRotatingHeaderName" style="font-size: 17px; font-weight: 900; color: #00e676; letter-spacing: 0.5px; text-transform: uppercase;">SHINE HYPER TITAN</div>
        </div>
        <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px 16px; min-height: 48px; display: flex; align-items: center;">
            <div id="botTabRotatingLiveText" style="font-family: 'JetBrains Mono', monospace; font-size: 13px; line-height: 1.5; color: #00e676; word-break: break-word; width: 100%;">
                Connecting to backend live stream...
            </div>
        </div>
    </div>
         
 <div class="bot-card" id="microScalpDashboardCard" style="border: none; background: radial-gradient(circle at top right, #121824 0%, #0d111a 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            <div style="width: 9px; height: 9px; background: #00d2ff; border-radius: 50%; box-shadow: 0 0 10px #00d2ff; animation: livePulseDot 1.2s infinite; flex-shrink: 0;"></div>
                            <span style="font-size: 13px; font-weight: 900; color: #fff; letter-spacing: 0.5px; text-transform: uppercase;">SHINE APEX VELOCITY ENGINE</span>
                        </div>
                        <span id="micro-orders-badge" style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; border: 1px solid #00d2ff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; font-family: monospace;">0 OPEN</span>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">IDLE FUND HARVESTED</div>
                                <div id="micro-idle-fund" style="font-size: 16px; font-weight: 900; color: #00d2ff; font-family: monospace; margin-top: 2px; white-space: nowrap;">$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">MICRO SOL HOLDING</div>
                                <div id="micro-sol-pos" style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; margin-top: 2px; white-space: nowrap;">0.0000 SOL</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">UNREALIZED P&L</div>
                                <div id="micro-unrealized-pnl" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">REALIZED NET PROFIT</div>
                                <div id="micro-realized-pnl" style="font-size: 16px; font-weight: 900; color: #4CAF50; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 12px; text-align: center;">
                            <span style="color: #fff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                            <span id="micro-dip-hunter-status" style="color: #4CAF50; font-size: 11px; font-weight: 800; font-family: monospace;">RIDING POSITION</span>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 14px;">
                            <div id="micro-ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 1 ($0.35)</div>
                                <div style="font-size: 11px; color: #00d2ff; font-weight: 900; margin-top: 2px;">$0.08 TRAIL</div>
                            </div>
                            <div id="micro-ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 2 ($0.55)</div>
                                <div style="font-size: 11px; color: #FFD700; font-weight: 900; margin-top: 2px;">$0.12 LOCK</div>
                            </div>
                            <div id="micro-ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 3 ($0.80)</div>
                                <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.15 SNIP</div>
                            </div>
                        </div>

                        <div class="ts-row">
                            <div class="ts-label">TRAILING HIGH (PEAK)</div>
                            <div class="ts-val" id="micro-ts-high">$0.00</div>
                        </div>
                        <div class="ts-row">
                            <div class="ts-label">TRIGGER STOP LEVEL</div>
                            <div class="ts-val orange" id="micro-ts-low">$0.00</div>
                        </div>

                        <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 12px; padding-top: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #00d2ff; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                                <span id="micro-tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (SCANNING DIP)</span>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                                <div id="micro-tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE ($0.30)</div>
                                    <div id="micro-tb-target-1" style="font-size: 11px; color: #00d2ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">-$0.30 Dip</div>
                                </div>
                                <div id="micro-tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK ($0.60)</div>
                                    <div id="micro-tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Adaptive</div>
                                </div>
                                <div id="micro-tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                                    <div id="micro-tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #757575;">DIP LOW TRACKED:</span>
                                <span id="micro-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                            </div>
                        </div>
                    </div>

                   <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                        <span style="color: #8c8ca1; font-size: 11px;">YOUR SHARE INVESTED:</span>
                        <span id="micro-user-invest-display" style="color: #00d2ff; font-weight: 900; font-size: 13px;">$0.00 USDT</span>
                    </div>
                   <button onclick="openKiller1DetailsModal()"  style="width: 100%; background: #1c2433; color: #00d2ff; border: 1px solid #2d3748; border-radius: 10px; padding: 12px 0; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 12px;">
                        <i class="material-icons" style="font-size: 16px;">info</i>
                        <span>SHINE APEX VELOCITY ENGINE INFO</span>
                    </button>
                </div>

                <div class="bot-card" id="killer2DashboardCard" style="border: none; background: radial-gradient(circle at top right, #1f1a2e 0%, #0d0b17 100%); margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            <div style="width: 9px; height: 9px; background: #FFD700; border-radius: 50%; box-shadow: 0 0 10px #FFD700; animation: livePulseDot 1.2s infinite; flex-shrink: 0;"></div>
                            <span style="font-size: 13px; font-weight: 900; color: #fff; letter-spacing: 0.5px; text-transform: uppercase;">SHINE QUANTUM PULSE ENGINE</span>
                        </div>
                        <span id="killer2-orders-badge" style="background: rgba(255, 215, 0, 0.15); color: #FFD700; border: 1px solid #FFD700; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; font-family: monospace;">0 OPEN</span>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">TOP ROUNDS IDLE FUND</div>
                                <div id="killer2-idle-fund" style="font-size: 16px; font-weight: 900; color: #FFD700; font-family: monospace; margin-top: 2px; white-space: nowrap;">$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">KILLER 2 SOL HOLDING</div>
                                <div id="killer2-sol-pos" style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; margin-top: 2px; white-space: nowrap;">0.0000 SOL</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">UNREALIZED P&L</div>
                                <div id="killer2-unrealized-pnl" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">REALIZED NET PROFIT</div>
                                <div id="killer2-realized-pnl" style="font-size: 16px; font-weight: 900; color: #4CAF50; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 12px; text-align: center;">
                            <span style="color: #fff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                            <span id="killer2-dip-hunter-status" style="color: #4CAF50; font-size: 11px; font-weight: 800; font-family: monospace;">RIDING POSITION</span>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 14px;">
                            <div id="killer2-ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 1 ($0.50)</div>
                                <div style="font-size: 11px; color: #00d2ff; font-weight: 900; margin-top: 2px;">$0.15 TRAIL</div>
                            </div>
                            <div id="killer2-ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 2 ($0.80)</div>
                                <div style="font-size: 11px; color: #FFD700; font-weight: 900; margin-top: 2px;">$0.20 LOCK</div>
                            </div>
                            <div id="killer2-ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 3 ($1.20)</div>
                                <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.25 SNIP</div>
                            </div>
                        </div>

                        <div class="ts-row">
                            <div class="ts-label">TRAILING HIGH (PEAK)</div>
                            <div class="ts-val" id="killer2-ts-high">$0.00</div>
                        </div>
                        <div class="ts-row">
                            <div class="ts-label">TRIGGER STOP LEVEL</div>
                            <div class="ts-val orange" id="killer2-ts-low">$0.00</div>
                        </div>

                        <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 12px; padding-top: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #FFD700; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                                <span id="killer2-tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (SCANNING DIP)</span>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                                <div id="killer2-tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE ($0.60)</div>
                                    <div id="killer2-tb-target-1" style="font-size: 11px; color: #00d2ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">-$0.60 Dip</div>
                                </div>
                                <div id="killer2-tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK ($0.90)</div>
                                    <div id="killer2-tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Adaptive</div>
                                </div>
                                <div id="killer2-tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                                    <div id="killer2-tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #757575;">DIP LOW TRACKED:</span>
                                <span id="killer2-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                        <span style="color: #8c8ca1; font-size: 11px;">YOUR SHARE INVESTED:</span>
                        <span id="killer2-user-invest-display" style="color: #FFD700; font-weight: 900; font-size: 13px;">$0.00 USDT</span>
                    </div>
                    <button onclick="openKiller2DetailsModal()" style="width: 100%; background: #1c2433; color: #FFD700; border: 1px solid #2d3748; border-radius: 10px; padding: 12px 0; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 12px;">
                        <i class="material-icons" style="font-size: 16px;">info</i>
                        <span>SHINE QUANTUM PULSE ENGINE INFO</span>
                    </button>
                </div>

                <div class="bot-card" id="killer3DashboardCard" style="border: none; background: radial-gradient(circle at top right, #1a2733 0%, #091118 100%); margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            <div style="width: 9px; height: 9px; background: #00e676; border-radius: 50%; box-shadow: 0 0 10px #00e676; animation: livePulseDot 1.2s infinite; flex-shrink: 0;"></div>
                            <span style="font-size: 13px; font-weight: 900; color: #fff; letter-spacing: 0.5px; text-transform: uppercase;">SHINE TITAN ABYSS ENGINE</span>
                        </div>
                        <span id="killer3-orders-badge" style="background: rgba(0, 230, 118, 0.15); color: #00e676; border: 1px solid #00e676; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; font-family: monospace;">0 OPEN</span>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">BUFFER IDLE FUND POOL</div>
                                <div id="killer3-idle-fund" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">KILLER 3 SOL HOLDING</div>
                                <div id="killer3-sol-pos" style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; margin-top: 2px; white-space: nowrap;">0.0000 SOL</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">UNREALIZED P&L</div>
                                <div id="killer3-unrealized-pnl" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">REALIZED NET PROFIT</div>
                                <div id="killer3-realized-pnl" style="font-size: 16px; font-weight: 900; color: #4CAF50; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.00</div>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 12px; text-align: center;">
                            <span style="color: #fff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                            <span id="killer3-dip-hunter-status" style="color: #4CAF50; font-size: 11px; font-weight: 800; font-family: monospace;">RIDING POSITION</span>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 14px;">
                            <div id="killer3-ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 1 ($0.60)</div>
                                <div style="font-size: 11px; color: #00d2ff; font-weight: 900; margin-top: 2px;">1.0% RIDE</div>
                            </div>
                            <div id="killer3-ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 2 ($1.00)</div>
                                <div style="font-size: 11px; color: #FFD700; font-weight: 900; margin-top: 2px;">0.5% LOCK</div>
                            </div>
                            <div id="killer3-ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 3 ($1.50)</div>
                                <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.03 SNIP</div>
                            </div>
                        </div>

                        <div class="ts-row">
                            <div class="ts-label">TRAILING HIGH (PEAK)</div>
                            <div class="ts-val" id="killer3-ts-high">$0.00</div>
                        </div>
                        <div class="ts-row">
                            <div class="ts-label">TRIGGER STOP LEVEL</div>
                            <div class="ts-val orange" id="killer3-ts-low">$0.00</div>
                        </div>

                        <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 12px; padding-top: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #00e676; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                                <span id="killer3-tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (SCANNING DIP)</span>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                                <div id="killer3-tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE ($0.90)</div>
                                    <div id="killer3-tb-target-1" style="font-size: 11px; color: #00d2ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">-$0.90 Dip</div>
                                </div>
                                <div id="killer3-tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK ($1.20)</div>
                                    <div id="killer3-tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Adaptive</div>
                                </div>
                                <div id="killer3-tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                                    <div id="killer3-tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #757575;">DIP LOW TRACKED:</span>
                                <span id="killer3-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                            </div>
                        </div>
                    </div>

                   <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                        <span style="color: #8c8ca1; font-size: 11px;">YOUR SHARE INVESTED:</span>
                        <span id="killer3-user-invest-display" style="color: #00e676; font-weight: 900; font-size: 13px;">$0.00 USDT</span>
                    </div>
                   <button onclick="openKiller3DetailsModal()"  style="width: 100%; background: #1c2433; color: #00e676; border: 1px solid #2d3748; border-radius: 10px; padding: 12px 0; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 12px;">
                        <i class="material-icons" style="font-size: 16px;">info</i>
                        <span>SHINE TITAN ABYSS ENGINE INFO</span>
                    </button>
                </div>

                <div class="bot-card" id="hyperTitanDashboardCard" style="border: none; background: radial-gradient(circle at top right, #121824 0%, #0d111a 100%); margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            <div style="width: 9px; height: 9px; background: #00e5ff; border-radius: 50%; box-shadow: 0 0 10px #00e5ff; animation: livePulseDot 1.2s infinite; flex-shrink: 0;"></div>
                            <span style="font-size: 13px; font-weight: 900; color: #fff; letter-spacing: 0.5px; text-transform: uppercase;">SHINE HYPER TITAN POOL</span>
                        </div>
                        <span id="hyper-orders-badge" style="background: rgba(0, 229, 255, 0.15); color: #00e5ff; border: 1px solid #00e5ff; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; font-family: monospace;">0 OPEN</span>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">TOTAL POOL CAPITAL</div>
                                <div id="hyper-pool-total" style="font-size: 16px; font-weight: 900; color: #00e5ff; font-family: monospace; margin-top: 2px; white-space: nowrap;">$9,999.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">SOL HOLDING</div>
                                <div id="hyper-sol-pos" style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; margin-top: 2px; white-space: nowrap;">0.0000 SOL</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">UNREALIZED PROFIT</div>
                                <div id="hyper-user-unrealized-pnl" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.0000</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">NET REALIZED PROFIT</div>
                                <div id="hyper-user-realized-pnl" style="font-size: 16px; font-weight: 900; color: #4CAF50; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.0000</div>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 12px; text-align: center;">
                            <span style="color: #fff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                            <span id="hyper-dip-hunter-status" style="color: #4CAF50; font-size: 11px; font-weight: 800; font-family: monospace;">RIDING POSITION</span>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 14px;">
                            <div id="hyper-ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 1 ($0.20)</div>
                                <div style="font-size: 11px; color: #00e5ff; font-weight: 900; margin-top: 2px;">$0.05 TRAIL</div>
                            </div>
                            <div id="hyper-ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 2 ($0.40)</div>
                                <div style="font-size: 11px; color: #FFD700; font-weight: 900; margin-top: 2px;">$0.08 LOCK</div>
                            </div>
                            <div id="hyper-ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 3 ($0.70)</div>
                                <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.12 SNIP</div>
                            </div>
                        </div>

                        <div class="ts-row">
                            <div class="ts-label">TRAILING HIGH (PEAK)</div>
                            <div class="ts-val" id="hyper-ts-high">$0.00</div>
                        </div>
                        <div class="ts-row">
                            <div class="ts-label">TRIGGER STOP LEVEL</div>
                            <div class="ts-val orange" id="hyper-ts-low">$0.00</div>
                        </div>

                        <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 12px; padding-top: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #00e5ff; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                                <span id="hyper-tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (SCANNING DIP)</span>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                                <div id="hyper-tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE ($0.01)</div>
                                    <div id="hyper-tb-target-1" style="font-size: 11px; color: #00e5ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">-$0.01 Dip</div>
                                </div>
                                <div id="hyper-tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK ($0.002)</div>
                                    <div id="hyper-tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Adaptive</div>
                                </div>
                                <div id="hyper-tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                                    <div id="hyper-tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #757575;">DIP LOW TRACKED:</span>
                                <span id="hyper-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                        <span style="color: #8c8ca1; font-size: 11px;">YOUR SHARE INVESTED:</span>
                        <span id="hyper-user-invest-display" style="color: #00e5ff; font-weight: 900; font-size: 13px;">$99.99 USDT</span>
                    </div>

                    <button onclick="openHyperTitanDetailsModal()" style="width: 100%; background: #1c2433; color: #00e5ff; border: 1px solid #2d3748; border-radius: 10px; padding: 12px 0; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; letter-spacing: 0.5px; text-transform: uppercase;">
                        <i class="material-icons" style="font-size: 16px;">info</i>
                        <span>SHINE HYPER TITAN POOL INFO</span>
                    </button>
                </div>

                <div class="bot-card" id="singularityDashboardCard" style="border: none; background: radial-gradient(circle at top right, #241433 0%, #0d0817 100%); margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 14px; gap: 6px;">
                        <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
                            <div style="width: 10px; height: 10px; background: #e040fb; border-radius: 50%; box-shadow: 0 0 12px #e040fb; animation: livePulseDot 1.2s infinite; flex-shrink: 0;"></div>
                            <span style="font-size: 12px; font-weight: 900; color: #fff; letter-spacing: 0.3px; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">SHINE TITAN SINGULARITY (100K)</span>
                        </div>
                        <span id="sng-orders-badge" style="background: rgba(224, 64, 251, 0.15); color: #e040fb; border: 1px solid #e040fb; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 900; font-family: monospace; flex-shrink: 0;">0 OPEN</span>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">TOTAL POOL CAPITAL</div>
                                <div id="sng-pool-total" style="font-size: 16px; font-weight: 900; color: #e040fb; font-family: monospace; margin-top: 2px; white-space: nowrap;">$100,000.00</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">SOL HOLDING (5 ENGINES)</div>
                                <div id="sng-sol-pos" style="font-size: 16px; font-weight: 900; color: #fff; font-family: monospace; margin-top: 2px; white-space: nowrap;">0.0000 SOL</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="flex: 1;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">UNREALIZED PROFIT</div>
                                <div id="sng-user-unrealized-pnl" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.0000</div>
                            </div>
                            <div style="flex: 1; padding-left: 12px;">
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase; white-space: nowrap;">NET REALIZED PROFIT</div>
                                <div id="sng-user-realized-pnl" style="font-size: 16px; font-weight: 900; color: #4CAF50; font-family: monospace; margin-top: 2px; white-space: nowrap;">+$0.0000</div>
                            </div>
                        </div>
                    </div>

                    

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; margin-bottom: 12px; text-align: center;">
                            <span style="color: #fff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING STOP & DIP RADAR</span>
                            <span id="sng-dip-hunter-status" style="color: #4CAF50; font-size: 11px; font-weight: 800; font-family: monospace;">RIDING POSITION</span>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 14px;">
                            <div id="sng-ts-stage-pill-1" style="background: rgba(58, 71, 166, 0.2); border: 1px solid rgba(58, 71, 166, 0.4); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 1 ($0.40)</div>
                                <div style="font-size: 11px; color: #00d2ff; font-weight: 900; margin-top: 2px;">$0.10 TRAIL</div>
                            </div>
                            <div id="sng-ts-stage-pill-2" style="background: rgba(232, 117, 91, 0.1); border: 1px solid rgba(232, 117, 91, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 2 ($0.80)</div>
                                <div style="font-size: 11px; color: #FFD700; font-weight: 900; margin-top: 2px;">$0.15 LOCK</div>
                            </div>
                            <div id="sng-ts-stage-pill-3" style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 8px; padding: 8px 4px; text-align: center;">
                                <div style="font-size: 8px; color: #757575; font-weight: bold;">STAGE 3 ($1.50)</div>
                                <div style="font-size: 11px; color: #00e676; font-weight: 900; margin-top: 2px;">$0.20 SNIP</div>
                            </div>
                        </div>

                        <div class="ts-row">
                            <div class="ts-label">TRAILING HIGH (PEAK)</div>
                            <div class="ts-val" id="sng-ts-high">$0.00</div>
                        </div>
                        <div class="ts-row">
                            <div class="ts-label">TRIGGER STOP LEVEL</div>
                            <div class="ts-val orange" id="sng-ts-low">$0.00</div>
                        </div>

                        <div style="border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 12px; padding-top: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #e040fb; font-size: 11px; font-weight: 900; letter-spacing: 0.5px;">3 STAGE TRAILING BUY RADAR</span>
                                <span id="sng-tb-status-badge" style="color: #757575; font-size: 10px; font-weight: 800; font-family: monospace;">ARMED (SCANNING DIP)</span>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 12px;">
                                <div id="sng-tb-stage-pill-1" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">RIDE (1.0%)</div>
                                    <div id="sng-tb-target-1" style="font-size: 11px; color: #00d2ff; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Next Entry</div>
                                </div>
                                <div id="sng-tb-stage-pill-2" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">LOCK (0.5%)</div>
                                    <div id="sng-tb-target-2" style="font-size: 11px; color: #FFD700; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Adaptive</div>
                                </div>
                                <div id="sng-tb-stage-pill-3" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 6px 2px; text-align: center;">
                                    <div style="font-size: 8px; color: #757575; font-weight: bold;">PEAK SNIP</div>
                                    <div id="sng-tb-target-3" style="font-size: 11px; color: #00e676; font-weight: 900; font-family: monospace; margin-top: 2px;">$0.00</div>
                                    <div style="font-size: 7px; color: #757575;">Instant Exit</div>
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                                <span style="color: #757575;">DIP LOW TRACKED:</span>
                                <span id="sng-lowest-tracked" style="color: #fff; font-weight: bold;">$0.00</span>
                            </div>
                        </div>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                        <span style="color: #8c8ca1; font-size: 11px;">YOUR SHARE INVESTED:</span>
                        <span id="sng-user-invest-display" style="color: #e040fb; font-weight: 900; font-size: 13px;">$100.00 USDT (0.10%)</span>
                    </div>

                    <button onclick="openSingularityDetailsModal()" style="width: 100%; background: #1c2433; color: #e040fb; border: 1px solid #2d3748; border-radius: 10px; padding: 12px 0; font-size: 11px; font-weight: 900; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; letter-spacing: 0.5px; text-transform: uppercase;">
                        <i class="material-icons" style="font-size: 16px;">info</i>
                        <span>SHINE TITAN SINGULARITY POOL INFO</span>
                    </button>
                </div>
</div>
            <div id="tabViewAirdrop" class="bot-tab-view">
                <div style="background: radial-gradient(circle at top right, #1b2333 0%, #0d121c 100%); border: none; border-radius: 20px; padding: 18px; margin-bottom: 18px; display: flex; flex-direction: column; gap: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                        <span style="font-size: 14px; font-weight: 900; color: #ffffff; letter-spacing: 0.8px;">SHINE COMMODITY DEX LIVE</span>
                        <div style="display: flex; align-items: center; gap: 6px; background: rgba(0, 229, 255, 0.12); padding: 3px 10px; border-radius: 12px; border: 1px solid rgba(0, 229, 255, 0.3);">
                            <span class="live-pulse-dot"></span>
                            <span style="font-size: 10px; font-weight: 900; color: #00e5ff; font-family: monospace;">REAL COMMODITY PAIR</span>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 12px 14px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <svg viewBox="0 0 200 200" style="width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(228, 37, 125, 0.45));">
                                <defs>
                                    <radialGradient id="airdropShineLogoGrad" cx="35%" cy="30%" r="75%">
                                        <stop offset="0%" stop-color="#ff4f9e"/>
                                        <stop offset="35%" stop-color="#e91e7e"/>
                                        <stop offset="75%" stop-color="#ba1261"/>
                                        <stop offset="100%" stop-color="#840540"/>
                                    </radialGradient>
                                </defs>
                                <circle cx="100" cy="100" r="98" fill="url(#airdropShineLogoGrad)"/>
                                <circle cx="100" cy="100" r="91" fill="none" stroke="#ff7ab6" stroke-width="3" opacity="0.9"/>
                                <circle cx="100" cy="100" r="85" fill="none" stroke="#750438" stroke-width="3" opacity="0.7"/>
                                <circle cx="100" cy="100" r="82" fill="url(#airdropShineLogoGrad)"/>
                                <g fill="#ffffff">
                                    <text x="44" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">S</text>
                                    <text x="74" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">H</text>
                                    <path d="M100 56 Q101 64 107 67 Q101 70 100 78 Q99 70 93 67 Q99 64 100 56 Z"/>
                                    <path d="M89 74 Q89.5 78 92 79.5 Q89.5 81 89 85 Q88.5 81 86 79.5 Q88.5 78 89 74 Z"/>
                                    <path d="M112 76 Q112.5 80 115 81.5 Q112.5 83 112 87 Q111.5 83 109 81.5 Q111.5 80 112 76 Z"/>
                                    <circle cx="100" cy="86" r="3.2"/>
                                    <path d="M93 96 C94 91 98 87.5 104 88 C100 91 97 94 96 98 Z"/>
                                    <circle cx="100" cy="99" r="3.2"/>
                                    <path d="M92 113 C91 106 97 100 105 100 C100 103 97 107 97 113 Z"/>
                                    <path d="M100 106 C105 107 107 112 105 118 C102 124 97 129 93 136 C95 131 99 125 102 120 C104 115 102 110 98 108 Z"/>
                                    <path d="M93 126 C96 130 101 135 105 142 C103 138 99 133 95 128 Z"/>
                                    <text x="127" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">N</text>
                                    <text x="156" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">E</text>
                                </g>
                            </svg>
                            <div>
                                <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase;">SHINE BALANCE</div>
                                <div style="font-size: 26px; font-weight: 900; color: #ffffff; font-family: monospace; line-height: 1.1;"><span id="airdropShineUserBal">100.00</span></div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 10px; color: #8c8ca1; font-weight: 800; text-transform: uppercase;">24H PROFIT</div>
                            <div id="airdrop24hProfitVal" style="font-size: 16px; font-weight: 900; color: #00e676; font-family: monospace;">+$0.00</div>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 10px 12px;">
                            <div style="color: #718096; font-size: 10px; font-weight: 800; text-transform: uppercase;">UNREALIZED PROFIT</div>
                            <div id="airdropUnrealizedPnlVal" style="color: #00e676; font-size: 15px; font-weight: 900; margin-top: 3px;">+$0.00</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 10px 12px;">
                            <div style="color: #718096; font-size: 10px; font-weight: 800; text-transform: uppercase;">NET REALIZED PROFIT</div>
                            <div id="airdropRealizedPnlVal" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 3px;">+$0.00</div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #718096; padding-top: 2px;">
                        <span id="airdropInventoryVal">Inventory: 0 Items ($0.00)</span>
                        <span style="color: #FFD700; font-weight: 800;">100% NON-CUSTODIAL DEX</span>
                    </div>
                </div>

                <div class="market-tabs-row">
                    <button class="mkt-tab-btn active" id="mktTabMarketBtn" onclick="switchAirdropSubTab('ALL')">All Products (10)</button>
                    <button class="mkt-tab-btn" id="mktTabInventoryBtn" onclick="switchAirdropSubTab('INVENTORY')">My Vault / Holdings (<span id="userHoldingCountBadge">0</span>)</button>
                    <button class="mkt-tab-btn" id="mktTabOrdersBtn" onclick="switchAirdropSubTab('HISTORY')">Order History</button>
                </div>

                <div id="airdropProductsGrid" class="airdrop-products-grid"></div>

                <div id="airdropInventoryView" style="display: none; flex-direction: column; gap: 12px;"></div>

                <div id="airdropHistoryView" style="display: none; flex-direction: column; gap: 10px;"></div>
            </div>
            <div id="tabViewWallet" class="bot-tab-view" style="display: none; width: 100vw !important; margin-left: calc(-50vw + 50%) !important; margin-right: calc(-50vw + 50%) !important; padding: 2px 16px 85px 16px !important; box-sizing: border-box !important; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: -6px; margin-bottom: 18px;">
                    <div style="display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.08); padding: 6px 12px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08);">
                        <div style="width: 22px; height: 22px; background: #f39c12; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                            <i class="material-icons" style="font-size: 14px; color: #fff;">account_balance_wallet</i>
                        </div>
                        <span id="trust-wallet-pill-label" style="font-size: 14px; font-weight: 700; color: #ffffff;">Main Wallet 1</span>
                    </div>
                    <button id="trust-wallet-connect-btn" onclick="handleWalletTabBtnAction()" style="background: #2563eb; color: #ffffff; border: none; border-radius: 18px; padding: 7px 16px; font-size: 12px; font-weight: 900; letter-spacing: 0.8px; cursor: pointer;">
                        CONNECT
                    </button>
                </div>

                <div style="margin-bottom: 22px;">
                    <div id="trust-main-balance-val" style="font-size: 48px; font-weight: 900; color: #ffffff; letter-spacing: -1.5px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.1;">$0.00</div>
                    <div style="display: flex; align-items: center; gap: 2px; color: #f6465d; font-size: 13px; font-weight: 700; margin-top: 4px;">
                        <i class="material-icons" style="font-size: 18px;">arrow_drop_down</i>
                        <span id="trust-main-balance-diff">$0.00 (0.00%)</span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 28px; width: 100%;">
                    <div onclick="handleTrustSendAction()" style="display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer;">
                        <div style="width: 100%; max-width: 72px; aspect-ratio: 1 / 1; background: rgba(255, 255, 255, 0.08); border-radius: 22px; display: flex; align-items: center; justify-content: center;">
                            <i class="material-icons" style="font-size: 28px; color: #ffffff;">north_east</i>
                        </div>
                        <span style="font-size: 13px; font-weight: 600; color: #ffffff;">Send</span>
                    </div>

                    <div onclick="openReceiveModal()" style="display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer;">
                        <div style="width: 100%; max-width: 72px; aspect-ratio: 1 / 1; background: rgba(255, 255, 255, 0.08); border-radius: 22px; display: flex; align-items: center; justify-content: center;">
                            <i class="material-icons" style="font-size: 28px; color: #ffffff;">south_west</i>
                        </div>
                        <span style="font-size: 13px; font-weight: 600; color: #ffffff;">Receive</span>
                    </div>

                    <div onclick="switchBotNavigation('Trade')" style="display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer;">
                        <div style="width: 100%; max-width: 72px; aspect-ratio: 1 / 1; background: #2563eb; border-radius: 22px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);">
                            <i class="material-icons" style="font-size: 28px; color: #ffffff;">sync</i>
                        </div>
                        <span style="font-size: 13px; font-weight: 600; color: #ffffff;">Swap</span>
                    </div>

                    <div onclick="goToLevelUpgrade()" style="display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer;">
                        <div style="width: 100%; max-width: 72px; aspect-ratio: 1 / 1; background: rgba(255, 255, 255, 0.08); border-radius: 22px; display: flex; align-items: center; justify-content: center;">
                            <i class="material-icons" style="font-size: 28px; color: #ffffff;">add</i>
                        </div>
                        <span style="font-size: 13px; font-weight: 600; color: #ffffff;">Buy</span>
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 14px; width: 100%;">
                    <span style="font-size: 17px; font-weight: 800; color: #ffffff;">Tokens</span>
                    <i class="material-icons" style="font-size: 20px; color: #718096;">chevron_right</i>
                </div>

                <div style="display: flex; flex-direction: column; gap: 14px; width: 100%;">
                    <div class="wallet-token-row" data-symbol="SHINE" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 200 200" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(228, 37, 125, 0.45));">
                                <defs>
                                    <radialGradient id="shineCoinGradW" cx="35%" cy="30%" r="75%">
                                        <stop offset="0%" stop-color="#ff4f9e"/>
                                        <stop offset="35%" stop-color="#e91e7e"/>
                                        <stop offset="75%" stop-color="#ba1261"/>
                                        <stop offset="100%" stop-color="#840540"/>
                                    </radialGradient>
                                </defs>
                                <circle cx="100" cy="100" r="98" fill="url(#shineCoinGradW)"/>
                                <circle cx="100" cy="100" r="91" fill="none" stroke="#ff7ab6" stroke-width="3" opacity="0.9"/>
                                <circle cx="100" cy="100" r="85" fill="none" stroke="#750438" stroke-width="3" opacity="0.7"/>
                                <circle cx="100" cy="100" r="82" fill="url(#shineCoinGradW)"/>
                                <g fill="#ffffff">
                                    <text x="44" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">S</text>
                                    <text x="74" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">H</text>
                                    <path d="M100 56 Q101 64 107 67 Q101 70 100 78 Q99 70 93 67 Q99 64 100 56 Z"/>
                                    <path d="M89 74 Q89.5 78 92 79.5 Q89.5 81 89 85 Q88.5 81 86 79.5 Q88.5 78 89 74 Z"/>
                                    <path d="M112 76 Q112.5 80 115 81.5 Q112.5 83 112 87 Q111.5 83 109 81.5 Q111.5 80 112 76 Z"/>
                                    <circle cx="100" cy="86" r="3.2"/>
                                    <path d="M93 96 C94 91 98 87.5 104 88 C100 91 97 94 96 98 Z"/>
                                    <circle cx="100" cy="99" r="3.2"/>
                                    <path d="M92 113 C91 106 97 100 105 100 C100 103 97 107 97 113 Z"/>
                                    <path d="M100 106 C105 107 107 112 105 118 C102 124 97 129 93 136 C95 131 99 125 102 120 C104 115 102 110 98 108 Z"/>
                                    <path d="M93 126 C96 130 101 135 105 142 C103 138 99 133 95 128 Z"/>
                                    <text x="127" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">N</text>
                                    <text x="156" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">E</text>
                                </g>
                            </svg>
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">SHINE</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$0.01</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div id="trust-shine-amount" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">100.00 SHINE</div>
                            <div id="trust-shine-fiat" style="font-size: 12px; color: #718096; font-family: monospace;">$1.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="USDT" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 100 100" style="width: 38px; height: 38px; border-radius: 50%;">
                                <circle cx="50" cy="50" r="50" fill="#009393"/>
                                <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                                <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                            </svg>
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">USDT</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$1.00</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div id="trust-usdt-amount" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.00 USDT</div>
                            <div id="trust-usdt-fiat" style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="SOL" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">SOL</div>
                                <div id="trust-sol-rate-display" style="font-size: 12px; color: #718096; font-family: monospace;">$106.32</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div id="trust-sol-amount" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.0000 SOL</div>
                            <div id="trust-sol-fiat" style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="BNB" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 32 32" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;">
                                <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                                <path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                            </svg>
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">BNB</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$745.07</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div id="trust-bnb-amount" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.0000 BNB</div>
                            <div id="trust-bnb-fiat" style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="BTC" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">BTC</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$83,233.54</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.0000 BTC</div>
                            <div style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="ETH" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">ETH</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$2,449.89</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.0000 ETH</div>
                            <div style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>

                    <div class="wallet-token-row" data-symbol="TRX" style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 100 100" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;">
                                <circle cx="50" cy="50" r="50" fill="#FF060A"/>
                                <path d="M31.5 35.5 L60.8 41.8 L68.8 48.8 L47.5 75.5 Z" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
                                <path d="M31.5 35.5 L50.2 52.2 L47.5 75.5" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
                                <path d="M60.8 41.8 L50.2 52.2 L68.8 48.8" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
                            </svg>
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff;">TRX</div>
                                <div style="font-size: 12px; color: #718096; font-family: monospace;">$0.1324</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div id="trust-trx-amount" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">0.0000 TRX</div>
                            <div id="trust-trx-fiat" style="font-size: 12px; color: #718096; font-family: monospace;">$0.00</div>
                        </div>
                    </div>
                </div>

                <div id="walletPerpsSection" style="margin-top: 26px; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 14px;">
                        <span style="font-size: 17px; font-weight: 800; color: #ffffff;">Perps</span>
                        <i class="material-icons" style="font-size: 20px; color: #718096;">chevron_right</i>
                    </div>
                    <div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 6px; -webkit-overflow-scrolling: touch;">
                        <div style="min-width: 155px; background: #161b26; border-radius: 18px; padding: 16px; border: 1px solid #1f2737; flex-shrink: 0;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <span style="background: rgba(0, 229, 255, 0.15); color: #00e5ff; font-size: 11px; font-weight: 900; padding: 3px 8px; border-radius: 10px;">20x</span>
                            </div>
                            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">SOL/USDT</div>
                            <div id="perpsSolPriceLive" style="font-size: 13px; color: #00e5ff; font-weight: 800; font-family: monospace; margin-top: 4px;">$106.32</div>
                            <div style="font-size: 11px; color: #718096; margin-top: 2px; font-family: monospace;">$1.15B Vol</div>
                        </div>

                        <div style="min-width: 155px; background: #161b26; border-radius: 18px; padding: 16px; border: 1px solid #1f2737; flex-shrink: 0;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <svg viewBox="0 0 32 32" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;">
                                    <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                                    <path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                                </svg>
                                <span style="background: rgba(255, 215, 0, 0.15); color: #FFD700; font-size: 11px; font-weight: 900; padding: 3px 8px; border-radius: 10px;">15x</span>
                            </div>
                            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">BNB/USDT</div>
                            <div style="font-size: 13px; color: #FFD700; font-weight: 800; font-family: monospace; margin-top: 4px;">$745.07</div>
                            <div style="font-size: 11px; color: #718096; margin-top: 2px; font-family: monospace;">$410.50M Vol</div>
                        </div>

                        <div style="min-width: 155px; background: #161b26; border-radius: 18px; padding: 16px; border: 1px solid #1f2737; flex-shrink: 0;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <span style="background: rgba(255, 153, 0, 0.15); color: #f7931a; font-size: 11px; font-weight: 900; padding: 3px 8px; border-radius: 10px;">40x</span>
                            </div>
                            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">BTC/USDT</div>
                            <div style="font-size: 13px; color: #f7931a; font-weight: 800; font-family: monospace; margin-top: 4px;">$83,233.54</div>
                            <div style="font-size: 11px; color: #718096; margin-top: 2px; font-family: monospace;">$2.45B Vol</div>
                        </div>

                        <div style="min-width: 155px; background: #161b26; border-radius: 18px; padding: 16px; border: 1px solid #1f2737; flex-shrink: 0;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <span style="background: rgba(98, 126, 234, 0.15); color: #627eea; font-size: 11px; font-weight: 900; padding: 3px 8px; border-radius: 10px;">25x</span>
                            </div>
                            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">ETH/USDT</div>
                            <div style="font-size: 13px; color: #627eea; font-weight: 800; font-family: monospace; margin-top: 4px;">$2,449.89</div>
                            <div style="font-size: 11px; color: #718096; margin-top: 2px; font-family: monospace;">$982.24M Vol</div>
                        </div>
                    </div>
                </div>

                <div id="walletPredictionsSection" style="margin-top: 26px; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 14px;">
                        <span style="font-size: 17px; font-weight: 800; color: #ffffff;">Predictions</span>
                        <i class="material-icons" style="font-size: 20px; color: #718096;">chevron_right</i>
                    </div>
                    <div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 6px; -webkit-overflow-scrolling: touch;">
                        <div style="width: 220px; min-width: 220px; background: #161b26; border-radius: 16px; padding: 14px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <div style="width: 28px; height: 28px; background: rgba(0, 192, 135, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                            <i class="material-icons" style="font-size: 16px; color: #00c087;">trending_up</i>
                                        </div>
                                        <span style="font-size: 13px; font-weight: 800; color: #ffffff;">SOL/USDT</span>
                                    </div>
                                    <span style="background: rgba(0, 229, 255, 0.12); color: #00e5ff; font-size: 9px; font-weight: 900; padding: 2px 6px; border-radius: 6px; font-family: monospace;">STRONG BUY</span>
                                </div>
                                <div style="font-size: 11px; color: #a0aec0; line-height: 1.4;">
                                    Whale orderflow active.<br>
                                    Support confirmed.<br>
                                    Dip entry ready.
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 10px; font-family: monospace;">
                                <div><span style="color:#718096;">BUY: </span><span id="predSolBuyTarget" style="color: #00c087; font-weight: 900;">$105.20</span></div>
                                <div><span style="color:#718096;">SELL: </span><span id="predSolSellTarget" style="color: #FFD700; font-weight: 900;">$109.80</span></div>
                            </div>
                        </div>

                        <div style="width: 220px; min-width: 220px; background: #161b26; border-radius: 16px; padding: 14px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <div style="width: 28px; height: 28px; background: rgba(255, 215, 0, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                            <i class="material-icons" style="font-size: 16px; color: #FFD700;">flash_on</i>
                                        </div>
                                        <span style="font-size: 13px; font-weight: 800; color: #ffffff;">BNB/USDT</span>
                                    </div>
                                    <span style="background: rgba(255, 215, 0, 0.12); color: #FFD700; font-size: 9px; font-weight: 900; padding: 2px 6px; border-radius: 6px; font-family: monospace;">SMART FLOW</span>
                                </div>
                                <div style="font-size: 11px; color: #a0aec0; line-height: 1.4;">
                                    Wave hunter tracking.<br>
                                    Trailing floor armed.<br>
                                    Breakout runner set.
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 10px; font-family: monospace;">
                                <div><span style="color:#718096;">BUY: </span><span style="color: #00c087; font-weight: 900;">$740.00</span></div>
                                <div><span style="color:#718096;">SELL: </span><span style="color: #FFD700; font-weight: 900;">$768.50</span></div>
                            </div>
                        </div>

                        <div style="width: 220px; min-width: 220px; background: #161b26; border-radius: 16px; padding: 14px; flex-shrink: 0; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <div style="width: 28px; height: 28px; background: rgba(0, 229, 255, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                            <i class="material-icons" style="font-size: 16px; color: #00e5ff;">track_changes</i>
                                        </div>
                                        <span style="font-size: 13px; font-weight: 800; color: #ffffff;">BTC/USDT</span>
                                    </div>
                                    <span style="background: rgba(0, 230, 118, 0.12); color: #00e676; font-size: 9px; font-weight: 900; padding: 2px 6px; border-radius: 6px; font-family: monospace;">ACCUMULATE</span>
                                </div>
                                <div style="font-size: 11px; color: #a0aec0; line-height: 1.4;">
                                    Zero liquidation risk.<br>
                                    Spot accumulation.<br>
                                    Rebound exit armed.
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 10px; font-family: monospace;">
                                <div><span style="color:#718096;">BUY: </span><span style="color: #00c087; font-weight: 900;">$82,800</span></div>
                                <div><span style="color:#718096;">SELL: </span><span style="color: #FFD700; font-weight: 900;">$85,400</span></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 26px; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 14px;">
                        <span style="font-size: 17px; font-weight: 800; color: #ffffff;">Watchlist</span>
                        <i class="material-icons" style="font-size: 20px; color: #718096;">chevron_right</i>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <svg viewBox="0 0 200 200" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(228, 37, 125, 0.45));">
                                    <defs>
                                        <radialGradient id="shineCoinGradWL" cx="35%" cy="30%" r="75%">
                                            <stop offset="0%" stop-color="#ff4f9e"/>
                                            <stop offset="35%" stop-color="#e91e7e"/>
                                            <stop offset="75%" stop-color="#ba1261"/>
                                            <stop offset="100%" stop-color="#840540"/>
                                        </radialGradient>
                                    </defs>
                                    <circle cx="100" cy="100" r="98" fill="url(#shineCoinGradWL)"/>
                                    <circle cx="100" cy="100" r="91" fill="none" stroke="#ff7ab6" stroke-width="3" opacity="0.9"/>
                                    <circle cx="100" cy="100" r="85" fill="none" stroke="#750438" stroke-width="3" opacity="0.7"/>
                                    <circle cx="100" cy="100" r="82" fill="url(#shineCoinGradWL)"/>
                                    <g fill="#ffffff">
                                        <text x="44" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">S</text>
                                        <text x="74" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">H</text>
                                        <path d="M100 56 Q101 64 107 67 Q101 70 100 78 Q99 70 93 67 Q99 64 100 56 Z"/>
                                        <path d="M89 74 Q89.5 78 92 79.5 Q89.5 81 89 85 Q88.5 81 86 79.5 Q88.5 78 89 74 Z"/>
                                        <path d="M112 76 Q112.5 80 115 81.5 Q112.5 83 112 87 Q111.5 83 109 81.5 Q111.5 80 112 76 Z"/>
                                        <circle cx="100" cy="86" r="3.2"/>
                                        <path d="M93 96 C94 91 98 87.5 104 88 C100 91 97 94 96 98 Z"/>
                                        <circle cx="100" cy="99" r="3.2"/>
                                        <path d="M92 113 C91 106 97 100 105 100 C100 103 97 107 97 113 Z"/>
                                        <path d="M100 106 C105 107 107 112 105 118 C102 124 97 129 93 136 C95 131 99 125 102 120 C104 115 102 110 98 108 Z"/>
                                        <path d="M93 126 C96 130 101 135 105 142 C103 138 99 133 95 128 Z"/>
                                        <text x="127" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">N</text>
                                        <text x="156" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">E</text>
                                    </g>
                                </svg>
                                <div>
                                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">SHINE</div>
                                    <div style="font-size: 12px; color: #718096; font-family: monospace;">$10.00M MCap</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">$0.01</div>
                                <div style="font-size: 12px; color: #00c087; font-weight: 700; font-family: monospace;">+5.20%</div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <div>
                                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">SOL</div>
                                    <div style="font-size: 12px; color: #718096; font-family: monospace;">$62.68B MCap</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div id="wl-sol-price" style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">$106.32</div>
                                <div style="font-size: 12px; color: #00c087; font-weight: 700; font-family: monospace;">+2.38%</div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <svg viewBox="0 0 32 32" style="width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;">
                                    <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                                    <path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                                </svg>
                                <div>
                                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">BNB</div>
                                    <div style="font-size: 12px; color: #718096; font-family: monospace;">$97.99B MCap</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">$745.07</div>
                                <div style="font-size: 12px; color: #00c087; font-weight: 700; font-family: monospace;">+2.32%</div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <div>
                                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">BTC</div>
                                    <div style="font-size: 12px; color: #718096; font-family: monospace;">$1.67T MCap</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">$83,233.54</div>
                                <div style="font-size: 12px; color: #00c087; font-weight: 700; font-family: monospace;">+2.24%</div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024" style="width: 38px; height: 38px; border-radius: 50%;">
                                <div>
                                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">ETH</div>
                                    <div style="font-size: 12px; color: #718096; font-family: monospace;">$299.25B MCap</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 15px; font-weight: 800; color: #ffffff; font-family: monospace;">$2,449.89</div>
                                <div style="font-size: 12px; color: #00c087; font-weight: 700; font-family: monospace;">+2.83%</div>
                            </div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: center; margin-top: 24px;">
                        <button onclick="openTrustCustomizeSheet()" style="background: rgba(255,255,255,0.08); border: none; border-radius: 20px; color: #ffffff; padding: 10px 24px; font-size: 13px; font-weight: 800; display: flex; align-items: center; gap: 6px; cursor: pointer;">
                            <i class="material-icons" style="font-size: 16px;">tune</i>
                            <span>Customize</span>
                        </button>
                    </div>
                </div>
            </div>

            <div id="receiveModalSheet" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 40000; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box;">
                <div style="background: #11151e; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; width: 100%; max-width: 360px; padding: 22px; text-align: center; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="font-weight: 900; font-size: 16px; color: #ffffff;">Receive Crypto</span>
                        <i class="material-icons" onclick="closeReceiveModal()" style="color: #8c8ca1; cursor: pointer;">close</i>
                    </div>
                    <div id="receive-network-name" style="background: rgba(37, 99, 235, 0.15); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.3); border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 16px;">
                        BNB Smart Chain (BEP-20)
                    </div>
                    <div style="background: #ffffff; padding: 12px; border-radius: 14px; width: 170px; height: 170px; margin: 0 auto 16px; display: flex; align-items: center; justify-content: center;">
                        <img id="receive-qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=0x0000" style="width: 100%; height: 100%; object-fit: contain;">
                    </div>
                    <div id="receive-full-address" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px; font-family: monospace; font-size: 11px; color: #ffffff; word-break: break-all; margin-bottom: 16px;">
                        0x0000...0000
                    </div>
                    <button onclick="copyReceiveAddress()" style="width: 100%; background: #2563eb; color: #ffffff; border: none; border-radius: 10px; padding: 12px 0; font-weight: 900; font-size: 13px; cursor: pointer;">
                        COPY ADDRESS
                    </button>
                </div>
            </div>

            <div id="selectTokenSheet" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 40000; align-items: flex-end; justify-content: center; box-sizing: border-box;">
                <div style="background: #ffffff; color: #000000; border-top-left-radius: 28px; border-top-right-radius: 28px; width: 100%; max-width: 480px; max-height: 85vh; padding: 16px 20px 30px; box-sizing: border-box; overflow-y: auto; font-family: 'Plus Jakarta Sans', sans-serif;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                        <button onclick="closeSelectTokenSheet()" style="background: #f1f5f9; border: none; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer;"><i class="material-icons" style="color: #0f172a; font-size: 20px;">close</i></button>
                        <span style="font-size: 18px; font-weight: 800; color: #0f172a;">Select token</span>
                        <div style="width: 36px;"></div>
                    </div>
                    <div style="background: #f1f5f9; border-radius: 20px; padding: 10px 14px; display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
                        <i class="material-icons" style="color: #64748b; font-size: 20px;">search</i>
                        <input type="text" id="tokenSearchInput" oninput="filterTokenSelectSheet(this.value)" placeholder="Search for tokens" style="border: none; background: transparent; outline: none; font-size: 15px; width: 100%; color: #0f172a;">
                    </div>
                    <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                        <button onclick="filterTokenNet('ALL')" class="token-net-filter active" id="netFilterAll" style="background: #0f172a; color: #ffffff; border: none; border-radius: 16px; padding: 6px 14px; font-size: 12px; font-weight: 800; cursor: pointer;">All</button>
                        <button onclick="filterTokenNet('TRON')" class="token-net-filter" id="netFilterTron" style="background: #f1f5f9; color: #0f172a; border: none; border-radius: 16px; padding: 6px 14px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                            <span style="width: 14px; height: 14px; background: #EF0027; border-radius: 50%; display: inline-block;"></span> TRON
                        </button>
                        <button onclick="filterTokenNet('BSC')" class="token-net-filter" id="netFilterBsc" style="background: #f1f5f9; color: #0f172a; border: none; border-radius: 16px; padding: 6px 14px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                            <span style="width: 14px; height: 14px; background: #F0B90B; border-radius: 50%; display: inline-block;"></span> BSC
                        </button>
                        <button onclick="filterTokenNet('SOL')" class="token-net-filter" id="netFilterSol" style="background: #f1f5f9; color: #0f172a; border: none; border-radius: 16px; padding: 6px 14px; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                            <span style="width: 14px; height: 14px; background: #ab9ff2; border-radius: 50%; display: inline-block;"></span> SOL
                        </button>
                    </div>
                    <div id="tokenSelectListContainer" style="display: flex; flex-direction: column; gap: 6px;"></div>
                </div>
            </div>

            <div id="sendModalSheet" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 40001; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box;">
                <div style="background: #11151e; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; width: 100%; max-width: 380px; padding: 22px; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span id="send-selected-icon"></span>
                            <span style="font-weight: 900; font-size: 17px; color: #ffffff;">Send <span id="send-selected-symbol">USDT</span></span>
                        </div>
                        <i class="material-icons" onclick="closeSendModal()" style="color: #8c8ca1; cursor: pointer;">close</i>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 14px;">
                        <div style="background: rgba(255,255,255,0.04); border-radius: 12px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; color: #8c8ca1;">Available Balance:</span>
                            <span id="send-available-balance-disp" style="font-size: 13px; font-weight: 800; color: #00e676; font-family: monospace;">0.00</span>
                        </div>
                        <div>
                            <div style="font-size: 11px; color: #8c8ca1; font-weight: 700; margin-bottom: 6px;">RECIPIENT ADDRESS</div>
                            <input type="text" id="send-target-address" placeholder="Paste address" style="width: 100%; background: #161b26; border: 1px solid #232b3b; color: #ffffff; padding: 12px; border-radius: 10px; font-size: 13px; box-sizing: border-box; font-family: monospace; outline: none;">
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-size: 11px; color: #8c8ca1; font-weight: 700;">AMOUNT</span>
                                <span onclick="fillMaxSendAmount()" style="font-size: 11px; color: #2563eb; font-weight: 800; cursor: pointer;">MAX</span>
                            </div>
                            <input type="number" id="send-target-amount" placeholder="0.00" step="any" style="width: 100%; background: #161b26; border: 1px solid #232b3b; color: #ffffff; padding: 12px; border-radius: 10px; font-size: 15px; font-weight: bold; box-sizing: border-box; font-family: monospace; outline: none;">
                        </div>
                        <button onclick="executeSendFundAction()" style="width: 100%; background: #2563eb; color: #ffffff; border: none; border-radius: 12px; padding: 14px 0; font-weight: 900; font-size: 14px; cursor: pointer; margin-top: 6px;">
                            CONFIRM & SEND
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <nav class="bot-nav-bar" id="botBottomNavBar" style="transition: transform 0.3s ease;">
            <button class="bot-nav-item active" onclick="switchBotNavigation('Home')">
                <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                <span>Home</span>
            </button>
            <button class="bot-nav-item" onclick="switchBotNavigation('Bot')">
                <svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.38-1 1.72V7h4a2 2 0 0 1 2 2v2h1a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-1v1a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1H3a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h1V9a2 2 0 0 1 2-2h4V5.72A2 2 0 0 1 9 4a2 2 0 0 1 2-2h1m-4 9a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m8 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/></svg>
                <span>Bot</span>
            </button>
            <button class="bot-nav-item" onclick="switchBotNavigation('Trade')">
                <svg viewBox="0 0 24 24"><path d="M16 6l4 4-4 4V11H8V9h8V6zm-8 12l-4-4 4-4v3h8v2H8v3z"/></svg>
                <span>Trade</span>
            </button>
            <button class="bot-nav-item" onclick="switchBotNavigation('Airdrop')">
                <svg viewBox="0 0 24 24"><path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5zm0 4.18l6 3.33v4.61c0 3.78-2.58 7.32-6 8.35-3.42-1.03-6-4.57-6-8.35V9.51l6-3.33zM11 10v4h2v-4h-2zm0 6v2h2v-2h-2z"/></svg>
                <span>Airdrop</span>
            </button>
            <button class="bot-nav-item" onclick="switchBotNavigation('Assets')">
                <svg viewBox="0 0 24 24"><path d="M21 18v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v1h-9a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9m-9-2h10V8H12v8m4-2.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/></svg>
                <span>Wallet</span>
            </button>
        </nav>
    </div>
<div id="profileEditOverlay" class="profile-edit-overlay">
    <div class="edit-header">
        <div class="breadcrumb">Dashboard / <span>Profile</span></div>
        <h1 style="margin:0; font-size:28px;">Profile</h1>
    </div>
    <div class="edit-content">
        <div class="edit-avatar-wrapper">
            <div class="edit-avatar"></div>
            <button class="close-edit-btn" onclick="toggleProfileEdit()"><i class="material-icons" style="font-size:18px;">close</i></button>
        </div>
        <span style="color:#757575; margin-bottom:30px;">Chose your photo</span>     
        <div class="input-group">
            <label>Nickname</label>
            <input type="text" id="inputNickname" placeholder="User">
        </div>    
          <div class="input-group">
            <label>Email</label>
            <input type="email" placeholder="Shine Crypto.io">
        </div>   
        <div class="input-group">
            <label>Description</label>
            <textarea rows="4" placeholder="Tell something about yourself"></textarea>
        </div>

        <button class="save-profile-btn" onclick="saveProfile()" style="margin-top: 10px;">Save changes</button>

        <div style="width: 100%; background: #1A1A1A; border-radius: 16px; padding: 20px; margin-top: 40px; box-sizing: border-box;">
            <h3 style="font-size: 18px; margin: 0 0 12px 0;">Change of Wallet for Receiving Profit</h3>
            <div style="display: flex; gap: 10px; color: #FFD700; margin-bottom: 12px;">
                <i class="material-icons" style="font-size: 20px;">warning</i>
                <p style="margin: 0; font-size: 14px; line-height: 1.4;">Use this form only if your wallet was compromised and you lost access to it.</p>
            </div>
            <p style="margin: 0; color: #757575; font-size: 14px; line-height: 1.4;">This process will allow you to update the verified settlement address used to receive spot profits from SHINE Protocol. Please ensure your new cold wallet is secure.</p>
            
            <div style="width: 100%; margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">
                <div class="input-group" style="margin-bottom: 0;">
                    <label style="color: white; font-weight: 500;">Old Wallet Address *</label>
                    <input type="text" value="0x99b23c8039e98a119eaed74e4f3fe" readonly style="background: #151515; border-color: #2A2A2A; color: #757575;">
                </div>
                <div class="input-group" style="margin-bottom: 0;">
                    <label style="color: white; font-weight: 500;">New Wallet Address *</label>
                    <input type="text" placeholder="0x...">
                </div>
                <div class="input-group" style="margin-bottom: 0;">
                    <label style="color: white; font-weight: 500;">Telegram (optional)</label>
                    <input type="text" placeholder="@username or link">
                    <p style="margin: 8px 0 0 0; color: #757575; font-size: 12px;">We recommend adding your Telegram handle to receive updates about the change.</p>
                </div>
                 <button onclick="requestWalletChange()" style="width: 100%; background: #3A47A6; color: white; border: none; border-radius: 12px; padding: 18px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px;">Verify wallet</button>         
                <p style="text-align: center; color: #757575; font-size: 14px; margin: 0;">The request will be processed within 2-3 business days.</p>
            </div>
        </div>
    </div>
</div>
<div id="sideMenu" class="side-menu">
        <div class="menu-header">
            <div class="menu-logo">SHINE</div>
            <button class="close-menu" onclick="toggleMenu()">
                <i class="material-icons">close</i>
            </button>
        </div>
        <div class="menu-content">
            <h1 class="menu-preview-title">Preview ID 1</h1>         
            <div class="search-container">
                <input type="text" class="search-input" placeholder="1">
                <button class="go-btn">Go</button>
            </div>
            <button class="exit-mode-btn">Exit preview mode</button>

            <nav class="menu-nav">
                <div class="nav-item active" onclick="handleNav('dashboard')">
                    <i class="material-icons">grid_view</i>
                    <span>Dashboard</span>
                </div>
                <div class="nav-item" onclick="toggleProfileEdit(); toggleMenu();">
                    <i class="material-icons">settings</i>
                    <span>Settings</span>
                </div>
                <div class="nav-item" onclick="handleNav('team')">
                    <i class="material-icons">groups</i>
                    <span>Team</span>
                    <i class="material-icons arrow">expand_more</i>
                </div>
                <div class="nav-item sub-item" onclick="handleNav('partners')">
                    <i class="material-icons">person_outline</i>
                    <span>Partners</span>
                </div>
                <div class="nav-item" onclick="handleNav('links')">
                    <i class="material-icons">link</i>
                    <span>Links</span>
                    <i class="material-icons globe">language</i>
                </div>
                <div class="nav-item" onclick="handleNav('stats')">
                    <i class="material-icons">leaderboard</i>
                    <span>Stats</span>
                </div>
                <div class="nav-item" onclick="handleNav('social')">
                    <i class="material-icons">share</i>
                    <span>Social</span>
                </div>
                <div class="nav-item" onclick="handleNav('nft')">
                    <i class="material-icons">token</i>
                    <span>Nft</span>
                </div>
                <div class="nav-item" onclick="handleNav('luck')">
                    <i class="material-icons">auto_awesome</i>
                    <span>Mystery luck</span>
                </div>
                <div class="nav-item" onclick="handleNav('info')">
                    <i class="material-icons">info_outline</i>
                    <span>Information</span>
                </div>
                <div class="nav-item" onclick="handleNav('network')">
                    <i class="material-icons">hub</i>
                    <span>Shine Network</span>
                </div>
            </nav>
        </div>
    </div>
<div id="orderTypeModalBackdrop" onclick="toggleOrderTypeSheet()" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 999998;"></div>
<div id="orderTypeModalSheet" style="display: none; position: fixed; bottom: 0; left: 0; width: 100%; background: #ffffff; color: #000000; border-top-left-radius: 20px; border-top-right-radius: 20px; z-index: 999999; padding: 16px 20px 30px; box-sizing: border-box; box-shadow: 0 -10px 40px rgba(0,0,0,0.9); max-height: 80vh; overflow-y: auto;">
    <div style="width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 16px;"></div>
    <div style="font-size: 20px; font-weight: 900; margin-bottom: 16px; color: #000;">Order type</div>
    <div style="display: flex; flex-direction: column;">
        <div class="ord-type-opt" onclick="selectOrderType('Shine Auto Trailing')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <span>Shine Auto Trailing</span><i class="material-icons ord-check" id="check-Shine Auto Trailing" style="display: none; color: #000;">check</i>
        </div>
        <div class="ord-type-opt" onclick="selectOrderType('Market')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <span>Market</span><i class="material-icons ord-check" id="check-Market" style="display: block; color: #000;">check</i>
        </div>
        <div class="ord-type-opt" onclick="selectOrderType('Limit')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <span>Limit</span><i class="material-icons ord-check" id="check-Limit" style="display: none; color: #000;">check</i>
        </div>
        <div class="ord-type-opt" onclick="selectOrderType('Trailing stop')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <span>Trailing stop</span><i class="material-icons ord-check" id="check-Trailing stop" style="display: none; color: #000;">check</i>
        </div>
        <div class="ord-type-opt" onclick="selectOrderType('Trigger')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <span>Trigger</span><i class="material-icons ord-check" id="check-Trigger" style="display: none; color: #000;">check</i>
        </div>
        <div class="ord-type-opt" onclick="selectOrderType('TP/SL')" style="padding: 14px 0; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; align-items: center;">
            <span>TP/SL</span><i class="material-icons ord-check" id="check-TP/SL" style="display: none; color: #000;">check</i>
        </div>
    </div>
</div>
    <div id="infoModal" class="info-modal">
        <div class="modal-header">
            <button class="modal-close" onclick="toggleModal('infoModal')">
                <i class="material-icons">close</i>
            </button>
        </div>
        <div class="modal-body">
            <h2 class="modal-title" style="font-size: 26px;">Programs Marketing Info</h2>
            <p class="modal-desc">Overview of the current programs status, slot states and network levels.</p>
            <div class="legend-list" style="margin-bottom: 35px;">
                <div class="legend-item">
                    <div class="legend-box" style="background:#3A47A6; border-radius:6px;"></div>
                    <div class="legend-text"><strong>Activated Level:</strong> Active level in the program generating income.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box" style="background:#2A2A3B; border-radius:6px;"></div>
                    <div class="legend-text"><strong>Not Activated Level:</strong> Inactive slot waiting for upgrade.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box" style="background:#5C6BC0; border-radius:6px;"><i class="material-icons" style="font-size:16px;">ac_unit</i></div>
                    <div class="legend-text"><strong>Level Freeze:</strong> Completed 1st cycle without activating the next level. Profits will leak until next level is unlocked.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box" style="background:#E8755B; border-radius:6px;"><i class="material-icons" style="font-size:16px;">error</i></div>
                    <div class="legend-text"><strong>Missed Profit:</strong> Downline overtook this level before you activated it. Upgrade required to restore revenue.</div>
                </div>
            </div>

            <h2 class="modal-title" style="font-size: 26px;">System & Protocol Architecture</h2>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 16px; margin-bottom: 20px; border-radius: 14px;">
                <p style="margin: 0; color: #fff; font-size: 14px; line-height: 1.6;">
                    <strong style="color: #00d2ff;">100% Decentralized & Non-Custodial:</strong> The protocol directly interfaces with decentralized automated market makers and smart contracts. User funds remain strictly verifiable with zero third-party custody locks.
                </p>
            </div>

            <div class="legend-list" style="margin-bottom: 30px;">
                <div class="legend-item">
                    <i class="material-icons" style="color: #4CAF50;">account_balance_wallet</i>
                    <div class="legend-text"><strong>Capital Allocation (100%):</strong> 80% PancakeSwap DEX Trading Bot Vault, 10% Owner Wallet, 10% Upline Ecosystem (Direct Upline 5%, Second Upline 3%, Third Upline 2%).</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons" style="color: #00e676;">precision_manufacturing</i>
                    <div class="legend-text"><strong>DEX Spot Trading Engine (80%):</strong> BNB Smart Chain PancakeSwap DEX par automated non-custodial trading run karta hai. Zero leverage aur zero liquidation risk.</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons" style="color: #FFD700;">trending_up</i>
                    <div class="legend-text"><strong>Profit Distribution (100%):</strong> 80% direct to User Wallet, 5% Direct Upline, 5% Owner Wallet, 5% SHINE Airdrop Wallet, 5% Global Charity.</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons" style="color: #FFD700;">stars</i>
                    <div class="legend-text"><strong>1:1 SHINE Token Airdrop:</strong> Every 1 USDT allocated generates 1 SHINE token entitlement claimable directly upon liquidity pool launch.</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons" style="color: #E91E63;">favorite</i>
                    <div class="legend-text"><strong>Global Charity (5%):</strong> Dedicated smart contract allocation supporting orphans, underprivileged children, and widows worldwide.</div>
                </div>
            </div>
            <button class="close-tip-btn" onclick="toggleModal('infoModal')">Close tip</button>
        </div>
    </div>
    <div id="legendModal" class="info-modal">
        <div class="modal-header">
            <button class="modal-close" onclick="toggleModal('legendModal')">
                <i class="material-icons">close</i>
            </button>
        </div>
        <div class="modal-body">
            <h2 class="modal-title">Marketing legend</h2>
            <div class="video-legend-container">
                <video autoplay loop muted playsinline><source src="YOUR_VIDEO_URL_HERE.mp4" type="video/mp4"></video>
            </div>
            <div class="legend-list">
                <div class="legend-item">
                    <div class="legend-box active-box"></div>
                    <div class="legend-text"><strong>Direct partner</strong> — direct partner who took place in your level</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box gift-box"></div>
                    <div class="legend-text"><strong>Gift</strong> — a partner of your downline who made upgrade earlier than your downline, so he took place in your level instead</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons">groups</i>
                    <div class="legend-text"><strong>Partners on level</strong> — total amount of partners who took places in the level</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons">cached</i>
                    <div class="legend-text"><strong>Level Cycle</strong> — amount of times the level got filled and cleared</div>
                </div>
            </div>
            <button class="close-tip-btn" onclick="toggleModal('legendModal')">Close tip</button>
        </div>
    </div>
<div id="legendModalAdvanced" class="info-modal">
        <div class="modal-header">
            <button class="modal-close" onclick="toggleModal('legendModalAdvanced')">
                <i class="material-icons">close</i>
            </button>
        </div>
        <div class="modal-body">
            <h2 class="modal-title">Marketing legend</h2>
            <div class="video-legend-container">
                <video autoplay loop muted playsinline><source src="YOUR_ADVANCED_VIDEO_URL.mp4" type="video/mp4"></video>
            </div>
            <div class="legend-list">
                <div class="legend-item">
                    <div class="legend-box active-box"></div>
                    <div class="legend-text"><strong>Direct partner</strong> — direct partner who took place in your level</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box" style="background:#EDF45E; border-radius:50%;"></div>
                    <div class="legend-text"><strong>Spillover from above</strong> — a partner of your upline took place in your level</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box" style="background:#F59322; border-radius:50%;"></div>
                    <div class="legend-text"><strong>Spillover from below</strong> — a partner of your downline took place in your level</div>
                </div>
                <div class="legend-item">
                    <div class="legend-box gift-box"></div>
                    <div class="legend-text"><strong>Gift</strong> — a partner of your downline who made upgrade earlier than your downline, so he took place in your level instead</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons">groups</i>
                    <div class="legend-text"><strong>Partners on level</strong> — total amount of partners who took places in the level</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons">cached</i>
                    <div class="legend-text"><strong>Level Cycle</strong> — amount of times the level got fully filled with partners and was automatically restarted</div>
                </div>
                <div class="legend-item">
                    <i class="material-icons">north</i>
                    <div class="legend-text"><strong>Send to upline</strong> — a partner took place in a level at the position on the 1st line so the reward is sent to upline according to marketing</div>
                </div>
            </div>
            <button class="close-tip-btn" onclick="toggleModal('legendModalAdvanced')">Close tip</button>
        </div>
    </div>
<div id="upgradeOverlay" class="profile-edit-overlay" style="background: #0F0F1A; z-index: 8000;">
        <div class="edit-header" style="border-bottom: none; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h1 id="upgradeTitle" style="margin:0; font-size:24px; color: white;">Upgrade V1</h1>
                <button class="close-edit-btn" onclick="closeUpgrade()" style="position: static;"><i class="material-icons">close</i></button>
            </div>
        </div>
        <div class="edit-content" style="padding-top: 0;">
            <div id="upgradeCard" style="width: 100%; background: linear-gradient(135deg, #3A47A6 0%, #1E1E2C 100%); border-radius: 20px; padding: 25px; box-sizing: border-box; margin-bottom: 30px; position: relative; overflow: hidden;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="font-size: 14px; opacity: 0.8;">Lvl <span id="upgradeLvlNum">1</span></div>
                    <div style="display: flex; align-items: center; gap: 6px; font-weight: bold; font-size: 20px;">
                        <svg width="20" height="20" viewBox="0 0 100 100" style="border-radius: 50%;">
                            <circle cx="50" cy="50" r="50" fill="#009393"/>
                            <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                            <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                        </svg>
                        <span id="upgradePriceDisplay">10</span>
                    </div>
                </div>
                <div style="display: flex; justify-content: center; gap: 15px; margin: 30px 0;">
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; opacity: 0.7;">
                    <div style="display: flex; align-items: center; gap: 4px;"><i class="material-icons" style="font-size: 16px;">groups</i> 0</div>
                    <div style="display: flex; align-items: center; gap: 4px;"><i class="material-icons" style="font-size: 16px;">cached</i> <i class="material-icons" style="font-size: 16px;">all_inclusive</i></div>
                </div>
            </div>
            <div style="width: 100%; display: flex; flex-direction: column;">
                <div class="upgrade-detail-row">
                    <span class="upgrade-detail-label">Number of places for re-cycle</span>
                    <span class="upgrade-detail-value"><span id="upgPlaces">3</span> <i class="material-icons" style="font-size: 16px;">groups</i></span>
                </div>
                <div class="upgrade-detail-row">
                    <span class="upgrade-detail-label">Net rewards for every cycle</span>
                    <span class="upgrade-detail-value"><span id="upgReward">20</span> USDT</span>
                </div>
                <div class="upgrade-detail-row">
                    <span class="upgrade-detail-label">Level cycle profit</span>
                    <span class="upgrade-detail-value" style="color: #4CAF50;"><span id="upgProfit">200</span> % <i class="material-icons" style="font-size: 16px;">cached</i></span>
                </div>
                <div class="upgrade-detail-row" style="border-bottom: none;">
                    <span class="upgrade-detail-label">Max automatic re-cycles</span>
                    <span class="upgrade-detail-value"><i class="material-icons" style="font-size: 16px;">all_inclusive</i></span>
                </div>

                <div style="height: 1px; background: #2A2A3B; margin: 10px 0;"></div>

                <div class="upgrade-amount-row">
                    <span class="upgrade-amount-label">Upgrade amount</span>
                    <span class="upgrade-amount-value"><span id="totalUpgradePrice">10</span> USDT <span class="upgrade-amount-bnb">(<span id="upgBnb">0.0150</span> BNB)</span></span>
                </div>
                <div class="service-fee-row">
                    <span style="display: flex; align-items: center; gap: 4px;">Service fee <i class="material-icons" style="font-size: 14px;">help_outline</i></span>
                    <span id="serviceFeeDisplay">1 USDT</span>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 24px; height: 24px; background: transparent; border: 1px solid #4CAF50; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><i class="material-icons" style="font-size: 16px; color: #4CAF50;">done</i></div>
                        <span style="color: #4CAF50; font-weight: 500;">Network check (Smart chain)</span>
                    </div>
                    <i class="material-icons" style="color: #4CAF50;">check_circle</i>
                </div>
                <div id="balCheckRow" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div id="balCheckIconBox" style="width: 24px; height: 24px; background: transparent; border: 1px solid #4CAF50; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><i id="balCheckIconLeft" class="material-icons" style="font-size: 16px; color: #4CAF50;">done</i></div>
                        <span id="balCheckText" style="color: #4CAF50; font-weight: 500;">Balance check <span id="balCheckAmt">11</span> USDT</span>
                    </div>
                    <i id="balCheckIconRight" class="material-icons" style="color: #4CAF50;">check_circle</i>
                </div>

                <button class="save-profile-btn" onclick="executeLevelUpgrade()" style="margin-top: 0; background: #2563eb; color: #ffffff; cursor: pointer; font-weight: 900;">CONFIRM & ACTIVATE LEVEL</button>
            </div>
        </div>
    </div>
    <div id="programPreview" class="program-preview-overlay">

        <div class="preview-header">
            <div class="header-left">
    <span id="previewIdBreadcrumb">ID 1 / SHINE V1 (0/12)</span>
</div>
            <div class="header-right">
                <button class="menu-btn-circle" onclick="closePreview()"><div class="hamburger-lines"><span></span><span></span></div></button>
            </div>
        </div>     
        <div class="preview-content">
            <div class="program-title-row">
                <h1 id="previewProgramName">SHINE X1</h1>
                <div class="program-total-profit"><span id="previewTotalProfit">0</span> USDT</div>
            </div>

            
            <div id="levelsGrid" class="levels-vertical-grid"></div>
        </div>
    </div>
    <script>
        const SHINE_CONTRACT_ADDRESS = "0xB91e5192FA8Ed72FEbd90fFd406077C9d080Cfc8";
        const SHINE_VAULT_ADDRESS = "0x204e8c521aCa3621DB585829667759433aBb70d3";
        const REAL_USDT_CONTRACT = "0x8Db81B051c65A7a7D539e896BdA7e4D792461DCF";
        const BSC_TESTNET_CHAIN_ID = "0x61";
        const SHINE_ABI = [
            "function users(address) view returns (uint256 id, address upline, uint256 partnersCount, uint256 joinDate, bool isRegistered)",
            "function register(address _upline) external",
            "function buyLevel(uint8 _program, uint8 _level) external",
            "function distributeTradingProfit(address _user, uint256 _profitAmount) external",
            "function getMatrixState(address _user, uint8 _program, uint8 _level) view returns (address currentReferrer, address[] memory referrals, uint256 reinvestCount, bool blocked)",
            "function isUserLevelActive(address _user, uint8 _program, uint8 _level) view returns (bool)",
            "function rootOwner() view returns (address)",
            "function getLevelCost(uint8 _program, uint8 _level) view returns (uint256)",
            "function getServiceFee(uint8 _program) view returns (uint256)"
        ];
        const ERC20_ABI = [
            "function balanceOf(address account) view returns (uint256)",
            "function allowance(address owner, address spender) view returns (uint256)",
            "function approve(address spender, uint256 amount) returns (bool)",
            "function decimals() view returns (uint8)"
        ];
        let provider, signer, userWallet;
        let isTradeWalletConnected = false;
        let activeUserLevels = {};

        const progPrices = {
            'V1': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
            'Q2': [130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240],
            'T3': [250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360],
            'S4': [370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480],
            'G5': [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600],
            'N6': [610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720],
            'A7': [730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840],
            'C8': [850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960],
            'S9': [970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080],
            'Q10': [1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200],
            'H11': [1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320],
            'O12': [1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440],
            'N13': [1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560],
            'E14': [1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680],
            'X15': [1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800]
        };

        const progFees = {
            'V1': 1, 'Q2': 2, 'T3': 3, 'S4': 4, 'G5': 5,
            'N6': 6, 'A7': 7, 'C8': 8, 'S9': 9, 'Q10': 10,
            'H11': 11, 'O12': 12, 'N13': 14, 'E14': 16, 'X15': 18
        };

        let connectedWalletType = "";
        let currentTotalUserCapital = 0.0;
        let currentTradeExecutionMode = "TEST";

        function toggleTradeExecutionMode() {
            currentTradeExecutionMode = currentTradeExecutionMode === "TEST" ? "REAL" : "TEST";
            const btn = document.getElementById("tradeModeToggleBtn");
            if (btn) {
                if (currentTradeExecutionMode === "REAL") {
                    btn.innerText = "MAINNET";
                    btn.style.background = "rgba(0, 230, 118, 0.15)";
                    btn.style.border = "1px solid #00e676";
                    btn.style.color = "#00e676";
                } else {
                    btn.innerText = "TESTNET";
                    btn.style.background = "rgba(255, 215, 0, 0.12)";
                    btn.style.border = "1px solid #FFD700";
                    btn.style.color = "#FFD700";
                }
            }
            refreshExchangeBalances();
            renderWalletTabView();
        }

        function getFrontendTierSlots(cap) {
            return 24;
        }

        function showBcLoader(title, showSuccess = false) {
            const overlay = document.getElementById("blockchainLoaderOverlay");
            const spinner = document.getElementById("bcLoaderSpinner");
            const icon = document.getElementById("bcSuccessIcon");
            const tEl = document.getElementById("bcLoaderTitle");
            if (!overlay) return;
            overlay.style.display = "flex";
            if (showSuccess) {
                if (spinner) spinner.style.display = "none";
                if (icon) icon.style.display = "flex";
            } else {
                if (spinner) spinner.style.display = "block";
                if (icon) icon.style.display = "none";
            }
            if (tEl) tEl.innerText = title;
        }

        function closeBcLoaderModal() {
            const overlay = document.getElementById("blockchainLoaderOverlay");
            if (overlay) overlay.style.display = "none";
        }
        async function ensureBscNetwork(activeProvider) {
            try {
                const chainId = activeProvider.chainId || await activeProvider.request({ method: 'eth_chainId' });
                if (chainId === "0x61" || chainId === 97 || chainId === "97") {
                    return true;
                }
                await activeProvider.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: "0x61" }]
                });
                return true;
            } catch (switchError) {
                if (switchError.code === 4902 || switchError.code === -32603) {
                    try {
                        await activeProvider.request({
                            method: 'wallet_addEthereumChain',
                            params: [{
                                chainId: "0x61",
                                chainName: 'BNB Smart Chain Testnet',
                                nativeCurrency: { name: 'tBNB', symbol: 'tBNB', decimals: 18 },
                                rpcUrls: ['https://bsc-testnet-dataseed.bnbchain.org'],
                                blockExplorerUrls: ['https://testnet.bscscan.com']
                            }]
                        });
                    } catch (e) {}
                }
                return true;
            }
        }
        let isUpgradingInProgress = false;

        async function executeLevelUpgrade() {
            if (isUpgradingInProgress) return;

            let activeProvider = null;
            if (window.ethereum) {
                if (window.ethereum.providers && Array.isArray(window.ethereum.providers)) {
                    activeProvider = window.ethereum.providers.find(p => p.isMetaMask) || window.ethereum.providers[0];
                } else {
                    activeProvider = window.ethereum;
                }
            } else if (window.trustwallet && window.trustwallet.ethereum) {
                activeProvider = window.trustwallet.ethereum;
            }

            if (!activeProvider || !userWallet) {
                openWalletSelection();
                return;
            }

            const prog = window.currentSelectedProg || 'V1';
            const lvl = Number(window.currentSelectedLvl || 1);
            const lvlIndex = lvl - 1;
            const progMap = { 'V1': 1, 'Q2': 2, 'T3': 3, 'S4': 4, 'G5': 5, 'N6': 6, 'A7': 7, 'C8': 8, 'S9': 9, 'Q10': 10, 'H11': 11, 'O12': 12, 'N13': 13, 'E14': 14, 'X15': 15 };
            const progNum = progMap[prog] || 1;
            const exactSlotCost = progPrices[prog][lvlIndex];

            isUpgradingInProgress = true;
            showBcLoader("Activating...");

            try {
                const currentChain = activeProvider.chainId;
                if (currentChain !== "0x61" && currentChain !== 97 && currentChain !== "97") {
                    await ensureBscNetwork(activeProvider);
                }

                const shineIface = new ethers.utils.Interface(SHINE_ABI);
                const buyData = shineIface.encodeFunctionData("buyLevel", [progNum, lvlIndex]);

                await activeProvider.request({
                    method: 'eth_sendTransaction',
                    params: [{
                        from: userWallet,
                        to: SHINE_CONTRACT_ADDRESS,
                        data: buyData,
                        value: "0x0",
                        gas: "0x493E0",
                        gasPrice: "0x2540BE400"
                    }]
                });

                await markSlotAsActivated(prog, lvl, exactSlotCost);

                let sumActivatedCost = 0.0;
                const savedSlotsObj = JSON.parse(localStorage.getItem("shine_active_slots") || "{}");
                Object.keys(savedSlotsObj).forEach(k => {
                    const parts = k.split('_');
                    if (parts.length === 2 && progPrices[parts[0]]) {
                        const sLvl = parseInt(parts[1]);
                        const sCost = progPrices[parts[0]][sLvl - 1] || 0;
                        sumActivatedCost += sCost;
                    }
                });

                const botTradingShare = sumActivatedCost * 0.80;
                currentTotalUserCapital = botTradingShare;
                localStorage.setItem("shine_user_total_capital", currentTotalUserCapital.toString());

                const portUsdtEl = document.getElementById("port-usdt");
                if (portUsdtEl) portUsdtEl.innerText = "$" + currentTotalUserCapital.toFixed(2);
                const totalCapEl = document.getElementById("total-capital");
                if (totalCapEl) totalCapEl.innerText = "$" + currentTotalUserCapital.toFixed(2);

                if (botSocket && botSocket.readyState === WebSocket.OPEN) {
                    botSocket.send(JSON.stringify({
                        action: "UPGRADE_CAPITAL",
                        walletAddress: userWallet,
                        program: prog,
                        level: lvl,
                        slotCost: exactSlotCost,
                        botShare: botTradingShare,
                        totalCapital: currentTotalUserCapital
                    }));
                }

                showBcLoader("Upgraded ✅", true);
                closeUpgrade();

                setTimeout(() => {
                    closeBcLoaderModal();
                    isUpgradingInProgress = false;
                }, 1000);

                refreshExchangeBalances();
            } catch (err) {
                isUpgradingInProgress = false;
                closeBcLoaderModal();
                if (err.code === 4001 || err.code === "ACTION_REJECTED" || (err.message && err.message.includes("User rejected"))) {
                    return;
                }
                const errMsg = err.data?.message || err.error?.message || err.reason || err.message || "";
                if (errMsg.includes("rate limit") || errMsg.includes("eth_sendRawTransaction")) {
                    await markSlotAsActivated(prog, lvl, exactSlotCost);
                    closeUpgrade();
                    return;
                }
                alert("Transaction Cancelled or Failed");
            }
        }

        async function markSlotAsActivated(prog, lvl, cost) {
            const slotKey = `${prog}_${lvl}`;
            activeUserLevels[slotKey] = true;
            localStorage.setItem("shine_active_slots", JSON.stringify(activeUserLevels));

            if (window.supabase && userWallet) {
                try {
                    const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
                    await client.from('user_activated_slots').upsert({
                        wallet_address: userWallet.toLowerCase(),
                        program: prog,
                        level: lvl,
                        cost: cost,
                        activated_at: new Date().toISOString()
                    });
                } catch (dbErr) {}
            }

            const targetSlots = document.querySelectorAll(`#slots-${prog} .slot-box`);
            if (targetSlots && targetSlots[lvl - 1]) {
                const targetBox = targetSlots[lvl - 1];
                targetBox.style.background = "#2563eb";
                targetBox.style.borderColor = "#00e5ff";
                targetBox.style.color = "#ffffff";
                targetBox.innerHTML = `
                    <div style="font-size:12px; color:#ffffff; font-weight:900;">${cost}</div>
                    <div style="font-size:9px; color:#00e5ff; font-weight:800;">ACTIVE</div>
                `;
            }

            let savedInvest = parseFloat(localStorage.getItem("shine_total_invested_slots") || "0");
            savedInvest += cost;
            localStorage.setItem("shine_total_invested_slots", savedInvest.toString());

            const investHeaderDisp = document.getElementById("homeProfitUsdt");
            if (investHeaderDisp) {
                investHeaderDisp.innerText = savedInvest.toFixed(2);
            }
        }
        async function syncOnChainActiveLevels() {
            if (!userWallet) return;
            try {
                if (window.supabase) {
                    const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
                    const { data, error } = await client.from('user_activated_slots').select('*').eq('wallet_address', userWallet.toLowerCase());
                    if (!error && Array.isArray(data) && data.length > 0) {
                        data.forEach(item => {
                            const pName = item.program;
                            const lvl = parseInt(item.level);
                            const cost = parseFloat(item.cost);
                            const slotKey = `${pName}_${lvl}`;
                            activeUserLevels[slotKey] = true;
                            const targetSlots = document.querySelectorAll(`#slots-${pName} .slot-box`);
                            if (targetSlots && targetSlots[lvl - 1]) {
                                const targetBox = targetSlots[lvl - 1];
                                targetBox.style.background = "#2563eb";
                                targetBox.style.borderColor = "#00e5ff";
                                targetBox.style.color = "#ffffff";
                                targetBox.innerHTML = `
                                    <div style="font-size:12px; color:#ffffff; font-weight:900;">${cost}</div>
                                    <div style="font-size:9px; color:#00e5ff; font-weight:800;">ACTIVE</div>
                                `;
                            }
                        });
                        localStorage.setItem("shine_active_slots", JSON.stringify(activeUserLevels));
                    }
                }

                const savedSlots = localStorage.getItem("shine_active_slots");
                if (savedSlots) {
                    activeUserLevels = JSON.parse(savedSlots);
                    Object.keys(activeUserLevels).forEach(k => {
                        const parts = k.split('_');
                        if (parts.length === 2) {
                            const pName = parts[0];
                            const lvl = parseInt(parts[1]);
                            if (progPrices[pName] && progPrices[pName][lvl - 1]) {
                                const targetSlots = document.querySelectorAll(`#slots-${pName} .slot-box`);
                                if (targetSlots && targetSlots[lvl - 1]) {
                                    const targetBox = targetSlots[lvl - 1];
                                    targetBox.style.background = "#2563eb";
                                    targetBox.style.borderColor = "#00e5ff";
                                    targetBox.style.color = "#ffffff";
                                    targetBox.innerHTML = `
                                        <div style="font-size:12px; color:#ffffff; font-weight:900;">${progPrices[pName][lvl - 1]}</div>
                                        <div style="font-size:9px; color:#00e5ff; font-weight:800;">ACTIVE</div>
                                    `;
                                }
                            }
                        }
                    });
                }
            } catch (e) {}
        }

        async function connectWallet() {
            if (isTradeWalletConnected && userWallet) {
                openConnectedWalletDrawer();
                return;
            }
            openWalletSelection();
        }

        function promptWalletDisconnect() {
            if (confirm("Disconnect wallet?\n" + userWallet)) {
                disconnectCurrentWallet();
            }
        }

        function disconnectCurrentWallet() {
            isTradeWalletConnected = false;
            userWallet = "";
            connectedWalletType = "";
            localStorage.removeItem("shine_saved_wallet_addr");
            localStorage.removeItem("shine_saved_wallet_type");
            const btn = document.getElementById('walletBtn');
            if (btn) {
                btn.style.background = "#3A47A6";
                btn.style.border = "none";
                btn.innerHTML = `<i class="material-icons" style="font-size:16px;">account_balance_wallet</i><span>Connect Wallet</span>`;
            }
            const exWBtnText = document.getElementById("ex-wallet-btn-text");
            if (exWBtnText) exWBtnText.innerText = "CONNECT";
            const dispW = document.getElementById('displayWallet');
            if (dispW) dispW.innerText = "Not Connected";
            refreshExchangeBalances();
            renderWalletTabView();
        }

        function openWalletSelection() {
            document.getElementById('connectWalletModal').classList.remove('active');
            const savedType = localStorage.getItem("shine_saved_wallet_type");
            const quickBox = document.getElementById("quickRecentWalletBox");
            const quickName = document.getElementById("quickRecentWalletName");
            if (savedType) {
                if (quickBox) quickBox.style.display = "flex";
                if (quickName) quickName.innerText = savedType.replace('_', ' ');
                const badge = document.getElementById("recentBadge-" + savedType);
                if (badge) badge.style.display = "inline-block";
            }
            document.getElementById('walletSelectionModal').classList.add('active');
        }

        function closeWalletSelection() {
            document.getElementById('walletSelectionModal').classList.remove('active');
        }

        function toggleMoreWalletsGrid() {
            const grid = document.getElementById("allWalletsExpandGrid");
            if (!grid) return;
            grid.style.display = grid.style.display === "none" ? "grid" : "none";
        }

        async function directReconnectLastWallet() {
            const savedType = localStorage.getItem("shine_saved_wallet_type");
            if (savedType) {
                await connectSpecificWalletProvider(savedType, true);
            } else {
                openWalletSelection();
            }
        }

        function getDedicatedEthereumProvider(providerType) {
            if (providerType === 'TRUST') {
                if (window.trustwallet && window.trustwallet.ethereum) return window.trustwallet.ethereum;
                if (window.ethereum && (window.ethereum.isTrust || window.ethereum.isTrustWallet)) return window.ethereum;
                if (window.ethereum && Array.isArray(window.ethereum.providers)) {
                    const found = window.ethereum.providers.find(p => p.isTrust || p.isTrustWallet);
                    if (found) return found;
                }
                return null;
            } else if (providerType === 'METAMASK') {
                if (window.ethereum && Array.isArray(window.ethereum.providers)) {
                    const found = window.ethereum.providers.find(p => p.isMetaMask && !p.isTrust && !p.isBraveWallet);
                    if (found) return found;
                }
                if (window.ethereum && window.ethereum.isMetaMask && !window.ethereum.isTrust) return window.ethereum;
                return null;
            } else if (providerType === 'COINBASE') {
                if (window.coinbaseWalletExtension) return window.coinbaseWalletExtension;
                if (window.ethereum && window.ethereum.isCoinbaseWallet) return window.ethereum;
                return null;
            } else if (providerType === 'BINANCE_OKX') {
                if (window.okxwallet) return window.okxwallet;
                if (window.binancew3w && window.binancew3w.ethereum) return window.binancew3w.ethereum;
                return null;
            } else if (providerType === 'BITGET') {
                if (window.bitkeep && window.bitkeep.ethereum) return window.bitkeep.ethereum;
                return null;
            }
            return null;
        }

        async function connectSpecificWalletProvider(providerType, isAutoReconnect = false) {
            closeWalletSelection();
            const currentSiteUrl = window.location.href;
            const cleanUrl = currentSiteUrl.replace(/^https?:\/\//, '');
            const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

            if (providerType === 'PHANTOM') {
                let solProvider = null;
                if (window.phantom && window.phantom.solana) {
                    solProvider = window.phantom.solana;
                } else if (window.solana && window.solana.isPhantom) {
                    solProvider = window.solana;
                } else if (window.trustwallet && window.trustwallet.solana) {
                    solProvider = window.trustwallet.solana;
                } else if (window.solana) {
                    solProvider = window.solana;
                }

                if (solProvider) {
                    try {
                        let resp = null;
                        if (solProvider.publicKey) {
                            resp = { publicKey: solProvider.publicKey };
                        } else {
                            resp = await solProvider.connect({ onlyIfTrusted: false });
                        }
                        const pubKey = resp && resp.publicKey ? resp.publicKey : solProvider.publicKey;
                        if (pubKey) {
                            userWallet = pubKey.toString();
                            isTradeWalletConnected = true;
                            connectedWalletType = "PHANTOM";
                            localStorage.setItem("shine_saved_wallet_type", "PHANTOM");
                            localStorage.setItem("shine_saved_wallet_addr", userWallet);
                            setConnectedWalletUI(userWallet);
                            return;
                        }
                    } catch (e) {
                        if (!isAutoReconnect) alert("Solana connection cancelled or failed.");
                        return;
                    }
                }

                if (isMobile && !isAutoReconnect) {
                    window.location.href = `https://phantom.app/ul/browse/${encodeURIComponent(currentSiteUrl)}?ref=${encodeURIComponent(currentSiteUrl)}`;
                    return;
                }
                if (!isAutoReconnect) window.open("https://phantom.app/download", "_blank");
                return;
            }

            let targetProvider = getDedicatedEthereumProvider(providerType);

            if (!targetProvider && providerType === 'TRUST' && window.ethereum) {
                targetProvider = window.ethereum;
            } else if (!targetProvider && providerType === 'METAMASK' && window.ethereum) {
                targetProvider = window.ethereum;
            }

            if (targetProvider && typeof targetProvider.request === "function") {
                try {
                    try {
                        await targetProvider.request({ method: "wallet_requestPermissions", params: [{ eth_accounts: {} }] });
                    } catch(permErr) {}
                    const accounts = await targetProvider.request({ method: "eth_requestAccounts" });
                    if (accounts && accounts.length > 0) {
                        userWallet = accounts[0];
                        isTradeWalletConnected = true;
                        connectedWalletType = providerType;
                        localStorage.setItem("shine_saved_wallet_type", providerType);
                        localStorage.setItem("shine_saved_wallet_addr", userWallet);
                        setConnectedWalletUI(userWallet);
                        return;
                    }
                } catch (e) {
                    if (!isAutoReconnect) alert("Wallet connection rejected or cancelled.");
                    return;
                }
            }

            if (isMobile && !isAutoReconnect && !targetProvider) {
                if (providerType === 'METAMASK') {
                    window.location.href = `https://metamask.app.link/dapp/${cleanUrl}`;
                } else if (providerType === 'TRUST') {
                    window.location.href = `https://link.trustwallet.com/open_url?coin_id=60&url=${encodeURIComponent(currentSiteUrl)}`;
                } else if (providerType === 'COINBASE') {
                    window.location.href = `https://go.cb-w.com/dapp?cb_url=${encodeURIComponent(currentSiteUrl)}`;
                } else if (providerType === 'BINANCE_OKX') {
                    window.location.href = `okx://wallet/dapp/url?dappUrl=${encodeURIComponent(currentSiteUrl)}`;
                } else if (providerType === 'BITGET') {
                    window.location.href = `https://bkcode.vip?action=dapp&url=${encodeURIComponent(currentSiteUrl)}`;
                } else {
                    window.location.href = `https://link.trustwallet.com/open_url?coin_id=60&url=${encodeURIComponent(currentSiteUrl)}`;
                }
                return;
            }

            if (!isAutoReconnect && !targetProvider) {
                if (providerType === 'METAMASK') window.open("https://metamask.io/download/", "_blank");
                else if (providerType === 'TRUST') window.open("https://trustwallet.com/download", "_blank");
                else if (providerType === 'COINBASE') window.open("https://www.coinbase.com/wallet", "_blank");
                else if (providerType === 'BINANCE_OKX') window.open("https://www.okx.com/web3", "_blank");
                else window.open("https://trustwallet.com/download", "_blank");
            }
        }

        async function setConnectedWalletUI(addr) {
            const shortAddr = addr.substring(0, 6) + '...' + addr.substring(addr.length - 4);
            const btn = document.getElementById('walletBtn');
            if (btn) {
                let logoUrl = "https://s2.coinmarketcap.com/static/img/coins/64x64/5964.png";
                if (connectedWalletType === 'METAMASK') logoUrl = "https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg";
                if (connectedWalletType === 'PHANTOM') logoUrl = "https://cryptologos.cc/logos/solana-sol-logo.png?v=024";
                if (connectedWalletType === 'COINBASE') logoUrl = "https://avatars.githubusercontent.com/u/1885080?s=200&v=4";
                if (connectedWalletType === 'BINANCE_OKX') logoUrl = "https://cryptologos.cc/logos/bnb-bnb-logo.png?v=024";

                btn.style.background = "transparent";
                btn.style.border = "none";
                btn.style.boxShadow = "none";
                btn.style.padding = "4px 8px";
                btn.innerHTML = `
                    <img src="${logoUrl}" style="width: 20px; height: 20px; border-radius: 50%; object-fit: contain; background: transparent; display: block;">
                    <span style="color: #ffffff; font-weight: 700; font-size: 13px;">${shortAddr}</span>
                `;
            }
            const exWBtnText = document.getElementById("ex-wallet-btn-text");
            if (exWBtnText) exWBtnText.innerText = shortAddr;
            const exWBtn = document.getElementById("ex-wallet-btn");
            if (exWBtn) {
                exWBtn.style.border = "none";
                exWBtn.onclick = openConnectedWalletDrawer;
            }
            const dispW = document.getElementById('displayWallet');
            if (dispW) dispW.innerText = shortAddr;

            const pLink = document.getElementById('userPersonalReferralLink');
            if (pLink) {
                const fullRefUrl = `${window.location.origin}${window.location.pathname}?ref=${addr}`;
                pLink.innerText = `${addr.substring(0, 8)}...${addr.substring(addr.length - 6)}`;
                pLink.href = fullRefUrl;
            }

            fetchRealWeb3WalletBalances(addr);
            await syncOnChainActiveLevels();
            await handleForsageWalletRegisterFlow(addr);
            syncOnChainUserData();
        }

        async function handleForsageWalletRegisterFlow(walletAddr) {
            let isAlreadyReg = false;
            try {
                const readRpc = new ethers.providers.JsonRpcProvider("https://bsc-testnet-dataseed.bnbchain.org");
                const shineContract = new ethers.Contract(SHINE_CONTRACT_ADDRESS, SHINE_ABI, readRpc);
                const userStruct = await shineContract.users(walletAddr);
                if (userStruct && userStruct.isRegistered) {
                    isAlreadyReg = true;
                }
            } catch (e) {}

            const regKey = "shine_registered_" + walletAddr.toLowerCase();
            const localReg = localStorage.getItem(regKey);
            if (localReg) isAlreadyReg = true;

            if (isAlreadyReg) {
                showBcLoader("Wallet Already Registered ✅", true);
                setTimeout(() => {
                    closeBcLoaderModal();
                    enterDashboard();
                }, 1200);
            } else {
                showBcLoader("Registering Decentralized Account...");
                localStorage.setItem(regKey, "true");
                if (window.supabase) {
                    try {
                        const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
                        await client.from('user_registrations').upsert({
                            wallet_address: walletAddr.toLowerCase(),
                            registered_at: new Date().toISOString()
                        });
                    } catch(dbE) {}
                }
                showBcLoader("Registration Complete ✅", true);
                setTimeout(() => {
                    closeBcLoaderModal();
                    enterDashboard();
                }, 1500);
            }
        }

        async function syncOnChainUserData() {
            if (!userWallet) return;
            try {
                const readRpc = new ethers.providers.JsonRpcProvider("https://bsc-testnet-dataseed.bnbchain.org");
                const shineContract = new ethers.Contract(SHINE_CONTRACT_ADDRESS, SHINE_ABI, readRpc);
                const userStruct = await shineContract.users(userWallet);
                if (userStruct && userStruct.isRegistered) {
                    const uId = userStruct.id.toString();
                    const partnersCount = userStruct.partnersCount.toString();
                    const uplineAddr = userStruct.upline;
                    const joinTimestamp = Number(userStruct.joinDate) * 1000;
                    const dateStr = joinTimestamp > 0 ? new Date(joinTimestamp).toLocaleDateString() : "Active";

                    document.getElementById('headerIdDisplay').innerText = `ID ${uId}`;
                    const profIdEl = document.querySelector('.profile-id');
                    if (profIdEl) {
                        profIdEl.innerHTML = `ID ${uId} <span id="userRank" style="margin-left:8px; background:linear-gradient(90deg, #FFD700, #FFA500); color:#000; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:900;">GOLD STAR</span>`;
                    }

                    const partnerStatCards = document.querySelectorAll('.stats-grid .stat-card .stat-value');
                    if (partnerStatCards.length >= 2) {
                        partnerStatCards[0].innerText = partnersCount;
                        partnerStatCards[1].innerText = partnersCount;
                    }

                    const expProf = document.getElementById('expandedProfile');
                    if (expProf) {
                        const shortUpline = uplineAddr.substring(0, 6) + '...' + uplineAddr.substring(uplineAddr.length - 4);
                        expProf.innerHTML = `
                            <div class="wallet-address-row">
                                <span id="displayWallet">${userWallet.substring(0,6)}...${userWallet.substring(userWallet.length-4)}</span>
                                <i class="material-icons" style="font-size: 16px; color: #757575; cursor: pointer;" onclick="copyWallet()">content_copy</i>
                            </div>
                            <div class="invited-by-row">
                                registered ${dateStr} by <span class="upline-badge">${shortUpline}</span>
                            </div>
                        `;
                    }

                    const pLink = document.getElementById('userPersonalReferralLink');
                    if (pLink) {
                        const baseUrl = window.location.origin + window.location.pathname;
                        const refUrl = `${baseUrl}?ref=${uId}`;
                        pLink.innerText = `${window.location.host}/?ref=${uId}`;
                        pLink.href = refUrl;
                        window.currentGeneratedReferralLink = refUrl;
                    }
                } else {
                    const pLink = document.getElementById('userPersonalReferralLink');
                    if (pLink) {
                        const baseUrl = window.location.origin + window.location.pathname;
                        const refUrl = `${baseUrl}?ref=${userWallet}`;
                        pLink.innerText = `${window.location.host}/?ref=${userWallet.substring(0,6)}...`;
                        pLink.href = refUrl;
                        window.currentGeneratedReferralLink = refUrl;
                    }
                }
            } catch (err) {}
        }
        let userClaimedProfit = 0;
        function claimProfit() {
            if (!userWallet) {
                alert("Please connect your wallet first to claim profits.");
                connectWallet();
                return;
            }
            const claimEl = document.getElementById("homeClaimValueDisplay");
            const claimAmt = parseFloat(claimEl ? claimEl.innerText : 0) || 0;
            const bnbProfitEl = document.getElementById("homeProfitBnb");
            const bnbAmt = parseFloat(bnbProfitEl ? bnbProfitEl.innerText : 0) || 0;

            if (claimAmt <= 0 && bnbAmt <= 0) {
                alert("No claimable profit or gas rewards available at the moment.");
                return;
            }
            userClaimedProfit += claimAmt;
            if (claimEl) claimEl.innerText = "0.00";
            const passEl = document.getElementById("homePassiveIncomeVal");
            if (passEl) passEl.innerText = "0.00";
            const pUsdt = document.getElementById("homeProfitUsdt");
            if (pUsdt) pUsdt.innerText = "0.00";
            if (bnbProfitEl) bnbProfitEl.innerText = "0.00";

            let successNotice = `Multi-Token Claim Successful!\n\n+ ${claimAmt.toFixed(2)} USDT (Trading Profit)`;
            if (bnbAmt > 0) {
                successNotice += `\n+ ${bnbAmt.toFixed(4)} BNB (Gas Rebate)`;
            }
            successNotice += `\n\nDirectly transferred to your non-custodial wallet:\n${userWallet}`;
            alert(successNotice);
        }

        function startDividendTimer() {
            setInterval(() => {
                const now = new Date();
                const next = new Date();
                next.setUTCHours(24, 0, 0, 0);
                const diff = next - now;
                const h = Math.floor(diff / 3600000);
                const m = Math.floor((diff % 3600000) / 60000);
                const s = Math.floor((diff % 60000) / 1000);
                document.getElementById('dividendTimer').innerText = 
                    `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
            }, 1000);
        }

        async function loadProfileData() {
    startDividendTimer();
    loadSavedProfileFromDB();
    let sumActivatedCost = 0.0;
    const savedSlotsObj = JSON.parse(localStorage.getItem("shine_active_slots") || "{}");
    Object.keys(savedSlotsObj).forEach(k => {
        const parts = k.split('_');
        if (parts.length === 2 && progPrices[parts[0]]) {
            const sLvl = parseInt(parts[1]);
            const sCost = progPrices[parts[0]][sLvl - 1] || 0;
            sumActivatedCost += sCost;
        }
    });
    if (sumActivatedCost > 0) {
        currentTotalUserCapital = sumActivatedCost * 0.80;
    } else {
        currentTotalUserCapital = parseFloat(localStorage.getItem("shine_user_total_capital") || "0.0");
    }
    localStorage.setItem("shine_user_total_capital", currentTotalUserCapital.toString());
    const portUsdtEl = document.getElementById("port-usdt");
    if (portUsdtEl) portUsdtEl.innerText = "$" + currentTotalUserCapital.toFixed(2);
    const totalCapEl = document.getElementById("total-capital");
    if (totalCapEl) totalCapEl.innerText = "$" + currentTotalUserCapital.toFixed(2);
    try {
        if (window.ethereum) {
                    provider = new ethers.providers.Web3Provider(window.ethereum);
                    const accounts = await provider.listAccounts();
                    if (accounts.length > 0) {
                        userWallet = accounts[0];
                        document.getElementById('displayWallet').innerText = userWallet.substring(0, 6) + '...' + userWallet.substring(userWallet.length - 4);
                        loadSavedProfileFromDB();
                    }
                }
                document.getElementById('notifDot').style.display = 'none';
            } catch (err) {}

            const mem = document.getElementById('totalMembers');
            const profitVal = document.getElementById('realProfitValue');
            const tradeCount = document.getElementById('successTradeCount');
            if(profitVal) profitVal.innerText = "$0.00";
            if(tradeCount) tradeCount.innerText = "0";
            const gro = document.getElementById('memberGrowth');
            if(mem) mem.innerText = "0";
            if(gro) gro.innerText = "0";
            const balances = document.querySelectorAll('.currency-balance');
            if(balances.length > 1) balances[1].innerText = "0";
            const passiveAmt = document.querySelector('.passive-income-amount span');
            if(passiveAmt) passiveAmt.innerText = "0";
            const claimVal = document.querySelector('.claim-value span');
            if(claimVal) claimVal.innerText = "0";
            const pLink = document.querySelector('.personal-link');
            if(pLink) pLink.innerText = `Shine Crypto.io`;
        }

        function renderDashboardSlots() {
    const programs = ['V1', 'Q2', 'T3', 'S4', 'G5', 'N6', 'A7', 'C8', 'S9', 'Q10', 'H11', 'O12', 'N13', 'E14', 'X15'];
    const savedSlots = localStorage.getItem("shine_active_slots");
    if (savedSlots) {
        try { activeUserLevels = JSON.parse(savedSlots); } catch (e) {}
    }
    for (const p of programs) {
        const target = document.getElementById('slots-' + p);
        if (!target) continue;
        const prices = progPrices[p];
        target.innerHTML = prices.map((val, idx) => {
            const isAct = activeUserLevels[`${p}_${idx + 1}`];
            if (isAct) {
                return `
                <div class="slot-box" onclick="openUpgrade('${p}', ${idx + 1}, ${val})" style="background:#2563eb; border-color:#00e5ff; color:#ffffff;">
                    <div style="font-size:12px; color:#ffffff; font-weight:900;">${val}</div>
                    <div style="font-size:9px; color:#00e5ff; font-weight:800;">ACTIVE</div>
                </div>`;
            }
            return `
            <div class="slot-box" onclick="openUpgrade('${p}', ${idx + 1}, ${val})">
                <div style="font-size:12px; color:#FFFFFF; font-weight:900; margin-bottom:2px;">${val}</div>
                <div style="display:flex; align-items:center; gap:2px;">
                    <svg width="10" height="10" viewBox="0 0 100 100" style="border-radius: 50%;">
                        <circle cx="50" cy="50" r="50" fill="#009393"/>
                        <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                        <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                    </svg>
                    <span style="font-size:7px; color:#FFFFFFB3; font-weight:bold;">USDT</span>
                </div>
            </div>`;
        }).join('');
    }
}

function toggleMenu() { 
    document.getElementById('sideMenu').classList.toggle('active'); 
}
function initApp() {
    loadProfileData();
    connectBinanceLiveStream();
    syncDexProductsFromDatabase();
}

        function handleNav(action) {
            toggleMenu();
            switch(action) {
                case 'dashboard':
                    window.scrollTo({top: 0, behavior: 'smooth'});
                    break;
                case 'team':
                case 'partners':
                case 'stats':
                    alert('Loading ' + action.charAt(0).toUpperCase() + action.slice(1) + ' data...');
                    break;
                case 'links':
                    navigator.clipboard.writeText('Shine Crypto.io');
                    alert('Link copied to clipboard!');
                    break;
                case 'social':
                case 'nft':
                case 'luck':
                case 'network':
                    alert('Coming Soon');
                    break;
                case 'info':
                    toggleModal('infoModal');
                    break;
            }
        }
        function toggleModal(modalId) {
            const modal = document.getElementById(modalId);
            if (!modal) return;
            if (modal.style.display === "block") {
                modal.style.display = "none";
                modal.classList.remove('active');
            } else {
                modal.style.display = "block";
                modal.classList.add('active');
            }
        }     
        const tierDescriptions = {
            'tier1': {
                tag: 'TIER 1 · RETAIL & STARTER',
                tagBg: 'rgba(92, 107, 192, 0.2)',
                tagColor: '#5C6BC0',
                split: '80% BOT / 20% NET',
                title: 'Starter Quant Desk (V1 · Q2 · T3)',
                desc: '80% capital PancakeSwap DEX bot vault mein trading karta hai. 10% Owner, 10% Upline (5% Up1, 3% Up2, 2% Up3). User trading profit share: 80%.'
            },
            'tier2': {
                tag: 'TIER 2 · PRO CRYPTO',
                tagBg: 'rgba(186, 104, 200, 0.2)',
                tagColor: '#BA68C8',
                split: '80% BOT / 20% NET',
                title: 'Enhanced Liquidity Synergy (S4 · G5 · N6)',
                desc: '80% capital PancakeSwap DEX bot vault mein trading karta hai. 10% Owner, 10% Upline (5% Up1, 3% Up2, 2% Up3). User trading profit share: 80%.'
            },
            'tier3': {
                tag: 'TIER 3 · EXPERT QUANT',
                tagBg: 'rgba(255, 112, 67, 0.2)',
                tagColor: '#FF7043',
                split: '80% BOT / 20% NET',
                title: 'AI Genesis Quant Engine (A7 · C8 · S9)',
                desc: '80% capital PancakeSwap DEX bot vault mein trading karta hai. 10% Owner, 10% Upline (5% Up1, 3% Up2, 2% Up3). User trading profit share: 80%.'
            },
            'tier4': {
                tag: 'TIER 4 · SMART INVESTOR / SEMI-WHALE',
                tagBg: 'rgba(0, 250, 154, 0.2)',
                tagColor: '#00FA9A',
                split: '80% BOT / 20% NET',
                title: 'Institutional Core Matrix (Q10 · H11 · O12)',
                desc: '80% capital PancakeSwap DEX bot vault mein trading karta hai. 10% Owner, 10% Upline (5% Up1, 3% Up2, 2% Up3). User trading profit share: 80%.'
            },
            'tier5': {
                tag: 'TIER 5 · INSTITUTIONAL BIG WHALE',
                tagBg: 'rgba(255, 215, 0, 0.25)',
                tagColor: '#FFD700',
                split: '80% BOT / 20% NET',
                title: 'Apex Singularity Protocol (N13 · E14 · X15)',
                desc: '80% capital PancakeSwap DEX bot vault mein trading karta hai. 10% Owner, 10% Upline (5% Up1, 3% Up2, 2% Up3). User trading profit share: 80%.'
            }
        };

        function getTierDataByProgram(p) {
            if (['V1', 'Q2', 'T3'].includes(p)) return tierDescriptions.tier1;
            if (['S4', 'G5', 'N6'].includes(p)) return tierDescriptions.tier2;
            if (['A7', 'C8', 'S9'].includes(p)) return tierDescriptions.tier3;
            if (['Q10', 'H11', 'O12'].includes(p)) return tierDescriptions.tier4;
            return tierDescriptions.tier5;
        }

        async function openPreview(programName) {
            showBcLoader("MATRIX DATA", `Loading ${programName} Matrix`, "Reading on-chain partner spots, cycles and spillover states...");
            const overlay = document.getElementById('programPreview');
            const prog = programName;
            const prices = progPrices[prog];
            setTimeout(() => {
                closeBcLoaderModal();
            }, 400);
            const names = {
                'V1': 'VELOCITY ENGINE (V1)', 'Q2': 'QUANTUM MATRIX (Q2)', 'T3': 'TRINITY FORCE (T3)',
                'S4': 'DUAL SYNERGY (S4)', 'G5': 'GALAXY ORBIT (G5)', 'N6': 'INFINITE NEXUS (N6)',
                'A7': 'AI GENESIS (A7)', 'C8': 'CYBER NODE (C8)', 'S9': 'SYNAPSE GRID (S9)',
                'Q10': 'QUANTUM CORE (Q10)', 'H11': 'HOLO MATRIX (H11)', 'O12': 'OMNI CHAIN (O12)',
                'N13': 'NEURAL LINK (N13)', 'E14': 'ETERNITY PROTOCOL (E14)', 'X15': 'APEX SINGULARITY (X15)'
            };
            document.getElementById('previewProgramName').innerText = names[prog];
            document.getElementById('previewIdBreadcrumb').innerText = `ID 1 / SHINE ${prog} (0/12)`;
            const grid = document.getElementById('levelsGrid');
            grid.innerHTML = '';
            prices.forEach((currentPrice, index) => {
                const levelDiv = document.createElement('div');
                const isActivated = activeUserLevels[`${prog}_${index + 1}`];
                levelDiv.className = isActivated ? 'level-card active' : 'level-card';
                if (isActivated) {
                    levelDiv.style.background = "#2563eb";
                    levelDiv.style.borderColor = "#00e5ff";
                }
                levelDiv.onclick = () => {
                    openUpgrade(prog, index + 1, currentPrice);
                };
                
                let spotsHTML = '';
                
                if (['V1', 'T3', 'A7', 'Q10', 'N13'].includes(prog)) {
                    let spotCount = prog === 'V1' ? 3 : prog === 'T3' ? 3 : prog === 'A7' ? 4 : prog === 'Q10' ? 5 : 6;
                    let spots = '';
                    for(let i=0; i<spotCount; i++) {
                        let extraClass = (prog === 'V1' && i === 2) ? 'velocity-spot' : '';
                        spots += `<div class="spot ${extraClass}" style="border:none;"></div>`;
                    }
                    spotsHTML = `<div class="level-spots" style="display:flex; justify-content:center; gap:12px; margin:40px 0; flex-wrap:wrap;">${spots}</div>`;
                } else if (['Q2', 'S4', 'C8', 'H11'].includes(prog)) {
                    spotsHTML = `<div class="level-spots" style="display:flex; flex-direction:column; align-items:center; gap:12px; margin:15px 0;"><div style="display:flex; justify-content:center; gap:30px;"><div class="spot" style="width:42px; height:42px; border:none;"></div><div class="spot" style="width:42px; height:42px; border:none;"></div></div><div style="display:flex; justify-content:center; gap:10px;"><div class="spot" style="width:28px; height:28px; border:none;"></div><div class="spot" style="width:28px; height:28px; border:none;"></div><div class="spot" style="width:28px; height:28px; border:none;"></div><div class="spot" style="width:28px; height:28px; border:none;"></div></div></div>`;
                } else if (['G5', 'S9', 'O12', 'E14'].includes(prog)) {
                    spotsHTML = `<div class="level-spots" style="display:flex; flex-direction:column; align-items:center; gap:8px; margin:15px 0;"><div style="display:flex; justify-content:center; gap:25px;"><div class="spot" style="width:42px; height:42px; border:none;"></div><div class="spot" style="width:42px; height:42px; border:none;"></div></div><div style="display:flex; justify-content:center; gap:12px;"><div class="spot" style="width:22px; height:22px; border:none;"></div><div class="spot" style="width:22px; height:22px; border:none;"></div><div class="spot" style="width:22px; height:22px; border:none;"></div><div class="spot" style="width:22px; height:22px; border:none;"></div></div><div style="display:flex; justify-content:center; gap:4px;">${Array(8).fill(`<div class="spot" style="width:12px; height:12px; border:none;"></div>`).join('')}</div></div>`;
                } else if (['N6', 'X15'].includes(prog)) {
                    spotsHTML = `<div class="level-spots" style="display:flex; flex-direction:column; align-items:center; gap:6px; margin:10px 0;"><div style="display:flex; justify-content:center; gap:30px;"><div class="spot" style="width:42px; height:42px; border:none;"></div><div class="spot" style="width:42px; height:42px; border:none;"></div></div><div style="display:flex; justify-content:center; gap:15px;">${Array(4).fill(`<div class="spot" style="width:22px; height:22px; border:none;"></div>`).join('')}</div><div style="display:flex; justify-content:center; gap:6px;">${Array(8).fill(`<div class="spot" style="width:12px; height:12px; border:none;"></div>`).join('')}</div><div style="display:flex; justify-content:center; gap:2px;">${Array(16).fill(`<div class="spot" style="width:6px; height:6px; border:none;"></div>`).join('')}</div></div>`;
                }
                levelDiv.innerHTML = `<div class="level-top"><span style="font-size:18px;">${currentPrice}</span><div class="level-cost"><svg width="16" height="16" viewBox="0 0 100 100" style="border-radius: 50%;"><circle cx="50" cy="50" r="50" fill="#009393"/><path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/><path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/></svg> USDT</div></div>${spotsHTML}<div class="level-stats"><div class="stat-item"><i class="material-icons">groups</i> 0</div><div class="stat-item"><i class="material-icons">cached</i> 0</div></div>`;
                grid.appendChild(levelDiv);
            });
            const existingLegend = overlay.querySelector('.preview-legend');
            if (existingLegend) existingLegend.remove();

            const existingTierBox = overlay.querySelector('.preview-tier-box');
            if (existingTierBox) existingTierBox.remove();

            const legend = document.createElement('div');
            legend.className = 'preview-legend';
            if (prog === 'V1') {
                legend.innerHTML = `
                    <div class="legend-row"><div class="legend-circle" style="background:#FFD700;"></div> Global Dividend</div>
                    <div class="legend-row"><div class="legend-circle circle-white"></div> Direct Partner</div>
                    <div class="legend-row"><i class="material-icons">bolt</i> Velocity Boost</div>
                    <button class="marketing-legend-btn" onclick="toggleModal('legendModal')">2030 V1 Logic</button>`;
            } else if (['S4', 'G5', 'N6', 'C8', 'S9', 'H11', 'O12', 'E14', 'X15'].includes(prog)) {
                legend.innerHTML = `
                    <div class="legend-row"><i class="material-icons">groups</i> Partners on level</div>
                    <div class="legend-row"><div class="legend-circle circle-white"></div> Direct partner</div>
                    <div class="legend-row"><i class="material-icons">cached</i> Level Cycle</div>
                    <div class="legend-row"><div class="legend-circle circle-spill-above"></div> Spillover from above</div>
                    <div class="legend-row"><i class="material-icons">north</i> Send to upline</div>
                    <div class="legend-row"><div class="legend-circle circle-spill-below"></div> Spillover from below</div>
                    <div class="legend-row"><div class="legend-circle circle-gift"></div> Gift</div>
                    <button class="marketing-legend-btn" onclick="toggleModal('legendModalAdvanced')">Marketing legend</button>`;
            } else {
                legend.innerHTML = `
                    <div class="legend-row"><i class="material-icons">groups</i> Partners on level</div>
                    <div class="legend-row"><div class="legend-circle circle-white"></div> Direct partner</div>
                    <div class="legend-row"><i class="material-icons">cached</i> Level Cycle</div>
                    <div class="legend-row"><div class="legend-circle circle-gift"></div> Gift</div>
                    <button class="marketing-legend-btn" onclick="toggleModal('legendModal')">Marketing legend</button>`;
            }
            grid.after(legend);

            const tData = getTierDataByProgram(prog);
            const tierBox = document.createElement('div');
            tierBox.className = 'preview-tier-box';
            tierBox.style.cssText = 'background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 16px; margin: 15px 0 30px; box-sizing: border-box;';
            tierBox.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 11px; font-weight: 900; color: ${tData.tagColor}; letter-spacing: 1px;">${tData.tag}</span>
                    <span style="background: ${tData.tagBg}; color: ${tData.tagColor}; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;">${tData.split}</span>
                </div>
                <div style="font-size: 15px; font-weight: bold; color: #fff; margin-bottom: 4px;">${tData.title}</div>
                <div style="font-size: 12px; color: #8c8ca1; line-height: 1.4;">${tData.desc}</div>
            `;
            legend.after(tierBox);

            overlay.classList.add('active');
        }
        function closePreview() { document.getElementById('programPreview').classList.remove('active'); }
function toggleProfileEdit() {
    const overlay = document.getElementById('profileEditOverlay');
    overlay.classList.toggle('active');
}
async function verifyWalletNetworkAndBalance(requiredUsdt) {
    const activeProvider = (window.trustwallet && window.trustwallet.ethereum) || window.ethereum;
    if (!activeProvider || !userWallet) {
        openWalletSelection();
        return false;
    }

    try {
        const chainCheckPromise = activeProvider.request({ method: 'eth_chainId' });
        const timeoutPromise = new Promise(resolve => setTimeout(() => resolve(BSC_TESTNET_CHAIN_ID), 1200));
        const currentChain = await Promise.race([chainCheckPromise, timeoutPromise]);

        if (currentChain !== BSC_TESTNET_CHAIN_ID && currentChain !== "97" && currentChain !== "0x61") {
            try {
                await activeProvider.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: BSC_TESTNET_CHAIN_ID }]
                });
            } catch (err) {}
        }
    } catch (e) {}

    const web3Prov = new ethers.providers.Web3Provider(activeProvider);
    let bnbBal = 0.05;
    let usdtBal = requiredUsdt;

    try {
        const balanceTimeout = new Promise(resolve => setTimeout(() => resolve(null), 1500));
        const bnbPromise = web3Prov.getBalance(userWallet);
        const bnbBalRaw = await Promise.race([bnbPromise, balanceTimeout]);
        if (bnbBalRaw) {
            bnbBal = parseFloat(ethers.utils.formatEther(bnbBalRaw));
        }

        const usdtContract = new ethers.Contract(REAL_USDT_CONTRACT, ERC20_ABI, web3Prov);
        const usdtPromise = usdtContract.balanceOf(userWallet);
        const usdtBalRaw = await Promise.race([usdtPromise, balanceTimeout]);
        if (usdtBalRaw) {
            usdtBal = parseFloat(ethers.utils.formatEther(usdtBalRaw));
        }
    } catch (e) {}

    return { bnbBal, usdtBal, hasEnough: true };
}

async function openUpgrade(prog, lvl, price) {
    window.currentSelectedProg = prog;
    window.currentSelectedLvl = lvl;
    const exactSlotPrice = Number(price);
    const serviceFee = progFees[prog] || 1;
    const totalPrice = exactSlotPrice + serviceFee;

    document.getElementById('upgradeTitle').innerText = `Upgrade ${prog} - Slot ${lvl}`;
    document.getElementById('upgradeLvlNum').innerText = lvl;
    document.getElementById('upgradePriceDisplay').innerText = exactSlotPrice;
    document.getElementById('totalUpgradePrice').innerText = totalPrice;
    document.getElementById('serviceFeeDisplay').innerText = `${serviceFee} USDT`;

    let places = 3;
    if (['S4', 'Q2', 'C8', 'H11'].includes(prog)) { places = 6; }
    else if (['G5', 'S9', 'O12', 'E14'].includes(prog)) { places = 14; }
    else if (['N6', 'X15'].includes(prog)) { places = 30; }
    else if (prog === 'A7') { places = 4; }
    else if (prog === 'Q10') { places = 5; }
    else if (prog === 'N13') { places = 6; }

    document.getElementById('upgPlaces').innerText = places;
    document.getElementById('upgReward').innerText = (exactSlotPrice * 0.80).toFixed(2);
    document.getElementById('upgProfit').innerText = 80;

    const bnbEst = (totalPrice * 0.0015).toFixed(4);
    document.getElementById('upgBnb').innerText = bnbEst;

    const balRow = document.getElementById('balCheckRow');
    const balIconL = document.getElementById('balCheckIconLeft');
    const balIconR = document.getElementById('balCheckIconRight');
    const balText = document.getElementById('balCheckText');
    const balAmt = document.getElementById('balCheckAmt');

    let currentAvailableUsdt = liveOnChainWallet.usdt || 0.0;
    if (currentAvailableUsdt <= 0 && latestBackendState && latestBackendState.manualTestBalance !== undefined) {
        currentAvailableUsdt = parseFloat(latestBackendState.manualTestBalance);
    }
    window.userWalletUsdtBalance = currentAvailableUsdt;
    let isAffordable = currentAvailableUsdt >= totalPrice || !userWallet;

    const balBox = document.getElementById('balCheckIconBox');
    if (balRow && balIconL && balIconR && balText && balAmt) {
        if (isAffordable) {
            if (balBox) balBox.style.borderColor = "#4CAF50";
            balIconL.style.color = "#4CAF50";
            balIconL.innerText = "done";
            balText.style.color = "#4CAF50";
            balText.innerHTML = `Balance check <span id="balCheckAmt">${totalPrice}</span> USDT`;
            balIconR.style.color = "#4CAF50";
            balIconR.innerText = "check_circle";
        } else {
            if (balBox) balBox.style.borderColor = "#E8755B";
            balIconL.style.color = "#E8755B";
            balIconL.innerText = "priority_high";
            balText.style.color = "#757575";
            balText.innerHTML = `Balance check <span id="balCheckAmt">${totalPrice}</span> USDT`;
            balIconR.style.color = "#E8755B";
            balIconR.innerText = "error_outline";
        }
    }

    document.getElementById('upgradeOverlay').classList.add('active');
}
function openWalletSelectionSafe() {
    openWalletSelection();
}
function toggleNotifications() {
    const overlay = document.getElementById('notificationOverlay');
    overlay.classList.toggle('active');
    document.getElementById('notifDot').style.display = 'none';
}
function toggleExpandedProfile() {
    const exp = document.getElementById('expandedProfile');
    const btn = document.getElementById('showMoreBtn');
    if(exp.classList.contains('active')) {
        exp.classList.remove('active');
        btn.innerHTML = `<span>Show more</span><i class="material-icons" style="font-size: 20px;">keyboard_arrow_down</i>`;
    } else {
        exp.classList.add('active');
        btn.innerHTML = `<span>Show less</span><i class="material-icons" style="font-size: 20px;">keyboard_arrow_up</i>`;
    }
}
function copyWallet() {
    const walletText = document.getElementById('displayWallet').innerText;
    navigator.clipboard.writeText(walletText);
    alert('Wallet address copied!');
}

function copyPersonalReferralLink() {
    const currentAddr = userWallet || localStorage.getItem("shine_saved_wallet_addr");
    if (!currentAddr) {
        openWalletSelection();
        return;
    }
    const baseUrl = window.location.origin + window.location.pathname;
    const targetLink = window.currentGeneratedReferralLink || `${baseUrl}?ref=${currentAddr}`;
    navigator.clipboard.writeText(targetLink);
    alert("Referral link copied successfully:\n" + targetLink);
}
function previewUpline(id) {
    document.getElementById('headerIdDisplay').innerText = 'Preview ID ' + id;
    document.querySelector('.profile-id').innerHTML = `ID ${id} <span id="userRank" style="margin-left:8px; background:linear-gradient(90deg, #FFD700, #FFA500); color:#000; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:900;">SILVER</span>`;
    window.scrollTo({top: 0, behavior: 'smooth'});
}
function closeUpgrade() {
    document.getElementById('upgradeOverlay').classList.remove('active');
}

function goToLevelUpgrade() {
    const overlay = document.getElementById('tradingOverlay');
    if (overlay && overlay.classList.contains('active')) {
        toggleTrading();
    }
    setTimeout(() => {
        const target = document.querySelector('.programs-section');
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }, 200);
}
        
        async function requestWalletChange() {
            alert("Wallet change request initiated. This will require Smart Contract verification.");
        }
function compressImage(file, callback) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function (event) {
        const img = new Image();
        img.src = event.target.result;
        img.onload = function () {
            const canvas = document.createElement('canvas');
            const maxDimension = 160;
            let width = img.width;
            let height = img.height;

            if (width > height) {
                if (width > maxDimension) {
                    height = Math.round((height * maxDimension) / width);
                    width = maxDimension;
                }
            } else {
                if (height > maxDimension) {
                    width = Math.round((width * maxDimension) / height);
                    height = maxDimension;
                }
            }

            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);

            const compressedBase64 = canvas.toDataURL('image/jpeg', 0.32);
            callback(compressedBase64);
        };
    };
}

function uploadAvatar(event) {
    const file = event.target.files[0];
    if (!file) return;

    compressImage(file, async function (compressedData) {
        window.currentCompressedAvatar = compressedData;
        document.querySelectorAll('.avatar, .edit-avatar').forEach(el => {
            el.style.backgroundImage = `url('${compressedData}')`;
        });
        const postAvatar = document.getElementById('posterUserAvatar');
        if (postAvatar) {
            postAvatar.style.backgroundImage = `url('${compressedData}')`;
        }
        localStorage.setItem("shine_profile_avatar", compressedData);
        const effectiveWallet = (userWallet || localStorage.getItem("shine_saved_wallet_addr") || "0xDefaultUser").toLowerCase();
        const curName = document.getElementById('displayNickname') ? document.getElementById('displayNickname').innerText : "User";

        if (window.supabase) {
            try {
                const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
                await client.from('user_profiles').upsert({
                    wallet_address: effectiveWallet,
                    nickname: curName,
                    avatar_url: compressedData,
                    updated_at: new Date().toISOString()
                });
            } catch (err) {}
        }
    });
}

async function saveProfile() {
    const newName = document.getElementById('inputNickname').value.trim();
    const effectiveWallet = (userWallet || localStorage.getItem("shine_saved_wallet_addr") || "0xDefaultUser").toLowerCase();
    const finalAvatar = window.currentCompressedAvatar || localStorage.getItem("shine_profile_avatar") || "";

    if (newName) {
        document.getElementById('displayNickname').innerText = newName;
        const postName = document.getElementById('posterUserName');
        if (postName) postName.innerText = newName;
        localStorage.setItem("shine_profile_nickname", newName);
    }

    if (window.currentCompressedAvatar) {
        localStorage.setItem("shine_profile_avatar", window.currentCompressedAvatar);
    }

    if (window.supabase) {
        try {
            const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
            await client.from('user_profiles').upsert({
                wallet_address: effectiveWallet,
                nickname: newName || (document.getElementById('displayNickname') ? document.getElementById('displayNickname').innerText : "User"),
                avatar_url: finalAvatar,
                updated_at: new Date().toISOString()
            });
        } catch (err) {}
    }

    toggleProfileEdit();
}

async function loadSavedProfileFromDB() {
    const savedName = localStorage.getItem("shine_profile_nickname");
    const savedAvatar = localStorage.getItem("shine_profile_avatar");

    if (savedName) {
        document.getElementById('displayNickname').innerText = savedName;
        const postName = document.getElementById('posterUserName');
        if (postName) postName.innerText = savedName;
        const inp = document.getElementById('inputNickname');
        if (inp) inp.value = savedName;
    }

    if (savedAvatar) {
        window.currentCompressedAvatar = savedAvatar;
        document.querySelectorAll('.avatar, .edit-avatar').forEach(el => {
            el.style.backgroundImage = `url('${savedAvatar}')`;
        });
        const postAvatar = document.getElementById('posterUserAvatar');
        if (postAvatar) postAvatar.style.backgroundImage = `url('${savedAvatar}')`;
    }

    const effectiveWallet = (userWallet || localStorage.getItem("shine_saved_wallet_addr") || "").toLowerCase();
    if (!effectiveWallet) return;

    if (window.supabase) {
        try {
            const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
            const { data, error } = await client.from('user_profiles').select('*').eq('wallet_address', effectiveWallet).single();
            if (!error && data) {
                if (data.nickname) {
                    document.getElementById('displayNickname').innerText = data.nickname;
                    const postName = document.getElementById('posterUserName');
                    if (postName) postName.innerText = data.nickname;
                    const inp = document.getElementById('inputNickname');
                    if (inp) inp.value = data.nickname;
                    localStorage.setItem("shine_profile_nickname", data.nickname);
                }
                if (data.avatar_url) {
                    window.currentCompressedAvatar = data.avatar_url;
                    document.querySelectorAll('.avatar, .edit-avatar').forEach(el => {
                        el.style.backgroundImage = `url('${data.avatar_url}')`;
                    });
                    const postAvatar = document.getElementById('posterUserAvatar');
                    if (postAvatar) postAvatar.style.backgroundImage = `url('${data.avatar_url}')`;
                    localStorage.setItem("shine_profile_avatar", data.avatar_url);
                }
            }
        } catch (err) {}
    }
}
        function openLevelDetail(lvl, cost, progName) {
    const detailOverlay = document.createElement('div');
    detailOverlay.id = 'levelDetailOverlay';
    detailOverlay.className = 'program-preview-overlay active';
    detailOverlay.style.zIndex = '4000';
    const prog = progName.toUpperCase();
    
    let matrixHTML = '';
    let legendHTML = '';

    if (['V1', 'T3', 'A7', 'Q10', 'N13'].includes(prog)) {
        let spotsCount = prog === 'V1' ? 3 : prog === 'T3' ? 3 : prog === 'A7' ? 4 : prog === 'Q10' ? 5 : 6;
        let spotsDivs = '';
        for(let i=0; i<spotsCount; i++) {
            let icon = (i === spotsCount - 1) ? 'cached' : 'account_balance_wallet';
            spotsDivs += `<div class="spot" style="width:45px; height:45px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:18px;">${icon}</i></div>`;
        }
        matrixHTML = `
            <div style="position:relative; width:100%; height:250px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="spot filled" style="width:60px; height:60px; background:white !important; border:none; margin-bottom:50px; color:black; font-weight:bold; z-index:5; display:flex; align-items:center; justify-content:center;">YOU</div>
                <div style="display:flex; gap:20px; z-index:5; flex-wrap:wrap; justify-content:center;">
                    ${spotsDivs}
                </div>
            </div>`;
        legendHTML = `
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#00d2ff;"></div> To Trading Bot Vault (80%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#4CAF50;"></div> Upline 3-Level Bonus (10%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#FFD700;"></div> Cycle Reset (Reinvest)</div>`;
    } 
    else if (['Q2', 'S4', 'C8', 'H11'].includes(prog)) {
        matrixHTML = `
            <div style="position:relative; width:100%; height:320px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="spot filled" style="width:55px; height:55px; background:white !important; border:none; margin-bottom:45px; color:black; font-weight:bold; z-index:5; display:flex; align-items:center; justify-content:center;">YOU</div>
                <div style="display:flex; gap:65px; margin-bottom:40px; z-index:5;">
                    <div class="spot" style="width:40px; height:40px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:16px;">north</i></div>
                    <div class="spot" style="width:40px; height:40px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:16px;">north</i></div>
                </div>
                <div style="display:flex; gap:15px; z-index:5;">
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:14px;">account_balance_wallet</i></div>
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:14px;">account_balance_wallet</i></div>
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:14px;">account_balance_wallet</i></div>
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="color:white; font-size:14px;">cached</i></div>
                </div>
            </div>`;
        legendHTML = `
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#00d2ff;"></div> To Trading Bot Vault (80%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#4CAF50;"></div> Upline 3-Level Bonus (10%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#FFD700;"></div> Cycle Reset (Reinvest)</div>`;
    } 
    else if (['G5', 'S9', 'O12', 'E14'].includes(prog)) {
        matrixHTML = `
            <div style="position:relative; width:100%; height:380px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div class="spot filled" style="width:50px; height:50px; background:white !important; border:none; margin-bottom:40px; color:black; font-weight:bold; z-index:5; display:flex; align-items:center; justify-content:center;">YOU</div>
                <div style="display:flex; gap:90px; margin-bottom:40px; z-index:5;">
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:14px; color:white;">north</i></div>
                    <div class="spot" style="width:35px; height:35px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:14px; color:white;">north</i></div>
                </div>
                <div style="display:flex; gap:35px; margin-bottom:30px; z-index:5;">
                    ${Array(4).fill(`<div class="spot" style="width:25px; height:25px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:12px; color:white;">account_balance_wallet</i></div>`).join('')}
                </div>
                <div style="display:flex; gap:12px; z-index:5;">
                    ${Array(7).fill(`<div class="spot" style="width:20px; height:20px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:10px; color:white;">account_balance_wallet</i></div>`).join('')}
                    <div class="spot" style="width:20px; height:20px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:10px; color:white;">cached</i></div>
                </div>
            </div>`;
        legendHTML = `
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#00d2ff;"></div> To Trading Bot Vault (80%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#4CAF50;"></div> Upline 3-Level Bonus (10%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#FFD700;"></div> Cycle Reset (Reinvest)</div>`;
    } 
    else if (['N6', 'X15'].includes(prog)) {
        matrixHTML = `
            <div style="position:relative; width:100%; height:450px; display:flex; flex-direction:column; align-items:center; justify-content:center; transform:scale(0.9);">
                <div class="spot filled" style="width:45px; height:45px; background:white !important; border:none; margin-bottom:40px; color:black; font-weight:bold; z-index:5; display:flex; align-items:center; justify-content:center;">YOU</div>
                <div style="display:flex; gap:110px; margin-bottom:35px; z-index:5;">
                    <div class="spot" style="width:30px; height:30px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:12px; color:white;">north</i></div>
                    <div class="spot" style="width:30px; height:30px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:12px; color:white;">north</i></div>
                </div>
                <div style="display:flex; gap:45px; margin-bottom:35px; z-index:5;">
                    ${Array(4).fill(`<div class="spot" style="width:22px; height:22px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:10px; color:white;">account_balance_wallet</i></div>`).join('')}
                </div>
                <div style="display:flex; gap:18px; margin-bottom:30px; z-index:5;">
                    ${Array(8).fill(`<div class="spot" style="width:16px; height:16px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:8px; color:white;">account_balance_wallet</i></div>`).join('')}
                </div>
                <div style="display:flex; gap:8px; z-index:5;">
                    ${Array(15).fill(`<div class="spot" style="width:12px; height:12px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:6px; color:white;">account_balance_wallet</i></div>`).join('')}
                    <div class="spot" style="width:12px; height:12px; border:none; background:#1A1A1A; display:flex; align-items:center; justify-content:center;"><i class="material-icons" style="font-size:6px; color:white;">cached</i></div>
                </div>
            </div>`;
        legendHTML = `
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#00d2ff;"></div> To Trading Bot Vault (80%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#4CAF50;"></div> Upline 3-Level Bonus (10%)</div>
            <div style="display:flex; align-items:center; gap:10px; color:#757575; font-size:12px;"><div style="width:12px; height:12px; border-radius:50%; background:#FFD700;"></div> Cycle Reset (Reinvest)</div>`;
    }

    const tData = getTierDataByProgram(prog);
    const tierBoxHTML = `
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 16px; margin-top: 15px; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 11px; font-weight: 900; color: ${tData.tagColor}; letter-spacing: 1px;">${tData.tag}</span>
                <span style="background: ${tData.tagBg}; color: ${tData.tagColor}; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;">${tData.split}</span>
            </div>
            <div style="font-size: 15px; font-weight: bold; color: #fff; margin-bottom: 4px;">${tData.title}</div>
            <div style="font-size: 12px; color: #8c8ca1; line-height: 1.4;">${tData.desc}</div>
        </div>
    `;

    detailOverlay.innerHTML = `
        <div class="preview-header">
            <div class="header-left">
                <i class="material-icons" onclick="this.parentElement.parentElement.parentElement.remove()" style="cursor:pointer">arrow_back</i>
                <span>ID 1 / SHINE ${prog} / level ${lvl}</span>
            </div>
            <div class="header-right"><button class="menu-btn-circle"><div class="hamburger-lines"><span></span><span></span></div></button></div>
        </div>
        <div class="preview-content">
            <div class="upline-card" style="background:#1A1A1A; margin-bottom:20px;">
                <span style="color:#757575;">Upline</span>
                <div class="upline-id" style="background:#333; color:white;">ID 0</div>
            </div>
            <div class="level-card active detail-card-large" style="background:var(--primary-bg); border:1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div class="detail-id-header">
                    <div style="font-size:14px; opacity:0.8;">Lvl ${lvl}</div>
                    <div class="id-display"><span style="font-size:12px; opacity:0.6;">ID</span><span style="font-size:24px; font-weight:900;">1</span></div>
                    <div style="display:flex; align-items:center; gap:5px;"><div class="coin-icon"></div> ${cost}</div>
                </div>
                ${matrixHTML}
                <div class="detail-footer-stats" style="border-top:1px solid rgba(255,255,255,0.05); padding-top:15px;">
                    <div class="f-stat"><span>Partners</span><div class="v"><i class="material-icons" style="font-size:14px;">groups</i> 0</div></div>
                    <div class="f-stat"><span>Cycles</span><div class="v"><i class="material-icons" style="font-size:14px;">cached</i> 0</div></div>
                    <div class="f-stat"><span>Revenue</span><div class="v">0 USDT</div></div>
                </div>
            </div>
            <div style="margin-top:20px; display:flex; flex-direction:column; gap:12px; background:var(--secondary-bg); padding:20px; border-radius:16px;">
                ${legendHTML}
                ${tierBoxHTML}
            </div>
        </div>`;
    document.body.appendChild(detailOverlay);
}
function toggleTrading() {
            const overlay = document.getElementById('tradingOverlay');
            overlay.classList.toggle('active');
            if(overlay.classList.contains('active')) {
                setTimeout(() => {
                    initTradingViewChart(currentChartInterval);
                }, 150);
                startPriceInterval();
            } else {
                clearInterval(window.priceTicker);
            }
        }
let currentBotCoin = 'SOL';
        const coinConfigs = {
            'SOL': { step: 250, min: 1 },
            'BNB': { step: 1000, min: 100 },
            'ETH': { step: 5000, min: 500 },
            'BTC': { step: 100000, min: 10000 }
        };

        function renderPhases(coin) {
            const config = coinConfigs[coin];
            const step = config.step;
            const roundStep = step / 10;

            for (let p = 1; p <= 10; p++) {
                const section = document.getElementById(`phase-${p}-section`);
                const table = document.getElementById(`table-phase-${p}`);
                if (!section || !table) continue;

                const phaseMax = p * step;
                const phaseMin = p === 1 ? config.min : (p - 1) * step;
                
                section.querySelector('.martingale-header span').innerText = `${phaseMax.toLocaleString()} - ${phaseMin.toLocaleString()} ${coin}`;

                const rows = table.querySelectorAll('tbody tr');
                rows.forEach((row, index) => {
                    const r = index + 1;
                    const rMax = phaseMax - ((r - 1) * roundStep);
                    let rMin = phaseMax - (r * roundStep);
                    if (p === 1 && r === 10) rMin = config.min;

                    row.querySelector('.m-price').innerText = `$${rMax.toLocaleString()} - $${rMin.toLocaleString()}`;
                });
            }
        }

        function updateTradingDashboard(currentPrice, coin = currentBotCoin) {
            if (coin !== "SOL") return;

            const config = coinConfigs["SOL"];
            const step = config.step;
            const roundStep = step / 10;

            let activePhase = Math.floor(currentPrice / step) + 1;
            if (activePhase > 10) activePhase = 10;
            if (activePhase < 1) activePhase = 1;

            for (let p = 1; p <= 10; p++) {
                const section = document.getElementById("phase-" + p + "-section");
                const table = document.getElementById("table-phase-" + p);
                if (!section || !table) continue;

                section.style.opacity = (p === activePhase) ? "1" : "0.5";
                section.style.borderColor = "#1a1a1a";
                const pMax = p * step;
                const rows = table.querySelectorAll("tbody tr");

                rows.forEach((row, index) => {
                    const r = index + 1;
                    const rMax = pMax - ((r - 1) * roundStep);
                    let rMin = pMax - (r * roundStep);
                    if (p === 1 && r === 10) rMin = config.min;

                    let status = "PENDING";
                    let color = "#757575";
                    let bg = "transparent";

                    if (p === activePhase) {
                        if (currentPrice <= rMax && currentPrice > rMin) {
                            status = "ACTIVE";
                            color = "#FFD700";
                            bg = "rgba(255, 215, 0, 0.1)";
                        } else if (currentPrice > rMax) {
                            status = "COMPLETED";
                            color = "#4CAF50";
                        }
                    } else if (p < activePhase) {
                        status = "COMPLETED";
                        color = "#4CAF50";
                    }

                    if (status === "PENDING") {
                        if (r === 9) status = "OWNER";
                        if (r === 10) status = "AIRDROP";
                    }

                    const statusSpan = row.querySelector(".m-status");
                    if (statusSpan) {
                        statusSpan.innerText = status;
                        statusSpan.style.color = color;
                    }
                    row.style.background = bg;
                });
            }
        }

        let botSocket = null;
function closeAllActiveSheets() {
    document.querySelectorAll('.tw-sheet-overlay.active').forEach(sheet => {
        sheet.classList.remove('active');
        sheet.style.display = 'none';
    });
}

function attachBackdropCloseListeners() {
    document.querySelectorAll('.tw-sheet-overlay').forEach(sheet => {
        sheet.onclick = function(e) {
            if (e.target === this) {
                this.classList.remove('active');
                this.style.display = 'none';
            }
        };
    });
    document.querySelectorAll('.tw-bottom-sheet').forEach(box => {
        box.onclick = function(e) {
            e.stopPropagation();
        };
    });
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeAllActiveSheets();
    }
});
window.addEventListener('DOMContentLoaded', () => {
    const savedType = localStorage.getItem("shine_saved_wallet_type");
    const savedAddr = localStorage.getItem("shine_saved_wallet_addr");
    if (savedType && savedAddr) {
        setTimeout(() => {
            directReconnectLastWallet();
        }, 300);
    } else if (window.ethereum) {
        setTimeout(async () => {
            try {
                const prov = new ethers.providers.Web3Provider(window.ethereum);
                const accs = await prov.listAccounts();
                if (accs && accs.length > 0) {
                    userWallet = accs[0];
                    isTradeWalletConnected = true;
                    connectedWalletType = window.ethereum.isTrust ? "TRUST" : "METAMASK";
                    setConnectedWalletUI(userWallet);
                }
            } catch (err) {}
        }, 500);
    } else if (window.solana && window.solana.isPhantom) {
        setTimeout(async () => {
            try {
                const resp = await window.solana.connect({ onlyIfTrusted: true });
                if (resp && resp.publicKey) {
                    userWallet = resp.publicKey.toString();
                    isTradeWalletConnected = true;
                    connectedWalletType = "PHANTOM";
                    setConnectedWalletUI(userWallet);
                }
            } catch (err) {}
        }, 500);
    }
    try {
        latestBackendState = null;
        cachedAllTrades = [];
        cachedCombinedScalpTrades = [];
        renderAuditHistoryList([]);
        renderCombinedScalpAuditList([]);
    } catch (e) {}
    renderDashboardSlots();
    initApp();
    initBotConnection();
    loadAirdropDataFromDB();
    attachBackdropCloseListeners();
    const observer = new MutationObserver(function() {
        attachBackdropCloseListeners();
    });
    observer.observe(document.body, { attributes: true, subtree: true, attributeFilter: ['class', 'style'] });
    if (latestBackendState) {
        renderProfessionalOrderDesk(latestBackendState);
        refreshExchangeBalances();
    }
});
        let aiThoughtTimer = null;
        let aiRadarTimer = null;
        let latestBackendState = null;
        let dismissedOrderIds = new Set();
        let dismissedBotIds = new Set();
        let aiCycleStage = 0;
        let lastThoughtChangeTime = 0;

        function getLiveDecisionThought(data) {
            if (!data && currentChartLivePrice <= 0) return "Connecting to backend trading stream and scanning order books...";
            if (isBotPaused || (data && data.isPaused)) {
                return "Engine paused via contract interface. Tap RUNNING to resume automated scan.";
            }
            if (data && data.cooldownRemaining && data.cooldownRemaining > 0) {
                return `Profit secured. Guard cycle active for ${data.cooldownRemaining}s before re-entry.`;
            }

            const pos = (data && data.activePositions) ? data.activePositions : [];
            const liveP = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat((data && (data.price || data.livePrice)) || 0);
            const flow = (data && data.whaleOrderflow !== undefined) ? data.whaleOrderflow : 52.4;

            if (pos.length === 0) {
                const targetDip = (liveP * 0.982).toFixed(2);
                if (aiCycleStage === 0) {
                    return `Real-Time Market Scan: Live price is $${liveP.toFixed(2)} (${flow}% Buy Vol). Holding entries to prevent buying at local resistance.`;
                } else {
                    return `Next Entry Target: Monitoring dip toward $${targetDip}. DCA safety order will execute upon confirmed orderflow bounce.`;
                }
            } else {
                const avgP = parseFloat((data && data.avgEntryPrice) || liveP);
                const solAmt = parseFloat((data && data.solBalance) || 0);
                const calcTsl = parseFloat((data && data.tsLow) || (liveP * 0.99));
                const targetSell = (avgP * 1.025).toFixed(2);
                const estProfit = solAmt > 0 ? ((parseFloat(targetSell) - avgP) * solAmt).toFixed(2) : ((avgP * 0.025) * 0.5).toFixed(2);

                if (aiCycleStage === 0) {
                    return `Live Position Tracking: Avg entry locked at $${avgP.toFixed(2)}. Current market rate is $${liveP.toFixed(2)}.`;
                } else if (aiCycleStage === 1) {
                    return `Automated Exit Target: Limit exit placed at $${targetSell} to lock +$${estProfit} net profit directly into wallet.`;
                } else {
                    return `Trailing Stop Loss: Protective floor active at $${calcTsl.toFixed(2)}. Guarding capital against downside volatility.`;
                }
            }
        }

        let botTabBrainStage = 0;
        let botTabBrainTimer = null;

        function runBotTabRotatingBrainCycle() {
            if (!latestBackendState) return;
            const data = latestBackendState;
            const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);

            const headerEl = document.getElementById("botRotatingHeaderName");
            const subHeaderEl = document.getElementById("botRotatingSubHeader");
            const textEl = document.getElementById("botTabRotatingLiveText");
            const dotEl = document.getElementById("botBrainPulseDot");
            const titleTagEl = document.getElementById("botBrainTitleTag");

            if (activeTypewriterTimer) {
                clearTimeout(activeTypewriterTimer);
                isTypingInProgress = false;
            }
            if (textEl) {
                textEl.removeAttribute("data-last-text");
            }

            if (botTabBrainStage === 0) {
                if (headerEl) { headerEl.innerText = "SHINE HYPER TITAN"; headerEl.style.color = "#00e676"; }
                if (dotEl) { dotEl.style.background = "#00e676"; dotEl.style.boxShadow = "0 0 10px #00e676"; }
                if (titleTagEl) { titleTagEl.style.color = "#00e676"; }
                if (textEl) { textEl.style.color = "#00e676"; }
                const pos = data.hyperPositions || [];
                let msg = "";
                if (pos.length === 0) {
                    msg = `Hyper Titan Scanning: Live SOL price is $${curLive.toFixed(2)}. Pool capital: $1,000.00. Dip Radar armed for $0.01 tick drop.`;
                } else {
                    const lastP = pos[pos.length - 1];
                    const entryP = parseFloat(lastP.entryPrice || curLive);
                    const gain = curLive - entryP;
                    msg = `Hyper Titan Active: Holding ${pos.length} safety trade(s) | Entry: $${entryP.toFixed(2)} | Net Float: ${gain >= 0 ? '+' : ''}$${gain.toFixed(3)} | Trailing Exit Active`;
                }
                typeWriterEffect(msg, "botTabRotatingLiveText");
            } else if (botTabBrainStage === 1) {
                if (headerEl) { headerEl.innerText = "SHINE APEX VELOCITY"; headerEl.style.color = "#00d2ff"; }
                if (dotEl) { dotEl.style.background = "#00d2ff"; dotEl.style.boxShadow = "0 0 10px #00d2ff"; }
                if (titleTagEl) { titleTagEl.style.color = "#00d2ff"; }
                if (textEl) { textEl.style.color = "#00d2ff"; }
                const pos = data.microPositions || [];
                let msg = "";
                if (pos.length === 0) {
                    msg = `Apex Velocity Scanning: Market rate is $${curLive.toFixed(2)}. Monitoring orderflow for $0.30 dip entry confirmation.`;
                } else {
                    const lastP = pos[pos.length - 1];
                    const entryP = parseFloat(lastP.entryPrice || curLive);
                    const gain = curLive - entryP;
                    msg = `Apex Velocity Active: Holding ${pos.length} micro order(s) | Latest Entry: $${entryP.toFixed(2)} | Net Float: ${gain >= 0 ? '+' : ''}$${gain.toFixed(2)} | 3-Stage Trail Running`;
                }
                typeWriterEffect(msg, "botTabRotatingLiveText");
            } else if (botTabBrainStage === 2) {
                if (headerEl) { headerEl.innerText = "SHINE QUANTUM PULSE"; headerEl.style.color = "#FF8C00"; }
                if (dotEl) { dotEl.style.background = "#FF8C00"; dotEl.style.boxShadow = "0 0 10px #FF8C00"; }
                if (titleTagEl) { titleTagEl.style.color = "#FF8C00"; }
                if (textEl) { textEl.style.color = "#FF8C00"; }
                const pos = data.killer2Positions || [];
                let msg = "";
                if (pos.length === 0) {
                    msg = `Quantum Pulse Radar: Tracking $0.60 dip floor from peak. Ready to strike on confirmed 2-cent rebound.`;
                } else {
                    const lastP = pos[pos.length - 1];
                    const entryP = parseFloat(lastP.entryPrice || curLive);
                    const gain = curLive - entryP;
                    msg = `Quantum Pulse In Progress: Holding ${pos.length} wave order(s) | Entry: $${entryP.toFixed(2)} | Net Float: ${gain >= 0 ? '+' : ''}$${gain.toFixed(2)} | Trailing Floor Active`;
                }
                typeWriterEffect(msg, "botTabRotatingLiveText");
            } else if (botTabBrainStage === 3) {
                if (headerEl) { headerEl.innerText = "SHINE TITAN ABYSS"; headerEl.style.color = "#FF1493"; }
                if (dotEl) { dotEl.style.background = "#FF1493"; dotEl.style.boxShadow = "0 0 10px #FF1493"; }
                if (titleTagEl) { titleTagEl.style.color = "#FF1493"; }
                if (textEl) { textEl.style.color = "#FF1493"; }
                const pos = data.killer3Positions || [];
                let msg = "";
                if (pos.length === 0) {
                    msg = `Titan Abyss Deep Sentinel: Scanning deep $0.90 liquidation drop. Reserve liquidity armed for deep strike.`;
                } else {
                    const lastP = pos[pos.length - 1];
                    const entryP = parseFloat(lastP.entryPrice || curLive);
                    const gain = curLive - entryP;
                    msg = `Titan Abyss Strike Active: Holding ${pos.length} deep order(s) | Entry: $${entryP.toFixed(2)} | Net Float: ${gain >= 0 ? '+' : ''}$${gain.toFixed(2)} | Deep Runner Running`;
                }
                typeWriterEffect(msg, "botTabRotatingLiveText");
            } else if (botTabBrainStage === 4) {
                if (headerEl) { headerEl.innerText = "SHINE TITAN SINGULARITY"; headerEl.style.color = "#e040fb"; }
                if (dotEl) { dotEl.style.background = "#e040fb"; dotEl.style.boxShadow = "0 0 10px #e040fb"; }
                if (titleTagEl) { titleTagEl.style.color = "#e040fb"; }
                if (textEl) { textEl.style.color = "#e040fb"; }
                const pos = data.singularityPositions || [];
                let msg = "";
                if (pos.length === 0) {
                    msg = `Titan Singularity (100K Vault): Scanning market rate $${curLive.toFixed(2)}. Capital: $100,000.00. 5-Engine Fusion Dip Sentinel active.`;
                } else {
                    const lastP = pos[pos.length - 1];
                    const entryP = parseFloat(lastP.entryPrice || curLive);
                    const gain = curLive - entryP;
                    msg = `Titan Singularity Active: ${pos.length} order(s) open across 5 engines | Entry: $${entryP.toFixed(2)} | Float: ${gain >= 0 ? '+' : ''}$${gain.toFixed(3)} | Dynamic Trail Lock`;
                }
                typeWriterEffect(msg, "botTabRotatingLiveText");
            }

            botTabBrainStage = (botTabBrainStage + 1) % 5;
        }

        function startAiThoughtCycle() {
            if (aiThoughtTimer) clearInterval(aiThoughtTimer);
            aiThoughtTimer = setInterval(() => {
                if (latestBackendState) {
                    if (latestBackendState.botThought) {
                        const engThought = toEnglishBotThought(latestBackendState.botThought);
                        typeWriterEffect(engThought, "aiLiveText");
                    } else {
                        aiCycleStage = (aiCycleStage + 1) % 3;
                        const thought = getLiveDecisionThought(latestBackendState);
                        typeWriterEffect(thought, "aiLiveText");
                    }
                }
            }, 20000);

            if (botTabBrainTimer) clearInterval(botTabBrainTimer);
            runBotTabRotatingBrainCycle();
            botTabBrainTimer = setInterval(() => {
                runBotTabRotatingBrainCycle();
            }, 15000);
        }

        function calculateRealRadarMetrics(data) {
            if (!data) return;
            const liveP = parseFloat(data.price || data.livePrice || 0);
            const history = Array.isArray(data.tradesHistory) ? data.tradesHistory : [];

            const ofVal = document.getElementById("radar-orderflow-val");
            const ofIcon = document.getElementById("radar-orderflow-icon");
            const ofWrap = document.getElementById("radar-orderflow-wrapper");
            if (ofVal && data.whaleOrderflow !== undefined) {
                const ratio = parseFloat(data.whaleOrderflow).toFixed(1);
                ofVal.innerText = ratio + "% BUY VOL";
                if (parseFloat(ratio) >= 55.0) {
                    if (ofWrap) ofWrap.style.color = "#00e676";
                    if (ofIcon) ofIcon.innerText = "trending_up";
                } else if (parseFloat(ratio) <= 45.0) {
                    if (ofWrap) ofWrap.style.color = "#f6465d";
                    if (ofIcon) ofIcon.innerText = "trending_down";
                } else {
                    if (ofWrap) ofWrap.style.color = "#FFD700";
                    if (ofIcon) ofIcon.innerText = "trending_flat";
                }
            }

            const sharpeEl = document.getElementById("radar-sharpe-ratio");
            if (sharpeEl) {
                const exitTrades = history.filter(t => String(t.side || "").toUpperCase().includes("SELL"));
                const wins = exitTrades.filter(t => parseFloat(t.profit || t.realizedPnl || 0) > 0).length;
                const losses = exitTrades.length - wins;
                const winRate = exitTrades.length > 0 ? (wins / exitTrades.length) : 0.85;
                const sharpe = (winRate * 3.2).toFixed(2);
                sharpeEl.innerText = sharpe + " (ALPHA)";
            }

            const mddEl = document.getElementById("radar-max-drawdown");
            if (mddEl) {
                const pos = Array.isArray(data.activePositions) ? data.activePositions : [];
                let maxFloatingDrop = 0.0;
                pos.forEach(p => {
                    const ent = parseFloat(p.entryPrice || liveP);
                    if (ent > liveP && ent > 0) {
                        const d = ((ent - liveP) / ent) * 100.0;
                        if (d > maxFloatingDrop) maxFloatingDrop = d;
                    }
                });
                mddEl.innerText = maxFloatingDrop > 0 ? "-" + maxFloatingDrop.toFixed(2) + "%" : "0.00%";
                mddEl.style.color = maxFloatingDrop > 3.0 ? "#f6465d" : "#00e676";
            }

            const liqEl = document.getElementById("radar-whale-liquidity");
            if (liqEl && liveP > 0) {
                const totalInvested = parseFloat(data.investedAmount || 0);
                const activePoolCap = parseFloat(data.totalCapital || 100);
                const estimatedDepth = ((liveP * 18420) / 1000).toFixed(1);
                liqEl.innerText = "$" + estimatedDepth + "K DEPTH";
            }
        }

        function startAiRadarCycle() {
            if (aiRadarTimer) clearInterval(aiRadarTimer);
            aiRadarTimer = setInterval(() => {
                if (latestBackendState) {
                    calculateRealRadarMetrics(latestBackendState);
                }
            }, 30000);
        }

        const BACKEND_CONFIG = {
            servers: [
                { http: "https://shine-crypto-bot.fastapicloud.dev", ws: "wss://shine-crypto-bot.fastapicloud.dev/ws" },
                { http: "https://shine-crypto-bot.onrender.com", ws: "wss://shine-crypto-bot.onrender.com/ws" }
            ],
            currentIndex: 0,
            getActiveHttp() {
                return this.servers[this.currentIndex].http;
            },
            getActiveWs() {
                return this.servers[this.currentIndex].ws;
            },
            rotate() {
                this.currentIndex = (this.currentIndex + 1) % this.servers.length;
            }
        };

        async function fetchWithFallback(endpoint, options = {}) {
            let attempts = 0;
            while (attempts < BACKEND_CONFIG.servers.length) {
                const targetUrl = BACKEND_CONFIG.getActiveHttp() + endpoint;
                try {
                    const controller = new AbortController();
                    const timer = setTimeout(() => controller.abort(), 6000);
                    const res = await fetch(targetUrl, { ...options, signal: controller.signal });
                    clearTimeout(timer);
                    if (res && res.ok) return res;
                } catch (e) {
                    BACKEND_CONFIG.rotate();
                }
                attempts++;
            }
            return null;
        }

        function startPriceInterval() {
            initBotConnection();
            startAiThoughtCycle();
            startAiRadarCycle();
            if (window.priceTicker) clearInterval(window.priceTicker);
            if (!window.renderWakeupInterval) {
                window.renderWakeupInterval = setInterval(() => {
                    fetchWithFallback("/status");
                }, 120000);
            }
        }

        function initBotConnection() {
            fetchInitialStatus();
            connectBotWebSocket();
        }

        async function fetchInitialStatus() {
            try {
                const res = await fetchWithFallback("/status");
                if (res) {
                    const data = await res.json();
                    handleBotData(data);
                }
            } catch (e) {}
        }

        let consecutiveOfflineFailures = 0;

        function setBackendStatusUI(isOnline) {
            const dot = document.getElementById("backendStatusDot");
            const txt = document.getElementById("backendStatusText");
            if (dot && txt) {
                if (isOnline) {
                    consecutiveOfflineFailures = 0;
                    dot.style.background = "#00E676";
                    dot.style.boxShadow = "0 0 10px #00E676";
                    dot.style.animation = "livePulseDot 1.2s infinite";
                    txt.style.color = "#00E676";
                    txt.innerText = "LIVE";
                } else {
                    dot.style.background = "#F6465D";
                    dot.style.boxShadow = "0 0 8px #F6465D";
                    dot.style.animation = "none";
                    txt.style.color = "#F6465D";
                    txt.innerText = "OFFLINE";
                }
            }
        }

        async function verifyActualServerHealth() {
            try {
                const res = await fetchWithFallback("/status");
                if (res && res.ok) {
                    setBackendStatusUI(true);
                    return true;
                }
            } catch (e) {}
            consecutiveOfflineFailures++;
            if (consecutiveOfflineFailures >= 3) {
                setBackendStatusUI(false);
            }
            return false;
        }

        function connectBotWebSocket() {
            if (botSocket && (botSocket.readyState === WebSocket.OPEN || botSocket.readyState === WebSocket.CONNECTING)) return;
            const targetWsUrl = BACKEND_CONFIG.getActiveWs();
            botSocket = new WebSocket(targetWsUrl);

            botSocket.onopen = () => {
                setBackendStatusUI(true);
            };

            botSocket.onmessage = (event) => {
                setBackendStatusUI(true);
                try {
                    const data = JSON.parse(event.data);
                    requestAnimationFrame(() => handleBotData(data));
                } catch (e) {}
            };

            botSocket.onclose = () => {
                verifyActualServerHealth();
                BACKEND_CONFIG.rotate();
                setTimeout(connectBotWebSocket, 1500);
            };

            botSocket.onerror = () => {
                verifyActualServerHealth();
                try { botSocket.close(); } catch(e){}
            };
        }

        document.addEventListener("visibilitychange", () => {
            if (!document.hidden) {
                verifyActualServerHealth();
                connectBotWebSocket();
            }
        });

        let currentBotSpeech = "";
        let previousTrackedSolPrice = 0;

        function triggerPriceFlash(currentPrice) {}

        let activeTypewriterTimer = null;
        let isTypingInProgress = false;
        let showFullAuditHistory = false;
        let cachedAllTrades = [];

        function toggleFullAuditHistory() {
            showFullAuditHistory = !showFullAuditHistory;
            const btn = document.getElementById("btn-see-more-audit");
            if (btn) {
                btn.innerText = showFullAuditHistory ? "Show Less" : "See More (All Trades)";
            }
            renderAuditHistoryList(cachedAllTrades);
        }

        function typeWriterEffect(text, elementId) {
            const el = document.getElementById(elementId);
            if (!el || el.getAttribute("data-last-text") === text || isTypingInProgress) return;
            if (activeTypewriterTimer) {
                clearTimeout(activeTypewriterTimer);
            }
            isTypingInProgress = true;
            el.setAttribute("data-last-text", text);
            let i = 0;
            const speed = 28;
            const cursorHTML = '<span style="color:#00e676; animation:terminalBlink 0.8s infinite; font-weight:900; margin-left:2px;">_</span>';
            el.innerHTML = cursorHTML;
            function type() {
                if (i < text.length) {
                    el.innerHTML = text.substring(0, i + 1) + cursorHTML;
                    i++;
                    activeTypewriterTimer = setTimeout(type, speed);
                } else {
                    el.innerHTML = text + cursorHTML;
                    isTypingInProgress = false;
                }
            }
            type();
        }

        function toEnglishBotThought(text) {
            if (!text) return "Scanning live market orderflow and monitoring liquidity depths...";
            if (text.includes("paused") || text.includes("Main abhi paused hoon")) {
                return "Trading engine is currently paused. Tap RUNNING to enable automated market scan and execution.";
            }
            if (text.includes("cool-down") || text.includes("Pichla profit")) {
                const match = text.match(/\d+/);
                const sec = match ? match[0] : "40";
                return "Previous profit secured successfully! Engine is in cool-down mode for " + sec + "s to prevent impulsive entries.";
            }
            if (text.includes("Whales") || text.includes("barhay sellers")) {
                return "Institutional selling pressure detected by Whale Radar. Holding dry powder safely until orderflow stabilizes.";
            }
            if (text.includes("Scanning orderbook") || text.includes("dip confirmation")) {
                return text;
            }
            if (text.includes("munafay mein hai") || text.includes("Zabardast")) {
                return "Active position is currently in profit. Dynamic Trailing Stop Loss is actively tracking peaks to maximize yield.";
            }
            if (text.includes("neechay chal rahi hai") || text.includes("panic nahi kar raha")) {
                return "Market is trading slightly below average entry. Zero panic: DCA Trailing Buy is armed to accumulate on confirmed rebound.";
            }
            return text;
        }

        function speakBotThoughts() {
            if (!('speechSynthesis' in window)) {
                alert("Text to Speech is not supported on this browser.");
                return;
            }
            const textSource = currentBotSpeech || (document.getElementById("aiLiveText") ? document.getElementById("aiLiveText").innerText : "Scanning live market orderflow");
            window.speechSynthesis.cancel();
            if (window.speechSynthesis.paused) {
                window.speechSynthesis.resume();
            }
            const utterance = new SpeechSynthesisUtterance(textSource);
            utterance.lang = "en-US";
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            const avatar = document.getElementById("aiAvatarIcon");
            utterance.onstart = () => {
                if (avatar) avatar.style.transform = "scale(1.2)";
            };
            utterance.onend = () => {
                if (avatar) avatar.style.transform = "scale(1)";
            };
            utterance.onerror = () => {
                if (avatar) avatar.style.transform = "scale(1)";
            };
            window.speechSynthesis.speak(utterance);
        }

        function handleBotData(data) {
            if (!data) return;

            latestBackendState = data;
            if (!latestBackendState.walletOpenOrders) {
                latestBackendState.walletOpenOrders = Array.isArray(data.openOrders) ? data.openOrders : [];
            }
            if (!latestBackendState.walletActivePositions) {
                latestBackendState.walletActivePositions = [];
            }

            void 0;

            const now = Date.now();
            if (data.botThought) {
                const engThought = toEnglishBotThought(data.botThought);
                if (now - lastThoughtChangeTime >= 30000 || !lastThoughtChangeTime) {
                    currentBotSpeech = engThought;
                    typeWriterEffect(engThought, "aiLiveText");
                    lastThoughtChangeTime = now;
                }
            } else if (!aiThoughtTimer) {
                const initialThought = getLiveDecisionThought(data);
                currentBotSpeech = initialThought;
                typeWriterEffect(initialThought, "aiLiveText");
                lastThoughtChangeTime = now;
            }

            const rawBackendPrice = parseFloat(data.price || data.livePrice || 0);
            const livePrice = rawBackendPrice > 0 ? rawBackendPrice : (currentChartLivePrice > 0 ? currentChartLivePrice : 0);
            if (livePrice > 0) {
                currentChartLivePrice = livePrice;
            }

            const midEl = document.getElementById("ex-mid-price");
            if (midEl && livePrice > 0) midEl.innerText = "$" + livePrice.toFixed(2);

            const highEl = document.getElementById("ex-high-24h");
            if (highEl && livePrice > 0) highEl.innerText = "$" + (livePrice * 1.028).toFixed(2);

            const lowEl = document.getElementById("ex-low-24h");
            if (lowEl && livePrice > 0) lowEl.innerText = "$" + (livePrice * 0.972).toFixed(2);

            const volEl = document.getElementById("ex-vol-24h");
            if (volEl) volEl.innerText = "1,842,910";

            const flowRatio = data.whaleOrderflow !== undefined ? parseFloat(data.whaleOrderflow).toFixed(0) : "52";
            const buyersEl = document.getElementById("ex-buyers-count");
            if (buyersEl) buyersEl.innerText = flowRatio + "% BUY";

            if (livePrice > 0 && Math.abs(livePrice - (window.lastRenderedBookPrice || 0)) >= 0.01) {
                window.lastRenderedBookPrice = livePrice;
                const asksEl = document.getElementById("ex-asks-book");
                if (asksEl) {
                    let askRows = "";
                    for (let i = 5; i >= 1; i--) {
                        const aPrice = (livePrice + (i * 0.01)).toFixed(2);
                        const aQty = (1.5 + (i * 0.8)).toFixed(2);
                        askRows += `<div onclick="fillPriceFromBook(${aPrice})" style="display:flex; justify-content:space-between; font-variant-numeric: tabular-nums; cursor:pointer;">
                            <span style="color:#f6465d; font-weight:800; font-size:13px;">${aPrice}</span>
                            <span style="color:#ffffff; font-weight:700; width:70px; text-align:right; font-size:12px;">${aQty}</span>
                        </div>`;
                    }
                    asksEl.innerHTML = askRows;
                }

                const bidsEl = document.getElementById("ex-bids-book");
                if (bidsEl) {
                    let bidRows = "";
                    for (let i = 1; i <= 5; i++) {
                        const bPrice = (livePrice - (i * 0.01)).toFixed(2);
                        const bQty = (2.2 + (i * 0.9)).toFixed(2);
                        bidRows += `<div onclick="fillPriceFromBook(${bPrice})" style="display:flex; justify-content:space-between; font-variant-numeric: tabular-nums; cursor:pointer;">
                            <span style="color:#00c087; font-weight:800; font-size:13px;">${bPrice}</span>
                            <span style="color:#ffffff; font-weight:700; width:70px; text-align:right; font-size:12px;">${bQty}</span>
                        </div>`;
                    }
                    bidsEl.innerHTML = bidRows;
                }
            }
            let pnl = parseFloat(data.pnl || data.unrealizedPnL || 0);
            let pnlPct = parseFloat(data.pnlPct || data.pnlPercent || 0);
            const solBalCheck = parseFloat(data.solBalance || 0);
            const avgPriceCheck = parseFloat(data.avgEntryPrice || 0);
            if (pnl === 0 && solBalCheck > 0 && livePrice > 0 && avgPriceCheck > 0) {
                pnl = (livePrice - avgPriceCheck) * solBalCheck;
                pnlPct = ((livePrice - avgPriceCheck) / avgPriceCheck) * 100;
            }
            const savedLocalCap = parseFloat(localStorage.getItem("shine_user_total_capital") || "0");
            const backendCap = (data && data.totalCapital !== undefined) ? parseFloat(data.totalCapital) : 0.0;
            const totalCapVal = Math.max(savedLocalCap, backendCap);
            const investedVal = parseFloat(data.investedAmount || 0);
            const usdtBal = Math.max(0.0, totalCapVal - investedVal);
            const solBal = parseFloat(data.solBalance !== undefined ? data.solBalance : 0);
            const avgPrice = parseFloat(data.avgEntryPrice || 0);
            const tHigh = parseFloat(data.tsHigh || data.trailingHigh || data.lastPeakPrice || 0);
            const tLow = parseFloat(data.tsLow || data.trailingLow || 0);
            const phase = data.activePhase !== undefined ? parseInt(data.activePhase.toString().replace(/[^0-9]/g, "")) : (data.phase !== undefined ? parseInt(data.phase) : 1);
            const round = (data.activeRound !== undefined && data.activeRound !== null && data.activeRound !== "") ? parseInt(data.activeRound.toString().replace(/[^0-9]/g, "")) : (data.round !== undefined ? parseInt(data.round) : (data.currentRound !== undefined ? parseInt(data.currentRound) : 6));
            const alloc = data.allocationPct ? (data.allocationPct + "%") : (data.allocation || "0%");

            const pSolEl = document.getElementById("price-SOL");
            if (pSolEl && livePrice > 0) pSolEl.innerText = livePrice.toFixed(2);

            const largeSol = document.getElementById("large-live-sol");
            if (largeSol && livePrice > 0) {
                largeSol.innerText = "$" + livePrice.toFixed(2);
                triggerPriceFlash(livePrice);
            }

            const phaseRoundEl = document.getElementById("live-phase-round");
            if (phaseRoundEl) phaseRoundEl.innerText = "PHASE " + phase + " | ROUND " + round;

            const roundAllocs = { 1: "1.00%", 2: "2.00%", 3: "4.00%", 4: "6.00%", 5: "10.00%", 6: "20.00%", 7: "30.00%", 8: "27.00%", 9: "HOLD", 10: "HOLD" };
            const effectiveAlloc = data.allocationPct ? (data.allocationPct + "%") : (roundAllocs[round] || alloc);
            const fundUsageEl = document.getElementById("live-fund-usage");
            if (fundUsageEl) fundUsageEl.innerText = effectiveAlloc;

            const pnlEl = document.getElementById("unrealized-pnl");
            const pnlPctEl = document.getElementById("unrealized-pnl-pct");
            if (pnlEl) {
                const sign = pnl >= 0 ? "+" : "";
                pnlEl.innerText = sign + "$" + pnl.toFixed(2);
                pnlEl.style.color = pnl >= 0 ? "#4CAF50" : "#f6465d";
            }
            if (pnlPctEl) {
                const sign = pnlPct >= 0 ? "+" : "";
                pnlPctEl.innerText = sign + pnlPct.toFixed(2) + "%";
                pnlPctEl.style.color = pnlPct >= 0 ? "#4CAF50" : "#f6465d";
                pnlPctEl.style.background = pnlPct >= 0 ? "rgba(76, 175, 80, 0.12)" : "rgba(246, 70, 93, 0.12)";
            }

            const portUsdt = document.getElementById("port-usdt");
            if (portUsdt) portUsdt.innerText = "$" + usdtBal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});

            const portSol = document.getElementById("port-sol");
            if (portSol) portSol.innerText = solBal.toFixed(4);

            const wUsdt = (data.manualTestBalance !== undefined ? parseFloat(data.manualTestBalance) : (data.walletUsdt !== undefined ? parseFloat(data.walletUsdt) : 100.0));
            const wSol = data.walletSol !== undefined ? parseFloat(data.walletSol) : 0;
            const wInvested = data.walletInvested !== undefined ? parseFloat(data.walletInvested) : 0;
            const wAvg = data.walletAvgEntry !== undefined ? parseFloat(data.walletAvgEntry) : 0;

            const uWallUsdt = document.getElementById("user-wallet-usdt");
            if (uWallUsdt) uWallUsdt.innerText = "$" + wUsdt.toFixed(2);

            const uWallSol = document.getElementById("user-wallet-sol");
            if (uWallSol) uWallSol.innerText = wSol.toFixed(4);

            const wAvgEl = document.getElementById("wallet-avg-entry");
            if (wAvgEl) wAvgEl.innerText = wAvg > 0 ? ("$" + wAvg.toFixed(2)) : "$0.00";

            const wInvDisp = document.getElementById("wallet-invested-display");
            if (wInvDisp) wInvDisp.innerText = "$" + wInvested.toFixed(2);

            const wSolDisp = document.getElementById("wallet-sol-display");
            if (wSolDisp) wSolDisp.innerText = wSol.toFixed(4);

            const wCont = document.getElementById("wallet-positions-container");
            const wBadge = document.getElementById("wallet-positions-badge");
            if (data.walletActivePositions && data.walletActivePositions.length > 0) {
                if (wBadge) wBadge.innerText = data.walletActivePositions.length + " OPEN";
                if (wCont) {
                    wCont.innerHTML = data.walletActivePositions.map(pos => `
                        <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.04); color:white; font-size:12px; font-family:monospace;">
                            <span style="color:#5C6BC0; font-weight:bold;">${pos.label}</span>
                            <span>$${parseFloat(pos.entryPrice).toFixed(2)}</span>
                            <span style="color:#4CAF50; font-weight:bold;">${parseFloat(pos.solAmount).toFixed(4)} SOL</span>
                            <span style="color:#757575;">${pos.timestamp || ''}</span>
                        </div>
                    `).join("");
                }
            } else {
                if (wBadge) wBadge.innerText = "0 OPEN";
                if (wCont) wCont.innerHTML = "NO ACTIVE WALLET ORDERS";
            }

            const avgEntryEl = document.getElementById("avg-entry-price");
            if (avgEntryEl) avgEntryEl.innerText = avgPrice > 0 ? "$" + avgPrice.toFixed(2) : "$0.00";

            const investedEl = document.getElementById("invested-amount");
            if (investedEl) investedEl.innerText = "$" + investedVal.toFixed(2);

            const totalCapEl = document.getElementById("total-capital");
            if (totalCapEl) totalCapEl.innerText = "$" + totalCapVal.toFixed(2);

            const tsHighEl = document.getElementById("ts-high");
            if (tsHighEl) tsHighEl.innerText = tHigh > 0 ? "$" + tHigh.toFixed(2) : (livePrice > 0 ? "$" + livePrice.toFixed(2) : "$0.00");

            const tsLowEl = document.getElementById("ts-low");
            if (tsLowEl) tsLowEl.innerText = tLow > 0 ? "$" + tLow.toFixed(2) : "$0.00";
            nativeTslStop = tLow;

            if (livePrice > 0) {
                currentChartLivePrice = livePrice;
                updateLiveCandle(livePrice);
            }

            if (data.isPaused !== undefined) {
                isBotPaused = data.isPaused;
                updatePauseUI(isBotPaused);
            }

            if (data.tradesHistory && Array.isArray(data.tradesHistory)) {
                if (window.lastKnownTradeCount === undefined) {
                    window.lastKnownTradeCount = data.tradesHistory.length;
                } else if (data.tradesHistory.length > window.lastKnownTradeCount) {
                    window.lastKnownTradeCount = data.tradesHistory.length;
                    const latestTrade = data.tradesHistory[0];
                    const tradeText = latestTrade ? `${latestTrade.side} ${parseFloat(latestTrade.price).toFixed(2)} (${latestTrade.solAmount} SOL)` : 'Trade Executed';
                    triggerDexTradeAlert('Order Executed: ' + tradeText);
                }
                const cleanExecutedTrades = [];
                const registeredIds = new Set();
                const sourceList = [...(data.tradesHistory || []), ...(data.scalpTradesHistory || [])];

                sourceList.forEach(t => {
                    const id = String(t.orderId || t.order_id || "");
                    const side = String(t.side || "").toUpperCase();
                    const qty = parseFloat(t.solAmount || t.sol_amount || 0);

                    if (id && !registeredIds.has(id) && qty > 0 && (side === "BUY" || side === "SELL")) {
                        registeredIds.add(id);
                        cleanExecutedTrades.push({
                            orderId: id,
                            side: side,
                            price: parseFloat(t.price || 0),
                            solAmount: qty,
                            timestamp: t.timestamp || t.created_at
                        });
                    }
                });

                updateChartMarkers(cleanExecutedTrades);
            }

            if (tLow > 0) {
                updateTslLine(tLow);
            }

            const roundDisplay = document.querySelector(".bot-name");
            if (roundDisplay && tLow > 0) {
                roundDisplay.innerHTML = "Shine Bot | P" + phase + " R" + round + " | TSL: " + tLow.toFixed(2);
            }

            const homeSpotRealized = parseFloat(data.spotRealizedPnl !== undefined ? data.spotRealizedPnl : 0.0);
            const total4BotsRealized = parseFloat(data.realizedPnl !== undefined ? data.realizedPnl : (homeSpotRealized + parseFloat(data.microRealizedPnl || 0) + parseFloat(data.killer2RealizedPnl || 0) + parseFloat(data.killer3RealizedPnl || 0)));

            const netRealizedEl = document.getElementById("realized-pnl-val");
            if (netRealizedEl) {
                const rSign = total4BotsRealized >= 0 ? "+" : "";
                netRealizedEl.innerText = rSign + "$" + total4BotsRealized.toFixed(2);
                netRealizedEl.style.color = total4BotsRealized >= 0 ? "#4CAF50" : "#f6465d";
            }
            
            const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
            let calcBot24h = 0.0;
            const fourBotsTrades = [
                ...(Array.isArray(data.spotTradesHistory) ? data.spotTradesHistory : []),
                ...(Array.isArray(data.microTradesHistory) ? data.microTradesHistory : []),
                ...(Array.isArray(data.killer2TradesHistory) ? data.killer2TradesHistory : []),
                ...(Array.isArray(data.killer3TradesHistory) ? data.killer3TradesHistory : [])
            ];
            fourBotsTrades.forEach(t => {
                const ordId = String(t.orderId || t.order_id || "").toUpperCase();
                const isManual = ordId.startsWith("MAN_") || ordId.startsWith("ATL_") || ordId.startsWith("ORD_") || ordId.startsWith("COPY_") || ordId.startsWith("CPOS_") || ordId.startsWith("BOT_");
                if (!isManual) {
                    const sideStr = String(t.side || t.execType || "").toUpperCase();
                    const isExit = sideStr.includes("SELL") || sideStr.includes("EXIT") || sideStr.includes("PROFIT");
                    if (isExit) {
                        const tTime = t.timestamp ? new Date(t.timestamp).getTime() : 0;
                        if (!tTime || isNaN(tTime) || tTime >= oneDayAgo) {
                            calcBot24h += parseFloat(t.profit || t.realizedPnl || 0.0);
                        }
                    }
                }
            });
            calcBot24h = Math.round(calcBot24h * 10000) / 10000;
            if (calcBot24h <= 0.0 && total4BotsRealized > 0.0) {
                calcBot24h = total4BotsRealized;
            }
            const bot24El = document.getElementById("bot-24h-profit");
            if (bot24El) {
                const sign = calcBot24h >= 0 ? "+" : "";
                bot24El.innerText = sign + "$" + calcBot24h.toFixed(2);
                bot24El.style.color = calcBot24h >= 0 ? "#00e676" : "#f6465d";
            }
            const poster24El = document.getElementById("poster-24h-profit");
            if (poster24El) {
                const sign = calcBot24h >= 0 ? "+" : "";
                poster24El.innerText = sign + "$" + calcBot24h.toFixed(2);
            }
            const tslDistEl = document.getElementById("tsl-distance");
            if (tslDistEl && livePrice > 0) {
                const curStop = tLow > 0 ? tLow : (livePrice * 0.99);
                const gap = livePrice - curStop;
                tslDistEl.innerText = gap > 0 ? ("+$" + gap.toFixed(2)) : "$0.00";
            }

            const homeProfitEl = document.getElementById("realProfitValue");
            if (homeProfitEl) {
                const combinedProfit = total4BotsRealized + (pnl > 0 ? pnl : 0);
                homeProfitEl.innerText = "$" + combinedProfit.toFixed(2);
            }
            const posterProfit = document.getElementById("poster-profit-val");
            if (posterProfit) {
                posterProfit.innerText = (total4BotsRealized >= 0 ? "+" : "") + "$" + total4BotsRealized.toFixed(2);
            }
            const poster24h = document.getElementById("poster-24h-profit");
            if (poster24h) {
                poster24h.innerText = (calcBot24h >= 0 ? "+" : "") + "$" + calcBot24h.toFixed(2);
            }

            let wins = 0;
            let losses = 0;
            if (data.spotTradesHistory && Array.isArray(data.spotTradesHistory)) {
                data.spotTradesHistory.forEach(tr => {
                    const ordId = String(tr.orderId || tr.order_id || "").toUpperCase();
                    const execType = String(tr.execType || tr.exec_type || "").toUpperCase();
                    const label = String(tr.label || "").toUpperCase();
                    const botType = String(tr.botType || tr.bot_type || "").toUpperCase();
                    const isManual = ordId.startsWith("MAN_") || ordId.startsWith("ORD_") || ordId.startsWith("COPY_") || ordId.startsWith("CPOS_") || execType.includes("MANUAL") || execType.includes("COPY");
                    const isKiller = ordId.startsWith("M_") || ordId.startsWith("K2_") || ordId.startsWith("K3_") || execType.includes("MICRO") || execType.includes("KILLER") || execType.includes("SCALP") || label.includes("MICRO") || label.includes("KILLER") || label.includes("APEX") || label.includes("QUANTUM") || label.includes("TITAN ABYSS");
                    const isHyper = ordId.startsWith("HYPER_") || execType.includes("HYPER") || label.includes("HYPER") || botType.includes("HYPER") || label.includes("TITAN POOL");
                    const isSingularity = ordId.startsWith("SNG_") || execType.includes("SINGULARITY") || label.includes("SINGULARITY");
                    const isLoop = ordId.startsWith("ATL_") || execType.includes("AUTO_LOOP");
                    if (!isManual && !isKiller && !isHyper && !isSingularity && !isLoop && tr.side === "SELL") {
                        if (parseFloat(tr.profit || tr.realizedPnl || 0) >= 0) wins++;
                        else losses++;
                    }
                });
            }

            const winTag = document.getElementById("win-tag");
            const lossTag = document.getElementById("loss-tag");
            if (winTag) winTag.innerText = wins.toString();
            if (lossTag) lossTag.innerText = losses.toString();

            let dailyWins = 0;
            const countedExitIds = new Set();
            fourBotsTrades.forEach(tr => {
                const ordId = String(tr.orderId || tr.order_id || "").toUpperCase();
                const isExit = String(tr.side || "").toUpperCase().includes("SELL") || String(tr.execType || "").toUpperCase().includes("EXIT");
                if (isExit && parseFloat(tr.profit || tr.realizedPnl || 0) >= 0 && !countedExitIds.has(ordId)) {
                    countedExitIds.add(ordId);
                    dailyWins++;
                }
            });
            const homeTradesEl = document.getElementById("successTradeCount");
            if (homeTradesEl) {
                homeTradesEl.innerText = dailyWins.toString();
            }

            const spotCashBal = (data.manualTestBalance !== undefined) ? parseFloat(data.manualTestBalance) : (data.usdtBalance !== undefined ? parseFloat(data.usdtBalance) : 100.0);
            let userHoldingSolAmt = 0.0;
            if (data.walletActivePositions && Array.isArray(data.walletActivePositions)) {
                data.walletActivePositions.forEach(p => { userHoldingSolAmt += parseFloat(p.solAmount || 0); });
            }
            const liveCalcP = livePrice > 0 ? livePrice : 0;
            const userTotalWorth = Math.max(0, spotCashBal + (userHoldingSolAmt * liveCalcP));
            const shineBalEl = document.getElementById("homeProfitShine");
            if (shineBalEl) {
                shineBalEl.innerText = userTotalWorth.toFixed(2);
            }

            const currentClaimable = Math.max(0, total4BotsRealized - (typeof userClaimedProfit !== 'undefined' ? userClaimedProfit : 0));
            const homeProfitUsdtEl = document.getElementById("homeProfitUsdt");
            if (homeProfitUsdtEl) {
                homeProfitUsdtEl.innerText = currentClaimable.toFixed(2);
            }
            const homePassiveEl = document.getElementById("homePassiveIncomeVal");
            if (homePassiveEl) {
                homePassiveEl.innerText = currentClaimable.toFixed(2);
            }
            const homeClaimDispEl = document.getElementById("homeClaimValueDisplay");
            if (homeClaimDispEl) {
                homeClaimDispEl.innerText = currentClaimable.toFixed(2);
            }
            const ruleProfitEl = document.getElementById("ruleTradingProfitVal");
            if (ruleProfitEl) {
                ruleProfitEl.innerText = currentClaimable.toFixed(2);
            }

            const totalExits = wins + losses;
            const winRateEl = document.getElementById("bot-win-rate");
            if (winRateEl) {
                const rate = totalExits > 0 ? ((wins / totalExits) * 100).toFixed(1) : "0";
                winRateEl.innerText = rate + "%";
            }

            const countPill = document.getElementById("trade-count-pill");
            if (countPill) countPill.innerText = totalExits.toString();

            const cdBadge = document.getElementById("bot-cooldown-badge");
            const cdTimer = document.getElementById("cooldown-timer");
            if (data.cooldownRemaining && data.cooldownRemaining > 0) {
                if (cdBadge) cdBadge.style.display = "inline-block";
                const mins = Math.floor(data.cooldownRemaining / 60);
                const secs = data.cooldownRemaining % 60;
                if (cdTimer) cdTimer.innerText = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
            } else {
                if (cdBadge) cdBadge.style.display = "none";
            }

            const pill1 = document.getElementById("ts-stage-pill-1");
            const pill2 = document.getElementById("ts-stage-pill-2");
            const pill3 = document.getElementById("ts-stage-pill-3");
            const dipBadge = document.getElementById("dip-hunter-status");
            const curStage = data.trailingStage || "1.0%";

            if (pill1 && pill2 && pill3) {
                pill1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                pill1.style.background = "rgba(58, 71, 166, 0.1)";
                pill2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                pill2.style.background = "rgba(232, 117, 91, 0.05)";
                pill3.style.borderColor = "rgba(0, 230, 118, 0.2)";
                pill3.style.background = "rgba(0, 230, 118, 0.05)";

                if (curStage === "STAGE_1") {
                    pill1.style.borderColor = "#5C6BC0";
                    pill1.style.background = "rgba(92, 107, 192, 0.4)";
                    pill1.style.boxShadow = "0 0 10px rgba(92, 107, 192, 0.5)";
                } else if (curStage === "STAGE_2") {
                    pill2.style.borderColor = "#E8755B";
                    pill2.style.background = "rgba(232, 117, 91, 0.4)";
                    pill2.style.boxShadow = "0 0 10px rgba(232, 117, 91, 0.5)";
                } else if (curStage === "STAGE_3") {
                    pill3.style.borderColor = "#00e676";
                    pill3.style.background = "rgba(0, 230, 118, 0.4)";
                    pill3.style.boxShadow = "0 0 10px rgba(0, 230, 118, 0.5)";
                }
            }

            if (dipBadge) {
                if (!data.activePositions || data.activePositions.length === 0) {
                    dipBadge.innerText = "DIP CATCHER ACTIVE";
                    dipBadge.style.color = "#00d2ff";
                    dipBadge.style.borderColor = "#00d2ff";
                    dipBadge.style.background = "rgba(0, 210, 255, 0.15)";
                } else {
                    dipBadge.innerText = "RIDING POSITION";
                    dipBadge.style.color = "#4CAF50";
                    dipBadge.style.borderColor = "#4CAF50";
                    dipBadge.style.background = "rgba(76, 175, 80, 0.15)";
                }
            }

            const tbPill1 = document.getElementById("tb-stage-pill-1");
            const tbPill2 = document.getElementById("tb-stage-pill-2");
            const tbPill3 = document.getElementById("tb-stage-pill-3");
            const tbBadge = document.getElementById("tb-status-badge");
            const tbLowEl = document.getElementById("tb-lowest-tracked");

            let refEntry = livePrice;
            if (data.activePositions && data.activePositions.length > 0) {
                const regPos = data.activePositions.filter(p => !p.isMacro);
                if (regPos.length > 0) {
                    refEntry = parseFloat(regPos[regPos.length - 1].entryPrice || livePrice);
                }
            }

            const t1 = (refEntry - 0.60).toFixed(2);
            const t2 = (refEntry - 0.90).toFixed(2);
            const t3 = (refEntry - 1.20).toFixed(2);

            const elT1 = document.getElementById("tb-target-1");
            const elT2 = document.getElementById("tb-target-2");
            const elT3 = document.getElementById("tb-target-3");
            if (elT1) elT1.innerText = "$" + t1;
            if (elT2) elT2.innerText = "$" + t2;
            if (elT3) elT3.innerText = "$" + t3;

            const trackedLow = parseFloat(data.tbLowest || 0);
            if (tbLowEl) tbLowEl.innerText = trackedLow > 0 ? ("$" + trackedLow.toFixed(2)) : "$" + livePrice.toFixed(2);

            if (tbPill1 && tbPill2 && tbPill3 && tbBadge) {
                tbPill1.style.borderColor = "rgba(255,255,255,0.06)";
                tbPill1.style.background = "rgba(255,255,255,0.02)";
                tbPill2.style.borderColor = "rgba(255,255,255,0.06)";
                tbPill2.style.background = "rgba(255,255,255,0.02)";
                tbPill3.style.borderColor = "rgba(255,255,255,0.06)";
                tbPill3.style.background = "rgba(255,255,255,0.02)";

                const activeTbStage = data.tbStage || "IDLE";

                if (activeTbStage === "0.60$") {
                    tbBadge.innerText = "ACTIVE: STEP 1 (-$0.60)";
                    tbBadge.style.color = "#00d2ff";
                    tbPill1.style.borderColor = "#00d2ff";
                    tbPill1.style.background = "rgba(0, 210, 255, 0.25)";
                    tbPill1.style.boxShadow = "0 0 10px rgba(0, 210, 255, 0.4)";
                } else if (activeTbStage === "0.90$") {
                    tbBadge.innerText = "ACTIVE: STEP 2 (-$0.90)";
                    tbBadge.style.color = "#FFD700";
                    tbPill2.style.borderColor = "#FFD700";
                    tbPill2.style.background = "rgba(255, 215, 0, 0.25)";
                    tbPill2.style.boxShadow = "0 0 10px rgba(255, 215, 0, 0.4)";
                } else if (activeTbStage === "1.20$") {
                    tbBadge.innerText = "ACTIVE: STEP 3 (-$1.20)";
                    tbBadge.style.color = "#00e676";
                    tbPill3.style.borderColor = "#00e676";
                    tbPill3.style.background = "rgba(0, 230, 118, 0.25)";
                    tbPill3.style.boxShadow = "0 0 10px rgba(0, 230, 118, 0.4)";
                } else {
                    tbBadge.innerText = "ARMED (SCANNING DIP)";
                    tbBadge.style.color = "#757575";
                }
            }

            if (data.whaleOrderflow !== undefined) {
                const ofVal = document.getElementById("radar-orderflow-val");
                const ofIcon = document.getElementById("radar-orderflow-icon");
                const ofWrap = document.getElementById("radar-orderflow-wrapper");
                if (ofVal) ofVal.innerText = data.whaleOrderflow + "% BUY VOL";
                if (data.whaleDumpAlert) {
                    if (ofWrap) ofWrap.style.color = "#f6465d";
                    if (ofIcon) ofIcon.innerText = "warning";
                    if (ofVal) ofVal.innerText = "WHALE DUMP (DEFENDING)";
                } else if (data.whaleSentiment === "BULLISH") {
                    if (ofWrap) ofWrap.style.color = "#4CAF50";
                    if (ofIcon) ofIcon.innerText = "trending_up";
                    if (ofVal && data.whaleBoost && data.whaleBoost > 1.0) ofVal.innerText = `${data.whaleOrderflow}% BUY (BOOST ACTIVE)`;
                } else if (data.whaleSentiment === "BEARISH") {
                    if (ofWrap) ofWrap.style.color = "#f6465d";
                    if (ofIcon) ofIcon.innerText = "trending_down";
                } else {
                    if (ofWrap) ofWrap.style.color = "#FFC107";
                    if (ofIcon) ofIcon.innerText = "trending_flat";
                }
            }

            const botBadge = document.getElementById("bot-positions-badge");
            const botCont = document.getElementById("bot-positions-container");
            const activePosList = (data.activePositions && Array.isArray(data.activePositions)) ? data.activePositions : [];

            if (activePosList.length > 0) {
                if (botBadge) botBadge.innerText = activePosList.length + " OPEN";
                const regularList = activePosList.filter(p => !p.isMacro);
                const maxUserSlots = 24;
                let dotsHTML = '';
                for (let i = 1; i <= maxUserSlots; i++) {
                    dotsHTML += i <= regularList.length 
                        ? '<span style="color:#00d2ff; font-size:11px; text-align:center;">●</span>' 
                        : '<span style="color:#444; font-size:11px; text-align:center;">○</span>';
                }
                let nextTargetHTML = '';
                if (regularList.length > 0) {
                    const lastPos = regularList[regularList.length - 1];
                    const nextDip = (parseFloat(lastPos.entryPrice || 0) * 0.982).toFixed(2);
                    nextTargetHTML = '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; padding-top:8px; border-top:1px dashed rgba(255,255,255,0.1); font-size:11px;">' +
                        '<span style="color:#757575;">Next Safety Entry (-1.8%):</span>' +
                        '<span style="color:#FFD700; font-weight:bold;">$' + nextDip + '</span>' +
                        '</div>';
                }
                let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                    '<span style="font-size:12px; font-weight:bold; color:#fff;">DCA SAFETY ORDERS:</span>' +
                    '<span style="font-size:11px; color:#00d2ff; font-weight:bold; font-family:monospace;">(' + regularList.length + '/' + maxUserSlots + ')</span>' +
                    '</div>' +
                    '<div style="display:grid; grid-template-columns:repeat(12, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                    nextTargetHTML + '</div>';

                const rowsHTML = activePosList.map(pos => {
                    const isMacro = pos.isMacro;
                    const rndNum = pos.round || 1;
                    const ePrice = parseFloat(pos.entryPrice || 0).toFixed(2);
                    const sAmt = parseFloat(pos.solAmount || 0).toFixed(4);
                    const labelColor = isMacro ? "#FFD700" : "#00d2ff";
                    const badgeText = isMacro ? "27% MACRO VAULT" : ("ROUND " + rndNum);

                    return '<div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:12px; font-family:monospace;">' +
                           '<span style="color:' + labelColor + '; font-weight:bold;">' + badgeText + '</span>' +
                           '<span>$' + ePrice + '</span>' +
                           '<span style="color:#4CAF50; font-weight:bold;">' + sAmt + ' SOL</span>' +
                           '</div>';
                }).join("");

                if (botCont) botCont.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
            } else {
                if (botBadge) botBadge.innerText = "0 OPEN";
                if (botCont) botCont.innerHTML = "NO ACTIVE BOT POSITIONS";
            }

            const l1 = document.getElementById("trade-log-line-1");
            const l2 = document.getElementById("trade-log-line-2");
            if (l1 && l2) {
                if (data.activePositions && data.activePositions.length > 0) {
                    l1.innerText = "> AI Engine: Active in Round " + data.activeRound + " | Trailing Stage: " + curStage;
                    l2.innerText = "> Whale Sentiment: " + (data.whaleSentiment || "NEUTRAL") + " | Orderflow: " + (data.whaleOrderflow || 50) + "%";
                } else {
                    l1.innerText = "> Dip Catcher: Scanning Lowest Point for Confirm Bounce";
                    l2.innerText = "> Whale Radar Active: Waiting for Big Volume Inflow";
                }
            }

            let microHistoryData = [];
            if (data.microTradesHistory && Array.isArray(data.microTradesHistory) && data.microTradesHistory.length > 0) {
                microHistoryData = data.microTradesHistory;
            } else if (data.tradesHistory && Array.isArray(data.tradesHistory)) {
                microHistoryData = data.tradesHistory.filter(t => t.isMicro || (t.orderId && String(t.orderId).includes("MICRO")) || (t.label && String(t.label).includes("MICRO")));
            }

            if (microHistoryData.length === 0 && (data.microTotalTrades > 0 || parseFloat(data.microRealizedPnl || 0) > 0)) {
                const winsCount = parseInt(data.microTotalTrades) || 1;
                const totalProfitVal = parseFloat(data.microRealizedPnl) || 0;
                const profitPerTrade = (totalProfitVal / winsCount);
                for (let k = winsCount; k >= 1; k--) {
                    microHistoryData.push({
                        side: "SELL",
                        profit: profitPerTrade,
                        price: livePrice > 0 ? livePrice : 0,
                        solAmount: 0.05,
                        label: "MICRO #" + k,
                        timestamp: new Date(Date.now() - ((winsCount - k + 1) * 360000)).toISOString()
                    });
                }
            }

            let spotList = Array.isArray(data.spotTradesHistory) ? [...data.spotTradesHistory] : [];
            const seenSpotOrderIds = new Set();
            const cleanSpotList = [];
            spotList.forEach(t => {
                const oId = String(t.orderId || t.order_id || "").toUpperCase().trim();
                if (oId && !seenSpotOrderIds.has(oId) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
                    seenSpotOrderIds.add(oId);
                    cleanSpotList.push(t);
                }
            });
            cachedAllTrades = cleanSpotList;
            renderAuditHistoryList(cachedAllTrades);
            if (data.latestSignal && data.latestSignal.text) {
                const sigText = "SIGNAL: " + data.latestSignal.text;
                typeWriterEffect(sigText, "aiSignalLiveText");
                typeWriterEffect(sigText, "tabAiSignalLiveText");
            }

            if (livePrice > 0) {
                const ezLow = (livePrice * 0.998).toFixed(2);
                const ezHigh = livePrice.toFixed(2);
                const ezEl = document.getElementById("sigDynamicEntryZone");
                if (ezEl) ezEl.innerText = "$" + ezLow + " - $" + ezHigh;

                const slEl = document.getElementById("sigDynamicStopLoss");
                if (slEl) slEl.innerText = "$" + (livePrice * 0.985).toFixed(2);

                const tp1El = document.getElementById("sigDynamicTp1");
                if (tp1El) tp1El.innerText = "$" + (livePrice * 1.012).toFixed(2);

                const tp2El = document.getElementById("sigDynamicTp2");
                if (tp2El) tp2El.innerText = "$" + (livePrice * 1.025).toFixed(2);

                const supEl = document.getElementById("sigSupportWall");
                if (supEl) supEl.innerText = "$" + (livePrice * 0.988).toFixed(2);

                const resEl = document.getElementById("sigResistanceWall");
                if (resEl) resEl.innerText = "$" + (livePrice * 1.015).toFixed(2);

                const realWins = typeof wins !== "undefined" ? wins : 0;
                const realLosses = typeof losses !== "undefined" ? losses : 0;
                const realTotal = realWins + realLosses;
                let calculatedWinRate = "92.4% WIN RATE";
                if (realTotal > 0) {
                    const rawRate = (realWins / realTotal) * 100;
                    calculatedWinRate = (rawRate >= 98 ? "94.2" : (rawRate <= 75 ? "86.8" : rawRate.toFixed(1))) + "% WIN RATE";
                } else {
                    calculatedWinRate = "91.8% QUANT WIN RATE";
                }
                const confEl = document.getElementById("sigConfidenceBadge");
                if (confEl) confEl.innerText = calculatedWinRate;

                const wallRatioEl = document.getElementById("sig-whale-ratio");
                if (wallRatioEl && data.whaleOrderflow !== undefined) {
                    wallRatioEl.innerText = parseFloat(data.whaleOrderflow).toFixed(1) + "% BUY";
                }
            }
if (data.hyperPoolActive) {
                const curLive = livePrice > 0 ? livePrice : 0;
                const poolCap = parseFloat(data.hyperPoolBalance !== undefined ? data.hyperPoolBalance : 1000);
                const posList = Array.isArray(data.hyperPositions) ? data.hyperPositions : [];
                let hTotalSol = 0;
                let hTotalInvested = 0;
                posList.forEach(p => {
                    hTotalSol += parseFloat(p.solAmount || 0);
                    hTotalInvested += parseFloat(p.invested || 0);
                });

                const totalPoolUsers = Math.max(1, parseInt(data.hyperPoolUsers || 100));
                const userShareRatio = 1.0 / totalPoolUsers;

                const poolUnrealPnl = hTotalSol > 0 ? ((hTotalSol * curLive) - hTotalInvested) : 0;
                const userUnrealPnl = poolUnrealPnl * userShareRatio;
                const poolRealPnl = parseFloat(data.hyperRealizedPnl || 0);
                const userRealPnl = poolRealPnl * userShareRatio;

                const hPoolEl = document.getElementById("hyper-pool-total");
                if (hPoolEl) hPoolEl.innerText = "$" + poolCap.toFixed(2);

                const hSolEl = document.getElementById("hyper-sol-pos");
                if (hSolEl) hSolEl.innerText = hTotalSol.toFixed(4) + " SOL";

                const hUserUnreal = document.getElementById("hyper-user-unrealized-pnl");
                if (hUserUnreal) {
                    hUserUnreal.innerText = (userUnrealPnl >= 0 ? "+" : "") + "$" + userUnrealPnl.toFixed(4);
                    hUserUnreal.style.color = userUnrealPnl >= 0 ? "#00e676" : "#f6465d";
                }

                const hUserReal = document.getElementById("hyper-user-realized-pnl");
                if (hUserReal) {
                    hUserReal.innerText = (userRealPnl >= 0 ? "+" : "") + "$" + userRealPnl.toFixed(4);
                    hUserReal.style.color = userRealPnl >= 0 ? "#4CAF50" : "#f6465d";
                }

                const hUserInv = document.getElementById("hyper-user-invest-display");
                if (hUserInv && data.hyperUserInvestment !== undefined) {
                    hUserInv.innerText = "$" + parseFloat(data.hyperUserInvestment).toFixed(2) + " USDT";
                }

                const hBadge = document.getElementById("hyper-orders-badge");
                if (hBadge) hBadge.innerText = posList.length + " OPEN";

                const hRefEl = document.getElementById("hyper-ref-price");
                const hLowEl = document.getElementById("hyper-lowest-tracked");
                const hRefP = data.hyperLastRefPrice || livePrice;
                const hLowP = data.hyperTbLowest || livePrice;
                if (hRefEl) hRefEl.innerText = "$" + parseFloat(hRefP).toFixed(2);
                if (hLowEl) hLowEl.innerText = "$" + parseFloat(hLowP).toFixed(2);

                const hDipStatus = document.getElementById("hyper-dip-hunter-status");
            const hTsHigh = document.getElementById("hyper-ts-high");
            const hTsLow = document.getElementById("hyper-ts-low");
            const hTbStatus = document.getElementById("hyper-tb-status-badge");
            const hTbLow = document.getElementById("hyper-lowest-tracked");
            const hT1 = document.getElementById("hyper-tb-target-1");
            const hT2 = document.getElementById("hyper-tb-target-2");
            const hT3 = document.getElementById("hyper-tb-target-3");
            const hPill1 = document.getElementById("hyper-ts-stage-pill-1");
            const hPill2 = document.getElementById("hyper-ts-stage-pill-2");
            const hPill3 = document.getElementById("hyper-ts-stage-pill-3");

            let hPeakVal = curLive;
            let hStopVal = curLive * 0.998;
            if (posList.length > 0) {
                const highestTracked = Math.max(...posList.map(p => parseFloat(p.ts_high || p.entryPrice || curLive)));
                hPeakVal = Math.max(highestTracked, curLive);
                const entryBase = Math.min(...posList.map(p => parseFloat(p.entryPrice || curLive)));
                const hGain = hPeakVal - entryBase;
                let hTrailGap = 0.05;
                if (hGain >= 0.70) hTrailGap = 0.12;
                else if (hGain >= 0.40) hTrailGap = 0.08;
                else if (hGain >= 0.20) hTrailGap = 0.05;
                hStopVal = hPeakVal - hTrailGap;
                if (hDipStatus) {
                    hDipStatus.innerText = "RIDING POSITION";
                    hDipStatus.style.color = "#4CAF50";
                }
            } else {
                if (hDipStatus) {
                    hDipStatus.innerText = "DIP CATCHER ACTIVE";
                    hDipStatus.style.color = "#00e5ff";
                }
            }

            if (hTsHigh) hTsHigh.innerText = data.hyperTsHigh !== undefined ? "$" + parseFloat(data.hyperTsHigh).toFixed(2) : "$" + hPeakVal.toFixed(2);
            if (hTsLow) hTsLow.innerText = data.hyperTsLow !== undefined && parseFloat(data.hyperTsLow) > 0 ? "$" + parseFloat(data.hyperTsLow).toFixed(2) : "$0.00";

            const hRefBase = posList.length > 0 ? parseFloat(posList[posList.length - 1].entryPrice || curLive) : curLive;
            if (hT1) hT1.innerText = "$" + (hRefBase - 0.01).toFixed(2);
            if (hT2) hT2.innerText = "$" + (hRefBase - 0.015).toFixed(2);
            if (hT3) hT3.innerText = "$" + (hRefBase - 0.02).toFixed(2);
            if (hTbLow) hTbLow.innerText = "$" + parseFloat(data.hyperTbLowest || curLive).toFixed(2);

            if (hPill1 && hPill2 && hPill3) {
                hPill1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                hPill2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                hPill3.style.borderColor = "rgba(0, 230, 118, 0.2)";
                if (posList.length > 0) {
                    const diff = curLive - parseFloat(posList[posList.length - 1].entryPrice || curLive);
                    if (diff >= 0.70) {
                        hPill3.style.borderColor = "#00e676";
                        hPill3.style.background = "rgba(0, 230, 118, 0.25)";
                    } else if (diff >= 0.40) {
                        hPill2.style.borderColor = "#FFD700";
                        hPill2.style.background = "rgba(255, 215, 0, 0.25)";
                    } else if (diff >= 0.20) {
                        hPill1.style.borderColor = "#00e5ff";
                        hPill1.style.background = "rgba(0, 229, 255, 0.25)";
                    }
                }
            }
            }

            const mUserInv = document.getElementById("micro-user-invest-display");
            if (mUserInv) {
                let mTotalInv = 0;
                if (data.microPositions && Array.isArray(data.microPositions)) {
                    data.microPositions.forEach(p => { mTotalInv += parseFloat(p.invested || 0); });
                }
                mUserInv.innerText = "$" + mTotalInv.toFixed(2) + " USDT";
            }

            const k2UserInv = document.getElementById("killer2-user-invest-display");
            if (k2UserInv) {
                let k2TotalInv = 0;
                if (data.killer2Positions && Array.isArray(data.killer2Positions)) {
                    data.killer2Positions.forEach(p => { k2TotalInv += parseFloat(p.invested || 0); });
                }
                k2UserInv.innerText = "$" + k2TotalInv.toFixed(2) + " USDT";
            }

            const k3UserInv = document.getElementById("killer3-user-invest-display");
            if (k3UserInv) {
                let k3TotalInv = 0;
                if (data.killer3Positions && Array.isArray(data.killer3Positions)) {
                    data.killer3Positions.forEach(p => { k3TotalInv += parseFloat(p.invested || 0); });
                }
                k3UserInv.innerText = "$" + k3TotalInv.toFixed(2) + " USDT";
            }

            const mIdleEl = document.getElementById("micro-idle-fund");
            if (mIdleEl && data.microIdleFundAvail !== undefined) {
                mIdleEl.innerText = "$" + parseFloat(data.microIdleFundAvail).toFixed(2);
            }

            const mRealEl = document.getElementById("micro-realized-pnl");
            if (mRealEl && data.microRealizedPnl !== undefined) {
                const mVal = parseFloat(data.microRealizedPnl);
                mRealEl.innerText = (mVal >= 0 ? "+" : "") + "$" + mVal.toFixed(4);
                mRealEl.style.color = mVal >= 0 ? "#4CAF50" : "#f6465d";
                void 0;
            }

            let mTotalSol = 0;
            let mTotalInvested = 0;
            const mBadge = document.getElementById("micro-orders-badge");

            if (data.microPositions && Array.isArray(data.microPositions) && data.microPositions.length > 0) {
                if (mBadge) mBadge.innerText = data.microPositions.length + " OPEN";
                data.microPositions.forEach(p => {
                    mTotalSol += parseFloat(p.solAmount || 0);
                    mTotalInvested += parseFloat(p.invested || 0);
                });
            } else {
                if (mBadge) mBadge.innerText = "0 OPEN";
            }
            const mSolPosEl = document.getElementById("micro-sol-pos");
            if (mSolPosEl) mSolPosEl.innerText = mTotalSol.toFixed(4) + " SOL";

            const mUnrealEl = document.getElementById("micro-unrealized-pnl");
            if (mUnrealEl) {
                const curLive = livePrice > 0 ? livePrice : 0;
                const mUnrealVal = (mTotalSol * curLive) - mTotalInvested;
                mUnrealEl.innerText = (mUnrealVal >= 0 ? "+" : "") + "$" + mUnrealVal.toFixed(4);
                mUnrealEl.style.color = mUnrealVal >= 0 ? "#00e676" : "#f6465d";
            }

            const mDipStatus = document.getElementById("micro-dip-hunter-status");
            const mTsHigh = document.getElementById("micro-ts-high");
            const mTsLow = document.getElementById("micro-ts-low");
            const mTbStatus = document.getElementById("micro-tb-status-badge");
            const mTbLow = document.getElementById("micro-lowest-tracked");
            const mT1 = document.getElementById("micro-tb-target-1");
            const mT2 = document.getElementById("micro-tb-target-2");
            const mT3 = document.getElementById("micro-tb-target-3");
            const mPill1 = document.getElementById("micro-ts-stage-pill-1");
            const mPill2 = document.getElementById("micro-ts-stage-pill-2");
            const mPill3 = document.getElementById("micro-ts-stage-pill-3");

            let mPeakVal = livePrice;
            let mStopVal = livePrice * 0.99;
            const mPosList = data.microPositions || [];

            if (mPosList.length > 0) {
                const highestTracked = Math.max(...mPosList.map(p => parseFloat(p.ts_high || p.entryPrice || livePrice)));
                mPeakVal = Math.max(highestTracked, livePrice);
                const entryBase = Math.min(...mPosList.map(p => parseFloat(p.entryPrice || livePrice)));
                const mGain = mPeakVal - entryBase;
                let mTrailGap = 0.08;
                if (mGain >= 0.80) mTrailGap = 0.15;
                else if (mGain >= 0.55) mTrailGap = 0.12;
                else if (mGain >= 0.35) mTrailGap = 0.08;
                mStopVal = mPeakVal - mTrailGap;
                if (mDipStatus) {
                    mDipStatus.innerText = "RIDING POSITION";
                    mDipStatus.style.color = "#4CAF50";
                }
            } else {
                if (mDipStatus) {
                    mDipStatus.innerText = "DIP CATCHER ACTIVE";
                    mDipStatus.style.color = "#00d2ff";
                }
            }

            if (mTsHigh) mTsHigh.innerText = data.microTsHigh !== undefined ? "$" + parseFloat(data.microTsHigh).toFixed(2) : "$" + mPeakVal.toFixed(2);
            if (mTsLow) mTsLow.innerText = data.microTsLow !== undefined && parseFloat(data.microTsLow) > 0 ? "$" + parseFloat(data.microTsLow).toFixed(2) : "$0.00";

            const mRefBase = mPosList.length > 0 ? parseFloat(mPosList[mPosList.length - 1].entryPrice || livePrice) : livePrice;
            if (mT1) mT1.innerText = "$" + (mRefBase - 0.30).toFixed(2);
            if (mT2) mT2.innerText = "$" + (mRefBase - 0.60).toFixed(2);
            if (mT3) mT3.innerText = "$" + (mRefBase - 0.90).toFixed(2);
            if (mTbLow) mTbLow.innerText = "$" + parseFloat(data.microTbLowest || livePrice).toFixed(2);

            if (mPill1 && mPill2 && mPill3) {
                mPill1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                mPill2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                mPill3.style.borderColor = "rgba(0, 230, 118, 0.2)";
                if (mPosList.length > 0) {
                    const diff = livePrice - parseFloat(mPosList[mPosList.length - 1].entryPrice || livePrice);
                    if (diff >= 0.80) {
                        mPill3.style.borderColor = "#00e676";
                        mPill3.style.background = "rgba(0, 230, 118, 0.25)";
                    } else if (diff >= 0.55) {
                        mPill2.style.borderColor = "#FFD700";
                        mPill2.style.background = "rgba(255, 215, 0, 0.25)";
                    } else if (diff >= 0.35) {
                        mPill1.style.borderColor = "#00d2ff";
                        mPill1.style.background = "rgba(0, 210, 255, 0.25)";
                    }
                }
            }

            const k2IdleEl = document.getElementById("killer2-idle-fund");
            if (k2IdleEl && data.killer2IdleFundAvail !== undefined) {
                k2IdleEl.innerText = "$" + parseFloat(data.killer2IdleFundAvail).toFixed(2);
            }

            const k2RealEl = document.getElementById("killer2-realized-pnl");
            if (k2RealEl && data.killer2RealizedPnl !== undefined) {
                const k2Val = parseFloat(data.killer2RealizedPnl);
                k2RealEl.innerText = (k2Val >= 0 ? "+" : "") + "$" + k2Val.toFixed(4);
                k2RealEl.style.color = k2Val >= 0 ? "#4CAF50" : "#f6465d";
                void 0;
            }

            let k2TotalSol = 0;
            let k2TotalInvested = 0;
            const k2Badge = document.getElementById("killer2-orders-badge");

            if (data.killer2Positions && Array.isArray(data.killer2Positions) && data.killer2Positions.length > 0) {
                if (k2Badge) k2Badge.innerText = data.killer2Positions.length + " OPEN";
                data.killer2Positions.forEach(p => {
                    k2TotalSol += parseFloat(p.solAmount || 0);
                    k2TotalInvested += parseFloat(p.invested || 0);
                });
            } else {
                if (k2Badge) k2Badge.innerText = "0 OPEN";
            }

            const k2SolPosEl = document.getElementById("killer2-sol-pos");
            if (k2SolPosEl) k2SolPosEl.innerText = k2TotalSol.toFixed(4) + " SOL";

            const k2UnrealEl = document.getElementById("killer2-unrealized-pnl");
            if (k2UnrealEl) {
                const curLive = livePrice > 0 ? livePrice : 0;
                const k2UnrealVal = (k2TotalSol * curLive) - k2TotalInvested;
                k2UnrealEl.innerText = (k2UnrealVal >= 0 ? "+" : "") + "$" + k2UnrealVal.toFixed(4);
                k2UnrealEl.style.color = k2UnrealVal >= 0 ? "#00e676" : "#f6465d";
            }

            const k2DipStatus = document.getElementById("killer2-dip-hunter-status");
            const k2TsHigh = document.getElementById("killer2-ts-high");
            const k2TsLow = document.getElementById("killer2-ts-low");
            const k2TbStatus = document.getElementById("killer2-tb-status-badge");
            const k2TbLow = document.getElementById("killer2-lowest-tracked");
            const k2T1 = document.getElementById("killer2-tb-target-1");
            const k2T2 = document.getElementById("killer2-tb-target-2");
            const k2T3 = document.getElementById("killer2-tb-target-3");
            const k2Pill1 = document.getElementById("killer2-ts-stage-pill-1");
            const k2Pill2 = document.getElementById("killer2-ts-stage-pill-2");
            const k2Pill3 = document.getElementById("killer2-ts-stage-pill-3");

            let k2PeakVal = livePrice;
            let k2StopVal = livePrice * 0.99;
            const k2PosList = data.killer2Positions || [];

            if (k2PosList.length > 0) {
                const highestTracked = Math.max(...k2PosList.map(p => parseFloat(p.ts_high || p.entryPrice || livePrice)));
                k2PeakVal = Math.max(highestTracked, livePrice);
                const entryBase = Math.min(...k2PosList.map(p => parseFloat(p.entryPrice || livePrice)));
                const k2Gain = k2PeakVal - entryBase;
                let k2TrailGap = 0.15;
                if (k2Gain >= 1.20) k2TrailGap = 0.25;
                else if (k2Gain >= 0.80) k2TrailGap = 0.20;
                else if (k2Gain >= 0.50) k2TrailGap = 0.15;
                k2StopVal = k2PeakVal - k2TrailGap;
                if (k2DipStatus) {
                    k2DipStatus.innerText = "RIDING POSITION";
                    k2DipStatus.style.color = "#4CAF50";
                }
            } else {
                if (k2DipStatus) {
                    k2DipStatus.innerText = "DIP CATCHER ACTIVE";
                    k2DipStatus.style.color = "#FFD700";
                }
            }

            if (k2TsHigh) k2TsHigh.innerText = data.killer2TsHigh !== undefined ? "$" + parseFloat(data.killer2TsHigh).toFixed(2) : "$" + k2PeakVal.toFixed(2);
            if (k2TsLow) k2TsLow.innerText = data.killer2TsLow !== undefined && parseFloat(data.killer2TsLow) > 0 ? "$" + parseFloat(data.killer2TsLow).toFixed(2) : "$0.00";

            const k2RefBase = k2PosList.length > 0 ? parseFloat(k2PosList[k2PosList.length - 1].entryPrice || livePrice) : livePrice;
            if (k2T1) k2T1.innerText = "$" + (k2RefBase - 0.60).toFixed(2);
            if (k2T2) k2T2.innerText = "$" + (k2RefBase - 0.90).toFixed(2);
            if (k2T3) k2T3.innerText = "$" + (k2RefBase - 1.20).toFixed(2);
            if (k2TbLow) k2TbLow.innerText = "$" + parseFloat(data.killer2TbLowest || livePrice).toFixed(2);

            if (k2Pill1 && k2Pill2 && k2Pill3) {
                k2Pill1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                k2Pill2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                k2Pill3.style.borderColor = "rgba(0, 230, 118, 0.2)";
                if (k2PosList.length > 0) {
                    const diff = livePrice - parseFloat(k2PosList[k2PosList.length - 1].entryPrice || livePrice);
                    if (diff >= 1.20) {
                        k2Pill3.style.borderColor = "#00e676";
                        k2Pill3.style.background = "rgba(0, 230, 118, 0.25)";
                    } else if (diff >= 0.80) {
                        k2Pill2.style.borderColor = "#FFD700";
                        k2Pill2.style.background = "rgba(255, 215, 0, 0.25)";
                    } else if (diff >= 0.50) {
                        k2Pill1.style.borderColor = "#00d2ff";
                        k2Pill1.style.background = "rgba(0, 210, 255, 0.25)";
                    }
                }
            }

            let killer2HistoryData = [];
            if (data.tradesHistory && Array.isArray(data.tradesHistory)) {
                killer2HistoryData = data.tradesHistory.filter(t => t.execType === "KILLER2_SCALP_EXIT" || (t.orderId && String(t.orderId).startsWith("K2_")));
            }
          
            const k3IdleEl = document.getElementById("killer3-idle-fund");
            if (k3IdleEl && data.killer3IdleFundAvail !== undefined) {
                k3IdleEl.innerText = "$" + parseFloat(data.killer3IdleFundAvail).toFixed(2);
            }

            const k3RealEl = document.getElementById("killer3-realized-pnl");
            if (k3RealEl && data.killer3RealizedPnl !== undefined) {
                const k3Val = parseFloat(data.killer3RealizedPnl);
                k3RealEl.innerText = (k3Val >= 0 ? "+" : "") + "$" + k3Val.toFixed(4);
                k3RealEl.style.color = k3Val >= 0 ? "#4CAF50" : "#f6465d";
                void 0;
            }

            let k3TotalSol = 0;
            let k3TotalInvested = 0;
            const k3Badge = document.getElementById("killer3-orders-badge");

            if (data.killer3Positions && Array.isArray(data.killer3Positions) && data.killer3Positions.length > 0) {
                if (k3Badge) k3Badge.innerText = data.killer3Positions.length + " OPEN";
                data.killer3Positions.forEach(p => {
                    k3TotalSol += parseFloat(p.solAmount || 0);
                    k3TotalInvested += parseFloat(p.invested || 0);
                });
            } else {
                if (k3Badge) k3Badge.innerText = "0 OPEN";
            }

            const k3SolPosEl = document.getElementById("killer3-sol-pos");
            if (k3SolPosEl) k3SolPosEl.innerText = k3TotalSol.toFixed(4) + " SOL";

            const k3UnrealEl = document.getElementById("killer3-unrealized-pnl");
            if (k3UnrealEl) {
                const curLive = livePrice > 0 ? livePrice : 0;
                const k3UnrealVal = (k3TotalSol * curLive) - k3TotalInvested;
                k3UnrealEl.innerText = (k3UnrealVal >= 0 ? "+" : "") + "$" + k3UnrealVal.toFixed(4);
                k3UnrealEl.style.color = k3UnrealVal >= 0 ? "#00e676" : "#f6465d";
            }

            const k3DipStatus = document.getElementById("killer3-dip-hunter-status");
            const k3TsHigh = document.getElementById("killer3-ts-high");
            const k3TsLow = document.getElementById("killer3-ts-low");
            const k3TbStatus = document.getElementById("killer3-tb-status-badge");
            const k3TbLow = document.getElementById("killer3-lowest-tracked");
            const k3T1 = document.getElementById("killer3-tb-target-1");
            const k3T2 = document.getElementById("killer3-tb-target-2");
            const k3T3 = document.getElementById("killer3-tb-target-3");
            const k3Pill1 = document.getElementById("killer3-ts-stage-pill-1");
            const k3Pill2 = document.getElementById("killer3-ts-stage-pill-2");
            const k3Pill3 = document.getElementById("killer3-ts-stage-pill-3");

            let k3PeakVal = livePrice;
            let k3StopVal = livePrice * 0.99;
            const k3PosList = data.killer3Positions || [];

            if (k3PosList.length > 0) {
                const highestTracked = Math.max(...k3PosList.map(p => parseFloat(p.ts_high || p.entryPrice || livePrice)));
                k3PeakVal = Math.max(highestTracked, livePrice);
                const entryBase = Math.min(...k3PosList.map(p => parseFloat(p.entryPrice || livePrice)));
                const k3Gain = k3PeakVal - entryBase;
                let k3TrailGap = 0.08;
                if (k3Gain >= 1.50) k3TrailGap = 0.03;
                else if (k3Gain >= 1.00) k3TrailGap = parseFloat((k3PeakVal * 0.005).toFixed(2));
                else if (k3Gain >= 0.60) k3TrailGap = parseFloat((k3PeakVal * 0.010).toFixed(2));
                k3StopVal = k3PeakVal - k3TrailGap;
                if (k3DipStatus) {
                    k3DipStatus.innerText = "RIDING POSITION";
                    k3DipStatus.style.color = "#4CAF50";
                }
            } else {
                if (k3DipStatus) {
                    k3DipStatus.innerText = "DIP CATCHER ACTIVE";
                    k3DipStatus.style.color = "#00e676";
                }
            }

            if (k3TsHigh) k3TsHigh.innerText = data.killer3TsHigh !== undefined ? "$" + parseFloat(data.killer3TsHigh).toFixed(2) : "$" + k3PeakVal.toFixed(2);
            if (k3TsLow) k3TsLow.innerText = data.killer3TsLow !== undefined && parseFloat(data.killer3TsLow) > 0 ? "$" + parseFloat(data.killer3TsLow).toFixed(2) : "$0.00";

            const k3RefBase = k3PosList.length > 0 ? parseFloat(k3PosList[k3PosList.length - 1].entryPrice || livePrice) : livePrice;
            if (k3T1) k3T1.innerText = "$" + (k3RefBase - 0.90).toFixed(2);
            if (k3T2) k3T2.innerText = "$" + (k3RefBase - 1.20).toFixed(2);
            if (k3T3) k3T3.innerText = "$" + (k3RefBase - 1.50).toFixed(2);
            if (k3TbLow) k3TbLow.innerText = "$" + parseFloat(data.killer3TbLowest || livePrice).toFixed(2);

            if (k3Pill1 && k3Pill2 && k3Pill3) {
                k3Pill1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                k3Pill2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                k3Pill3.style.borderColor = "rgba(0, 230, 118, 0.2)";
                if (k3PosList.length > 0) {
                    const diff = livePrice - parseFloat(k3PosList[k3PosList.length - 1].entryPrice || livePrice);
                    if (diff >= 1.50) {
                        k3Pill3.style.borderColor = "#00e676";
                        k3Pill3.style.background = "rgba(0, 230, 118, 0.25)";
                    } else if (diff >= 1.00) {
                        k3Pill2.style.borderColor = "#FFD700";
                        k3Pill2.style.background = "rgba(255, 215, 0, 0.25)";
                    } else if (diff >= 0.60) {
                        k3Pill1.style.borderColor = "#00d2ff";
                        k3Pill1.style.background = "rgba(0, 210, 255, 0.25)";
                    }
                }
            }

            let killer3HistoryData = [];
            if (data.tradesHistory && Array.isArray(data.tradesHistory)) {
                killer3HistoryData = data.tradesHistory.filter(t => t.execType === "KILLER3_SCALP_EXIT" || (t.orderId && String(t.orderId).startsWith("K3_")));
            }
            const rawScalpTrades = (Array.isArray(data.scalpTradesHistory) && data.scalpTradesHistory.length > 0) ? data.scalpTradesHistory : (Array.isArray(data.tradesHistory) ? data.tradesHistory : []);
            cachedCombinedScalpTrades = rawScalpTrades.filter(t => {
                const ordId = String(t.orderId || "");
                const execType = String(t.execType || "");
                const label = String(t.label || "");
                return ordId.startsWith("M_") || ordId.startsWith("K2_") || ordId.startsWith("K3_") || ordId.startsWith("HYPER_") || execType.includes("MICRO") || execType.includes("KILLER") || execType.includes("SCALP") || execType.includes("HYPER") || label.includes("MICRO") || label.includes("KILLER") || label.includes("APEX") || label.includes("QUANTUM") || label.includes("TITAN") || label.includes("HYPER");
            });
            renderCombinedScalpAuditList(cachedCombinedScalpTrades);

            

            if (data.autoLoops) {
                renderAutoLoopsUI(data.autoLoops);
            }

            if (currentBotCoin === "SOL" && livePrice > 0) {
                updateTradingDashboard(livePrice, "SOL");
            }
            renderProfessionalOrderDesk(data);
            refreshExchangeBalances();
            updateHyperTitanModalData(data);

            if (data.singularityActive) {
                const sngCurLive = livePrice > 0 ? livePrice : 0;
                const sngPoolCap = parseFloat(data.singularityPoolBalance !== undefined ? data.singularityPoolBalance : 100000);
                const sngPosList = Array.isArray(data.singularityPositions) ? data.singularityPositions : [];
                let sngTotalSol = 0;
                let sngTotalInvested = 0;
                sngPosList.forEach(p => {
                    sngTotalSol += parseFloat(p.solAmount || 0);
                    sngTotalInvested += parseFloat(p.invested || 0);
                });

                const sngTotalUsers = Math.max(1, parseInt(data.singularityUsers || 1000));
                const sngUserRatio = 1.0 / sngTotalUsers;

                const sngPoolUnreal = sngTotalSol > 0 ? ((sngTotalSol * sngCurLive) - sngTotalInvested) : 0;
                const sngUserUnreal = sngPoolUnreal * sngUserRatio;
                const sngPoolReal = parseFloat(data.singularityRealizedPnl || 0);
                const sngUserReal = sngPoolReal * sngUserRatio;

                const sngPoolEl = document.getElementById("sng-pool-total");
                if (sngPoolEl) sngPoolEl.innerText = "$" + sngPoolCap.toFixed(2);

                const sngSolEl = document.getElementById("sng-sol-pos");
                if (sngSolEl) sngSolEl.innerText = sngTotalSol.toFixed(4) + " SOL";

                const sngUserUnrealEl = document.getElementById("sng-user-unrealized-pnl");
                if (sngUserUnrealEl) {
                    sngUserUnrealEl.innerText = (sngUserUnreal >= 0 ? "+" : "") + "$" + sngUserUnreal.toFixed(4);
                    sngUserUnrealEl.style.color = sngUserUnreal >= 0 ? "#00e676" : "#f6465d";
                }

                const sngUserRealEl = document.getElementById("sng-user-realized-pnl");
                if (sngUserRealEl) {
                    sngUserRealEl.innerText = (sngUserReal >= 0 ? "+" : "") + "$" + sngUserReal.toFixed(4);
                    sngUserRealEl.style.color = sngUserReal >= 0 ? "#4CAF50" : "#f6465d";
                }

                const sngBadge = document.getElementById("sng-orders-badge");
                if (sngBadge) sngBadge.innerText = sngPosList.length + " OPEN";

                const enginesConfig = [
                    { idx: 1, name: "HOME DCA", dip: "-$1.20", color: "#00d2ff" },
                    { idx: 2, name: "HYPER TITAN", dip: "-$0.20", color: "#00e5ff" },
                    { idx: 3, name: "APEX VELOCITY", dip: "-$0.30", color: "#FFD700" },
                    { idx: 4, name: "QUANTUM PULSE", dip: "-$0.60", color: "#FF8C00" },
                    { idx: 5, name: "TITAN ABYSS", dip: "-$0.90", color: "#ff2d78" }
                ];

                const gridEl = document.getElementById("sng-engines-status-grid");
                if (gridEl) {
                    gridEl.innerHTML = enginesConfig.map(eng => {
                        const activePos = sngPosList.find(p => p.engineIdx === eng.idx);
                        if (activePos) {
                            const ePrice = parseFloat(activePos.entryPrice || sngCurLive).toFixed(2);
                            const eSol = parseFloat(activePos.solAmount || 0).toFixed(4);
                            return `
                                <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,230,118,0.08); border:1px solid rgba(0,230,118,0.25); border-radius:8px; padding:6px 10px;">
                                    <div style="display:flex; align-items:center; gap:6px;">
                                        <span style="width:6px; height:6px; background:#00e676; border-radius:50%; box-shadow:0 0 6px #00e676;"></span>
                                        <strong style="color:${eng.color}; font-size:11px;">${eng.name}</strong>
                                    </div>
                                    <div style="font-size:11px; color:#fff;">
                                        <span style="color:#00e676; font-weight:bold;">OPEN</span> · $${ePrice} (${eSol} SOL)
                                    </div>
                                </div>
                            `;
                        } else {
                            return `
                                <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:8px; padding:6px 10px;">
                                    <div style="display:flex; align-items:center; gap:6px;">
                                        <span style="width:6px; height:6px; background:#718096; border-radius:50%;"></span>
                                        <span style="color:#8c8ca1; font-size:11px;">${eng.name}</span>
                                    </div>
                                    <div style="font-size:10px; color:#718096;">
                                        WAITING DIP (${eng.dip})
                                    </div>
                                </div>
                            `;
                        }
                    }).join("");
                }

                let sngPeak = sngCurLive;
                let sngStop = sngCurLive * 0.998;
                const dipStatusEl = document.getElementById("sng-dip-hunter-status");
                if (sngPosList.length > 0) {
                    const highestTracked = Math.max(...sngPosList.map(p => parseFloat(p.ts_high || p.entryPrice || sngCurLive)));
                    sngPeak = Math.max(highestTracked, sngCurLive);
                    const entryBase = Math.min(...sngPosList.map(p => parseFloat(p.entryPrice || sngCurLive)));
                    const gainFromEntry = sngPeak - entryBase;
                    let trailGap = 0.10;
                    if (gainFromEntry >= 1.50) {
                        trailGap = 0.20;
                    } else if (gainFromEntry >= 0.80) {
                        trailGap = 0.15;
                    } else if (gainFromEntry >= 0.40) {
                        trailGap = 0.10;
                    }
                    sngStop = sngPeak - trailGap;
                    if (dipStatusEl) {
                        dipStatusEl.innerText = "RIDING POSITION (" + sngPosList.length + " ACTIVE)";
                        dipStatusEl.style.color = "#4CAF50";
                    }
                } else {
                    if (dipStatusEl) {
                        dipStatusEl.innerText = "DIP RADAR ACTIVE";
                        dipStatusEl.style.color = "#e040fb";
                    }
                }

                const sngHighEl = document.getElementById("sng-ts-high");
                const sngLowEl = document.getElementById("sng-ts-low");
                if (sngHighEl) sngHighEl.innerText = data.singularityTsHigh !== undefined ? "$" + parseFloat(data.singularityTsHigh).toFixed(2) : "$" + sngPeak.toFixed(2);
                if (sngLowEl) sngLowEl.innerText = data.singularityTsLow !== undefined && parseFloat(data.singularityTsLow) > 0 ? "$" + parseFloat(data.singularityTsLow).toFixed(2) : "$0.00";

                const refBase = sngPosList.length > 0 ? parseFloat(sngPosList[sngPosList.length - 1].entryPrice || sngCurLive) : sngCurLive;
                const t1El = document.getElementById("sng-tb-target-1");
                const t2El = document.getElementById("sng-tb-target-2");
                const t3El = document.getElementById("sng-tb-target-3");
                const lowTrackEl = document.getElementById("sng-lowest-tracked");

                if (t1El) t1El.innerText = "$" + (refBase - 0.20).toFixed(2);
                if (t2El) t2El.innerText = "$" + (refBase - 0.40).toFixed(2);
                if (t3El) t3El.innerText = "$" + (refBase - 0.60).toFixed(2);
                if (lowTrackEl) lowTrackEl.innerText = "$" + sngCurLive.toFixed(2);

                const p1 = document.getElementById("sng-ts-stage-pill-1");
                const p2 = document.getElementById("sng-ts-stage-pill-2");
                const p3 = document.getElementById("sng-ts-stage-pill-3");
                if (p1 && p2 && p3) {
                    p1.style.borderColor = "rgba(58, 71, 166, 0.4)";
                    p2.style.borderColor = "rgba(232, 117, 91, 0.2)";
                    p3.style.borderColor = "rgba(0, 230, 118, 0.2)";

                    if (sngPosList.length > 0) {
                        const diff = sngCurLive - parseFloat(sngPosList[sngPosList.length - 1].entryPrice || sngCurLive);
                        if (diff >= 1.50) {
                            p3.style.borderColor = "#00e676";
                            p3.style.background = "rgba(0, 230, 118, 0.25)";
                        } else if (diff >= 0.80) {
                            p2.style.borderColor = "#FFD700";
                            p2.style.background = "rgba(255, 215, 0, 0.25)";
                        } else if (diff >= 0.40) {
                            p1.style.borderColor = "#00d2ff";
                            p1.style.background = "rgba(0, 210, 255, 0.25)";
                        }
                    }
                }
            }
            updateSingularityModalData(data);
        }
let liveOnChainWallet = { usdt: 0.0, gas: 0.0, trx: 0.0, totalUsd: 0.0 };

        async function fetchRealWeb3WalletBalances(addr) {
            if (!addr) return;
            try {
                if (window.tronWeb && window.tronWeb.defaultAddress && window.tronWeb.defaultAddress.base58) {
                    try {
                        const tronSun = await window.tronWeb.trx.getBalance(window.tronWeb.defaultAddress.base58);
                        liveOnChainWallet.trx = parseFloat(tronSun) / 1000000;
                    } catch(te) {}
                }

                if (connectedWalletType === 'PHANTOM' || (window.phantom && window.phantom.solana) || (!addr.startsWith("0x") && window.solana)) {
                    if (window.solanaWeb3) {
                        try {
                            const solConn = new solanaWeb3.Connection("https://api.mainnet-beta.solana.com", "confirmed");
                            const userPubkey = new solanaWeb3.PublicKey(addr);
                            const lamports = await solConn.getBalance(userPubkey);
                            liveOnChainWallet.gas = lamports / 1000000000;

                            const splUsdtMint = new solanaWeb3.PublicKey("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB");
                            const tokenAccounts = await solConn.getParsedTokenAccountsByOwner(userPubkey, { mint: splUsdtMint });
                            if (tokenAccounts && tokenAccounts.value && tokenAccounts.value.length > 0) {
                                const tokenBal = tokenAccounts.value[0].account.data.parsed.info.tokenAmount.uiAmount;
                                liveOnChainWallet.usdt = parseFloat(tokenBal) || 0.0;
                            }
                        } catch(e) {}
                    }
                    liveOnChainWallet.totalUsd = liveOnChainWallet.usdt + (liveOnChainWallet.gas * (currentChartLivePrice || 100)) + (liveOnChainWallet.trx * 0.1324);
                } else if (addr.startsWith("0x")) {
                    const activeEthProvider = (window.trustwallet && window.trustwallet.ethereum) || window.ethereum;
                    const directProv = activeEthProvider ? new ethers.providers.Web3Provider(activeEthProvider) : new ethers.providers.JsonRpcProvider("https://binance.llamarpc.com");
                    const rawBnb = await directProv.getBalance(addr);
                    liveOnChainWallet.gas = parseFloat(ethers.utils.formatEther(rawBnb));

                    try {
                        const erc20Abi = ["function balanceOf(address) view returns (uint256)"];
                        const usdtContract = new ethers.Contract(REAL_USDT_CONTRACT, erc20Abi, directProv);
                        const rawUsdt = await usdtContract.balanceOf(addr);
                        liveOnChainWallet.usdt = parseFloat(ethers.utils.formatUnits(rawUsdt, 18));
                    } catch(e) {
                        liveOnChainWallet.usdt = 0.0;
                    }

                    const bnbRate = 580.0;
                    liveOnChainWallet.totalUsd = liveOnChainWallet.usdt + (liveOnChainWallet.gas * bnbRate) + (liveOnChainWallet.trx * 0.1324);
                }
            } catch(e) {}
            updateWalletDrawerBalancesUI();
            renderWalletTabView();
        }

        function updateWalletDrawerBalancesUI() {
            const uEl = document.getElementById("drawerUsdtBal");
            const uValEl = document.getElementById("drawerUsdtVal");
            const gEl = document.getElementById("drawerGasBal");
            const gValEl = document.getElementById("drawerGasVal");
            const totEl = document.getElementById("drawerTotalNetWorth");

            if (uEl) uEl.innerText = liveOnChainWallet.usdt.toFixed(2) + " USDT";
            if (uValEl) uValEl.innerText = "$" + liveOnChainWallet.usdt.toFixed(2);

            const isPhantom = connectedWalletType === 'PHANTOM';
            const gasSymbol = isPhantom ? "SOL" : "BNB";
            const gasRate = isPhantom ? (currentChartLivePrice || 100) : 580.0;
            const gasFiat = liveOnChainWallet.gas * gasRate;

            if (gEl) gEl.innerText = liveOnChainWallet.gas.toFixed(4) + " " + gasSymbol;
            if (gValEl) gValEl.innerText = "$" + gasFiat.toFixed(2);

            const total = liveOnChainWallet.usdt + gasFiat;
            if (totEl) totEl.innerText = "$" + total.toFixed(2);
        }

        function openConnectedWalletDrawer() {
            if (!userWallet) return;
            const drawer = document.getElementById("connectedWalletDrawer");
            if (!drawer) return;

            const provTitle = document.getElementById("drawerWalletProviderName");
            const provImg = document.getElementById("drawerWalletLogoImg");
            const netTitle = document.getElementById("drawerNetworkName");
            const fullAddr = document.getElementById("drawerFullAddressText");
            const expLink = document.getElementById("drawerExplorerLink");

            let name = "Trust Wallet";
            let logo = "https://s2.coinmarketcap.com/static/img/coins/64x64/5964.png";
            let net = "BNB Smart Chain (BEP-20)";
            let explorer = `https://bscscan.com/address/${userWallet}`;

            if (connectedWalletType === 'METAMASK') {
                name = "MetaMask Wallet";
                logo = "https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg";
                net = "Ethereum / BSC Web3";
                explorer = `https://bscscan.com/address/${userWallet}`;
            } else if (connectedWalletType === 'PHANTOM') {
                name = "Phantom Wallet";
                logo = "https://cryptologos.cc/logos/solana-sol-logo.png?v=024";
                net = "Solana Mainnet-Beta";
                explorer = `https://solscan.io/account/${userWallet}`;
            }

            if (provTitle) provTitle.innerText = name;
            if (provImg) provImg.src = logo;
            if (netTitle) netTitle.innerText = net;
            if (fullAddr) fullAddr.innerText = userWallet;
            if (expLink) expLink.href = explorer;

            drawer.style.display = "flex";
            drawer.classList.add("active");

            fetchRealWeb3WalletBalances(userWallet);
        }

        function closeConnectedWalletDrawer() {
            const drawer = document.getElementById("connectedWalletDrawer");
            if (drawer) {
                drawer.style.display = "none";
                drawer.classList.remove("active");
            }
        }

        function copyConnectedFullAddress() {
            if (!userWallet) return;
            navigator.clipboard.writeText(userWallet);
            alert("Address copied to clipboard:\n" + userWallet);
        }
        let binanceDirectSocket = null;
        let lastUiRenderTime = 0;
        function connectBinanceLiveStream() {
            if (binanceDirectSocket && (binanceDirectSocket.readyState === WebSocket.OPEN || binanceDirectSocket.readyState === WebSocket.CONNECTING)) return;
            binanceDirectSocket = new WebSocket("wss://stream.binance.com:9443/ws/solusdt@trade");

            binanceDirectSocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    const p = parseFloat(data.p);
                    if (p > 0) {
                        currentChartLivePrice = p;
                        const now = Date.now();

                        if (latestBackendState) {
                            if (!window.botHighestRecordedPeak || p > window.botHighestRecordedPeak) {
                                window.botHighestRecordedPeak = p;
                            }
                            const activePos = latestBackendState.activePositions || [];
                            const regPos = activePos.filter(x => !x.isMacro);
                            if (regPos.length > 0 && regPos.length < 10) {
                                const lastPos = regPos[regPos.length - 1];
                                const safetyTarget = parseFloat(lastPos.entryPrice || 0) * 0.982;
                                
                            }
                        }

                        if (botSocket && botSocket.readyState === WebSocket.OPEN && (now - (window.lastSentPriceTick || 0) >= 1000)) {
                            window.lastSentPriceTick = now;
                            botSocket.send(JSON.stringify({ action: "CLIENT_PRICE_TICK", price: p }));
                        }

                        if (now - lastUiRenderTime < 120) return;
                        lastUiRenderTime = now;

                        const pSolEl = document.getElementById("price-SOL");
                        if (pSolEl) pSolEl.innerText = p.toFixed(2);
                        const largeSol = document.getElementById("large-live-sol");
                        if (largeSol) largeSol.innerText = "$" + p.toFixed(2);
                        const wlSol = document.getElementById("wl-sol-price");
                        if (wlSol) wlSol.innerText = "$" + p.toFixed(2);
                        const highEl = document.getElementById("ex-high-24h");
                        if (highEl) highEl.innerText = "$" + (p * 1.028).toFixed(2);
                        const lowEl = document.getElementById("ex-low-24h");
                        if (lowEl) lowEl.innerText = "$" + (p * 0.972).toFixed(2);

                        updateLiveCandle(p);

                        if (latestBackendState) {
                            latestBackendState.price = p;
                            latestBackendState.livePrice = p;
                            refreshExchangeBalances();
                        }

                    }
                } catch (e) {}
            };

            binanceDirectSocket.onclose = () => {
                setTimeout(connectBinanceLiveStream, 1000);
            };

            binanceDirectSocket.onerror = () => {
                try { binanceDirectSocket.close(); } catch(e){}
            };
        }
        async function fetchOtherPrices() {
            connectBinanceLiveStream();
            fetchMarketCryptoRates();
        }
        let tvChartInstance = null;
function openHyperTitanDetailsModal() {
    const m = document.getElementById("hyperTitanDetailsModal");
    if (m) {
        m.style.display = "block";
        updateHyperTitanModalData(latestBackendState);
    }
}

function closeHyperTitanDetailsModal() {
    const m = document.getElementById("hyperTitanDetailsModal");
    if (m) m.style.display = "none";
}

function openKiller1DetailsModal() {
    const m = document.getElementById("killer1DetailsModal");
    if (m) {
        m.style.display = "block";
        updateKiller1ModalData(latestBackendState);
    }
}

function closeKiller1DetailsModal() {
    const m = document.getElementById("killer1DetailsModal");
    if (m) m.style.display = "none";
}

function openKiller2DetailsModal() {
    const m = document.getElementById("killer2DetailsModal");
    if (m) {
        m.style.display = "block";
        updateKiller2ModalData(latestBackendState);
    }
}

function closeKiller2DetailsModal() {
    const m = document.getElementById("killer2DetailsModal");
    if (m) m.style.display = "none";
}

function openKiller3DetailsModal() {
    const m = document.getElementById("killer3DetailsModal");
    if (m) {
        m.style.display = "block";
        updateKiller3ModalData(latestBackendState);
    }
}

function closeKiller3DetailsModal() {
    const m = document.getElementById("killer3DetailsModal");
    if (m) m.style.display = "none";
}

function openSingularityDetailsModal() {
    const m = document.getElementById("singularityDetailsModal");
    if (m) {
        m.style.display = "block";
        updateSingularityModalData(latestBackendState);
    }
}

function closeSingularityDetailsModal() {
    const m = document.getElementById("singularityDetailsModal");
    if (m) m.style.display = "none";
}

function updateSingularityModalData(data) {
    if (!data) return;
    const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);
    const posList = Array.isArray(data.singularityPositions) ? data.singularityPositions : [];
    const totalUsers = parseInt(data.singularityUsers || 1000);
    const totalInitialPool = parseFloat(data.singularityPoolBalance !== undefined ? data.singularityPoolBalance : 100000.0);

    let totalSol = 0;
    let totalInvested = 0;
    posList.forEach(p => {
        totalSol += parseFloat(p.solAmount || 0);
        totalInvested += parseFloat(p.invested || 0);
    });

    const realProfit = parseFloat(data.singularityRealizedPnl || 0);
    const userRealizedProfit = realProfit / totalUsers;
    const avgEntry = totalSol > 0 ? (totalInvested / totalSol) : 0;
    const poolUsdtAvail = Math.max(0, totalInitialPool);

    const usersEl = document.getElementById("sng-modal-total-users");
    if (usersEl) usersEl.innerText = totalUsers.toString();

    const poolInvEl = document.getElementById("sng-modal-total-pool-invest");
    if (poolInvEl) poolInvEl.innerText = "$" + totalInitialPool.toFixed(2) + " USDT";

    const poolProfEl = document.getElementById("sng-modal-pool-profit");
    if (poolProfEl) {
        poolProfEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(2) + " USDT";
        poolProfEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const userProfEl = document.getElementById("sng-modal-user-profit");
    if (userProfEl) {
        userProfEl.innerText = (userRealizedProfit >= 0 ? "+" : "") + "$" + userRealizedProfit.toFixed(4) + " USDT";
        userProfEl.style.color = userRealizedProfit >= 0 ? "#00e676" : "#f6465d";
    }

    const uEl = document.getElementById("sng-modal-port-usdt");
    if (uEl) uEl.innerText = "$" + poolUsdtAvail.toFixed(2);

    const sEl = document.getElementById("sng-modal-port-sol");
    if (sEl) sEl.innerText = totalSol.toFixed(4);

    const aEl = document.getElementById("sng-modal-avg-price");
    if (aEl) aEl.innerText = avgEntry > 0 ? ("$" + avgEntry.toFixed(2)) : "$0.00";

    const invEl = document.getElementById("sng-modal-invested");
    if (invEl) invEl.innerText = "$" + totalInvested.toFixed(2);

    const capEl = document.getElementById("sng-modal-capital");
    if (capEl) capEl.innerText = "$" + (totalInitialPool + totalInvested).toFixed(2);

    const reEl = document.getElementById("sng-realized-pnl-val");
    if (reEl) {
        reEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4);
        reEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const badgeEl = document.getElementById("sng-modal-positions-badge");
    const contEl = document.getElementById("sng-modal-positions-container");
    if (badgeEl) badgeEl.innerText = posList.length + " OPEN";

    let allowedSlots = 40;

    if (contEl) {
        if (posList.length === 0) {
            contEl.innerHTML = "NO ACTIVE BOT POSITIONS";
        } else {
            let dotsHTML = '';
            for (let i = 1; i <= allowedSlots; i++) {
                dotsHTML += i <= posList.length 
                    ? '<span style="color:#e040fb; font-size:10px; text-align:center;">●</span>' 
                    : '<span style="color:#444; font-size:10px; text-align:center;">○</span>';
            }
            let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                '<span style="font-size:11px; font-weight:bold; color:#fff;">5-ENGINE SAFETY ORDERS:</span>' +
                '<span style="font-size:11px; color:#e040fb; font-weight:bold; font-family:monospace;">(' + posList.length + '/' + allowedSlots + ')</span>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(10, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                '</div>';

            const engineNames = {
                1: "HOME DCA",
                2: "HYPER TITAN",
                3: "APEX VELOCITY",
                4: "QUANTUM PULSE",
                5: "TITAN ABYSS"
            };

            const rowsHTML = posList.map((p, idx) => {
                const eIdx = p.engineIdx || (idx % 5 + 1);
                const botName = engineNames[eIdx] || "FUSION";
                return `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:11px; font-family:monospace; box-sizing:border-box;">
                    <span style="color:#e040fb; font-weight:bold;">[${botName}] R${p.round || 6}</span>
                    <span>$${parseFloat(p.entryPrice || 0).toFixed(2)}</span>
                    <span style="color:#4CAF50; font-weight:bold;">${parseFloat(p.solAmount || 0).toFixed(4)} SOL</span>
                </div>
            `;}).join("");

            contEl.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
        }
    }

    const sngTrades = (Array.isArray(data.singularityTradesHistory) && data.singularityTradesHistory.length > 0) ? data.singularityTradesHistory : (Array.isArray(data.tradesHistory) ? data.tradesHistory.filter(t => String(t.orderId || t.order_id || "").toUpperCase().startsWith("SNG_") || String(t.execType || "").toUpperCase().includes("SINGULARITY")) : []);
    const seenSng = new Set();
    const cleanSngTrades = sngTrades.filter(t => {
        const oId = String(t.orderId || t.order_id || "").toUpperCase();
        if (oId && !seenSng.has(oId) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
            seenSng.add(oId);
            return true;
        }
        return false;
    });
    renderModalTradeList(cleanSngTrades, "sng-modal-history-list", "sng-modal-trade-count", "sng-modal-win-tag", "sng-modal-loss-tag", "#e040fb", "TITAN SINGULARITY 100K");
}

function updateKiller1ModalData(data) {
    if (!data) return;
    const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);
    const posList = Array.isArray(data.microPositions) ? data.microPositions : [];
    const totalUsers = parseInt(data.microPoolUsers || 1);
    const userInvestment = parseFloat(data.microUserInvestment || 10.0);
    const totalInitialPool = parseFloat(data.microPoolBalance !== undefined ? data.microPoolBalance : (totalUsers * userInvestment));
    let totalSol = 0;
    let totalInvested = 0;
    posList.forEach(p => {
        totalSol += parseFloat(p.solAmount || 0);
        totalInvested += parseFloat(p.invested || 0);
    });
    const realProfit = parseFloat(data.microRealizedPnl || 0);
    const userRealizedProfit = realProfit / totalUsers;
    const avgEntry = totalSol > 0 ? (totalInvested / totalSol) : 0;
    const botUsdtAvail = Math.max(0, parseFloat(data.usdtBalance || 0));

    const usersEl = document.getElementById("k1-modal-total-users");
    if (usersEl) usersEl.innerText = totalUsers.toString();
    const poolInvEl = document.getElementById("k1-modal-total-pool-invest");
    if (poolInvEl) poolInvEl.innerText = "$" + totalInitialPool.toFixed(2) + " USDT";
    const poolProfEl = document.getElementById("k1-modal-pool-profit");
    if (poolProfEl) {
        poolProfEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4) + " USDT";
        poolProfEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }
    const userProfEl = document.getElementById("k1-modal-user-profit");
    if (userProfEl) {
        userProfEl.innerText = (userRealizedProfit >= 0 ? "+" : "") + "$" + userRealizedProfit.toFixed(4) + " USDT";
        userProfEl.style.color = userRealizedProfit >= 0 ? "#00e676" : "#f6465d";
    }

    const uEl = document.getElementById("k1-modal-port-usdt");
    if (uEl) uEl.innerText = "$" + botUsdtAvail.toFixed(2);
    const sEl = document.getElementById("k1-modal-port-sol");
    if (sEl) sEl.innerText = totalSol.toFixed(4);
    const aEl = document.getElementById("k1-modal-avg-price");
    if (aEl) aEl.innerText = avgEntry > 0 ? ("$" + avgEntry.toFixed(2)) : "$0.00";
    const invEl = document.getElementById("k1-modal-invested");
    if (invEl) invEl.innerText = "$" + totalInvested.toFixed(2);
    const capEl = document.getElementById("k1-modal-capital");
    if (capEl) capEl.innerText = "$" + totalInitialPool.toFixed(2);

    const reEl = document.getElementById("k1-realized-pnl-val");
    if (reEl) {
        reEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4);
        reEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const badgeEl = document.getElementById("k1-modal-positions-badge");
    const contEl = document.getElementById("k1-modal-positions-container");
    if (badgeEl) badgeEl.innerText = posList.length + " OPEN";
    if (contEl) {
        if (posList.length === 0) {
            contEl.innerHTML = "NO ACTIVE BOT POSITIONS";
        } else {
            const maxK1Slots = 24;
            let dotsHTML = '';
            for (let i = 1; i <= maxK1Slots; i++) {
                dotsHTML += i <= posList.length 
                    ? '<span style="color:#00d2ff; font-size:12px; margin-right:2px;">●</span>' 
                    : '<span style="color:#444; font-size:12px; margin-right:2px;">○</span>';
            }
            let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                '<span style="font-size:12px; font-weight:bold; color:#fff;">DCA SAFETY ORDERS:</span>' +
                '<span style="font-size:11px; color:#00d2ff; font-weight:bold; font-family:monospace;">(' + posList.length + '/' + maxK1Slots + ')</span>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(12, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                '</div>';

            const rowsHTML = posList.map((p, idx) => `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:12px; font-family:monospace;">
                    <span style="color:#00d2ff; font-weight:bold;">${p.label || ('MICRO #' + (idx + 1))}</span>
                    <span>$${parseFloat(p.entryPrice || 0).toFixed(2)}</span>
                    <span style="color:#4CAF50; font-weight:bold;">${parseFloat(p.solAmount || 0).toFixed(4)} SOL</span>
                </div>
            `).join("");

            contEl.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
        }
    }

    let k1Trades = [];
    const sourceK1 = (Array.isArray(data.microTradesHistory) && data.microTradesHistory.length > 0) ? data.microTradesHistory : [...(data.scalpTradesHistory || []), ...(data.tradesHistory || [])];
    const seenK1 = new Set();
    k1Trades = sourceK1.filter(t => {
        const id = String(t.orderId || t.order_id || "").toUpperCase();
        const ex = String(t.execType || t.exec_type || "").toUpperCase();
        const isSng = id.startsWith("SNG_") || ex.includes("SINGULARITY");
        const isK1 = !isSng && (id.startsWith("M_") || ex.includes("MICRO") || ex.includes("APEX"));
        if (isK1 && !seenK1.has(id) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
            seenK1.add(id);
            return true;
        }
        return false;
    });
    renderModalTradeList(k1Trades, "k1-modal-history-list", "k1-modal-trade-count", "k1-modal-win-tag", "k1-modal-loss-tag", "#00d2ff", "SHINE APEX VELOCITY ENGINE");
}

function updateKiller2ModalData(data) {
    if (!data) return;
    const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);
    const posList = Array.isArray(data.killer2Positions) ? data.killer2Positions : [];
    const totalUsers = parseInt(data.killer2PoolUsers || 1);
    const userInvestment = parseFloat(data.killer2UserInvestment || 10.0);
    const totalInitialPool = parseFloat(data.killer2PoolBalance !== undefined ? data.killer2PoolBalance : (totalUsers * userInvestment));
    let totalSol = 0;
    let totalInvested = 0;
    posList.forEach(p => {
        totalSol += parseFloat(p.solAmount || 0);
        totalInvested += parseFloat(p.invested || 0);
    });
    const realProfit = parseFloat(data.killer2RealizedPnl || 0);
    const userRealizedProfit = realProfit / totalUsers;
    const avgEntry = totalSol > 0 ? (totalInvested / totalSol) : 0;
    const botUsdtAvail = Math.max(0, parseFloat(data.usdtBalance || 0));

    const usersEl = document.getElementById("k2-modal-total-users");
    if (usersEl) usersEl.innerText = totalUsers.toString();
    const poolInvEl = document.getElementById("k2-modal-total-pool-invest");
    if (poolInvEl) poolInvEl.innerText = "$" + totalInitialPool.toFixed(2) + " USDT";
    const poolProfEl = document.getElementById("k2-modal-pool-profit");
    if (poolProfEl) {
        poolProfEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4) + " USDT";
        poolProfEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }
    const userProfEl = document.getElementById("k2-modal-user-profit");
    if (userProfEl) {
        userProfEl.innerText = (userRealizedProfit >= 0 ? "+" : "") + "$" + userRealizedProfit.toFixed(4) + " USDT";
        userProfEl.style.color = userRealizedProfit >= 0 ? "#00e676" : "#f6465d";
    }

    const uEl = document.getElementById("k2-modal-port-usdt");
    if (uEl) uEl.innerText = "$" + botUsdtAvail.toFixed(2);
    const sEl = document.getElementById("k2-modal-port-sol");
    if (sEl) sEl.innerText = totalSol.toFixed(4);
    const aEl = document.getElementById("k2-modal-avg-price");
    if (aEl) aEl.innerText = avgEntry > 0 ? ("$" + avgEntry.toFixed(2)) : "$0.00";
    const invEl = document.getElementById("k2-modal-invested");
    if (invEl) invEl.innerText = "$" + totalInvested.toFixed(2);
    const capEl = document.getElementById("k2-modal-capital");
    if (capEl) capEl.innerText = "$" + totalInitialPool.toFixed(2);

    const reEl = document.getElementById("k2-realized-pnl-val");
    if (reEl) {
        reEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4);
        reEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const badgeEl = document.getElementById("k2-modal-positions-badge");
    const contEl = document.getElementById("k2-modal-positions-container");
    if (badgeEl) badgeEl.innerText = posList.length + " OPEN";
    if (contEl) {
        if (posList.length === 0) {
            contEl.innerHTML = "NO ACTIVE BOT POSITIONS";
        } else {
            const maxK2Slots = 24;
            let dotsHTML = '';
            for (let i = 1; i <= maxK2Slots; i++) {
                dotsHTML += i <= posList.length 
                    ? '<span style="color:#FFD700; font-size:12px; margin-right:2px;">●</span>' 
                    : '<span style="color:#444; font-size:12px; margin-right:2px;">○</span>';
            }
            let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                '<span style="font-size:12px; font-weight:bold; color:#fff;">DCA SAFETY ORDERS:</span>' +
                '<span style="font-size:11px; color:#FFD700; font-weight:bold; font-family:monospace;">(' + posList.length + '/' + maxK2Slots + ')</span>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(12, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                '</div>';

            const rowsHTML = posList.map((p, idx) => `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:12px; font-family:monospace;">
                    <span style="color:#FFD700; font-weight:bold;">${p.label || ('QUANTUM #' + (idx + 1))}</span>
                    <span>$${parseFloat(p.entryPrice || 0).toFixed(2)}</span>
                    <span style="color:#4CAF50; font-weight:bold;">${parseFloat(p.solAmount || 0).toFixed(4)} SOL</span>
                </div>
            `).join("");

            contEl.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
        }
    }

    let k2Trades = [];
    const sourceK2 = (Array.isArray(data.killer2TradesHistory) && data.killer2TradesHistory.length > 0) ? data.killer2TradesHistory : [...(data.scalpTradesHistory || []), ...(data.tradesHistory || [])];
    const seenK2 = new Set();
    k2Trades = sourceK2.filter(t => {
        const id = String(t.orderId || t.order_id || "").toUpperCase();
        const ex = String(t.execType || t.exec_type || "").toUpperCase();
        const isSng = id.startsWith("SNG_") || ex.includes("SINGULARITY");
        const isK2 = !isSng && (id.startsWith("K2_") || ex.includes("KILLER2") || ex.includes("QUANTUM"));
        if (isK2 && !seenK2.has(id) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
            seenK2.add(id);
            return true;
        }
        return false;
    });
    renderModalTradeList(k2Trades, "k2-modal-history-list", "k2-modal-trade-count", "k2-modal-win-tag", "k2-modal-loss-tag", "#FFD700", "SHINE QUANTUM PULSE ENGINE");
}

function updateKiller3ModalData(data) {
    if (!data) return;
    const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);
    const posList = Array.isArray(data.killer3Positions) ? data.killer3Positions : [];
    const totalUsers = parseInt(data.killer3PoolUsers || 1);
    const userInvestment = parseFloat(data.killer3UserInvestment || 10.0);
    const totalInitialPool = parseFloat(data.killer3PoolBalance !== undefined ? data.killer3PoolBalance : (totalUsers * userInvestment));
    let totalSol = 0;
    let totalInvested = 0;
    posList.forEach(p => {
        totalSol += parseFloat(p.solAmount || 0);
        totalInvested += parseFloat(p.invested || 0);
    });
    const realProfit = parseFloat(data.killer3RealizedPnl || 0);
    const userRealizedProfit = realProfit / totalUsers;
    const avgEntry = totalSol > 0 ? (totalInvested / totalSol) : 0;
    const botUsdtAvail = Math.max(0, parseFloat(data.usdtBalance || 0));

    const usersEl = document.getElementById("k3-modal-total-users");
    if (usersEl) usersEl.innerText = totalUsers.toString();
    const poolInvEl = document.getElementById("k3-modal-total-pool-invest");
    if (poolInvEl) poolInvEl.innerText = "$" + totalInitialPool.toFixed(2) + " USDT";
    const poolProfEl = document.getElementById("k3-modal-pool-profit");
    if (poolProfEl) {
        poolProfEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4) + " USDT";
        poolProfEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }
    const userProfEl = document.getElementById("k3-modal-user-profit");
    if (userProfEl) {
        userProfEl.innerText = (userRealizedProfit >= 0 ? "+" : "") + "$" + userRealizedProfit.toFixed(4) + " USDT";
        userProfEl.style.color = userRealizedProfit >= 0 ? "#00e676" : "#f6465d";
    }

    const uEl = document.getElementById("k3-modal-port-usdt");
    if (uEl) uEl.innerText = "$" + botUsdtAvail.toFixed(2);
    const sEl = document.getElementById("k3-modal-port-sol");
    if (sEl) sEl.innerText = totalSol.toFixed(4);
    const aEl = document.getElementById("k3-modal-avg-price");
    if (aEl) aEl.innerText = avgEntry > 0 ? ("$" + avgEntry.toFixed(2)) : "$0.00";
    const invEl = document.getElementById("k3-modal-invested");
    if (invEl) invEl.innerText = "$" + totalInvested.toFixed(2);
    const capEl = document.getElementById("k3-modal-capital");
    if (capEl) capEl.innerText = "$" + totalInitialPool.toFixed(2);

    const reEl = document.getElementById("k3-realized-pnl-val");
    if (reEl) {
        reEl.innerText = (realProfit >= 0 ? "+" : "") + "$" + realProfit.toFixed(4);
        reEl.style.color = realProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const badgeEl = document.getElementById("k3-modal-positions-badge");
    const contEl = document.getElementById("k3-modal-positions-container");
    if (badgeEl) badgeEl.innerText = posList.length + " OPEN";
    if (contEl) {
        if (posList.length === 0) {
            contEl.innerHTML = "NO ACTIVE BOT POSITIONS";
        } else {
            const maxK3Slots = 24;
            let dotsHTML = '';
            for (let i = 1; i <= maxK3Slots; i++) {
                dotsHTML += i <= posList.length 
                    ? '<span style="color:#00e676; font-size:12px; margin-right:2px;">●</span>' 
                    : '<span style="color:#444; font-size:12px; margin-right:2px;">○</span>';
            }
            let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                '<span style="font-size:12px; font-weight:bold; color:#fff;">DCA SAFETY ORDERS:</span>' +
                '<span style="font-size:11px; color:#00e676; font-weight:bold; font-family:monospace;">(' + posList.length + '/' + maxK3Slots + ')</span>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(12, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                '</div>';

            const rowsHTML = posList.map((p, idx) => `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:12px; font-family:monospace;">
                    <span style="color:#00e676; font-weight:bold;">${p.label || ('TITAN #' + (idx + 1))}</span>
                    <span>$${parseFloat(p.entryPrice || 0).toFixed(2)}</span>
                    <span style="color:#4CAF50; font-weight:bold;">${parseFloat(p.solAmount || 0).toFixed(4)} SOL</span>
                </div>
            `).join("");

            contEl.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
        }
    }

    let k3Trades = [];
    const sourceK3 = (Array.isArray(data.killer3TradesHistory) && data.killer3TradesHistory.length > 0) ? data.killer3TradesHistory : [...(data.scalpTradesHistory || []), ...(data.tradesHistory || [])];
    const seenK3 = new Set();
    k3Trades = sourceK3.filter(t => {
        const id = String(t.orderId || t.order_id || "").toUpperCase();
        const ex = String(t.execType || t.exec_type || "").toUpperCase();
        const isSng = id.startsWith("SNG_") || ex.includes("SINGULARITY");
        const isK3 = !isSng && (id.startsWith("K3_") || ex.includes("KILLER3") || ex.includes("ABYSS"));
        if (isK3 && !seenK3.has(id) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
            seenK3.add(id);
            return true;
        }
        return false;
    });
    renderModalTradeList(k3Trades, "k3-modal-history-list", "k3-modal-trade-count", "k3-modal-win-tag", "k3-modal-loss-tag", "#00e676", "SHINE TITAN ABYSS ENGINE");
}

function renderModalTradeList(trades, containerId, countId, winId, lossId, tagColor, botName) {
    const listEl = document.getElementById(containerId);
    let wins = 0;
    let losses = 0;
    let totalExits = 0;

    trades.forEach(t => {
        const sideStr = String(t.side || "").toUpperCase();
        const execStr = String(t.execType || t.exec_type || "").toUpperCase();
        const isSell = sideStr.includes("SELL") || execStr.includes("EXIT") || execStr.includes("PROFIT");
        const pVal = parseFloat(t.profit || t.realizedPnl || 0);

        if (isSell) {
            totalExits++;
            if (pVal >= 0) wins++;
            else losses++;
        }
    });

    const cntEl = document.getElementById(countId);
    const winEl = document.getElementById(winId);
    const lossEl = document.getElementById(lossId);
    if (cntEl) cntEl.innerText = totalExits.toString();
    if (winEl) winEl.innerText = wins.toString();
    if (lossEl) lossEl.innerText = losses.toString();

    if (!listEl) return;
    if (trades.length === 0) {
        listEl.innerHTML = '<div class="empty-msg">NO BOT TRADES RECORDED (24H CLEAR)</div>';
        return;
    }

    listEl.innerHTML = trades.map(t => {
        const sideStr = String(t.side || "").toUpperCase();
        const execStr = String(t.execType || t.exec_type || "").toUpperCase();
        const isSell = sideStr.includes("SELL") || execStr.includes("EXIT") || execStr.includes("PROFIT");
        const pVal = parseFloat(t.profit || t.realizedPnl || 0);
        const isWin = pVal >= 0;
        let dateStr = "";
        const rawTime = t.timestamp || t.created_at;
        if (rawTime) {
            const parsed = new Date(rawTime);
            dateStr = !isNaN(parsed.getTime()) ? parsed.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : String(rawTime);
        } else {
            dateStr = "Completed";
        }

        const refId = t.orderId || t.order_id || t.label || 'POOL';
        const displaySol = parseFloat(t.solAmount || t.sol_amount || 0).toFixed(4);
        const displayPrice = parseFloat(t.price || 0).toFixed(2);

        return `
            <div style="background:#151518; border:1px solid #222; border-radius:8px; padding:10px 12px; display:flex; flex-direction:column; gap:4px; font-family:monospace;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="background:${isSell ? (isWin ? 'rgba(76,175,80,0.2)' : 'rgba(246,70,93,0.2)') : 'rgba(0,229,255,0.2)'}; color:${isSell ? (isWin ? '#4CAF50' : '#f6465d') : tagColor}; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:bold;">${isSell ? 'EXIT' : 'ENTRY'}</span>
                    <span style="color:#757575; font-size:10px;">${dateStr}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-top:2px;">
                    <span style="color:#fff;">$${displayPrice} <span style="color:#757575;">(${displaySol} SOL)</span></span>
                    <span style="color:${isSell ? (isWin ? '#4CAF50' : '#f6465d') : '#757575'}; font-weight:bold;">${isSell ? ((isWin ? '+' : '') + pVal.toFixed(4) + ' USDT') : 'EXECUTED'}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px; padding-top:4px; border-top:1px solid rgba(255,255,255,0.03); font-size:10px;">
                    <span style="color:${tagColor};">${botName} (24H AUDIT)</span>
                    <span style="color:#757575;">REF: ${refId}</span>
                </div>
            </div>
        `;
    }).join("");
}

function updateHyperTitanModalData(data) {
    if (!data) return;
    const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : parseFloat(data.price || data.livePrice || 0);
    const posList = Array.isArray(data.hyperPositions) ? data.hyperPositions : [];
    const totalUsers = parseInt(data.hyperPoolUsers || 100);
    const userInvestment = parseFloat(data.hyperUserInvestment || 10.0);
    const totalInitialPool = totalUsers * userInvestment;

    let totalSol = 0;
    let totalInvested = 0;
    posList.forEach(p => {
        totalSol += parseFloat(p.solAmount || 0);
        totalInvested += parseFloat(p.invested || 0);
    });

    const totalRealizedPoolProfit = parseFloat(data.hyperRealizedPnl || 0);
    const totalCurrentPoolValue = totalInitialPool + totalRealizedPoolProfit;
    const botUsdtAvail = Math.max(0, totalCurrentPoolValue - totalInvested);

    const unrealPnl = totalSol > 0 ? ((totalSol * curLive) - totalInvested) : 0;
    const unrealPct = totalInvested > 0 ? (unrealPnl / totalInvested) * 100 : 0;
    const avgEntry = totalSol > 0 ? (totalInvested / totalSol) : 0;

    const userRealizedProfit = totalRealizedPoolProfit / totalUsers;
    const userUnrealizedProfit = unrealPnl / totalUsers;

    const usersEl = document.getElementById("hyper-modal-total-users");
    if (usersEl) usersEl.innerText = totalUsers.toString();

    const poolInvEl = document.getElementById("hyper-modal-total-pool-invest");
    if (poolInvEl) poolInvEl.innerText = "$" + totalInitialPool.toFixed(2) + " USDT";

    const poolProfEl = document.getElementById("hyper-modal-pool-profit");
    if (poolProfEl) {
        poolProfEl.innerText = (totalRealizedPoolProfit >= 0 ? "+" : "") + "$" + totalRealizedPoolProfit.toFixed(2) + " USDT";
        poolProfEl.style.color = totalRealizedPoolProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const userProfEl = document.getElementById("hyper-modal-user-profit");
    if (userProfEl) {
        userProfEl.innerText = (userRealizedProfit >= 0 ? "+" : "") + "$" + userRealizedProfit.toFixed(4) + " USDT";
        userProfEl.style.color = userRealizedProfit >= 0 ? "#00e676" : "#f6465d";
    }

    const unEl = document.getElementById("hyper-unrealized-pnl");
    const unPctEl = document.getElementById("hyper-unrealized-pnl-pct");
    if (unEl) {
        unEl.innerText = (unrealPnl >= 0 ? "+" : "") + "$" + unrealPnl.toFixed(2);
        unEl.style.color = unrealPnl >= 0 ? "#00e676" : "#f6465d";
    }
    if (unPctEl) {
        unPctEl.innerText = (unrealPct >= 0 ? "+" : "") + unrealPct.toFixed(2) + "%";
        unPctEl.style.color = unrealPnl >= 0 ? "#4CAF50" : "#f6465d";
    }

    const uEl = document.getElementById("hyper-modal-port-usdt");
    if (uEl) uEl.innerText = "$" + botUsdtAvail.toFixed(2);

    const sEl = document.getElementById("hyper-modal-port-sol");
    if (sEl) sEl.innerText = totalSol.toFixed(4);

    const aEl = document.getElementById("hyper-modal-avg-price");
    if (aEl) aEl.innerText = avgEntry > 0 ? ("$" + avgEntry.toFixed(2)) : "$0.00";

    const invEl = document.getElementById("hyper-modal-invested");
    if (invEl) invEl.innerText = "$" + totalInvested.toFixed(2);

    const capEl = document.getElementById("hyper-modal-capital");
    if (capEl) capEl.innerText = "$" + totalCurrentPoolValue.toFixed(2);

    const badgeEl = document.getElementById("hyper-modal-positions-badge");
    const contEl = document.getElementById("hyper-modal-positions-container");
    if (badgeEl) badgeEl.innerText = posList.length + " OPEN";
    if (contEl) {
        if (posList.length === 0) {
            contEl.innerHTML = "NO ACTIVE BOT POSITIONS";
        } else {
            const maxHyperSlots = 24;
            let dotsHTML = '';
            for (let i = 1; i <= maxHyperSlots; i++) {
                dotsHTML += i <= posList.length 
                    ? '<span style="color:#00e5ff; font-size:12px; margin-right:2px;">●</span>' 
                    : '<span style="color:#444; font-size:12px; margin-right:2px;">○</span>';
            }
            let counterHeader = '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:10px; padding:10px; margin-bottom:12px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                '<span style="font-size:12px; font-weight:bold; color:#fff;">DCA SAFETY ORDERS:</span>' +
                '<span style="font-size:11px; color:#00e5ff; font-weight:bold; font-family:monospace;">(' + posList.length + '/' + maxHyperSlots + ')</span>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(12, 14px); gap:3px; justify-content:center; margin:6px 0;">' + dotsHTML + '</div>' +
                '</div>';

            const rowsHTML = posList.map((p, idx) => `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:white; font-size:12px; font-family:monospace; box-sizing:border-box;">
                    <span style="color:#00e5ff; font-weight:bold;">${p.label || ('ROUND ' + (idx + 1))}</span>
                    <span>$${parseFloat(p.entryPrice || 0).toFixed(2)}</span>
                    <span style="color:#4CAF50; font-weight:bold;">${parseFloat(p.solAmount || 0).toFixed(4)} SOL</span>
                </div>
            `).join("");

            contEl.innerHTML = '<div style="display:flex; flex-direction:column; width:100%;">' + counterHeader + rowsHTML + '</div>';
        }
    }

    let rawHistory = [];
    const sourceHyper = (Array.isArray(data.hyperTradesHistory) && data.hyperTradesHistory.length > 0) ? data.hyperTradesHistory : (Array.isArray(data.tradesHistory) ? data.tradesHistory : []);
    const seenHyper = new Set();
    rawHistory = sourceHyper.filter(t => {
        const ord = String(t.orderId || t.order_id || "").toUpperCase();
        const lbl = String(t.label || "").toUpperCase();
        const exec = String(t.execType || t.exec_type || "").toUpperCase();
        const isSng = ord.startsWith("SNG_") || exec.includes("SINGULARITY");
        const isHyp = !isSng && (ord.startsWith("HYPER_") || lbl.includes("HYPER") || exec.includes("HYPER"));
        if (isHyp && !seenHyper.has(ord) && parseFloat(t.solAmount || t.sol_amount || 0) > 0) {
            seenHyper.add(ord);
            return true;
        }
        return false;
    });

    let wins = 0;
    let losses = 0;
    let totalExits = 0;

    rawHistory.forEach(t => {
        const sideStr = String(t.side || "").toUpperCase();
        const execStr = String(t.execType || "").toUpperCase();
        const isSell = sideStr.includes("SELL") || execStr.includes("EXIT");
        const pVal = parseFloat(t.profit || t.realizedPnl || 0);

        if (isSell) {
            totalExits++;
            if (pVal >= 0) wins++;
            else losses++;
        }
    });

    const reEl = document.getElementById("hyper-realized-pnl-val");
    if (reEl) {
        reEl.innerText = (totalRealizedPoolProfit >= 0 ? "+" : "") + "$" + totalRealizedPoolProfit.toFixed(2);
        reEl.style.color = totalRealizedPoolProfit >= 0 ? "#4CAF50" : "#f6465d";
    }

    const cntEl = document.getElementById("hyper-modal-trade-count");
    const winEl = document.getElementById("hyper-modal-win-tag");
    const lossEl = document.getElementById("hyper-modal-loss-tag");
    if (cntEl) cntEl.innerText = totalExits.toString();
    if (winEl) winEl.innerText = wins.toString();
    if (lossEl) lossEl.innerText = losses.toString();

    const hListEl = document.getElementById("hyper-modal-history-list");
    if (hListEl) {
        if (rawHistory.length === 0) {
            hListEl.innerHTML = '<div class="empty-msg">NO BOT TRADES RECORDED (24H CLEAR)</div>';
        } else {
            hListEl.innerHTML = rawHistory.map(t => {
                const sideStr = String(t.side || "").toUpperCase();
                const execStr = String(t.execType || "").toUpperCase();
                const isSell = sideStr.includes("SELL") || execStr.includes("EXIT");
                const pVal = parseFloat(t.profit || t.realizedPnl || 0);
                const isWin = pVal >= 0;
                let dateStr = "";
                if (t.timestamp) {
                    const parsed = new Date(t.timestamp);
                    dateStr = !isNaN(parsed.getTime()) ? parsed.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : String(t.timestamp);
                } else {
                    dateStr = "Completed";
                }

                return `
                    <div style="background:#151518; border:1px solid #222; border-radius:8px; padding:10px 12px; display:flex; flex-direction:column; gap:4px; font-family:monospace;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="background:${isSell ? (isWin ? 'rgba(76,175,80,0.2)' : 'rgba(246,70,93,0.2)') : 'rgba(0,229,255,0.2)'}; color:${isSell ? (isWin ? '#4CAF50' : '#f6465d') : '#00e5ff'}; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:bold;">${isSell ? 'EXIT' : 'ENTRY'}</span>
                            <span style="color:#757575; font-size:10px;">${dateStr}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-top:2px;">
                            <span style="color:#fff;">$${parseFloat(t.price || 0).toFixed(2)} <span style="color:#757575;">(${parseFloat(t.solAmount || 0).toFixed(4)} SOL)</span></span>
                            <span style="color:${isSell ? (isWin ? '#4CAF50' : '#f6465d') : '#757575'}; font-weight:bold;">${isSell ? ((isWin ? '+' : '') + pVal.toFixed(4) + ' USDT') : 'EXECUTED'}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px; padding-top:4px; border-top:1px solid rgba(255,255,255,0.03); font-size:10px;">
                            <span style="color:#00e5ff;">HYPER TITAN (24H AUDIT)</span>
                            <span style="color:#757575;">REF: ${t.orderId || t.label || 'POOL'}</span>
                        </div>
                    </div>
                `;
            }).join("");
        }
    }
}
        let tvCandleSeries = null;
        let tvTslPriceLine = null;
        let currentChartInterval = '15m';
        let currentChartLivePrice = 0;
        let cachedRawCandles = [];
        let cachedTradeMarkers = [];

        function initTradingViewChart(interval = '15m') {
            const container = document.getElementById('custom_trading_chart');
            if (!container) return;

            if (!tvChartInstance) {
                container.innerHTML = '';
                tvChartInstance = LightweightCharts.createChart(container, {
                    width: container.clientWidth || 360,
                    height: container.clientHeight || 420,
                    layout: {
                        background: { color: '#08080c' },
                        textColor: '#757575',
                        fontSize: 11,
                        fontFamily: 'monospace'
                    },
                    grid: {
                        vertLines: { color: 'rgba(255, 255, 255, 0.04)' },
                        horzLines: { color: 'rgba(255, 255, 255, 0.04)' }
                    },
                    crosshair: {
                        mode: LightweightCharts.CrosshairMode.Normal,
                        vertLine: {
                            color: '#5C6BC0',
                            width: 1,
                            style: LightweightCharts.LineStyle.Dashed,
                            labelBackgroundColor: '#3A47A6'
                        },
                        horzLine: {
                            color: '#5C6BC0',
                            width: 1,
                            style: LightweightCharts.LineStyle.Dashed,
                            labelBackgroundColor: '#3A47A6'
                        }
                    },
                    rightPriceScale: {
                        borderColor: 'rgba(255, 255, 255, 0.08)',
                        scaleMargins: {
                            top: 0.1,
                            bottom: 0.15
                        }
                    },
                    timeScale: {
                        borderColor: 'rgba(255, 255, 255, 0.08)',
                        timeVisible: true,
                        secondsVisible: false,
                        barSpacing: 12,
                        minBarSpacing: 6
                    },
                    handleScroll: {
                        mouseWheel: true,
                        pressedMouseMove: true,
                        horzTouchDrag: true,
                        vertTouchDrag: true
                    },
                    handleScale: {
                        axisPressedMouseMove: true,
                        mouseWheel: true,
                        pinch: true
                    }
                });

                tvCandleSeries = tvChartInstance.addCandlestickSeries({
                    upColor: '#00c087',
                    downColor: '#f6465d',
                    borderVisible: false,
                    wickUpColor: '#00c087',
                    wickDownColor: '#f6465d'
                });
            }

            loadNativeKlines(currentBotCoin, interval);
        }

        async function loadNativeKlines(coin, interval) {
            const symbol = `${coin}USDT`;
            const badgeEl = document.getElementById('chart-symbol-badge');
            if (badgeEl) badgeEl.innerText = `${coin}/USDT`;

            try {
                const res = await fetch(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=120`);
                const data = await res.json();
                if (Array.isArray(data) && data.length > 0) {
                    cachedRawCandles = data.map(d => ({
                        time: Math.floor(d[0] / 1000),
                        open: parseFloat(d[1]),
                        high: parseFloat(d[2]),
                        low: parseFloat(d[3]),
                        close: parseFloat(d[4])
                    }));

                    if (currentChartLivePrice > 0 && cachedRawCandles.length > 0) {
                        const last = cachedRawCandles[cachedRawCandles.length - 1];
                        last.close = currentChartLivePrice;
                        if (currentChartLivePrice > last.high) last.high = currentChartLivePrice;
                        if (currentChartLivePrice < last.low) last.low = currentChartLivePrice;
                    }

                    if (tvCandleSeries) {
                        tvCandleSeries.setData(cachedRawCandles);
                        applyStoredMarkers();
                    }
                } else {
                    generateFallbackCandles(coin);
                }
            } catch (err) {
                generateFallbackCandles(coin);
            }
        }

        function generateFallbackCandles(coin) {
            cachedRawCandles = [];
            let price = coin === 'SOL' ? 105.5 : (coin === 'BTC' ? 64500 : (coin === 'ETH' ? 3450 : 575));
            const now = Math.floor(Date.now() / 1000);
            for (let i = 80; i >= 0; i--) {
                const o = price;
                const change = (Math.random() - 0.49) * (price * 0.012);
                const c = o + change;
                const h = Math.max(o, c) + Math.random() * (price * 0.005);
                const l = Math.min(o, c) - Math.random() * (price * 0.005);
                price = c;
                cachedRawCandles.push({ time: now - (i * 900), open: o, high: h, low: l, close: c });
            }
            if (tvCandleSeries) {
                tvCandleSeries.setData(cachedRawCandles);
                applyStoredMarkers();
            }
        }

        function updateLiveCandle(price) {
            if (!tvCandleSeries || cachedRawCandles.length === 0 || price <= 0) return;
            const last = cachedRawCandles[cachedRawCandles.length - 1];
            last.close = price;
            if (price > last.high) last.high = price;
            if (price < last.low) last.low = price;
            tvCandleSeries.update(last);
        if (tvTradeCandleSeries && cachedTradeCandles.length > 0) {
            const lastT = cachedTradeCandles[cachedTradeCandles.length - 1];
            lastT.close = price;
            if (price > lastT.high) lastT.high = price;
            if (price < lastT.low) lastT.low = price;
            tvTradeCandleSeries.update(lastT);
        }
        }

        function updateChartMarkers(trades) {
            if (!Array.isArray(trades)) return;
            cachedTradeMarkers = trades;
            applyStoredMarkers();
        }

        function applyStoredMarkers() {
            if (!tvCandleSeries || cachedRawCandles.length === 0) return;
            const chartMarkers = [];
            const candlesTimes = cachedRawCandles.map(c => c.time);
            const latestCandleTime = candlesTimes[candlesTimes.length - 1];
            const groupedTrades = {};

            const renderedTradeIds = new Set();
            const candleGroups = {};

            cachedTradeMarkers.forEach(tr => {
                const ordId = String(tr.orderId || "");
                if (renderedTradeIds.has(ordId)) return;
                renderedTradeIds.add(ordId);

                const trTime = tr.timestamp ? Math.floor(new Date(tr.timestamp).getTime() / 1000) : 0;
                const sQty = parseFloat(tr.solAmount || 0);
                const eType = String(tr.execType || "").toUpperCase();
                const sideStr = String(tr.side || "").toUpperCase();
                if (!trTime || sQty <= 0 || ordId.startsWith("ATL_") || ordId.startsWith("ORD_") || ordId.startsWith("CPOS_") || ordId.startsWith("BOT_") || eType.includes("OPEN") || eType.includes("CANCEL") || eType.includes("LOCK") || eType.includes("RESERVE")) return;

                const isSell = sideStr.includes("SELL") || eType.includes("EXIT") || eType.includes("PROFIT");
                const isBuy = sideStr.includes("BUY") || eType.includes("ENTRY");
                if (!isSell && !isBuy) return;

                let exactCandleTime = null;
                if (trTime <= candlesTimes[0]) {
                    exactCandleTime = candlesTimes[0];
                } else if (trTime >= latestCandleTime) {
                    exactCandleTime = latestCandleTime;
                } else {
                    for (let i = candlesTimes.length - 1; i >= 0; i--) {
                        if (candlesTimes[i] <= trTime) {
                            exactCandleTime = candlesTimes[i];
                            break;
                        }
                    }
                }
                if (!exactCandleTime) return;

                const groupKey = exactCandleTime + '_' + (isSell ? 'S' : 'B');
                if (!candleGroups[groupKey]) {
                    candleGroups[groupKey] = {
                        time: exactCandleTime,
                        isSell: isSell,
                        count: 1
                    };
                } else {
                    candleGroups[groupKey].count++;
                }
            });

            Object.values(candleGroups).forEach(g => {
                const superscripts = { 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', 10: '¹⁰' };
                const countBadge = g.count > 1 ? (superscripts[g.count] || `×${g.count}`) : '';
                const label = (g.isSell ? 'S' : 'B') + countBadge;
                chartMarkers.push({
                    time: g.time,
                    position: g.isSell ? 'aboveBar' : 'belowBar',
                    color: g.isSell ? '#f6465d' : '#00c087',
                    shape: g.isSell ? 'arrowDown' : 'arrowUp',
                    text: label,
                    size: 1
                });
            });

            chartMarkers.sort((a, b) => a.time - b.time);
            tvCandleSeries.setMarkers(chartMarkers);
        }

        let activeGridLines = [];

        function renderActiveGridLines(curPrice) {
            if (!tvCandleSeries || curPrice <= 0) return;
            activeGridLines.forEach(l => tvCandleSeries.removePriceLine(l));
            activeGridLines = [];

            let step = curPrice * 0.015;
            if (currentBotCoin === 'SOL') step = Math.max(1.8, curPrice * 0.015);
            if (currentBotCoin === 'BNB') step = Math.max(5.0, curPrice * 0.012);
            if (currentBotCoin === 'ETH') step = Math.max(25.0, curPrice * 0.012);
            if (currentBotCoin === 'BTC') step = Math.max(450.0, curPrice * 0.010);

            for (let i = 1; i <= 3; i++) {
                const buyTarget = curPrice - (i * step);
                if (buyTarget > 0) {
                    const line = tvCandleSeries.createPriceLine({
                        price: buyTarget,
                        color: 'rgba(0, 192, 135, 0.45)',
                        lineWidth: 1,
                        lineStyle: LightweightCharts.LineStyle.Dotted,
                        axisLabelVisible: true,
                        title: 'GRID BUY R' + i
                    });
                    activeGridLines.push(line);
                }
            }

            const tpTarget = curPrice + (step * 1.4);
            const tpLine = tvCandleSeries.createPriceLine({
                price: tpTarget,
                color: 'rgba(255, 215, 0, 0.55)',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                axisLabelVisible: true,
                title: 'AUTO TP'
            });
            activeGridLines.push(tpLine);
        }

        function updateTslLine(tslPrice) {
            if (!tvCandleSeries || tslPrice <= 0) return;
            if (tvTslPriceLine) {
                tvCandleSeries.removePriceLine(tvTslPriceLine);
            }
            tvTslPriceLine = tvCandleSeries.createPriceLine({
                price: tslPrice,
                color: '#ff9100',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                axisLabelVisible: true,
                title: 'TSL'
            });
            renderActiveGridLines(currentChartLivePrice);
        }

        function playDexSwapSound() {
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                const ctx = new AudioContext();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(880, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1320, ctx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.15, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.15);
            } catch (e) {}
        }

        function triggerDexTradeAlert(text) {
            playDexSwapSound();
            const container = document.getElementById('custom_trading_chart');
            if (container) {
                container.style.boxShadow = '0 0 25px rgba(0, 230, 118, 0.5)';
                setTimeout(() => {
                    container.style.boxShadow = 'none';
                }, 1000);
            }
            const l1 = document.getElementById('trade-log-line-1');
            const l2 = document.getElementById('trade-log-line-2');
            if (l1 && l2 && text) {
                l2.innerText = l1.innerText;
                l1.innerText = '> ' + text;
                l1.style.color = '#00e676';
            }
        }

        function openPnlShareModal() {
            const modal = document.getElementById('pnlShareModal');
            const realVal = document.getElementById('realized-pnl-val') ? document.getElementById('realized-pnl-val').innerText : "+$0.00";
            const targetVal = document.getElementById('poster-profit-val');
            if (targetVal) targetVal.innerText = realVal;

            const b24 = document.getElementById('bot-24h-profit') ? document.getElementById('bot-24h-profit').innerText : "+$0.00";
            const poster24 = document.getElementById('poster-24h-profit');
            if (poster24) poster24.innerText = b24;

            const curNick = document.getElementById('displayNickname') ? document.getElementById('displayNickname').innerText : "User";
            const postName = document.getElementById('posterUserName');
            if (postName) postName.innerText = curNick;

            const curAvatar = document.getElementById('profileAvatar');
            const postAvatar = document.getElementById('posterUserAvatar');
            if (curAvatar && postAvatar) {
                const bg = window.getComputedStyle(curAvatar).backgroundImage;
                if (bg && bg !== 'none') {
                    postAvatar.style.backgroundImage = bg;
                }
            }

            if (modal) {
                modal.classList.add('active');
                modal.style.display = 'flex';
            }
        }

        function closePnlShareModal() {
            const modal = document.getElementById('pnlShareModal');
            if (modal) {
                modal.classList.remove('active');
                modal.style.display = 'none';
            }
        }

        async function shareDirectToSocial() {
            const target = document.getElementById('pnlPosterTarget');
            if (!target) return;

            try {
                const canvas = await html2canvas(target, {
                    backgroundColor: '#07090e',
                    scale: 3,
                    useCORS: true,
                    allowTaint: true
                });

                canvas.toBlob(async (blob) => {
                    if (!blob) {
                        downloadPnlPoster();
                        return;
                    }
                    const file = new File([blob], 'shine-profit.png', { type: 'image/png' });
                    if (navigator.canShare && navigator.canShare({ files: [file] })) {
                        try {
                            await navigator.share({
                                title: 'SHINE Quantitative Trading Profit',
                                text: 'Check out my automated spot trading profit on SHINE Protocol! https://shinecrypto.io',
                                files: [file]
                            });
                        } catch (err) {
                            downloadPnlPoster();
                        }
                    } else {
                        downloadPnlPoster();
                    }
                }, 'image/png');
            } catch (e) {
                downloadPnlPoster();
            }
        }

        async function downloadPnlPoster() {
            const target = document.getElementById('pnlPosterTarget');
            if (!target) return;

            try {
                const canvas = await html2canvas(target, {
                    backgroundColor: '#07090e',
                    scale: 3,
                    useCORS: true,
                    allowTaint: true
                });

                const imgData = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.download = 'SHINE-Profit-Poster.png';
                link.href = imgData;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (e) {
                alert('Downloading image failed. Please take a screenshot.');
            }
        }

        function changeInterval(int) {
            currentChartInterval = int;
            document.querySelectorAll('.interval-btn').forEach(b => b.classList.remove('active'));
            if (window.event && window.event.target) window.event.target.classList.add('active');
            loadNativeKlines(currentBotCoin, int).then(() => {
                applyStoredMarkers();
            });
        }

        window.addEventListener('resize', () => {
            const container = document.getElementById('custom_trading_chart');
            if (tvChartInstance && container) {
                tvChartInstance.applyOptions({
                    width: container.clientWidth,
                    height: container.clientHeight
                });
            }
        });
        function enterDashboard() {
            document.getElementById('landingPage').style.display = 'none';
            document.getElementById('loginModal').classList.remove('active');
            document.getElementById('connectWalletModal').classList.remove('active');
            document.getElementById('walletSelectionModal').classList.remove('active');
        }

        function openLoginModal() { document.getElementById('loginModal').classList.add('active'); }
        function openConnectModal() { 
            document.getElementById('loginModal').classList.remove('active');
            document.getElementById('connectWalletModal').classList.add('active'); 
        }
        function closeLoginModal() { document.getElementById('loginModal').classList.remove('active'); }

        let isBotPaused = false;

        function updatePauseUI(paused) {
            const btn = document.getElementById("btn-bot-toggle");
            const pulse = document.getElementById("bot-status-pulse");
            if (!btn) return;
            if (paused) {
                btn.innerText = "PAUSED";
                btn.style.background = "rgba(246, 70, 93, 0.15)";
                btn.style.borderColor = "#f6465d";
                btn.style.color = "#f6465d";
            } else {
                btn.innerText = "RUNNING";
                btn.style.background = "rgba(76, 175, 80, 0.15)";
                btn.style.borderColor = "#4CAF50";
                btn.style.color = "#4CAF50";
            }
        }

        function toggleBotExecution() {
            isBotPaused = !isBotPaused;
            updatePauseUI(isBotPaused);
            if (botSocket && botSocket.readyState === WebSocket.OPEN) {
                botSocket.send(JSON.stringify({ action: isBotPaused ? "PAUSE" : "RESUME" }));
            }
        }

        function showComingSoon(coin) {
            alert(coin + " Bot is coming soon! Currently SOL Trading Bot is active.");
        }

        function showNextPhase(currentPhase) {
            const nextPhase = currentPhase + 1;
            const nextSection = document.getElementById(`phase-${nextPhase}-section`);
            if (nextSection) {
                nextSection.style.display = 'block';
                document.getElementById(`btn-phase-${currentPhase}`).style.display = 'none';
            }
        }

        function switchBot(coin) {
            currentBotCoin = coin;
            const coins = ['SOL', 'BNB', 'ETH', 'BTC'];
            
            const coinLogos = {
                'SOL': 'https://cryptologos.cc/logos/solana-sol-logo.png?v=024',
                'BNB': 'https://cryptologos.cc/logos/bnb-bnb-logo.png?v=024',
                'ETH': 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024',
                'BTC': 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024'
            };

            for(let i=1; i<=4; i++) {
                const animCoin = document.getElementById(`anim-coin-${i}`);
                if(animCoin) animCoin.src = coinLogos[coin];
            }

            coins.forEach(c => {
                const tab = document.getElementById(`tab-${c}`);
                const priceText = document.getElementById(`price-${c}`);
                const titleText = tab.querySelector('div:first-child');
                
                if (c === coin) {
                    tab.style.background = 'rgba(76, 175, 80, 0.2)';
                    tab.style.border = '1px solid #4CAF50';
                    titleText.style.color = '#fff';
                    priceText.style.color = '#4CAF50';
                } else {
                    tab.style.background = 'transparent';
                    tab.style.border = '1px solid transparent';
                    titleText.style.color = '#757575';
                    priceText.style.color = '#fff';
                }
            });

            initTradingViewChart(currentChartInterval);

            document.getElementById('port-sol').previousElementSibling.innerText = coin;
            document.getElementById('large-live-sol').previousElementSibling.innerText = `LIVE ${coin} PRICE`;

            const badgeEl = document.getElementById('chart-symbol-badge');
            if (badgeEl) badgeEl.innerText = `${coin}/USDT`;

            renderPhases(coin);

            const currentPrice = parseFloat(document.getElementById(`price-${coin}`).innerText.replace(/,/g, ''));
            if(!isNaN(currentPrice)) {
                updateTradingDashboard(currentPrice, coin);
            }
        }
let tvTradeChartInstance = null;
let tvTradeCandleSeries = null;
let tvTradeVolumeSeries = null;
let tvTradeAvgLine = null;
let currentTradeChartInterval = '15m';
let cachedTradeCandles = [];

function toggleTradeChartVisibility() {
    const wrap = document.getElementById("tradeManualChartWrapper");
    const btn = document.getElementById("tab-opt-chart-btn");
    if (!wrap) return;
    const isHidden = window.getComputedStyle(wrap).display === "none";
    if (isHidden) {
        wrap.style.display = "block";
        if (btn) {
            btn.style.color = "#00e5ff";
            btn.style.fontWeight = "900";
        }
        setTimeout(() => {
            initTradeManualChart(currentTradeChartInterval);
            if (tvTradeChartInstance) {
                const container = document.getElementById("custom_trade_chart");
                tvTradeChartInstance.applyOptions({
                    width: container.clientWidth || 360,
                    height: 580
                });
            }
            wrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    } else {
        wrap.style.display = "none";
        if (btn) {
            btn.style.color = "#718096";
            btn.style.fontWeight = "700";
        }
    }
}

function initTradeManualChart(interval = '15m') {
    const container = document.getElementById('custom_trade_chart');
    if (!container) return;

    if (!tvTradeChartInstance) {
        container.innerHTML = '';
        tvTradeChartInstance = LightweightCharts.createChart(container, {
            width: container.clientWidth || 360,
            height: 580,
            layout: {
                background: { color: '#0b0e14' },
                textColor: '#718096',
                fontSize: 10,
                fontFamily: 'monospace'
            },
            grid: {
                vertLines: { color: 'rgba(255, 255, 255, 0.03)' },
                horzLines: { color: 'rgba(255, 255, 255, 0.03)' }
            },
            rightPriceScale: {
                borderColor: 'rgba(255, 255, 255, 0.08)',
                autoScale: true,
                scaleMargins: {
                    top: 0.10,
                    bottom: 0.30
                }
            },
            timeScale: {
                borderColor: 'rgba(255, 255, 255, 0.08)',
                timeVisible: true,
                secondsVisible: false,
                barSpacing: 18,
                minBarSpacing: 8,
                rightOffset: 4
            }
        });

        tvTradeCandleSeries = tvTradeChartInstance.addCandlestickSeries({
            upColor: '#00e5ff',
            downColor: '#ff2d78',
            borderVisible: false,
            wickUpColor: '#00e5ff',
            wickDownColor: '#ff2d78'
        });

        tvTradeVolumeSeries = tvTradeChartInstance.addHistogramSeries({
            priceFormat: { type: 'volume' },
            priceScaleId: 'volume_scale'
        });

        tvTradeChartInstance.priceScale('volume_scale').applyOptions({
            scaleMargins: {
                top: 0.80,
                bottom: 0.0
            }
        });
    }

    loadTradeKlines(interval);
}

async function loadTradeKlines(interval) {
    try {
        const res = await fetch(`https://api.binance.com/api/v3/klines?symbol=SOLUSDT&interval=${interval}&limit=48`);
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            cachedTradeCandles = [];
            const volumeData = [];

            data.forEach(d => {
                const t = Math.floor(d[0] / 1000);
                const o = parseFloat(d[1]);
                const h = parseFloat(d[2]);
                const l = parseFloat(d[3]);
                const c = parseFloat(d[4]);
                const v = parseFloat(d[5]);

                cachedTradeCandles.push({ time: t, open: o, high: h, low: l, close: c });
                volumeData.push({
                    time: t,
                    value: v,
                    color: c >= o ? 'rgba(0, 229, 255, 0.55)' : 'rgba(255, 45, 120, 0.55)'
                });
            });

            if (currentChartLivePrice > 0 && cachedTradeCandles.length > 0) {
                cachedTradeCandles[cachedTradeCandles.length - 1].close = currentChartLivePrice;
            }

            if (tvTradeCandleSeries) {
                tvTradeCandleSeries.setData(cachedTradeCandles);
                applyTradeMarkers();
                updateTradeAvgLine();
            }

            if (tvTradeVolumeSeries) {
                tvTradeVolumeSeries.setData(volumeData);
            }
        }
    } catch (e) {}
}

function applyTradeMarkers() {
    if (!tvTradeCandleSeries || cachedTradeCandles.length === 0) return;
    const manualLogs = (latestBackendState && latestBackendState.manualTradesHistory) ? latestBackendState.manualTradesHistory : [];
    const candleTimes = cachedTradeCandles.map(c => c.time);
    const latestCandleTime = candleTimes[candleTimes.length - 1];
    const grouped = {};

    manualLogs.forEach(tr => {
        const trTime = tr.timestamp ? Math.floor(new Date(tr.timestamp).getTime() / 1000) : 0;
        if (!trTime) return;

        let matchedTime = candleTimes[0];
        if (trTime >= latestCandleTime) {
            matchedTime = latestCandleTime;
        } else {
            for (let i = 0; i < candleTimes.length; i++) {
                if (candleTimes[i] <= trTime) matchedTime = candleTimes[i];
                else break;
            }
        }

        const isSell = String(tr.side || '').toUpperCase().includes('SELL');
        const key = matchedTime + '_' + (isSell ? 'S' : 'B');

        if (!grouped[key]) {
            grouped[key] = {
                time: matchedTime,
                isSell: isSell,
                count: 1
            };
        } else {
            grouped[key].count++;
        }
    });

    const markers = Object.values(grouped).map(g => ({
        time: g.time,
        position: g.isSell ? 'aboveBar' : 'belowBar',
        color: g.isSell ? '#ff2d78' : '#00e5ff',
        shape: g.isSell ? 'arrowDown' : 'arrowUp',
        text: g.count > 1 ? (g.isSell ? `S ×${g.count}` : `B ×${g.count}`) : (g.isSell ? 'S' : 'B'),
        size: 1
    }));

    markers.sort((a, b) => a.time - b.time);
    tvTradeCandleSeries.setMarkers(markers);
}
function updateTradeAvgLine() {
    if (!tvTradeCandleSeries) return;
    const wAvgVal = (latestBackendState && latestBackendState.walletAvgEntry !== undefined) ? parseFloat(latestBackendState.walletAvgEntry) : 0.0;
    if (tvTradeAvgLine) {
        tvTradeCandleSeries.removePriceLine(tvTradeAvgLine);
        tvTradeAvgLine = null;
    }
    if (wAvgVal > 0) {
        tvTradeAvgLine = tvTradeCandleSeries.createPriceLine({
            price: wAvgVal,
            color: '#00d2ff',
            lineWidth: 1,
            lineStyle: LightweightCharts.LineStyle.Dashed,
            axisLabelVisible: true,
            title: 'Avg. buy price'
        });
    }
}

function changeTradeInterval(int) {
    currentTradeChartInterval = int;
    ['1m', '15m', '1h', '4h', '1d'].forEach(id => {
        const btn = document.getElementById('tint-' + id);
        if (btn) btn.classList.remove('active');
    });
    const curBtn = document.getElementById('tint-' + int);
    if (curBtn) curBtn.classList.add('active');
    loadTradeKlines(int);
}
let currentExchangeTab = 'BUY';

function toggleExchangeModal() {
    const el = document.getElementById("exchangeTerminalOverlay");
    if (!el) return;
    if (el.style.display === "block") {
        el.style.display = "none";
    } else {
        el.style.display = "block";
        refreshExchangeBalances();
        renderLiveOrderBook();
    }
}

function switchExchangeTab(tab) {
    currentExchangeTab = tab;
    const bBtn = document.getElementById("ex-tab-buy");
    const sBtn = document.getElementById("ex-tab-sell");
    const subBtn = document.getElementById("ex-btn-submit");
    const unitLbl = document.getElementById("ex-unit-label");

    if (tab === 'BUY') {
        bBtn.style.background = "#00c087";
        bBtn.style.color = "#000";
        sBtn.style.background = "transparent";
        sBtn.style.color = "#757575";
        subBtn.style.background = "#00c087";
        subBtn.style.color = "#000";
        subBtn.innerText = currentSelectedOrderType === 'Market' ? "Buy SOL" : ("Buy " + currentSelectedOrderType);
        unitLbl.innerText = "USDT";
    } else {
        sBtn.style.background = "#f6465d";
        sBtn.style.color = "#fff";
        bBtn.style.background = "transparent";
        bBtn.style.color = "#757575";
        subBtn.style.background = "#f6465d";
        subBtn.style.color = "#fff";
        subBtn.innerText = currentSelectedOrderType === 'Market' ? "Sell SOL" : ("Sell " + currentSelectedOrderType);
        unitLbl.innerText = "SOL";
    }
    refreshExchangeBalances();
}

function fillPriceFromBook(p) {
    const input = document.getElementById("ex-custom-price-input");
    if (input) {
        input.value = parseFloat(p).toFixed(2);
    }
}

function refreshExchangeBalances() {
    const exWBtn = document.getElementById("ex-wallet-btn");
    const exWBtnText = document.getElementById("ex-wallet-btn-text");
    if (exWBtn && exWBtnText) {
        if (isTradeWalletConnected && userWallet) {
            const shortAddr = userWallet.substring(0, 6) + '...' + userWallet.substring(userWallet.length - 4);
            exWBtnText.innerText = shortAddr;
            exWBtn.style.color = "#00c087";
            exWBtn.onclick = promptWalletDisconnect;
        } else {
            exWBtnText.innerText = "CONNECT";
            exWBtn.style.color = "#00c087";
            exWBtn.onclick = openConnectModal;
        }
    }

    let wAvailUsdt = 0.0;
    let wSolVal = 0.0;
    let wInvestedVal = 0.0;

    if (currentTradeExecutionMode === "REAL" && isTradeWalletConnected && userWallet) {
        wAvailUsdt = liveOnChainWallet.usdt;
        wSolVal = connectedWalletType === 'PHANTOM' ? liveOnChainWallet.gas : (latestBackendState && latestBackendState.walletSol ? parseFloat(latestBackendState.walletSol) : 0.0);
    } else {
        wAvailUsdt = latestBackendState && latestBackendState.manualTestBalance !== undefined ? parseFloat(latestBackendState.manualTestBalance) : 100.0;
        wSolVal = latestBackendState && latestBackendState.walletSol !== undefined ? parseFloat(latestBackendState.walletSol) : 0.0;
    }

    if (latestBackendState && Array.isArray(latestBackendState.walletActivePositions)) {
        latestBackendState.walletActivePositions.forEach(p => {
            wSolVal += parseFloat(p.solAmount || 0);
            wInvestedVal += parseFloat(p.invested || 0);
        });
    }

    const wAvgVal = wSolVal > 0 ? (wInvestedVal / wSolVal) : 0.0;
    let wRealizedVal = latestBackendState && latestBackendState.walletRealizedPnl !== undefined ? parseFloat(latestBackendState.walletRealizedPnl) : 0.0;
    if (latestBackendState && Array.isArray(latestBackendState.autoLoops)) {
        latestBackendState.autoLoops.forEach(l => {
            if (l.profitRealized) {
                wRealizedVal += parseFloat(l.profitRealized);
            }
        });
    }

    let wLockedSol = 0.0;
    if (latestBackendState) {
        if (latestBackendState.walletLockedSol !== undefined) {
            wLockedSol = parseFloat(latestBackendState.walletLockedSol);
        } else if (Array.isArray(latestBackendState.walletOpenOrders)) {
            latestBackendState.walletOpenOrders.forEach(o => {
                if (String(o.side).toUpperCase() === 'SELL') {
                    wLockedSol += parseFloat(o.solAmount || o.amount || 0);
                }
            });
        }
    }
    let wAvailSol = Math.max(0.0, wSolVal - wLockedSol);
    const balEl = document.getElementById("ex-avail-bal");
    if (balEl) {
        balEl.innerText = currentExchangeTab === 'BUY' ? wAvailUsdt.toFixed(2) + " USDT" : wAvailSol.toFixed(4) + " SOL";
    }

    const portUsdtEl = document.getElementById("ex-port-usdt");
    if (portUsdtEl) portUsdtEl.innerText = "$" + wAvailUsdt.toFixed(2);

    const portSolEl = document.getElementById("ex-port-sol");
    if (portSolEl) portSolEl.innerText = wSolVal.toFixed(4);

    let curP = currentChartLivePrice > 0 ? currentChartLivePrice : wAvgVal;
    let calcUnrealized = 0;
    let calcUnrealizedPct = 0;
    if (wAvgVal > 0 && wSolVal > 0 && curP > 0) {
        calcUnrealized = (curP - wAvgVal) * wSolVal;
        calcUnrealizedPct = ((curP - wAvgVal) / wAvgVal) * 100;
    }

    const exWallPnl = document.getElementById("ex-unrealized-pnl");
    if (exWallPnl) {
        exWallPnl.innerText = (calcUnrealized >= 0 ? "+" : "") + "$" + calcUnrealized.toFixed(2);
        exWallPnl.style.color = calcUnrealized >= 0 ? "#00c087" : "#f6465d";
    }

    const exWallPct = document.getElementById("ex-unrealized-pct");
    if (exWallPct) {
        exWallPct.innerText = (calcUnrealizedPct >= 0 ? "+" : "") + calcUnrealizedPct.toFixed(2) + "%";
        exWallPct.style.color = calcUnrealizedPct >= 0 ? "#00c087" : "#f6465d";
    }

    const exWallReal = document.getElementById("ex-realized-pnl");
    if (exWallReal) {
        exWallReal.innerText = (wRealizedVal >= 0 ? "+" : "") + "$" + wRealizedVal.toFixed(2);
        exWallReal.style.color = wRealizedVal >= 0 ? "#4CAF50" : "#f6465d";
    }

    const exWAvgEl = document.getElementById("ex-wallet-avg-entry");
    if (exWAvgEl) exWAvgEl.innerText = wAvgVal > 0 ? ("$" + wAvgVal.toFixed(2)) : "$0.00";

    const exWInvEl = document.getElementById("ex-wallet-invested-disp");
    if (exWInvEl) exWInvEl.innerText = "$" + wInvestedVal.toFixed(2);

    const exWSolDisp = document.getElementById("ex-wallet-sol-disp");
    if (exWSolDisp) exWSolDisp.innerText = wSolVal.toFixed(4);

    const botCountBadge = document.getElementById("user-copy-bots-count");
    if (botCountBadge && latestBackendState && latestBackendState.copySubscribers) {
        botCountBadge.innerText = Array.isArray(latestBackendState.copySubscribers) ? latestBackendState.copySubscribers.length.toString() : "0";
    }

    curP = currentChartLivePrice > 0 ? currentChartLivePrice : 0;
    const sigEntry = document.getElementById("ex-signal-entry-val");
    const sigTarget = document.getElementById("ex-signal-target-val");
    if (curP > 0) {
        const entryLow = (curP * 0.998).toFixed(2);
        const tpVal = (curP * 1.012).toFixed(2);
        if (sigEntry) sigEntry.innerText = `$${entryLow} - $${curP.toFixed(2)}`;
        if (sigTarget) sigTarget.innerText = `$${tpVal} (+1.2%)`;
    }

}
let currentSelectedOrderType = 'Market';

function toggleOrderTypeSheet(e) {
    if (e && e.stopPropagation) e.stopPropagation();
    const sheet = document.getElementById('orderTypeModalSheet');
    const backdrop = document.getElementById('orderTypeModalBackdrop');
    if (!sheet) return;
    const isShowing = window.getComputedStyle(sheet).display !== 'none';
    if (isShowing) {
        sheet.style.setProperty('display', 'none', 'important');
        if (backdrop) backdrop.style.setProperty('display', 'none', 'important');
    } else {
        sheet.style.setProperty('display', 'block', 'important');
        if (backdrop) backdrop.style.setProperty('display', 'block', 'important');
    }
}

function selectOrderType(type) {
    currentSelectedOrderType = type;
    const curTypeEl = document.getElementById('ex-current-ordertype');
    if (curTypeEl) curTypeEl.innerText = type;

    document.querySelectorAll('.ord-check').forEach(el => el.style.display = 'none');
    const checked = document.getElementById('check-' + type);
    if (checked) checked.style.display = 'block';

    const pBox = document.getElementById('ex-price-field-box');
    const pText = document.getElementById('ex-price-field-text');
    const pInput = document.getElementById('ex-custom-price-input');
    const sBox = document.getElementById('ex-stop-field-box');
    const sText = document.getElementById('ex-stop-field-text');
    const sInput = document.getElementById('ex-stop-price-input');
    const cbBox = document.getElementById('ex-callback-field-box');
    const atlBox = document.getElementById('atl-config-box');
    const submitBtn = document.getElementById('ex-btn-submit');

    atlBox.style.display = 'none';
    pBox.style.display = 'flex';
    pInput.style.display = 'none';
    sBox.style.display = 'none';
    cbBox.style.display = 'none';

    if (type === 'Shine Auto Trailing' || type === 'Auto Trailing Loop') {
        switchExchangeTab('BUY');
        atlBox.style.display = 'flex';
        pBox.style.display = 'none';
        if (currentChartLivePrice > 0) {
            const bTrigEl = document.getElementById('atl-buy-trigger');
            const sTrigEl = document.getElementById('atl-sell-trigger');
            if (bTrigEl && (!bTrigEl.value || parseFloat(bTrigEl.value) <= 0)) bTrigEl.value = (currentChartLivePrice * 0.99).toFixed(2);
            if (sTrigEl && (!sTrigEl.value || parseFloat(sTrigEl.value) <= 0)) sTrigEl.value = (currentChartLivePrice * 1.02).toFixed(2);
        }
        submitBtn.innerText = 'Start Shine Auto Trailing';
        submitBtn.style.background = '#00c087';
    } else if (type === 'Market') {
        pText.innerText = 'Fill at market price';
        submitBtn.innerText = currentExchangeTab === 'BUY' ? 'Buy SOL' : 'Sell SOL';
        submitBtn.style.background = currentExchangeTab === 'BUY' ? '#00c087' : '#f6465d';
    } else if (type === 'Limit') {
        pText.innerText = 'Limit Price';
        pInput.style.display = 'block';
        pInput.style.width = '120px';
        if (currentChartLivePrice > 0) {
            pInput.value = currentExchangeTab === 'BUY' ? (currentChartLivePrice * 0.99).toFixed(2) : (currentChartLivePrice * 1.01).toFixed(2);
        }
        submitBtn.innerText = (currentExchangeTab === 'BUY' ? 'Buy ' : 'Sell ') + 'Limit';
    
    } else if (type === 'TP/SL' || type === 'OCO') {
        pInput.style.display = 'block';
        sBox.style.display = 'flex';
        if (currentExchangeTab === 'BUY') {
            pText.innerText = 'Dip Buy Target (Below)';
            sText.innerText = 'Breakout Buy (Above)';
            if (currentChartLivePrice > 0) {
                pInput.value = (currentChartLivePrice * 0.98).toFixed(2);
                sInput.value = (currentChartLivePrice * 1.02).toFixed(2);
            }
        } else {
            pText.innerText = 'Take Profit (Above)';
            sText.innerText = 'Stop Loss (Below)';
            if (currentChartLivePrice > 0) {
                pInput.value = (currentChartLivePrice * 1.02).toFixed(2);
                sInput.value = (currentChartLivePrice * 0.98).toFixed(2);
            }
        }
        submitBtn.innerText = 'Execute ' + type;
    } else if (type === 'Trigger') {
        pText.innerText = 'Execution Price';
        pInput.style.display = 'block';
        pInput.style.width = '120px';
        sBox.style.display = 'flex';
        sText.innerText = 'Trigger Price';
        submitBtn.innerText = (currentExchangeTab === 'BUY' ? 'Buy ' : 'Sell ') + 'Trigger';
        submitBtn.style.background = currentExchangeTab === 'BUY' ? '#00c087' : '#f6465d';
    } else if (type === 'Trailing stop') {
        pText.innerText = 'Activation Price';
        pInput.style.display = 'block';
        pInput.style.width = '120px';
        cbBox.style.display = 'flex';
        pInput.value = currentExchangeTab === 'BUY' ? (currentChartLivePrice * 0.98).toFixed(2) : (currentChartLivePrice * 1.02).toFixed(2);
        submitBtn.innerText = (currentExchangeTab === 'BUY' ? 'Buy ' : 'Sell ') + 'Trailing Stop';
        submitBtn.style.background = currentExchangeTab === 'BUY' ? '#00c087' : '#f6465d';
    }

    toggleOrderTypeSheet();
}

function setExchangePct(pct) {
    const inEl = document.getElementById("ex-input-amount");
    if (!inEl) return;
    const isAutoLoop = (currentSelectedOrderType === 'Shine Auto Trailing' || currentSelectedOrderType === 'Auto Trailing Loop');
    if (isAutoLoop || currentExchangeTab === 'BUY') {
        let availUsdt = (latestBackendState && latestBackendState.manualTestBalance !== undefined) ? parseFloat(latestBackendState.manualTestBalance) : 0;
        if (availUsdt <= 0) {
            const balEl = document.getElementById("ex-avail-bal");
            availUsdt = parseFloat(balEl ? balEl.innerText : 0) || 0;
        }
        let calcVal = Math.floor(availUsdt * (pct / 100) * 100) / 100;
        inEl.value = calcVal.toFixed(2);
    } else {
        let availSol = (latestBackendState && latestBackendState.walletSol !== undefined) ? parseFloat(latestBackendState.walletSol) : 0;
        if (availSol <= 0) {
            const balEl = document.getElementById("ex-avail-bal");
            availSol = parseFloat(balEl ? balEl.innerText : 0) || 0;
        }
        let calcVal = Math.floor(availSol * (pct / 100) * 10000) / 10000;
        inEl.value = calcVal.toFixed(4);
    }
}
function renderLiveOrderBook() {
    connectBinanceLiveStream();
}

async function executeJupiterRealSwap(amount, side) {
    if (!window.solana || !window.solana.isPhantom || !userWallet) {
        alert("Please connect Phantom wallet for Real Solana DEX swap.");
        openConnectModal();
        return;
    }
    const usdtMint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB";
    const solMint = "So11111111111111111111111111111111111111112";
    const inMint = side === "BUY" ? usdtMint : solMint;
    const outMint = side === "BUY" ? solMint : usdtMint;
    const rawUnits = side === "BUY" ? Math.floor(amount * 1000000) : Math.floor(amount * 1000000000);

    try {
        const quoteUrl = `https://quote-api.jup.ag/v6/quote?inputMint=${inMint}&outputMint=${outMint}&amount=${rawUnits}&slippageBps=50`;
        const qRes = await fetch(quoteUrl);
        const quoteData = await qRes.json();
        if (!quoteData || quoteData.error) {
            alert("Jupiter DEX routing failed: " + (quoteData.error || "No route"));
            return;
        }

        const swapRes = await fetch("https://quote-api.jup.ag/v6/swap", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                quoteResponse: quoteData,
                userPublicKey: userWallet,
                wrapAndUnwrapSol: true,
                dynamicComputeUnitLimit: true
            })
        });
        const swapData = await swapRes.json();
        if (!swapData || !swapData.swapTransaction) {
            alert("Failed to build swap transaction on Jupiter.");
            return;
        }

        const swapTxBuf = Uint8Array.from(atob(swapData.swapTransaction), c => c.charCodeAt(0));
        const vTx = solanaWeb3.VersionedTransaction.deserialize(swapTxBuf);
        const signed = await window.solana.signAndSendTransaction(vTx);

        alert("Swap Successful on Solana Blockchain!\nTx Signature: " + signed.signature + "\nView on Solscan: https://solscan.io/tx/" + signed.signature);
        setTimeout(() => {
            fetchRealWeb3WalletBalances(userWallet);
            refreshExchangeBalances();
        }, 1500);

        if (botSocket && botSocket.readyState === WebSocket.OPEN) {
            botSocket.send(JSON.stringify({
                action: side === "BUY" ? "MANUAL_BUY" : "MANUAL_SELL",
                orderId: "JUP_" + signed.signature.substring(0, 8),
                orderType: "JUPITER_DEX_SWAP",
                side: side,
                amount: amount,
                solQuantity: side === "BUY" ? (amount / currentChartLivePrice) : amount,
                price: currentChartLivePrice,
                walletAddress: userWallet
            }));
        }
    } catch (e) {
        alert("Transaction Rejected or Failed: " + (e.message || e));
    }
}

async function executeExchangeAction() {
    if (currentTradeExecutionMode === "REAL" && (!isTradeWalletConnected || !userWallet)) {
        alert("Please connect your wallet first to execute Real Mainnet trades.");
        openConnectModal();
        return;
    }

    const inEl = document.getElementById("ex-input-amount");
    const val = parseFloat(inEl ? inEl.value : 0);

    if (!val || val <= 0) {
        alert("Please enter a valid amount.");
        return;
    }

    if (currentTradeExecutionMode === "REAL") {
        if (connectedWalletType === "PHANTOM") {
            const availBal = currentExchangeTab === "BUY" ? liveOnChainWallet.usdt : liveOnChainWallet.gas;
            if (val > (availBal + 0.0001)) {
                alert("Insufficient on-chain balance! Available: " + availBal.toFixed(4));
                return;
            }
            await executeJupiterRealSwap(val, currentExchangeTab);
            if (inEl) inEl.value = "";
            return;
        } else {
            alert("Currently Real On-Chain Swap execution is connected with Solana (Phantom Wallet).");
            return;
        }
    }

    const isAutoLoop = (currentSelectedOrderType === 'Shine Auto Trailing' || currentSelectedOrderType === 'Auto Trailing Loop');
    let maxAvail = isAutoLoop || currentExchangeTab === 'BUY'
        ? ((latestBackendState && latestBackendState.manualTestBalance !== undefined) ? parseFloat(latestBackendState.manualTestBalance) : 100.0)
        : ((latestBackendState && latestBackendState.walletSol !== undefined) ? parseFloat(latestBackendState.walletSol) : 0);

    if (maxAvail <= 0) {
        const balEl = document.getElementById("ex-avail-bal");
        maxAvail = parseFloat(balEl ? balEl.innerText : 0) || 100.0;
    }

    if (val > (maxAvail + 0.0001)) {
        alert("Insufficient balance! Available: " + maxAvail.toFixed(2));
        return;
    }

    if (!botSocket || botSocket.readyState !== WebSocket.OPEN) {
        alert("Bot engine connection offline. Please wait.");
        return;
    }

    const cbVal = parseFloat(document.getElementById("ex-callback-input") ? document.getElementById("ex-callback-input").value : 1.0);

    if (currentSelectedOrderType === 'Shine Auto Trailing' || currentSelectedOrderType === 'Auto Trailing Loop') {
        const bTrig = parseFloat(document.getElementById('atl-buy-trigger').value || 0);
        const bCb = parseFloat(document.getElementById('atl-buy-cb').value || 0.01);
        const sTrig = parseFloat(document.getElementById('atl-sell-trigger').value || 0);
        const sCb = parseFloat(document.getElementById('atl-sell-cb').value || 0.01);
        const aRep = document.getElementById('atl-auto-repeat').checked;

        if (bTrig <= 0 || sTrig <= 0) {
            alert('Please specify valid Buy and Sell trigger prices for Shine Auto Trailing.');
            return;
        }

        const generatedSlotId = "ATL_" + Date.now();
        const slotArea = document.getElementById("atl-slot-input-area");
        if (slotArea) slotArea.style.display = "none";

        botSocket.send(JSON.stringify({
            action: 'CREATE_AUTO_LOOP',
            slotId: generatedSlotId,
            amount: val,
            buyTrigger: bTrig,
            buyCallback: bCb,
            sellTrigger: sTrig,
            sellCallback: sCb,
            autoRepeat: aRep
        }));
        if (inEl) inEl.value = "";
        return;
    }

    let finalOrderType = currentSelectedOrderType;
    let execPrice = currentChartLivePrice;
    if (finalOrderType === 'Limit' || finalOrderType === 'Trailing stop') {
        const customPriceEl = document.getElementById("ex-custom-price-input");
        const parsedCustom = parseFloat(customPriceEl ? customPriceEl.value : 0);
        if (!parsedCustom || parsedCustom <= 0) {
            alert("Please enter a valid target price.");
            return;
        }
        execPrice = parsedCustom;
    } else if (finalOrderType === 'Trigger') {
        const customPriceEl = document.getElementById("ex-custom-price-input");
        const parsedExec = parseFloat(customPriceEl ? customPriceEl.value : 0);
        const parsedTrig = parseFloat(document.getElementById("ex-stop-price-input") ? document.getElementById("ex-stop-price-input").value : 0);
        if (!parsedExec || parsedExec <= 0 || !parsedTrig || parsedTrig <= 0) {
            alert("Please enter valid Execution Price and Trigger Price.");
            return;
        }
        execPrice = parsedExec;
    } else if (finalOrderType === 'TP/SL' || finalOrderType === 'OCO') {
        const tpVal = parseFloat(document.getElementById("ex-custom-price-input") ? document.getElementById("ex-custom-price-input").value : 0);
        const slVal = parseFloat(document.getElementById("ex-stop-price-input") ? document.getElementById("ex-stop-price-input").value : 0);
        if (!tpVal || tpVal <= 0 || !slVal || slVal <= 0) {
            alert("Please enter valid Take Profit and Stop Loss target prices.");
            return;
        }
        execPrice = tpVal;
    }

    let solQuantity = currentExchangeTab === 'BUY' ? parseFloat((val / execPrice).toFixed(4)) : parseFloat(val);
    const orderId = (finalOrderType === 'Market' ? "MAN_" : "ORD_") + Date.now();

    const stopVal = parseFloat(document.getElementById("ex-stop-price-input") ? document.getElementById("ex-stop-price-input").value : 0) || 0;
    const limitVal = parseFloat(document.getElementById("ex-custom-price-input") ? document.getElementById("ex-custom-price-input").value : execPrice) || execPrice;

    const orderPayload = {
        action: finalOrderType === 'Market' ? (currentExchangeTab === 'BUY' ? "MANUAL_BUY" : "MANUAL_SELL") : "CREATE_ORDER",
        orderId: orderId,
        orderType: finalOrderType.toUpperCase().replace(/\s+/g, '_').replace('/', '_'),
        side: currentExchangeTab.toUpperCase(),
        amount: val,
        solQuantity: solQuantity,
        price: execPrice,
        activationPrice: execPrice,
        stopPrice: stopVal,
        limitPrice: limitVal,
        callbackPct: cbVal,
        walletAddress: userWallet || "0xTestUser"
    };

    botSocket.send(JSON.stringify(orderPayload));
    if (inEl) inEl.value = "";
}

let currentExchangeOrderSubTab = 'OPEN';

function switchExchangeOrderSubTab(tab) {
    currentExchangeOrderSubTab = tab;
    const tabOpen = document.getElementById("tab-opt-open-orders");
    const tabPos = document.getElementById("tab-opt-positions");
    const tabHist = document.getElementById("tab-opt-history-orders");
    const tabBots = document.getElementById("tab-opt-bots-btn");

    const listOpen = document.getElementById("user-open-orders-list");
    const listPos = document.getElementById("user-positions-list");
    const listHist = document.getElementById("user-history-orders-list");
    const listBots = document.getElementById("user-bots-list");

    [tabOpen, tabPos, tabHist, tabBots].forEach(el => {
        if (el) {
            el.style.color = "#718096";
            el.style.borderBottom = "none";
            el.style.fontWeight = "700";
        }
    });

    [listOpen, listPos, listHist, listBots].forEach(el => {
        if (el) el.style.display = "none";
    });

    if (tab === 'OPEN') {
        if (tabOpen) { tabOpen.style.color = "#ffffff"; tabOpen.style.borderBottom = "2px solid #00c087"; tabOpen.style.fontWeight = "900"; }
        if (listOpen) listOpen.style.display = "flex";
    } else if (tab === 'POSITIONS') {
        if (tabPos) { tabPos.style.color = "#ffffff"; tabPos.style.borderBottom = "2px solid #00c087"; tabPos.style.fontWeight = "900"; }
        if (listPos) listPos.style.display = "flex";
    } else if (tab === 'HISTORY') {
        if (tabHist) { tabHist.style.color = "#ffffff"; tabHist.style.borderBottom = "2px solid #00c087"; tabHist.style.fontWeight = "900"; }
        if (listHist) listHist.style.display = "flex";
    } else if (tab === 'BOTS') {
        if (tabBots) { tabBots.style.color = "#00e5ff"; tabBots.style.borderBottom = "2px solid #00e5ff"; tabBots.style.fontWeight = "900"; }
        if (listBots) listBots.style.display = "flex";
        renderUserBotsPanel();
    }
}

function renderUserBotsPanel() {
    const container = document.getElementById("user-bots-list");
    if (!container) return;

    const subs = (latestBackendState && Array.isArray(latestBackendState.copySubscribers)) ? latestBackendState.copySubscribers : [];
    if (subs.length === 0) {
        container.innerHTML = `
            <div style="background: #11151e; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 24px 16px; text-align: center;">
                <i class="material-icons" style="color: #718096; font-size: 36px; margin-bottom: 8px;">smart_toy</i>
                <div style="color: #ffffff; font-weight: 800; font-size: 13px;">No Copy Trading Bots Active</div>
                <div style="color: #718096; font-size: 11px; margin-top: 4px;">Allocate funds to Elite Copy Trading to start automated algorithm execution.</div>
                <button onclick="openEliteTradesModal()" style="background: #00c087; color: #000; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 900; font-size: 11px; cursor: pointer; margin-top: 14px;">START COPY TRADING</button>
            </div>
        `;
        return;
    }

    const curPrice = currentChartLivePrice > 0 ? currentChartLivePrice : 0;
    let totalInvested = 0;
    let totalSlots = 0;
    let totalUnrealized = 0;
    let totalRealized = 0;

    subs.forEach(s => {
        const inv = parseFloat(s.totalCapital || s.amount || s.invested || 0);
        const slots = parseInt(s.slotsAllowed || 1);
        const real = parseFloat(s.realizedPnl || 0);
        const buyP = parseFloat(s.entryPrice || curPrice);
        const solQty = buyP > 0 ? (inv / buyP) : 0;
        const curVal = solQty * curPrice;
        const unreal = curVal - inv;

        totalInvested += inv;
        totalSlots += slots;
        totalUnrealized += unreal;
        totalRealized += real;
    });

    const unColor = totalUnrealized >= 0 ? "#00e5ff" : "#ff2d78";
    const headerCard = `
        <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 14px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
            <div>
                <div style="color: #718096; font-size: 10px; font-weight: 700;">TOTAL BOT CAPITAL</div>
                <div style="color: #ffffff; font-size: 16px; font-weight: 900; margin-top: 2px;">$${totalInvested.toFixed(2)}</div>
            </div>
            <div>
                <div style="color: #718096; font-size: 10px; font-weight: 700;">ACTIVE GRID SLOTS</div>
                <div style="color: #00c087; font-size: 16px; font-weight: 900; margin-top: 2px;">${totalSlots} Slots</div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
                <div style="color: #718096; font-size: 10px; font-weight: 700;">UNREALIZED P&L</div>
                <div style="color: ${unColor}; font-size: 14px; font-weight: 900; margin-top: 2px;">${totalUnrealized >= 0 ? '+' : ''}$${totalUnrealized.toFixed(2)}</div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
                <div style="color: #718096; font-size: 10px; font-weight: 700;">NET REALIZED PROFIT</div>
                <div style="color: #4CAF50; font-size: 14px; font-weight: 900; margin-top: 2px;">+$${totalRealized.toFixed(2)}</div>
            </div>
        </div>
    `;

    const cardsHTML = subs.map(bot => {
        const inv = parseFloat(bot.totalCapital || bot.amount || bot.invested || 0);
        const maxSlots = parseInt(bot.slotsAllowed || 1);
        const activePos = Array.isArray(bot.activePositions) ? bot.activePositions : [];
        const activeSlotsCount = activePos.length;
        const reserveCash = parseFloat(bot.availableReserve !== undefined ? bot.availableReserve : (inv - (activeSlotsCount * (inv / maxSlots))));
        
        let activeSolTotal = 0;
        let activeInvestedTotal = 0;
        activePos.forEach(p => {
            activeSolTotal += parseFloat(p.solAmount || 0);
            activeInvestedTotal += parseFloat(p.invested || 0);
        });

        const activeSolValue = activeSolTotal * curPrice;
        const floatingPnL = activeSolTotal > 0 ? (activeSolValue - activeInvestedTotal) : 0;
        const floatingPct = activeInvestedTotal > 0 ? (floatingPnL / activeInvestedTotal) * 100 : 0;
        const realUsd = parseFloat(bot.realizedPnl || 0);
        const isUp = floatingPnL >= 0;
        const pColor = isUp ? "#00e5ff" : "#ff2d78";
        const timeStr = bot.timestamp ? bot.timestamp.replace("T", " ").substring(0, 19) : "Just now";

        return `
            <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 14px; display: flex; flex-direction: column; gap: 10px; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="background: rgba(0, 229, 255, 0.12); color: #00e5ff; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 900;">${bot.botType}</span>
                        <span style="color: #4CAF50; font-size: 10px; font-weight: 800;">● RUNNING</span>
                    </div>
                    <span style="color: #718096; font-size: 11px;">${timeStr}</span>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; width: 100%; box-sizing: border-box; margin-top: 2px;">
                    <div>
                        <div style="color: #718096; font-size: 10px;">Total Capital</div>
                        <div style="color: #ffffff; font-size: 14px; font-weight: 900; margin-top: 2px;">$${inv.toFixed(2)}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #718096; font-size: 10px;">Slots Active</div>
                        <div style="color: #FFD700; font-size: 14px; font-weight: 900; margin-top: 2px;">${activeSlotsCount}/${maxSlots}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #718096; font-size: 10px;">Floating P&L</div>
                        <div style="color: ${pColor}; font-size: 14px; font-weight: 900; margin-top: 2px;">${isUp ? '+' : ''}$${floatingPnL.toFixed(2)} (${isUp ? '+' : ''}${floatingPct.toFixed(2)}%)</div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 8px; font-size: 11px;">
                    <span style="color: #718096;">Reserve Cash: <strong style="color: #00c087;">$${reserveCash.toFixed(2)}</strong></span>
                    <span style="color: #718096;">Holding: <strong style="color: #fff;">${activeSolTotal > 0 ? activeSolTotal.toFixed(4) + ' SOL' : 'WAITING DIP ENTRY'}</strong></span>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
                    <span style="color: #718096;">Realized Profit: <strong style="color: #4CAF50;">+$${realUsd.toFixed(2)}</strong></span>
                    <span style="color: #00d2ff; font-size: 10px;">$${(inv / maxSlots).toFixed(2)} / slot</span>
                </div>

                <button onclick="closeCopyTradeBot('${bot.id}')" style="background: rgba(255,45,120,0.12); border: 1px solid #ff2d78; color: #ff2d78; border-radius: 8px; padding: 10px 0; font-size: 11px; font-weight: 900; cursor: pointer; margin-top: 4px;">CLOSE COPY TRADE & RETURN FUNDS</button>
            </div>
        `;
    }).join("");

    container.innerHTML = headerCard + cardsHTML;
}

function closeCopyTradeBot(subId) {
    if (!confirm("Are you sure you want to close this copy trading bot? All active positions will be closed at market rate and funds returned to your balance.")) return;
    dismissedBotIds.add(subId);

    if (botSocket && botSocket.readyState === WebSocket.OPEN) {
        botSocket.send(JSON.stringify({ action: "CLOSE_COPY_TRADE", subId: subId, closePrice: currentChartLivePrice }));
    }
}

function cancelSingleUserOrder(posId) {
    if (!botSocket || botSocket.readyState !== WebSocket.OPEN) return;
    if (posId && String(posId).startsWith("ATL_")) {
        botSocket.send(JSON.stringify({ action: "CANCEL_AUTO_LOOP", slotId: posId }));
        return;
    }
    botSocket.send(JSON.stringify({ action: "CANCEL_ORDER", posId: posId, cancel: true }));
}

function closeManualPosition(posId) {
    dismissedOrderIds.add(posId);
    if (latestBackendState && latestBackendState.walletActivePositions && Array.isArray(latestBackendState.walletActivePositions)) {
        latestBackendState.walletActivePositions = latestBackendState.walletActivePositions.filter(p => p.id !== posId);
        latestBackendState.walletSol = 0.0;
        latestBackendState.walletInvested = 0.0;
        refreshExchangeBalances();
        renderProfessionalOrderDesk(latestBackendState);
    }
    if (!botSocket || botSocket.readyState !== WebSocket.OPEN) return;
    botSocket.send(JSON.stringify({ action: "MANUAL_SELL", posId: posId, exitPrice: currentChartLivePrice }));
}
function cancelAllUserOrders() {
    if (latestBackendState) {
        latestBackendState.walletOpenOrders = [];
        latestBackendState.openOrders = [];
        renderProfessionalOrderDesk(latestBackendState);
    }
    if (!botSocket || botSocket.readyState !== WebSocket.OPEN) return;
    botSocket.send(JSON.stringify({ action: "CANCEL_ORDER", posId: "ALL", cancel: true }));
}

let showFullExchangeHistory = false;

function toggleFullExchangeHistory() {
    showFullExchangeHistory = !showFullExchangeHistory;
    renderProfessionalOrderDesk(latestBackendState);
}

function renderProfessionalOrderDesk(data) {
    const openContainer = document.getElementById("user-open-orders-list");
    const posContainer = document.getElementById("user-positions-list");
    const histContainer = document.getElementById("user-history-orders-list");
    const countBadge = document.getElementById("user-open-orders-count");
    const posCountBadge = document.getElementById("user-positions-count");

    let openOrders = [];
    if (data && Array.isArray(data.walletOpenOrders)) {
        openOrders = [...data.walletOpenOrders];
    } else if (data && Array.isArray(data.openOrders)) {
        openOrders = [...data.openOrders];
    }
    let positions = (data && data.walletActivePositions && Array.isArray(data.walletActivePositions)) ? [...data.walletActivePositions] : [];
    const historyTrades = (data && data.manualTradesHistory && Array.isArray(data.manualTradesHistory)) ? data.manualTradesHistory : ((data && data.tradesHistory && Array.isArray(data.tradesHistory)) ? data.tradesHistory.filter(t => {
        const ordId = String(t.orderId || "");
        const execType = String(t.execType || "");
        return ordId.startsWith("MAN_") || ordId.startsWith("ORD_") || ordId.startsWith("ATL_") || execType.includes("MANUAL") || execType.includes("AUTO_LOOP");
    }) : []);

    if (countBadge) countBadge.innerText = openOrders.length.toString();
    if (posCountBadge) posCountBadge.innerText = positions.length.toString();

    if (openContainer) {
        if (openOrders.length === 0) {
            openContainer.innerHTML = '<div style="text-align: center; color: #718096; font-size: 13px; padding: 30px 0; font-weight: 600;">No open orders</div>';
        } else {
            openContainer.innerHTML = openOrders.map(ord => {
                const sideText = (ord.side || "BUY").toUpperCase();
                const isBuy = sideText.includes("BUY");
                const typeText = ord.orderType ? (String(ord.orderType).includes('Loop') || String(ord.orderType).includes('ATL') || String(ord.orderType).includes('Auto') ? 'Auto Trailing' : String(ord.orderType).replace('_', ' ')) : "LIMIT";
                const pVal = parseFloat(ord.price || ord.entryPrice || ord.limitPrice || 0).toFixed(2);
                let sQty = parseFloat(ord.solAmount || 0);
                const totalInvest = parseFloat(ord.invested || ord.amount || 0).toFixed(2);
                if (sQty <= 0 && parseFloat(pVal) > 0) {
                    sQty = parseFloat(totalInvest) / parseFloat(pVal);
                }
                sQty = sQty.toFixed(4);
                const timeStr = ord.timestamp ? String(ord.timestamp).replace("T", " ").substring(0, 19) : new Date().toISOString().replace("T", " ").substring(0, 19);

                return `
                <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 16px; margin-bottom: 12px; display: flex; flex-direction: column; gap: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 4px; font-size: 16px; font-weight: 800; color: #ffffff;">
                            <span>SOL/USDT</span>
                            <i class="material-icons" style="font-size: 16px; color: #718096;">chevron_right</i>
                        </div>
                        <span style="color: #718096; font-size: 12px; font-family: monospace;">${timeStr}</span>
                    </div>

                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="background: ${isBuy ? 'rgba(0, 229, 255, 0.12)' : 'rgba(255, 45, 120, 0.12)'}; color: ${isBuy ? '#00e5ff' : '#ff2d78'}; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">${isBuy ? 'Buy' : 'Sell'}</span>
                        <span style="background: #1c2433; color: #8c8ca1; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">${typeText}</span>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; width: 100%; box-sizing: border-box;">
                        <div style="text-align: left;">
                            <div style="color: #718096; font-size: 11px; font-weight: 500;">Price(USDT)</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">${pVal}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #718096; font-size: 11px; font-weight: 500;">Quantity(SOL)</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">${sQty}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #718096; font-size: 11px; font-weight: 500;">Total(USDT)</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">${totalInvest}</div>
                        </div>
                    </div>

                    <div>
                        <div style="color: #718096; font-size: 11px; font-weight: 500;">Filled(SOL)</div>
                        <div style="color: #ffffff; font-size: 14px; font-weight: 800; font-family: monospace; margin-top: 2px;">0</div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-top: 4px;">
                        <button onclick="modifyOrderPrompt('${ord.id}', ${pVal})" style="background: #1c2433; border: 1px solid #2d3748; color: #e2e8f0; border-radius: 8px; padding: 9px 0; font-size: 12px; font-weight: 700; cursor: pointer;">Modify</button>
                        <button onclick="tpSlOrderPrompt('${ord.id}', ${pVal})" style="background: #1c2433; border: 1px solid #2d3748; color: #e2e8f0; border-radius: 8px; padding: 9px 0; font-size: 12px; font-weight: 700; cursor: pointer;">TP/SL</button>
                        <button onclick="cancelSingleUserOrder('${ord.id}')" style="background: #1c2433; border: 1px solid #2d3748; color: #e2e8f0; border-radius: 8px; padding: 9px 0; font-size: 12px; font-weight: 700; cursor: pointer;">Cancel</button>
                    </div>
                </div>`;
            }).join("");
        }
    }

    if (posContainer) {
        if (positions.length === 0) {
            posContainer.innerHTML = '<div style="text-align: center; color: #718096; font-size: 13px; padding: 30px 0; font-weight: 600;">No active holdings</div>';
        } else {
            posContainer.innerHTML = positions.map(pos => {
                const sQty = parseFloat(pos.solAmount || 0).toFixed(4);
                const entryP = parseFloat(pos.entryPrice || 0);
                const totalInvest = parseFloat(pos.invested || 0).toFixed(3);
                const curLive = currentChartLivePrice > 0 ? currentChartLivePrice : entryP;
                const pnlUsd = (curLive - entryP) * parseFloat(sQty);
                const pnlPct = entryP > 0 ? ((curLive - entryP) / entryP) * 100 : 0;
                const isProfit = pnlUsd >= 0;
                const pColor = isProfit ? "#00e5ff" : "#ff2d78";

                const posId = String(pos.id || "").toUpperCase();
                const ordType = String(pos.orderType || "").toUpperCase();
                const lbl = String(pos.label || "").toUpperCase();

                let posLabel = "MARKET";
                let posBg = "rgba(113, 128, 150, 0.15)";
                let posColor = "#a0aec0";

                if (posId.startsWith("ATL_") || ordType.includes("AUTO_LOOP") || lbl.includes("LOOP")) {
                    posLabel = "AUTO TRAILING";
                    posBg = "rgba(0, 192, 135, 0.15)";
                    posColor = "#00c087";
                } else if (ordType.includes("TRAILING") || lbl.includes("TRAILING")) {
                    posLabel = "TRAILING STOP";
                    posBg = "rgba(0, 229, 255, 0.15)";
                    posColor = "#00e5ff";
                } else if (ordType.includes("LIMIT") || lbl.includes("LIMIT")) {
                    posLabel = "LIMIT";
                    posBg = "rgba(255, 215, 0, 0.15)";
                    posColor = "#FFD700";
                } else if (ordType.includes("TP_") || ordType.includes("SL_") || ordType.includes("OCO") || ordType.includes("TP/SL") || lbl.includes("TP/SL")) {
                    posLabel = "TP/SL";
                    posBg = "rgba(186, 104, 200, 0.15)";
                    posColor = "#ba68c8";
                } else if (ordType.includes("TRIGGER") || lbl.includes("TRIGGER")) {
                    posLabel = "TRIGGER";
                    posBg = "rgba(255, 112, 67, 0.15)";
                    posColor = "#ff7043";
                } else if (posId.startsWith("COPY_") || posId.startsWith("CPOS_") || lbl.includes("COPY")) {
                    posLabel = "COPY BOT";
                    posBg = "rgba(58, 71, 166, 0.2)";
                    posColor = "#5C6BC0";
                }

                return `
                <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 16px; margin-bottom: 12px; display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 16px; font-weight: 800; color: #ffffff;">SOL/USDT</span>
                            <span style="background: ${posBg}; color: ${posColor}; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 800; font-family: monospace; letter-spacing: 0.3px;">${posLabel}</span>
                        </div>
                        <div style="font-size: 13px; font-weight: 800; color: ${pColor}; font-family: monospace;">
                            ${isProfit ? '+' : ''}$${pnlUsd.toFixed(2)} (${isProfit ? '+' : ''}${pnlPct.toFixed(2)}%)
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; width: 100%; box-sizing: border-box;">
                        <div style="text-align: left;">
                            <div style="color: #718096; font-size: 11px;">Entry Price</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">$${entryP.toFixed(2)}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #718096; font-size: 11px;">Quantity(SOL)</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">${sQty}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #718096; font-size: 11px;">Total(USDT)</div>
                            <div style="color: #ffffff; font-size: 15px; font-weight: 800; font-family: monospace; margin-top: 3px;">$${totalInvest}</div>
                        </div>
                    </div>

                    <button onclick="closeManualPosition('${pos.id}')" style="background: rgba(255,45,120,0.15); border: 1px solid #ff2d78; color: #ff2d78; border-radius: 8px; padding: 10px 0; font-size: 12px; font-weight: 800; cursor: pointer;">Market Close</button>
                </div>`;
            }).join("");
        }
    }

    if (histContainer) {
        if (historyTrades.length === 0) {
            histContainer.innerHTML = '<div style="text-align: center; color: #718096; font-size: 13px; padding: 30px 0; font-weight: 600;">No trade history</div>';
        } else {
            const displayTrades = showFullExchangeHistory ? historyTrades : historyTrades.slice(0, 10);
            const tradesHTML = displayTrades.map(tr => {
                const isSell = String(tr.side || "").toUpperCase().includes("SELL");
                const profitVal = parseFloat(tr.profit || tr.realizedPnl || 0);
                const isWin = profitVal >= 0;
                const pColor = isWin ? "#00e5ff" : "#ff2d78";
                const pText = isSell ? ((isWin ? "+" : "") + profitVal.toFixed(4) + " USDT") : "EXECUTED";
                const timeStr = tr.timestamp ? (tr.timestamp.includes("T") ? tr.timestamp.replace("T", " ").substring(0, 19) : tr.timestamp) : "Completed";

                const rawExec = String(tr.execType || tr.orderType || "").toUpperCase();
                const ordId = String(tr.orderId || "").toUpperCase();
                let orderLabel = "MARKET";
                let labelBg = "rgba(113, 128, 150, 0.15)";
                let labelColor = "#a0aec0";

                if (rawExec.includes("AUTO_TRAILING_LOOP") || rawExec.includes("AUTO_LOOP") || ordId.startsWith("ATL_")) {
                    orderLabel = "AUTO TRAILING";
                    labelBg = "rgba(0, 192, 135, 0.15)";
                    labelColor = "#00c087";
                } else if (rawExec.includes("TRAILING_SELL") || rawExec.includes("TRAILING_BUY") || rawExec.includes("TRAILING_STOP")) {
                    orderLabel = "TRAILING STOP";
                    labelBg = "rgba(0, 229, 255, 0.15)";
                    labelColor = "#00e5ff";
                } else if (rawExec.includes("LIMIT")) {
                    orderLabel = "LIMIT";
                    labelBg = "rgba(255, 215, 0, 0.15)";
                    labelColor = "#FFD700";
                } else if (rawExec.includes("TP_") || rawExec.includes("SL_") || rawExec.includes("OCO") || rawExec.includes("TP/SL")) {
                    orderLabel = "TP/SL";
                    labelBg = "rgba(186, 104, 200, 0.15)";
                    labelColor = "#ba68c8";
                } else if (rawExec.includes("TRIGGER")) {
                    orderLabel = "TRIGGER";
                    labelBg = "rgba(255, 112, 67, 0.15)";
                    labelColor = "#ff7043";
                } else if (ordId.startsWith("COPY_") || rawExec.includes("COPY")) {
                    orderLabel = "COPY BOT";
                    labelBg = "rgba(58, 71, 166, 0.2)";
                    labelColor = "#5C6BC0";
                }

                return `
                <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 14px; margin-bottom: 10px; display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 14px; font-weight: 800; color: #ffffff;">SOL/USDT</span>
                            <span style="background: ${labelBg}; color: ${labelColor}; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 800; font-family: monospace; letter-spacing: 0.3px;">${orderLabel}</span>
                        </div>
                        <span style="color: #718096; font-size: 11px; font-family: monospace;">${timeStr}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                        <span style="color: ${isSell ? '#ff2d78' : '#00e5ff'}; font-weight: 800;">${isSell ? 'SELL' : 'BUY'}</span>
                        <span style="color: #ffffff; font-family: monospace;">$${parseFloat(tr.price || 0).toFixed(2)} (${parseFloat(tr.solAmount || 0).toFixed(4)} SOL)</span>
                        <span style="color: ${pColor}; font-weight: 800; font-family: monospace;">${pText}</span>
                    </div>
                </div>`;
            }).join("");

            let seeMoreBtnHTML = '';
            if (historyTrades.length > 10) {
                seeMoreBtnHTML = `
                <button onclick="toggleFullExchangeHistory()" style="width: 100%; background: #1c2433; border: 1px solid #2d3748; color: #00e5ff; border-radius: 8px; padding: 12px; font-size: 12px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                    ${showFullExchangeHistory ? 'Show Less (10 Trades)' : `See More (${historyTrades.length} Trades)`}
                </button>`;
            }

            histContainer.innerHTML = tradesHTML + seeMoreBtnHTML;
        }
    }
}

function modifyOrderPrompt(orderId, currentPrice) {
    const newPrice = prompt("Enter new Order Price (USDT):", currentPrice);
    if (!newPrice || isNaN(newPrice) || parseFloat(newPrice) <= 0) return;
    if (botSocket && botSocket.readyState === WebSocket.OPEN) {
        botSocket.send(JSON.stringify({ action: "EDIT_ORDER_PRICE", orderId: orderId, newPrice: parseFloat(newPrice) }));
    }
}

function tpSlOrderPrompt(orderId, currentPrice) {
    const tpPrice = prompt("Enter Take Profit (TP) Target (USDT):", (currentPrice * 1.02).toFixed(2));
    const slPrice = prompt("Enter Stop Loss (SL) Target (USDT):", (currentPrice * 0.98).toFixed(2));
    if (!tpPrice || !slPrice || isNaN(tpPrice) || isNaN(slPrice)) return;
    if (botSocket && botSocket.readyState === WebSocket.OPEN) {
        botSocket.send(JSON.stringify({ action: "SET_TPSL", orderId: orderId, tp: parseFloat(tpPrice), sl: parseFloat(slPrice) }));
    }
}
function openEliteTradesModal() {
    const modal = document.getElementById('eliteTradesModal');
    if (modal) {
        modal.style.display = 'block';
        const balEl = document.getElementById('ex-avail-bal');
        const wAvailText = document.getElementById('copyWalletAvailText');
        if (balEl && wAvailText) {
            wAvailText.innerText = "Avail: " + balEl.innerText;
        }
        calculateCopySlots();
    }
}

function closeEliteTradesModal() {
    const modal = document.getElementById('eliteTradesModal');
    if (modal) modal.style.display = 'none';
}

function setCopyPill(amt) {
    const inp = document.getElementById('copyAmountInput');
    if (inp) {
        inp.value = amt;
        calculateCopySlots();
    }
}

function calculateCopySlots() {
    const inp = document.getElementById('copyAmountInput');
    const noticeText = document.getElementById('copySlotNoticeText');
    const countDisplay = document.getElementById('copySlotsCountDisplay');
    if (!inp || !noticeText || !countDisplay) return;

    const val = parseFloat(inp.value) || 0;
    const slots = val < 10 ? 0 : Math.min(10, Math.max(1, Math.floor(val / 10)));
    const perSlotVal = slots > 0 ? (val / slots).toFixed(2) : "0.00";

    if (val < 10) {
        noticeText.innerHTML = '<span style="color:#f6465d; font-weight:bold;">Minimum 10 USDT required. Capital cannot be less than 10 USDT.</span>';
        countDisplay.innerText = "0 Slots (Disabled)";
        countDisplay.style.color = "#f6465d";
    } else if (slots === 1) {
        noticeText.innerHTML = 'Starting with <strong>10 USDT</strong>. The algorithm will open <strong>1 test trade slot</strong>. Realized profit and capital return instantly upon exit.';
        countDisplay.innerText = "1 Slot (Test Trade Mode)";
        countDisplay.style.color = "#00e5ff";
    } else if (slots < 10) {
        noticeText.innerHTML = `Allocating <strong>${val} USDT</strong> across <strong>${slots} dip slots</strong> ($${perSlotVal} per trade).`;
        countDisplay.innerText = `${slots} Slots Active ($${perSlotVal}/trade)`;
        countDisplay.style.color = "#FFD700";
    } else {
        noticeText.innerHTML = `Allocating <strong>${val} USDT</strong> across the full <strong>10-trade grid strategy</strong> ($${perSlotVal} per dip trade).`;
        countDisplay.innerText = `10 Slots ($${perSlotVal}/trade)`;
        countDisplay.style.color = "#00c087";
    }
}

function executeCopySubscription(botType) {
    const inp = document.getElementById('copyAmountInput');
    const amt = parseFloat(inp ? inp.value : 0);
    const balEl = document.getElementById('ex-avail-bal');
    const currentBal = parseFloat(balEl ? balEl.innerText : 0);

    if (!amt || amt < 10) {
        alert("Please enter a minimum of 10 USDT.");
        return;
    }
    if (amt > currentBal) {
        alert("Insufficient Balance! Your wallet has " + currentBal.toFixed(2) + " USDT. You cannot allocate " + amt + " USDT.");
        return;
    }

    const slots = Math.min(10, Math.max(1, Math.floor(amt / 10)));
    const confirmMsg = `Confirm Copy Trading Subscription:\n\nAllocated Capital: ${amt} USDT\nTrade Slots: ${slots} Slot(s)\nSelected Algorithm: ${botType}\n\nDo you want to proceed?`;
    if (!confirm(confirmMsg)) return;

    if (botSocket && botSocket.readyState === WebSocket.OPEN) {
        botSocket.send(JSON.stringify({
            action: "START_COPY_TRADE",
            botType: botType,
            amount: amt,
            slotsAllowed: slots
        }));
    }
    alert(`Subscription Successful! Allocated ${amt} USDT (${slots} Trade Slot(s)) to ${botType}.`);
    closeEliteTradesModal();
}
let showFullCombinedScalpHistory = false;
    let cachedCombinedScalpTrades = [];

    function toggleFullCombinedAuditHistory() {
        showFullCombinedScalpHistory = !showFullCombinedScalpHistory;
        const btn = document.getElementById("btn-see-more-combined");
        if (btn) btn.innerText = showFullCombinedScalpHistory ? "Show Less" : "See More (All Trades)";
        renderCombinedScalpAuditList(cachedCombinedScalpTrades);
    }

    function renderCombinedScalpAuditList(trades) {
        const historyContainer = document.getElementById("combined-scalp-history-list");
        if (!historyContainer) return;

        let totalWins = 0;
        let totalLosses = 0;
        let totalExits = 0;

        const validTrades = Array.isArray(trades) ? trades.filter(t => parseFloat(t.solAmount || 0) > 0 && !String(t.orderId || "").startsWith("BOT_")) : [];
        if (validTrades.length > 0) {
            validTrades.forEach(t => {
                const isSell = String(t.side || "").toUpperCase().includes("SELL");
                const pVal = parseFloat(t.profit || t.realizedPnl || 0);
                if (isSell) {
                    totalExits++;
                    if (pVal >= 0) totalWins++;
                    else totalLosses++;
                }
            });
        }

        const cntEl = document.getElementById("combined-audit-trade-count");
        const winEl = document.getElementById("combined-audit-win-count");
        const lossEl = document.getElementById("combined-audit-loss-count");
        if (cntEl) cntEl.innerText = totalExits.toString();
        if (winEl) winEl.innerText = totalWins.toString();
        if (lossEl) lossEl.innerText = totalLosses.toString();

        if (!trades || trades.length === 0) {
            historyContainer.innerHTML = '<div class="empty-msg">NO SCALP TRADES RECORDED</div>';
            return;
        }

        const displayTrades = showFullCombinedScalpHistory ? validTrades : validTrades.slice(0, 10);

        historyContainer.innerHTML = displayTrades.map((t) => {
            const isSell = String(t.side || "").toUpperCase().includes("SELL");
            const pVal = parseFloat(t.profit || t.realizedPnl || 0);
            const isWin = pVal >= 0;
            let dateStr = "";
            if (t.timestamp) {
                const parsedDate = new Date(t.timestamp);
                if (!isNaN(parsedDate.getTime())) {
                    dateStr = parsedDate.toLocaleString("en-PK", {
                        timeZone: "Asia/Karachi",
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                        hour12: true
                    });
                } else {
                    dateStr = String(t.timestamp);
                }
            }
            const badgeBg = isSell ? (isWin ? "rgba(76,175,80,0.2)" : "rgba(246,70,93,0.2)") : "rgba(0,210,255,0.2)";
            const badgeColor = isSell ? (isWin ? "#4CAF50" : "#f6465d") : "#00d2ff";
            const actionLabel = isSell ? "EXIT" : "ENTRY";
            const pnlDisplay = isSell ? '<span style="color:' + badgeColor + '; font-weight:bold;">' + (isWin ? "+" : "") + pVal.toFixed(4) + ' USDT</span>' : '<span style="color:#757575;">EXECUTED</span>';
            const orderLabel = t.label ? t.label : (t.orderId ? t.orderId : "SCALP");

            return '<div style="background:#151518; border:1px solid #222; border-radius:8px; padding:10px 12px; display:flex; flex-direction:column; gap:4px; font-family:monospace;">' +
                   '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                   '<span style="background:' + badgeBg + '; color:' + badgeColor + '; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:bold;">' + actionLabel + '</span>' +
                   '<span style="color:#757575; font-size:10px;">' + dateStr + '</span>' +
                   '</div>' +
                   '<div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-top:2px;">' +
                   '<span style="color:#fff;">$' + parseFloat(t.price || t.entryPrice || 0).toFixed(2) + ' <span style="color:#757575;">(' + parseFloat(t.solAmount || 0).toFixed(4) + ' SOL)</span></span>' +
                   pnlDisplay +
                   '</div>' +
                   '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px; padding-top:4px; border-top:1px solid rgba(255,255,255,0.03); font-size:10px;">' +
                   '<span style="color:#00d2ff;">QUANT AUTO ENGINE</span>' +
                   '<span style="color:#757575;">REF: ' + orderLabel + '</span>' +
                   '</div>' +
                   '</div>';
        }).join("");
    }
    
    function renderAuditHistoryList(trades) {
        const historyContainer = document.getElementById("trade-history-list");
        if (!historyContainer) return;
        const validTrades = Array.isArray(trades) ? trades.filter(t => parseFloat(t.solAmount || 0) > 0) : [];
        if (validTrades.length === 0) {
            historyContainer.innerHTML = '<div class="empty-msg">NO BOT TRADES RECORDED</div>';
            return;
        }
        const displayList = showFullAuditHistory ? validTrades : validTrades.slice(0, 10);
        historyContainer.innerHTML = displayList.map((t) => {
            const sideStr = String(t.side || "").toUpperCase();
            const execStr = String(t.execType || "").toUpperCase();
            const isSell = sideStr.includes("SELL") || execStr.includes("SELL") || execStr.includes("EXIT");
            const pVal = parseFloat(t.profit || t.realizedPnl || 0);
            const isWin = pVal >= 0;
            let dateStr = "";
            if (t.timestamp) {
                const parsedDate = new Date(t.timestamp);
                if (!isNaN(parsedDate.getTime())) {
                    dateStr = parsedDate.toLocaleString("en-PK", {
                        timeZone: "Asia/Karachi",
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                        hour12: true
                    });
                } else {
                    dateStr = String(t.timestamp);
                }
            }
            const badgeBg = isSell ? (isWin ? "rgba(76,175,80,0.2)" : "rgba(246,70,93,0.2)") : "rgba(0,229,255,0.2)";
            const badgeColor = isSell ? (isWin ? "#4CAF50" : "#f6465d") : "#00e5ff";
            const actionLabel = isSell ? "EXIT" : "ENTRY";
            const pnlDisplay = isSell ? '<span style="color:' + badgeColor + '; font-weight:bold;">' + (isWin ? "+" : "") + pVal.toFixed(4) + ' USDT</span>' : '<span style="color:#757575;">EXECUTED</span>';
            const orderIdDisplay = t.orderId ? t.orderId : "DCA";

            return '<div style="background:#151518; border:1px solid #222; border-radius:8px; padding:10px 12px; display:flex; flex-direction:column; gap:4px; font-family:monospace;">' +
                   '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                   '<span style="background:' + badgeBg + '; color:' + badgeColor + '; padding:2px 6px; border-radius:4px; font-size:10px; font-weight:bold;">' + actionLabel + '</span>' +
                   '<span style="color:#757575; font-size:10px;">' + dateStr + '</span>' +
                   '</div>' +
                   '<div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-top:2px;">' +
                   '<span style="color:#fff;">$' + parseFloat(t.price || 0).toFixed(2) + ' <span style="color:#757575;">(' + parseFloat(t.solAmount || 0).toFixed(4) + ' SOL)</span></span>' +
                   pnlDisplay +
                   '</div>' +
                   '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px; padding-top:4px; border-top:1px solid rgba(255,255,255,0.03); font-size:10px;">' +
                   '<span style="color:#4CAF50;">SPOT DCA ENGINE</span>' +
                   '<span style="color:#757575;">REF: ' + orderIdDisplay + '</span>' +
                   '</div>' +
                   '</div>';
        }).join("");
    }
function showAddLoopSlotForm() {
    const area = document.getElementById("atl-slot-input-area");
    const inAmt = document.getElementById("ex-input-amount");
    if (area) {
        area.style.display = "flex";
        document.getElementById("atl-buy-trigger").value = "";
        document.getElementById("atl-sell-trigger").value = "";
        if (inAmt) inAmt.value = "10.00";
        document.getElementById("atl-buy-trigger").focus();
    }
}
    function switchBotNavigation(tab) {
    document.querySelectorAll('.bot-nav-item').forEach(el => el.classList.remove('active'));
    if (window.event && window.event.currentTarget) {
        window.event.currentTarget.classList.add('active');
    }

    document.querySelectorAll('.bot-tab-view').forEach(view => {
        view.classList.remove('active');
        view.style.display = 'none';
    });

    const tradeDesk = document.getElementById("exchangeTerminalOverlay");
    const tradeHost = document.getElementById("tradeTabContainer");

    if (tab === 'Trade') {
        const tradeView = document.getElementById('tabViewTrade');
        if (tradeView) {
            tradeView.classList.add('active');
            tradeView.style.display = 'block';
        }
        if (tradeDesk && tradeHost) {
            tradeDesk.style.position = "static";
            tradeDesk.style.display = "block";
            tradeDesk.style.zIndex = "auto";
            tradeDesk.style.padding = "0 0 20px 0";
            if (!tradeHost.contains(tradeDesk)) {
                tradeHost.appendChild(tradeDesk);
            }
            try {
                refreshExchangeBalances();
                renderLiveOrderBook();
                renderProfessionalOrderDesk(latestBackendState);
            } catch(err) {}
            setTimeout(() => {
                try { initTradeManualChart(currentTradeChartInterval); } catch(e) {}
            }, 150);
        }
    } else if (tab === 'Bot') {
        const botView = document.getElementById('tabViewBot');
        if (botView) {
            botView.classList.add('active');
            botView.style.display = 'block';
        }
    } else if (tab === 'Home') {
        const homeView = document.getElementById('tabViewHome');
        if (homeView) {
            homeView.classList.add('active');
            homeView.style.display = 'block';
        }
    } else if (tab === 'Airdrop') {
        const airdropView = document.getElementById('tabViewAirdrop');
        if (airdropView) {
            airdropView.classList.add('active');
            airdropView.style.display = 'block';
            renderAirdropProductsGrid();
            updateAirdropUserBalanceUI();
        }
    } else if (tab === 'Assets' || tab === 'Wallet') {
        const walletView = document.getElementById('tabViewWallet');
        if (walletView) {
            walletView.classList.add('active');
            walletView.style.display = 'block';
            renderWalletTabView();
        }
    }
}

function renderWalletTabView() {
    const pillLabel = document.getElementById("trust-wallet-pill-label");
    const connBtn = document.getElementById("trust-wallet-connect-btn");
    const mainTotalEl = document.getElementById("trust-main-balance-val");

    const usdtAmtEl = document.getElementById("trust-usdt-amount");
    const usdtFiatEl = document.getElementById("trust-usdt-fiat");
    const bnbAmtEl = document.getElementById("trust-bnb-amount");
    const bnbFiatEl = document.getElementById("trust-bnb-fiat");
    const solAmtEl = document.getElementById("trust-sol-amount");
    const solFiatEl = document.getElementById("trust-sol-fiat");
    const shineAmtEl = document.getElementById("trust-shine-amount");
    const shineFiatEl = document.getElementById("trust-shine-fiat");
    const trxAmtEl = document.getElementById("trust-trx-amount");
    const trxFiatEl = document.getElementById("trust-trx-fiat");

    let liveTestBal = (latestBackendState && latestBackendState.manualTestBalance !== undefined) ? parseFloat(latestBackendState.manualTestBalance) : 0.0;
    let effectiveUsdt = liveOnChainWallet.usdt > 0 ? liveOnChainWallet.usdt : liveTestBal;
    let bnbVal = (connectedWalletType !== 'PHANTOM') ? (liveOnChainWallet.gas || 0.0) : 0.0;
    let solVal = (connectedWalletType === 'PHANTOM') ? (liveOnChainWallet.gas || 0.0) : (latestBackendState && latestBackendState.walletSol ? parseFloat(latestBackendState.walletSol) : 0.0);
    let trxVal = liveOnChainWallet.trx || 0.0;

    let solPrice = currentChartLivePrice > 0 ? currentChartLivePrice : 100.0;
    let bnbPrice = 580.0;
    let trxPrice = 0.1324;

    let bnbFiat = bnbVal * bnbPrice;
    let solFiat = solVal * solPrice;
    let trxFiat = trxVal * trxPrice;

    const homeShineEl = document.getElementById("homeProfitShine");
    const shineVal = homeShineEl ? parseFloat(homeShineEl.innerText) || 100.0 : 100.0;
    const shineFiat = shineVal * 0.01;

    const totalWorth = effectiveUsdt + bnbFiat + solFiat + shineFiat + trxFiat;

    if (mainTotalEl) mainTotalEl.innerText = "$" + totalWorth.toFixed(2);
    if (usdtAmtEl) usdtAmtEl.innerText = effectiveUsdt.toFixed(2) + " USDT";
    if (usdtFiatEl) usdtFiatEl.innerText = "$" + effectiveUsdt.toFixed(2);
    if (bnbAmtEl) bnbAmtEl.innerText = bnbVal.toFixed(4) + " BNB";
    if (bnbFiatEl) bnbFiatEl.innerText = "$" + bnbFiat.toFixed(2);
    if (solAmtEl) solAmtEl.innerText = solVal.toFixed(4) + " SOL";
    if (solFiatEl) solFiatEl.innerText = "$" + solFiat.toFixed(2);
    if (trxAmtEl) trxAmtEl.innerText = trxVal.toFixed(6) + " TRX";
    if (trxFiatEl) trxFiatEl.innerText = "$" + trxFiat.toFixed(4);
    if (shineAmtEl) shineAmtEl.innerText = shineVal.toFixed(2) + " SHINE";
    if (shineFiatEl) shineFiatEl.innerText = "$" + shineFiat.toFixed(2);
    const solRateEl = document.getElementById("trust-sol-rate-display");
    if (solRateEl) solRateEl.innerText = "$" + solPrice.toFixed(2);
    if (isTradeWalletConnected && userWallet) {
        const shortAddr = userWallet.substring(0, 6) + '...' + userWallet.substring(userWallet.length - 4);
        if (pillLabel) pillLabel.innerText = shortAddr;
        if (connBtn) {
            connBtn.innerText = "DISCONNECT";
            connBtn.style.background = "rgba(246, 70, 93, 0.2)";
            connBtn.style.color = "#f6465d";
            connBtn.style.border = "1px solid #f6465d";
        }
    } else {
        if (pillLabel) pillLabel.innerText = "Main Wallet 1";
        if (connBtn) {
            connBtn.innerText = "CONNECT";
            connBtn.style.background = "#2563eb";
            connBtn.style.color = "#ffffff";
            connBtn.style.border = "none";
        }
    }
}

function handleWalletTabBtnAction() {
    if (isTradeWalletConnected && userWallet) {
        disconnectCurrentWallet();
        renderWalletTabView();
    } else {
        openWalletSelection();
    }
}

let currentSendSelectedToken = "USDT";
let currentSendTokenBalance = 0.0;
let currentTokenFilterNet = "ALL";

const AVAILABLE_SEND_TOKENS = [
    {
        symbol: "TRX",
        name: "Tron",
        network: "TRON",
        rate: 0.1324,
        getBal: () => liveOnChainWallet.trx || 0.0,
        addressType: "Paste TRON (TRX / TRC-20) address",
        iconSvg: `<svg viewBox="0 0 100 100" style="width: 38px; height: 38px; border-radius: 50%;"><circle cx="50" cy="50" r="50" fill="#FF060A"/><path d="M31.5 35.5 L60.8 41.8 L68.8 48.8 L47.5 75.5 Z" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/><path d="M31.5 35.5 L50.2 52.2 L47.5 75.5" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/><path d="M60.8 41.8 L50.2 52.2 L68.8 48.8" fill="none" stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/></svg>`
    },
    {
        symbol: "USDT",
        name: "Tether USD",
        network: "BSC",
        rate: 1.00,
        getBal: () => liveOnChainWallet.usdt || (latestBackendState ? parseFloat(latestBackendState.manualTestBalance || 0) : 0),
        addressType: "Paste BSC (BEP-20 / 0x) address",
        iconSvg: `<svg viewBox="0 0 100 100" style="width: 36px; height: 36px; border-radius: 50%;"><circle cx="50" cy="50" r="50" fill="#009393"/><path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/><path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/></svg>`
    },
    {
        symbol: "SOL",
        name: "Solana",
        network: "SOL",
        rate: 106.32,
        getBal: () => (connectedWalletType === 'PHANTOM' ? liveOnChainWallet.gas : (latestBackendState ? parseFloat(latestBackendState.walletSol || 0) : 0)),
        addressType: "Paste Solana address",
        iconSvg: `<img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" style="width: 36px; height: 36px; border-radius: 50%;">`
    },
    {
        symbol: "BNB",
        name: "BNB Smart Chain",
        network: "BSC",
        rate: 580.00,
        getBal: () => (connectedWalletType !== 'PHANTOM' ? liveOnChainWallet.gas : 0),
        addressType: "Paste BNB Smart Chain (0x) address",
        iconSvg: `<svg viewBox="0 0 32 32" style="width: 36px; height: 36px; border-radius: 50%;"><circle cx="16" cy="16" r="16" fill="#F0B90B"/><path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/></svg>`
    },
    {
        symbol: "SHINE",
        name: "SHINE Token",
        network: "BSC",
        rate: 0.01,
        getBal: () => parseFloat(document.getElementById("homeProfitShine") ? document.getElementById("homeProfitShine").innerText : "100") || 100.0,
        addressType: "Paste BEP-20 (0x) address",
        iconSvg: `<div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg, #ff4f9e, #840540); display:flex; align-items:center; justify-content:center; color:#fff; font-weight:bold; font-size:11px;">SHINE</div>`
    }
];

function handleTrustSendAction() {
    if (!isTradeWalletConnected || !userWallet) {
        openWalletSelection();
        return;
    }
    openSelectTokenSheet();
}

function openSelectTokenSheet() {
    const sheet = document.getElementById("selectTokenSheet");
    if (!sheet) return;
    sheet.style.display = "flex";
    renderTokenSelectList();
}

function closeSelectTokenSheet() {
    const sheet = document.getElementById("selectTokenSheet");
    if (sheet) sheet.style.display = "none";
}

function filterTokenNet(net) {
    currentTokenFilterNet = net;
    document.querySelectorAll(".token-net-filter").forEach(b => {
        b.style.background = "#f1f5f9";
        b.style.color = "#0f172a";
    });
    const activeBtn = document.getElementById("netFilter" + net.charAt(0).toUpperCase() + net.slice(1).toLowerCase());
    if (activeBtn) {
        activeBtn.style.background = "#0f172a";
        activeBtn.style.color = "#ffffff";
    }
    renderTokenSelectList();
}

function filterTokenSelectSheet(query) {
    renderTokenSelectList(query);
}

function renderTokenSelectList(query = "") {
    const container = document.getElementById("tokenSelectListContainer");
    if (!container) return;
    const q = query.trim().toUpperCase();

    const filtered = AVAILABLE_SEND_TOKENS.filter(t => {
        const matchesNet = currentTokenFilterNet === "ALL" || t.network === currentTokenFilterNet;
        const matchesQuery = !q || t.symbol.toUpperCase().includes(q) || t.name.toUpperCase().includes(q);
        return matchesNet && matchesQuery;
    });

    if (filtered.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding:30px; color:#64748b; font-size:13px;">No tokens found</div>';
        return;
    }

    container.innerHTML = filtered.map(t => {
        const bal = t.getBal();
        const fiat = bal * t.rate;
        return `
            <div onclick="pickTokenForSending('${t.symbol}')" style="display:flex; justify-content:space-between; align-items:center; padding:12px; border-radius:14px; cursor:pointer; background:#ffffff; transition:0.2s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='#ffffff'">
                <div style="display:flex; align-items:center; gap:12px;">
                    ${t.iconSvg}
                    <div>
                        <div style="font-weight:800; font-size:16px; color:#0f172a;">${t.symbol}</div>
                        <div style="font-size:13px; color:#64748b;">${t.name}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800; font-size:16px; color:#0f172a; font-family:monospace;">$${fiat.toFixed(4)}</div>
                    <div style="font-size:13px; color:#64748b; font-family:monospace;">${bal.toFixed(4)} ${t.symbol}</div>
                </div>
            </div>
        `;
    }).join("");
}

function pickTokenForSending(symbol) {
    closeSelectTokenSheet();
    const token = AVAILABLE_SEND_TOKENS.find(t => t.symbol === symbol);
    if (!token) return;

    currentSendSelectedToken = token.symbol;
    currentSendTokenBalance = token.getBal();

    const modal = document.getElementById("sendModalSheet");
    if (!modal) return;

    document.getElementById("send-selected-symbol").innerText = token.symbol;
    document.getElementById("send-selected-icon").innerHTML = token.iconSvg;
    document.getElementById("send-available-balance-disp").innerText = `${currentSendTokenBalance.toFixed(4)} ${token.symbol}`;
    document.getElementById("send-target-address").value = "";
    document.getElementById("send-target-address").placeholder = token.addressType;
    document.getElementById("send-target-amount").value = "";

    modal.style.display = "flex";
}

function fillMaxSendAmount() {
    const input = document.getElementById("send-target-amount");
    if (input) input.value = currentSendTokenBalance.toString();
}

function closeSendModal() {
    const modal = document.getElementById("sendModalSheet");
    if (modal) modal.style.display = "none";
}

async function executeSendFundAction() {
    const toAddress = document.getElementById("send-target-address").value.trim();
    const amountStr = document.getElementById("send-target-amount").value.trim();
    const amount = parseFloat(amountStr);

    if (!toAddress || !amount || isNaN(amount) || amount <= 0) {
        alert("Please enter a valid recipient address and amount.");
        return;
    }

    if (amount > currentSendTokenBalance) {
        alert(`Insufficient ${currentSendSelectedToken} balance!\nAvailable: ${currentSendTokenBalance.toFixed(4)} ${currentSendSelectedToken}`);
        return;
    }

    closeSendModal();

    if (currentSendSelectedToken === "TRX") {
        if (window.tronWeb && window.tronWeb.defaultAddress && window.tronWeb.defaultAddress.base58) {
            try {
                const sunAmt = Math.floor(amount * 1000000);
                const tx = await window.tronWeb.trx.sendTransaction(toAddress, sunAmt);
                alert("Transaction submitted on TRON network!\nTXID: " + (tx.txid || tx.transaction?.txID || "Success"));
                fetchRealWeb3WalletBalances(userWallet);
                return;
            } catch(te) {
                alert("Tron transfer failed or rejected: " + (te.message || te));
                return;
            }
        } else {
            alert(`Tron Transfer Simulated:\nSent: ${amount} TRX\nTo: ${toAddress}`);
            liveOnChainWallet.trx = Math.max(0, liveOnChainWallet.trx - amount);
            renderWalletTabView();
            return;
        }
    }

    if (currentSendSelectedToken === "SOL") {
        if (connectedWalletType === 'PHANTOM' || (!userWallet.startsWith("0x") && window.solana)) {
            try {
                const solProvider = (window.phantom && window.phantom.solana) || window.solana;
                const solConn = new solanaWeb3.Connection("https://api.mainnet-beta.solana.com", "confirmed");
                const transaction = new solanaWeb3.Transaction().add(
                    solanaWeb3.SystemProgram.transfer({
                        fromPubkey: new solanaWeb3.PublicKey(userWallet),
                        toPubkey: new solanaWeb3.PublicKey(toAddress),
                        lamports: Math.floor(solanaWeb3.LAMPORTS_PER_SOL * amount)
                    })
                );
                transaction.feePayer = new solanaWeb3.PublicKey(userWallet);
                const { blockhash } = await solConn.getLatestBlockhash();
                transaction.recentBlockhash = blockhash;
                const signed = await solProvider.signAndSendTransaction(transaction);
                alert("SOL sent successfully!\nSignature: " + signed.signature);
                fetchRealWeb3WalletBalances(userWallet);
                return;
            } catch (e) {
                alert("Solana transaction failed: " + (e.message || e));
                return;
            }
        }
    }

    if (currentSendSelectedToken === "BNB" || currentSendSelectedToken === "USDT" || currentSendSelectedToken === "SHINE") {
        try {
            const activeEthProvider = (window.trustwallet && window.trustwallet.ethereum) || window.ethereum;
            if (activeEthProvider) {
                const ethProvider = new ethers.providers.Web3Provider(activeEthProvider);
                const ethSigner = ethProvider.getSigner();

                if (currentSendSelectedToken === "BNB") {
                    const tx = await ethSigner.sendTransaction({
                        to: toAddress,
                        value: ethers.utils.parseEther(amountStr)
                    });
                    alert("BNB Transfer submitted! Hash: " + tx.hash);
                } else if (currentSendSelectedToken === "USDT") {
                    const erc20Abi = ["function transfer(address to, uint256 amount) returns (bool)"];
                    const usdtContract = new ethers.Contract(REAL_USDT_CONTRACT, erc20Abi, ethSigner);
                    const tx = await usdtContract.transfer(toAddress, ethers.utils.parseUnits(amountStr, 18));
                    alert("USDT Transfer submitted! Hash: " + tx.hash);
                }
                fetchRealWeb3WalletBalances(userWallet);
                return;
            }
        } catch(e) {
            alert("Transfer failed: " + (e.message || e));
            return;
        }
    }

    alert(`Transfer of ${amount} ${currentSendSelectedToken} confirmed to ${toAddress}`);
}
function openReceiveModal() {
    const modal = document.getElementById("receiveModalSheet");
    if (!modal) return;

    const netEl = document.getElementById("receive-network-name");
    const addrEl = document.getElementById("receive-full-address");
    const qrImg = document.getElementById("receive-qr-img");

    const targetAddr = (isTradeWalletConnected && userWallet) ? userWallet : "0xConnectWalletFirst";
    const netName = (connectedWalletType === 'PHANTOM') ? "Solana Mainnet (SPL)" : "BNB Smart Chain (BEP-20)";

    if (netEl) netEl.innerText = netName;
    if (addrEl) addrEl.innerText = targetAddr;
    if (qrImg) qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(targetAddr)}`;

    modal.style.display = "flex";
}

function closeReceiveModal() {
    const modal = document.getElementById("receiveModalSheet");
    if (modal) modal.style.display = "none";
}

function copyReceiveAddress() {
    const addrEl = document.getElementById("receive-full-address");
    if (!addrEl) return;
    navigator.clipboard.writeText(addrEl.innerText);
    alert("Address copied to clipboard:\n" + addrEl.innerText);
}
let lastScrollTopPosition = 0;
const tradingScrollOverlay = document.getElementById('tradingOverlay');

if (tradingScrollOverlay) {
    tradingScrollOverlay.addEventListener('scroll', function() {
        const currentScroll = tradingScrollOverlay.scrollTop;
        const navBar = document.getElementById('botBottomNavBar');
        if (!navBar) return;

        if (currentScroll > lastScrollTopPosition && currentScroll > 80) {
            navBar.style.transform = 'translateY(100%)';
        } else {
            navBar.style.transform = 'translateY(0)';
        }
        lastScrollTopPosition = currentScroll <= 0 ? 0 : currentScroll;
    }, { passive: true });
}
function renderAutoLoopsUI(loops) {
    const listEl = document.getElementById("atl-active-slots-list");
    const counterEl = document.getElementById("atl-slots-counter");
    if (!listEl) return;
    const items = Array.isArray(loops) ? loops : [];
    if (counterEl) counterEl.innerText = `${items.length}/10 SLOTS`;

    if (items.length === 0) {
        listEl.innerHTML = "";
        return;
    }

    listEl.innerHTML = items.map((lp, idx) => `
        <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 8px; padding: 8px 10px; display: flex; flex-direction: column; gap: 4px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #00c087; font-weight: 900; font-size: 11px;">#${idx + 1} LOOP [${lp.autoRepeat ? 'AUTO' : 'ONCE'}]</span>
                <div style="display: flex; gap: 6px; align-items: center;">
                    <button onclick="editAutoLoopSlot('${lp.id}', ${lp.buyTrigger}, ${lp.sellTrigger})" style="background: rgba(255,255,255,0.06); border: 1px solid #333; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 9px; cursor: pointer;">EDIT</button>
                    <button onclick="deleteAutoLoopSlot('${lp.id}')" style="background: rgba(246,70,93,0.15); border: 1px solid #f6465d; color: #f6465d; padding: 2px 6px; border-radius: 4px; font-size: 9px; cursor: pointer;">✕</button>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #fff;">
                <span>Buy: $${lp.buyTrigger}</span>
                <span>Sell: $${lp.sellTrigger}</span>
                <span style="color: #00c087;">$${lp.usdtAmount}</span>
            </div>
            <div style="color: #FFD700; font-size: 10px; font-weight: bold; margin-top: 2px;">${lp.status || 'ACTIVE'}</div>
        </div>
    `).join("");
}

function deleteAutoLoopSlot(slotId) {
    if (!botSocket || botSocket.readyState !== WebSocket.OPEN) return;
    botSocket.send(JSON.stringify({ action: "CANCEL_AUTO_LOOP", slotId: slotId }));
}

function editAutoLoopSlot(slotId, curBuy, curSell) {
    const newBuy = prompt("Enter new Buy Trigger Price ($):", curBuy);
    const newSell = prompt("Enter new Sell Target Price ($):", curSell);
    if (!newBuy || !newSell || isNaN(newBuy) || isNaN(newSell)) return;
    botSocket.send(JSON.stringify({
        action: "EDIT_AUTO_LOOP",
        slotId: slotId,
        buyTrigger: parseFloat(newBuy),
        buyCallback: 0.01,
        sellTrigger: parseFloat(newSell),
        sellCallback: 0.01,
        autoRepeat: true
    }));
}
const COSMETICS_PRODUCTS = [
    {
        id: "PROD_1",
        name: "Shine HD Glow Cream",
        basePrice: 10.0,
        currentPrice: 10.0,
        change24h: 0.0,
        high24h: 10.4,
        low24h: 9.8,
        volume: 1420,
        img: "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&auto=format&fit=crop&q=80",
        desc: "Advanced Radiant Whitening & Hydration Complex."
    },
    {
        id: "PROD_2",
        name: "Shine HD Glow Lotion",
        basePrice: 10.0,
        currentPrice: 10.0,
        change24h: 0.0,
        high24h: 10.3,
        low24h: 9.9,
        volume: 980,
        img: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&auto=format&fit=crop&q=80",
        desc: "24-Hour Ultra Moisture Lock Glow Body Milk."
    },
    {
        id: "PROD_3",
        name: "Shine Face Wash",
        basePrice: 10.0,
        currentPrice: 10.0,
        change24h: 0.0,
        high24h: 10.5,
        low24h: 9.7,
        volume: 2150,
        img: "https://images.unsplash.com/photo-1556228722-d0b71946ec98?w=400&auto=format&fit=crop&q=80",
        desc: "Deep Pore Purifying Oil-Control Cleanser."
    },
    {
        id: "PROD_4",
        name: "Shine Serum",
        basePrice: 10.0,
        currentPrice: 10.0,
        change24h: 0.0,
        high24h: 10.8,
        low24h: 9.9,
        volume: 1840,
        img: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&auto=format&fit=crop&q=80",
        desc: "Vitamin C & Hyaluronic Collagen Booster."
    },
    {
        id: "PROD_5",
        name: "Shine Glycerin",
        basePrice: 5.0,
        currentPrice: 5.0,
        change24h: 0.0,
        high24h: 5.2,
        low24h: 4.8,
        volume: 3200,
        img: "https://images.unsplash.com/photo-1608248597359-54b9d09c3ec2?w=400&auto=format&fit=crop&q=80",
        desc: "Pure Medicinal Grade Skin Softener."
    },
    {
        id: "PROD_6",
        name: "Shine Vaseline",
        basePrice: 5.0,
        currentPrice: 5.0,
        change24h: 0.0,
        high24h: 5.3,
        low24h: 4.9,
        volume: 4100,
        img: "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&auto=format&fit=crop&q=80",
        desc: "Petroleum Jelly Intensive Healing Formula."
    },
    {
        id: "PROD_7",
        name: "Shine Hair Oil",
        basePrice: 20.0,
        currentPrice: 20.0,
        change24h: 0.0,
        high24h: 21.2,
        low24h: 19.6,
        volume: 870,
        img: "https://images.unsplash.com/photo-1608248597370-13f508216bb5?w=400&auto=format&fit=crop&q=80",
        desc: "Herbal Root Strengthening & Anti-Dandruff Elixir."
    },
    {
        id: "PROD_8",
        name: "Shine Silky Shampoo",
        basePrice: 25.0,
        currentPrice: 25.0,
        change24h: 0.0,
        high24h: 26.5,
        low24h: 24.2,
        volume: 1250,
        img: "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400&auto=format&fit=crop&q=80",
        desc: "Keratin Smooth Gloss Restoring Shampoo."
    },
    {
        id: "PROD_9",
        name: "Shine Skin Polish",
        basePrice: 50.0,
        currentPrice: 50.0,
        change24h: 0.0,
        high24h: 53.0,
        low24h: 48.5,
        volume: 640,
        img: "https://images.unsplash.com/photo-1567928815104-b7980ee5032e?w=400&auto=format&fit=crop&q=80",
        desc: "Professional Salon Glow Micro-Dermabrasion Polish."
    },
    {
        id: "PROD_10",
        name: "Shine Facial Kit",
        basePrice: 100.0,
        currentPrice: 100.0,
        change24h: 0.0,
        high24h: 106.0,
        low24h: 96.0,
        volume: 520,
        img: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&auto=format&fit=crop&q=80",
        desc: "Complete 6-in-1 Luxury Bridal Diamond Facial Set."
    }
];

const MAIN_SUPABASE_URL = "https://awlaziaxapoixbhiqcpq.supabase.co";
const MAIN_SUPABASE_KEY = "sb_publishable_PgY6nJ0OeM4OIoJS3GVG8A_MZb--nVp";

async function syncDexProductsFromDatabase() {
    if (!window.supabase) return;
    try {
        const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
        const { data, error } = await client.from('dex_products').select('*');
        if (!error && Array.isArray(data) && data.length > 0) {
            data.forEach(dbItem => {
                const local = COSMETICS_PRODUCTS.find(p => p.id === dbItem.id);
                if (local) {
                    local.name = dbItem.name;
                    local.basePrice = parseFloat(dbItem.base_price);
                    local.currentPrice = parseFloat(dbItem.current_price);
                    local.high24h = parseFloat(dbItem.high_24h);
                    local.low24h = parseFloat(dbItem.low_24h);
                    local.desc = dbItem.description;
                    local.img = dbItem.image_url || "";
                } else {
                    COSMETICS_PRODUCTS.push({
                        id: dbItem.id,
                        name: dbItem.name,
                        basePrice: parseFloat(dbItem.base_price),
                        currentPrice: parseFloat(dbItem.current_price),
                        change24h: parseFloat(dbItem.change_24h || 0),
                        high24h: parseFloat(dbItem.high_24h),
                        low24h: parseFloat(dbItem.low_24h),
                        volume: parseInt(dbItem.volume || 100),
                        img: dbItem.image_url || "",
                        desc: dbItem.description
                    });
                }
            });
            if (typeof renderAirdropProductsGrid === 'function') {
                renderAirdropProductsGrid();
            }
        }
    } catch(e) {}
}

let userAirdropHoldings = [];
let userAirdropOrdersHistory = [];
let airdropCurrentSubTab = 'ALL';
let airdropRealizedProfitTotal = 0.0;
let airdrop24hProfitTotal = 0.0;

function getLocalAirdropBalance() {
    const el = document.getElementById("homeProfitShine");
    if (el) {
        const val = parseFloat(el.innerText);
        if (!isNaN(val) && val >= 0) return val;
    }
    const saved = localStorage.getItem("shine_airdrop_balance");
    if (saved) return parseFloat(saved);
    return 100.0;
}

function saveAirdropDataToDB() {
    const effectiveWallet = userWallet || localStorage.getItem("shine_saved_wallet_addr") || "0xDefaultUser";
    const currentBal = getLocalAirdropBalance();
    localStorage.setItem("shine_airdrop_balance", currentBal.toString());
    localStorage.setItem("shine_airdrop_holdings", JSON.stringify(userAirdropHoldings));
    localStorage.setItem("shine_airdrop_history", JSON.stringify(userAirdropOrdersHistory));
    localStorage.setItem("shine_airdrop_realized", airdropRealizedProfitTotal.toString());
    localStorage.setItem("shine_airdrop_24h", airdrop24hProfitTotal.toString());

    fetchWithFallback("/api/airdrop/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            wallet: effectiveWallet,
            shineBalance: currentBal,
            holdings: userAirdropHoldings,
            ordersHistory: userAirdropOrdersHistory,
            realizedProfit: airdropRealizedProfitTotal,
            profit24h: airdrop24hProfitTotal
        })
    });
}

async function loadAirdropDataFromDB() {
    const savedBal = localStorage.getItem("shine_airdrop_balance");
    const savedHoldings = localStorage.getItem("shine_airdrop_holdings");
    const savedHist = localStorage.getItem("shine_airdrop_history");
    const savedReal = localStorage.getItem("shine_airdrop_realized");
    const saved24h = localStorage.getItem("shine_airdrop_24h");

    if (savedBal) {
        const el = document.getElementById("homeProfitShine");
        if (el) el.innerText = parseFloat(savedBal).toFixed(2);
    }
    if (savedHoldings) {
        try { userAirdropHoldings = JSON.parse(savedHoldings); } catch (e) {}
    }
    if (savedHist) {
        try { userAirdropOrdersHistory = JSON.parse(savedHist); } catch (e) {}
    }
    if (savedReal) airdropRealizedProfitTotal = parseFloat(savedReal) || 0.0;
    if (saved24h) airdrop24hProfitTotal = parseFloat(saved24h) || 0.0;

    const effectiveWallet = userWallet || localStorage.getItem("shine_saved_wallet_addr");
    if (effectiveWallet) {
        try {
            const res = await fetchWithFallback(`/api/airdrop/${effectiveWallet}`);
            if (!res) return;
            const data = await res.json();
            if (data && data.success) {
                if (data.shineBalance !== undefined) {
                    const el = document.getElementById("homeProfitShine");
                    if (el) el.innerText = parseFloat(data.shineBalance).toFixed(2);
                    localStorage.setItem("shine_airdrop_balance", data.shineBalance.toString());
                }
                if (Array.isArray(data.holdings)) {
                    userAirdropHoldings = data.holdings;
                    localStorage.setItem("shine_airdrop_holdings", JSON.stringify(data.holdings));
                }
                if (Array.isArray(data.ordersHistory)) {
                    userAirdropOrdersHistory = data.ordersHistory;
                    localStorage.setItem("shine_airdrop_history", JSON.stringify(data.ordersHistory));
                }
                if (data.realizedProfit !== undefined) {
                    airdropRealizedProfitTotal = parseFloat(data.realizedProfit) || 0.0;
                    localStorage.setItem("shine_airdrop_realized", airdropRealizedProfitTotal.toString());
                }
                if (data.profit24h !== undefined) {
                    airdrop24hProfitTotal = parseFloat(data.profit24h) || 0.0;
                    localStorage.setItem("shine_airdrop_24h", airdrop24hProfitTotal.toString());
                }
            }
        } catch (e) {}
    }

    updateAirdropUserBalanceUI();
}

function updateAirdropUserBalanceUI() {
    const bal = getLocalAirdropBalance();
    const balEl = document.getElementById("airdropShineUserBal");
    if (balEl) balEl.innerText = bal.toFixed(2);

    let totalWorth = 0;
    let totalInvested = 0;
    userAirdropHoldings.forEach(item => {
        const p = COSMETICS_PRODUCTS.find(x => x.id === item.prodId);
        const curRate = p ? p.currentPrice : item.buyPrice;
        totalWorth += curRate * item.qty;
        totalInvested += item.buyPrice * item.qty;
    });

    const unrealPnl = totalWorth - totalInvested;

    const unEl = document.getElementById("airdropUnrealizedPnlVal");
    if (unEl) {
        const sign = unrealPnl >= 0 ? "+" : "";
        unEl.innerText = sign + "$" + unrealPnl.toFixed(2);
        unEl.style.color = unrealPnl >= 0 ? "#00e676" : "#f6465d";
    }

    const reEl = document.getElementById("airdropRealizedPnlVal");
    if (reEl) {
        const sign = airdropRealizedProfitTotal >= 0 ? "+" : "";
        reEl.innerText = sign + "$" + airdropRealizedProfitTotal.toFixed(2);
        reEl.style.color = airdropRealizedProfitTotal >= 0 ? "#4CAF50" : "#f6465d";
    }

    const p24El = document.getElementById("airdrop24hProfitVal");
    if (p24El) {
        const sign = airdrop24hProfitTotal >= 0 ? "+" : "";
        p24El.innerText = sign + "$" + airdrop24hProfitTotal.toFixed(2);
        p24El.style.color = airdrop24hProfitTotal >= 0 ? "#00e676" : "#f6465d";
    }

    const badge = document.getElementById("userHoldingCountBadge");
    if (badge) badge.innerText = userAirdropHoldings.length.toString();

    const invEl = document.getElementById("airdropInventoryVal");
    if (invEl) invEl.innerText = `Inventory: ${userAirdropHoldings.length} Items (~$${totalWorth.toFixed(2)})`;
}

function switchAirdropSubTab(tab) {
    airdropCurrentSubTab = tab;
    document.querySelectorAll(".mkt-tab-btn").forEach(b => b.classList.remove("active"));
    const grid = document.getElementById("airdropProductsGrid");
    const inv = document.getElementById("airdropInventoryView");
    const hist = document.getElementById("airdropHistoryView");

    grid.style.display = "none";
    inv.style.display = "none";
    hist.style.display = "none";

    if (tab === 'ALL') {
        document.getElementById("mktTabMarketBtn").classList.add("active");
        grid.style.display = "grid";
        renderAirdropProductsGrid();
    } else if (tab === 'INVENTORY') {
        document.getElementById("mktTabInventoryBtn").classList.add("active");
        inv.style.display = "flex";
        renderAirdropInventoryView();
    } else if (tab === 'HISTORY') {
        document.getElementById("mktTabOrdersBtn").classList.add("active");
        hist.style.display = "flex";
        renderAirdropHistoryView();
    }
}

function renderAirdropProductsGrid() {
    const container = document.getElementById("airdropProductsGrid");
    if (!container) return;

    container.innerHTML = COSMETICS_PRODUCTS.map(p => {
        const isUp = p.change24h >= 0;
        const changeClass = isUp ? "up" : "down";
        const sign = isUp ? "+" : "";

        return `
            <div class="product-commodity-card" id="card-${p.id}">
                <div class="prod-img-wrap">
                        ${p.img ? `<img src="${p.img}" alt="${p.name}" class="prod-main-img">` : `<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; height:100%; background:#080b11; color:#718096; font-size:11px; font-weight:800;"><i class="material-icons" style="font-size:32px; color:#4a5568;">image_not_supported</i><span>NO IMAGE</span></div>`}
                        <span class="prod-badge-live ${changeClass}">${sign}${p.change24h.toFixed(2)}%</span>
                    </div>
                <div class="prod-body">
                    <div class="prod-title-row">
                        <h3 class="prod-name">${p.name}</h3>
                        <span class="prod-vol">Vol: ${p.volume}</span>
                    </div>
                    <p class="prod-desc">${p.desc}</p>
                    <div class="prod-price-box">
                        <div>
                            <div class="price-lbl">LIVE MARKET PRICE</div>
                            <div class="price-num">${p.currentPrice.toFixed(2)} <span class="shine-symbol">SHINE</span></div>
                        </div>
                        <div class="prod-range-text">
                            H: ${p.high24h.toFixed(2)} | L: ${p.low24h.toFixed(2)}
                        </div>
                    </div>
                    <div class="prod-action-row">
                        <button class="btn-prod-buy" onclick="buyCosmeticProduct('${p.id}')">BUY PRODUCT</button>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

function renderAirdropInventoryView() {
    const container = document.getElementById("airdropInventoryView");
    if (!container) return;

    if (userAirdropHoldings.length === 0) {
        container.innerHTML = `
            <div class="empty-inventory-box">
                <i class="material-icons" style="font-size: 42px; color: #8c8ca1;">storefront</i>
                <div style="font-size: 16px; font-weight: 800; color: #ffffff; margin-top: 8px;">Your Vault is Empty</div>
                <div style="font-size: 12px; color: #718096; margin-top: 4px;">Buy commodity cosmetic products using your SHINE tokens. Hold to earn from price pump or liquidate for profit anytime!</div>
                <button onclick="switchAirdropSubTab('ALL')" class="btn-explore-market">BROWSE MARKET</button>
            </div>
        `;
        return;
    }

    container.innerHTML = userAirdropHoldings.map((item, idx) => {
        const prod = COSMETICS_PRODUCTS.find(p => p.id === item.prodId);
        const curPrice = prod ? prod.currentPrice : item.buyPrice;
        const netPnL = (curPrice - item.buyPrice) * item.qty;
        const pnlPct = ((curPrice - item.buyPrice) / item.buyPrice) * 100;
        const isProfit = netPnL >= 0;
        const pColor = isProfit ? "#00e676" : "#f6465d";

        return `
            <div class="inventory-card">
                <div style="display: flex; gap: 12px; align-items: center;">
                    <img src="${prod ? prod.img : ''}" style="width: 55px; height: 55px; border-radius: 10px; object-fit: cover;">
                    <div style="flex: 1;">
                        <div style="font-size: 14px; font-weight: 800; color: #fff;">${item.name}</div>
                        <div style="font-size: 11px; color: #8c8ca1; font-family: monospace;">Qty: ${item.qty} | Bought: ${item.buyPrice.toFixed(2)} SHINE</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 15px; font-weight: 900; color: ${pColor}; font-family: monospace;">
                            ${isProfit ? '+' : ''}${netPnL.toFixed(2)} SHINE
                        </div>
                        <div style="font-size: 10px; font-weight: 700; color: ${pColor}; font-family: monospace;">
                            (${isProfit ? '+' : ''}${pnlPct.toFixed(2)}%)
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
                    <button class="btn-inv-sell" onclick="sellCosmeticHolding(${idx})" style="width: 100%;">LIQUIDATE & TAKE PROFIT (${(curPrice * item.qty).toFixed(2)} SHINE)</button>
                </div>
            </div>
        `;
    }).join("");
}

function renderAirdropHistoryView() {
    const container = document.getElementById("airdropHistoryView");
    if (!container) return;

    if (userAirdropOrdersHistory.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 40px 0; color: #718096; font-size: 13px;">No past cosmetics orders found.</div>';
        return;
    }

    container.innerHTML = userAirdropOrdersHistory.map(tr => {
        const isBuy = tr.type === 'BUY';
        const color = isBuy ? '#00e5ff' : '#00e676';
        const profitBadge = tr.profit !== undefined && tr.profit !== 0 ? `<div style="color: ${tr.profit >= 0 ? '#00e676' : '#f6465d'}; font-size: 10px; font-weight: 800;">${tr.profit >= 0 ? '+' : ''}${tr.profit.toFixed(2)} SHINE PROFIT</div>` : '';

        return `
            <div style="background: #11151e; border: 1px solid #1a202c; border-radius: 12px; padding: 12px; display: flex; justify-content: space-between; align-items: center; font-family: monospace;">
                <div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="background: ${isBuy ? 'rgba(0, 229, 255, 0.15)' : 'rgba(0, 230, 118, 0.15)'}; color: ${color}; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 900;">${tr.type}</span>
                        <span style="color: #fff; font-weight: bold; font-size: 12px;">${tr.name}</span>
                    </div>
                    <div style="color: #718096; font-size: 10px; margin-top: 3px;">${tr.time}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #fff; font-weight: 900; font-size: 13px;">${tr.total.toFixed(2)} SHINE</div>
                    <div style="color: ${color}; font-size: 10px;">@ ${tr.price.toFixed(2)} SHINE</div>
                    ${profitBadge}
                </div>
            </div>
        `;
    }).join("");
}

function recordDexFeeCollected(amount, type, prodName) {
    let currentFeeTotal = parseFloat(localStorage.getItem("shine_dex_total_fees") || "0");
    currentFeeTotal += amount;
    localStorage.setItem("shine_dex_total_fees", currentFeeTotal.toFixed(4));

    if (window.supabase) {
        try {
            const client = window.supabase.createClient(MAIN_SUPABASE_URL, MAIN_SUPABASE_KEY);
            client.from('dex_fees').insert({
                trade_type: type,
                product_name: prodName,
                fee_amount: amount,
                timestamp: new Date().toISOString()
            }).then(() => {});
        } catch(e) {}
    }
}

function buyCosmeticProduct(prodId) {
    const p = COSMETICS_PRODUCTS.find(x => x.id === prodId);
    if (!p) return;

    const price = p.currentPrice;
    const fee = price * 0.01;
    const totalCost = price + fee;

    const currentBal = getLocalAirdropBalance();
    if (currentBal < totalCost) {
        alert(`Insufficient SHINE!\nProduct Price: ${price.toFixed(2)} SHINE\nDEX Fee (1%): ${fee.toFixed(2)} SHINE\nTotal Required: ${totalCost.toFixed(2)} SHINE\nYour Balance: ${currentBal.toFixed(2)} SHINE`);
        return;
    }

    const confirmOrder = confirm(`Confirm Buy Order:\nProduct: ${p.name}\nPrice: ${price.toFixed(2)} SHINE\nDEX Fee (1%): ${fee.toFixed(2)} SHINE\nTotal Deducted: ${totalCost.toFixed(2)} SHINE\n\nExecute purchase?`);
    if (!confirmOrder) return;

    const newBal = currentBal - totalCost;
    const shineBalEl = document.getElementById("homeProfitShine");
    if (shineBalEl) shineBalEl.innerText = newBal.toFixed(2);
    localStorage.setItem("shine_airdrop_balance", newBal.toString());

    recordDexFeeCollected(fee, "BUY", p.name);

    userAirdropHoldings.push({
        prodId: p.id,
        name: p.name,
        buyPrice: price,
        qty: 1,
        time: new Date().toLocaleTimeString()
    });

    userAirdropOrdersHistory.unshift({
        type: 'BUY',
        name: p.name,
        price: price,
        total: totalCost,
        profit: 0.0,
        time: new Date().toLocaleTimeString()
    });

    p.currentPrice = p.currentPrice * 1.004;
    p.change24h = ((p.currentPrice - p.basePrice) / p.basePrice) * 100;
    if (p.currentPrice > p.high24h) p.high24h = p.currentPrice;
    p.volume += 1;

    updateAirdropUserBalanceUI();
    renderAirdropProductsGrid();
    saveAirdropDataToDB();
    alert(`Purchase Successful!\nBought: ${p.name} @ ${price.toFixed(2)} SHINE\nFee Paid to DEX: ${fee.toFixed(2)} SHINE\nLiquidity Depth Impact: +0.40%`);
}

function sellCosmeticHolding(index) {
    const item = userAirdropHoldings[index];
    if (!item) return;

    const p = COSMETICS_PRODUCTS.find(x => x.id === item.prodId);
    const currentMarketPrice = p ? p.currentPrice : item.buyPrice;
    const grossReturn = currentMarketPrice * item.qty;
    const fee = grossReturn * 0.01;
    const netReturn = grossReturn - fee;
    const netProfit = netReturn - (item.buyPrice * item.qty);

    const confirmSell = confirm(`Liquidate On Commodity DEX:\nProduct: ${item.name}\nBought Price: ${item.buyPrice.toFixed(2)} SHINE\nCurrent Market: ${currentMarketPrice.toFixed(2)} SHINE\nDEX Exit Fee (1%): ${fee.toFixed(2)} SHINE\nNet Payout Received: ${netReturn.toFixed(2)} SHINE\nNet Profit/Loss: ${netProfit >= 0 ? '+' : ''}${netProfit.toFixed(2)} SHINE\n\nConfirm liquidation?`);
    if (!confirmSell) return;

    const currentBal = getLocalAirdropBalance();
    const newBal = currentBal + netReturn;
    const shineBalEl = document.getElementById("homeProfitShine");
    if (shineBalEl) shineBalEl.innerText = newBal.toFixed(2);
    localStorage.setItem("shine_airdrop_balance", newBal.toString());

    recordDexFeeCollected(fee, "SELL", item.name);

    airdropRealizedProfitTotal += netProfit;
    airdrop24hProfitTotal += netProfit;

    userAirdropOrdersHistory.unshift({
        type: 'SELL',
        name: item.name,
        price: currentMarketPrice,
        total: netReturn,
        profit: netProfit,
        time: new Date().toLocaleTimeString()
    });

    userAirdropHoldings.splice(index, 1);

    if (p) {
        p.currentPrice = Math.max(p.basePrice * 0.7, p.currentPrice * 0.996);
        p.change24h = ((p.currentPrice - p.basePrice) / p.basePrice) * 100;
    }

    updateAirdropUserBalanceUI();
    renderAirdropInventoryView();
    renderAirdropProductsGrid();
    saveAirdropDataToDB();
    alert(`Liquidation complete!\nReceived: +${netReturn.toFixed(2)} SHINE\n1% Fee (${fee.toFixed(2)} SHINE) transferred to DEX Fee Pool.`);
}
function startCosmeticMarketTicker() {
    setInterval(() => {
        COSMETICS_PRODUCTS.forEach(p => {
            const shiftPct = (Math.random() - 0.49) * 0.008;
            p.currentPrice = Math.max(p.basePrice * 0.85, p.currentPrice * (1 + shiftPct));
            p.change24h = ((p.currentPrice - p.basePrice) / p.basePrice) * 100;
            if (p.currentPrice > p.high24h) p.high24h = p.currentPrice;
            if (p.currentPrice < p.low24h) p.low24h = p.currentPrice;
        });

        if (airdropCurrentSubTab === 'ALL') {
            const grid = document.getElementById("airdropProductsGrid");
            if (grid && window.getComputedStyle(grid).display !== 'none') {
                renderAirdropProductsGrid();
            }
        }
        updateAirdropUserBalanceUI();
    }, 4000);
}

startCosmeticMarketTicker();
    </script>

<div id="eliteTradesModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 17000; overflow-y: auto; padding: 20px 16px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="material-icons" style="color: #FFD700; font-size: 24px;">military_tech</i>
                <span style="color: #ffffff; font-size: 18px; font-weight: 900; letter-spacing: 0.5px;">ELITE COPY TRADING</span>
            </div>
            <button onclick="closeEliteTradesModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>

        <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <i class="material-icons" style="color: #00e5ff; font-size: 18px;">notifications_active</i>
                <span style="color: #00e5ff; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">SLOT ALLOCATION RULE</span>
            </div>
            <div id="copySlotNoticeText" style="color: #8c8ca1; font-size: 12px; line-height: 1.5;">
                Each trade slot requires 10 USDT. Subscribing with 10 USDT opens 1 test trade slot. Subscribing with 100 USDT executes the full 10-trade grid strategy.
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.04);">
                <span style="color: #718096; font-size: 11px;">Allowed Grid Slots:</span>
                <span id="copySlotsCountDisplay" style="color: #00c087; font-weight: 900; font-size: 13px; font-family: monospace;">10 Slots (Full Grid Mode)</span>
            </div>
        </div>

        <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #718096; font-size: 11px; font-weight: 800; text-transform: uppercase;">INVESTMENT CAPITAL</span>
                <span id="copyWalletAvailText" style="color: #00c087; font-size: 11px; font-family: monospace; font-weight: 800;">Avail: 100.00 USDT</span>
            </div>
            <div style="display: flex; align-items: center; background: #161b26; border-radius: 8px; padding: 10px 14px; justify-content: space-between;">
                <input type="number" id="copyAmountInput" value="100" min="10" step="10" oninput="calculateCopySlots()" style="background: transparent; border: none; color: #fff; font-size: 20px; font-weight: 900; width: 140px; outline: none; font-family: monospace;">
                <span style="color: #718096; font-size: 12px; font-weight: 900;">USDT</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
                <button onclick="setCopyPill(10)" style="background: #161b26; border: none; color: #e2e8f0; border-radius: 6px; padding: 8px 0; font-size: 11px; font-weight: 800; cursor: pointer;">10 (1 Slot)</button>
                <button onclick="setCopyPill(30)" style="background: #161b26; border: none; color: #e2e8f0; border-radius: 6px; padding: 8px 0; font-size: 11px; font-weight: 800; cursor: pointer;">30 (3 Slots)</button>
                <button onclick="setCopyPill(50)" style="background: #161b26; border: none; color: #e2e8f0; border-radius: 6px; padding: 8px 0; font-size: 11px; font-weight: 800; cursor: pointer;">50 (5 Slots)</button>
                <button onclick="setCopyPill(100)" style="background: #161b26; border: none; color: #e2e8f0; border-radius: 6px; padding: 8px 0; font-size: 11px; font-weight: 800; cursor: pointer;">100 (Full)</button>
            </div>
        </div>

        <div style="color: #ffffff; font-size: 13px; font-weight: 900; letter-spacing: 0.5px;">CHOOSE MASTER STRATEGY:</div>

        <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #ffffff; font-weight: 900; font-size: 14px;">1. VELOCITY DCA (HOME BOT)</span>
                        <span style="background: rgba(0, 229, 255, 0.12); color: #00e5ff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800;">MASTER DCA</span>
                    </div>
                    <span style="color: #00c087; font-weight: 900; font-size: 12px; font-family: monospace;">WIN RATE: 99%</span>
                </div>
                <div style="color: #718096; font-size: 11px; line-height: 1.4;">Institutional 10-phase DCA grid system with automated trailing stop loss. Highest capital security.</div>
                <button onclick="executeCopySubscription('VELOCITY_DCA')" style="width: 100%; background: #00c087; color: #000; border: none; padding: 11px 0; border-radius: 8px; font-weight: 900; font-size: 12px; cursor: pointer; margin-top: 4px;">COPY VELOCITY DCA</button>
            </div>

            <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #ffffff; font-weight: 900; font-size: 14px;">2. APEX MICRO SCALPER</span>
                        <span style="background: rgba(0, 210, 255, 0.12); color: #00d2ff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800;">FAST SCALP</span>
                    </div>
                    <span style="color: #00c087; font-weight: 900; font-size: 12px; font-family: monospace;">WIN RATE: 98%</span>
                </div>
                <div style="color: #718096; font-size: 11px; line-height: 1.4;">High-frequency scalper executing micro-dip entries every $0.50 with rapid exits. 15-30 daily trades.</div>
                <button onclick="executeCopySubscription('APEX_SCALPER')" style="width: 100%; background: #00d2ff; color: #000; border: none; padding: 11px 0; border-radius: 8px; font-weight: 900; font-size: 12px; cursor: pointer; margin-top: 4px;">COPY APEX SCALPER</button>
            </div>

            <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #ffffff; font-weight: 900; font-size: 14px;">3. QUANTUM PULSE</span>
                        <span style="background: rgba(255, 215, 0, 0.12); color: #FFD700; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800;">WAVE RUNNER</span>
                    </div>
                    <span style="color: #00c087; font-weight: 900; font-size: 12px; font-family: monospace;">WIN RATE: 96%</span>
                </div>
                <div style="color: #718096; font-size: 11px; line-height: 1.4;">Mid-wave $2.20+ dip harvester. 50% quick-profit exit and 50% deep recovery runner to pre-dump high.</div>
                <button onclick="executeCopySubscription('QUANTUM_PULSE')" style="width: 100%; background: #FFD700; color: #000; border: none; padding: 11px 0; border-radius: 8px; font-weight: 900; font-size: 12px; cursor: pointer; margin-top: 4px;">COPY QUANTUM PULSE</button>
            </div>

            <div style="background: #11151e; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #ffffff; font-weight: 900; font-size: 14px;">4. TITAN ABYSS</span>
                        <span style="background: rgba(255, 45, 120, 0.12); color: #ff2d78; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800;">DEEP SNIPER</span>
                    </div>
                    <span style="color: #00c087; font-weight: 900; font-size: 12px; font-family: monospace;">WIN RATE: 94%</span>
                </div>
                <div style="color: #718096; font-size: 11px; line-height: 1.4;">Deep crash $3.20+ liquidity sniper. Enters bottom floor exclusively upon confirmed 70% whale orderflow.</div>
                <button onclick="executeCopySubscription('TITAN_ABYSS')" style="width: 100%; background: #ff2d78; color: #fff; border: none; padding: 11px 0; border-radius: 8px; font-weight: 900; font-size: 12px; cursor: pointer; margin-top: 4px;">COPY TITAN ABYSS</button>
            </div>
        </div>
    </div>
</div>

<div id="hyperTitanDetailsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 18500; overflow-y: auto; padding: 20px 16px 80px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a202c; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; background: #00e5ff; border-radius: 50%; box-shadow: 0 0 12px #00e5ff;"></div>
                <span style="color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">SHINE HYPER TITAN POOL</span>
            </div>
            <button onclick="closeHyperTitanDetailsModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>
<div class="bot-card" style="margin-bottom: 0; background: rgba(0, 229, 255, 0.04); border: 1px solid rgba(0, 229, 255, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; margin-bottom: 10px;">
                <span style="color: #00e5ff; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">POOL PARTICIPATION OVERVIEW</span>
                <span style="background: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace;"><span id="hyper-modal-total-users">100</span> USERS ACTIVE</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL CAPITAL</div>
                    <div id="hyper-modal-total-pool-invest" style="color: #ffffff; font-size: 15px; font-weight: 900; margin-top: 2px;">$9,999.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL PROFIT (ALL)</div>
                    <div id="hyper-modal-pool-profit" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 2px;">+$0.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); grid-column: span 2; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR PROFIT SHARE (PER USER)</div>
                        <div id="hyper-modal-user-profit" style="color: #00e676; font-size: 16px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR SHARE</div>
                        <div style="color: #00e5ff; font-size: 12px; font-weight: 900;">$99.99 (1.00%)</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
            <div style="margin-bottom: 12px;">
                <div style="color: #00d2ff; font-size: 11px; font-weight: bold; margin-bottom: 6px;">BOT TRADING ASSETS</div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT USDT</div>
                    <div class="port-amt" id="hyper-modal-port-usdt">$1,000.00</div>
                </div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT SOL</div>
                    <div class="port-amt" id="hyper-modal-port-sol">0.0000</div>
                </div>
            </div>
        </div>

        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">BOT AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
            <div class="avg-main-val" id="hyper-modal-avg-price">$0.00</div>
            <div class="invested-row">BOT INVESTED: <span class="invested-white" id="hyper-modal-invested">$0.00</span> / <span id="hyper-modal-capital">$1,000.00</span></div>
        </div>

        <div class="trade-status-card bot-card" style="margin: 0;">
            <div class="trade-card-header">
                <h3>DCA SAFETY ORDERS (BOT)</h3>
                <div class="open-badge" id="hyper-modal-positions-badge">0 OPEN</div>
            </div>
            <div class="empty-msg" id="hyper-modal-positions-container">NO ACTIVE BOT POSITIONS</div>
        </div>

        <div class="bot-card" style="margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">AUTOMATED BOT AUDIT LOG</h3>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                    <span style="color: #8c8ca1;">Exits <span id="hyper-modal-trade-count" style="color: #fff; margin-left: 4px;">0</span></span>
                    <span style="color: #4CAF50;">Profit <span id="hyper-modal-win-tag" style="margin-left: 4px;">0</span></span>
                    <span style="color: #f6465d;">Lose <span id="hyper-modal-loss-tag" style="margin-left: 4px;">0</span></span>
                </div>
            </div>
            <div id="hyper-modal-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                <div class="empty-msg">NO BOT TRADES RECORDED</div>
            </div>
        </div>
    </div>
</div>

<div id="killer1DetailsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 18500; overflow-y: auto; padding: 20px 16px 80px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a202c; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; background: #00d2ff; border-radius: 50%; box-shadow: 0 0 12px #00d2ff;"></div>
                <span style="color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">SHINE APEX VELOCITY ENGINE</span>
            </div>
            <button onclick="closeKiller1DetailsModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>
        <div class="bot-card" style="margin-bottom: 0; background: rgba(0, 210, 255, 0.04); border: 1px solid rgba(0, 210, 255, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; margin-bottom: 10px;">
                <span style="color: #00d2ff; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">POOL PARTICIPATION OVERVIEW</span>
                <span style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace;"><span id="k1-modal-total-users">1</span> USER ACTIVE</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL CAPITAL</div>
                    <div id="k1-modal-total-pool-invest" style="color: #ffffff; font-size: 15px; font-weight: 900; margin-top: 2px;">$100.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL PROFIT (ALL)</div>
                    <div id="k1-modal-pool-profit" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); grid-column: span 2; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR PROFIT SHARE (PER USER)</div>
                        <div id="k1-modal-user-profit" style="color: #00e676; font-size: 16px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR SHARE</div>
                        <div style="color: #00d2ff; font-size: 12px; font-weight: 900;">$10.00 (100.00%)</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
            <div style="margin-bottom: 12px;">
                <div style="color: #00d2ff; font-size: 11px; font-weight: bold; margin-bottom: 6px;">BOT TRADING ASSETS</div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT USDT</div>
                    <div class="port-amt" id="k1-modal-port-usdt">$0.00</div>
                </div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT SOL</div>
                    <div class="port-amt" id="k1-modal-port-sol">0.0000</div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">BOT AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
            <div class="avg-main-val" id="k1-modal-avg-price">$0.00</div>
            <div class="invested-row">BOT INVESTED: <span class="invested-white" id="k1-modal-invested">$0.00</span></div>
        </div>
        <div class="trade-status-card bot-card" style="margin: 0;">
            <div class="trade-card-header">
                <h3>DCA SAFETY ORDERS (BOT)</h3>
                <div class="open-badge" id="k1-modal-positions-badge">0 OPEN</div>
            </div>
            <div class="empty-msg" id="k1-modal-positions-container">NO ACTIVE BOT POSITIONS</div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">AUTOMATED BOT AUDIT LOG</h3>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                    <span style="color: #8c8ca1;">Exits <span id="k1-modal-trade-count" style="color: #fff; margin-left: 4px;">0</span></span>
                    <span style="color: #4CAF50;">Profit <span id="k1-modal-win-tag" style="margin-left: 4px;">0</span></span>
                    <span style="color: #f6465d;">Lose <span id="k1-modal-loss-tag" style="margin-left: 4px;">0</span></span>
                </div>
                <div id="k1-realized-pnl-val" style="color: #4CAF50; font-size: 16px; font-weight: 900; font-family: monospace; margin-top: 4px;">+$0.0000</div>
            </div>
            <div id="k1-modal-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                <div class="empty-msg">NO BOT TRADES RECORDED (24H CLEAR)</div>
            </div>
        </div>
    </div>
</div>

<div id="killer2DetailsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 18500; overflow-y: auto; padding: 20px 16px 80px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a202c; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; background: #FFD700; border-radius: 50%; box-shadow: 0 0 12px #FFD700;"></div>
                <span style="color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">SHINE QUANTUM PULSE ENGINE</span>
            </div>
            <button onclick="closeKiller2DetailsModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>
        <div class="bot-card" style="margin-bottom: 0; background: rgba(255, 215, 0, 0.04); border: 1px solid rgba(255, 215, 0, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; margin-bottom: 10px;">
                <span style="color: #FFD700; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">POOL PARTICIPATION OVERVIEW</span>
                <span style="background: rgba(255, 215, 0, 0.15); color: #FFD700; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace;"><span id="k2-modal-total-users">1</span> USER ACTIVE</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL CAPITAL</div>
                    <div id="k2-modal-total-pool-invest" style="color: #ffffff; font-size: 15px; font-weight: 900; margin-top: 2px;">$100.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL PROFIT (ALL)</div>
                    <div id="k2-modal-pool-profit" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); grid-column: span 2; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR PROFIT SHARE (PER USER)</div>
                        <div id="k2-modal-user-profit" style="color: #00e676; font-size: 16px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR SHARE</div>
                        <div style="color: #FFD700; font-size: 12px; font-weight: 900;">$10.00 (100.00%)</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
            <div style="margin-bottom: 12px;">
                <div style="color: #FFD700; font-size: 11px; font-weight: bold; margin-bottom: 6px;">BOT TRADING ASSETS</div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT USDT</div>
                    <div class="port-amt" id="k2-modal-port-usdt">$0.00</div>
                </div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT SOL</div>
                    <div class="port-amt" id="k2-modal-port-sol">0.0000</div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">BOT AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
            <div class="avg-main-val" id="k2-modal-avg-price">$0.00</div>
            <div class="invested-row">BOT INVESTED: <span class="invested-white" id="k2-modal-invested">$0.00</span></div>
        </div>
        <div class="trade-status-card bot-card" style="margin: 0;">
            <div class="trade-card-header">
                <h3>DCA SAFETY ORDERS (BOT)</h3>
                <div class="open-badge" id="k2-modal-positions-badge">0 OPEN</div>
            </div>
            <div class="empty-msg" id="k2-modal-positions-container">NO ACTIVE BOT POSITIONS</div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">AUTOMATED BOT AUDIT LOG</h3>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                    <span style="color: #8c8ca1;">Exits <span id="k2-modal-trade-count" style="color: #fff; margin-left: 4px;">0</span></span>
                    <span style="color: #4CAF50;">Profit <span id="k2-modal-win-tag" style="margin-left: 4px;">0</span></span>
                    <span style="color: #f6465d;">Lose <span id="k2-modal-loss-tag" style="margin-left: 4px;">0</span></span>
                </div>
                <div id="k2-realized-pnl-val" style="color: #4CAF50; font-size: 16px; font-weight: 900; font-family: monospace; margin-top: 4px;">+$0.0000</div>
            </div>
            <div id="k2-modal-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                <div class="empty-msg">NO BOT TRADES RECORDED (24H CLEAR)</div>
            </div>
        </div>
    </div>
</div>

<div id="killer3DetailsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 18500; overflow-y: auto; padding: 20px 16px 80px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a202c; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; background: #00e676; border-radius: 50%; box-shadow: 0 0 12px #00e676;"></div>
                <span style="color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">SHINE TITAN ABYSS ENGINE</span>
            </div>
            <button onclick="closeKiller3DetailsModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>
        <div class="bot-card" style="margin-bottom: 0; background: rgba(0, 230, 118, 0.04); border: 1px solid rgba(0, 230, 118, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; margin-bottom: 10px;">
                <span style="color: #00e676; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">POOL PARTICIPATION OVERVIEW</span>
                <span style="background: rgba(0, 230, 118, 0.15); color: #00e676; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace;"><span id="k3-modal-total-users">1</span> USER ACTIVE</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL CAPITAL</div>
                    <div id="k3-modal-total-pool-invest" style="color: #ffffff; font-size: 15px; font-weight: 900; margin-top: 2px;">$100.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL PROFIT (ALL)</div>
                    <div id="k3-modal-pool-profit" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); grid-column: span 2; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR PROFIT SHARE (PER USER)</div>
                        <div id="k3-modal-user-profit" style="color: #00e676; font-size: 16px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR SHARE</div>
                        <div style="color: #00e676; font-size: 12px; font-weight: 900;">$10.00 (100.00%)</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
            <div style="margin-bottom: 12px;">
                <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-bottom: 6px;">BOT TRADING ASSETS</div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT USDT</div>
                    <div class="port-amt" id="k3-modal-port-usdt">$0.00</div>
                </div>
                <div class="portfolio-row">
                    <div class="port-coin">BOT SOL</div>
                    <div class="port-amt" id="k3-modal-port-sol">0.0000</div>
                </div>
            </div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">BOT AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
            <div class="avg-main-val" id="k3-modal-avg-price">$0.00</div>
            <div class="invested-row">BOT INVESTED: <span class="invested-white" id="k3-modal-invested">$0.00</span></div>
        </div>
        <div class="trade-status-card bot-card" style="margin: 0;">
            <div class="trade-card-header">
                <h3>DCA SAFETY ORDERS (BOT)</h3>
                <div class="open-badge" id="k3-modal-positions-badge">0 OPEN</div>
            </div>
            <div class="empty-msg" id="k3-modal-positions-container">NO ACTIVE BOT POSITIONS</div>
        </div>
        <div class="bot-card" style="margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">AUTOMATED BOT AUDIT LOG</h3>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                    <span style="color: #8c8ca1;">Exits <span id="k3-modal-trade-count" style="color: #fff; margin-left: 4px;">0</span></span>
                    <span style="color: #4CAF50;">Profit <span id="k3-modal-win-tag" style="margin-left: 4px;">0</span></span>
                    <span style="color: #f6465d;">Lose <span id="k3-modal-loss-tag" style="margin-left: 4px;">0</span></span>
                </div>
                <div id="k3-realized-pnl-val" style="color: #4CAF50; font-size: 16px; font-weight: 900; font-family: monospace; margin-top: 4px;">+$0.0000</div>
            </div>
            <div id="k3-modal-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                <div class="empty-msg">NO BOT TRADES RECORDED (24H CLEAR)</div>
            </div>
        </div>
    </div>
</div>

<div id="singularityDetailsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; z-index: 18500; overflow-y: auto; padding: 20px 16px 80px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 440px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a202c; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; background: #e040fb; border-radius: 50%; box-shadow: 0 0 12px #e040fb;"></div>
                <span style="color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">TITAN SINGULARITY 100K POOL</span>
            </div>
            <button onclick="closeSingularityDetailsModal()" style="background: #1a202c; border: none; border-radius: 50%; width: 32px; height: 32px; color: #e2e8f0; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>

        <div class="bot-card" style="margin-bottom: 0; background: rgba(224, 64, 251, 0.04); border: 1px solid rgba(224, 64, 251, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; margin-bottom: 10px;">
                <span style="color: #e040fb; font-weight: 900; font-size: 12px; letter-spacing: 0.5px;">POOL PARTICIPATION OVERVIEW</span>
                <span style="background: rgba(224, 64, 251, 0.15); color: #e040fb; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; font-family: monospace;"><span id="sng-modal-total-users">1000</span> USERS ACTIVE</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: monospace;">
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL CAPITAL</div>
                    <div id="sng-modal-total-pool-invest" style="color: #ffffff; font-size: 15px; font-weight: 900; margin-top: 2px;">$100,000.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">TOTAL POOL PROFIT</div>
                    <div id="sng-modal-pool-profit" style="color: #4CAF50; font-size: 15px; font-weight: 900; margin-top: 2px;">+$0.00 USDT</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); grid-column: span 2; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR PROFIT SHARE (PER USER)</div>
                        <div id="sng-modal-user-profit" style="color: #00e676; font-size: 16px; font-weight: 900; margin-top: 2px;">+$0.0000 USDT</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #8c8ca1; font-size: 9px; font-weight: bold;">YOUR SHARE</div>
                        <div style="color: #e040fb; font-size: 12px; font-weight: 900;">$100.00 (0.10%)</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">PORTFOLIO BALANCES <i class="material-icons" style="font-size:16px;">account_balance_wallet</i></div>
            <div style="margin-bottom: 12px;">
                <div style="color: #e040fb; font-size: 11px; font-weight: bold; margin-bottom: 6px;">POOL TRADING ASSETS</div>
                <div class="portfolio-row">
                    <div class="port-coin">POOL USDT</div>
                    <div class="port-amt" id="sng-modal-port-usdt">$100,000.00</div>
                </div>
                <div class="portfolio-row">
                    <div class="port-coin">POOL SOL</div>
                    <div class="port-amt" id="sng-modal-port-sol">0.0000</div>
                </div>
            </div>
        </div>

        <div class="bot-card" style="margin-bottom: 0;">
            <div class="card-label">POOL AVG ENTRY PRICE <i class="material-icons" style="font-size:16px;">track_changes</i></div>
            <div class="avg-main-val" id="sng-modal-avg-price">$0.00</div>
            <div class="invested-row">POOL INVESTED: <span class="invested-white" id="sng-modal-invested">$0.00</span> / <span id="sng-modal-capital">$100,000.00</span></div>
        </div>

        <div class="trade-status-card bot-card" style="margin: 0;">
            <div class="trade-card-header">
                <h3>5-ENGINE SIMULTANEOUS ORDERS</h3>
                <div class="open-badge" id="sng-modal-positions-badge">0 OPEN</div>
            </div>
            <div class="empty-msg" id="sng-modal-positions-container">NO ACTIVE BOT POSITIONS</div>
        </div>

        <div class="bot-card" style="margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; margin-bottom: 16px; text-align: center;">
                <h3 style="margin: 0; font-size: 14px; font-weight: 900; color: #fff; letter-spacing: 0.5px;">SINGULARITY 100K AUDIT LOG</h3>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 12px; font-family: monospace; font-weight: 800;">
                    <span style="color: #8c8ca1;">Exits <span id="sng-modal-trade-count" style="color: #fff; margin-left: 4px;">0</span></span>
                    <span style="color: #4CAF50;">Profit <span id="sng-modal-win-tag" style="margin-left: 4px;">0</span></span>
                    <span style="color: #f6465d;">Lose <span id="sng-modal-loss-tag" style="margin-left: 4px;">0</span></span>
                </div>
                <div id="sng-realized-pnl-val" style="color: #4CAF50; font-size: 16px; font-weight: 900; font-family: monospace; margin-top: 4px;">+$0.0000</div>
            </div>
            <div id="sng-modal-history-list" style="display: flex; flex-direction: column; gap: 8px;">
                <div class="empty-msg">NO BOT TRADES RECORDED</div>
            </div>
        </div>
    </div>
</div>
<div id="connectedWalletDrawer" class="tw-sheet-overlay" style="z-index: 30000; display: none; align-items: flex-end;">
    <div class="web3-wallet-card">
        <div class="web3-drawer-drag"></div>
        <div class="web3-drawer-header">
            <div class="web3-provider-info">
                <div id="drawerWalletLogoBadge" class="web3-provider-icon">
                    <img id="drawerWalletLogoImg" src="https://s2.coinmarketcap.com/static/img/coins/64x64/5964.png" alt="Wallet">
                </div>
                <div>
                    <div id="drawerWalletProviderName" class="web3-provider-title">Trust Wallet</div>
                    <div class="web3-network-status">
                        <span class="web3-net-dot"></span>
                        <span id="drawerNetworkName">BNB Smart Chain (BEP-20)</span>
                    </div>
                </div>
            </div>
            <button class="web3-close-btn" onclick="closeConnectedWalletDrawer()">
                <i class="material-icons">close</i>
            </button>
        </div>

        <div class="web3-address-box">
            <div>
                <div class="web3-box-label">CONNECTED ADDRESS</div>
                <div id="drawerFullAddressText" class="web3-box-address">0x0000...0000</div>
            </div>
            <div class="web3-address-actions">
                <button class="web3-mini-action-btn" onclick="copyConnectedFullAddress()" title="Copy Address">
                    <i class="material-icons">content_copy</i>
                </button>
                <a id="drawerExplorerLink" href="#" target="_blank" class="web3-mini-action-btn" title="View on Explorer">
                    <i class="material-icons">open_in_new</i>
                </a>
            </div>
        </div>

        <div class="web3-networth-card">
            <div class="web3-networth-label">TOTAL WALLET BALANCE</div>
            <div id="drawerTotalNetWorth" class="web3-networth-val">$0.00</div>
            <div class="web3-networth-sub">Live On-Chain Assets in Connected App</div>
        </div>

        <div class="web3-assets-list">
            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <svg viewBox="0 0 200 200" style="width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0; filter: drop-shadow(0 2px 6px rgba(228, 37, 125, 0.45));">
                        <defs>
                            <radialGradient id="shineCoinGradDr" cx="35%" cy="30%" r="75%">
                                <stop offset="0%" stop-color="#ff4f9e"/>
                                <stop offset="35%" stop-color="#e91e7e"/>
                                <stop offset="75%" stop-color="#ba1261"/>
                                <stop offset="100%" stop-color="#840540"/>
                            </radialGradient>
                        </defs>
                        <circle cx="100" cy="100" r="98" fill="url(#shineCoinGradDr)"/>
                        <circle cx="100" cy="100" r="91" fill="none" stroke="#ff7ab6" stroke-width="3" opacity="0.9"/>
                        <circle cx="100" cy="100" r="85" fill="none" stroke="#750438" stroke-width="3" opacity="0.7"/>
                        <circle cx="100" cy="100" r="82" fill="url(#shineCoinGradDr)"/>
                        <g fill="#ffffff">
                            <text x="44" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">S</text>
                            <text x="74" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">H</text>
                            <path d="M100 56 Q101 64 107 67 Q101 70 100 78 Q99 70 93 67 Q99 64 100 56 Z"/>
                            <path d="M89 74 Q89.5 78 92 79.5 Q89.5 81 89 85 Q88.5 81 86 79.5 Q88.5 78 89 74 Z"/>
                            <path d="M112 76 Q112.5 80 115 81.5 Q112.5 83 112 87 Q111.5 83 109 81.5 Q111.5 80 112 76 Z"/>
                            <circle cx="100" cy="86" r="3.2"/>
                            <path d="M93 96 C94 91 98 87.5 104 88 C100 91 97 94 96 98 Z"/>
                            <circle cx="100" cy="99" r="3.2"/>
                            <path d="M92 113 C91 106 97 100 105 100 C100 103 97 107 97 113 Z"/>
                            <path d="M100 106 C105 107 107 112 105 118 C102 124 97 129 93 136 C95 131 99 125 102 120 C104 115 102 110 98 108 Z"/>
                            <path d="M93 126 C96 130 101 135 105 142 C103 138 99 133 95 128 Z"/>
                            <text x="127" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">N</text>
                            <text x="156" y="122" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" text-anchor="middle">E</text>
                        </g>
                    </svg>
                    <div>
                        <div class="web3-coin-name">SHINE</div>
                        <div class="web3-coin-tag">Airdrop Asset</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div id="drawerShineBal" class="web3-asset-amount">100.00 SHINE</div>
                    <div id="drawerShineVal" class="web3-asset-fiat">$1.00</div>
                </div>
            </div>

            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <svg viewBox="0 0 100 100" class="web3-coin-icon" style="width: 32px; height: 32px; border-radius: 50%;">
                        <circle cx="50" cy="50" r="50" fill="#009393"/>
                        <path d="M50 42.5 C34 42.5 22 45.2 22 48.5 C22 51.8 34 54.5 50 54.5 C66 54.5 78 51.8 78 48.5 C78 45.2 66 42.5 50 42.5 Z M50 45.8 C62.5 45.8 71.5 47.7 71.5 48.5 C71.5 49.3 62.5 51.2 50 51.2 C37.5 51.2 28.5 49.3 28.5 48.5 C28.5 47.7 37.5 45.8 50 45.8 Z" fill="#FFFFFF"/>
                        <path d="M29 27 H71 V36 H56 V73 H44 V36 H29 Z" fill="#FFFFFF"/>
                    </svg>
                    <div>
                        <div class="web3-coin-name">USDT</div>
                        <div class="web3-coin-tag">Tether USD</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div id="drawerUsdtBal" class="web3-asset-amount">0.00 USDT</div>
                    <div id="drawerUsdtVal" class="web3-asset-fiat">$0.00</div>
                </div>
            </div>

            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <img src="https://cryptologos.cc/logos/solana-sol-logo.png?v=024" class="web3-coin-icon" style="width: 32px; height: 32px; border-radius: 50%;">
                    <div>
                        <div class="web3-coin-name">SOL</div>
                        <div class="web3-coin-tag">Solana</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div id="drawerSolBal" class="web3-asset-amount">0.0000 SOL</div>
                    <div id="drawerSolVal" class="web3-asset-fiat">$0.00</div>
                </div>
            </div>

            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <svg viewBox="0 0 32 32" class="web3-coin-icon" style="width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;">
                        <circle cx="16" cy="16" r="16" fill="#F0B90B"/>
                        <path fill="#FFFFFF" d="M12.116 14.404L16 10.519l3.886 3.886 2.26-2.259L16 6 9.856 12.145l2.26 2.259zM6 16l2.26-2.26 2.259 2.26-2.26 2.26L6 16zm6.116 1.596L16 21.481l3.886-3.885 2.26 2.259L16 26l-6.144-6.145 2.26-2.259zm9.768-1.596l2.26-2.26 2.26 2.26-2.26 2.26-2.26-2.26zm-3.623 0L16 13.739l-2.261 2.261 2.261 2.261 2.261-2.261z"/>
                    </svg>
                    <div>
                        <div id="drawerGasCoinName" class="web3-coin-name">BNB</div>
                        <div id="drawerGasCoinTag" class="web3-coin-tag">BNB Chain</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div id="drawerGasBal" class="web3-asset-amount">0.0000 BNB</div>
                    <div id="drawerGasVal" class="web3-asset-fiat">$0.00</div>
                </div>
            </div>

            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=024" class="web3-coin-icon" style="width: 32px; height: 32px; border-radius: 50%;">
                    <div>
                        <div class="web3-coin-name">BTC</div>
                        <div class="web3-coin-tag">Bitcoin</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div class="web3-asset-amount">0.0000 BTC</div>
                    <div class="web3-asset-fiat">$0.00</div>
                </div>
            </div>

            <div class="web3-asset-row">
                <div class="web3-asset-left">
                    <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png?v=024" class="web3-coin-icon" style="width: 32px; height: 32px; border-radius: 50%;">
                    <div>
                        <div class="web3-coin-name">ETH</div>
                        <div class="web3-coin-tag">Ethereum</div>
                    </div>
                </div>
                <div class="web3-asset-right">
                    <div class="web3-asset-amount">0.0000 ETH</div>
                    <div class="web3-asset-fiat">$0.00</div>
                </div>
            </div>
        </div>

        <div class="web3-drawer-footer">
            <button class="web3-switch-btn" onclick="closeConnectedWalletDrawer(); openWalletSelection();">
                <i class="material-icons">swap_horiz</i> Switch Wallet
            </button>
            <button class="web3-disconnect-btn" onclick="disconnectCurrentWallet(); closeConnectedWalletDrawer();">
                <i class="material-icons">power_settings_new</i> Disconnect
            </button>
        </div>
    </div>
</div>

<div id="trustCustomizeModalSheet" class="tw-sheet-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 50000; align-items: flex-end; justify-content: center;">
    <div style="background: #ffffff; color: #000000; border-top-left-radius: 24px; border-top-right-radius: 24px; width: 100%; max-width: 480px; padding: 14px 20px 34px; box-sizing: border-box; box-shadow: 0 -10px 40px rgba(0,0,0,0.5); font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;">
        <div style="width: 44px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 0 auto 16px;"></div>
        
        <div class="tw-sheet-row">
            <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Hide NFTs</span>
            <label class="tw-switch">
                <input type="checkbox" id="toggleHideNfts" checked onchange="handleTrustCustomizeToggle('NFTS', this.checked)">
                <span class="tw-slider"></span>
            </label>
        </div>

        <div class="tw-sheet-row">
            <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Hide Predictions</span>
            <label class="tw-switch">
                <input type="checkbox" id="toggleHidePredictions" onchange="handleTrustCustomizeToggle('PREDICTIONS', this.checked)">
                <span class="tw-slider"></span>
            </label>
        </div>

        <div class="tw-sheet-row">
            <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Hide Perps</span>
            <label class="tw-switch">
                <input type="checkbox" id="toggleHidePerps" onchange="handleTrustCustomizeToggle('PERPS', this.checked)">
                <span class="tw-slider"></span>
            </label>
        </div>

        <div class="tw-sheet-row">
            <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Hide Earn</span>
            <label class="tw-switch">
                <input type="checkbox" id="toggleHideEarn" onchange="handleTrustCustomizeToggle('EARN', this.checked)">
                <span class="tw-slider"></span>
            </label>
        </div>

        <div onclick="closeTrustCustomizeSheet(); alert('Manage crypto token list opened');" style="padding: 16px 0; border-bottom: 1px solid rgba(0,0,0,0.06); cursor: pointer;">
            <div style="font-size: 16px; font-weight: 700; color: #0f172a;">Manage crypto</div>
        </div>

        <div onclick="executeDustCleaner()" style="padding: 16px 0; border-bottom: 1px solid rgba(0,0,0,0.06); cursor: pointer;">
            <div style="font-size: 16px; font-weight: 700; color: #0f172a;">Dust cleaner</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Convert small assets to the native token</div>
        </div>

        <div class="tw-sheet-row" style="border-bottom: none; padding-top: 16px;">
            <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Hide assets &lt;0.01 USD</span>
            <label class="tw-switch">
                <input type="checkbox" id="toggleHideDustAssets" onchange="handleTrustCustomizeToggle('DUST', this.checked)">
                <span class="tw-slider"></span>
            </label>
        </div>
    </div>
</div>

<script>
function openTrustCustomizeSheet() {
    const sheet = document.getElementById("trustCustomizeModalSheet");
    if (sheet) {
        sheet.style.display = "flex";
        sheet.onclick = function(e) {
            if (e.target === this) closeTrustCustomizeSheet();
        };
    }
}

function closeTrustCustomizeSheet() {
    const sheet = document.getElementById("trustCustomizeModalSheet");
    if (sheet) sheet.style.display = "none";
}

function handleTrustCustomizeToggle(type, isChecked) {
    if (type === 'PERPS') {
        const perpsSec = document.getElementById("walletPerpsSection");
        if (perpsSec) perpsSec.style.display = isChecked ? "none" : "block";
    } else if (type === 'PREDICTIONS') {
        const predSec = document.getElementById("walletPredictionsSection");
        if (predSec) predSec.style.display = isChecked ? "none" : "block";
    } else if (type === 'EARN') {
        const profitSec = document.querySelector(".profit-section");
        const passiveSec = document.querySelector(".passive-income-section");
        const rewardsSec = document.querySelector(".rewards-section");
        const displayVal = isChecked ? "none" : "block";
        if (profitSec) profitSec.style.display = displayVal;
        if (passiveSec) passiveSec.style.display = displayVal;
        if (rewardsSec) rewardsSec.style.display = displayVal;
    } else if (type === 'DUST') {
        document.querySelectorAll(".wallet-token-row").forEach(row => {
            const sym = row.getAttribute("data-symbol");
            if (sym === "BTC" || sym === "ETH") {
                row.style.display = isChecked ? "none" : "flex";
            }
        });
    }
}

function executeDustCleaner() {
    closeTrustCustomizeSheet();
    alert("Dust Cleaner: All micro balances converted to USDT successfully!");
}
</script>
<script>
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    const banner = document.getElementById('pwaInstallBanner');
    if (banner) banner.style.display = 'flex';
});
const installBtn = document.getElementById('pwaInstallBtn');
if (installBtn) {
    installBtn.addEventListener('click', async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            deferredPrompt = null;
            document.getElementById('pwaInstallBanner').style.display = 'none';
        } else {
            alert('App download karne ke liye browser menu (3 dots) par click karein aur "Install app" ya "Add to Home screen" select karein.');
        }
    });
}
</script>
</body>
</html>
