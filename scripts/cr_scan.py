#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.getcwd()
# 支持的代码文件后缀
CODE_EXTENSIONS = ('.kt', '.java')
# 排除的目录
EXCLUDE_DIRS = ('build', 'test', 'androidTest', '.git', '.gradle')

# 规则配置
RULES = [
    # ==================== 一、Android命名规范 ====================
    # 枚举类命名检查
    {
        'name': '枚举类命名重复冗余',
        'level': '警告',
        'pattern': r'public enum E\w+Enum|enum class E\w+Enum',
        'violation': '《一、Android命名规范.md》第191条：枚举类以Enum作为后缀标识',
        'reason': '枚举类同时使用了E前缀和Enum后缀，属于命名冗余',
        'fix': '去掉E前缀，保留Enum后缀'
    },
    {
        'name': '枚举类缺少统一后缀',
        'level': '警告',
        'pattern': r'public enum (?!\w+Enum)\w+[^E]$|enum class (?!\w+Enum)\w+[^E]$',
        'violation': '《一、Android命名规范.md》第191条：枚举类以Enum作为后缀标识',
        'reason': '枚举类没有按照规范添加Enum后缀，命名不统一',
        'fix': '添加Enum后缀'
    },
    # 事件类命名检查
    {
        'name': 'Event事件类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Event)\w+Bean.*{|class (?!\w+Event)\w+Bean.*{',
        'violation': '《一、Android命名规范.md》第187条：事件类以Event/EventBus作为后缀标识',
        'reason': '该类属于EventBus事件类，放在event包下，却使用了Bean后缀',
        'fix': '改为Event后缀'
    },
    # ViewModel命名检查
    {
        'name': 'ViewModel类禁止使用VM简写后缀',
        'level': '警告',
        'pattern': r'public class \w+VM extends|class \w+VM :',
        'violation': '《一、Android命名规范.md》第185条：ViewModel类以ViewModel作为后缀标识',
        'reason': 'ViewModel类使用了VM简写后缀，不符合统一命名规范',
        'fix': '将VM简写改为完整的ViewModel后缀'
    },
    {
        'name': 'ViewModel类缺少统一后缀',
        'level': '警告',
        'pattern': r'public class (?!\w+ViewModel)\w+ extends (ViewModel|AndroidViewModel|BaseViewModel)|class (?!\w+ViewModel)\w+ : (ViewModel|AndroidViewModel|BaseViewModel)',
        'violation': '《一、Android命名规范.md》第185条：ViewModel类以ViewModel作为后缀标识',
        'reason': 'ViewModel类没有添加ViewModel后缀，命名不符合规范',
        'fix': '类名末尾添加ViewModel后缀'
    },
    # Activity命名检查
    {
        'name': 'Activity类禁止使用Act简写后缀',
        'level': '警告',
        'pattern': r'public class \w+Act extends|class \w+Act :',
        'violation': '《一、Android命名规范.md》第180条：Activity类以Activity作为后缀标识',
        'reason': 'Activity类使用了Act简写后缀，不符合统一命名规范',
        'fix': '将Act简写改为完整的Activity后缀'
    },
    {
        'name': 'Activity类缺少统一后缀',
        'level': '警告',
        'pattern': r'public class (?!\w+Activity)\w+ extends (Activity|AppCompatActivity|ComponentActivity|BaseActivity)|class (?!\w+Activity)\w+ : (Activity|AppCompatActivity|ComponentActivity|BaseActivity)',
        'violation': '《一、Android命名规范.md》第180条：Activity类以Activity作为后缀标识',
        'reason': 'Activity类没有添加Activity后缀，命名不符合规范',
        'fix': '类名末尾添加Activity后缀'
    },
    # Fragment命名检查
    {
        'name': 'Fragment类禁止使用Frag简写后缀',
        'level': '警告',
        'pattern': r'public class \w+Frag extends|class \w+Frag :',
        'violation': '《一、Android命名规范.md》第182条：Fragment类以Fragment作为后缀标识',
        'reason': 'Fragment类使用了Frag简写后缀，不符合统一命名规范',
        'fix': '将Frag简写改为完整的Fragment后缀'
    },
    {
        'name': 'Fragment类缺少统一后缀',
        'level': '警告',
        'pattern': r'public class (?!\w+Fragment)\w+ extends (?!FragmentPagerAdapter|FragmentStatePagerAdapter)(Fragment|DialogFragment|BaseFragment)|class (?!\w+Fragment)\w+ : (?!FragmentPagerAdapter|FragmentStatePagerAdapter)(Fragment|DialogFragment|BaseFragment)',
        'violation': '《一、Android命名规范.md》第182条：Fragment类以Fragment作为后缀标识',
        'reason': 'Fragment类没有添加Fragment后缀，命名不符合规范',
        'fix': '类名末尾添加Fragment后缀'
    },

    # ==================== 三、Android编码规范 ====================
    # 禁止使用System.out.println
    {
        'name': '禁止使用System.out.println输出日志',
        'level': '警告',
        'pattern': r'System\.out\.println|System\.err\.println',
        'violation': '《三、Android编码规范.md》第56条：禁止使用System.out输出日志',
        'reason': 'System.out.println没有日志级别控制，生产环境无法关闭，会泄露敏感信息',
        'fix': '使用LogUtils.d/e/i/w替代System.out.println'
    },
    # 禁止硬编码字符串
    {
        'name': '禁止直接硬编码字符串',
        'level': '建议',
        'pattern': r'Toast\.makeText\(.*,".*"\)|Snackbar\.make\(.*,".*"\)',
        'violation': '《三、Android编码规范.md》第78条：字符串资源需统一放在strings.xml中',
        'reason': '直接硬编码字符串不利于国际化和统一管理',
        'fix': '使用getResources().getString(R.string.xxx)替代硬编码字符串'
    },
    # 线程池使用检查
    {
        'name': '禁止直接new Thread创建线程',
        'level': '警告',
        'pattern': r'new Thread\(|new Runnable\(',
        'violation': '《八、进程、线程与消息通信.md》第34条：统一使用线程池管理线程',
        'reason': '直接new Thread会导致线程无节制创建，无法统一管理，容易造成内存泄漏',
        'fix': '使用项目统一封装的ThreadPoolExecutor或Coroutine替代'
    },

    # ==================== 八、Android应用安全开发规范 ====================
    # WebView安全检查
    {
        'name': 'WebView未禁用JavaScriptInterface风险',
        'level': '严重',
        'pattern': r'setJavaScriptEnabled\(true\)',
        'violation': '《八、Android应用安全开发规范.md》第123条：WebView需严格控制JavaScript权限',
        'reason': '开启JavaScript且未正确配置接口会导致远程代码执行漏洞',
        'fix': '不需要JS交互时设置setJavaScriptEnabled(false)，需要时需对JS接口做安全校验'
    },
    # 明文存储敏感信息
    {
        'name': '禁止明文存储敏感信息到SharedPreferences',
        'level': '严重',
        'pattern': r'putString\(".*password.*"|putString\(".*token.*"|putString\(".*secret.*"',
        'violation': '《八、Android应用安全开发规范.md》第89条：敏感信息需加密存储',
        'reason': 'SharedPreferences明文存储密码、token等敏感信息会导致信息泄露',
        'fix': '使用加密存储方案，如EncryptedSharedPreferences或项目统一的安全存储工具'
    },

    # ==================== 模块专项检查规则 ====================
    # Event目录专项检查
    {
        'name': 'Event类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Event)\w+.*{|class (?!\w+Event)\w+.*{',
        'violation': '《一、Android命名规范.md》第187条：事件类以Event作为后缀标识',
        'reason': '该类放在event目录下，属于EventBus事件类，命名不符合规范',
        'fix': '类名末尾添加Event后缀',
        'path_filter': '/event/'
    },

    # 适配器类专项检查（不基于目录，基于继承关系）
    {
        'name': '适配器类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Adapter)\w+ extends (RecyclerView\.Adapter|BaseAdapter|PagerAdapter|FragmentPagerAdapter|FragmentStatePagerAdapter)|class (?!\w+Adapter)\w+ : (RecyclerView\.Adapter|BaseAdapter|PagerAdapter|FragmentPagerAdapter|FragmentStatePagerAdapter)',
        'violation': '《一、Android命名规范.md》第195条：适配器类以Adapter作为后缀标识',
        'reason': '该类是适配器类，继承了Adapter相关父类，命名不符合规范',
        'fix': '类名末尾添加Adapter后缀',
    },
    # ViewHolder专项检查
    {
        'name': 'ViewHolder类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!(ViewHolder|\w+ViewHolder))\w+ extends RecyclerView\.ViewHolder|class (?!(ViewHolder|\w+ViewHolder))\w+ : RecyclerView\.ViewHolder',
        'violation': '《一、Android命名规范.md》第202条：列表项ViewHolder类以ViewHolder作为后缀标识',
        'reason': '该类是RecyclerView的ViewHolder类，命名不符合规范',
        'fix': '类名末尾添加ViewHolder后缀，或者直接命名为ViewHolder',
    },

    # Helper目录专项检查
    {
        'name': '帮助类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Helper)\w+.*{|class (?!\w+Helper)\w+.*{',
        'violation': '《一、Android命名规范.md》第193条：帮助类以Helper作为后缀标识',
        'reason': '该类放在helper目录下，属于帮助类，命名不符合规范',
        'fix': '类名末尾添加Helper后缀',
        'path_filter': '/helper/'
    },

    # Manager目录专项检查
    {
        'name': '管理类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Manager)\w+.*{|class (?!\w+Manager)\w+.*{',
        'violation': '《一、Android命名规范.md》第192条：管理类以Manager作为后缀标识',
        'reason': '该类放在manager目录下，属于管理类，命名不符合规范',
        'fix': '类名末尾添加Manager后缀',
        'path_filter': '/manager/'
    },

    # Constants目录专项检查
    {
        'name': '常量类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Constants?)\w+.*{|class (?!\w+Constants?)\w+.*{',
        'violation': '《一、Android命名规范.md》第194条：常量类以Constants作为后缀标识',
        'reason': '该类放在constants目录下，属于常量类，命名不符合规范',
        'fix': '类名末尾添加Constants后缀',
        'path_filter': '/constants/'
    },

    # Listener目录专项检查
    {
        'name': '监听器类命名不符合规范',
        'level': '警告',
        'pattern': r'public (class|interface) (?!\w+(Listener|Callback))\w+.*{|(class|interface) (?!\w+(Listener|Callback))\w+.*{',
        'violation': '《一、Android命名规范.md》第196条：监听器/回调类以Listener/Callback作为后缀标识',
        'reason': '该类放在listener目录下，属于监听器/回调类，命名不符合规范',
        'fix': '类名末尾添加Listener或Callback后缀',
        'path_filter': '/listener/'
    },

    # Implement目录专项检查
    {
        'name': '实现类命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Impl)\w+.*{|class (?!\w+Impl)\w+.*{',
        'violation': '《一、Android命名规范.md》第197条：接口实现类以Impl作为后缀标识',
        'reason': '该类放在implement目录下，属于接口实现类，命名不符合规范',
        'fix': '类名末尾添加Impl后缀',
        'path_filter': '/implement/'
    },

    # 网络API模块专项检查
    {
        'name': 'API接口类命名不符合规范',
        'level': '警告',
        'pattern': r'public (class|interface) (?!\w+Api)\w+.*{|(class|interface) (?!\w+Api)\w+.*{',
        'violation': '《一、Android命名规范.md》第198条：API接口类以Api作为后缀标识',
        'reason': '该类放在apis目录下，属于网络API接口类，命名不符合规范',
        'fix': '类名末尾添加Api后缀',
        'path_filter': '/apis/'
    },

    # 数据模型专项检查
    {
        'name': '请求数据模型命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Request)\w+.*{|class (?!\w+Request)\w+.*{',
        'violation': '《一、Android命名规范.md》第199条：请求数据模型以Request作为后缀标识',
        'reason': '该类放在request目录下，属于请求数据模型，命名不符合规范',
        'fix': '类名末尾添加Request后缀',
        'path_filter': '/request/'
    },
    {
        'name': '响应数据模型命名不符合规范',
        'level': '警告',
        'pattern': r'public class (?!\w+Response)\w+.*{|class (?!\w+Response)\w+.*{',
        'violation': '《一、Android命名规范.md》第200条：响应数据模型以Response作为后缀标识',
        'reason': '该类放在response目录下，属于响应数据模型，命名不符合规范',
        'fix': '类名末尾添加Response后缀',
        'path_filter': '/response/'
    },

    # 自定义View专项检查
    {
        'name': '自定义View命名不符合规范',
        'level': '警告',
        'pattern': r'public class \w+ extends (View|ViewGroup|TextView|ImageView|LinearLayout|RelativeLayout|ConstraintLayout)|class \w+ : (View|ViewGroup|TextView|ImageView|LinearLayout|RelativeLayout|ConstraintLayout)',
        'violation': '《一、Android命名规范.md》第201条：自定义View需清晰标识组件类型',
        'reason': '自定义View类名没有明确标识组件类型，不符合命名规范',
        'fix': '类名添加对应组件标识（如AtourButton、RoundImageView等）',
        'path_filter': '/widget/'
    },

    # ==================== 高级检查规则 ====================
    # 不安全强制类型转换检查
    {
        'name': '不安全的强制类型转换风险',
        'level': '严重',
        'pattern': r'\sas\s(ArrayList|LinkedList|MutableList|HashMap)\??',
        'violation': '《三、Android 编码规范》类型安全相关要求',
        'reason': '直接强制转换集合类型，如果实际返回的是其他集合实现类，会出现类型转换异常导致崩溃',
        'fix': '使用安全的转换方式，如`arrayListOf(*it.toTypedArray())`或者修改接口定义明确返回类型',
    },

    # 包名小写规范检查
    {
        'name': '包名目录命名不规范',
        'level': '警告',
        'pattern': r'^package.*[A-Z].*$',
        'violation': '《一、Android命名规范》包命名规范（包名全部小写）',
        'reason': '包名/目录名中包含大写字母，不符合包名必须全部小写的规范',
        'fix': '将包名/目录名改为全小写，同时修改所有对应类的package声明',
    },

    # 旧网络请求方式检查
    {
        'name': '网络请求方式不统一',
        'level': '警告',
        'pattern': r'RetrofitManager\.createService|RetrofitUtils\.create',
        'violation': '项目网络迁移规范',
        'reason': '使用旧的RetrofitManager/RetrofitUtils方式创建网络服务，不符合项目最新的网络架构要求',
        'fix': '使用新的lib_network模块 + Hilt依赖注入方式，在ViewModel中通过@Inject注入Service实例',
    },

    # 模糊变量名检查
    {
        'name': '变量命名不清晰',
        'level': '警告',
        'pattern': r'private\s+(var|val)\s+(api|data|info|bean|obj|temp)\s*:',
        'violation': '《一、Android命名规范》变量命名规范',
        'reason': '变量名过于模糊，无法明确表示其用途和类型，不符合变量命名要清晰表达含义的要求',
        'fix': '修改为更有语义的变量名，如`couponService`、`userInfo`、`orderList`等',
    },
    # requireContext安全检查
    {
        'name': '使用requireContext()可能导致崩溃',
        'level': '严重',
        'pattern': r'requireContext\(\)',
        'violation': '《三、Android 编码规范.md》第一条：不得使用requireContext()，需对获取的context进行判空处理',
        'reason': 'requireContext()在context为空时会直接抛出IllegalStateException异常，当Fragment已经 detached但代码还在执行时会导致崩溃',
        'fix': '使用安全的context判空方式：`context?.let { safeContext -> ... }`',
    },
    # 方法小驼峰命名检查
    {
        'name': '方法命名不符合小驼峰规范',
        'level': '警告',
        'pattern': r'(fun|Observable|Single|Call)\s+[A-Z]\w*\(',
        'violation': '《一、Android命名规范.md》方法命名规范：小驼峰命名法，动词开头',
        'reason': '方法名首字母大写，不符合小驼峰命名规范',
        'fix': '改为小驼峰命名，首字母小写',
    }
]

