<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>방패로 막기 게임</title>
    <style>
        body {
            margin: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: sans-serif;
            overflow: hidden;
        }
        canvas {
            background-color: #111;
            border: 4px solid #fff;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="600"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 게임 상태
let score = 0;
let gameOver = false;

// 방패 (플레이어)
const shield = {
    x: canvas.width / 2 - 40,
    y: canvas.height - 80,
    width: 80,
    height: 15
};

// 발사체 배열
const projectiles = [];

// 발사체 생성 함수
function spawnProjectile() {
    if (gameOver) return;

    const isArrow = Math.random() > 0.5; // 반반 확률로 화살 또는 총알
    const type = isArrow ? 'arrow' : 'bullet';
    const size = isArrow ? 20 : 8;
    const speed = isArrow ? 4 : 7; // 총알이 더 빠름

    projectiles.push({
        x: Math.random() * (canvas.width - 20) + 10,
        y: 0,
        type: type,
        speed: speed,
        size: size
    });

    // 점수가 높아질수록 생성 속도가 빨라짐
    let nextSpawn = Math.max(300, 1000 - score * 20);
    setTimeout(spawnProjectile, nextSpawn);
}

// 마우스 이동 감지
canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    
    // 방패가 화면 밖으로 나가지 않도록 제한
    shield.x = mouseX - shield.width / 2;
    if (shield.x < 0) shield.x = 0;
    if (shield.x > canvas.width - shield.width) shield.x = canvas.width - shield.width;
});

// 터치 이벤트 지원 (모바일)
canvas.addEventListener("touchmove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const touchX = e.touches[0].clientX - rect.left;
    shield.x = touchX - shield.width / 2;
    if (shield.x < 0) shield.x = 0;
    if (shield.x > canvas.width - shield.width) shield.x = canvas.width - shield.width;
    e.preventDefault();
});

// 재시작 클릭
canvas.addEventListener("click", () => {
    if (gameOver) {
        gameOver = false;
        score = 0;
        projectiles.length = 0;
        spawnProjectile();
        update();
    }
});

// 게임 루프
function update() {
    if (gameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "white";
        ctx.font = "30px Arial";
        ctx.textAlign = "center";
        ctx.fillText("게임 오버!", canvas.width / 2, canvas.height / 2 - 20);
        
        ctx.font = "20px Arial";
        ctx.fillText(`최종 점수: ${score}`, canvas.width / 2, canvas.height / 2 + 20);
        ctx.fillText("클릭하여 다시 시작", canvas.width / 2, canvas.height / 2 + 60);
        return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 방패 그리기
    ctx.fillStyle = "#2ecc71"; // 초록색 방패
    ctx.fillRect(shield.x, shield.y, shield.width, shield.height);

    // 발사체 업데이트 및 그리기
    for (let i = projectiles.length - 1; i >= 0; i--) {
        const p = projectiles[i];
        p.y += p.speed;

        if (p.type === 'arrow') {
            // 화살 그리기 (노란색 세로선)
            ctx.strokeStyle = "#f1c40f";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x, p.y + p.size);
            ctx.stroke();
        } else {
            // 총알 그리기 (빨간색 원)
            ctx.fillStyle = "#e74c3c";
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        }

        // 충돌 검사 (방패로 막았을 때)
        if (p.y + p.size >= shield.y && p.y <= shield.y + shield.height &&
            p.x >= shield.x && p.x <= shield.x + shield.width) {
            projectiles.splice(i, 1);
            score++;
            continue;
        }

        // 바닥에 닿았을 때 (놓쳤을 때 -> 게임 오버)
        if (p.y > canvas.height) {
            gameOver = true;
        }
    }

    // 점수 표시
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.textAlign = "left";
    ctx.fillText(`점수: ${score}`, 20, 40);

    requestAnimationFrame(update);
}

// 게임 시작
spawnProjectile();
update();
</script>

</body>
</html>