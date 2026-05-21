## 1. 密码学安全规范
### 1.1 【强制】禁止使用常量初始化矢量（IV）
**风险等级**：高危  
**说明**：

+ 常量初始化向量会显著降低密码安全性，容易受到字典攻击和重放攻击
+ IV的作用是为密文的第一个block提供随机性，确保相同明文生成不同密文
+ AES-CBC模式下必须使用安全的随机IV

**正确实现**：

```java
public class SecureCryptoHelper {
    private static final int IV_LENGTH = 16; // AES block size
    
    public static IvParameterSpec generateSecureIV() {
        byte[] iv = new byte[IV_LENGTH];
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(iv);
        return new IvParameterSpec(iv);
    }
    
    // 完整加密示例
    public static byte[] encryptData(byte[] data, SecretKey key) throws Exception {
        IvParameterSpec iv = generateSecureIV();
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        
        byte[] encrypted = cipher.doFinal(data);
        // 需要将IV与密文一起存储/传输
        ByteBuffer byteBuffer = ByteBuffer.allocate(iv.getIV().length + encrypted.length);
        byteBuffer.put(iv.getIV());
        byteBuffer.put(encrypted);
        return byteBuffer.array();
    }
}
```

**错误示例**：

```java
// 反例1：硬编码IV
IvParameterSpec iv = new IvParameterSpec("1234567890123456".getBytes());

// 反例2：使用固定种子
SecureRandom predictableRandom = new SecureRandom("fixedSeed".getBytes());
byte[] predictableIV = new byte[16];
predictableRandom.nextBytes(predictableIV);
```

### 1.2 【强制】AES/DES/DESede加密禁止使用ECB模式
**风险等级**：高危  
**说明**：

+ ECB模式相同明文块生成相同密文块，泄露数据模式
+ 对于大块数据，ECB模式会暴露数据的结构性信息
+ 建议使用CBC、CTR或GCM等更安全的模式

**推荐模式**：

```java
public class EncryptionManager {
    // 推荐使用CBC模式
    private static final String TRANSFORMATION_CBC = "AES/CBC/PKCS5Padding";
    
    // 或者使用GCM模式（推荐用于新项目）
    private static final String TRANSFORMATION_GCM = "AES/GCM/NoPadding";
    
    public static byte[] encryptWithGCM(byte[] data, SecretKey key) throws Exception {
        byte[] iv = new byte[12]; // GCM推荐12字节IV
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(iv);
        
        GCMParameterSpec parameterSpec = new GCMParameterSpec(128, iv);
        Cipher cipher = Cipher.getInstance(TRANSFORMATION_GCM);
        cipher.init(Cipher.ENCRYPT_MODE, key, parameterSpec);
        
        byte[] cipherText = cipher.doFinal(data);
        // 将IV与密文一起存储
        return combineIvAndCipherText(iv, cipherText);
    }
}
```

## 2. 应用组件安全
### 2.1 【强制】android:allowBackup必须设置为false
**风险等级**：中危  
**说明**：

+ 防止应用数据被恶意应用通过备份机制导出
+ 保护用户敏感信息不被未授权访问

**配置示例**：

```xml
<application
    android:name=".MyApplication"
    android:allowBackup="false"
    android:fullBackupContent="@xml/backup_rules" <!-- 如果必须备份，定义明确规则 -->
    tools:ignore="AllowBackup,GoogleAppIndexingWarning">
    
    <!-- 其他组件配置 -->
</application>

```

**备份规则配置**（如需部分备份）：

```xml
<!-- res/xml/backup_rules.xml -->
<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
    <!-- 排除敏感数据 -->
    <exclude domain="sharedpref" path="user_credentials.xml"/>
    <exclude domain="database" path="sensitive_data.db"/>
    <exclude domain="file" path="private_files/"/>
    
    <!-- 包含非敏感数据 -->
    <include domain="sharedpref" path="app_preferences.xml"/>
</full-backup-content>

```

### 2.2 【强制】组件导出权限严格控制
**风险等级**：高危

**说明**：

+ 避免组件被其他应用恶意调用
+ 根据最小权限原则设置exported属性

**安全配置**：

