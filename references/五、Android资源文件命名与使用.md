+ <font style="color:#FF0000;">【强制】</font><font style="color:#333332;">必须遵守，违反本约定或将会引起严重的后果； </font>
+ <font style="color:#333332;"></font><font style="color:#528135;">【推荐】</font><font style="color:#333332;">尽量遵守，长期遵守有助于系统稳定性和合作效率的提升； </font>
+ <font style="color:#2E5395;">【参考】</font><font style="color:#333332;">充分理解，技术意识的引导，是个人学习、团队沟通、项目合作的方向。</font>

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">资源文件需带模块前缀。</font>
### <font style="color:#333332;">原则</font>
+ **模块化项目**：所有资源文件（如 `drawable`、`layout`、`string`、`color` 等）必须带模块前缀，以避免跨模块命名冲突，提高可维护性。
+ **单模块 App**：可以不加前缀，但仍需保持资源命名语义清晰、易读。

### 规范示例
| 类型 | 模块化项目示例 | 单模块 App 示例 | 说明 |
| --- | --- | --- | --- |
| Drawable | module_home_icon_back | icon_back | 模块前缀+功能描述 |
| Layout | module_user_activity_profile | activity_profile | 模块前缀+布局类型+功能 |
| String | module_order_label_status | label_status | 模块前缀+功能描述 |
| Color | module_chat_color_primary | color_primary | 模块前缀+功能描述 |


## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">layout文件的命名方式</font>
### 基本原则
+ 命名格式：

```kotlin
module_componentType_function[_level]
```

+ 其中：
    - `module`：模块前缀（例如 `home`、`user`、`order` 等）
    - `componentType`：组件类型（`activity`、`fragment`、`dialog` 等）
    - `function`：该布局的具体功能或用途（可由多个单词构成，用下划线分隔）
    - `level`（可选）：层级标识，用于多级结构（`level1`, `level2`, `level3` 或 `group`, `child` 等）

:::color3
若项目为单模块 App，可省略模块前缀。

:::

### 命名规范示例
| 场景 | 命名示例 | 说明 |
| --- | --- | --- |
| Activity 布局 | home_activity_main.xml | Activity 对应布局，以 `module_activity_`开头 |
| Fragment 布局 | user_fragment_profile.xml | Fragment 对应布局，以 `module_fragment_`开头 |
| Dialog 布局 | common_dialog_loading.xml | Dialog 对应布局，以 `module_dialog_`开头 |
| Include 布局 | home_include_header.xml | 仅供 include 的布局，以 `module_include_`开头 |
| ListView 行布局 | order_list_item_detail.xml | ListView 行布局，以 `module_list_item_`开头 |
| RecyclerView item 布局（单级） | feed_recycle_item_post.xml | RecyclerView item 布局，以 `module_recycle_item_`开头 |
| RecyclerView item 布局（多级） | ①feed_recycle_item_post_level1.xml<br/>②feed_recycle_item_post_level2.xml | RecyclerView 多级 item，使用层级后缀标识 |
| RecyclerView 分组结构（推荐命名） | order_recycle_item_group.xml（一级）   order_recycle_item_child.xml（二级） | 分组型结构推荐使用 `group`、`child` |
| GridView item 布局 | album_grid_item_photo.xml | GridView item 布局，以 `module_grid_item_`开头 |


### 补充建议：
1. 布局文件名应尽量反映布局用途，不使用无意义的命名（如 `layout1.xml`、`test.xml`）。
2. 公共布局（如统一标题栏、通用加载状态）建议使用 `common_` 作为模块前缀。
3. 当布局复杂或由多种状态组成时，可进一步细分，例如：
    - `home_recycle_item_article_header.xml`
    - `home_recycle_item_article_footer.xml`
4. 命名全部使用小写字母与下划线 `_`，避免驼峰写法。

## <font style="color:#528135;">【推荐】</font>Drawable 资源命名规范
### 命名规则
采用 **小写单词 + 下划线** 的命名方式，格式如下：

