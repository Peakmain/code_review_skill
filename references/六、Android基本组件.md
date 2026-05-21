## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">Activity 间数据通信避免传递大对象</font>
### 原则：
+ Activity 之间进行数据传递时，**禁止通过 Intent + Parcelable / Serializable** 的方式传递大体积数据（如大型对象、图片字节流、集合、Map 等）。
+ 否则可能触发系统异常 `**TransactionTooLargeException**`，导致页面跳转失败或应用崩溃。

### 问题说明
Android 在进行进程间通信（Binder）时，对单次传输数据大小有严格限制（一般为 1MB）。

当使用以下方式传递大数据时，会触发异常：

```java
Intent intent = new Intent(context, DetailActivity.class);
intent.putExtra("userInfo", largeParcelableObject); // ⚠️ 大对象传输
startActivity(intent);
```

出现如下错误：

```java
android.os.TransactionTooLargeException
```

:::info
**典型触发场景：**

+ 通过 `Intent.putExtra()` 传递复杂对象或大量数据
+ 使用 `Bundle` 在 Activity 或 Fragment 之间传递过多数据
+ 保存过大的数据到 `onSaveInstanceState()`
+ 大量使用 Parcelable 对象作为参数传递

:::

### 推荐解决方案
| 场景 | 推荐方案 |
| --- | --- |
| 数据量小、轻量级参数 | 使用 Intent + Bundle 传递（如 ID、标识符） |
| 数据量大、对象复杂 | 使用全局数据缓存、ViewModel、EventBus、单例对象、Repository 等方案 |
| 跨进程通信 | 使用 AIDL 或 ContentProvider |
| 跨页面传递图片、文件等资源 | 仅传递路径或 URI，不直接传递字节流 |


### 正例
#### 使用 ViewModel / Repository 共享数据（推荐）
```java
// ViewModel 方式（推荐）
val sharedViewModel = ViewModelProvider(this)[SharedViewModel::class.java]
sharedViewModel.userInfo = largeUserObject

// 启动下一个页面
startActivity(Intent(this, DetailActivity::class.java))
```

#### 使用 EventBus 进行页面间事件传递
```java
// 发送方
EventBus.getDefault().postSticky(new UserEvent(largeUserObject));

// 接收方
@Subscribe(threadMode = ThreadMode.MAIN, sticky = true)
public void onUserEvent(UserEvent event) {
    User user = event.getUser();
}
```

#### 使用缓存或单例对象
```java
// 临时存储数据
DataCache.getInstance().put("userInfo", largeUserObject);

// 下一个页面读取
User user = DataCache.getInstance().get("userInfo");
```

### 反例
#### 不当使用 Parcelable：
```java
Intent intent = new Intent(context, DetailActivity.class);
intent.putExtra("user", largeParcelableObject); // 大对象传递
startActivity(intent);
```

#### 不当使用 Bundle：
```java
Bundle bundle = new Bundle();
bundle.putSerializable("list", largeList); // 集合过大
intent.putExtras(bundle);
```

### 总结
| 项目 | 建议 |
| --- | --- |
| 小数据 | 可用 Intent + Bundle |
| 大对象 | 避免 Parcelable，使用共享数据方式 |
| 图片/文件 | 仅传 URI / Path，不传 Bitmap / Byte[] |
| 临时数据 | 可放入单例或 Application 缓存 |
| 长期数据 | 建议存储至数据库或磁盘缓存 |


## <font style="color:#528135;">【推荐】</font>Activity 状态保存与数据持久化规范
`Activity#onSaveInstanceState()` 方法不是标准生命周期回调方法，系统并不保证在所有情况下都会调用。其设计初衷是为了在 **Activity 被系统意外销毁（如内存不足或配置变更）** 时，保存少量 **临时性 UI 状态数据**。

因此，使用时应遵循以下规范：

### 适用场景
仅用于保存 **短期、轻量的 UI 状态**，如：

+ EditText 的输入内容
+ ScrollView 的滚动位置
+ RecyclerView 的当前选中项
+ 临时选中状态（如 tab、checkbox 等）

---

### 不适用场景
**禁止** 使用 `onSaveInstanceState()` 保存：

