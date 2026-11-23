
import streamlit as st
import streamlit.components.v1 as components
import json


# -----------------------------------------
# 1. 게임에 사용할 리스트
# -----------------------------------------

coolant_list = [
    "물-에틸렌글리콜",
    "절연 냉각유",
    "액체 질소"
]

track_sectors = [
    "Sector 1",
    "Sector 2",
    "Sector 3"
]


# -----------------------------------------
# 2. 냉각 성능을 계산하는 함수
# -----------------------------------------

def simulate_race(coolant, flow_rate, battery_output):

    # if-elif-else: 냉각수 종류에 따라 냉각 효율 결정
    if coolant == "물-에틸렌글리콜":
        cooling_efficiency = 1.0

    elif coolant == "절연 냉각유":
        cooling_efficiency = 0.9

    elif coolant == "액체 질소":
        cooling_efficiency = 1.2

    else:
        cooling_efficiency = 0.0

    # 배터리 출력과 유량을 이용한 초기 온도 계산
    temperature = (
        38
        + (battery_output - 50) * 0.22
        - (flow_rate - 1) * 0.75 * cooling_efficiency
    )

    # if-elif-else: 배터리 온도 상태 판정
    if temperature > 80:
        result = "과열"

    elif temperature >= 40:
        result = "최적"

    else:
        result = "과냉각"

    return temperature, result, cooling_efficiency


# -----------------------------------------
# 3. 페이지 기본 설정
# -----------------------------------------