```kotlin
module_function_view_state
```

### 字段说明
+ `module`：模块名（如 `login`、`home`、`user`）
+ `function`：业务功能描述（如 `tabs`、`btn`、`icon`）
+ `view`：控件类型或用途（如 `btn`、`icon`、`bg`）
+ `state`（可选）：控件状态限定词（如 `normal`、`pressed`、`selected`）



例如：

+ `login_btn_pressed`
+ `tabs_icon_home_normal`



:::info
**存放规则：**

+ 根据分辨率分别放入对应的 `drawable-mdpi`、`drawable-hdpi`、`drawable-xhdpi` 等目录中。
+ 若对包体积敏感，**建议仅保留一套资源**（例如 `drawable-xxhdpi`），由系统自动进行缩放

:::

### 常用状态限定词：
| 状态 | 说明 |
| --- | --- |
| `normal` | 默认状态 |
| `pressed` | 按下状态 |
| `focused` | 焦点状态 |
| `disabled` | 不可用状态 |
| `selected` | 选中状态 |


### 命名示例
| 资源类型 | 命名示例 | 说明 |
| --- | --- | --- |
| 按钮背景 | login_btn_pressed | 登录模块按钮按下状态 |
| 图标资源 | tabs_icon_home_normal | 底部导航“首页”图标默认状态 |
| 背景图片 | user_bg_profile_header | 用户中心顶部背景 |
| 分割线 | common_divider_horizontal | 通用水平分割线 |


### 注意事项：
+ 禁止使用驼峰命名，如 `loginBtnPressed`。
+ 不建议在名称中出现分辨率信息（如 `_hdpi`、`_xhdpi`），由目录区分。
+ 公共资源统一使用 `common_` 前缀。
+ 状态图可使用 `selector` 定义多态效果，命名示例：`login_btn_selector.xml`。



## <font style="color:#528135;">【推荐】</font>Anim 资源命名规范
### 命名规则
采用 **小写单词 + 下划线** 的方式命名，格式如下：

```kotlin
module_logic_[direction|index]
```

+ `module`：模块名（如 `login`、`home`、`common`）
+ `logic`：动画逻辑名称（如 `fade_in`、`push_down_in`）
+ `direction`：动画方向（如 `left`、`right`、`up`、`down`）
+ `index`：帧动画编号（如 `001`、`002`）



### Tween 动画(补间动画)
使用简单图像变换（如平移、缩放、透明度变化等）的动画资源。

命名示例：

| 动画类型 | 命名示例 | 说明 |
| --- | --- | --- |
| 渐入动画 | `common_fade_in` | 通用渐入效果 |
| 渐出动画 | `common_fade_out` | 通用渐出效果 |
| 下滑进入动画 | `home_push_down_in` | 从上向下进入 |
| 上滑退出动画 | `home_push_up_out` | 从下向上退出 |




### Frame 动画(逐帧动画)
由多张图片按顺序播放形成动画。

| 动画类型 | 命名示例 | 说明 |
| --- | --- | --- |
| 加载动画帧 | `loading_grey_001` | 第 1 帧灰色加载动画 |
| 加载动画帧 | `loading_grey_002` | 第 2 帧灰色加载动画 |
| 加载动画总文件 | `common_anim_loading.xml` | 帧动画 XML 文件 |


### 注意事项：
1.  公共动画统一使用 `common_` 前缀。
2. Tween 动画名称应语义化，能直观表达效果。
3. Frame 动画的帧文件保持命名一致并按序号递增（如 `_001`, `_002`, `_003`）。
4. 动画文件统一放置在 `res/anim` 目录中，不与 `drawable` 混放。



## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">color资源命名规范</font>
### 基本要求
**颜色值统一采用 **`**#AARRGGBB**`** 格式**（带透明度，语义化命名），例如

```xml
#FF33B5E5
```

+ 所有颜色资源统一存放在 `**module_colors.xml**` 文件中（例如：`home_colors.xml`、`common_colors.xml`）。
+ 命名一律使用 **小写字母 + 下划线 **`**_**`** 分隔**。

