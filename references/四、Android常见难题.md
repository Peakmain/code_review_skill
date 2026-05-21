# <font style="color:rgb(51, 51, 51);">ProcessLifecycleInitializer报错</font>
## 错误信息
<font style="color:rgb(51, 51, 51);">ProcessLifecycleInitializer cannot be initialized lazily. Please ensure that you have: <meta-data android:name='androidx.lifecycle.ProcessLifecycleInitializer' android:value='androidx.startup' /> under InitializationProvider in your AndroidManifest.xml</font>

<font style="color:rgb(51, 51, 51);">com.shell.vmp.Vmc.iV(Native Method)</font>

## <font style="color:rgb(51, 51, 51);">解决方案</font>
+ 添加依赖

```java
implementation "androidx.startup:startup-runtime:1.2.0"
```

+ 在 `AndroidManifest.xml` 中添加初始化配置

```java
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false">
    <meta-data
        android:name="androidx.lifecycle.ProcessLifecycleInitializer"
        android:value="androidx.startup" />
</provider>
```

# <font style="color:rgb(51, 51, 51);">WebView 多进程目录问题</font>
## 错误信息
<font style="color:rgb(51, 51, 51);">Using WebView from more than one process at once with the same data directory is not supported. https://crbug.com/558377 : Current process com.atour.atourlife (pid 3610), lock owner com.atour.atourlife (pid 5734)</font>

<font style="color:rgb(51, 51, 51);">com.atour.atourlife.hybrid.HybridWebView.<init>(HybridWebView.java:48)</font>

## <font style="color:rgb(51, 51, 51);">解决方案</font>
```java
private void setWebViewDir() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
        String processName = getCurrentProcessName();
        if (!AtourLifeApplication.get().getApplicationContext().getPackageName().equals(processName)) {
            if (!TextUtils.isEmpty(processName)) {
                WebView.setDataDirectorySuffix(processName);
            }
        }
    }

}

private String getCurrentProcessName() {
    int pid = android.os.Process.myPid();
    ActivityManager manager = (ActivityManager) getContext().getSystemService(Context.ACTIVITY_SERVICE);
    for (ActivityManager.RunningAppProcessInfo processInfo : manager.getRunningAppProcesses()) {
        if (processInfo.pid == pid) {
            return processInfo.processName;
        }
    }
    return null;
}
```

# Android旧项目添加Compose
```kotlin
distributionUrl=https://services.gradle.org/distributions/gradle-7.5-bin.zip
```

```kotlin
classpath "com.android.tools.build:gradle:7.0.4"
ext.kotlin_version = '1.7.10'
```

```kotlin
buildFeatures {
    compose true
}
kotlinOptions {
    jvmTarget = '1.8'
}
composeOptions {
    kotlinCompilerExtensionVersion '1.3.0'
    kotlinCompilerVersion '1.6.10'
}

```

```kotlin
implementation("androidx.compose.ui:ui:1.2.1")
// Tooling support (Previews, etc.)
implementation("androidx.compose.ui:ui-tooling:1.2.1")
// Foundation (Border, Background, Box, Image, Scroll, shapes, animations, etc.)
implementation("androidx.compose.foundation:foundation:1.2.1")
// Material Design
implementation("androidx.compose.material:material:1.2.1")
// Material design icons
implementation("androidx.compose.material:material-icons-core:1.2.1")
implementation("androidx.compose.material:material-icons-extended:1.2.1")
```

+ 示例代码

```kotlin
val composeView: ComposeView? = fragmentView?.findViewById(R.id.compose_view)
composeView?.setContent {
    ComposeContent()
}
@Composable
fun ComposeContent() {
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(text = "这是一个 Compose 的 Text 组件")
        Button(onClick = { count++ }) {
            Text(text = "Compose 按钮点击次数: $count")
        }
    }
}
```