+ 业务数据或大对象（如图片、列表、model对象等）
+ 需要长期保存或恢复的用户数据（如草稿、缓存、登录信息）
+ 复杂对象引用（如 Context、Handler、线程对象）

原因：

+ 系统序列化这些对象会导致 **TransactionTooLargeException** 或性能问题
+ Activity 被彻底销毁后，这些对象将无法恢复

---

### 正确做法
1. **UI临时数据 → **`**onSaveInstanceState()**`

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("input_text", editText.text.toString())
}
```

2. **业务数据或持久化内容 → **`**onPause()**`** / **`**onStop()**`

```kotlin
override fun onPause() {
    super.onPause()
    // 使用 DataStore / Room / SharedPreferences 等进行持久化保存
    saveDraftToLocal()
}
```

3. **大数据传递 → 使用 EventBus / ViewModel / 单例缓存**  
避免通过 `Intent.putExtra()` 传递大数据对象：

```kotlin
// ❌ 错误做法
intent.putExtra("userInfo", largeParcelableData)

// ✅ 推荐做法
EventBus.getDefault().postSticky(UserEvent(largeData))
```

---

### 总结
| 场景 | 推荐方法 | 说明 |
| --- | --- | --- |
| 临时 UI 状态 | `onSaveInstanceState()` | 轻量、短期恢复 |
| 长期业务数据 | `onPause()`/ `onStop()` | 持久化存储 |
| 大数据传递 | EventBus / ViewModel / 单例缓存 | 避免 Intent 传递 |




## <font style="color:#DF2A3F;">【强制】</font>禁止在 `Service#onStartCommand()` 或 `onBind()` 中执行耗时操作
+ Android 的 Service 组件默认运行在 **主线程（UI 线程）** 中，若在 onStartCommand() 或 onBind() 中直接执行耗时操作（如网络请求、文件读写、数据库操作等），会导致 **主线程阻塞**，从而引发 **ANR（Application Not Responding）** 或界面卡顿问题。
+ 因此，必须将耗时任务放入 **子线程** 或使用 **异步机制**（如 IntentService、HandlerThread、ThreadPoolExecutor 等）中执行。

