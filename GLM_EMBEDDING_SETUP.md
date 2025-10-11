# GLM Embedding 集成指南

## 概述

本项目已成功集成GLM (智谱AI) Embedding模型，支持使用GLM的embedding-3和embedding-2模型生成高质量的中文文本向量。

## 支持的模型

### GLM Embedding-3 (推荐)
- **默认维度**: 2048
- **可选维度**: 256, 512, 1024, 2048
- **Token限制**: 单条最多3072 tokens，数组最大64条
- **特点**: 最新模型，支持多维度选择，性能更优

### GLM Embedding-2
- **固定维度**: 1024
- **Token限制**: 单条最多512 tokens，数组总长度不超过8K
- **特点**: 稳定版本，适合一般场景

## 配置步骤

### 1. 获取API密钥

访问 [智谱AI开放平台](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) 获取API密钥。

### 2. 更新环境配置

在 `.env` 文件中添加以下配置：

```bash
# -- GLM (智谱AI) Embeddings Settings --
GLM_API_KEY="your_glm_api_key_here"
GLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4/embeddings"
GLM_EMBEDDINGS_MODEL_NAME="embedding-3"
GLM_EMBEDDINGS_DIMENSIONS="1024"

# 设置embeddings provider为glm
EMBEDDINGS_PROVIDER="glm"
```

### 3. 配置参数说明

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `GLM_API_KEY` | GLM API密钥 | - | 必填 |
| `GLM_BASE_URL` | GLM API端点 | - | https://open.bigmodel.cn/api/paas/v4/embeddings |
| `GLM_EMBEDDINGS_MODEL_NAME` | 模型名称 | embedding-3, embedding-2 | embedding-3 |
| `GLM_EMBEDDINGS_DIMENSIONS` | 向量维度 | 256, 512, 1024, 2048 | 1024 |
| `EMBEDDINGS_PROVIDER` | Embedding提供者 | openai, ollama, glm | openai |

## 使用示例

### 基本配置

```bash
# 使用GLM Embedding-3，1024维度
EMBEDDINGS_PROVIDER="glm"
GLM_API_KEY="your_api_key"
GLM_EMBEDDINGS_MODEL_NAME="embedding-3"
GLM_EMBEDDINGS_DIMENSIONS="1024"
```

### 高性能配置

```bash
# 使用GLM Embedding-3，512维度（平衡性能和准确性）
EMBEDDINGS_PROVIDER="glm"
GLM_API_KEY="your_api_key"
GLM_EMBEDDINGS_MODEL_NAME="embedding-3"
GLM_EMBEDDINGS_DIMENSIONS="512"
```

### 兼容性配置

```bash
# 使用GLM Embedding-2，固定1024维度
EMBEDDINGS_PROVIDER="glm"
GLM_API_KEY="your_api_key"
GLM_EMBEDDINGS_MODEL_NAME="embedding-2"
```

## 重构知识库

当切换到GLM embedding时，需要重新构建知识库以匹配新的向量维度：

```bash
# 1. 备份现有知识库
cd backend
mv chroma_db chroma_db_backup

# 2. 重新构建知识库
source ../venv/bin/activate
PYTHONPATH=. python app/scripts/build_vector_store.py

# 3. 重启后端服务
# 停止当前服务，然后重新启动
```

## 测试功能

运行测试脚本验证GLM embedding功能：

```bash
source venv/bin/activate
python test_glm_embeddings.py
```

## 性能对比

| 模型 | 维度 | Token限制 | 中文优化 | 性能特点 |
|------|------|-----------|----------|----------|
| `embedding-3` | 256-2048 | 3072 | ⭐⭐⭐⭐⭐ | 最新模型，多维度可选 |
| `embedding-2` | 1024 | 512 | ⭐⭐⭐⭐ | 稳定版本，通用性强 |
| `qwen2.5:0.5b` | 896 | 2K+ | ⭐⭐⭐⭐ | 本地模型，无API调用 |
| `nomic-embed-text` | 768 | 8192 | ⭐⭐⭐ | 轻量级，速度快 |

## 注意事项

1. **API配额**: GLM API有调用限制，请关注您的API使用量
2. **向量维度**: 切换embedding模型后必须重新构建知识库
3. **网络连接**: GLM需要网络连接到智谱AI服务
4. **错误处理**: 系统已集成完善的错误处理和重试机制

## 故障排除

### 常见错误

1. **`GLM_API_KEY is required`**
   - 确保在.env文件中正确设置了GLM_API_KEY

2. **`Invalid API key`**
   - 检查API密钥是否正确和有效

3. **`Collection expecting embedding with dimension X, got Y`**
   - 需要重新构建知识库以匹配新的向量维度

4. **网络连接错误**
   - 检查网络连接和API端点是否可访问

### 调试命令

```bash
# 检查配置
source venv/bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('GLM API Key:', 'SET' if os.getenv('GLM_API_KEY') else 'NOT SET')
print('Embeddings Provider:', os.getenv('EMBEDDINGS_PROVIDER'))
"
```

## 完成

GLM embedding已成功集成到您的AI电商助手系统中！配置API密钥后即可开始使用高质量的中文embedding服务。