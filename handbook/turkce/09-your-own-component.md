# 9. Kendi bileşeniniz

Birden çok kez gereken bir parça (bir kart, bir formun bir satırı, bir puanlama) sizin bir sınıfınız olur. Nesnelerini
bir `with` bloğunda yapar, değiştireceklerini saklar ve metotları vardır. JavaScript gerekmez.

## Bir kart

```python
from ozdenui import App, HGroup, Label, SmartButton, VGroup

CARD_LOOK = dict(width=220, height="auto", align="left top", padding=16, gap=8, color="white", round=12)

class Card:
    """Bir kart: bir başlık, bir metin ve bir düğme. Düğmesine tıklanınca on_open(card) çalışır."""

    def __init__(self, title, text, on_open=None):
        self.on_open = on_open
        with VGroup(**CARD_LOOK) as self.box:
            self.title = Label(text=title, font_size=18, bold=True)
            Label(text=text, text_color="#5A6270")
            SmartButton(text="Aç", on_click=self.open)

    def open(self):
        if self.on_open:
            self.on_open(self)

    def set_title(self, title):
        self.title.text = title

def start(page):
    page.color = "#F4F5F7"
    with HGroup(gap=16, padding=24, wrap=True):
        for name in ["Satış", "Stok", "Siparişler"]:
            Card(name, "Bugün güncellendi.", on_open=lambda card: card.set_title("Açıldı"))

App(start, title="Kartlar", size=(760, 240)).run()
```

- **`Box`'ın alt sınıfı değil, düz bir sınıf.** Sınıf nesnelerini saklar (`self.box`, `self.title`). Bir ozdenui
  nesnesine verilen bir ad, sayfaya onun değerlerinden biri olarak gider: `box.title = ...` kutuyu değiştirir, hiçbir
  şey saklamaz.
- **Metotlar onu değiştirir** (`set_title()`), bileşenlerin metotlarının yaptığı gibi.
- **Nesneleri olağan nesnelerdir:** `card.box.remove()` kartı ve içindeki her şeyi siler; `card.box.on("mouseenter", fn)`
  ve `card.title.measure("width")` her nesnede olduğu gibi çalışır.
- **Onu bir dosya olarak paylaşın:** `card.py` dosyasına koyun, sonra ona ihtiyacı olan her programda
  `from card import Card` yazın.

## Kendi durumu ve kendi callback'i

Sizin bir bileşeniniz durumunu Python'da tutar ve kullanıcı onu değiştirince programa haber verir:

```python
from functools import partial
from ozdenui import App, HGroup, Label, VGroup

STAR_ON = "#E0A038"
STAR_OFF = "#C9CDD4"

class Rating:
    """Beş yıldız: rating.value (0 ile 5 arası); kullanıcı bir yıldıza tıklayınca on_change(rating)."""

    def __init__(self, value=0, on_change=None):
        self.value = value
        self.on_change = on_change
        with HGroup(hug=True, gap=4) as self.box:
            self.stars = [Label(text="★", font_size=28, on_click=partial(self.click, number)) for number in range(1, 6)]
        self.show()

    def set_value(self, value):
        """Koddan: bileşenlerin yaptığı gibi on_change'i çağırmaz."""
        self.value = value
        self.show()

    def click(self, number):
        self.set_value(number)
        if self.on_change:
            self.on_change(self)

    def show(self):
        for number, star in enumerate(self.stars, start=1):
            star.text_color = STAR_ON if number <= self.value else STAR_OFF

def start(page):
    with VGroup(gap=12):
        said = Label(text="Puan verin", font_size=16)
        Rating(value=3, on_change=lambda rating: said.set(text=f"{rating.value} yıldız"))

App(start, title="Puan", size=(320, 200)).run()
```

`partial(self.click, number)` her yıldıza kendi numarasını verir (`lambda number=number: self.click(number)` de
verir).

## Nesne tutan bir bileşen

Nesne tuttuğu kutuya bir ad verin; `Tabs`'ın `tabs.panel()` verdiği gibi:

```python
class Section:
    """Bir formun başlıklı bir bölümü: section = Section("Ses"); with section.body: ..."""

    def __init__(self, title):
        with VGroup(width="100%", height="auto", gap=8, align="left top") as self.box:
            Label(text=title.upper(), font_size=11, bold=True, text_color="#5A6270")
            self.body = VGroup(width="100%", height="auto", gap=10, align="left top")

sound = Section("Ses")
with sound.body:
    CheckBox(text="Ses çal")
    Slider(value=7, min_value=0, max_value=10)
```

## Hangisi Python'un, hangisi sayfanın

**"Bir tıklama, sonra bir değişiklik" Python'undur.** Fonksiyonunuz çalışır, sayfa değişikliği yaklaşık 3 ms sonra
gösterir.

**"Her kare, farenin her hareketi" sayfanındır.** Python'dan gönderilen çok adımlı bir hareket takılarak ilerler.
Sayfaya nasıl hareket edeceğini söyleyin, sonra varılacak yeri verin:

```python
ball.call("setMotion", "left 0.3s, opacity 0.2s")   # bu değerler artık yumuşakça değişir
ball.left = 300                                      # sayfa onu 0.3 sn'de oraya götürür
```

Bir `Canvas` bunu kendiliğinden yapar: serbest çizgileri ve sürüklenen şekilleri sayfa çizer, Python yalnız sonlarını
duyar.

### Hemen cevap vermesi gereken bir callback

basic.js bileşenlerinin bazı callback'leri hemen bir cevap döndürmek zorundadır (bir listenin bir satırını çizen bir
fonksiyon, bir tıklamayı durduran bir denetim). Python'un cevabı biraz sonra gelir; bu yüzden böyle bir callback bir
Python fonksiyonu olamaz. Bunun yerine değerleri sayfaya gitmeden önce Python'da biçimlendirin ve bileşenlerin verdiği
parametreleri kullanın (10. bölüm bunları sayar).

## Sonraki

[10. bölüm: Daha ileri](10-going-further.md).