```xml
<!-- Activity安全配置 -->
<activity
    android:name=".MainActivity"
    android:exported="true"> <!-- 主Activity通常需要导出 -->
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
<!-- 内部Activity不应导出 -->
<activity
    android:name=".InternalSettingsActivity"
    android:exported="false"
    android:permission="com.example.app.INTERNAL_PERMISSION">
</activity>
<!-- Service安全配置 -->
<service
    android:name=".BackgroundService"
    android:exported="false"
    android:permission="com.example.app.SERVICE_PERMISSION">
</service>
<!-- BroadcastReceiver安全配置 -->
<receiver
    android:name=".MyReceiver"
    android:exported="false">
</receiver>
<!-- 需要接收系统广播的Receiver -->
<receiver
    android:name=".BootReceiver"
    android:exported="true"
    android:permission="android.permission.BOOT_COMPLETED">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>

```

### 2.3 【强制】发布版本android:debuggable必须为false
**风险等级**：中危

**说明**：

+ 防止应用被调试分析，泄露敏感逻辑和数据
+ 生产环境必须关闭调试功能

**Gradle配置**：

```groovy
android {
    buildTypes {
        debug {
            debuggable true
            minifyEnabled false
        }
        release {
            debuggable false
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            
            // 额外的发布配置
            shrinkResources true
            zipAlignEnabled true
        }
    }
}
```

## 3. 网络安全
### 3.1 【强制】HTTPS通信严格验证
**风险等级**：高危  
**说明**：

+ 防止中间人攻击
+ 确保与可信服务器建立安全连接

**安全实现**：

```java
public class SecureHttpClient {
    private static final String TRUSTED_HOSTNAME = "api.yourapp.com";
    
    public static OkHttpClient createSecureClient() {
        try {
            // 创建证书验证TrustManager
            X509TrustManager trustManager = createStrictTrustManager();
            
            // 创建SSLContext
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, new TrustManager[]{trustManager}, new SecureRandom());
            
            return new OkHttpClient.Builder()
                    .sslSocketFactory(sslContext.getSocketFactory(), trustManager)
                    .hostnameVerifier(createStrictHostnameVerifier())
                    .build();
                    
        } catch (Exception e) {
            throw new RuntimeException("Failed to create secure HTTP client", e);
        }
    }
    
    private static X509TrustManager createStrictTrustManager() {
        return new X509TrustManager() {
            @Override
            public void checkClientTrusted(X509Certificate[] chain, String authType) 
                throws CertificateException {
                // 验证客户端证书（如需要）
                if (chain == null || chain.length == 0) {
                    throw new CertificateException("No client certificates provided");
                }
            }
            
            @Override
            public void checkServerTrusted(X509Certificate[] chain, String authType) 
                throws CertificateException {
                if (chain == null || chain.length == 0) {
                    throw new CertificateException("No server certificates provided");
                }
                
                // 验证证书链
                for (X509Certificate cert : chain) {
                    cert.checkValidity();
                    // 额外的证书验证逻辑
                    verifyCertificate(cert);
                }
                
                // 可以添加证书锁定（Certificate Pinning）
                verifyCertificatePinning(chain[0]);
            }
            
            @Override
            public X509Certificate[] getAcceptedIssuers() {
                return new X509Certificate[0]; // 返回空数组表示不信任任何CA
            }
        };
    }
    
    private static HostnameVerifier createStrictHostnameVerifier() {
        return (hostname, session) -> {
            // 严格的主机名验证
            if (!TRUSTED_HOSTNAME.equals(hostname)) {
                Log.w("Security", "Rejected untrusted hostname: " + hostname);
                return false;
            }
            
            // 使用默认验证器进行额外验证
            HostnameVerifier defaultVerifier = HttpsURLConnection.getDefaultHostnameVerifier();
            return defaultVerifier.verify(hostname, session);
        };
    }
}
```

### 3.2 【强制】WebView安全设置
**风险等级**：中危

**完整安全配置**：

