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
const finishedBadges = (tag = "h2") => `<${tag}><span class="badge bg-danger" style="color: #3c3d30;">已經結束</span></${tag}>`
const unableBadges = (tag = "h2") => `<${tag}><span class="badge bg-secondary">無法判斷</span></${tag}>`