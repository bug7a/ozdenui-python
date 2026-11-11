# 7. Görünüm

En genişinden en küçüğüne üç düzey vardır: pencerenin **teması** (açık ya da koyu), pencerenin **stili** (olağan görünüm
ya da sizin renginizdeki minimal görünüm) ve **tek bir bileşenin görünümü** (paketi ve renkleri). Kodunuzun verdiği bir
görünüm, pencerenin görünümüne her zaman baskın gelir.

## Koyu bir pencere

```python
App(start, theme="dark").run()     # "light" (varsayılan), "dark" ya da "auto": sistem ne istiyorsa
```

- Her bileşen koyu görünümünü alır; diyaloglar ve toast'lar da.
- Sayfa, bir `Label`, bir `Box` ve bir `Input` da uyar: koyu bir zemin, açık bir metin.
- Bir `SmartButton`'ın `tone`'u koyu tonuna döner (`"cyan"` → `"cyanDark"`).
- `page.app.theme` `"light"` ya da `"dark"`'tır (`"auto"`dan sonra da): kendi nesnelerinizin renkleri için kullanın.

```python
TEXT_SOFT = {"light": "#5A6270", "dark": "#9AA3B5"}
Label(text="Bugün güncellendi", text_color=TEXT_SOFT[page.app.theme])
```

On beş bileşen sayfadayken temasını değiştirebilir (`log.set_theme("dark")`, ayrıca `log.theme = "dark"`):
`LogView`, `ImageView`, `MarkdownView`, `JsonView`, `ChatView`, `RangeSlider`, `StepBar`, `Canvas`, `MenuBar`, `ToolBar`,
`StatusBar`, `Splitter`, `CodeEditor`, `Accordion` ve `GraphBox`. Öbürleri görünümlerini yapılırken alır; bu yüzden
bütün bir pencere temasını sayfasını yeniden yaparak değiştirir:

```python
page.app.set_theme("dark")    # "light", "dark" ya da "auto": sayfa yeniden yapılır ve start() yeniden çalışır
```

Programınızın kendi değişkenlerinde tuttukları kalır; nesneler baştan başlar (bir alana yazılmış metin gider).
`examples/gallery.py` ve `gallery-styled.py`'nin ToolBar'ında bunun için bir Dark / Light düğmesi var.

## Sizin renginizde minimal görünüm

```python
App(start, style="minimal").run()                          # küçük ve çizgilerden yapılmış; theme="dark" de çalışır
App(start, style="minimal", accent="#2A78D6").run()        # aynısı, sizin renginizde
```

**`style="minimal"`** 40 kadar bileşene minimal görünümlerini verir: 28 px denetimler, 13 px metin, kendilerine ait
dolgu ve gölge yok; böylece pencerenin zeminini alırlar. Bir araç, bir düzenleyici, bir ayarlar paneli bu görünümde
sakin durur.

**`accent`** minimal görünüme tek bir renk verir. Renk, görünümün mürekkebini çizdiği yerlere gider: açık bir anahtar,
işaretli bir kutu, bir kaydırıcının ve bir ilerleme çubuğunun dolgusu, seçili sekme, satır ve adım, yazarken bir alanın
kenarı ve ana düğme. Çizgiler, metinler ve odak halkası oldukları gibi kalır.

```python
from ozdenui import App, CheckBox, HGroup, Label, ProgressBar, SmartButton, Tabs, Toggle, VGroup

THEME = "light"            # "dark" ya da "auto": sistem ne istiyorsa
ACCENT = "#2A78D6"         # beyaz üstünde okunan bir renk: seçili sekmenin metni de bu renktir
GROUND = {"light": "#FFFFFF", "dark": "#1A1A19"}

def start(page):
    page.color = GROUND[page.app.theme]
    with VGroup(gap=14, padding=30, align="left top"):
        Label(text="Hesap", font_size=18, bold=True)
        Tabs(tabs=["Genel", "Gizlilik", "Gelişmiş"], panels=False, width=300)
        CheckBox(text="Beni hatırla", checked=True)
        with HGroup(hug=True, gap=10):
            Toggle(value=True)
            Label(text="Sesler", font_size=13)
        ProgressBar(title_text="Yükleniyor", value=62, width=260)
        with HGroup(hug=True, gap=8):
            SmartButton(text="İptal")
            SmartButton(text="Kaydet", tone="accent")
            SmartButton(text="Sil", style_name="minimalDanger")

App(start, title="Minimal", size=(420, 380), theme=THEME, style="minimal", accent=ACCENT).run()
```

- **`tone="accent"`** her pencerenin ana işlemidir: burada vurgu rengi, vurgusuz minimal görünümde görünümün mürekkebi,
  olağan görünümde `"cyan"`.
- **`style_name="minimalDanger"`**: minimal görünümde bir silme düğmesi (koyu pencerede koyu ikizi).
- **Koyu bir pencerede** renk, koyu zeminde okunana kadar açılır. `accent_dark="#7FB6DE"` onu sizin seçmenizi sağlar.
- **Rengin üstündeki metin** (seçili bir gün, ana düğme) beyaz ya da koyudur; hangisi daha iyi okunuyorsa.
- Minimal görünümü olmayan bir bileşen olağan görünümünü korur. `examples/minimal_theme.py` hepsini,
  `examples/minimal_accent.py` vurgu rengini gösterir.

## Tek bir bileşenin görünümü

### Bir paket: style_name

Çoğu bileşenin paket denen birkaç görünümü vardır. Bir sınıfın açıklaması paketlerini sayar:

```python
CheckBox(text="Beni hatırla", style_name="modern")
ItemList(items=photos, layout="grid", style_name="gallery")
SmartButton(text="İleri", style_name="pill", tone="blue")
```

Adını verdiğiniz bir paket her pencerede kalır; koyu bir pencerede, koyu ikizi olan açık bir paket ikizini alır
(`"gallery"` → `"galleryDark"`, `"minimalDanger"` → `"minimalDangerDark"`).

### Sizin renkleriniz: style

`style` bir bileşenin parçalarını değiştirir. Anahtarları, her parametre gibi, snake_case yazılabilir:

```python
SmartButton(text="Git", style={"box": {"color": "#2A78D6"}, "hover": {"color": "#2367BA"},
                               "label": {"text_color": "white"}})
ItemList(items=fruits, style={"box": {"color": "white"}})
Toggle(value=True, background_style={"selected_color": "#6AC966"})
```

- `style={...}` paketin üstüne gelir: verdiğiniz kazanır, kalanı kalır.
- Parçaların adları (`box`, `hover`, `label`...) bileşenin basic.js'teki adlarıdır;
  [katalog](https://bug7a.github.io/js-components/) her bileşenin kodunu gösterir.
- Adı `_style` ile biten bir parametre (`background_style`, `button_style`) de bir stildir.
- `framed=False` bileşenin çerçevesini kaldırır (kutusunda kenarlık ve yuvarlak köşe yok): iki çubuğun arasını dolduran
  bir `LogView` ya da `CodeEditor`. Tek kelimeyle `style={"box": {"border": 0, "round": 0}}`.

### Düz nesneler

Bir `Box`, bir `Label`, bir grup renklerini değerlerinden alır (`color`, `text_color`, `border_color`): 2. bölüm. Bir
programın renklerini dosyasının başında adlarıyla tutun, böylece bir değişiklik tek satır olur:

```python
PAGE_COLOR = "#F4F5F7"
CARD_COLOR = "#FFFFFF"
TEXT_SOFT = "#5A6270"
```

## Sonraki

[8. bölüm: Veri ve resimler](08-data-and-pictures.md).