```java
public class SecureWebViewHelper {
    
    public static void configureWebViewSecurity(WebView webView) {
        WebSettings settings = webView.getSettings();
        
        // 基础安全设置
        settings.setAllowFileAccess(false);
        settings.setAllowFileAccessFromFileURLs(false);
        settings.setAllowUniversalAccessFromFileURLs(false);
        settings.setAllowContentAccess(false);
        
        // JavaScript安全
        settings.setJavaScriptEnabled(true); // 如必须启用
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        
        // 其他安全设置
        settings.setSavePassword(false);
        settings.setSaveFormData(false);
        settings.setGeolocationEnabled(false);
        
        // 针对API级别调整
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            settings.setAllowUniversalAccessFromFileURLs(false);
        }
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            settings.setMediaPlaybackRequiresUserGesture(true);
        }
        
        // 移除不安全的接口
        removeDangerousInterfaces(webView);
    }
    
    // 安全地添加JavaScript接口
    public static void addSecureJavascriptInterface(WebView webView, Object object, String name) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            webView.addJavascriptInterface(object, name);
        } else {
            Log.w("Security", "JavascriptInterface not supported below API 17");
        }
    }
    
    // 安全的WebViewClient实现
    public static class SecureWebViewClient extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            String url = request.getUrl().toString();
            
            // URL白名单验证
            if (!isUrlAllowed(url)) {
                Log.w("Security", "Blocked navigation to: " + url);
                return true; // 阻止导航
            }
            
            // 防止恶意scheme
            if (hasDangerousScheme(url)) {
                return true;
            }
            
            return super.shouldOverrideUrlLoading(view, request);
        }
        
        private boolean isUrlAllowed(String url) {
            // 实现URL白名单逻辑
            return url.startsWith("https://yourapp.com/") || 
                   url.startsWith("https://cdn.yourapp.com/");
        }
        
        private boolean hasDangerousScheme(String url) {
            String lowerUrl = url.toLowerCase();
            return lowerUrl.startsWith("file://") || 
                   lowerUrl.startsWith("content://") ||
                   lowerUrl.startsWith("sms:") ||
                   lowerUrl.startsWith("tel:") ||
                   lowerUrl.startsWith("mailto:");
        }
    }
}
```

## 4. 数据安全
### 4.1 【强制】禁止在Log中打印敏感信息
**风险等级**：中危

**安全日志实践**：

```java
public class SecureLogger {
    private static final boolean IS_DEBUG = BuildConfig.DEBUG;
    
    // 敏感信息模式（用于检测和过滤）
    private static final Pattern SENSITIVE_PATTERNS = Pattern.compile(
        "(password|pwd|token|auth|key|secret|credit.?card|ssn|social.?security)",
        Pattern.CASE_INSENSITIVE
    );
    
    public static void d(String tag, String message) {
        if (IS_DEBUG) {
            String safeMessage = sanitizeMessage(message);
            Log.d(tag, safeMessage);
        }
    }
    
    public static void i(String tag, String message) {
        String safeMessage = sanitizeMessage(message);
        Log.i(tag, safeMessage);
    }
    
    public static void e(String tag, String message, Throwable throwable) {
        String safeMessage = sanitizeMessage(message);
        Log.e(tag, safeMessage, throwable);
    }
    
    private static String sanitizeMessage(String message) {
        if (message == null) return null;
        
        // 检测并过滤敏感信息
        if (containsSensitiveInfo(message)) {
            return "[FILTERED: Contains sensitive information]";
        }
        
        return message;
    }
    
    private static boolean containsSensitiveInfo(String message) {
        return SENSITIVE_PATTERNS.matcher(message).find();
    }
    
    // 安全地记录用户ID等标识信息
    public static String secureUserId(String userId) {
        if (userId == null || userId.length() <= 4) {
            return "***";
        }
        return userId.substring(0, 2) + "***" + userId.substring(userId.length() - 2);
    }
}
```

**使用示例**：

```java
// 正确使用
String userToken = getAuthToken();
SecureLogger.d("Auth", "User authentication initiated for: " + SecureLogger.secureUserId(userId));

// 错误示例 - 直接记录敏感信息
Log.d("Auth", "User token: " + userToken); // 反例
```

### 4.2 【强制】本地加密密钥不能硬编码
**风险等级**：高危

**安全密钥管理**：