### 命名格式
```xml
module_logic_color
```

+ `module`：模块名（如 `login`、`home`、`user`、`common`）
+ `logic`：逻辑用途或组件描述（如 `btn_bg`、`title_text`、`divider`）
+ `color`：固定后缀，标识为颜色资源

### 示例
```xml
<color name="login_btn_bg_color">#FF33B5E5</color>
<color name="home_title_text_color">#FF222222</color>
<color name="common_divider_color">#FFE5E5E5</color>
```

### 语义化命名 和 颜色直命名（以色值命名）的区别
| 策略 | 示例 | 优点 | 缺点 | 推荐场景 |
| --- | --- | --- | --- | --- |
| **语义化命名** | `login_btn_bg_color` | 语义清晰，方便查找与统一管理 | 颜色变更需多处同步修改 | 设计稳定、颜色复用率高的场景 |
| **颜色直命名** | `color_33b5e5e5` | 快速开发，方便临时定义与维护 | 不易体现用途，难以统一风格 | 早期开发或 UI 频繁变化的项目 |


### 推荐实践
#### 项目初期（设计未稳定）
可采用 **颜色直命名方式**，如

```xml
<color name="color_33b5e5e5">#33B5E5E5</color>
```

优点是维护方便，快速修改即可生效。

#### **项目稳定期（设计规范已确定）**：
建议逐步过渡为 语义化命名方式，统一由 UI 规范驱动：

```xml
<color name="common_primary_color">#33B5E5E5</color>
<color name="common_text_hint_color">#99000000</color>
```

#### **公共颜色** 统一放置在 `common_colors.xml` 中，例如：
```xml
<color name="common_color_primary">#FF6200EE</color>
<color name="common_color_background">#FFFFFFFF</color>
```

#### 命名不应出现模块前缀和通用前缀混用，如 `common_login_btn_bg_color`，需保持一致。
:::info
+ 若团队已有稳定的 **设计规范与色板**，推荐使用 **语义化命名**。
+ 若团队偏向快速开发、UI 变动频繁，可采用 **色值命名（color_XXXXXX）**，并在项目后期逐步替换为语义化命名。

:::

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">dimen资源命名规范</font>
### 基本要求
+ **命名格式**：采用 **小写单词 + 下划线 **`**_**`** 分隔** 的方式。
+ 所有尺寸资源应统一存放在对应模块的 `module_dimens.xml` 文件中。

> 例如：`home_dimens.xml`、`user_dimens.xml`、`common_dimens.xml`。
>

单位统一使用 `**dp**` 或 `**sp**`，禁止在布局中直接写死数值



### 命名格式
```xml
module_description
```

+ `module`：模块前缀（如 `login`、`home`、`user`、`common`）
+ `description`：描述信息（可由多个单词组成，体现用途）

```xml
<dimen name="login_horizontal_line_height">1dp</dimen>
<dimen name="home_banner_height">180dp</dimen>
<dimen name="user_avatar_size">64dp</dimen>
```

### 分类命名建议
| 分类 | 命名示例 | 说明 |
| --- | --- | --- |
| **通用间距** | `common_margin_small`<br/>`common_margin_large` | 通用外边距 |
| **控件尺寸** | `home_button_height`<br/>`home_icon_size` | 控件大小 |
| **字体大小** | `common_text_size_title`<br/>`common_text_size_hint` | 字体尺寸，单位使用 `sp` |
| **分割线/边框** | `common_divider_height`<br/>`common_border_width` | 分割线或边框宽度 |
| **特殊布局尺寸** | `order_card_corner_radius` | 特定控件属性尺寸（如圆角） |


### 使用建议
#### 通用尺寸统一管理
项目中常用间距、字体大小等应集中放在 `common_dimens.xml` 中，并定义清晰的语义，如：

