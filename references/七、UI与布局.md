## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">减少布局层级，禁止使用多层 LinearLayout 嵌套</font>
### <font style="color:#000000;">规范说法</font>
:::info
**布局中不得使用多重 LinearLayout 嵌套**。

在必须嵌套的场景下，应优先使用 **RelativeLayout（或 ConstraintLayout）**，以减少 View 层级，提升渲染性能。

:::

### 背景与原理
在 Android UI 渲染流程中，每一个 View 都会经历三个阶段：

```java
measure → layout → draw
```

整个过程自顶向下执行：

1. **measure**：计算每个 View 的尺寸。
2. **layout**：确定每个 View 的位置。
3. **draw**：将内容绘制到屏幕上。

当布局层级过深时（尤其是多层嵌套的 LinearLayout），父 View 在测量子 View 时会触发多次 measure 流程，从而导致：

+ **多次重复测量**
+ **measure/layout 时间翻倍**
+ **UI 卡顿、掉帧**
+ **渲染时间超过 16ms（60fps）预算，导致卡顿**

:::info
📊 结论：  
布局层级越深 → measure 次数越多 → CPU 计算越多 → 帧率下降。

:::

### 错误示例（反例）
```xml
<!-- ❌ 过度嵌套的 LinearLayout -->
<LinearLayout
  xmlns:android="http://schemas.android.com/apk/res/android"
  android:orientation="vertical"
  android:layout_width="match_parent"
  android:layout_height="match_parent">

  <LinearLayout
    android:orientation="horizontal"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <LinearLayout
      android:orientation="vertical"
      android:layout_width="wrap_content"
      android:layout_height="wrap_content">

      <TextView
        android:text="用户名"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"/>

      <TextView
        android:text="账号信息"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"/>

    </LinearLayout>

    <ImageView
      android:src="@drawable/ic_avatar"
      android:layout_width="48dp"
      android:layout_height="48dp"/>
  </LinearLayout>
</LinearLayout>
```

问题：

+ 三层 LinearLayout 嵌套。
+ 同时存在纵向 + 横向嵌套，造成多次测量。
+ 每次绘制都要遍历更多节点 → measure/layout/draw 时间翻倍。

### 正确示例（正例）
使用 `RelativeLayout`（或 `ConstraintLayout`）替代

```xml
<RelativeLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/iv_avatar"
        android:src="@drawable/ic_avatar"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:layout_alignParentEnd="true"/>

    <TextView
        android:id="@+id/tv_name"
        android:text="用户名"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_toStartOf="@id/iv_avatar"/>

    <TextView
        android:id="@+id/tv_info"
        android:text="账号信息"
        android:layout_below="@id/tv_name"
        android:layout_toStartOf="@id/iv_avatar"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"/>

</RelativeLayout>
```

优点：

+ 布局结构扁平，仅一层容器。
+ 减少了 2 层 measure/layout。
+ 性能显著提升。



使用 `ConstraintLayout`（推荐）

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/iv_avatar"
        android:src="@drawable/ic_avatar"
        android:layout_width="48dp"
        android:layout_height="48dp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>

    <TextView
        android:id="@+id/tv_name"
        android:text="用户名"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>

    <TextView
        android:id="@+id/tv_info"
        android:text="账号信息"
        app:layout_constraintStart_toStartOf="@id/tv_name"
        app:layout_constraintTop_toBottomOf="@id/tv_name"/>