### 正确示例（推荐做法）
#### 使用 `IntentService` 自动处理异步任务（推荐方案）
```java
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }

    public void startIntentService(View view) {
        Intent intent = new Intent(this, MyIntentService.class);
        startService(intent);
    }
}

public class MyIntentService extends IntentService {

    public MyIntentService() {
        super("MyIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        // 在子线程中执行耗时任务
        try {
            // 模拟耗时任务
            Thread.sleep(3000);
            Log.d("MyIntentService", "任务执行完成");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

🔹 **优点：**

+ 内部自动创建 **独立工作线程**，无需手动管理线程；
+ 每个任务会按顺序依次执行；
+ 任务执行完毕后会自动 **stopSelf()**，节省资源；
+ 不会阻塞主线程，安全可靠。

---

### 错误示例（反例）
```java
public class MyService extends Service {
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // ❌ 直接在主线程中执行耗时操作
        doSomeLongTask(); 
        return START_STICKY;
    }

    private void doSomeLongTask() {
        try {
            Thread.sleep(5000); // 模拟耗时操作
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

🔹 **问题分析：**

+ `onStartCommand()` 在主线程中执行；
+ 阻塞主线程导致应用无响应；
+ 极易触发 **ANR（5秒规则）**；
+ 同时影响应用 UI 响应能力。

---

### 其他替代方案
如果项目使用 **Kotlin + 协程** 或 **现代架构组件**，也可以考虑以下方案：

#### 使用协程异步处理
```kotlin
class MyService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        CoroutineScope(Dispatchers.IO).launch {
            // 执行耗时操作
            delay(3000)
            Log.d("MyService", "任务完成")
            stopSelf(startId)
        }
        return START_NOT_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
```

#### 使用线程池
```java
private final ExecutorService executor = Executors.newSingleThreadExecutor();

@Override
public int onStartCommand(Intent intent, int flags, int startId) {
    executor.execute(() -> {
        // 在后台线程中执行任务
        performLongTask();
        stopSelf(startId);
    });
    return START_NOT_STICKY;
}
```

### 总结规范
| 规范项 | 要求 |
| --- | --- |
| 不可做的事 | 不得在 `onStartCommand()`/ `onBind()`中执行耗时操作 |
| 推荐做法 | 使用 `IntentService`、`HandlerThread` 或线程池执行任务 |
| 问题后果 | 造成主线程阻塞，引发 ANR、UI 卡顿或系统回收 |
| 适用场景 | 后台任务处理、上传/下载、数据同步等操作 |


### 为什么 IntentService 在 Android 8.0 以后被 JobIntentService 取代
#### 背景
在 **Android 8.0（API 26）** 中，Google 对后台执行策略进行了重大调整，引入了严格的 **后台执行限制（Background Execution Limits）**。=

其核心目标是：

> 限制应用在后台时的任意长时间运行，减少电量消耗、提升系统流畅度。
>

具体来说：

+ 当应用处于**后台（后台进程或后台 Service）**时，
    - Android **禁止**应用随意启动后台 `Service`。
+ 如果应用试图在后台调用 `startService()`，系统会抛出：

```java
IllegalStateException: Not allowed to start service Intent ...
```

这直接导致了传统的 `IntentService` 在 8.0 及以后系统上 **不再安全可用**。

#### IntentService 的局限性
`IntentService` 原本是个非常经典的异步任务执行类，它：

+ 在独立线程中顺序执行任务；
+ 执行完自动停止自身；
+ 避免了线程管理的复杂性。

但在 Android 8.0 后，它存在以下局限：

| 问题 | 说明 |
| --- | --- |
| ❌ 无法在后台启动 | 当应用不在前台时调用 `startService()`会抛异常 |
| ❌ 无法保证任务执行 | 系统可能直接终止后台 Service |
| ❌ 无法与新后台调度机制（JobScheduler）集成 | 不支持条件调度（如网络状态、充电状态等） |


#### `JobIntentService` 的出现
为了解决上述问题，Google 推出了 `**JobIntentService**`—— 一个 **兼容旧版本 + 遵守后台执行限制** 的替代方案。

:::info
**设计目标**

+ 在 **Android 8.0+** 上自动使用 `JobScheduler`；
+ 在 **Android 8.0 以下** 仍然用老的 `IntentService` 机制；
+ 开发者无需关心 API 版本，使用方式与 `IntentService` 基本一致。

:::

#### JobIntentService 使用示例
```java
public class MyJobIntentService extends JobIntentService {

    public static void enqueueWork(Context context, Intent work) {
        enqueueWork(context, MyJobIntentService.class, 1000, work);
    }

    @Override
    protected void onHandleWork(@NonNull Intent intent) {
        // 后台线程中执行任务
        Log.d("MyJobIntentService", "执行后台任务: " + intent);
    }
}
```

调用方式：

```java
Intent work = new Intent();
work.putExtra("task", "sync_data");
MyJobIntentService.enqueueWork(context, work);
```

:::info
**特点：**

+ `enqueueWork()` 代替了传统的 `startService()`；
+ 系统会自动判断使用哪种执行机制：
    - Android < 8.0 → 启动普通 Service；
    - Android ≥ 8.0 → 通过 `JobScheduler` 执行任务；
+ 任务自动在后台线程执行，不阻塞主线程；
+ 系统会在任务完成后自动结束。

:::

#### `JobIntentService` 与 `IntentService` 的对比
| 对比项 | IntentService | JobIntentService |
| --- | --- | --- |
| 启动方式 | `startService()` | `enqueueWork()` |
| 后台限制 | ❌ 8.0 后无法后台启动 | ✅ 兼容 8.0 后台限制 |
| 任务线程 | 独立工作线程 | 独立线程（内部封装） |
| 自动停止 | ✅ | ✅ |
| 任务调度 | ❌ 不支持 | ✅ 集成 `JobScheduler` |
| 系统兼容性 | Android < 8.0 | Android 全版本 |


#### 未来趋势与替代方案
`JobIntentService` 是一个过渡解决方案，在 **Android Jetpack** 体系中，Google 后续推荐开发者优先使用更现代的方案：

| 替代方案 | 说明 |
| --- | --- |
| ✅ **WorkManager** | 推荐方案，支持任务约束、重试、持久化执行，完全替代 `JobIntentService` |
| 🔹 **JobScheduler** | 原生系统任务调度 API，适用于系统级任务 |
| 🔹 **ForegroundService** | 适用于需要用户感知的长期任务（如下载、导航） |


#### 总结规范
| 规范项 | 推荐方案 |
| --- | --- |
| Android < 8.0 | 可使用 `IntentService` |
| Android 8.0+ | 使用 `JobIntentService`或 `WorkManager` |
| 长期后台任务 | 使用 `ForegroundService` |
| 定时、重试、条件任务 | 使用 `WorkManager` |
| 临时后台轻任务 | 可继续使用 `JobIntentService` |


## <font style="color:#DF2A3F;">【强制】</font>禁止通过隐式广播发送敏感信息
在 Android 中，使用 **Context#sendBroadcast()** 发送隐式广播时，系统会将广播分发给 **所有注册了匹配 IntentFilter 的应用**。

如果广播中包含敏感数据（如密码、IP、端口、用户信息等），则可能被 **恶意应用接收**，造成信息泄漏或安全隐患。

### 问题说明
1. **隐式广播被所有应用接收**

```java
Intent intent = new Intent();
intent.setAction("com.sample.action.server_running");
intent.putExtra("local_ip", localIp);
intent.putExtra("port", port);
intent.putExtra("code", pwd);
context.sendBroadcast(intent); // ❌ 发送敏感信息
```

+ 任意注册了 `"com.sample.action.server_running"` 的第三方应用都可以收到该广播；
+ 恶意应用可能 **拦截、修改或丢弃广播**。

****

2. **有序广播的风险**

使用 `**sendOrderedBroadcast()**` 时：

+ 高优先级的恶意 Receiver 可以 **丢弃广播**，导致服务不可用；
+ 或 **篡改广播数据**，向结果注入恶意信息。



### 正确做法（推荐）
如果广播仅限应用内部使用，应使用 `**LocalBroadcastManager**`，避免跨应用泄漏：

```java
Intent intent = new Intent("my-sensitive-event");
intent.putExtra("event", "this is a test event");

// 仅在本应用内部分发
LocalBroadcastManager.getInstance(this).sendBroadcast(intent);
```

优点：

+ 广播仅在应用内部传递，**外部应用无法接收**；
+ 提升安全性，防止敏感信息外泄；
+ 避免有序广播被恶意篡改。

---

### 反例
```java
Intent v1 = new Intent();
v1.setAction("com.sample.action.server_running");
v1.putExtra("local_ip", localIp);
v1.putExtra("port", port);
v1.putExtra("code", pwd);
v1.putExtra("connected", status);
context.sendBroadcast(v1); // ❌ 隐式广播发送敏感信息
```

潜在风险：

```java
final class MaliciousReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent != null && "com.sample.action.server_running".equals(intent.getAction())) {
            String ip = intent.getStringExtra("local_ip");
            String pwd = intent.getStringExtra("code");
            int port = intent.getIntExtra("port", 0);
            boolean connected = intent.getBooleanExtra("connected", false);
            // 恶意应用获取敏感信息
        }
    }
}
```

---

### 规范总结
| 规范项 | 要求 |
| --- | --- |
| 敏感信息广播 | **禁止使用隐式广播**发送 |
| 应用内广播 | 使用 `LocalBroadcastManager` |
| 系统广播 | 如果必须使用全局广播，**避免传递敏感信息**，或使用权限保护 `<permission>` |
| 有序广播 | 避免发送关键任务数据，以防被拦截或篡改 |




**扩展建议**：

+ 对于真正需要跨应用通信的数据，使用 **绑定服务、ContentProvider、AIDL 或自定义权限**，确保数据安全。
+ 永远不要在 Intent 中传递密码、用户密钥或敏感配置信息。

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">Fragment 添加与 commit() 使用规范</font>
在 Android 中，Fragment 的状态管理依赖于 **Activity 生命周期**，如果在 **Activity 状态保存之后**调用 `FragmentTransaction.commit()`，可能导致 **IllegalStateException: commit after state saved** 或页面状态丢失。

因此，需要遵循以下规范：

### 核心原则
1. **不要随意使用 **`**commitAllowingStateLoss()**`
    - 该方法会忽略 Activity 状态保存时的异常，但可能导致 **UI 状态丢失**；
    - 只有在明确知道 **丢失此次 commit 不影响用户体验** 时，才能使用，并且必须通过 Code Review。
2. **推荐调用时机**
    - 在 `**Activity#onPostResume()**` 或 `**FragmentActivity#onResumeFragments()**` 中执行 commit；
    - 必要时，也可在 `**onCreate()**` 中执行（确保尚未调用 `onSaveInstanceState()`）。
3. **避免通过 try-catch 捕获异常**
    - 直接忽略异常无法保证页面状态正确，仍可能导致潜在 bug。

---

### 问题说明
+ Activity 被销毁前，系统会在 `**onSaveInstanceState()**` 保存状态；
+ 若此时执行 `FragmentTransaction.commit()`，状态恢复时 Fragment 可能无法正确还原；
+ 系统会抛出 `IllegalStateException: commit after state saved`，影响用户体验。

### 正确示例（正例）
```java
public class MainActivity extends FragmentActivity {
    FragmentManager fragmentManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        fragmentManager = getSupportFragmentManager();

        // 在 onCreate() 调用 commit，确保尚未保存状态
        FragmentTransaction ft = fragmentManager.beginTransaction();
        MyFragment fragment = new MyFragment();
        ft.replace(R.id.fragment_container, fragment);
        ft.commit();
    }
}
```

✅ **要点**：

+ 在 `onCreate()` 执行时，Activity 状态尚未保存，可以安全 commit；
+ 若 commit 时机不确定，可放在 `onPostResume()` 或 `onResumeFragments()`。

---

### 错误示例（反例）
```java
public class MainActivity extends FragmentActivity {
    FragmentManager fragmentManager;

    @Override
    public void onSaveInstanceState(Bundle outState, PersistableBundle outPersistentState) {
        super.onSaveInstanceState(outState, outPersistentState);

        fragmentManager = getSupportFragmentManager();
        FragmentTransaction ft = fragmentManager.beginTransaction();
        MyFragment fragment = new MyFragment();
        ft.replace(R.id.fragment_container, fragment);

        ft.commit(); // ❌ Activity 状态已保存，可能抛出 IllegalStateException
    }
}
```

❌ **问题**：

+ commit 在 `onSaveInstanceState()` 之后执行，可能导致页面状态丢失或 crash；
+ 不能依赖 try-catch 捕获异常，这不是解决根本问题的方式。

---

### 规范总结
| 规范项 | 推荐做法 |
| --- | --- |
| commit 时机 | `onCreate()`（尚未保存状态）、`onPostResume()`、`onResumeFragments()` |
| 禁止行为 | 随意使用 `commitAllowingStateLoss()`或 try-catch 忽略异常 |
| 使用条件 | 仅在确认 commit 丢失不会影响 UX 时使用 `commitAllowingStateLoss()` |
| 原因 | 保证 Fragment 状态与 Activity 状态同步，防止 IllegalStateException 和 UI 丢失 |


💡 **扩展建议**：

+ 尽量提前在 `onCreate()` 或 **事件触发前**准备好 Fragment，避免在 Activity 状态不确定时再执行 commit。
+ 若必须在异步回调中更新 Fragment，可通过 **Handler 或 LifecycleObserver** 确保 commit 时机安全。



## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">Activity 资源释放时机规范</font>
在 Android 中，`**Activity#onDestroy()**`** 并不保证在 Activity 即将结束时立即执行**，其调用时机可能受系统回收、配置变化（如屏幕旋转）、内存紧张等因素影响。

因此，不建议在 `onDestroy()` 中执行关键的资源释放工作，尤其是：

+ 工作线程（Thread、HandlerThread、Executor）销毁或停止；
+ 数据库或文件流关闭；
+ 其它耗时或依赖系统状态的操作。

### 正确做法（推荐）
1. **结合生命周期方法执行资源释放**

| 资源类型 | 推荐释放时机 | 说明 |
| --- | --- | --- |
| 工作线程 | `onPause()`/ `onStop()` | 结合 `isFinishing()`判断，确保仅在 Activity 真正结束时释放线程，避免延迟或多次释放 |
| UI 相关资源 | `onStop()` | 保证在界面不可见时释放占用资源 |
| 持久化数据 | `onPause()` | 保存临时数据，避免 onDestroy 被系统跳过 |


```java
@Override
protected void onPause() {
    super.onPause();

    if (isFinishing()) {
        // Activity 正在结束，安全释放资源
        if (workerThread != null) {
            workerThread.quit();
            workerThread = null;
        }
    }
}
```

### 问题说明
+ onDestroy() 的调用不确定性：
    - 系统可能 **直接杀掉进程**，跳过 onDestroy()；
    - Activity 因 **配置变化**（如屏幕旋转）而被销毁，此时不一定希望释放线程；
    - 在耗时操作中依赖 onDestroy()，可能导致 **资源未及时释放** 或 **内存泄漏**。
+ 使用 `isFinishing()` 判断可以避免在 **配置变化** 下误释放资源：

```java
@Override
protected void onStop() {
    super.onStop();
    if (isFinishing()) {
        // Activity 正在彻底结束
    }
}
```

### 总结规范
| 规范项 | 推荐做法 |
| --- | --- |
| 资源释放 | 避免放在 `onDestroy()`中 |
| 生命周期选择 | `onPause()` / `onStop()`+ `isFinishing()`判断 |
| 风险 | 延迟释放资源、内存泄漏、线程残留、不可预期行为 |
| 特殊情况 | 对于仅在配置变化时销毁的 Activity，不应释放长期线程或全局资源 |




💡 **扩展建议**：

+ 对于 **长期运行的后台任务**，考虑放到 **ViewModel、Service 或 Application 级别**，避免依赖 Activity 生命周期；
+ 对于 **临时线程或任务**，结合 `onStop()` 或 `onPause()` 及时释放，提升系统响应和资源利用效率。



## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">应用内广播优先使用 LocalBroadcastManager</font>
在 Android 中，如果广播仅用于应用内部通信，应优先使用 `**LocalBroadcastManager**` 而不是全局广播（`Context#sendBroadcast()`），原因如下：

### 优势
1. **安全性更高**
    - 广播只在应用内部传递，**外部应用无法接收**，防止敏感信息泄漏或恶意拦截。
2. **运行效率更高**
    - LocalBroadcastManager 不需要跨进程通信，发送和接收更快，系统开销更低。
3. **避免全局广播风险**
    - 全局广播可能被恶意应用监听或篡改；
    - 有序广播中，高优先级的恶意 Receiver 可能丢弃或修改广播，导致业务异常。

---

### 正确使用示例（正例）
```java
public class MainActivity extends AppCompatActivity {
    private MyReceiver receiver;
    private IntentFilter filter;
    private Context context;
    private static final String MY_BROADCAST_TAG = "com.peakmain.localbroadcast";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context = this;
        setContentView(R.layout.activity_main);

        receiver = new MyReceiver();
        filter = new IntentFilter();
        filter.addAction(MY_BROADCAST_TAG);

        Button button = findViewById(R.id.button);
        button.setOnClickListener(view -> {
            Intent intent = new Intent(MY_BROADCAST_TAG);
            LocalBroadcastManager.getInstance(context).sendBroadcast(intent);
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        LocalBroadcastManager.getInstance(context).registerReceiver(receiver, filter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        LocalBroadcastManager.getInstance(context).unregisterReceiver(receiver);
    }

    class MyReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            // 处理广播消息
        }
    }
}
```

✅ **要点**：

+ 注册和注销广播 **与生命周期绑定**（`onResume()` / `onPause()`）；
+ 只用于应用内部通信，避免敏感信息泄露。

---

### 错误示例（反例）
```java
// 所有广播都使用全局广播
Intent intent = new Intent("com.peakmain.broadcastreceiver.SOME_ACTION");
sendBroadcast(intent); // ❌ 外部应用可能接收
```

❌ **问题**：

+ 敏感信息可能被其他应用获取；
+ 全局广播增加系统开销，效率低；
+ 有序广播可能被高优先级 Receiver 丢弃或篡改。

---

### 规范总结
| 规范项 | 推荐做法 |
| --- | --- |
| 广播类型 | 应用内通信 → 使用 `LocalBroadcastManager` |
| 注册/注销时机 | 与 Activity / Fragment 生命周期绑定 |
| 安全风险 | 避免全局广播发送敏感信息 |
| 系统开销 | LocalBroadcastManager 更轻量、高效 |


---

💡 **扩展建议**：

+ 对于跨应用通信，仍需使用 **全局广播 + 权限保护 **`**<permission>**` 或 **Service / ContentProvider**；
+ 尽量避免使用全局广播发送敏感信息，保障应用安全。

<font style="color:#000000;"></font>

## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">动态注册 BroadcastReceiver 必须成对使用 register/unregister</font>
在 Android 中，动态注册的 `**BroadcastReceiver**` 必须与生命周期方法对应成对注册和注销，否则可能导致 **内存泄漏** 或 **系统异常**。

---

### 核心原则
1. **注册与注销要对应**
    - `registerReceiver()` 必须在合适的生命周期方法中注册；
    - `unregisterReceiver()` 必须在对应生命周期方法中注销。
2. **避免静态注册导致的资源泄漏**
    - 动态注册的 Receiver 如果在 Activity 多次 onResume 中注册，但在 onPause 或 onDestroy 没有注销，可能导致重复注册；
    - 特定机型（如华为）可能因为注册过多 Receiver 触发系统资源管控，应用直接崩溃。

---

### 正确示例（正例）
```java
public class MainActivity extends AppCompatActivity {
    private static MyReceiver myReceiver = new MyReceiver();

    @Override
    protected void onResume() {
        super.onResume();
        IntentFilter filter = new IntentFilter("com.example.myservice");
        registerReceiver(myReceiver, filter);  // 注册
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(myReceiver);       // 注销，与 onResume 成对
    }
}
```

✅ **要点**：

+ 注册在 `onResume()`，注销在 `onPause()`，生命周期对应；
+ 避免在 onDestroy 中注销，因为 onResume 可能多次执行，导致多次注册未注销。

---

### 错误示例（反例）
```java
public class MainActivity extends AppCompatActivity {
    private static MyReceiver myReceiver;

    @Override
    protected void onResume() {
        super.onResume();
        myReceiver = new MyReceiver();
        IntentFilter filter = new IntentFilter("com.example.myservice");
        registerReceiver(myReceiver, filter); // ❌ 多次 onResume 可能重复注册
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(myReceiver); // ❌ 无法匹配多次注册
    }
}
```

❌ **问题**：

+ Activity 生命周期多次触发 onResume → 多次注册 Receiver；
+ onDestroy 只注销一次 → 剩余 Receiver 未注销，导致 **内存泄漏** 或系统异常。

---

### 规范总结
| 规范项 | 推荐做法 |
| --- | --- |
| 注册位置 | `onResume()`/ `onStart()`（视使用场景而定） |
| 注销位置 | `onPause()` / `onStop()`与注册成对 |
| 风险 | 多次注册未注销 → 内存泄漏；系统资源占用过多 → 崩溃 |
| 特殊机型 | 华为、OPPO 等对 Receiver 数量有限制，必须成对注销 |


---

💡 **扩展建议**：

+ 对于 **仅应用内广播**，使用 **LocalBroadcastManager**，同样要求注册和注销成对；
+ 对于 **跨 Activity 或长期运行的广播**，建议使用 **Service + 静态注册** 或 **ViewModel/LiveData**，减少手动管理广播的复杂性。

<font style="color:#000000;"></font>

## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">隐式 Intent 使用必须增加过滤，防止被恶意拦截或调用</font>
### 背景说明
在 Android 中，启动组件（Activity、Service、BroadcastReceiver）时可使用两种方式：

1. **显式 Intent**：指定具体组件类名，例如：

```java
Intent intent = new Intent(this, TargetActivity.class);
startActivity(intent);
```

+ 安全，调用链明确，只有本应用可调用。
2. **隐式 Intent**：不指定具体组件，只指定动作（action）、数据（data）或 category，例如：

```java
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setData(Uri.parse("https://example.com"));
startActivity(intent);
```

+ 系统会匹配所有能够响应该 Intent 的组件。
+ **风险**：如果过滤不严格，恶意应用可能劫持隐式 Intent，访问敏感数据或执行危险操作。



### 隐式 Intent 常见风险
1. **敏感信息泄露**
    - 通过隐式 Intent 传递的敏感数据（如 cookie、用户 ID、token 等）可能被恶意应用获取。
2. **恶意篡改或劫持**
    - 恶意应用可能注册高优先级 Receiver，劫持广播或阻止 Activity 启动。
3. **安全漏洞示例**
    - 通过浏览器点击恶意 Scheme URL 启动应用组件，未过滤参数可能执行非法操作。

---

### 使用规范与强制要求
#### Manifest 或代码中增加过滤
+ **AndroidManifest.xml**

```xml
<activity android:name=".MyActivity">
    <intent-filter>
        <action android:name="com.example.MY_ACTION"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="myapp" android:host="open" />
    </intent-filter>
</activity>
```

+ **代码中使用 IntentFilter**

```java
IntentFilter filter = new IntentFilter();
filter.addAction("com.example.MY_ACTION");
filter.addCategory(Intent.CATEGORY_BROWSABLE);
registerReceiver(myReceiver, filter);
```

✅ 目的：只允许符合特定 Action、Category、Scheme 的 Intent 被组件接收。

#### 使用 Intent.parseUri() 时严格校验
1. 将 URI 转换为 Intent：

```java
Intent intent = Intent.parseUri(uri, 0);
```

2. **严格过滤**：

```java
// 确保 BROWSABLE category 存在
intent.addCategory(Intent.CATEGORY_BROWSABLE);

// 清空可能被篡改的显式组件和 Selector
intent.setComponent(null);
intent.setSelector(null);
```

3. **启动组件**

```java
if (intent.resolveActivity(getPackageManager()) != null) {
    startActivity(intent);
} else {
    // 找不到匹配组件，安全处理
}
```

---

#### 对 URI 或 Scheme 做白名单校验
```java
Uri data = intent.getData();
if (data != null && "myapp".equals(data.getScheme()) && "open".equals(data.getHost())) {
    startActivity(intent);
} else {
    // 非法 URI，拒绝处理
}
```

✅ 目的：防止外部恶意 URL 触发应用行为。

---

### 正反例
**正例：安全启动外部 Scheme URI**

```java
Intent intent = Intent.parseUri(uri, 0);
intent.addCategory(Intent.CATEGORY_BROWSABLE);
intent.setComponent(null);
intent.setSelector(null);

Uri data = intent.getData();
if (data != null && "myapp".equals(data.getScheme()) && "open".equals(data.getHost())) {
    context.startActivityIfNeeded(intent, -1);
}
```

**反例：直接解析并启动**

```java
Intent intent = Intent.parseUri(uri.toString().substring(15), 0);
context.startActivity(intent);  // ❌ 无过滤，可能被劫持
```

---

### 总结规范
| 规范项 | 推荐做法 |
| --- | --- |
| 隐式调用组件 | 必须在 Manifest 使用 `<intent-filter>`或在代码中使用 `IntentFilter` |
| 浏览器或外部 Scheme | 必须包含 `BROWSABLE`category，校验 Scheme + Host |
| URI / Intent 数据 | 严格校验，使用白名单或合法性判断 |
| 启动前检查 | 使用 `resolveActivity()`检查可用组件，避免 `ActivityNotFoundException` |
| 安全处理 | 清空显式组件 `setComponent(null)`和 Selector `setSelector(null)` |


---

### 开发者经验提示
1. **尽量使用显式 Intent**，减少安全风险；
2. **外部 URI 或 Scheme 必须校验**，避免 XSS、命令注入等漏洞；
3. **结合 Activity 生命周期**，使用 `startActivityIfNeeded()` 或 `resolveActivity()` 检查，保证调用安全；
4. **不要信任外部传入的参数**，敏感信息不通过隐式 Intent 传递。



