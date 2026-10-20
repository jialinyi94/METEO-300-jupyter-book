---
title: 导言
---

本书写给 AI 天气分析师。读者会用 Python 和机器学习，但学过的气象学不多。本书用真实 data 讲大气科学。

## 每页回答四个问题

1. 真实 data 长什么样？
2. 最常用的 dataset 是哪一个？
3. 哪些软件包处理和计算这些 data？
4. 这些 data 和 AI weather model 有什么联系？

## 每页的六节

每个主题页都有六节，顺序固定。

1. 知识点：本页的物理知识和公式。
2. 真实 data：一张真实 data 的图或表。
3. dataset：最常用的 dataset 和它的访问方式。
4. 计算：用软件包算出一个值，再用手算核对它。
5. AI 天气连接：这个量在 AI weather model 里的角色。
6. 练习：用真实 data 做的练习。

## 结构

本书有 15 个主题页，分成四个部分：

1. pressure 与热力学
2. 动力学、water vapour 与稳定度
3. geopotential height、向量微积分与 thermal wind
4. atmospheric boundary layer、vorticity 与 extratropical cyclone

参考部分有 dataset、工具包、术语表和写作规范。

## 出处

知识点取自宾夕法尼亚州立大学的公开课程 [METEO 300](https://www.e-education.psu.edu/meteo300/)。课程作者是 William H. Brune，课程以 CC BY-NC-SA 4.0 许可发布。本书改编课程的内容，所以本书的正文也以 CC BY-NC-SA 4.0 发布。

## 运行页面

每个页面都是一个 MyST Markdown notebook。安装 uv 后，在仓库目录运行 `uv sync`。然后用 Jupyter 打开 `docs/topics/` 里的页面，或者用 `uv run jupyter-book start --execute` 在本地预览全书。

## 写作规范

本书的中文正文遵守[写作规范](docs/reference/style.md)。每个概念只用一个术语，术语见[术语表](docs/reference/glossary.md)。
