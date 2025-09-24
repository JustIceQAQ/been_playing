document.addEventListener('keydown', function (e) {
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        return false;
    }
});


(function () {
    let detected = false;

    const detectDevTools = () => {
        const before = performance.now();
        debugger;
        const after = performance.now();
        let result = after - before
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
                <img src="icon_folder/....png" alt="? 你想幹嘛?? 🤨">
            </div>
        `;
        document.title = "? 你想幹嘛?? 🤨";
        document.body.style.backgroundColor = "#000";
        window.onbeforeunload = null;
        window.onkeydown = window.onmousedown = window.onmousemove = () => false;
    };

    setInterval(detectDevTools, 1000);
})();
