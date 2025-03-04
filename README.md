# Kali arabic Pro v7.0

## مقدمة
يُعد **Kali Arabic Pro v7.0** مجموعة شاملة من أدوات الاختبار الأمني الموجهة لمستخدمي توزيعة Kali Linux، حيث يوفر البرنامج قوائم متعددة تشمل:
- **الشبكات والأمان:** أدوات فحص الشبكات واختبار الثغرات.
- **الهندسة الاجتماعية:** أدوات التصيد واستغلال الثغرات.
- **إدارة النظام:** إنشاء تقارير أمنية، مراقبة الموارد وتنظيف النظام.
- **أدوات متقدمة:** Metasploit Framework، جمع المعلومات باستخدام theHarvester، وإدارة الحمولات باستخدام MSFvenom.
- **أدوات البلوتوث:** التحكم في خدمة البلوتوث، البحث عن الأجهزة، وإجراء عمليات الإقران والاتصال.

## المتطلبات
- **توزيعة Linux:** يُفضل استخدام Kali Linux.
- **صلاحيات الجذر (root):** يجب تشغيل البرنامج بصلاحيات `root` لتنفيذ أوامر النظام.
- **الحزم المطلوبة:** تعتمد وظائف البرنامج على وجود عدة حزم مثل:
  - `nmap`
  - `tcpdump`
  - `masscan`
  - `msfvenom` و `msfconsole`
  - `bluetoothctl` و `rfkill`
  - وغيرها.
  
يمكن تثبيت جميع الحزم المطلوبة من خلال خيار "تثبيت الحزم المطلوبة" في القائمة الرئيسية.

## التثبيت
1. **تحميل الكود:**
   - قم بتنزيل الملفات من مستودع المشروع أو انسخ الكود المصدري إلى ملف باسم مثلاً `kali_ar.py`.
2. **إعطاء صلاحيات التنفيذ:**
   - افتح الطرفية (Terminal) وانتقل إلى المجلد الذي يحتوي على الملف.
   - نفذ الأمر التالي:
      ```bash
     git clone https://github.com/aymdev01/kali-arabic.git
      ```
       ```bash
       cd kali-arabic
        ```
     ```bash
     chmod +x kali_ar.py
     ```
     ```bash
     sudo ./kali_ar.py
     ```
3. **تثبيت الحزم المطلوبة (اختياري):**
   - يمكنك استخدام خيار "تثبيت الحزم المطلوبة" من القائمة الرئيسية لتثبيت جميع الأدوات والبرامج اللازمة تلقائيًا.

## كيفية التشغيل والتفعيل
1. **تشغيل البرنامج:**
   - نظراً لأن البرنامج يحتاج إلى صلاحيات الجذر، قم بتشغيله باستخدام:
     ```bash
     sudo ./kali_ar.py
     ```
2. **عرض الشعار والمعلومات:**
   - عند التشغيل، سيتم عرض شريط ترويسة (banner) مع معلومات النظام الأساسية مثل اسم المستخدم والنظام والإصدار والوقت.
3. **التفاعل مع القوائم:**
   - يتم عرض القائمة الرئيسية التي تحتوي على مجموعة من الأقسام مثل الشبكات، الهندسة الاجتماعية، إدارة النظام، والأدوات المتقدمة.
   - أدخل رقم الخيار المطلوب لمتابعة الإجراءات.
4. **تنفيذ الأوامر:**
   - عند اختيار أمر معين، سيُطلب منك إدخال المعطيات المطلوبة (مثل هدف الفحص، عنوان MAC، إلخ).
   - بعد التأكيد، يتم عرض الأمر النهائي مع خيار لتعديله قبل التنفيذ.
   - يتم تنفيذ الأمر وعرض النتائج مع تسجيل العملية في ملف السجل.

## كيفية استخدام الأدوات
- **الشبكات والأمان:** تشمل فحص الشبكة باستخدام nmap، تحليل الحزم باستخدام tcpdump، ومسح المنافذ باستخدام masscan.
- **الهندسة الاجتماعية:** تتضمن أدوات التصيد باستخدام SET Arabic وإنشاء حمولة استغلال باستخدام msfvenom.
- **أدوات البلوتوث:** يمكنك الدخول لقائمة البلوتوث للتحكم بخدمات البلوتوث والبحث عن الأجهزة والإقران والاتصال.
- **إدارة النظام:** يوفر البرنامج إمكانيات إنشاء تقارير أمنية، مراقبة الموارد باستخدام htop وتنظيف النظام.

## المساهمة والتطوير
- يمكنك تعديل الكود وإضافة قوائم أو أدوات جديدة وفق النمط المتبع.
- يُفضل الالتزام بالتنسيق الموجود وتعليقات الكود لتسهيل الصيانة والتطوير.

## التواصل
--------

## الشكر والتقدير
شكراً لكل من ساهم في تطوير أدوات Kali Linux والمجتمع الأمني الذي يتيح تبادل المعرفة والأدوات.

---

*يرجى ملاحظة أن تشغيل بعض الأدوات قد يتطلب إعدادات خاصة أو تكوينات إضافية تتعلق بالشبكات أو الأجهزة المستخدمة.*
# kali-arabic
