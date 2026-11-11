# 3. Yerleşim

Kendi yeri olan nesne (`Box(20, 20, 100, 100)`) bir oyun ya da bir çizim için iyidir. Bir programın penceresi ise
**gruplarla** daha kolay kurulur: gruplar nesnelerini yerleştirir, pencerenin boyu değişince de yeniden yerleştirir.

## VGroup ve HGroup

```python
with VGroup(gap=10, padding=20, align="left top"):
    Label(text="Bir")
    Label(text="İki")             # "Bir"in altında, 10 px aşağıda
    with HGroup(hug=True, gap=8):
        SmartButton(text="Evet")
        SmartButton(text="Hayır")  # "Evet"in yanında
```

- `VGroup` nesnelerini alt alta koyar, `HGroup` yan yana.
- Bir grup, kutusu kadar büyüktür: `width="100%"`, `height="100%"`. `hug=True` onu yalnız nesneleri kadar büyük yapar.
- `gap`: nesneler arasındaki boşluk. `padding`: kenarının içindeki boşluk: `20` ya da `[x, y]` (`[30, 12]`).
- `align`: nesnelerin durduğu yer: `"center"` (varsayılan), `"left top"`, `"right center"`, `"center bottom"`...
- `wrap=True`: yer kalmayınca nesneler bir sonraki satıra geçer (kartlar, etiketler).
- Bir grup bir `Box`'tır: `color`, `round`, `border` onda da çalışır.

Bir grupta bir nesneye yalnız boyutu gerekir: `Label(text="Bir", width=200)`. Boyutu verilmezse içeriği kadar
büyüktür.

**Sığmayınca:** kutusunun alabileceğinden çok nesnesi olan bir grup onları sıkıştırır ve biri ötekinin üstüne gelebilir
(bir kartın altında kalan bir başlık). Pencereye daha çok yer verin ya da içeriği bir `ScrollArea`'ya koyun (aşağıda).

## Kalan yeri almak: fill=True

Alışılmış bir pencere: üstte bir çubuk, ortada bütün yeri alan bir bölüm, altta bir satır.

```python
from ozdenui import App, HGroup, Label, ScrollArea, SmartButton, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=0):
        with HGroup(height=52, padding=[16, 0], gap=10, align="left center", color="white"):
            Label(text="Notlar", font_size=18, bold=True)
            SmartButton(text="Yeni", tone="cyan")
        with HGroup(gap=0, fill=True):
            with VGroup(width=180, height="100%", padding=16, gap=8, align="left top", color="#E9EBEF"):
                for folder in ("Tümü", "İş", "Ev"):
                    Label(text=folder, font_size=15)
            with ScrollArea(padding=16, gap=12):
                for number in range(1, 41):
                    Label(text=f"Not {number}", font_size=15)
        Label(text="40 not", font_size=13, text_color="#5A6270", height=28)

App(start, title="Notlar", size=(640, 420)).run()
```

- `fill=True` bir nesneye öbürlerinin bıraktığı yeri verir: bir `VGroup`'ta kalan **yüksekliği** (çubuk ile alt satır
  arasındaki orta sıra), bir `HGroup`'ta kalan **genişliği** (klasörlerin yanındaki notlar). Her nesne bunu alabilir:
  `HGroup(fill=True)`, `LogView(fill=True)`, `Splitter(fill=True)`.
- `ScrollArea()`, `fill=True` gibi öbürlerinin bıraktığı yeri alır ve içindekileri kaydırır. Bir grupta değil de
  doğrudan sayfada yapılırsa bütün penceredir.
- İçindeki nesneler bir `VGroup`'taki gibi alt alta dizilir: ona `align`, `gap` ve `padding` verin (padding onlarla
  birlikte kayar). `scroll_x=True` yana da kaydırır. Kitin `ScrollArea`'sıdır, kitin kaydırma çubuğuyla (açık renk ya
  da `style_name="dark"`: koyu bir pencere onu kendiliğinden seçer).

## GridGroup: sütunlar ve satırlar

```python
from ozdenui import App, GridGroup, SmartButton

def start(page):
    with GridGroup(columns=4, gap=8, padding=16) as grid:
        for key in "789/456*123-0.=+":
            SmartButton(text=key)
        grid.place(SmartButton(text="Temizle"), column_span=4)

App(start, title="Tuşlar", size=(320, 300)).run()
```

- Nesneler hücrelere sırayla girer: soldan sağa, satır satır.
- `columns=4`: eşit sütunlar. `columns=[120, "1fr", "auto"]`: 120 px, kalan yer, içeriği kadar geniş.
- Bir nesne hücresini doldurur; ızgaraya verilen `align="left center"` ise her nesneyi hücresinin içine yerleştirir.
- `grid.place(obj, column_span=2)`, `grid.place(obj, column=1, row=0)`: kendine ait bir hücre (0'dan sayılır).
- Öbür gruplardan farklı olarak bir ızgara satırları kadar yüksektir. `examples/calculator.py` eksiksiz bir hesap
  makinesidir.

## Gruptan taşanlar

Bir grup kenarından taşanı kesmez: bir düğmenin odak halkası, bir gölge ya da fare üstüne gelince büyüyen bir düğme
küçük bir grupta da bütün görünür:

```python
with HGroup(hug=True, gap=8):
    SmartButton(text="Kaydet", tone="cyan")
    SmartButton(text="İptal")
```

Kesmenin amaç olduğu yerde (bir çerçevedeki resim) `clip_content=True` keser. Kayan bir grup (başında `scroll_y=True`) ve bir
`ScrollArea` kendiliğinden keser.

İki varsayılan basic.js'tekiyle aynı değildir; böylece program daha az söyler:

- basic.js'te bir `VGroup` / `HGroup` içeriğini keser (`clipContent: 1`); Python'da kesmez.
- `MenuBar`, `ToolBar`, `StatusBar` ve `SearchInput` bir grupta küçülmez (`shrink=0`): bir `ScrollArea` ya da
  `fill=True` bir nesne kalan yeri alırken boylarını korurlar. `shrink=1` küçülmelerine izin verir.

## Kendi yeri olan nesne

Bir grubun dışında, bir `Box`'ta ya da sayfada, bir nesne onu koyduğunuz yerde durur: `left`, `top`, `width`,
`height`. Bir oyun, bir çizim ya da başka bir şeyin üstüne gelen bir katman için yol budur:

```python
with Box(0, 0, 400, 300, color="#1E2230") as board:
    player = Box(180, 130, 40, 40, color="#5BBAC1", round=8)
player.left += 20      # onu 20 px sağa götürür
```

`examples/game.py` bir kutuyu tuşlarla hareket ettirir. Bir boyut metin de olabilir: `Box(0, 0, "100%", "100%")`
kutusunu doldurur.

## Pencerenin boyu değişince

Gruplar nesnelerini kendiliğinden yeniden yerleştirir. Kendi hesaplarınız için `page.width` ve `page.height` her zaman
günceldir; `page.on("resize", fn)` de size haber verir:

```python
page.on("resize", lambda: print(page.width, page.height))
```

## Sonraki

[4. bölüm: Olaylar ve zaman](04-events-and-time.md): tıklamalar, tuşlar, zamanlayıcılar ve uzun işler.
