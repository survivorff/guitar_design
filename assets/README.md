# assets · 图示资源

本目录存放知识库用到的图示(SVG 矢量图)和生成脚本。

## 结构
- `images/` —— 所有 SVG 图示(和弦图、指板图、五声盒子、吉他部件、坐姿、扫弦方向等)
- `scripts/generate_diagrams.py` —— 生成上述图示的 Python 脚本

## 为什么用 SVG
- **矢量**:任意缩放不糊。
- **文本格式**:可被 git 版本管理、可 diff、体积小。
- **GitHub 原生渲染**:在 Markdown 里 `![](...)` 直接显示。
- **可复现**:改脚本即可批量重新生成,保证风格一致、数据准确。

## 重新生成
```bash
python3 assets/scripts/generate_diagrams.py
```
脚本只依赖 Python 标准库,无需安装第三方包。

## 新增图示
在 `generate_diagrams.py` 里:
- 加新和弦:往 `CHORDS` 字典加一项(格式见注释)。
- 加新类型图:仿照现有函数写一个返回 SVG 字符串的函数,再 `save(...)`。

> 真实照片/视频类内容(如精细的手型、姿势)不在此生成,文档中会用示意图 + 视频参考指引代替。
