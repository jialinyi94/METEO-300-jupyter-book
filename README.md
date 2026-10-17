# METEO-300-jupyter-book

一本用真实数据学大气科学的数据书，写给 AI 天气分析师。网站用 Jupyter Book 2 构建。

<!-- 书名、副标题和作者只写在 myst.yml 里。 -->

## 定位

本书的每一页回答四个问题：

1. 真实数据长什么样？
2. 最常用的数据集是哪一个？
3. 哪些软件包处理和计算这些数据？
4. 这些数据和 AI 天气模型有什么联系？

知识点取自宾夕法尼亚州立大学的公开课程 [METEO 300](https://www.e-education.psu.edu/meteo300/)。

## 构建网站

```bash
uv sync                                                # 安装环境
uv run jupyter-book build --html --execute --strict    # 构建网站，执行 notebook
uv run jupyter-book start --execute                    # 本地预览
```

网站输出到 `_build/html/`。

## 检查

```bash
uv run pre-commit install           # 以后每次提交前自动检查
uv run pre-commit run --all-files   # 检查全部文件
uv run python tools/ste_check.py    # 只检查写作规范
uv run pytest                       # 运行单元测试
```

## 添加依赖

```bash
uv add <package>
```

uv 同时更新 `pyproject.toml` 和 `uv.lock`。两个文件一起提交。

## 目录

| 路径 | 内容 |
|---|---|
| `myst.yml` | 书名、目录和网站设置 |
| `intro.md` | 导言 |
| `docs/topics/` | 15 个主题页 |
| `docs/reference/` | 参考页 |
| `docs/_template.md` | 页面模板 |
| `src/meteo300/` | Python 包 |
| `tools/` | 检查工具 |
| `tests/` | 单元测试 |
| `STYLE.md` | 写作规范 |
| `glossary.md` | 术语表 |

## 许可

本仓库使用两种许可：

- 正文、图和练习以 CC BY-NC-SA 4.0 发布，全文见 `LICENSE-CONTENT`。正文改编自 METEO 300，原课程使用这个许可，所以本书也使用它。
- 代码以 MIT 发布，全文见 `LICENSE`。代码包括 `src/`、`tools/`、`tests/` 和页面里的代码单元。
- `data/samples/` 里的数据样本沿用各自来源的许可，见同一目录里的署名文件。

## English summary

This repository holds a data book about atmospheric science for AI weather analysts.
Each page shows real data, the most-used dataset, the Python packages and the link to AI weather models.
The text is in Chinese.
The content adapts the Penn State course METEO 300 under CC BY-NC-SA 4.0.
The code uses the MIT License.
