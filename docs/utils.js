const notStartedBadges = (tag = "h2") => `<${tag}><span class="badge bg-warning" style="color: #3c3d30;">尚未開始</span></${tag}>`
const inProgressBadges = (tag = "h2") => `<${tag}><span class="badge bg-success">進行中</span></${tag}>`
const finishedBadges = (tag = "h2") => `<${tag}><span class="badge bg-danger" style="color: #3c3d30;">已經結束</span></${tag}>`
const unableBadges = (tag = "h2") => `<${tag}><span class="badge bg-secondary">無法判斷</span></${tag}>`