</androidx.constraintlayout.widget.ConstraintLayout>
```

:::info
+ ConstraintLayout 支持复杂的相对定位关系，几乎可以替代所有嵌套的 LinearLayout/RelativeLayout 结构。
+ Android 官方推荐使用 ConstraintLayout 构建复杂布局。

:::

| 优化手段 | 作用 |
| --- | --- |
| 避免多层 LinearLayout 嵌套 | 减少 measure/layout 计算量 |
| 使用 RelativeLayout / ConstraintLayout | 扁平化布局结构 |
| 使用 `<merge>`、`<include>` | 降低布局层级，提高复用性 |
| 移除不可见/无用的 View | 降低绘制负担 |
| 保证渲染时间 < 16ms | 确保 UI 流畅不卡顿 |


## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">对话框与浮层使用规范</font>
### 规范说明
+ 在 **Activity** 中显示对话框或弹出浮层时，**推荐使用 **`**DialogFragment**`，而非直接使用 `Dialog` / `AlertDialog`。
+ 通过 `DialogFragment` 管理弹窗，能够与 **Activity/Fragment 的生命周期联动**，避免窗口泄漏、状态异常或崩溃问题。



### 原因分析
在传统的 `Dialog` / `AlertDialog` 中：

+ 弹窗独立于 `Activity` 生命周期，不会自动随 Activity 销毁而销毁；
+ 若在 `Activity` 退出后仍持有弹窗引用，可能触发 **WindowLeaked 异常**；
+ 横竖屏切换或进程恢复时，`Dialog` 的状态不会自动保存，导致界面还原错误；
+ 需要手动管理 show/dismiss 时机，代码复杂且易错。



而 `DialogFragment` 作为 Fragment 的一种特殊形式，具备以下优势：

1. ✅ 生命周期自动跟随宿主（Activity 或 Fragment）；
2. ✅ 支持状态保存与恢复（orientation change、进程重启）；
3. ✅ 可通过 `FragmentManager` 统一管理（支持回退栈、事务动画）；
4. ✅ 更方便与 ViewModel、DataBinding、Compose 等架构集成。



### 正确示例
```java
public class MainActivity extends AppCompatActivity {

    public void showPromptDialog(String message) {
        PromptDialogFragment dialog = PromptDialogFragment.newInstance(message);
        dialog.show(getSupportFragmentManager(), "PromptDialog");
    }

    public static class PromptDialogFragment extends DialogFragment {

        public static PromptDialogFragment newInstance(String text) {
            Bundle args = new Bundle();
            args.putString("text", text);
            PromptDialogFragment fragment = new PromptDialogFragment();
            fragment.setArguments(args);
            return fragment;
        }

        @Nullable
        @Override
        public View onCreateView(
                @NonNull LayoutInflater inflater,
                @Nullable ViewGroup container,
                @Nullable Bundle savedInstanceState
        ) {
            getDialog().requestWindowFeature(Window.FEATURE_NO_TITLE);
            View view = inflater.inflate(R.layout.fragment_prompt, container, false);
            TextView tvMessage = view.findViewById(R.id.tvMessage);
            tvMessage.setText(getArguments().getString("text"));
            return view;
        }

        @Override
        public void onStart() {
            super.onStart();
            // 可在此统一设置弹窗宽高、动画、圆角、背景透明度等
            Window window = getDialog().getWindow();
            if (window != null) {
                window.setLayout(ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.WRAP_CONTENT);
                window.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
            }
        }
    }
}
```

### 错误示例
```java
public class MainActivity extends AppCompatActivity {
    private AlertDialog dialog;

