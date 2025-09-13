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

        if (window.outerWidth - window.innerWidth > threshold ||
            window.outerHeight - window.innerHeight > threshold) {
            detected = true;
        }
        console.log(threshold, window.outerWidth - window.innerWidth, window.outerHeight - window.innerHeight)

        const before = performance.now();
        debugger;
        const after = performance.now();
        let result = after - before
        console.log(result)
        if (result > 1000) {
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
