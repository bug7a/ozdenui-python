# 5. Bileşenler

Bir bileşen, pencerenin hazır bir parçasıdır ve 2. bölümün nesnelerinden yapılmıştır: bekleme saati olan bir düğme,
başlığı ve uyarısı olan bir alan, arama kutusu olan bir liste, 100000 satırlık bir tablo. Bunların 53'ünün bir Python
sınıfı var; 35 kadarı daha `Component("Ad")` ile çalışır.

## Her bileşen nasıl çalışır

```python
remember = CheckBox(text="Beni hatırla", checked=True, on_change=show)
```

- **Parametreler anahtar kelimeli argümanlardır**, snake_case yazılır: `title_text`, `selected_keys`, `panel_height`.
  Çoğunun kısa bir adı da vardır: `label_text` için `text`, `icon_file` için `icon`.
- **Bir callback bir parametredir**: `on_change=show`. Bir olay gibi ne gerekiyorsa onu alır: `show()`, `show(box)` ya
  da daha fazlası (bir `ItemList`'in `on_change(lst, selected_items)`'ı). Her sınıfın açıklaması argümanlarını
  sayar: `help(ItemList)`.
- **Durumu Python'dadır**: `remember.checked`, `select.value`, `table.rows`. Bunları okumak sayfaya bir şey sormaz.
- **Değiştirmek** bir öznitelik ya da bir metotla olur: `remember.checked = False`, `bar.value = 40`,
  `lst.add_item(...)`. Bileşenin sonradan değiştirebildiği bir parametre de adıyla değişir:
  `field.unit_text = "kg"`. Kodunuzun yaptığı bir değişiklik callback'i çağırmaz; yalnız kullanıcınınki çağırır. (İki
  istisna: `ProgressBar`'ın `on_complete`'i değeri `max_value`'ya ulaşınca çalışır, `Stepper`'ın `increase()` /
  `decrease()`'i `on_change`'i çağırır.)

## İki sekmeli bir form

```python
from ozdenui import (App, CheckBox, HGroup, Label, RadioButton, SelectBox, Slider, SmartButton, Tabs, TextField,
                     Toast, Toggle, VGroup)

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=16, padding=24, align="left top"):
        Label(text="Ayarlar", font_size=24, bold=True)
        with VGroup(width=460, height="auto", padding=20, gap=16, align="left top", color="white", round=12):
            tabs = Tabs(tabs=["Profil", "Ses"], panel_height=240)
            with tabs.panel("Profil"):
                with VGroup(width="100%", height="auto", gap=14, padding=[0, 16], align="left top"):
                    view["name"] = TextField(title_text="Ad", required=True, required_text="Gerekli", width=400)
                    view["language"] = SelectBox(options=["Türkçe", "English", "Deutsch"], value="Türkçe", width=400)
                    view["news"] = CheckBox(text="Bana haberleri gönder")
            with tabs.panel("Ses"):
                with VGroup(width="100%", height="auto", gap=16, padding=[0, 16], align="left top"):
                    view["volume"] = Slider(value=7, min_value=0, max_value=10, width=400)
                    with HGroup(hug=True, gap=18):
                        for quality in ("Düşük", "Normal", "Yüksek"):
                            RadioButton(group="quality", value=quality, text=quality, checked=(quality == "Normal"))
                    view["sounds"] = Toggle(value=True)
            SmartButton(text="Kaydet", tone="cyan", on_click=save)

def save():
    if not view["name"].check():          # alanın üstünde uyarıyı gösterir
        return
    settings = {
        "name": view["name"].text,
        "language": view["language"].value,
        "news": view["news"].checked,
        "volume": view["volume"].value,
        "quality": RadioButton.value_of("quality"),
        "sounds": view["sounds"].value,
    }
    print(settings)
    Toast.success("Kaydedildi.")

App(start, title="Ayarlar", size=(540, 580)).run()
```

`examples/settings.py` üç sekmeli, daha uzun bir örnektir.

## Bileşenler, yaptıkları işe göre

### Düğmeler

| | |
|---|---|
| `SmartButton(text="Kaydet", tone="cyan", on_click=save)` | `tone`: `"cyan"` ana işlem, `"orange"` bir silme, `"yellow"`, `"green"`, `"blue"`, `"white"`; `"accent"`: her pencerenin ana işlemi (7. bölüm) |
| `SmartButton(text="", icon=svg_or_path, aria_label="Daha fazla")` | bir simge düğmesi: bir kare |
| `button.waiting = True` | üstünde bir saat; `button.waiting = False`'a kadar tıklama almaz |
| `SmartButton(text="Sil", ask="Silmek için yeniden tıklayın.")` | ilk tıklama sorar, ikincisi `on_click`'i çalıştırır |
| `button.enabled = False`, `button.text = "Kaydedildi"` | |

### Alanlar

