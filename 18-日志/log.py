from loguru import logger

log = logger

# 配置日志文件
logger.add("./data/log.txt", level="INFO", rotation="10MB", compression="zip")
# 配置控制台日志文件
logger.add("./data/console.txt", level="INFO", rotation="10MB", compression="zip", colorize=True)
