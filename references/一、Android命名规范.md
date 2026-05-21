## 单层项目架构
+ 一个Activity有多个Fragment，每个Fragment建立一个目录进行管理

```plain
├── apis                        // 网络模块
│   ├── service                 // API接口服务（封装网络请求）
│   └── response                // 网络请求的响应数据模型（如果较复杂的话）
│
├── main                        // 首页模块
│   ├── firstpage               // 预订页相关
│   │   ├── adapter             // - 适配器
│   │   ├── event               // - EventBus相关
│   │   ├── helper              // - 帮助类，数据处理相关
│   │   ├── manager             // - 管理类，视图管理、UI相关
│   │   └── viewmodel           // - ViewModel相关
│   │   └── constants           // - 预订页相关常量
│   │   └── listener            // - 事件处理相关
│   ├── journeyhelper           // 行程助手
│   ├── mine                    // 我的模块
│   └── activity        				// activity相关
│
├── login                       // 登录模块
│   ├── activity                // - 登录页面相关（如LoginActivity）
│   ├── adapter                 // - 登录页面适配器
│   ├── event                   // - 登录模块的EventBus相关
│   ├── helper                  // - 登录模块的辅助工具类
│   ├── manager                 // - 登录相关UI管理类
│   └── viewmodel               // - 登录模块的ViewModel
│   └── implement               // - 接口/抽象类的实现类
│
├── hotel                       // 酒店模块
│   ├── list                    // - 酒店列表
│   ├── detail                  // - 酒店详情
│   └── manager                 // - 酒店相关的UI管理类
│
├── order                       // 订单模块
│   ├── list                    // - 订单列表
│   ├── detail                  // - 订单详情
│   ├── manager                 // - 订单列表、详情页共有管理类
│   ├── viewmodel               // - 订单列表、详情页共有viewModel
│   └── helper                  // - 订单列表、详情页共有帮助类
│
├── coupon                      // 优惠券模块
│   ├── list                    // - 优惠券列表相关
│   ├── detail                  // - 优惠券详情相关
│   └── helper                  // - 优惠券列表、详情页共有帮助类
│
├── webview                      // H5模块
│   ├── handle                   // - 老的H5协议相关
│   ├── newhandle                // - 新的H5协议相关
│
├── common                      // 通用模块
│   ├── manager                 // 通用组件的管理类（如全局UI、全局管理）
│   ├── helper                  // 通用组件的帮助类（如数据处理）
│   ├── widget                  // 自定义组件
│   ├── constants               // 常量
│   ├── viewmodel               // 通用的ViewModel（如应用状态、用户信息等）
│   ├── utils                   // 工具类（如日期、网络、文件处理等通用工具）
│   └── network                 // 网络请求模块（如网络层封装，HTTP工具等）
│
│
├── models                      // 数据模型
│   └── journeyhelper           // 行程助手模块
│   │		└── request             // - 请求数据模型
│   │		└── body                // - 请求数据body模型
│   │		└── response            // - 响应数据模型
│   │		└── bean                // - 其他数据模型
│   │		└── enums               // - 枚举数据模型
│   │		└── interfaces          // - 接口数据模型
│   │		└── parmas              // - 参数数据模型
│   └── login                   // 登录模块
│
```

+ 目录名要小写，类名第一个字母大写
+ 所有数据实体类放到models目录下
    - 所有的请求数据模型放到request目录下
    - 所有的响应数据模型(后台返回结果)放到response目录下
    - 其他数据模型(和网络无关的)放到bean
    - 和无网络无关的请求参数放到parmas
+ 通用常量类放到common->constants目录下,某个模块下的放到对应目录下的constants
    - 如预订相关的requestCode，就放到firstpage目录下的constants中
+ 通用manager放到common->manager目录下,某个模块下的放到对应目录下的manager

## request、response、bean、body和response如何选择
### params（参数数据模型）
+ `params` 主要用于封装 **请求中的参数**。这些参数通常是客户端发送到服务器的请求中所需要的输入数据。`params` 通常用于网络请求中作为请求体、URL 参数或请求头中的数据
+ `**params**` 是请求中携带的参数，通常是构建 `**body**` 的一部分
+ 用于客户端向服务器传递参数，通常是函数或 API 调用时传递的参数数据模型

