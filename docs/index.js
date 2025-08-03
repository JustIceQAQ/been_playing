document.addEventListener('keydown', function (e) {
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        return false;
    }
});


(function () {
    let detected = false;

    const detectDevTools = () => {
        const threshold = 160;

        // 方法 1：尺寸變化
        if (window.outerWidth - window.innerWidth > threshold ||
            window.outerHeight - window.innerHeight > threshold) {
            detected = true;
        }

        // 方法 2：檢查是否斷點中斷（可混用 debugger + 時間）
        const before = performance.now();
        debugger;
        const after = performance.now();
        if (after - before > 100) {
            detected = true;
        }

        if (detected) {
            destroyPage();
        }
    };

    const destroyPage = () => {
        document.body.innerHTML = `
            <div style="display:flex;align-items:center;justify-content:center;height:100vh;font-size:2rem;color:red;">
                ⚠️ 頁面損毀，請重新整理
            </div>
        `;
        document.title = "已損毀";
        document.body.style.backgroundColor = "#000";
        window.onbeforeunload = null;
        window.onkeydown = window.onmousedown = window.onmousemove = () => false;
    };

    setInterval(detectDevTools, 1000);
})();