```xml
<dimen name="common_margin_small">4dp</dimen>
<dimen name="common_margin_medium">8dp</dimen>
<dimen name="common_margin_large">16dp</dimen>
<dimen name="common_text_size_title">18sp</dimen>
<dimen name="common_text_size_content">14sp</dimen>
```

#### 模块私有尺寸独立管理
仅在单个模块内使用的尺寸应写入该模块的 `module_dimens.xml` 文件中

#### 保持语义清晰、避免重复定义
+ 若同一功能存在多个相同值，应抽取为公共资源。
+ 避免无意义命名，如 `height_1`、`padding_5dp` 等。

#### 统一单位规则
+ UI 尺寸使用 `dp`，字体尺寸使用 `sp`。
+ 禁止混用单位，如 `px`

:::info
✅ **通用尺寸** → 放在 `common_dimens.xml`，命名以 `common_` 开头。

✅ **模块私有尺寸** → 放在 `module_dimens.xml`，命名以模块名前缀开头。

✅ **命名语义化**，避免直接写数值含义（如 `_16dp`、`_24sp`）。

:::

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">style 资源命名规范</font>
### 基本要求
+ 命名规则：采用

```xml
父Style名.当前Style名
```

的方式命名

+ **命名格式**：首字母大写，遵循驼峰命名规则（与其他资源类型区分）。
+ **存放位置**：统一写入对应模块的 `module_styles.xml` 文件中。

> 如：`home_styles.xml`、`login_styles.xml`、`common_styles.xml`
>

### 命名格式说明
```xml
<style name="ParentStyle.CurrentStyle">
    ...
</style>
```

| 字段 | 说明 |
| --- | --- |
| ParentStyle | 父级样式名（可为系统或自定义样式） |
| CurrentStyle | 当前样式在父样式基础上的扩展命名 |
| 大小写规则 | 每个单词首字母大写，使用`.`分隔层级 |


### 命名示例
| 场景 | 示例命名 | 说明 |
| --- | --- | --- |
| **Activity 主题样式** | `<style name="ParentTheme.ThisActivityTheme">` | 继承父主题，应用于当前 Activity |
| **通用按钮样式** | `<style name="Base.Button.Primary">` | 以 `Base`为父样式的主按钮样式 |
| **对话框样式** | `<style name="Base.Dialog.Transparent">` | 透明对话框样式 |
| **模块主题样式** | `<style name="Home.Theme.Light">` | 首页模块的浅色主题 |
| **文字样式** | `<style name="Common.Text.Title">` | 公共标题文字样式 |


### 推荐结构
在多模块项目中，建议按模块拆分并遵循层级命名，结构清晰如下：

```xml
<!-- common_styles.xml -->
<style name="Base.AppTheme" parent="Theme.MaterialComponents.DayNight.NoActionBar">
    <!-- 全局通用样式 -->
</style>

<style name="Base.Button" parent="Widget.MaterialComponents.Button">
    <item name="android:textAllCaps">false</item>
</style>

<style name="Base.Button.Primary" parent="Base.Button">
    <item name="backgroundTint">@color/common_color_primary</item>
</style>

<!-- home_styles.xml -->
<style name="Base.AppTheme.Home" parent="Base.AppTheme">
    <item name="colorPrimary">@color/home_color_primary</item>
    <item name="colorAccent">@color/home_color_accent</item>
</style>

<style name="Base.Text.HomeTitle" parent="Common.Text.Title">
    <item name="android:textColor">@color/home_color_title</item>
</style>
```

### 使用建议
1. **分层组织**
    - 公共基础样式（如主题、按钮、文字）放在 `common_styles.xml`。
    - 模块特定样式放在 `module_styles.xml`，继承自公共样式。
2. **命名保持层级语义化**
    - 例如：`Base.AppTheme` → `Base.AppTheme.Home` → `Base.AppTheme.Home.Dark`
    - 直观反映继承关系与使用场景。
3. **首字母大写、驼峰命名**
    - 与资源文件（小写+下划线）区分开，更符合 Android 官方命名风格。