```java
public class SecureKeyManager {
    private static final String ANDROID_KEYSTORE = "AndroidKeyStore";
    private static final String KEY_ALIAS = "com.yourapp.encryption_key";
    
    /**
     * 使用Android KeyStore安全生成和存储密钥
     */
    public static SecretKey getOrCreateSecretKey() throws Exception {
        KeyStore keyStore = KeyStore.getInstance(ANDROID_KEYSTORE);
        keyStore.load(null);
        
        if (!keyStore.containsAlias(KEY_ALIAS)) {
            return generateNewSecretKey();
        }
        
        KeyStore.SecretKeyEntry secretKeyEntry = (KeyStore.SecretKeyEntry) keyStore.getEntry(KEY_ALIAS, null);
        return secretKeyEntry.getSecretKey();
    }
    
    private static SecretKey generateNewSecretKey() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE);
        
        KeyGenParameterSpec keyGenParameterSpec = new KeyGenParameterSpec.Builder(
            KEY_ALIAS,
            KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
            .setBlockModes(KeyProperties.BLOCK_MODE_CBC)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_PKCS7)
            .setRandomizedEncryptionRequired(true)
            .setUserAuthenticationRequired(true) // 可选：需要用户认证
            .setUserAuthenticationValidityDurationSeconds(30) // 认证有效期
            .build();
            
        keyGenerator.init(keyGenParameterSpec);
        return keyGenerator.generateKey();
    }
    
    /**
     * 安全存储数据
     */
    public static byte[] encryptData(byte[] data) throws Exception {
        SecretKey secretKey = getOrCreateSecretKey();
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS7Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        
        byte[] iv = cipher.getIV();
        byte[] encrypted = cipher.doFinal(data);
        
        // 组合IV和加密数据
        return combineIvAndData(iv, encrypted);
    }
}
```

## 5. 文件与存储安全
### 5.1 【推荐】Zip文件路径安全
**风险等级**：中危

**安全解压实现**：

```java
public class SecureZipExtractor {
    
    public static void extractZipSecurely(File zipFile, File targetDir) throws Exception {
        try (ZipFile zip = new ZipFile(zipFile)) {
            Enumeration<? extends ZipEntry> entries = zip.entries();
            
            while (entries.hasMoreElements()) {
                ZipEntry entry = entries.nextElement();
                
                // 检查路径遍历攻击
                if (isPathTraversal(entry.getName(), targetDir)) {
                    throw new SecurityException("Potential path traversal attack detected: " + entry.getName());
                }
                
                // 检查绝对路径
                if (new File(entry.getName()).isAbsolute()) {
                    throw new SecurityException("Absolute path not allowed: " + entry.getName());
                }
                
                // 检查符号链接（如果支持）
                if (entry.isUnix() && isSymbolicLink(entry)) {
                    throw new SecurityException("Symbolic links not allowed");
                }
                
                File outputFile = new File(targetDir, entry.getName());
                
                // 确保输出文件在目标目录内
                if (!outputFile.getCanonicalPath().startsWith(targetDir.getCanonicalPath())) {
                    throw new SecurityException("Path traversal attempt: " + entry.getName());
                }
                
                // 创建目录结构
                if (entry.isDirectory()) {
                    if (!outputFile.exists() && !outputFile.mkdirs()) {
                        throw new IOException("Failed to create directory: " + outputFile.getAbsolutePath());
                    }
                } else {
                    // 解压文件
                    extractFile(zip, entry, outputFile);
                }
            }
        }
    }
    
    private static boolean isPathTraversal(String entryName, File targetDir) throws IOException {
        File file = new File(targetDir, entryName);
        
        // 检查路径遍历模式
        if (entryName.contains("..") || entryName.contains("./") || entryName.contains("\\")) {
            return true;
        }
        
        // 规范路径检查
        String canonicalPath = file.getCanonicalPath();
        String canonicalTarget = targetDir.getCanonicalPath();
        
        return !canonicalPath.startsWith(canonicalTarget + File.separator);
    }
    
    private static void extractFile(ZipFile zip, ZipEntry entry, File outputFile) throws IOException {
        // 确保父目录存在
        File parent = outputFile.getParentFile();
        if (!parent.exists() && !parent.mkdirs()) {
            throw new IOException("Failed to create parent directory: " + parent.getAbsolutePath());
        }
        
        try (InputStream is = zip.getInputStream(entry);
             FileOutputStream fos = new FileOutputStream(outputFile)) {
            
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
            }
        }
    }
}
```

### 5.2 【推荐】防截屏、防录屏
**风险等级**：低危

**完整实现**：