| | |
|---|---|
| `TextField(title_text="Ad", placeholder="Ada", on_change=fn, on_enter=fn)` | `field.text`; `on_change` her değişiklikte, `on_enter` Enter'da çalışır |
| `EmailField`, `PasswordField`, `NumberField`, `TextAreaField` | aynısı; bir e-posta, bir parola, bir sayı (`field.value`), çok satır için |
| `TextField(required=True)`, sonra `field.check()` | alanın üstünde uyarıyı gösterir; hiç uyarı yoksa `True` |
| `TextField(max_length=40)`, `PasswordField(min_length=8)` | en çok ve en az harf sayısı |
| `UrlField(title_text="Site", text="github.com")` | `field.text`: protokolüyle bütün adres (`https://github.com`) |
| `PhoneField(country_code="+1", unit_text="US")`, `CurrencyField(value=1234.5, unit_text="$")` | maskesindeki numara; üçlü gruplarla yazılan tutar (`field.value` bir sayı) |
| `SearchInput(placeholder="Ara", on_change=fn)` | her değişiklikte `fn(box)`, Enter'da `on_enter`; `box.text` |
| `TagInput(tags=["ses"], suggestions=[...], on_change=fn)` | `field.tags` |

`if name.check() and email.check(): save()` bir formun bütün uyarılarını gösterir ve hiç uyarı olup olmadığını söyler.

### Seçimler

| | |
|---|---|
| `CheckBox(text="Beni hatırla", checked=True)` | `box.checked` |
| `Toggle(value=True)` | `toggle.value` |
| `RadioButton(group="size", value="M", text="Orta")` | `RadioButton.value_of("size")` |
| `SelectBox(options=["Elma", "Armut"], value="Armut")` | `select.value` |
| `Slider(value=30, min_value=0, max_value=100, on_change_end=fn)` | `slider.value`; `on_change_end`: fare onu bırakınca |
| `SliderField(text="Ses", value=5, min_value=0, max_value=10)`, `Stepper(value=2, min_value=0, max_value=10)` | `.value` |
| `RangeSlider(low=200, high=800, max_value=1000, step=50)` | `slider.low`, `slider.high` |
| `DatePicker(value="2026-11-20")`, `TimePicker(value="19:30")`, `ColorPicker(value="#3871E0")` | `.value`; ayrıca `.date` (bir `datetime.date`) ve `.time` (bir `datetime.time`) |

### Listeler, tablolar ve ağaçlar

```python
fruits = ItemList(items=["Elma", {"key": "p", "text": "Armut", "description": "Yeşil"}],
                  selection="multiple", height=240, on_change=lambda lst, items: print(lst.selected_keys))
fruits.add_item({"key": "c", "text": "Kiraz"})
fruits.remove_item("p")
```

- **`ItemList`**: `lst.items`, `lst.selected_keys`, `lst.selected`. Metin olarak verilen bir öğe, sırasını anahtar
  olarak alır (`{"key": "0", "text": "Elma"}`); `"enabled": False` olan seçilemez. `layout="grid", style_name="gallery"`
  resimleri gösterir
  (`examples/photos.py`).
- **`SmartTable(columns=[{"key": "name", "title": "Ad"}], rows=[...], height=300, on_select=fn)`**: çok sayıda satır
  (yalnız görünen satırlar yapılır), bir süzgeç kutusu ve sıralama. `on_select(table, row)`.
- **`DataTable`**: seçili satırı sizin verdiğiniz hâliyle geri veren daha küçük bir tablo: `table.selected_row`.
- **`TreeView(items=[{"key": "a", "text": "A", "children": ["b"]}], on_select=fn)`**: `tree.value`. Büyük bir ağaç,
  bir dal açılınca okunur: `"has_children": True` ve `on_load_children(tree, node)` (`examples/files.py`).
- **`SortableList(items=["Satış", "Stok"], on_change=fn)`**: sırayı kullanıcı değiştirir (soldaki tutamakla ya da
  Boşluk ve oklarla); `lst.items` öğelerinizi yeni sırasıyla verir. `on_change(lst, item, from_index, to_index)`.
- **Bir öğenin anahtarları** kitin adlarıdır: `text`, `description`, `icon_file`, `enabled`... `text`'i olmayan ve
  listesinin tanımadığı bir anahtarı olan bir öğe (`"title"`) boş bir satır olurdu: terminal bunu bir kez, programınızın
  satırıyla söyler.

### Sizin nesnelerinizi tutan alanlar

Bazı bileşenler sizin nesnelerinizi tutar. Her biri bir `with` bloğuna bir kutu verir:

```python
tabs = Tabs(tabs=["Siparişler", "Müşteriler"])
with tabs.panel("Siparişler"):
    Label(text="Henüz sipariş yok")

acc = Accordion(sections=["Genel", "Gelişmiş"])
with acc.section("Genel"):
    CheckBox(text="Sistemle birlikte başlat")

split = Splitter(first_size=240)          # iki alan, aralarında sürüklenen bir çizgi
with split.first:
    Label(text="Sol")
with split.second:
    Label(text="Sağ")

panel = SidePanel(title_text="Süzgeçler")   # yandan kayarak gelir
with panel.body:
    CheckBox(text="Yalnız yeniler")
SmartButton(text="Süzgeçler", on_click=panel.open)
```