```kotlin
data class LoginParams(
    val username: String,
    val password: String
)
```

### **request**（请求数据模型）
+ `request` 主要表示 **整个请求的封装**，它不仅包含了参数数据，还可能包含额外的请求信息（如请求头、请求类型等）
+ `request` 对象通常是请求的数据载体，包含了发送请求时所需的所有信息。
+ 用于表示 API 请求的完整结构，通常用于通过 HTTP 请求发送到服务器。`request` 可能会包含请求方法、URL、请求头等信息。

```kotlin
data class LoginRequest(
    val params: LoginParams,  // 请求参数
    val header: RequestHeader // 请求头
)
```

### body模型
+ **Request 中的 body**：`request` 对象的 `body` 通常指的是请求数据部分。
+ 例如，登录请求的 `body` 就是包含用户名和密码的 JSON 数据（如 `params` 或 `request` 模型中的数据）。
+ 它可以是一个嵌套的对象，包含多个字段，表示要发送的完整数据结构

```kotlin
data class LoginRequestBody(
    val username: String,
    val password: String
)

data class LoginRequest(
    val body: LoginRequestBody
)
```

+ `**params**` 是请求中携带的参数，通常是构建 `**body**` 的一部分
+ `**request**` 是封装整个请求的结构，包含 `**body**`。
+ `**response**` 是服务器返回的结构，`body` 是响应数据部分。

### **response**（响应数据模型）
+ `response` 是用来封装 **从服务器返回的响应数据**。它通常包含状态码、响应消息、以及实际的数据部分。响应模型的设计需要反映服务器返回的完整结构，包括可能的错误信息或数据。
+ 用于表示服务器响应的数据结构。通常是 API 请求返回的数据模型

```kotlin
data class LoginResponse(
    val success: Boolean,
    val user: User?,
    val errorMessage: String?
)
```

### **bean**（实体数据模型）
+ `bean` 是 **数据实体模型**，它通常表示系统中使用的核心业务对象
+ 与 `params` 和 `request` 不同，`bean` 更加通用，可能表示数据库实体、展示对象或核心业务对象
+ 用于表示系统中的核心实体，通常没有特定的 API 请求或响应结构。可以在请求、响应、数据库或其他地方使用

```kotlin
data class User(
    val id: Long,
    val name: String,
    val email: String
)
```

## manager、utils和helper如何选择
+ utils：通用的并且无状态的，所有方法通常都是 **静态的**
+ manager：所有涉及到**View相关**或者**全局配置**的，都用manager
+ helper：所有涉及到**数据处理、转换** 或 **复杂计算** 的任务，都用helper

## 命名规范
### 总体命名规范
+ **统一性**：项目中命名使用统一的风格，尽量避免混乱和不一致的命名方式。
+ **简洁与可读性**：命名尽量简洁，并能清晰表达变量、类、方法等的用途。
+ **驼峰式命名法（CamelCase）**：类名、方法名、属性名等都使用驼峰式命名。
+ **常量使用全大写**：常量、静态变量使用大写字母，并用下划线分隔单词。
+ **缩写与简写**：尽量避免使用不常见的缩写，除非它们是广泛接受的（如URL、JSON等）。

### 类命名规范
+ 类名首字母大写，使用驼峰命名法。
+ 类名应描述类的作用或用途，避免使用过于抽象或模糊的名称