    @Override
    protected void onResume() {
        super.onResume();
        dialog = new AlertDialog.Builder(this)
                .setMessage("This is a dialog")
                .setPositiveButton("OK", null)
                .create();
        dialog.show(); // ❌ 若此时Activity进入后台或旋转屏幕，可能WindowLeaked
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // ❌ 若Activity已销毁但未调用dismiss，会导致WindowLeaked
        if (dialog != null && dialog.isShowing()) {
            dialog.dismiss();
        }
    }
}
```

**问题：**

+ 弹窗与 Activity 生命周期不一致；
+ 旋转屏幕后，原弹窗实例不再有效；
+ 容易引起 `android.view.WindowLeaked` 异常。



### 扩展建议
#### Jetpack Compose 场景
在 Compose 中无需使用 `DialogFragment`，但依然要**遵循生命周期安全与状态恢复原则**。

示例：

```kotlin
@Composable
fun PromptDialog(show: Boolean, message: String, onDismiss: () -> Unit) {
    if (show) {
        Dialog(onDismissRequest = onDismiss) {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = Color.White
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = message)
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(onClick = onDismiss) { Text("OK") }
                }
            }
        }
    }
}
```

Compose 的 `Dialog` 是 Composable 内联函数（`inline`），无需 Fragment 托管，但仍应使用 `ViewModel` 或 `rememberSaveable` 保存状态，防止配置更改导致的状态丢失。

### 总结
| 场景 | 推荐实现 | 优点 |
| --- | --- | --- |
| 传统 View 系统 | `DialogFragment` | 生命周期安全，状态可恢复 |
| Compose 架构 | Compose `Dialog` | 轻量、声明式、内联优化 |
| 跨组件弹窗 | `DialogFragment`+ `FragmentManager` | 支持回退栈与事务动画 |
| 临时性 Toast/Popup | `PopupWindow`/ `Snackbar` | 不建议长期存在 |


## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">DialogFragment / Fragment：</font>**禁止**<font style="color:#000000;">使用带参数的构造函数；必须保留</font>**无参构造函数**<font style="color:#000000;">（并优先使用 newInstance + setArguments）或使用 FragmentFactory 注入</font>
### 原因（为什么会出错）
+ 系统（`FragmentManager`）在恢复 Fragment 时，会通过反射调用 **无参构造函数** 创建实例并恢复状态（从 `savedInstanceState` 或 `arguments` 恢复）。
+ 如果你只实现了带参数的构造函数而没有无参构造函数，系统在进程被杀后重建 Fragment 会失败，通常表现为 `Fragment` 恢复崩溃或 `IllegalStateException`/`InstantiationException` 等异常。

### 错误示例（不要这样写）
```java
public class PromptDialogFragment extends DialogFragment {
    private String text;

    // ❌ 带参构造器（会导致 Fragment 恢复失败）
    public PromptDialogFragment(String text) {
        this.text = text;
    }

    // 如果没有无参构造器，FragmentManager 无法重建该 Fragment
}
```

### 推荐做法一：使用 newInstance() + setArguments(Bundle)（最通用、兼容性最好）
```java
public class PromptDialogFragment extends DialogFragment {
    private static final String KEY_TEXT = "key_text";

    public PromptDialogFragment() {
        // 必须保留 public 无参构造函数
    }

    public static PromptDialogFragment newInstance(String text) {
        PromptDialogFragment fragment = new PromptDialogFragment();
        Bundle args = new Bundle();
        args.putString(KEY_TEXT, text);
        fragment.setArguments(args);
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(...) {
        String text = getArguments() != null ? getArguments().getString(KEY_TEXT) : "";
        // 使用 text 初始化 View
    }
}
```

优点：

+ 与 FragmentManager 的恢复机制完全兼容；
+ 支持进程被杀后自动恢复（系统会保存并恢复 `arguments`）；
+ 简洁、安全（推荐写法，适用于手册规范）。

### 推荐做法二：如果必须依赖构造注入（例如使用依赖注入框架），使用 FragmentFactory（进阶）
现代 `Fragment` 恢复机制允许你设置自定义 `FragmentFactory` 来控制实例化，从而安全地使用构造参数注入。



步骤示例

1. 自定义 FragmentFactory

```java
public class MyFragmentFactory extends FragmentFactory {
    private final MyDependency dep;

    public MyFragmentFactory(MyDependency dep) {
        this.dep = dep;
    }

