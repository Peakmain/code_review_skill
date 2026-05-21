---
name: code_review
description: Android项目代码规范审查工具，基于自定义的10套代码规范文档，对指定类或整个项目进行全面CR，输出问题代码、原因、修改建议，并生成Markdown格式的审查报告。使用场景：(1) 对单个Kotlin/Java类进行代码规范审查，(2) 对整个Android项目进行全量代码规范审查，(3) 生成标准化的CR报告文档。
---

# Android 代码规范审查 Skill 使用指南

## 功能说明
本工具基于10套自定义Android代码规范文档，对代码进行自动化规范审查，输出标准化的审查报告。

## 引用规范文档
所有审查依据均来自 `references/` 目录下的规范文档：
1. [一、Android命名规范.md](references/一、Android命名规范.md)
2. [二、Android开发手册——Android UI和布局规范.md](references/二、Android开发手册——Android UI和布局规范.md)
3. [三、Android 编码规范.md](references/三、Android 编码规范.md)
4. [四、Android常见难题.md](references/四、Android常见难题.md)
5. [五、Android资源文件命名与使用.md](references/五、Android资源文件命名与使用.md)
6. [六、Android基本组件.md](references/六、Android基本组件.md)
7. [七、UI与布局.md](references/七、UI与布局.md)
8. [八、Android应用安全开发规范.md](references/八、Android应用安全开发规范.md)
9. [八、进程、线程与消息通信.md](references/八、进程、线程与消息通信.md)
10. [九、文件与数据库.md](references/九、文件与数据库.md)

## 使用流程

### 自动化扫描（推荐）
直接运行skill命令即可自动完成全量扫描：
```
/code_review all                # 审查整个项目所有Kotlin/Java文件
/code_review app/src/main/      # 审查指定目录
/code_review MainActivity.kt    # 审查单个文件
```

脚本会自动：
1. 遍历所有目标代码文件（自动排除build/test等目录）
2. 逐行扫描匹配规范规则
3. 自动收集所有问题点
4. 生成标准化Markdown审查报告

### 手动审查步骤
1. 确定审查范围
- 如果用户指定具体类/文件路径：只审查该文件
- 如果用户输入 `all`：审查整个项目的所有Kotlin/Java代码文件

2. 执行审查步骤
1. 读取目标文件内容
2. 对照上述10套规范文档逐行检查
3. 记录所有不符合规范的问题点：
   - 问题位置：文件路径 + 行号
   - 问题代码片段
   - 违反的规范条款
   - 问题原因说明
   - 具体修改建议
4. 统计审查结果：总问题数、各严重级别问题数

3. 输出审查报告
将审查结果输出为 Markdown 文档，文件命名规则：`peakmain_<审查对象>_cr.markdown`
- 审查单个文件：`peakmain_<类名>_cr.markdown`
- 审查整个项目：`peakmain_project_full_cr.markdown`

## 报告格式要求
```markdown
# Android 代码审查报告
## 基本信息
- 审查对象：xxx
- 审查时间：YYYY-MM-DD HH:MM:SS
- 总问题数：N
- 严重问题：N
- 警告问题：N
- 建议优化：N

## 问题详情
### 1. [问题级别] 问题简述
- **位置**：文件路径:行号
- **问题代码**：
```kotlin
// 问题代码片段
```
- **违反规范**：引用的规范文档条款
- **问题原因**：详细说明为什么不符合规范
- **修改建议**：给出具体的修正代码示例
```

## 问题级别定义
- **严重**：会导致功能异常、性能问题、安全漏洞的问题
- **警告**：不符合规范但不影响功能运行的问题
- **建议**：可以优化的代码写法，非强制要求

## 注意事项
1. 优先遵循项目本身的CLAUDE.md中的开发规范
2. 对于规范文档中没有明确说明的场景，按照Android官方最佳实践判断
3. 保留现有正确的代码风格，不要随意修改符合规范的代码