```java
public class ScreenSecurityHelper {
    
    /**
     * 为Activity启用防截屏保护
     */
    public static void enableScreenSecurity(Activity activity) {
        activity.getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        );
    }
    
    /**
     * 为Dialog启用防截屏保护
     */
    public static void enableScreenSecurity(Dialog dialog) {
        dialog.getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        );
    }
    
    /**
     * 为DialogFragment启用防截屏保护
     */
    public static class SecureDialogFragment extends DialogFragment {
        @Override
        public void onStart() {
            super.onStart();
            enableScreenSecurity(getDialog());
        }
    }
    
    /**
     * 检测录屏状态（API 21+）
     */
    @TargetApi(Build.VERSION_CODES.LOLLIPOP)
    public static boolean isScreenBeingRecorded(Activity activity) {
        MediaProjectionManager mediaProjectionManager = 
            (MediaProjectionManager) activity.getSystemService(Context.MEDIA_PROJECTION_SERVICE);
        return mediaProjectionManager != null && mediaProjectionManager.getActiveProjection() != null;
    }
    
    /**
     * 安全的内容显示处理
     */
    public static void handleSecureContentDisplay(Activity activity, View sensitiveView) {
        enableScreenSecurity(activity);
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            // 检测到录屏时隐藏敏感内容
            if (isScreenBeingRecorded(activity)) {
                sensitiveView.setVisibility(View.GONE);
                showSecurityWarning(activity);
            }
        }
    }
    
    private static void showSecurityWarning(Activity activity) {
        Toast.makeText(activity, "Screen recording detected. Sensitive content hidden.", 
                      Toast.LENGTH_LONG).show();
    }
}
```

## 6. 密码学算法规范
### 6.1 【推荐】Hash算法使用规范
**风险等级**：中危

**正确实现**：

```java
public class SecureHashHelper {
    private static final String SHA_256 = "SHA-256";
    private static final String SHA_512 = "SHA-512";
    private static final String PBKDF2_ALGORITHM = "PBKDF2WithHmacSHA256";
    
    /**
     * 安全的密码哈希（使用PBKDF2）
     */
    public static String hashPassword(String password, byte[] salt) throws Exception {
        int iterations = 10000;
        int keyLength = 256;
        
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, keyLength);
        SecretKeyFactory skf = SecretKeyFactory.getInstance(PBKDF2_ALGORITHM);
        byte[] hash = skf.generateSecret(spec).getEncoded();
        
        return bytesToHex(hash);
    }
    
    /**
     * 安全的文件校验和
     */
    public static String calculateFileChecksum(File file) throws Exception {
        MessageDigest digest = MessageDigest.getInstance(SHA_256);
        
        try (FileInputStream fis = new FileInputStream(file);
             DigestInputStream dis = new DigestInputStream(fis, digest)) {
             
            byte[] buffer = new byte[8192];
            while (dis.read(buffer) != -1) {
                // 读取文件并更新摘要
            }
        }
        
        byte[] hash = digest.digest();
        return bytesToHex(hash);
    }
    
    /**
     * 生成安全的随机盐值
     */
    public static byte[] generateSalt() {
        byte[] salt = new byte[32]; // 256位盐值
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(salt);
        return salt;
    }
    
    private static String bytesToHex(byte[] bytes) {
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02x", b));
        }
        return result.toString();
    }
}
```

## 7. 构建与发布安全
### 7.1 【强制】使用V2签名保护APK
**风险等级**：中危

**Gradle配置**：

```groovy
android {
    signingConfigs {
        release {
            storeFile file("your_keystore.jks")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias "your_key_alias"
            keyPassword System.getenv("KEY_PASSWORD")
            
            // 启用V3签名（API 28+）
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                v3SigningEnabled true
            }
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            
            // 启用资源混淆（可选）
            crunchPngs true
        }
    }
}
```

**构建安全检查清单**：

```bash
# 验证APK签名
apksigner verify --verbose app-release.apk

# 检查签名算法
keytool -list -v -keystore your_keystore.jks
```

## 8. 安全开发最佳实践
### 8.1 安全代码审查清单
+ 所有网络通信使用HTTPS
+ 证书验证严格实现
+ 敏感数据不硬编码
+ 日志中不包含敏感信息
+ 组件导出权限正确配置
+ WebView安全设置完整
+ 加密算法使用安全模式
+ 发布版本关闭调试功能
+ 备份功能正确配置
+ 密钥使用KeyStore管理

### 8.2 安全测试项目
```java
public class SecurityTestSuite {
    
    @Test
    public void testNoSensitiveDataInLogs() {
        // 自动化检查日志中的敏感信息
    }
    
    @Test
    public void testEncryptionImplementation() {
        // 验证加密实现正确性
    }
    
    @Test
    public void testNetworkSecurity() {
        // 测试HTTPS实现和证书验证
    }
    
    @Test 
    public void testComponentSecurity() {
        // 验证组件导出权限
    }
}
```