st.set_page_config(
    page_title="THERMAL RUSH",
    page_icon="🏎️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d1b, #101b32);
    color: white;
}
h1, h2, h3 {
    color: #55d9ff;
}
div[data-testid="stMetric"] {
    background: #15243d;
    border: 1px solid #245174;
    padding: 14px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# 4. 게임 제목 및 설명
# -----------------------------------------

st.title("🏎️ THERMAL RUSH")
st.subheader("F1 HYPERCAR BATTERY COOLING RACE")

st.write(
    "배터리 냉각 시스템을 설정하고 레이싱에 도전하세요. "
    "속도와 배터리 온도를 함께 관리해야 합니다."
)


# -----------------------------------------
# 5. 게임 설정
# -----------------------------------------

st.markdown("### ⚙️ 배터리 냉각 시스템 설정")

col1, col2, col3 = st.columns(3)

with col1:
    coolant = st.selectbox(
        "냉각수 종류",
        coolant_list
    )

with col2:
    flow_rate = st.slider(
        "냉각수 유량 (L/min)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

with col3:
    battery_output = st.slider(
        "배터리 출력 (%)",
        min_value=50,
        max_value=100,
        value=75,
        step=5
    )


# -----------------------------------------
# 6. 냉각 시스템 계산
# -----------------------------------------

initial_temperature, initial_result, cooling_efficiency = (
    simulate_race(coolant, flow_rate, battery_output)
)

st.markdown("### 📊 현재 냉각 시스템")

metric1, metric2, metric3 = st.columns(3)

metric1.metric("선택한 냉각수", coolant)
metric2.metric("예상 초기 온도", f"{initial_temperature:.1f} ℃")
metric3.metric("초기 상태", initial_result)


# -----------------------------------------
# 7. for 반복문으로 섹터 데이터 생성
# -----------------------------------------

sector_data = []

# for 반복문: track_sectors의 각 구간을 순서대로 처리
for sector_number, sector_name in enumerate(track_sectors):

    sector_data.append({
        "number": sector_number + 1,
        "name": sector_name
    })


# -----------------------------------------
# 8. JavaScript 게임에 전달할 데이터
# -----------------------------------------

game_config = {
    "coolant": coolant,
    "flow_rate": flow_rate,
    "battery_output": battery_output,
    "initial_temperature": initial_temperature,
    "cooling_efficiency": cooling_efficiency,
    "track_sectors": sector_data
}


# -----------------------------------------
# 9. 레이싱 게임 화면
# -----------------------------------------

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 12px;
    background: #080d1b;
    color: white;
    font-family: Arial, sans-serif;
}

.game_panel {
    max-width: 1100px;
    margin: auto;
    background: #101b32;
    border: 1px solid #245174;
    border-radius: 16px;
    padding: 15px;
}

.game_title {
    color: #55d9ff;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 12px;
}

.hud {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}

.hud_item {
    background: #172944;
    border: 1px solid #294d70;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
}

.hud_label {
    font-size: 12px;
    color: #a8c3dc;
}

.hud_value {
    font-size: 21px;
    font-weight: bold;
    color: #55d9ff;
    margin-top: 5px;
}

canvas {
    width: 100%;
    display: block;
    background: #142b28;
    border: 2px solid #55d9ff;
    border-radius: 10px;
    outline: none;
}

.controls {
    margin-top: 12px;
    padding: 12px;
    background: #172944;
    border-radius: 8px;
    color: #c9d9e9;
    line-height: 1.8;
    font-size: 13px;
}

button {
    background: #00bde8;
    color: #06111f;
    border: none;
    border-radius: 8px;
    padding: 12px 25px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 12px;
}

button:hover {
    background: #75e7ff;
}

.overlay {
    position: absolute;
    inset: 0;
    background: rgba(4, 10, 22, 0.88);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 10px;
    padding: 20px;
}

.game_area {
    position: relative;
}

.overlay h2 {
    color: #55d9ff;
    font-size: 30px;
}

.overlay p {
    line-height: 1.8;
    color: #d7e7f5;
}

.result_box {
    margin-top: 12px;
    padding: 14px;
    background: #172944;
    border: 1px solid #245174;
    border-radius: 10px;
    line-height: 1.8;
}

.sector_row {
    border-bottom: 1px solid #294d70;
    padding: 5px;
}
</style>
</head>

<body>

<div class="game_panel">

    <div class="game_title">THERMAL RUSH // RACING SYSTEM</div>

    <div class="hud">
        <div class="hud_item">
            <div class="hud_label">SPEED</div>
            <div class="hud_value" id="speed_value">0</div>
        </div>

        <div class="hud_item">
            <div class="hud_label">BATTERY TEMP</div>
            <div class="hud_value" id="temp_value">0℃</div>
        </div>

        <div class="hud_item">
            <div class="hud_label">RACE TIME</div>
            <div class="hud_value" id="time_value">0.0s</div>
        </div>

        <div class="hud_item">
            <div class="hud_label">SECTOR</div>
            <div class="hud_value" id="sector_value">1 / 3</div>
        </div>
    </div>

    <div class="game_area">

        <canvas id="race_canvas" width="1000" height="650"
                tabindex="0"></canvas>

        <div class="overlay" id="start_overlay">
            <h2>THERMAL RUSH</h2>
            <p>
                배터리 냉각 시스템을 관리하며 결승선을 통과하세요.<br>
                W 또는 ↑ 키를 눌러 가속할 수 있습니다.
            </p>
            <button id="start_button">START RACE</button>
        </div>

    </div>

    <div class="controls">
        <b>KEYBOARD CONTROL</b><br>
        W / ↑ : 가속 &nbsp;&nbsp; S / ↓ : 감속<br>
        A / ← : 왼쪽 이동 &nbsp;&nbsp; D / → : 오른쪽 이동<br>
        SHIFT : 드리프트 &nbsp;&nbsp; SPACE : 니트로
        <br>
        <span id="game_message">게임 시작 버튼을 눌러주세요.</span>
    </div>

    <div class="result_box" id="result_box" style="display:none;"></div>

</div>

<script>
const game_config = __CONFIG__;

const canvas = document.getElementById("race_canvas");
const ctx = canvas.getContext("2d");

const center_x = 500;
const center_y = 325;

const track_radius_x = 330;
const track_radius_y = 225;

const start_angle = -Math.PI / 2;

let race_angle = 0;
let car_speed = 0;
let lane_offset = 0;
let battery_temp = game_config.initial_temperature;
let race_time = 0;
let nitro_time = 0;
let last_time = 0;

let game_running = false;
let game_finished = false;
let drift_active = false;

let sector_records = [];
let last_sector = 0;

const keys = {};

const speed_value = document.getElementById("speed_value");
const temp_value = document.getElementById("temp_value");
const time_value = document.getElementById("time_value");
const sector_value = document.getElementById("sector_value");

const game_message = document.getElementById("game_message");
const result_box = document.getElementById("result_box");
const start_overlay = document.getElementById("start_overlay");


function draw_track() {

    ctx.fillStyle = "#173a31";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 트랙 외곽
    ctx.beginPath();
    ctx.ellipse(
        center_x, center_y,
        track_radius_x + 55,
        track_radius_y + 55,
        0, 0, Math.PI * 2
    );
    ctx.fillStyle = "#777d85";
    ctx.fill();

    // 트랙 내부
    ctx.beginPath();
    ctx.ellipse(
        center_x, center_y,
        track_radius_x,
        track_radius_y,
        0, 0, Math.PI * 2
    );
    ctx.fillStyle = "#252b35";
    ctx.fill();

    // 트랙 중앙 점선
    ctx.beginPath();
    ctx.ellipse(
        center_x, center_y,
        track_radius_x - 25,
        track_radius_y - 25,
        0, 0, Math.PI * 2
    );
    ctx.setLineDash([18, 15]);
    ctx.strokeStyle = "#b9c3cf";
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.setLineDash([]);

    // 결승선
    const finish_x = center_x;
    const finish_y = center_y - track_radius_y - 50;

    ctx.fillStyle = "#ffffff";

    for (let i = 0; i < 8; i++) {
        ctx.fillRect(finish_x - 35 + i * 9, finish_y, 9, 12);
    }

    // 트랙 구간 안내
    ctx.fillStyle = "#55d9ff";
    ctx.font = "bold 20px Arial";
    ctx.fillText("SECTOR 1", 750, 300);
    ctx.fillText("SECTOR 2", 430, 590);
    ctx.fillText("SECTOR 3", 150, 300);
}


function get_car_position() {

    const current_angle = start_angle + race_angle;

    const x = center_x +
        (track_radius_x + lane_offset) * Math.cos(current_angle);

    const y = center_y +
        (track_radius_y + lane_offset) * Math.sin(current_angle);

    const direction = Math.atan2(
        track_radius_y * Math.cos(current_angle),
        -track_radius_x * Math.sin(current_angle)
    );

    return {x, y, direction};
}


function draw_car() {

    const position = get_car_position();

    ctx.save();
    ctx.translate(position.x, position.y);
    ctx.rotate(position.direction);

    // 자동차 그림자
    ctx.fillStyle = "rgba(0,0,0,0.4)";
    ctx.fillRect(-22, -10, 48, 24);

    // 자동차 차체
    ctx.fillStyle = "#00cfff";
    ctx.fillRect(-24, -12, 48, 24);

    // 자동차 앞부분
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(12, -8, 10, 16);

    // 조종석
    ctx.fillStyle = "#10253c";
    ctx.fillRect(-8, -8, 15, 16);

    // 바퀴
    ctx.fillStyle = "#090d15";
    ctx.fillRect(-18, -16, 12, 5);
    ctx.fillRect(8, -16, 12, 5);
    ctx.fillRect(-18, 11, 12, 5);
    ctx.fillRect(8, 11, 12, 5);

    ctx.restore();
}


function draw_game() {

    draw_track();
    draw_car();
}


function update_hud() {

    speed_value.textContent = Math.round(car_speed * 1.8);
    temp_value.textContent = battery_temp.toFixed(1) + "℃";
    time_value.textContent = race_time.toFixed(1) + "s";

    const current_sector = Math.min(
        3,
        Math.floor(race_angle / (Math.PI * 2 / 3)) + 1
    );

    sector_value.textContent = current_sector + " / 3";

    if (battery_temp > 80) {
        temp_value.style.color = "#ff5555";
    } else if (battery_temp < 40) {
        temp_value.style.color = "#65baff";
    } else {
        temp_value.style.color = "#55d9ff";
    }
}


function record_sector(sector_number) {

    sector_records.push({
        name: game_config.track_sectors[sector_number].name,
        temperature: battery_temp.toFixed(1),
        time: race_time.toFixed(2)
    });
}


function finish_game(reason) {

    if (game_finished) {
        return;
    }

    game_finished = true;
    game_running = false;

    let grade = "B";

    if (reason === "FINISH") {

        if (battery_temp >= 40 && battery_temp <= 80) {
            grade = race_time < 18 ? "S" : "A";
        } else {
            grade = "C";
        }

    } else {
        grade = "F";
    }

    let sector_html = "";

    for (let i = 0; i < sector_records.length; i++) {

        sector_html +=
            '<div class="sector_row">' +
            sector_records[i].name +
            ' / 온도: ' + sector_records[i].temperature +
            '℃ / 기록: ' + sector_records[i].time + '초</div>';
    }

    result_box.style.display = "block";

    result_box.innerHTML =
        '<h2>RACE RESULT</h2>' +
        '<b>결과: ' + reason + '</b><br>' +
        '최종 온도: ' + battery_temp.toFixed(1) + '℃<br>' +
        '완주 시간: ' + race_time.toFixed(2) + '초<br>' +
        '등급: ' + grade +
        '<h3>SECTOR DATA</h3>' +
        sector_html +
        '<button id="restart_button">RESTART</button>';

    document.getElementById("restart_button").onclick = start_game;

    game_message.textContent = "경기가 종료되었습니다.";
}


function update_physics(delta_time) {

    const accelerate = keys["w"] || keys["arrowup"];
    const brake = keys["s"] || keys["arrowdown"];

    const left = keys["a"] || keys["arrowleft"];
    const right = keys["d"] || keys["arrowright"];

    drift_active = keys["shift"];

    const nitro_active = keys[" "] && nitro_time <= 0;

    // 가속 및 감속
    if (accelerate) {
        car_speed += 85 * delta_time;
    } else {
        car_speed -= 20 * delta_time;
    }

    if (brake) {
        car_speed -= 100 * delta_time;
    }

    // 니트로 사용
    if (nitro_active) {
        nitro_time = 2.0;
    }

    if (nitro_time > 0) {
        car_speed += 55 * delta_time;
        nitro_time -= delta_time;
    }

    car_speed = Math.max(0, Math.min(car_speed, 150));

    // 좌우 이동 및 드리프트
    const steering_speed = drift_active ? 75 : 48;

    if (left) {
        lane_offset -= steering_speed * delta_time;
    }

    if (right) {
        lane_offset += steering_speed * delta_time;
    }

    lane_offset = Math.max(-85, Math.min(85, lane_offset));

    // 트랙 이탈 시 속도 감소
    if (Math.abs(lane_offset) > 48) {
        car_speed *= 0.97;
        game_message.textContent = "주의! 트랙 바깥쪽으로 이동했습니다.";
    } else if (drift_active) {
        game_message.textContent = "DRIFTING!";
    } else if (nitro_time > 0) {
        game_message.textContent = "NITRO BOOST!";
    } else {
        game_message.textContent = "안정적으로 주행 중입니다.";
    }

    // 주행 거리와 시간 계산
    race_angle += (car_speed / 300) * delta_time;
    race_time += delta_time;

    // 배터리 온도 변화
    const heat_rate = game_config.battery_output / 100 * 2.2;
    const cooling_rate =
        game_config.flow_rate *
        0.12 *
        game_config.cooling_efficiency;

    battery_temp += (heat_rate - cooling_rate) * delta_time;

    // 섹터별 기록 저장
    const sector_number = Math.floor(
        race_angle / (Math.PI * 2 / 3)
    );

    if (sector_number > last_sector && last_sector < 3) {

        record_sector(last_sector);
        last_sector = sector_number;
    }

    // 과열 판정
    if (battery_temp > 100) {
        finish_game("OVERHEAT");
        return;
    }

    // 결승선 통과 판정
    if (race_angle >= Math.PI * 2) {

        if (sector_records.length < 3) {
            record_sector(2);
        }

        finish_game("FINISH");
    }
}


function game_loop(timestamp) {

    if (!game_running) {
        return;
    }

    if (last_time === 0) {
        last_time = timestamp;
    }

    const delta_time = Math.min(
        (timestamp - last_time) / 1000,
        0.05
    );

    last_time = timestamp;

    update_physics(delta_time);
    draw_game();
    update_hud();

    if (game_running) {
        requestAnimationFrame(game_loop);
    }
}


function start_game() {

    race_angle = 0;
    car_speed = 0;
    lane_offset = 0;

    battery_temp = game_config.initial_temperature;
    race_time = 0;
    nitro_time = 0;
    last_time = 0;

    sector_records = [];
    last_sector = 0;

    game_finished = false;
    game_running = true;

    result_box.style.display = "none";
    start_overlay.style.display = "none";

    game_message.textContent = "레이싱이 시작되었습니다!";

    canvas.focus();

    draw_game();
    update_hud();

    requestAnimationFrame(game_loop);
}


// 키보드 입력
window.addEventListener("keydown", function(event) {

    const key = event.key.toLowerCase();

    if (
        ["arrowup", "arrowdown", "arrowleft", "arrowright", " "]
        .includes(key)
    ) {
        event.preventDefault();
    }

    keys[key] = true;

});


window.addEventListener("keyup", function(event) {

    keys[event.key.toLowerCase()] = false;

});


window.addEventListener("blur", function() {

    for (const key in keys) {
        keys[key] = false;
    }

});


document.getElementById("start_button").onclick = start_game;


// 첫 화면 그리기
draw_game();
update_hud();

</script>

</body>
</html>
"""

# Python 설정 데이터를 JavaScript에 전달
game_html = game_html.replace(
    "__CONFIG__",
    json.dumps(game_config, ensure_ascii=False)
)

components.html(
    game_html,
    height=1000,
    scrolling=False
)
