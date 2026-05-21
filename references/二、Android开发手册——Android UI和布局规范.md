#### 文章系列
+ [《Android开发手册——Android代码规范》](https://juejin.cn/post/7262162940971499557)

#### UI和布局规范
##### 1.不得使用Shape设置圆角
<!-- 这是一张图片，ocr 内容为： -->
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4ffac0ba8e1b423e8124a797863931e8~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=584&h=174&s=24480&e=png&b=f2f2f2)

###### 弊端分析：
如上图：过去我们设置一个背景圆角，通常会首先定义一个资源如下：

```plain
<?xml version="1.0" encoding="UTF-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@android:color/white" />
    <corners android:radius="@dimen/dimen_4" />
    <stroke
        android:width="@dimen/dimen_1"
        android:color="@color/color_E5E4E0" />
</shape>
```

当有圆角或者颜色变化，我们会再定义一个资源文件，当圆角的边框发生变化又会再定义一个资源，如下

<!-- 这是一张图片，ocr 内容为： -->
![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c67c0a535df448029d814b880c222a0a~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=712&h=140&s=29593&e=png&b=3b3d3f)

弊端已经很明显

1. **资源文件爆炸**：为每个稍有不同的背景创建新的Shape资源文件，导致资源文件数量激增。这会使APK大小变得庞大，并且增加维护成本
2. **可读性差**：当需要进行修改时，维护者需要查找并辨识正确的资源文件。这对于新加入团队的开发者来说可能是一项挑战，因为他们需要花费更多的时间来理解和管理这些不同的资源文件
3. **灵活性受限**：使用 Shape 限制了对于背景样式的动态修改。例如，如果需要在运行时根据用户输入或者特定条件更改背景样式，Shape 的使用就显得捉襟见肘