| 类 | 描述 | 例如 |
| :---: | :---: | :---: |
| Activity类 | Activity作为后缀标识 | HotelListActivity、MainActivity |
| Fragment类 | Fragment作为后缀标识 | HomeFragment、MineFragement |
| Service类 | 以Service作为后缀标识 | DownloadSevice |
| BroadcastReceive类 | 以Receive作为后缀标识 | DownloadReceive |
| ContentProvider 类 | 以Provider作为后缀标识 | PushProvider |
| Adapter类 | Adapter作为后缀标识 | HotelListAdapter |
| 解析类 | Parser作为后缀标识 | HomeParser |
| 工具方法类 | Utils或者Manager作为后缀标识 | PkPermissionUtils |
| 数据库 | 以DBHelper作为后缀标识 | MebDbHelper |
| 抽象类 | Base/Abstract开头 | BaseActivity |
| ViewModel类 | ViewModel作为后缀标识 | HomeViewModel |
| 常量类 | Constants作为后缀标识 | UserConstants |
| 接口 | I开头/able/ible结尾 | IHomeView、Runnable |
| 事件类 | Event/EventBus作为后缀标识 | LoginEventBus |
| 网络接口相关 | Service后缀 | HotelService |
| request目录 | Request作为后缀标识 | HomeRequest |
| response目录 | Response作为后缀标识 | MarketingConfigResponse |
| bean目录 | Bean作为后缀标识 | LoginBean |
| Hilt 模块 | Module 作为后缀标识 | NetworkModule |
| 扩展函数 | Exit 作为后缀标识 | StringExt、ViewExt |




### 方法命名规范
#### 基本规则
+ **小驼峰命名法**（camelCase）
+ **动词**或**动词短语**开头
+ 清晰表达方法意图，方法名应自解释

#### 动词前缀
| 动词前缀 | 用途 | 示例 |
| --- | --- | --- |
| get/set | 获取/设置属性 | getUser()、setName() |
| is/has/can | 返回布尔值 | isValid()、hasData() |
| load | 加载数据 | loadData()、loadMore() |
| fetch | 网络/异步获取 | fetchUserInfo() |
| save | 保存 | saveData() |
| delete/remove | 删除 | deleteItem() |
| update | 更新 | updateUi() |
| init/setup | 初始化 | initView()、setupListener() |
| show/hide | 显示/隐藏 | showLoading()、hideDialog() |
| navigate/goTo | 页面跳转 | navigateToDetail() |
| handle/on | 处理事件 | handleEvent()、onClick() |
| create | 创建对象 | createOkHttpClient() |
| build | 构建 | buildRetrofit() |
| convert/transform | 转换 | convertToDto() |
| validate | 校验 | validateInput() |




#### 生命周期方法
直接使用 Android 标准命名：

```kotlin
override fun onCreate(savedInstanceState: Bundle?) { ... }
override fun onViewCreated(view: View, savedInstanceState: Bundle?) { ... }
override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) { ... }
```

#### 回调方法
+ on 前缀 + 事件名

```kotlin
fun onItemClick(position: Int) { ... }
fun onSuccess(data: T) { ... }
fun onError(throwable: Throwable) { ... }
fun onLoadingChanged(isLoading: Boolean) { ... }
```

#### 扩展方法（Kotlin）
+ 直接描述功能，Receiver 类型隐含在方法名中

```kotlin
fun String.md5(): String { ... }              // "123".md5()
fun View.gone() { ... }                        // view.gone()
fun Int.dpToPx(): Int { ... }                  // 16.dpToPx()
fun Context.toast(message: String) { ... }     // context.toast("hello")
```

### **变量命名规范**
#### 基本规则
| 类型 | 命名规则 | 示例 |
| --- | --- | --- |
| 成员变量 | 小驼峰（camelCase） | userName、adapter |
| 常量 | 全大写下划线分隔 | MAX_SIZE、BASE_URL |
| 静态变量 | 全大写下划线分隔 | DEFAULT_TIMEOUT |
| 布尔值 | is/has/can 前缀 | isLoading、hasError、canEdit |


#### Kotlin 成员变量
```kotlin
class UserViewModel : ViewModel() {
    private val _userState = MutableStateFlow<UserState>(...)  // 内部可变变量，下划线前缀
    val userState: StateFlow<UserState> = _userState           // 对外暴露不可变变量
    
    private var currentPage = 0                                // ✅
    private val isLoading = MutableLiveData<Boolean>()         // ✅
}
```

#### Java 成员变量（Android 传统风格）
```java
public class BaseActivity {
    protected int mLayoutId;           // m 前缀，非公开，非静态
    private String mTitle;             // ✅
    public static final int CONSTANT = 1;  // 全大写
}
```