    @NonNull
    @Override
    public Fragment instantiate(@NonNull ClassLoader classLoader, @NonNull String className) {
        if (className.equals(MyInjectedFragment.class.getName())) {
            return new MyInjectedFragment(dep); // 安全注入
        }
        return super.instantiate(classLoader, className);
    }
}

```

2. 在 `Activity`/`FragmentManager` 设置工厂（应在 `super.onCreate()` 之前）：

```java
getSupportFragmentManager().setFragmentFactory(new MyFragmentFactory(dep));
```

3. `MyInjectedFragment` 可以有带参构造器：

```java
public class MyInjectedFragment extends Fragment {
    private final MyDependency dep;
    public MyInjectedFragment(MyDependency dep) {
        this.dep = dep;
    }
    // 仍需处理 arguments 保存 UI 状态
}
```

注意：使用 `FragmentFactory` 是进阶方案，需保证工厂在恢复前已设置，否则恢复时仍会使用默认构造器失败。

### 额外注意事项
1. **只把可序列化的轻量数据放入 **`**arguments**`（基本类型、String、Parcelable）。避免将大对象、Context、非序列化引用放入 `arguments`。
2. `arguments` 在进程被杀后会被系统保存并恢复，**newInstance + setArguments** 是恢复最可靠的方法。
3. 即使用 `FragmentFactory` 注入依赖，也应把需要保存的 UI 状态放 `arguments` 或 `savedInstanceState`。
4. **不要依赖 **`**onCreate**`** 的构造参数** —— 任何需要保留的状态都应通过 `arguments` 或 `ViewModel` 管理。
5. 在 Kotlin 中同样适用：避免只定义带参构造（尤其是 `@JvmOverloads` 或默认参数），要显式提供无参构造或使用 `FragmentFactory`/依赖注入框架（Hilt 的 `@AndroidEntryPoint` 等有相应处理）。

:::info
<font style="color:#DF2A3F;">【强制】</font>Fragment（包括 DialogFragment）不得仅实现带参数构造函数，必须保留无参构造函数。

说明：FragmentManager 恢复 Fragment 时会通过反射调用无参构造函数并恢复 arguments。推荐使用 newInstance(...) + setArguments(Bundle) 传参，或在需要构造注入时使用 FragmentFactory；禁止将非可序列化或大型对象放入 arguments。

:::

## <font style="color:#528135;">【推荐】</font>不能在 Activity 未完全显示前显示 PopupWindow 或 Dialog
### 说明
在 Android 的生命周期中，**Activity 并非在 **`**onCreate()**`** 执行完毕后立即可见或可交互**。  
Activity 从创建到可见、可交互的完整过程如下：

```plain
onCreate() → onStart() → onResume() → onAttachedToWindow() → onWindowFocusChanged(true)
```

其中：

+ 在 `**onAttachedToWindow()**` 时，Activity 才与 Window 建立关联；
+ 在 `**onWindowFocusChanged(true)**` 被调用后，Activity 才真正可交互、可安全展示 UI。

如果在 Activity 尚未与 Window 绑定（如 `onCreate()`、`onResume()` 期间）就显示 `Dialog` 或 `PopupWindow`，可能会出现以下问题：

+ 抛出 `WindowManager$BadTokenException`；
+ 弹窗显示位置异常（无动画、位置偏移、背景透明度错误等）；
+ 在 Activity 重建（例如旋转屏幕）时导致内存泄漏或崩溃。

因此，推荐的做法是在 `**onAttachedToWindow()**`** 之后**，尤其是在 `**onWindowFocusChanged(true)**` 回调后再显示弹窗。

### 正例：
```kotlin
class MainActivity : AppCompatActivity() {
    private var hasWindowFocus = false

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus && !hasWindowFocus) {
            hasWindowFocus = true
            showWelcomeDialog()
        }
    }

    private fun showWelcomeDialog() {
        val dialog = AlertDialog.Builder(this)
            .setTitle("欢迎使用")
            .setMessage("界面加载完成后再展示弹窗，避免窗口异常。")
            .setPositiveButton("确定", null)
            .create()
        dialog.show()
    }
}
```

这种写法确保：

+ Activity 已完全显示；
+ 不会在 Window 未就绪时创建窗口；
+ 有效避免 BadTokenException。

### 反例：
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    
    // ❌ 此时 Window 还未 attach，可能导致 BadTokenException
    AlertDialog.Builder(this)
        .setMessage("Activity 还没显示完就弹出")
        .show()
}
```

或：

```kotlin
override fun onResume() {
    super.onResume()
    // ❌ 此时 Window 尚未 Focus，部分 ROM 会显示异常或无动画
    popupWindow.showAtLocation(window.decorView, Gravity.CENTER, 0, 0)
}
```

