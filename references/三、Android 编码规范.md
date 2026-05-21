## [警告]不得使用requireContext()，需对获取的context进行判空处理
### 错误/正确示例
+ 错误示例

```java
rvFourthSpace.setLayoutManager(new LinearLayoutManager(requireContext()));
```

+ 正确示例

```java
Context context = getContext();
if (context != null) {
    rvFourthSpace.setLayoutManager(new LinearLayoutManager(context));
}
```

### Context判空封装
+ 封装代码

```java
fun Context?.handleEmpty(block: ((Context) -> Unit)? = null) {
    this?.let {
        block?.invoke(it)
    }
}
fun FragmentActivity?.handleEmptyActivity(block: ((FragmentActivity) -> Unit)? = null) {
    this?.let {
        block?.invoke(it)
    }
}
```

+ Java使用

```java
EmptyHandleUtilsKt.handleEmpty(getContext(), new Function1<Context, Unit>() {
    @Override
    public Unit invoke(Context context) {
        UrlDisposeUtils.schemeUrl(context, new Intent(), "", spaceItem.getDetailUrl());
        return null;
    }
});
```

可替换成lambda表达式

```java
EmptyHandleUtilsKt.handleEmpty(getContext(),  context-> {
    UrlDisposeUtils.schemeUrl(context, new Intent(), "", spaceItem.getDetailUrl());
    return null;
});
```

使用模板,方便直接复制粘贴使用

```java
EmptyHandleUtilsKt.handleEmpty(getContext(),  context-> {

    return null;
});
```

```java
EmptyHandleUtilsKt.handleEmptyActivity(getActivity(), activity -> {
    
    return null;
});
```

### setOnClickListener中对Context的使用，可使用v.getContext()
```java
   ivGrade.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AtourUtils.jumpToH52(v.getContext(), H5Service.MEMBRERIGHHTS, "", Constants.PAGE_NAME_TYPE_MEMBER_RIGHT);
            }
        });
```

<font style="color:#DF2A3F;">这里的v一定不会为空</font>

### <font style="color:#000000;">是否一定要对getContext()为空进行判断</font>
+ 不是一定，主要看具体场景以及其他架构或者系统底层是否运行为空
+ 用 @Nullable修饰的表示可以为空， 此时可以直接调用getContext()
    - 如系统源码VectorDrawableCompat中的theme
+ 用 @NonNull修饰的表示不可为空，需要对getContext()进行判空处理