#### 特殊前缀规则
| 前缀 | 用途 | 示例 |
| --- | --- | --- |
| m | Java 私有/保护成员变量 | mContext、mAdapter |
| s | Java 静态成员变量 | sInstance |
| _ | Kotlin 内部可变变量 | _uiState、_data |
| k | Kotlin 伴生对象常量 | 不推荐，直接用全大写 |


#### 集合变量
+ 复数形式或 List/Map/Set 后缀
+ 优先使用说明性名称

```kotlin
val users: List<User> = emptyList()              // ✅
val userList: List<User> = emptyList()           // ✅
val userMap: Map<String, User> = emptyMap()      // ✅
val userItems = mutableListOf<User>()            // ✅
```

#### 变量命名禁忌
+ ❌ 避免单字符变量名（循环变量 `i`、`j` 除外）
+ ❌ 避免拼音命名（除非是特定业务术语，如 `yaduo`）
+ ❌ 避免模糊名称：data、info、bean
+ ✅ 推荐：userData、orderInfo、hotelBean



### 接口命名规范
#### 基本规则
+ **大驼峰命名法**
+ **名词**或**形容词**（描述能力）
+ **不推荐**使用 `I` 前缀（如 IUserManager），现代 IDE 已能区分

#### 常见接口类型
##### 能力接口（形容词）
```kotlin
interface Clickable { ... }
interface Parcelable { ... }
interface Serializable { ... }
interface Initializable { ... }
interface Disposable { ... }
```

##### 行为接口（动词 + able）
```kotlin
interface Observer<T> { ... }
interface Callback<T> { ... }
interface Provider<T> { ... }
interface Factory<T> { ... }
```

##### 业务接口
```kotlin
interface UserApiService { ... }
interface OrderRepository { ... }
interface ImageLoader { ... }
```

##### Retrofit API 接口
+ 模块名 + Service 后缀
+ 一个接口对应一个业务模块的 API

```kotlin
// ✅ 正确示例
interface MineService {                  // 我的模块 API
    @GET("api/member/info")
    suspend fun fetchMemberData(): Response<MemberData>
    
    @GET("api/member/cards")
    suspend fun fetchUserMagicCards(): Response<List<UserMagicCard>>
}

interface HotelService { ... }           // 酒店模块 API
interface OrderService { ... }           // 订单模块 API

// ❌ 避免
interface ApiService { ... }             // 太泛，不知道哪个模块
interface MineApi { ... }                // 不统一，建议用 Service 后缀
```

### 泛型命名规范
#### 标准单字母
| 字母 | 含义 | 用途 |
| --- | --- | --- |
| `T` | Type | 通用类型 |
| `E` | Element | 集合元素 |
| `K` | Key | Map 键 |
| `V` | Value | Map 值 |
| `R` | Result | 返回结果 |
| `S` | Second | 第二个类型参数 |
| `U` | Third | 第三个类型参数 |
| `X` | Exception | 异常类型 |


#### 多参数示例
```kotlin
// 2个参数
interface Pair<K, V> {
    fun getKey(): K
    fun getValue(): V
}

// 3个参数
fun <T1, T2, R> combine(t1: T1, t2: T2, transform: (T1, T2) -> R): R { ... }

// 描述性多字符参数名（复杂场景）
interface <RepoT, ViewModelT, StateT> BaseContract { ... }
```

### 特殊类命名
+ 实现类以 Impl 结尾
+ 接口名不加前缀

```kotlin
interface UserRepository { ... }
class UserRepositoryImpl : UserRepository { ... }  // ✅
class IUserRepository { ... }                       // ❌ 不推荐匈牙利标记法
```

#### 抽象类
+ 可以 `Base` 或 `Abstract` 开头，优先 `Base`

```kotlin
abstract class BaseActivity : AppCompatActivity() { ... }  // ✅
abstract class AbstractDataHandler { ... }                  // ✅
```

#### 单例类
+ 与普通类相同，通过 object（Kotlin）或静态方法实现，不加特殊前缀

