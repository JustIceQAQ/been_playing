const getContrastYIQ = (hexcolor) => {
  const h = hexcolor.replace("#", "");
  const r = parseInt(h.substr(0, 2), 16) / 255;
  const g = parseInt(h.substr(2, 2), 16) / 255;
  const b = parseInt(h.substr(4, 2), 16) / 255;
  const lin = c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  const L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  return (1.05 / (L + 0.05)) >= ((L + 0.05) / 0.05) ? "#fff" : "#000";
};

const notStartedBadges = (tag = "h2", targetDate = null, countdownOnly = false) => {
  let content;
  if (countdownOnly && targetDate !== null) {
    content = dayjs().to(targetDate) + "開始";
  } else {
    const subtitle = targetDate !== null ? `<br><small>${dayjs().to(targetDate)}開始</small>` : "";
    content = `尚未開始${subtitle}`;
  }
  return `<${tag}><span class="badge bg-warning" style="color: #3c3d30;">${content}</span></${tag}>`;
}
const inProgressBadges = (tag = "h2", targetDate = null, countdownOnly = false) => {
  let content;
  if (countdownOnly && targetDate !== null) {
    content = dayjs().isSame(targetDate, "day") ? "今天結束" : dayjs().to(targetDate) + "結束";
  } else {
    content = "進行中";
  }
  return `<${tag}><span class="badge bg-success">${content}</span></${tag}>`;
}
const finishedBadges = (tag = "h2") => `<${tag}><span class="badge bg-danger">已經結束</span></${tag}>`
const unableBadges = (tag = "h2") => `<${tag}><span class="badge bg-secondary">無法判斷</span></${tag}>`