### 实战建议
| 场景 | 推荐时机 |
| --- | --- |
| 显示加载完成弹窗（例如欢迎、引导） | `onWindowFocusChanged(true)` |
| 动态提示框（如权限、更新提醒） | 使用 `lifecycleScope.launchWhenResumed { ... }` 或 `Handler.post { ... }` 延迟执行 |
| 显示 `PopupWindow` | 确保 `View.isAttachedToWindow == true`再调用 |
| DialogFragment | 调用 `show()`时确保 Fragment 已 attach，例如在 `onPostResume()`或通过 ViewModel 事件触发 |




### 补充说明
部分定制系统（如 MIUI、ColorOS）在 Activity 尚未完全可见时创建弹窗会直接崩溃，因此：

+ 不建议在 `onCreate()`、`onStart()` 阶段显示任何浮层；
+ 如果需要立即显示，可通过 `View.post {}` 或 `Handler.post {}` 延迟一帧执行：

```kotlin
override fun onResume() {
    super.onResume()
    window.decorView.post {
        showDialogSafely()
    }
}
```

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">尽量不要使用AnimationDrawable</font>
### 说明
`AnimationDrawable` 是 Android 早期提供的一种帧动画实现方式，它通过在 XML 中声明多张帧图片，并在运行时依次切换实现动画效果。

但它存在严重的性能问题和内存隐患，**尤其在帧数多或图片较大时极易导致 OOM 或内存泄漏**。

### 原理问题
+ 当 AnimationDrawable 初始化时，会**一次性加载所有帧图片到内存中**（`Bitmap` 全部常驻内存），即使动画未播放也会占用大量内存。
+ 并且 AnimationDrawable 没有提供手动释放机制，调用 stop() 也仅仅是停止播放，不会释放图片内存。
+ 即便调用 setCallback(null) 或置空引用，下一次重新进入界面时再次加载相同动画也容易触发崩溃（java.lang.OutOfMemoryError 或 android.graphics.Bitmap reused error）。

### 正例
仅当帧数少、图片体积较小时可使用：

```xml
<?xml version="1.0" encoding="utf-8"?>
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
  android:oneshot="true">
  <item android:drawable="@drawable/ic_heart_100" android:duration="500" />
  <item android:drawable="@drawable/ic_heart_75" android:duration="500" />
  <item android:drawable="@drawable/ic_heart_50" android:duration="500" />
  <item android:drawable="@drawable/ic_heart_25" android:duration="500" />
  <item android:drawable="@drawable/ic_heart_0" android:duration="500" />
</animation-list>
```

在 Java/Kotlin 中控制使用：

```kotlin
val imageView = findViewById<ImageView>(R.id.imageView)
imageView.setBackgroundResource(R.drawable.anim_heart)
val animation = imageView.background as AnimationDrawable
animation.start()
```

### 反例
帧数过多、图片过大（例如几十帧）会极度消耗内存，甚至导致 OOM：

```kotlin
<animation-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:oneshot="false">
    <item android:drawable="@drawable/soundwave_new_1_40" android:duration="100" />
    <item android:drawable="@drawable/soundwave_new_1_41" android:duration="100" />
    ...
    <item android:drawable="@drawable/soundwave_new_1_69" android:duration="100" />
</animation-list>
```

问题：

+ 所有 30+ 帧的图片在初始化时一次性加载；
+ 造成几十 MB 的内存开销；
+ 部分机型（尤其低端机）在解码时直接抛出 OOM；
+ 即使调用 `animation.stop()` 也不会释放内存。

### 推荐替代方案
| 方案 | 说明 | 适用场景 |
| --- | --- | --- |
| **LottieAnimationView** | 基于矢量动画 JSON 文件渲染，由 Airbnb 开发，内存占用极低 | 界面引导、按钮动画、loading 动效 |
| **帧动画逐帧加载方案** | 通过 `Handler`或 `Choreographer`动态切换图片，仅加载当前帧，播放结束立即回收 | 自定义控件、需要高帧动画的场景 |
| **AnimatedVectorDrawable** | 使用矢量图 + 属性动画实现，兼容性强，内存占用低 | 图标变换、进度动画 |
| **SurfaceView/TextureView + 绘制线程** | 适合复杂帧率动画或视频式动画，支持硬件加速 | 游戏、实时动效渲染 |


