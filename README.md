# Code Review Skill - Android 代码规范审查工具

基于 10 套自定义 Android 代码规范文档，对 Kotlin/Java 代码进行自动化规范审查，输出标准化 Markdown 审查报告。

## 目录结构

```
code_review/
├── SKILL.md                          # Skill 定义与使用指南
├── scripts/
│   └── cr_scan.py                    # 自动化扫描脚本（核心）
├── references/                       # 10套规范文档（审查依据）
│   ├── 一、Android命名规范.md
│   ├── 二、Android开发手册——Android UI和布局规范.md
│   ├── 三、Android 编码规范.md
│   ├── 四、Android常见难题.md
│   ├── 五、Android资源文件命名与使用.md
│   ├── 六、Android基本组件.md
│   ├── 七、UI与布局.md
│   ├── 八、Android应用安全开发规范.md
│   ├── 八、进程、线程与消息通信.md
│   └── 九、文件与数据库.md
└── README.md                         # 本文件
```

## 快速开始

### 方式一：Python 脚本扫描（推荐）

```bash
# 审查整个项目
python scripts/cr_scan.py all

# 审查指定目录
python scripts/cr_scan.py app/src/main/java/com/atour/atourlife/

# 审查单个文件
python scripts/cr_scan.py app/src/main/java/com/atour/atourlife/MainActivity.kt
```

脚本会自动：
1. 遍历目标代码文件（自动排除 `build/`、`test/`、`androidTest/`、`.git/`、`.gradle/` 目录）
2. 逐行扫描匹配规范规则
3. 收集所有问题点
4. 生成标准化 Markdown 审查报告

### 方式二：Claude Code Skill 调用

在 Claude Code 中直接使用：

```
/code_review all                        # 全量审查
/code_review app/src/main/              # 审查指定目录
/code_review MainActivity.kt            # 审查单个文件
```

## 审查规则覆盖

脚本内置 **30+ 条检查规则**，覆盖以下维度：

### 1. 命名规范（一、Android命名规范.md）

| 规则 | 级别 | 说明 |
|------|------|------|
| 枚举类命名冗余 | 警告 | 禁止同时使用 `E` 前缀和 `Enum` 后缀 |
| 枚举类缺少后缀 | 警告 | 枚举类须以 `Enum` 结尾 |
| ViewModel 命名 | 警告 | 禁止 `VM` 简写，须用完整 `ViewModel` 后缀 |
| Activity 命名 | 警告 | 禁止 `Act` 简写，须用完整 `Activity` 后缀 |
| Fragment 命名 | 警告 | 禁止 `Frag` 简写，须用完整 `Fragment` 后缀 |
| Event 事件类命名 | 警告 | 事件类须以 `Event` 结尾 |
| Adapter 适配器命名 | 警告 | 适配器须以 `Adapter` 结尾 |
| ViewHolder 命名 | 警告 | ViewHolder 须以 `ViewHolder` 结尾 |
| 目录专项命名 | 警告 | helper/manager/constants/listener/implement/apis/request/response/widget 目录下类名后缀检查 |
| 方法命名 | 警告 | 方法名须小驼峰，动词开头 |
| 变量命名 | 警告 | 禁止 `api`/`data`/`info`/`bean`/`obj`/`temp` 等模糊变量名 |
| 包名规范 | 警告 | 包名必须全部小写 |

### 2. 编码规范（三、Android编码规范.md）

| 规则 | 级别 | 说明 |
|------|------|------|
| 禁止 System.out.println | 警告 | 须使用 `LogUtils.d/e/i/w` |
| 禁止硬编码字符串 | 建议 | Toast/Snackbar 文本须使用 `R.string.xxx` |
| requireContext 安全检查 | **严重** | Fragment 中禁止使用 `requireContext()`，须判空 |
| 不安全类型转换 | **严重** | 集合类型禁止直接 `as` 强制转换 |

### 3. 安全规范（八、Android应用安全开发规范.md）