4. **避免重复命名与循环继承**
    - 子样式只继承一层，防止层级过深难以维护。
5. **模块化维护**
    - 当模块数量多时，每个模块维护独立的 `xxx_styles.xml`，统一由主模块汇总导入。

:::info
✅ **使用层级命名（ParentStyle.CurrentStyle）**，结构清晰、易追踪继承关系。

✅ **首字母大写、驼峰命名**，与普通资源区分，符合 Android 官方规范。

✅ **按模块拆分维护**，统一在 `module_styles.xml` 中定义，减少样式冲突。

:::

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">string资源文件命名规范</font>
### 原则
所有字符串常量（包括 UI 文案、提示语、错误信息、按钮文字等）均应集中存放于 `module_strings.xml` 文件中，统一管理，禁止在代码中直接硬编码。

### **命名规则**：
字符串名称采用小写单词 + 下划线方式命名，格式如下：

```xml
模块名_逻辑名称
```

### 示例
```xml
<string name="module_login_tips">请输入正确的用户名和密码</string>
<string name="module_homepage_notice_desc">欢迎回来，祝您入住愉快！</string>
<string name="module_profile_btn_logout">退出登录</string>
```

### 注意事项：
1. **模块前缀**：
    - 多模块项目需添加模块名前缀（如 `module_login_`）。
    - 单模块 App 可省略模块前缀（如 `app_` 也可省略）。
2. **禁止硬编码**：
    - 所有界面显示文字必须引用 `@string/xxx`，禁止直接在布局文件或代码中使用硬编码文本。
3. **命名建议**：
    - 业务功能清晰、语义明确。
    - 相同模块内保持命名统一，如：  
`module_login_title`、`module_login_button_text`、`module_login_error_pwd`。
4. **国际化支持**：
    - 字符串文件应支持多语言，如 `values-en/strings.xml`、`values-zh/strings.xml`。
    - 所有可见文本均需加入多语言资源文件，确保国际化可扩展。
5. **统一管理**：
    - 建议按模块拆分 string 文件，如：
        * `module_login_strings.xml`
        * `module_order_strings.xml`
        * `module_profile_strings.xml`
    - 主模块（app）可建立统一的 `app_strings.xml` 管理全局通用字符串。

## <font style="color:#528135;">【推荐】</font><font style="color:#000000;">Id资源命名规范</font>
### 原则
资源 ID 命名需简洁明了，遵循 **驼峰命名法（camelCase）**，并建议以控件类型的缩写作为前缀，以便快速识别控件类型与用途。

### 命名规则
```java
控件缩写 + 功能描述
```

### 示例
```java
<TextView
    android:id="@+id/tvUserName"
    ... />

<Button
    android:id="@+id/btnLogin"
    ... />

<EditText
    android:id="@+id/etPassword"
    ... />

<ImageView
    android:id="@+id/ivAvatar"
    ... />
```

### 常用控件缩写表
| 控件类型 | 缩写 | 示例 |
| --- | --- | --- |
| LinearLayout | ll | `llContainer` |
| RelativeLayout | rl | `rlRoot` |
| ConstraintLayout | cl | `clContent` |
| FrameLayout | fl | `flHeader` |
| ScrollView | sv | `svMain` |
| ListView | lv | `lvOrders` |
| RecyclerView | rv | `rvMessages` |
| TextView | tv | `tvTitle` |
| EditText | et | `etUserName` |
| Button | btn | `btnConfirm` |
| ImageView | iv | `ivIcon` |
| CheckBox | cb | `cbRemember` |
| RadioButton | rb | `rbMale` |
| Switch | sw | `swEnable` |
| ProgressBar | progress_bar | `progress_barLoading` |
| DatePicker | date_picker | `date_pickerBirth` |


:::color2
+ 若控件类型较少使用（如 `ProgressBar`、`DatePicker`），可采用全称小写 + 下划线命名方式（如 `progress_bar`、`date_picker`），保持语义清晰。
+ 常见控件优先使用固定缩写前缀，保证团队命名一致性。

:::