示例（替代实现）：

```kotlin
val frames = listOf(
    R.drawable.frame_1, R.drawable.frame_2, R.drawable.frame_3
)
val handler = Handler(Looper.getMainLooper())
var index = 0
val imageView = findViewById<ImageView>(R.id.imageView)

val runnable = object : Runnable {
    override fun run() {
        imageView.setImageResource(frames[index])
        index = (index + 1) % frames.size
        handler.postDelayed(this, 100)
    }
}
handler.post(runnable)
```

:::danger
+ ❗ 许多开发者误以为调用 animationDrawable.stop() 或 animationDrawable = null 能释放内存，实际上并不会。
+ 因为所有帧图片在加载时已存入 DrawableContainer.DrawableContainerState 的缓存中（Android Framework 内部类），即使对象置空仍被 DrawableState 持有。
+ 因此真正安全的释放方式只有**彻底销毁引用 + 强制触发 GC**，而这在实际应用中不可控。

:::

## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">禁止使用 ScrollView 包裹 ListView / GridView / ExpandableListView</font>
### 说明
在布局中使用 `ScrollView` 嵌套可滚动控件（如 `ListView`、`GridView`、`RecyclerView`）会导致严重的性能问题。

这是因为：

+ **ScrollView 会一次性测量子 View 的完整高度**<font style="color:#000000;">，而这些可滚动控件（尤其是 </font>`<font style="color:#000000;">ListView</font>`<font style="color:#000000;">）默认只加载屏幕内可见的 Item；</font>
+ <font style="color:#000000;">被包裹后，ListView 等组件的复用机制（convertView、RecyclerView.ViewHolder）会失效；</font>
+ <font style="color:#000000;">所有 Item 会一次性加载到内存中，造成：</font>
    - **UI 卡顿**
    - **内存占用暴增**
    - **CPU 重绘负担大**
    - **滑动冲突与焦点问题**

:::color3
官方文档中明确指出：

+ 不要在可滚动组件外再嵌套 `ScrollView`，否则会导致测量与绘制性能问题。

:::

### <font style="color:#000000;">风险示例（反例）</font>
```xml
<ScrollView>
  <LinearLayout
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <TextView
      android:text="标题" />

    <ListView
      android:id="@+id/list_view"
      android:layout_width="match_parent"
      android:layout_height="wrap_content" />

    <TextView
      android:text="底部说明文字" />
  </LinearLayout>
</ScrollView>
```

这种写法会导致 `ListView` 所有 Item **在初始化时全部加载进内存**。

在包含几十上百条数据时，会明显看到 **界面卡顿、图片闪烁、OOM** 等问题。

### 推荐方案一（现代 XML 实现）
#### 代码实现
如需顶部内容 + 列表共滚动，可使用 `NestedScrollView + RecyclerView`，并启用嵌套滚动支持：

```xml
<androidx.core.widget.NestedScrollView
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fillViewport="true">

    <LinearLayout
        android:orientation="vertical"
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <ImageView
            android:layout_width="match_parent"
            android:layout_height="200dp"
            android:src="@drawable/banner" />

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/recyclerView"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:nestedScrollingEnabled="false" />
    </LinearLayout>
</androidx.core.widget.NestedScrollView>
```

#### NestedScrollView + RecyclerView 的默认行为
+ 默认情况下，RecyclerView**自身支持嵌套滚动** (nestedScrollingEnabled = true)。
+ 当 RecyclerView 被放在 NestedScrollView 内时：
    - NestedScrollView 会在 measure 阶段让 RecyclerView**去测量所有子项的高度**；
    - 这会触发 RecyclerView **一次性创建所有 ViewHolder**，即加载了全部 Item；
    - 结果就是内存消耗大，卡顿明显，尤其是列表很长时。

