# Telegram Mini App 示例项目

这是一个完整的 Telegram Mini App 示例项目，展示了如何使用 Telegram Web App SDK 开发小程序。

## 功能特性

- 用户信息展示
- 计数器交互
- 发送数据给 Bot
- 弹窗显示
- 全屏切换
- 主题自适应（支持深色/浅色模式）
- 触觉反馈

## 快速开始

### 1. 部署 Web 应用

#### 方式一：使用 Vercel（推荐）
1. 将项目上传到 GitHub
2. 在 [Vercel](https://vercel.com) 导入项目
3. 自动部署后会获得 HTTPS 链接

#### 方式二：使用 Netlify
1. 将项目上传到 GitHub
2. 在 [Netlify](https://netlify.com) 导入项目
3. 自动部署后会获得 HTTPS 链接

#### 方式三：本地测试
```bash
# 使用 Python 启动本地服务器
python -m http.server 8000

# 或使用 Node.js
npx serve .
```

### 2. 配置 Telegram Bot

1. 在 Telegram 中搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 创建新 Bot
3. 设置 Bot 名称和用户名
4. 获取 Bot Token
5. 发送 `/mybots` 选择你的 Bot
6. 点击 **Bot Settings** → **Menu Button** → **Configure menu button**
7. 输入你的 Web 应用 URL（必须是 HTTPS）

### 3. 测试 Mini App

1. 在 Telegram 中搜索你的 Bot
2. 点击左下角的菜单按钮（或发送 `/start`）
3. 即可打开 Mini App

## 项目结构

```
telegram-mini-app/
├── index.html      # 主页面（单页应用）
└── README.md       # 项目说明
```

## 核心 API 使用示例

### 初始化
```javascript
let tg = window.Telegram.WebApp;
tg.ready();
tg.expand();
```

### 获取用户信息
```javascript
const user = tg.initDataUnsafe?.user;
console.log(user.username);
```

### 发送数据给 Bot
```javascript
tg.sendData(JSON.stringify({action: 'test', value: 123}));
```

### 显示弹窗
```javascript
tg.showPopup({
    title: '标题',
    message: '内容',
    buttons: [{id: 'ok', text: '确定'}]
});
```

## 自定义主题

Mini App 会自动适配 Telegram 的主题颜色：

```css
:root {
    --tg-theme-bg-color: #ffffff;
    --tg-theme-text-color: #000000;
    --tg-theme-button-color: #2481cc;
    --tg-theme-button-text-color: #ffffff;
    /* ... */
}
```

## 开发注意事项

1. **必须使用 HTTPS** - Telegram 要求 Mini App 必须通过 HTTPS 访问
2. **响应式设计** - 确保在各种屏幕尺寸上都能正常显示
3. **主题适配** - 使用 Telegram 提供的主题变量
4. **性能优化** - 保持加载速度快，用户体验流畅
5. **测试多平台** - 在 iOS、Android、Desktop 上都要测试

## 进阶功能

### 获取启动参数
```javascript
const params = new URLSearchParams(window.location.search);
const startParam = params.get('startapp');
```

### 设置主按钮
```javascript
tg.MainButton.setText('提交');
tg.MainButton.onClick(function() {
    // 处理点击
});
tg.MainButton.show();
```

### 显示加载指示器
```javascript
tg.showProgress(true);  // 显示
tg.showProgress(false); // 隐藏
```

## 参考资源

- [Telegram Web Apps 官方文档](https://core.telegram.org/bots/webapps)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Web App SDK 源码](https://telegram.org/js/telegram-web-app.js)

## 许可证

MIT License