<!-- 这是一张图片，ocr 内容为：URLDISPOSEUTILS.JAVA HOTELLISTACTIVITY.KTX ) MINEFRAGMENT.JAVA X VECTORDRAWABLECOMPAT.JAVA CONTEXTCOMPAT.JAVA SWOUT LIGLYING - MYCCTOR SCATE MUR ACMATIUCT .W ICTYILU 29 FLOAT EX ; VIEWPORTWIDTH / INTRINSICWIDTH; SCALEX FLOAT SCALEY - VIEWPORTHEIGHT / INTRINSICHEIGHT; 30  MATH.MIN(SCALEX, SCALEY); 31 RETURN 32 CREATE A VECTORDRAWABLECOMPAT OBJECT.  PARAMS: RES - THE RESOURCES. RESID - THE RESOURCE ID FOR VECTORDRAWABLECOMPAT OBJECT. THEME - THE THEME OF THIS VECTOR DRAWABLE, IT CAN BE NULL. A NEW VECTORDRAWABLECOMNAT OR NULL IF NARSING ERROR IS FOUND , @NULLABLE 43 PUBLIC STATIC VECTORDRAWABLECOMPAT CREATE(ENONNULL RESOURCES RES, QDRAVABLERES INT RESID. 44 @NULLABLE THEME THEME) { (BUILD.VERSION.SDK_INT >: 24) { IF 45 646 TINAL VECTORDRAWADLECOMPAT ARAWADLE 三 NEW VECTORURAWADLECOMPAT() DRAWABLE.MDELEGATEDRAWABLE - RESOURCESCOMPAT.GETDRAWABLE(RES, RESID, THEME); 47 DRAWABLE.MCACHEDCONSTANTSTATEDELEGATE - NEW VECTORDRAWABLEDELEGATESTATE( DRAWABLE.MDELEGATEDRAWABLE.GETCONSTANTSTATE()); 49 DRAWABLE: 50 RETURN -->
![](https://cdn.nlark.com/yuque/0/2024/png/25366497/1731566045774-8528ac5f-5b7c-482f-be08-8a03c59e340d.png)

```java

```

## EditText设置光标，若EditText有限制字符maxLength，setSelection必须判断原有字符长度和设置文本字符长度
+ 封装代码

```java
fun EditText?.setSelection(originName: String) {
    this?.let { editText ->
        val text = editText.text
        if (!TextUtils.isEmpty(originName)) {
            val length = originName.length
            setSelection(minOf(length, text.length))
        } else {
            setSelection(0)
        }
    }
}
```

+ Java使用代码

```java
etName.setText(originName);
EditTextUtilsKt.setSelection(etName,originName);
```

## 获取屏幕宽高或者dp转换，一律使用SizeUtils
+ dp转成px

```java
SizeUtils.dp2px(SCROLL_DISTANCE_CHANGE_BG_DP);
```

+ 获取宽高

```java
SizeUtils.getScreenHeight()
SizeUtils.getScreenWidth()
```



## 类中的成员变量/实例变量使用的时候必须判空
### 错误写法
```java
class A {
    private String fromPager="";
    void test(){
        if(fromPager.equals("peakmain")){

        }
    }
}
```

### 正确写法
#### 写法一
```java
class A {
    private String fromPager="";
    void test(){
        if(fromPager!=null&&fromPager.equals("peakmain")){

        }
    }
}
```

#### 写法二
```java
class A {
    private String fromPager="";
    void test(){
        if(fromPager==null){
            //业务逻辑处理
            return;
        }
        if(fromPager.equals("peakmain")){

        }
    }
}
```

## kotlin 中let、apply、run、also使用场景
### let
#### **使用场景**：
+ 主要用于对象不为 `null` 时执行某些操作（常用于可空类型）。
+ 可以通过 `it` 引用当前对象。
+ 通常用于避免多层嵌套的 `if-null` 检查。

#### 代码示例：
```kotlin
var context: Context? = null

context?.let {
    // 在 context 不为 null 时执行的逻辑
    Toast.makeText(it, "Context is not null", Toast.LENGTH_SHORT).show()
}

```

#### 适用场景
+ 这个值可能为空，需要判空处理

### <font style="color:rgba(0, 0, 0, 0.85);">apply</font>
#### **使用场景**：
+ 用于对对象的<font style="color:#DF2A3F;">多个属性进行初始化或修改</font>。
+ 通常用于配置 View 或对象的初始化。
+ 返回值是对象本身

#### 示例代码
```kotlin
var recyclerView: RecyclerView? = null

recyclerView?.apply {
    adapter = JourneyPreviewAdapter(context, items)
    layoutManager = LinearLayoutManager(context, RecyclerView.HORIZONTAL, false)
    setHasFixedSize(true)
}

```

#### 适合场景
+ 当需要对某个对象多次设置属性，如TextView设置背景颜色、字体大小、字体颜色

```kotlin
val person = Person().apply {
    name = "John"
    age = 30
}
println(person) // 输出：Person(name=John, age=30)
```

### run
#### **使用场景**：
+ 与 `let` 类似，但更注重在块内运行一段逻辑。
+ 可以直接访问 `this` 引用当前对象。
+ 通常用于执行 lambda 表达式，并返回一个结果。

#### 示例代码
```kotlin
var result = "Kotlin".run {
    println("Original: $this")
    length // 返回值
}
println("Length: $result") // 输出：Length: 6
```

#### 适用场景
+ 对一个对象执行逻辑，并返回计算结果

### also
+ 用于在链式调用中插入调试或打印操作

```kotlin
val person = Person().also {
    println("Creating person...")
    it.name = "John"
    it.age = 30
}
println(person) // 输出：Person(name=John, age=30)
```

### **总结对比**
| 方法 | 使用方式 | 作用域引用 | 返回值 | 适用场景 |
| --- | --- | --- | --- | --- |
| `let` | `obj?.let` | `it` | Lambda 表达式的结果 | 处理非空对象或转换结果 |
| `apply` | `obj.apply` | `this` | 对象本身 | 初始化或设置对象的多个属性 |
| `run` | `obj.run` | `this` | Lambda 表达式的结果 | 执行逻辑并返回结果，常用于计算 |
| `also` | `obj.also` | `it` | 对象本身 | 执行附加操作（如日志或调试），保持链式调用 |


## 使用setCompoundDrawablesWithIntrinsicBounds设置左、上、右、下四个方向的图标
+ 利用<font style="color:#DF2A3F;">setCompoundDrawablesWithIntrinsicBounds替换setCompoundDrawables</font>

不使用 `setCompoundDrawables` 的原因

+ 需要手动设置 Drawable 的边界
    - 需要手动调用 `setBounds()` 来定义每个 Drawable 的绘制边界，否则 `Drawable` 不会显示
    - 增加了额外的代码复杂度和出错几率

```java
Drawable leftDrawable = getResources().getDrawable(R.drawable.ic_example);
leftDrawable.setBounds(0, 0, leftDrawable.getIntrinsicWidth(), leftDrawable.getIntrinsicHeight());
textView.setCompoundDrawables(leftDrawable, null, null, null);
```

+ `setCompoundDrawablesWithIntrinsicBounds` 自动处理尺寸
    - `setCompoundDrawablesWithIntrinsicBounds` 提供了直接通过资源 ID 设置 `Drawable` 的方法，避免手动获取资源和设置边界，代码更简洁：

```java
textView.setCompoundDrawablesWithIntrinsicBounds(R.drawable.ic_peakmain, 0, 0, 0);
```

## Should not call Context. getDrawable or Resources. getDrawable directly
<font style="color:rgb(0, 0, 0) !important;">使用 </font>`<font style="color:rgb(0, 0, 0);">ContextCompat.getDrawable()</font>`

```java
// 不推荐（直接调用）
Drawable drawable = context.getDrawable(R.drawable.your_drawable);

// 推荐（兼容性调用）
Drawable drawable = ContextCompat.getDrawable(context, R.drawable.your_drawable);
```

<font style="color:rgb(0, 0, 0) !important;">使用 </font>`<font style="color:rgb(0, 0, 0);">ResourcesCompat.getDrawable()</font>`<font style="color:rgb(0, 0, 0) !important;">（当没有 Context 时)</font>

```java
// 不推荐
Drawable drawable = resources.getDrawable(R.drawable.your_drawable, theme);

// 推荐
Drawable drawable = ResourcesCompat.getDrawable(resources, R.drawable.your_drawable, theme);
```



## 使用 forEachIndexed 替代 for 循环，更加安全
```kotlin
lists.forEach { rowItems ->
    Row(
        Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(AtSpace.space_12)
    ) {
        // 添加边界检查确保安全访问
        for (index in rowItems.indices) {
            if (index >= 0 && index < rowItems.size) {
                HotelListGridItem(rowItems[index], index)
            }
        }
    }
}
```

### 问题分析
1. `index >= 0`** 永远为 true**：
    - `rowItems.indices` 返回的是一个有效的索引范围，从 0 开始
    - 因此通过 `for (index in rowItems.indices)` 得到的 index 值始终 >= 0
2. `index < rowItems.size`** 永远为 true**：
    - `rowItems.indices` 本身就保证了索引在有效范围内
    - 当执行到循环体内部时，index 必然小于 `rowItems.size`

### 实际问题所在
既然 `for (index in rowItems.indices)` 已经保证了索引安全，那为什么还会出现 `ArrayIndexOutOfBoundsException` 呢？

可能的原因包括：

1. **并发修改**：`rowItems` 在遍历过程中被其他线程修改
2. **作用域污染**：外部的 index 变量影响了当前作用域
3. **JVM 或 Compose 编译期问题**：在特定条件下出现的边界情况

### 建议解决方案
```kotlin
@Composable
fun HotelGridSection(chainResponses: List<ChainResponse>?) {
    if (chainResponses.isNullOrEmpty()) return
    val lists = chainResponses.chunked(2)
    Column(Modifier.padding(horizontal = AtSpace.space_18).padding(top = AtSpace.space_18)) {
        lists.forEach { rowItems ->
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(AtSpace.space_12)
            ) {
                // 使用 forEachIndexed 替代 for 循环，更加安全
                rowItems.forEachIndexed { index, item ->
                    HotelListGridItem(item, index)
                }
            }
        }
    }
}
```



## <font style="color:rgb(62, 52, 70);">Fragment 错误： NoSuchMethodException</font>
### 错误信息：
Unable to start activity ComponentInfo{com.atour.atourlife/com.atour.atourlife.main.activity.MainActivity}: androidx.fragment.app.Fragment$InstantiationException: Unable to instantiate fragment com.atour.atourlife.activity.dialog.MoreServiceDialog: could not find Fragment constructor

### 原因
MoreServiceDialog 类只定义了带参数的构造函数：

```java
  public MoreServiceDialog(Context context, JourneyOrderServiceResponse data, MoreServiceDialogCallback callBack)
```

+ Android Fragment 系统需要默认的无参构造函数来重新创建 Fragment 实例
+ 当应用进程被杀死后恢复时，系统无法通过反射创建 Fragment 实例

:::info
<font style="color:rgba(0, 0, 0, 0.85);">当系统因配置变更（如屏幕旋转）或内存不足等情况需要重建 Fragment 时，会通过 </font>**<font style="color:rgb(0, 0, 0) !important;">反射调用无参构造函数</font>**<font style="color:rgba(0, 0, 0, 0.85);"> 来创建新实例，而非使用带参构造函数或其他方式。</font>

:::

### 解决方案
为 MoreServiceDialog 添加默认构造函数：

```java
public class MoreServiceDialog extends BaseAtourDialogFragment {
    
    // 添加默认构造函数
    public MoreServiceDialog() {
        // 必须有这个无参构造函数
    }
    
    // 保留现有的带参构造函数
    public MoreServiceDialog(Context context, JourneyOrderServiceResponse data, MoreServiceDialogCallback callBack) {
        this.mCallBack = callBack;
        this.mDataInfo = data;
        this.mContext = context;
    }
    
    // ... 其他代码
}
```

:::info
**注意事项**

+ **Fragment 必须始终提供无参构造函数**
+ 参数应该通过 Bundle 和 setArguments()/getArguments() 方法传递
+ 避免在构造函数中直接传递复杂对象，应该使用 Parcelable 或基本数据类型通过 Bundle 传递

:::