所以，简单嵌套 ScrollView/NestedScrollView + RecyclerView **本质问题与 ScrollView + ListView 是一样的**。

#### nestedScrollingEnabled = false 的作用
当你设置：

```kotlin
recyclerView.isNestedScrollingEnabled = false
```

+ RecyclerView **放弃了自身的嵌套滚动行为**；
+ NestedScrollView 不再让 RecyclerView 完全展开测量：
    - RecyclerView 的 `onMeasure` 会被限制在屏幕可见区域；
    - 只会创建屏幕可见的 Item，达到懒加载效果；
+ 这样就避免了一次性加载所有 Item，性能问题得到缓解。

:::color3
注意：这种方式只是折中方案，仍然要避免非常长的列表，因为 NestedScrollView 仍然会处理整体滚动，RecyclerView 的回收机制可能受限。

:::

### 推荐方案二（Compose 实现）
在 **Jetpack Compose** 中，不存在传统意义的嵌套滚动问题。

如果需要头部内容 + 列表一体滚动，可以直接使用 `LazyColumn`：

```kotlin
LazyColumn {
    item {
        Image(
            painter = painterResource(R.drawable.banner),
            contentDescription = null,
            modifier = Modifier.fillMaxWidth().height(200.dp)
        )
    }

    items(listData) { item ->
        Text(
            text = item.title,
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        )
    }

    item {
        Text(
            text = "底部说明文字",
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        )
    }
}

```

:::color3
LazyColumn 会智能管理可见区域的 item，仅加载屏幕内内容，

无论嵌套多少层 Composable 函数，都不会引发性能问题（编译期 inline 优化）。

:::

| 场景 | 推荐控件 | 备注 |
| --- | --- | --- |
| 简单列表 | `RecyclerView` | 可自定义 LayoutManager |
| 复杂联动滚动 | `NestedScrollView + RecyclerView` | 注意禁用嵌套滚动 |
| Compose 界面 | `LazyColumn` / `LazyVerticalGrid` | 原生懒加载机制，性能最佳 |
| 动态内容过多 | 分段加载（分页 / 分屏） | 避免大体量 UI 一次性渲染 |




## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">不要在 Application 中缓存数据</font>
### 说明
Android 的 `Application` 对象虽然是全局单例，但并不适合作为数据缓存的存储场所：

+ 系统可能随时回收应用进程，Application 中的数据随时可能丢失；
+ 不同组件之间的数据共享应使用 **Intent、Bundle、SharedPreferences、数据库** 等机制；
+ 缓存数据放在 Application 中容易引发内存泄漏和生命周期管理问题。

### 反例（错误做法）
```kotlin
class MyApplication extends Application {
    String username;

    String getUsername() {
        return username;
    }

    void setUsername(String username) {
        this.username = username;
    }
}

class SetUsernameActivity extends Activity {
    @Override
    void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.set_username);
        MyApplication app = (MyApplication) getApplication();
        app.setUsername("tester1");
        startActivity(new Intent(this, GetUsernameActivity.class));
    }
}

class GetUsernameActivity extends Activity {
    TextView tv;

    @Override
    void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.get_username);
        tv = findViewById(R.id.username);
    }

    @Override
    void onResume() {
        super.onResume();
        MyApplication app = (MyApplication) getApplication();
        tv.setText("Welcome back! " + app.getUsername().toUpperCase());
    }
}
```

缺点：

1. 进程被杀后数据丢失；
2. 数据耦合 Application 生命周期，增加维护难度；
3. 不适合在多进程场景下使用。

### 推荐做法
#### 通过 Intent/Bundle 传递临时数据
```kotlin
Intent intent = new Intent(this, GetUsernameActivity.class);
intent.putExtra("username", "tester1");
startActivity(intent);
```

在目标 Activity 中：

```kotlin
String username = getIntent().getStringExtra("username");
```

#### 使用 SharedPreferences 或数据库存储可持久化数据
```kotlin
// 保存
SharedPreferences sp = getSharedPreferences("app_prefs", MODE_PRIVATE);
sp.edit().putString("username", "tester1").apply();

// 读取
String username = sp.getString("username", "");
```

