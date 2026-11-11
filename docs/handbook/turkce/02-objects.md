# 2. Nesneler

Her pencere beş düz nesneden yapılır: `Box`, `Label`, `Button`, `Input` ve `Icon`. 5. bölümün bileşenleri de bunlardan
yapılmıştır.

| Nesne | Nedir | Kendi değerleri |
|---|---|---|
| `Box` | bir dikdörtgen; başka nesneleri tutan tek nesne | `color`, `border`, `round`, `scroll_y` |
| `Label` | bir metin | `text`, `html`, `font_size`, `bold`, `text_color`, `text_align` |
| `Button` | sistemin düz bir düğmesi (daha güzeli `SmartButton`) | `text` |
| `Input` | tek satırlık bir metin alanı | `text`, `placeholder`, `on_enter` |
| `Icon` | bir resim | `picture` (bir yol, bytes, bir Pillow resmi, bir matplotlib figürü) |

## Yer ve boyut

Bir grubun dışındaki nesnenin kendi yeri vardır: `left`, `top`, `width`, `height`, px olarak. Bunları en başta ve bu
sırayla verin ya da adlarıyla yazın:

```python
Box(20, 20, 100, 100, color="orangered")
Box(left=20, top=20, width=100, height=100, color="orangered")    # aynısı
```

Bir boyut metin de olabilir: `width="100%"` (içinde olduğu kutunun genişliği), `height="auto"` (içeriği kadar yüksek).
Yeri verilmemiş bir nesne, kutusunun sol üst köşesinden başlar.

## Değerler

Bir değer, nesne yapılırken bir argümandır, sonra bir öznitelik:

```python
title = Label(text="Rapor", font_size=24, bold=True, text_color="#2B2B2B")
title.text = "Aylık rapor"                                # ekranda değiştirir
title.set(text="Yıllık rapor", font_size=28, bold=False)  # birden çoğunu bir kerede
print(title.text)                                         # "Yıllık rapor": Python'dan okunur, sayfaya sorulmaz
```

- **Adlar:** Python `font_size` yazar, basic.js `fontSize`; ikisi de kabul edilir.
- **Sayılar ve açık / kapalı değerler:** px olarak bir boyut bir sayıdır; `bold=True` ile `bold=True` aynıdır.
- **Renkler:** her CSS rengi: `"red"`, `"#2A78D6"`, `"rgba(0, 0, 0, 0.5)"`.

Her nesnede olan değerler:

| Değer | Örnek |
|---|---|
| `color` | zemin: `color="#FFFFFF"`, `color="transparent"` |
| `border`, `border_color` | `border=1, border_color="#DDD"` |
| `round` | köşeler: `round=8`; `round=100` bir kareden daire yapar |
| `opacity` | `opacity=0.5` |
| `visible` | `visible=False` gizler; bir grupta öbürleri boşluğu kapatır |
| `clickable` | fareyi dinleyen bir nesne tıklamaları kendiliğinden alır; `clickable=False` onları geçirir |
| `css` | CSS'in başka her şeyi: `css={"cursor": "pointer"}` |

### Vermediğiniz bir değer

`title.text` cevabı Python'dan verir, çünkü onu kodunuz verdi. Sayfanın belirlediği bir değer, ör. `width="auto"` olan
bir etiketin genişliği, `measure()` ile sorulur:

```python
width = title.measure("width")      # şu an ekrandaki genişlik, px olarak
```

Hiç verilmemiş bir değeri okumak, `measure()`'ı anan bir hata verir. `measure()` sayfayı bekler: onu bir döngüde
değil, gerektiğinde kullanın.

### Metin ve HTML

Bir `Label`'ın ya da bir `Button`'ın `text`'i tam yazıldığı gibi gösterilir; bu yüzden bir kullanıcının yazdığı ya da
bir dosyadan okunan metin olduğu gibi verilir (bir `<b>`, `<b>` olarak kalır). HTML, `html` ile verilir:

```python
note.text = typed_text
title.html = "<b>3</b> yeni"
```

basic.js'te `text` HTML'dir; Python'da basic.js'in `plainText`'idir (`plain_text` da çalışır). Bileşenlerin metinleri
de yazıldığı gibi gösterilir (`SmartButton(text=yazilan)`); `allow_html=True` onları HTML yapar.

## Bir Box'ın içindeki nesneler

`with box:` bloğun nesnelerini kutunun içinde yapar. Yerleri kutunun köşesinden sayılır:

```python
from ozdenui import App, Box, Icon, Input, Label, Button

CHECK = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="white"/>'
         b'<path d="M7.5 12.5l3 3 6-7" fill="none" stroke="#2B2B2B" stroke-width="2.4"/></svg>')

view = {}

def start(page):
    page.color = "#F4F5F7"
    with Box(20, 20, 320, 110, color="#5BBAC1", round=12) as view["card"]:
        Icon(20, 25, 60, 60, picture=CHECK)
        view["label"] = Label(100, 36, 200, 38, text="Merhaba", font_size=26, bold=True, text_color="white")
    view["input"] = Input(20, 150, 200, 40, placeholder="Bir metin yazın", on_enter=change)
    Button(230, 150, 110, 40, text="Değiştir", on_click=change)

def change():
    view["label"].text = view["input"].text.strip() or "Merhaba"

App(start, title="Bir kart", size=(360, 220)).run()
```

- `with Box(...) as view["card"]:` kutuyu tek satırda hem saklar hem açar.
- **Nesne yalnız bir `Box`'ın (ve kutu olan grupların) içinde durur.** `with Label():` hata verir. Bir düğmenin üstüne
  bir şey koymak için onu düğmeyle aynı kutuda, aynı yerde yapın.
- `Icon(picture=...)` burada bir SVG'nin bytes'ını alır; bir dosya yolu, bir Pillow resmi ya da bir matplotlib figürü de
  aynı çalışır.
- `on_enter=change`: alanda Enter, düğmenin yaptığını yapar.

## Silmek

```python
view["card"].remove()       # kart ve içindeki bütün nesneler
```

Silinen bir nesne gitmiştir: yeniden göstermek için yenisini yapın. Bir şeyi bir süre gizlemek için `visible=False`
kullanın.

## Bir kutuya sığmayınca

`scroll_y=True` bir kutunun içeriğini aşağı yukarı kaydırır (`scroll_x=True` yana). Bir grubun içinde 3. bölümün
`ScrollArea()`'sı aynı işi yapar ve kendisine verilen yeri alır.

## Sonraki

[3. bölüm: Yerleşim](03-layout.md): gruplar nesneleri sizin yerinize yerleştirir.
