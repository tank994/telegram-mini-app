"""
Telegram Mini App Bot 示例

这个 Bot 用于配合 Mini App 使用，接收用户发送的数据
"""

import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============== 配置区域 ==============
# 替换为你的 Bot Token（从 @BotFather 获取）
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# 替换为你的 Mini App URL（必须是 HTTPS）
WEB_APP_URL = "https://your-app.vercel.app"
# ======================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令"""
    user = update.effective_user
    
    # 创建内联键盘，包含打开 Mini App 的按钮
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 打开 Mini App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"你好 {user.first_name}! 👋\n\n"
        f"这是一个 Telegram Mini App 示例 Bot。\n"
        f"点击下方按钮打开 Mini App：",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /help 命令"""
    await update.message.reply_text(
        "可用命令：\n"
        "/start - 开始使用\n"
        "/help - 显示帮助\n"
        "/app - 打开 Mini App\n"
        "/data - 查看最近接收的数据"
    )


async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /app 命令 - 打开 Mini App"""
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 打开 Mini App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "点击按钮打开 Mini App：",
        reply_markup=reply_markup
    )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理从 Mini App 发送的数据"""
    if update.effective_message and update.effective_message.web_app_data:
        data = json.loads(update.effective_message.web_app_data.data)
        
        logger.info(f"收到来自 Mini App 的数据: {data}")
        
        # 根据数据类型处理
        if data.get('action') == 'counter_update':
            counter_value = data.get('value', 0)
            timestamp = data.get('timestamp', '未知时间')
            
            await update.message.reply_text(
                f"📊 收到计数器更新！\n\n"
                f"当前值: {counter_value}\n"
                f"时间: {timestamp}"
            )
        else:
            await update.message.reply_text(
                f"📨 收到数据：\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```",
                parse_mode='Markdown'
            )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理内联键盘按钮点击"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'open_app':
        await query.edit_message_text(
            "点击下方按钮打开 Mini App：",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text="🚀 打开 Mini App",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )]
            ])
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """错误处理"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "抱歉，发生了错误。请稍后重试。"
        )


def main() -> None:
    """启动 Bot"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("错误：请先设置 BOT_TOKEN！")
        print("1. 在 Telegram 中搜索 @BotFather")
        print("2. 创建新 Bot 并获取 Token")
        print("3. 将 Token 填入 bot.py 文件中的 BOT_TOKEN 变量")
        return
    
    if WEB_APP_URL == "https://your-app.vercel.app":
        print("警告：请设置正确的 WEB_APP_URL！")
    
    # 创建 Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("app", open_app))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # 添加错误处理器
    application.add_error_handler(error_handler)
    
    # 启动 Bot
    print("Bot 已启动！按 Ctrl+C 停止")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