#### 使用 Application 仅保存不可被系统回收的全局对象引用
比如第三方 SDK 单例或全局工具类，而非业务数据。



## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">Toast 的使用规范</font>
### 说明
+ Android 原生的 `Toast.makeText(...).show()` 会在连续调用时造成前一个 Toast 消息无法取消，出现“堆叠显示”的情况，影响用户体验。
+ 为了避免重复创建 Toast 对象和防止 UI 混乱，建议使用 **全局 Toast 单例**，或者在 Activity/Fragment 中复用同一个 Toast 实例。

### 正例（推荐做法）
```kotlin
public class ToastUtils {
    private static Toast toast;

    public static void showToast(Context context, String message) {
        if (toast == null) {
            toast = Toast.makeText(context.getApplicationContext(), message, Toast.LENGTH_SHORT);
        } else {
            toast.setText(message);
            toast.setDuration(Toast.LENGTH_SHORT);
        }
        toast.show();
    }
}

// 调用
ToastUtils.showToast(this, "操作成功");
```

优点：

+ 避免 Toast 消息堆叠；
+ 减少重复创建对象，提高性能；
+ 统一管理 Toast 的显示时机和样式。

### 反例（错误做法）
```kotlin
// 连续调用时会导致多条 Toast 堆叠显示
Toast.makeText(this, "第一条消息", Toast.LENGTH_SHORT).show();
Toast.makeText(this, "第二条消息", Toast.LENGTH_SHORT).show();
```

缺点：

+ 用户可能看不到第一条 Toast；
+ UI 体验差；
+ 无法统一控制 Toast 消息显示时长。

## <font style="color:#FF0000;">【强制】</font><font style="color:#000000;">Adapter 中 ViewHolder 的控件属性设置</font>
### 说明
+ 在使用 `Adapter` 时，如果你使用了 `ViewHolder` 做缓存，那么 `getView()` 方法中的 `convertView` 会被重复复用。
+ **无论某个子控件属性是否为 null 或透明**，都必须显式设置，否则在列表滑动过程中会出现显示错乱（复用导致上一次的属性残留）。

### 正例（推荐做法）
```java
@Override
public View getView(int position, View convertView, ViewGroup parent) {
    ViewHolder myViews;

    if (convertView == null) {
        myViews = new ViewHolder();
        convertView = mInflater.inflate(R.layout.list_item, null);
        myViews.mUsername = (TextView) convertView.findViewById(R.id.username);
        convertView.setTag(myViews);
    } else {
        myViews = (ViewHolder) convertView.getTag();
    }

    Info p = infoList.get(position);
    String dn = p.getDisplayName();
    myViews.mUsername.setText(StringUtils.isEmpty(dn) ? "" : dn);

    // 其他控件同理
    // myViews.mButton.setBackgroundColor(p.isActive() ? Color.BLUE : Color.TRANSPARENT);

    return convertView;
}

static class ViewHolder {
    private TextView mUsername;
    // 其他控件
}
```

### 反例（错误做法）
```java
@Override
public View getView(int position, View convertView, ViewGroup parent) {
    ViewHolder myViews;

    if (convertView == null) {
        myViews = new ViewHolder();
        convertView = mInflater.inflate(R.layout.list_item, null);
        myViews.mUsername = (TextView) convertView.findViewById(R.id.username);
        convertView.setTag(myViews);
    } else {
        myViews = (ViewHolder) convertView.getTag();
    }

    Info p = infoList.get(position);
    String dn = p.getDisplayName();

    // 仅在非空时设置，空文本未显式设置
    if (!StringUtils.isEmpty(dn)) {
        myViews.mUsername.setText(dn);
    }
    // 忽略 null 或透明属性设置，滑动时会出现错乱
    return convertView;
}
```



:::info
要点：

1. 对于 TextView，即使文本为 null，也必须 setText("")；
2. 对于背景、颜色等属性，即使是透明或默认值，也必须显式设置；
3. 保证 convertView 被复用时不会残留上一次的数据。

:::



