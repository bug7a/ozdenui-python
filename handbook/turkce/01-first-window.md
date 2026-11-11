# 1. İlk pencere

## Kurulum

```
pip install ozdenui
```

Python 3.9 ya da daha yenisi gerekir. Pencereyi açan [pywebview](https://pywebview.flowrl.com/)'i de getirir. Mac'te
sistemin Python'u ile önce pip'i güncelleyin (`python3 -m pip install --upgrade pip`): eski pip, pywebview'in bir
parçasını kaynaktan derlemeye çalışır ve başaramaz. Windows'ta pencere için WebView2 çalışma ortamı gerekir; çoğu
bilgisayarda vardır.

## Sayaçlı bir pencere

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=16):
        count = Label(text="0", font_size=64, bold=True)
        with HGroup(hug=True, gap=12):
            SmartButton(text="−", on_click=lambda: change(count, -1))
            SmartButton(text="+", tone="cyan", on_click=lambda: change(count, +1))

def change(count, step):
    count.text = str(int(count.text) + step)

App(start, title="Sayaç", size=(400, 320)).run()
```

Aşağıdan yukarı okuyun:

- **`App(start, title=..., size=...)`** penceredir. `.run()` onu açar ve pencere kapanınca döner. Programınızın
  sonunda, ana iş parçacığından bir kez çağırın.
- **`start(page)`** pencere hazır olunca çalışır ve nesneleri yapar. `page` pencerenin zeminidir: `color`, `width` ve
  `height` değerleri vardır; kendi kutusu olmayan her nesne onun üstündedir.
- **`with VGroup(gap=16):`** bir grup açar: bloğun içinde yapılan nesneler ona girer, alt alta ve 16 px aralıkla.
  İçindeki `HGroup` iki düğmeyi yan yana koyar; `hug=True` onu yalnız düğmeleri kadar büyük yapar.
- **`Label(text="0", font_size=64, bold=True)`** bir metindir. Değerleri anahtar kelimeli argümanlardır.
- **`on_click=lambda: change(count, -1)`** olaydır: bir tıklama fonksiyonu çalıştırır.
- **`count.text = ...`** etiketi değiştirir. `count.text` onu pencereye sormadan geri de okur.

Pencere, `start()`'ın ilk çizimi hazır olunca gösterilir; bu yüzden hiç boş açılmaz.

## Nasıl çalışır

Pencere, sistemin web görünümüdür (Mac'te WebKit, Windows'ta WebView2). İçindeki sayfada basic.js ve bileşenleri
vardır; paket onları yanında getirir, internet gerekmez.

```
Python kodunuz ──komutlar──▶ sayfa (basic.js nesneleri) ──▶ gördüğünüz
       ▲                                   │
       └──────── olaylar (bir tıklama) ◀───┘
```

- Python'daki her nesne, sayfaya komut gönderen küçük bir nesnedir. Bir fonksiyonun (`start`, bir olay, bir
  zamanlayıcı) bütün komutları birlikte, tek bir çağrıda gider: 1000 nesne Mac'te yaklaşık 50 ms sürer.
- Sayfadaki bir tıklama Python fonksiyonunuzu çağırır; yaptığı değişiklikler yaklaşık 3 ms sonra ekrandadır.
- Kodunuz Python'da çalışır, istediğiniz her kütüphaneyle: dosyalar, veritabanları, `requests`, `numpy`, bir yapay
  zekâ istemcisi.

## App

```python
App(start,
    title="Notlar",         # pencerenin başlığı
    size=(800, 600),        # px olarak genişlik ve yükseklik
    theme="light",          # "light", "dark" ya da "auto" (sistem ne istiyorsa): 7. bölüm
    style="",               # "" ya da "minimal": 7. bölüm
    components=(),          # yüklenecek başka bileşenler: 5. bölüm
    debug=False)            # True: web görünümünün geliştirici araçları (sağ tık > Inspect)
```

Fonksiyonlarınızın içinde `page.app` aynı `App`'tir:

```python
page.app.set_title("Notlar — kaydedildi")
page.app.close()            # pencereyi kapatır; run() döner
page.app.theme              # "light" ya da "dark"
page.app.set_theme("dark")  # pencere başka bir temada yeniden: 7. bölüm
```

## Birden çok fonksiyonlu bir program

Çoğu program, sonradan değiştireceği nesneleri saklar. Dosyanın başındaki bir sözlük bunun en basit yeridir:

```python
from ozdenui import App, Label, SmartButton, TextField, VGroup

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14, padding=40):
        view["name"] = TextField(title_text="Adınız ne?", placeholder="Ada", width=300, on_enter=greet)
        SmartButton(text="Selamla", tone="cyan", on_click=greet)
        view["answer"] = Label(text="", font_size=18)

def greet():
    typed = view["name"].text.strip()
    view["answer"].text = f"Merhaba, {typed}!" if typed else "Önce adınızı yazın."

App(start, title="Selamlama", size=(420, 320)).run()
```

`view["name"].text` her zaman alandaki metindir: sayfa onu her tuşta gönderir. Bir `Label` yazılan metni olduğu gibi
gösterir (bir `<b>`, `<b>` olarak kalır).

Bir sınıf da aynı iyi çalışır (`self.name = TextField(...)`, sonra `App(TodoApp().start)`): paketin `examples/todo.py`'si öyle
yazıldı; 9. bölüm bir sınıfla kendi bileşeninizi yapar.

## Sayfa yeniden yüklenince

`debug=True` ile sayfayı yeniden yüklemek (sağ tık > Reload) nesneleri yeniden yapar: `start()` yeniden çalışır ve
zamanlayıcılar durur. Verisini Python'da tutan bir program (bir liste, bir dosya) onu yeniden gösterir; başka bir şey
gerekmez.

## Sonraki

[2. bölüm: Nesneler](02-objects.md): beş düz nesne ve değerleri.
