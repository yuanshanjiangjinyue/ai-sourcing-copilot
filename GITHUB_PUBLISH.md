# 公开仓库发布流程

当前 GitHub 连接已确认可以访问你的 GitHub 账号，但没有新建 repository 的工具权限。为了避免污染已有项目，这个包没有写入任何现有仓库。

1. 登录 GitHub，在 https://github.com/new 创建一个**公开**空仓库，推荐名称 `ai-sourcing-copilot`。**不要勾选 Add a README、.gitignore 或 License**。
2. 把创建好的仓库 URL 发送到当前聊天，便于我继续使用已连接的 GitHub 仓库写入能力。
3. 如果你希望自行完成：下载带 `.git` 历史的发布包，解压并在项目目录运行：

   ```bash
   ./publish_to_github.sh yuanshanjiangjinyue/ai-sourcing-copilot
   ```

   Windows PowerShell 等价命令：

   ```powershell
   git remote add origin https://github.com/yuanshanjiangjinyue/ai-sourcing-copilot.git
   git push -u origin main
   ```

完成后可在 GitHub 的 Actions 页面观察 `Test demo API and matching logic`。**GitHub Pages 需要另外配置，不会因 push 自动部署。**

**知识产权风险**：公开代码不等于别人获得使用许可；但公开细节会影响未申请发明专利的新颖性。此仓库只包含演示用规则实现与虚构数据，不含专利技术交底、潜在客户名单、商业报价策略或 API 密钥。