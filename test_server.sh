#!/bin/bash

# 服务基础设置
export HOST=0.0.0.0
export PORT=8000
export WORKERS=1


# 参数接收
MODEL_PATH=""
PARAMS_PATH=""
MODEL_TYPE=""
MODEL_NAME=""
DEPLOY_DEVICE=""
DEPLOY_BACKEND=""

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model_path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --params_path)
            # 允许空字符串值
            if [ "$2" = '""' ] || [ "$2" = "''" ] || [ -z "$2" ]; then
                PARAMS_PATH=""
            else
                PARAMS_PATH="$2"
            fi
            shift 2
            ;;
        --model_type)
            MODEL_TYPE="$2"
            shift 2
            ;;
        --model_name)
            MODEL_NAME="$2"
            shift 2
            ;;
        --deploy_device)
            DEPLOY_DEVICE="$2"
            shift 2
            ;;
        --deploy_backend)
            DEPLOY_BACKEND="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done



# 检查必需参数
required_args=(
    "$MODEL_PATH"
    "$MODEL_TYPE"
    "$MODEL_NAME"
    "$DEPLOY_DEVICE"
    "$DEPLOY_BACKEND"
)

for arg in "${required_args[@]}"; do
    if [ -z "$arg" ]; then
        echo "错误：必需参数未提供！"
        echo "用法: $0 --model_path xxx [--params_path \"\"] --model_type xx --model_name xxx --deploy_device xxx --deploy_backend xxx"
        exit 1
    fi
done

# 设置环境变量——模型管理设置
export MODEL_PATH="$MODEL_PATH"
export PARAMS_PATH="$PARAMS_PATH"  # 允许为空
export MODEL_TYPE="$MODEL_TYPE"
export MODEL_NAME="$MODEL_NAME"
export DEPLOY_DEVICE="$DEPLOY_DEVICE"
export DEPLOY_BACKEND="$DEPLOY_BACKEND"


# 打印设置结果（可选）
echo "环境变量设置完成："
echo "-------------------------"
echo "MODEL_PATH:    ${MODEL_PATH:-<未设置>}"
echo "PARAMS_PATH:   ${PARAMS_PATH:-<未设置>}"
echo "MODEL_TYPE:    ${MODEL_TYPE:-<未设置>}"
echo "MODEL_NAME:    ${MODEL_NAME:-<未设置>}"
echo "DEPLOY_DEVICE: ${DEPLOY_DEVICE:-<未设置>}"
echo "DEPLOY_BACKEND:${DEPLOY_BACKEND:-<未设置>}"
echo "-------------------------"

nohup uvicorn main:app --host ${HOST} --port ${PORT} --workers ${WORKERS} > server.log 2>&1 &