```kotlin
object SingletonManager { ... }  // Kotlin
public class Singleton {         // Java
    private static Singleton instance;
}
```

### **layout文件命名规范**
app 的 module 都可移除 module(app) 前缀

| layout文件 | 例如 |
| --- | :---: |
| Activity 的 layou t以 module_activity 开头 | activity_main、ui_activity_login |
| Fragment 的 layout 以 module_fragment 开头 | fragment_home、ui_fragment_permission |
| Dialog 的 layout 以 module_dialog 开头 | dialog_share、ui_dialog_tip |
| include 的 layout 以 module_include 开头 | include_header、ui_include_header |
| ListView 的行 layout 以 module_list_item 开头 | list_item_hotel、ui_list_item_hotel |
| RecyclerView 的 item layout 以 module_recycle_item 开头 | recycle_item_hotel、ui_recycle_item_hotel |
| 多级嵌套的RecyclerView的item_layout以module_recycle_item_level | 一级：recycle_item_home   二级:假设你的二级RecyclerView显示商品的列表,可以命名：recylce_item_home_product   三级：假设你的三级RecyclerView显示商品的分类，可以命名：recycle_item_home_product_category |
| GridView 的 item layout 以 module_grid_item 开头 | grid_item_home、ui_grid_item_home |


### <font style="color:rgb(37, 41, 51);">anim 资源</font>
+ <font style="color:rgb(37, 41, 51);">anim 资源名称以小写单词+下划线的方式命名,采用以下规则</font>
+ <font style="color:rgb(37, 41, 51);">模块名_逻辑名称_[方向|序号]</font>
+ <font style="color:rgb(37, 41, 51);">Tween 动画（使用简单图像变换的动画，例如缩放、平移）资源</font>
    - <font style="color:rgb(37, 41, 51);">尽可能以通用的动画名称命名</font>
    - <font style="color:rgb(37, 41, 51);">如 module_fade_in , module_fade_out , module_push_down_in (动画+方向)</font>
+ <font style="color:rgb(37, 41, 51);">Frame 动画（按帧顺序播放图像的动画）资源</font>
    - <font style="color:rgb(37, 41, 51);">尽可能以模块+功能命名+序号</font>
    - <font style="color:rgb(37, 41, 51);">如：module_loading_grey_001</font>

### <font style="color:rgb(37, 41, 51);">color资源</font>
+ <font style="color:rgb(37, 41, 51);">一般公司颜色资源都是固定的那几套</font>
+ <font style="color:rgb(37, 41, 51);">color资源是以#AARRGGBB为格式，写入module_colors.xml中，所以使用命名可以使用格式</font>
    - <font style="color:rgb(37, 41, 51);">module_color_RRGGBB_透明度</font>
        * <font style="color:rgb(37, 41, 51);">如：</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);"><color name="color_272a2b">#272a2b</color></font>
    - <font style="color:rgb(37, 41, 51);">或module_颜色_透明度</font>
        * <font style="color:rgb(37, 41, 51);">如：</font><font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);"><color name="black_alpha_10">#1A000000</color></font>

### <font style="color:rgb(37, 41, 51);">dimen 资源</font>
<font style="color:rgb(37, 41, 51);">以dimen_数字为格式，写入module_colors.xml</font>

+ <font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);"><dimen name="dimen_0_5">0.5dp</dimen></font>
+ <font style="color:rgb(255, 80, 44);background-color:rgb(255, 245, 245);"><dimen name="dimen_1">1dp</dimen></font>

### <font style="color:rgb(37, 41, 51);">string资源文件</font>
<font style="color:rgb(37, 41, 51);">string资源文件或者文本用到字符需要全部写入module_strings.xml文件中，字符串以小写单词+下划线的方式命名，采用以下规则</font>

+ <font style="color:rgb(37, 41, 51);">模块名+逻辑名称</font>
+ <font style="color:rgb(37, 41, 51);">如：module_login_tips</font>

### <font style="color:rgb(37, 41, 51);">id 资源</font>
<font style="color:rgb(37, 41, 51);">id 资源原则上以驼峰法命名，View 组件的资源 id 建议以 View 的缩写作为前缀</font>