### Pencerenin çubukları

| | |
|---|---|
| `MenuBar(menus=[{"text": "Dosya", "items": [{"text": "Kaydet", "shortcut": "Ctrl+S", "on_click": save}]}])` | sayfanın içinde, pencerenin görünümünde; Mac'te Ctrl, Cmd'dir |
| `ToolBar(items=[{"key": "save", "icon": "save", "hint": "Kaydet", "on_click": save}, "-", ...])` | `"-"` bir çizgi; `toggle=True` basılı kalır; sığmayanlar bir "..." menüsüne girer |
| `StatusBar(message="Hazır", items=["UTF-8"])` | `bar.set_message("Kaydedildi", "success", 3000)`, `bar.set_busy(True)` |
| `ContextMenu(target=table, items=["Aç", "-", {"text": "Sil", "on_click": fn}])` | hedefe sağ tıklamak onu açar |

Menüsü, araç çubuğu, yeri dolduran bir listesi ve durum çubuğu olan bir pencere, bunların bir `VGroup(gap=0)`'udur;
ortadaki parçaya `fill=True` verilir (3. bölüm).

### İlerleme ve adımlar

| | |
|---|---|
| `ProgressBar(title_text="Kopyalanıyor", value=0)` | `bar.value = 40` |
| `LoadingScreen(title_text="Uygulamam", message_text="Okunuyor...")` | pencereyi örter; `loading.set_progress(0.4)`, `loading.close()` |
| `StepBar(steps=["Sepet", "Adres", "Ödeme"], step=1)` | `bar.next()`, `bar.previous()`, `bar.step` |
| `Tooltip(target=button, text="Dosyayı kaydeder")` | fare üstündeyken bir ipucu; öbür biçimleri 6. bölümde |

### Görünümler: 8. bölüm

`GraphBox` (grafikler), `LogView`, `ImageView`, `MarkdownView`, `JsonView`, `JsonEditor`, `CodeEditor`, `Canvas`, `ChatView` ve
`WebView` veri, resim, kod, bir konuşma ve web sayfası gösterir (`JsonEditor` ve `CodeEditor` yazdırır da): 8. bölüm.

### Bileşenlerin kendi metinleri

Bir bileşenin kendi yazdığı metinler (bir uyarı, diyaloğun düğmeleri, boş bir tablonun mesajı) İngilizcedir. Her biri
bir parametreyle değişir:

```python
TextField(title_text="Ad", required=True, required_text="Gerekli")                # "Required" yerine
Dialog.confirm("Dosya silinecek.", title="Silinsin mi?", confirm_text="Sil", cancel_text="Vazgeç", danger=True)
SmartTable(columns=columns, rows=rows, no_data_found_alert="Kayıt yok", all_titles_text="TÜMÜ")
DatePicker(value="2026-11-20", language="tr")                                       # ay ve gün adları Türkçe
JsonEditor(value=rows, texts={"add_row": "Satır", "search": "Satırlarda ara", "table": "Tablo"})
```

Bir bileşenin metin parametreleri, kaynağındaki varsayılan değerlerinde görülür (`requiredText: "Required"`); Python'da
snake_case yazılır. `JsonEditor`'ın metinleri tek bir `texts` sözlüğündedir; anahtarları da snake_case yazılabilir
(`add_row`).

## Öbür bileşenler: Component("Ad")

Kitte sınıflardan daha çok bileşen vardır. Her biri adıyla çalışır:

```python
from ozdenui import App, Component

def start(page):
    Component("Gauge", 20, 20, 180, 180, value=72, sub_text="Disk")

App(start, components=["Gauge"]).run()    # bileşeni ve gerekenleri yükler
```

- `components=[...]`, sayfanın kendiliğinden yüklemediği bileşenlerin dosyalarını yükler.
- Parametreleri basic.js'in parametreleridir; snake_case ya da camelCase yazılır. Bir fonksiyon bir callback'tir.
- `obj.call("setValue", 80)` metotlarını çağırır (10. bölüm).
- Liste: `Badge`, `Breadcrumbs`, `Filters`, `Gauge`, `HoldToConfirmButton`, `LeftMenu`, `MiniGraphBox`, `Notice`,
  `PageControl`, `TimeLine`, `TinyTable` ve daha fazlası; [katalog](https://bug7a.github.io/js-components/)
  her birini bir örnekle gösterir.

### Bir bileşenin içindeki kutu

`comp.part("content")` bir bileşenin içindeki, nesne koymak için bir kutudur: `with comp.part("content"): Label(...)`.
Yukarıdaki sınıflar kendi kutularını zaten verir (`tabs.panel()`, `split.first`).

## Sonraki

[6. bölüm: Diyaloglar, mesajlar ve dosyalar](06-dialogs-and-files.md).