| 规则 | 级别 | 说明 |
|------|------|------|
| WebView JS 接口风险 | **严重** | `setJavaScriptEnabled(true)` 需配合安全校验 |
| 明文存储敏感信息 | **严重** | 密码/token/secret 禁止明文存入 SharedPreferences |

### 4. 线程与进程（八、进程、线程与消息通信.md）

| 规则 | 级别 | 说明 |
|------|------|------|
| 禁止直接 new Thread | 警告 | 须使用线程池或 Coroutine |

### 5. 项目专项规则

| 规则 | 级别 | 说明 |
|------|------|------|
| 旧网络请求方式 | 警告 | `RetrofitManager.createService` 须迁移到 Hilt 注入 |

## 输出报告

审查完成后会在当前目录生成 Markdown 报告：

- 全量审查：`peakmain_project_full_cr.markdown`
- 单文件审查：`peakmain_<类名>_cr.markdown`

### 报告格式示例

```markdown
# Android 全量代码审查报告

## 基本信息
- 审查对象：整个亚朵生活Android项目（共 847 个代码文件）
- 审查时间：2026-05-21 14:30:00
- 总问题数：42
- 严重问题：5
- 警告问题：30
- 建议优化：7

## 问题详情

### 1. [严重] 不安全的强制类型转换风险
- **位置**：app/src/main/java/.../OrderViewModel.kt:128
- **问题代码**：
  ```java
  val list = response.data as ArrayList<OrderItem>
  ```
- **违反规范**：《三、Android 编码规范》类型安全相关要求
- **问题原因**：直接强制转换集合类型，实际类型不匹配会导致崩溃
- **修改建议**：使用安全转换方式或修改接口定义明确返回类型

### 2. [警告] ViewModel类禁止使用VM简写后缀
- **位置**：lib_hotel/src/main/java/.../HotelListVM.kt:15
- **问题代码**：
  ```java
  class HotelListVM : BaseViewModel()
  ```
- **违反规范**：《一、Android命名规范.md》第185条
- **问题原因**：ViewModel类使用了VM简写后缀
- **修改建议**：将VM简写改为完整的ViewModel后缀
```

## 问题级别说明

| 级别 | 含义 | 处理建议 |
|------|------|----------|
| **严重** | 可能导致崩溃、安全漏洞、功能异常 | 必须修复 |
| **警告** | 不符合规范但不影响功能 | 建议修复 |
| **建议** | 可优化的代码写法 | 可选修复 |

## 自定义规则

编辑 `scripts/cr_scan.py` 中的 `RULES` 列表即可添加/修改检查规则。规则结构：

```python
{
    'name': '规则名称',
    'level': '严重',          # 严重 / 警告 / 建议
    'pattern': r'正则表达式',  # 用于匹配问题代码
    'violation': '违反的规范条款',
    'reason': '问题原因说明',
    'fix': '修改建议',
    'path_filter': '/event/'  # 可选：限定检查的目录路径
}
```

### 添加新规则示例

```python
# 禁止使用 deprecated API
{
    'name': '使用了已废弃的API',
    'level': '警告',
    'pattern': r'AsyncTask|LocalBroadcastManager',
    'violation': 'Android官方最佳实践',
    'reason': '该API已被官方标记为废弃，应使用推荐的替代方案',
    'fix': 'AsyncTask → Coroutine，LocalBroadcastManager → LiveData/Flow'
}
```

## 排除目录

脚本默认跳过以下目录，不参与扫描：

- `build/` - 构建产物
- `test/` - 单元测试
- `androidTest/` - 仪表测试
- `.git/` - Git 版本控制
- `.gradle/` - Gradle 缓存

如需调整排除目录，修改 `cr_scan.py` 中的 `EXCLUDE_DIRS` 元组。

## 依赖要求

- Python 3.6+
- 无第三方依赖（仅使用标准库 `os`、`re`、`sys`、`datetime`）

## 注意事项

1. 脚本运行在项目根目录下，报告文件生成在**当前工作目录**
2. 审查结果仅供参考，最终以人工复核为准
3. 规范文档中的条款优先级高于脚本规则
4. 对于规范文档未明确覆盖的场景，遵循 Android 官方最佳实践