###### 替代方案
使用[BasicUI](https://github.com/Peakmain/BasicUI)库中的ShapeLinearLayout、ShapeTextView、ShapeConstraintLayout进行替换  
github使用文档：[TextView、LinearLayout和ConstraintLayout的封装](https://github.com/Peakmain/BasicUI/wiki/TextView%E3%80%81LinearLayout%E5%92%8CConstraintLayout%E7%9A%84%E5%B0%81%E8%A3%85)

**效果**  
<!-- 这是一张图片，ocr 内容为： -->
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bca66f5d326345d39639e69a8e9fd831~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=228&h=495&s=55975&e=png&b=fafafa)

**ShapeTextView**

这个支持设置背景颜色，背景的圆角，线条的颜色，线条的宽度，支持文字上下左右图片资源两者居中，减少布局嵌套

```xml
<com.peakmain.ui.widget.ShapeTextView
  android:id="@+id/shape_text_view"
  android:layout_width="@dimen/space_100"
  android:layout_height="@dimen/space_100"
  android:layout_centerInParent="true"
  android:gravity="center"
  android:textColor="@color/color_white"
  android:textSize="28sp"
  tools:text="A"
  app:shapeTvRadius="@dimen/space_6"
  app:shapeTvBackgroundColor="#333333" />
```

一共有以下属性

```xml

<!--自定以CircleImageView属性-->
<declare-styleable name="ShapeTextView">
  <!--设置线条的宽度-->
  <attr name="shapeTvStrokeWidth" format="dimension|reference" />
  <!--设置线条的颜色-->
  <attr name="shapeTvStrokeColor" format="color|reference" />
  <!--设置弧度-->
  <attr name="shapeTvRadius" format="dimension|reference" />
  <!--设置背景颜色-->
  <attr name="shapeTvBackgroundColor" format="color|reference" />
  <!--设置渐变开始颜色-->
  <attr name="shapeTvStartColor" format="color|reference" />
  <!--设置渐变结束颜色-->
  <attr name="shapeTvEndColor" format="color|reference" />
  <!--设置渐变方向-->
  <attr name="shapeTvOriention" format="integer">
    <enum name="LEFT_RIGHT" value="0" />
    <enum name="TOP_BOTTOM" value="1" />
  </attr>

  <!--RECTANGLE=0, OVAL=1, LINE=2, RING=3 默认是0-->
  <attr name="shapeTvShape" format="enum">
    <enum name="rectangle" value="0" />
    <enum name="oval" value="1" />
    <enum name="line" value="2" />
    <enum name="ring" value="3" />
  </attr>

  <!--是否开启点击后动画效果 默认false-->
  <attr name="shapeTvActiveMotion" format="boolean" />
  <!--按下后的背景颜色,也就是android:status_pressed功能-->
  <attr name="shapeTvPressedColor" format="color|reference" />
  <!--四周的圆角-->
  <attr name="shapeTvTopLeftRadius" format="dimension|reference" />
  <attr name="shapeTvTopRightRadius" format="dimension|reference" />
  <attr name="shapeTvBottomLeftRadius" format="dimension|reference" />
  <attr name="shapeTvBottomRightRadius" format="dimension|reference" />
</declare-styleable>

```

**ShapeLinearLayout**

使用

```xml
    <com.peakmain.ui.widget.ShapeLinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        app:shapeLlBackgroundColor="@color/white"
        app:shapeLlRadius="4dp" />
```

一共有以下几个属性

```xml
<!--自定义LinearLayout-->
<declare-styleable name="ShapeLinearLayout">

  <attr name="shapeLlStrokeWidth" format="dimension|reference" />
  <attr name="shapeLlStrokeColor" format="color|reference" />
  <!--background color-->
  <attr name="shapeLlBackgroundColor" format="color|reference" />
  <!--background radius-->
  <attr name="shapeLlRadius" format="dimension|reference" />
  <attr name="shapeLlStartColor" format="color|reference" />
  <attr name="shapeLlEndColor" format="color|reference" />
  <!--四周的圆角-->
  <attr name="shapeLlTopLeftRadius" format="dimension|reference" />
  <attr name="shapeLlTopRightRadius" format="dimension|reference" />
  <attr name="shapeLlBottomLeftRadius" format="dimension|reference" />
  <attr name="shapeLlBottomRightRadius" format="dimension|reference" />
</declare-styleable>

```

**ShapeConstraintLayout**

使用

```xml
<com.peakmain.ui.widget.ShapeConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:app="http://schemas.android.com/apk/res-auto"
  android:layout_width="match_parent"
  android:layout_height="wrap_content"
  android:paddingTop="@dimen/dimen_150"
  android:paddingBottom="@dimen/dimen_150"
  app:shapeClBackgroundColor="@color/white"
  app:shapeClTopLeftRadius="@dimen/dimen_4"
  app:shapeClTopRightRadius="@dimen/dimen_4">
```

一共有以下属性

```xml
<declare-styleable name="ShapeConstraintLayout">

  <attr name="shapeClStrokeWidth" format="dimension|reference" />
  <attr name="shapeClStrokeColor" format="color|reference" />
  <!--background color-->
  <attr name="shapeClBackgroundColor" format="color|reference" />
  <!--background radius-->
  <attr name="shapeClRadius" format="dimension|reference" />
  <attr name="shapeClStartColor" format="color|reference" />
  <attr name="shapeClEndColor" format="color|reference" />
  <!--四周的圆角-->
  <attr name="shapeClTopLeftRadius" format="dimension|reference" />
  <attr name="shapeClTopRightRadius" format="dimension|reference" />
  <attr name="shapeClBottomLeftRadius" format="dimension|reference" />
  <attr name="shapeClBottomRightRadius" format="dimension|reference" />
</declare-styleable>

```

##### 2. 使用自定义AlertDialog替换DialogFragment
+ 这里场景指的是点击的时候弹出Dialog的场景
+ 如果涉及到更复杂的逻辑，比如旋转屏幕或Activity生命周期变化时保持状态，或者需要与Activity进行交互，推荐使用DialogFragment
+ 使用的类是[AlertDialog](https://github.com/Peakmain/BasicUI/blob/master/ui/src/main/java/com/peakmain/ui/dialog/AlertDialog.kt)

**使用**

支持从底部弹出，支持宽度全屏，可设置动画

```java
      AlertDialog dialog = new AlertDialog.Builder(ImagePreviewActivity.this)
                .setContentView(R.layout.dialog_show_image_deal)
                .fromBottom(true)
                // Set click events for view
                .setOnClickListener(R.id.bt_logout, new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                    }
                })
                //set animation
                .setAnimation(R.style.dialog_from_bottom_anim)
                //Eject from bottom
                .fromButtom(true)
                //set width  MATCH_PARENT
                .setFullWidth()
                .show();
```

或

```java
       AlertDialog dialog = new AlertDialog.Builder(ImagePreviewActivity.this)
                                    .setContentView(R.layout.dialog_show_image_deal)
                                    .fromButtom(true)
                                    // Set click events for view
                                    .addOnClickListener(R.id.bt_logout, new Function1<AlertDialog, Unit>() {
                                        @Override
                                        public Unit invoke(AlertDialog alertDialog) {
                                            //alertDialog
                                            return null;
                                        }
                                    })
                                    //set animation
                                    .setAnimation(R.style.dialog_from_bottom_anim)
                                    //Eject from bottom
                                    .fromButtom(true)
                                    //set width  MATCH_PARENT
                                    .setFullWidth()
                                    .show();
```

##### 3.实战AlertDialog与ShapeConstraintLayout和ShapeTextView一起使用
我们经常会遇到下述图片场景

<!-- 这是一张图片，ocr 内容为： -->
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/98840704c39e4f24b4b7dbc8fce61709~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=322&h=314&s=93655&e=png&b=ffffff)

+ 中间文字区域是个可滚动区域
+ 底部按钮`我知道了`，是一个背景圆角且固定在底部
+ 弹框不超过某个高度，比如屏幕高度的1/2或者2/3
+ 宽度一般是屏幕宽度的2/3或者4/5

一般布局写法如下

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:paddingBottom="@dimen/dp_16"
    android:layout_height="wrap_content">

    <!--  顶部-背景图   -->
    <ImageView
        android:id="@+id/iv_bg_top_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="@dimen/dp_94"
        android:background="@drawable/bg_announcement"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!--  顶部-标题   -->
    <TextView
        android:id="@+id/tv_title_top_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginLeft="@dimen/dp_16"
        android:layout_marginTop="@dimen/dp_16"
        android:layout_marginRight="@dimen/dp_16"
        android:text="@string/libhotel_hotel_announcement"
        android:textColor="@color/white"
        android:textSize="@dimen/sp_17"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!--  中间部分：弹窗内容  -->
    <ScrollView
        android:id="@+id/sv_content_middle_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/iv_bg_top_dialog_announcement">

        <RelativeLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content">
            <!--  中间部分：弹窗内容  -->
            <TextView
                android:id="@+id/tv_content_middle_dialog_announcement"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginLeft="@dimen/dp_16"
                android:layout_marginRight="@dimen/dp_16"
                android:paddingTop="@dimen/dp_16"
                android:text="酒店全房型不能升级，SOLO单房公共卫生间，敬请谅解"
                android:textColor="@color/color_194D53"
                android:textSize="@dimen/sp_13" />
        </RelativeLayout>

    </ScrollView>

    <!--  底部：按钮 我知道了 -->
    <TextView
        android:id="@+id/tv_i_know_bottom_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginLeft="@dimen/dp_16"
        android:layout_marginTop="@dimen/dp_16"
        android:layout_marginRight="@dimen/dp_16"
        android:background="@drawable/libhotel_bg_shape_rectangle_circle_6cbd9b_4"
        android:text="@string/libhotel_i_know"
        android:textColor="@color/white"
        android:gravity="center"
        android:paddingTop="@dimen/dp_12"
        android:paddingBottom="@dimen/dp_12"
        android:textSize="@dimen/sp_14"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/sv_content_middle_dialog_announcement" />

</androidx.constraintlayout.widget.ConstraintLayout>

```

正如我们第一条所说，不得使用shape绘制圆角，而应该使用ShapeTextView和ShapeConstraintLayout,以下是修改后的布局

```xml
<?xml version="1.0" encoding="utf-8"?>
<com.peakmain.ui.widget.ShapeConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/cl_root"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:paddingBottom="@dimen/dp_16"
    app:shapeClBackgroundColor="@color/white"
    app:shapeClRadius="@dimen/dimen_8">

    <!--  顶部-背景图   -->
    <ImageView
        android:id="@+id/iv_bg_top_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="@dimen/dp_94"
        android:background="@drawable/bg_announcement"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!--  顶部-标题   -->
    <TextView
        android:id="@+id/tv_title_top_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginLeft="@dimen/dp_16"
        android:layout_marginTop="@dimen/dp_16"
        android:layout_marginRight="@dimen/dp_16"
        android:text="@string/libhotel_hotel_announcement"
        android:textColor="@color/white"
        android:textSize="@dimen/sp_17"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <!--  底部：按钮 我知道了 -->

    <ScrollView
        android:id="@+id/sv_content_middle_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginBottom="@dimen/dimen_16"
        app:layout_constrainedHeight="true"
        app:layout_constraintBottom_toTopOf="@id/tv_i_know_bottom_dialog_announcement"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/iv_bg_top_dialog_announcement">

        <TextView
            android:id="@+id/tv_content_middle_dialog_announcement"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginLeft="@dimen/dp_16"
            android:layout_marginRight="@dimen/dp_16"
            android:paddingTop="@dimen/dp_16"
            android:textColor="@color/color_194D53"
            android:textSize="@dimen/sp_13"
            tools:text="测试数据"
           />
    </ScrollView>

    <com.peakmain.ui.widget.ShapeTextView
        android:id="@+id/tv_i_know_bottom_dialog_announcement"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginLeft="@dimen/dp_16"
        android:layout_marginRight="@dimen/dp_16"
        android:gravity="center"
        android:paddingTop="@dimen/dp_12"
        android:paddingBottom="@dimen/dp_12"
        android:text="@string/libhotel_i_know"
        android:textColor="@color/white"
        android:textSize="@dimen/sp_14"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:shapeTvBackgroundColor="@color/color_6CBD9B"
        app:shapeTvRadius="@dimen/dimen_4" />

</com.peakmain.ui.widget.ShapeConstraintLayout>

```

我简化下代码，对设置圆角的TextView代码进行对比

<!-- 这是一张图片，ocr 内容为： -->
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3f2a15d4e1714d74a1ef9a6f0fb7e827~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1524&h=391&s=101744&e=png&b=ffffff)

**Dialog设置最大高度**

```kotlin
private fun dealWithAnnounceDialog(content: String) {
    val announceDialog = AlertDialog.Builder(this)
        .setContentView(R.layout.libhotel_dialog_announcement)
        .setText(R.id.tv_content_middle_dialog_announcement, content)
        .setWidthAndHeight(SizeUtils.screenWidth * 4 / 5, ViewGroup.LayoutParams.WRAP_CONTENT)
        .addOnClickListener(R.id.tv_i_know_bottom_dialog_announcement) {
            it?.dismiss()
        }
        .create()
    val view = announceDialog.getView<ConstraintLayout>(R.id.cl_root)
    view?.addOnGlobalLayoutListener {
        val layoutParams = view.layoutParams
        val height = view.measuredHeight
        if (height > SizeUtils.screenHeight * 1 / 2) {
            layoutParams?.height = SizeUtils.screenHeight * 1 / 2
            view.layoutParams = layoutParams
        }
    }
    announceDialog.show()

}
```

设置高度最大为屏幕的高度的1/2

##### 4.Glide设置圆角
+ 使用的类为[ImageLoader](https://github.com/Peakmain/BasicUI/blob/master/ui/src/main/java/com/peakmain/ui/imageLoader/ImageLoader.kt)
+ 简单使用

```java
ImageLoader.getInstance().displayImage(this, data.get(0).getUrl(), mImageView);
```

+ 占位图的使用

```java
ImageLoader.getInstance().displayImage(this, data.get(1).getUrl(), mImageView, R.mipmap.ic_default_portrait);
```

+ 圆角图片

```java
ImageLoader.getInstance().displayImageRound(this, data.get(2).getUrl(), mImageView,50 ,0);
```

+ 指定每个角是否需要圆角，设置它们为 true 或 false 来控制四个角是否圆角化

```java
ImageLoader.instance.displayImageRound(
    item.image,
    imageView,
    R.drawable.icon_loading,
    leftTop = true,
    rightTop = true,
    leftBottom = false,
    false,
    SizeUtils.dp2px(8f).toFloat()//圆角大小
)
```

+ 指定图片的大小

```java
ImageLoader.getInstance().displayImage(this,data.get(4).getUrl(),mImageView,800,800,0);
```

+ 切换图片加载库

```java
ImageLoader.getInstance().exchangeImageLoader(切换的库)
```

+ 设置user-agent，默认是userAgent的值是Android

```java
ImageLoader.instance.userAgent("自定义UserAgent")
```

#### 结束
+ 更多封装UI大家可以看 [BasicUI](https://github.com/Peakmain/BasicUI/wiki)的github