**<font style="color:rgb(37, 41, 51);">常见缩写表</font>**

| <font style="color:rgb(37, 41, 51);">名称</font> | <font style="color:rgb(37, 41, 51);">缩写前缀</font> |
| --- | --- |
| <font style="color:rgb(37, 41, 51);">LinearLayout</font> | <font style="color:rgb(37, 41, 51);">ll</font> |
| <font style="color:rgb(37, 41, 51);">RelativeLayout</font> | <font style="color:rgb(37, 41, 51);">rl</font> |
| <font style="color:rgb(37, 41, 51);">ConstraintLayout</font> | <font style="color:rgb(37, 41, 51);">cl</font> |
| <font style="color:rgb(37, 41, 51);">ListView</font> | <font style="color:rgb(37, 41, 51);">lv</font> |
| <font style="color:rgb(37, 41, 51);">ScollView</font> | <font style="color:rgb(37, 41, 51);">sv</font> |
| <font style="color:rgb(37, 41, 51);">TextView</font> | <font style="color:rgb(37, 41, 51);">tv</font> |
| <font style="color:rgb(37, 41, 51);">Button</font> | <font style="color:rgb(37, 41, 51);">bt/btn</font> |
| <font style="color:rgb(37, 41, 51);">ImageView</font> | <font style="color:rgb(37, 41, 51);">iv</font> |
| <font style="color:rgb(37, 41, 51);">CheckBox</font> | <font style="color:rgb(37, 41, 51);">cb</font> |
| <font style="color:rgb(37, 41, 51);">RadioButton</font> | <font style="color:rgb(37, 41, 51);">rb</font> |
| <font style="color:rgb(37, 41, 51);">EditText</font> | <font style="color:rgb(37, 41, 51);">et</font> |
| <font style="color:rgb(37, 41, 51);">ShapeTextView</font> | <font style="color:rgb(37, 41, 51);">stv</font> |
| <font style="color:rgb(37, 41, 51);">ShapeLinearLayout</font> | <font style="color:rgb(37, 41, 51);">sll</font> |
| <font style="color:rgb(37, 41, 51);">ShapeConstraintLayout</font> | <font style="color:rgb(37, 41, 51);">scl</font> |


### drawable资源命名
| 类型前缀 | 模板示例 | 适用场景 |
| --- | --- | --- |
| `ic_` | ic_[模块名]_[功能描述] | 图标（icon），常用于 toolbar、tab、按钮、item 左右侧 |
| `bg_` | bg_[模块名]_[用途描述] | 背景图（background） |
| `btn_` | btn_[模块名]_[用途/状态描述] | 按钮背景（通常是 selector/shape） |
| `shape_` | shape_[用途/颜色/圆角/边框描述] | 形状（shape drawable，通常是圆角/边框/颜色背景） |
| `line_` | line_[横/竖]_用途描述 | 分割线（divider） |
| `selector_` | selector_[用途/状态描述] | 状态选择器 selector |
| `img_` | img_[模块名]_[用途/场景] | 内容图片、展示图片、空态图 |
| `list_` | list_[模块名]_[用途/状态描述] | 列表 item 背景 |


模块前缀对照表（业务模块建议）

| 模块 | 前缀示例 |
| --- | --- |
| 启动页 / Splash | splash |
| 登录模块 | login |
| 首页模块 | home |
| 用户中心 | profile / user_center |
| 商品模块 | goods / product |
| 订单模块 | order |
| 支付模块 | pay |
| 搜索模块 | search |
| 消息模块 | message |
| 设置模块 | settings |
| 公共（通用模块） | common |
| 活动/营销 | activity / marketing |


多状态命名规则

| 状态 | 后缀 |
| --- | --- |
| 默认状态 | `_normal`<br/>（可省略） |
| 按下状态 | `_pressed` |
| 禁用状态 | `_disabled` |
| 选中状态 | `_selected` |
| 焦点状态 | `_focused` |
| 选中已勾选 | `_checked` |
| 夜间模式 | `_night` |