class CodeReviewer:
    def __init__(self, target):
        self.target = target
        self.issues = []
        self.total_files = 0
        self.scanned_files = 0

    def is_code_file(self, filename):
        return filename.endswith(CODE_EXTENSIONS)

    def scan_file(self, file_path):
        self.scanned_files += 1
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for rule in RULES:
                    # 路径过滤：如果规则有path_filter，只有路径匹配才检查（兼容Windows路径）
                    if 'path_filter' in rule:
                        # 统一转换为斜杠分隔
                        normalized_path = file_path.replace('\\', '/')
                        if rule['path_filter'] not in normalized_path:
                            continue

                    if re.search(rule['pattern'], line):
                        # 特殊检查：事件类必须在event包下
                        if rule['name'] == 'Event事件类命名不符合规范' and '/event/' not in file_path:
                            continue

                        self.issues.append({
                            'rule': rule,
                            'file': rel_path,
                            'line': line_num,
                            'code': line.strip()
                        })
        except Exception as e:
            print(f"扫描文件 {file_path} 出错: {e}")

    def scan_directory(self, dir_path):
        for root, dirs, files in os.walk(dir_path, topdown=True):
            # 从dirs中过滤掉要排除的目录，os.walk不会遍历这些目录，彻底排除
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if self.is_code_file(file):
                    file_path = os.path.join(root, file)
                    self.scan_file(file_path)
                    self.total_files += 1

    def generate_report(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_issues = len(self.issues)
        warning_count = len([i for i in self.issues if i['rule']['level'] == '警告'])
        suggestion_count = len([i for i in self.issues if i['rule']['level'] == '建议'])
        critical_count = total_issues - warning_count - suggestion_count

        report_content = f"""# Android 全量代码审查报告
## 基本信息
- 审查对象：{self.target if self.target != 'all' else f'整个亚朵生活Android项目（共{self.total_files}个代码文件）'}
- 审查时间：{now}
- 总问题数：{total_issues}
- 严重问题：{critical_count}
- 警告问题：{warning_count}
- 建议优化：{suggestion_count}

## 问题详情
"""

        for idx, issue in enumerate(self.issues, 1):
            rule = issue['rule']
            report_content += f"""### {idx}. [{rule['level']}] {rule['name']}
- **位置**：{issue['file']}:{issue['line']}
- **问题代码**：
```java
{issue['code']}
```
- **违反规范**：{rule['violation']}
- **问题原因**：{rule['reason']}
- **修改建议**：{rule['fix']}

"""

        # 保存报告
        if self.target == 'all':
            report_name = 'peakmain_project_full_cr.markdown'
        else:
            file_basename = os.path.basename(self.target).split('.')[0]
            report_name = f'peakmain_{file_basename}_cr.markdown'

        with open(report_name, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✅ 审查完成，报告已生成：{report_name}")
        print(f"📊 统计：扫描了{self.total_files}个文件，发现{total_issues}个问题")

    def run(self):
        print(f"🚀 开始代码审查，目标：{self.target}")

        if self.target == 'all':
            self.scan_directory(PROJECT_ROOT)
        else:
            target_path = os.path.abspath(self.target)
            if os.path.isfile(target_path) and self.is_code_file(target_path):
                self.scan_file(target_path)
                self.total_files = 1
            elif os.path.isdir(target_path):
                self.scan_directory(target_path)
            else:
                print(f"❌ 无效的目标路径：{self.target}")
                sys.exit(1)

        self.generate_report()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python cr_scan.py <目标路径/all>")
        print("示例：")
        print("  python cr_scan.py all                # 审查整个项目")
        print("  python cr_scan.py app/src/main/       # 审查app模块")
        print("  python cr_scan.py MainActivity.kt     # 审查单个文件")
        sys.exit(1)

    reviewer = CodeReviewer(sys.argv[1])
    reviewer.run()