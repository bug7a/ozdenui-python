# 8. Veri ve resimler

Bu bölümün bileşenleri, bir Python programında çoğunlukla bulunanları gösterir: sayılar, satırlar, çizimler, kayıtlar,
metinler ve kod. Hiçbiri sayfada başka bir kütüphane istemez.

## Grafikler: GraphBox

```python
GraphBox(type="bar", labels=["Oca", "Şub", "Mar"], values=[1200, 1900, 700], format_value="{:,.0f} TL")
```

- `type`: `"line"`, `"area"`, `"bar"`, `"pie"`, `"doughnut"`, `"radar"`, `"scatter"`, `"bubble"`.
- Daha çok çizgi ya da çubuk: `datasets=[{"label": "2025", "data": [8, 11, 9]}, {"label": "2026", "data": [10, 14, 12]}]`.
- Değerler listeler, numpy dizileri ya da bir pandas Series olabilir.
- `format_value` bir fonksiyon değil bir biçim metnidir, çünkü sayfa çizerken bir sayının metnine ihtiyaç duyar:
  `"{}"`, `"{:.2f}"`, `"{:,}"`, `"{:,.0f} TL"`, `"{:.1%}"`.
- Sonra: `graph.set_values([...])`, `graph.set_type("line")`, `graph.add_value("Nis", 15)`,
  `graph.save_image("grafik.png")`. `on_click(graph, item)`: `item["label"]`, `item["value"]`.

### Canlı bir grafik ve bir kayıt

```python
import random
import time
from ozdenui import App, GraphBox, LogView, VGroup, every

POINTS = 30
view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=12, padding=20):
        view["chart"] = GraphBox(type="area", title_text="Sıcaklık", labels=[], values=[], curve="smooth",
                                 show_points=False, max_count=POINTS, format_value="{:.1f}°", height=240)
        view["log"] = LogView(fill=True)
    every(1000, measure)

def measure():
    value = round(20 + random.uniform(-3, 3), 1)
    view["chart"].add_value(time.strftime("%H:%M:%S"), value)   # POINTS değerden sonra en eskisi gider
    if value > 22:
        view["log"].warn(f"Sıcak: {value}°")
    else:
        view["log"].info(f"{value}°")

App(start, title="Bir sensör", size=(560, 520)).run()
```

`examples/charts.py` canlı bir grafik, tıklanabilen çubuklar, bir halka grafik ve resim olarak kaydedilen bir grafik
gösterir.

## Tablolar

```python
people = [{"name": "Ada", "city": "Ankara", "orders": 12}, {"name": "Can", "city": "İzmir", "orders": 7}]
table = SmartTable(columns=[{"key": "name", "title": "Ad", "width": 200}, {"key": "city", "title": "Şehir"},
                            {"key": "orders", "title": "Siparişler", "type": "integer"}],
                   rows=people, height=300, on_select=lambda table, row: print(row["name"]))
```

- **`SmartTable`** yalnız görünen satırları yapar: 100000 satır Mac'te ona yaklaşık 2 sn'de ulaşır ve sonra hızlı
  kalır. Bir süzgeç kutusu ve başlıklarında sıralaması vardır. Bir satır, sütunların anahtarlarıyla bir sözlük ya da
  sütunların sırasıyla bir listedir. Değerler metin olarak gösterilir: onları Python'da biçimlendirin
  (`f"{price:,.2f}"`).
- **`DataTable`** birkaç yüz satıra kadar içindir; sütunları metinlerine göre genişler, `show_search=True` bir arama
  kutusu ekler ve `table.selected_row` satırı sizin verdiğiniz hâliyle verir.
- `examples/csv_viewer.py` bir CSV dosyasını bir SmartTable'da açar.

## Resimler

Bir resim bir dosya yolu, bytes, bir Pillow resmi, bir matplotlib figürü ya da bir adres olabilir:

```python
Icon(width=48, height=48, picture="logo.png")
view = ImageView(height=400, image="foto.jpg")     # tekerlekle ya da iki parmakla yakınlaşır, sürükleyince kayar
view.set_image(figure)                             # bir matplotlib figürü
```

- Aynı boyda yeni bir resim yakınlığı korur ve göz kırpmaz; bu yüzden bir program çizimini tekrar tekrar yenileyebilir
  (`examples/image_viewer.py`).
- Bir resim sayfaya çağrının içinde gider: 8 MB Mac'te yaklaşık 150 ms sürer. `picture_address(picture)` bir resmin
  adresini bir kez verir; çok kez gösterdiğiniz bir resim için kullanın.
- `ItemList(layout="grid", style_name="gallery")` çok sayıda resmi karolar olarak gösterir (`examples/photos.py`).

## Kayıtlar: LogView

```python
log = LogView(height=300)
log.info("Dosya okunuyor")
log.success("Bitti")
log.error("Dosya orada değil")
log.capture_print()                                     # print() onun içine gider (hatalar da, hata olarak)
logging.getLogger().addHandler(log.logging_handler())   # logging modülü de
```

Görünüm, okuyan kişi yukarı kaydırana kadar son satırı izler. Bir metin hiçbir zaman HTML olarak okunmaz.
`examples/job_log.py`.

## Metinler, JSON ve kod

| | |
|---|---|
| `MarkdownView(text="# Bir rapor\n\nBirkaç **kalın** kelime")` | `view.append_text(piece)` sona ekler: bir yapay zekânın geldikçe yazdığı cevap; `view.load_file("notlar.md")` |
| `JsonView(value=data, height=400, on_select=fn)` | her değer, bir milyon öğe de; bir tıklama yolunu söyler: `view.selected_path_text` (`users[0].name`), `view.selected_value` |
| `JsonEditor(value=rows, height=360, on_change=fn)` | bir tabloda yazılan JSON listesi ya da sözlüğü; `on_change(editor, value)` değerin bütününü alır, `editor.value` onu sorar; `JsonEditor.open(value=settings, on_apply=fn)`: Cancel ve Apply düğmeli bir pencerede |
| `CodeEditor(value="x = 1", language="python", height=300, on_change=fn)` | `editor.value`; Python, JavaScript, JSON, HTML, CSS, SQL, Bash |
| `ChatView(empty_text="Bir şey sorun", on_send=answer)` | bir yapay zekâyla konuşma: `on_send(chat, text)`; bir cevap Markdown'dır: `key = chat.add_message(role="assistant")`, sonra `chat.append_text(key, piece)`; `chat.busy = True` noktaları ve Durdur'u gösterir (`on_stop`) |
| `WebView(html=figure.to_html(), height=400)` | bir web sayfası ya da betikleriyle bir HTML metni: bir plotly grafiği, bir folium haritası, bir pandas tablosu (`df.to_html()`); `view.load("https://...")`, `on_message(view, data)` |

- Bir Markdown metni hiçbir zaman HTML olarak okunmaz ve içindeki hiçbir betik çalışmaz. `![Bir çizim](plot.png)` bu
  bilgisayardaki bir dosyayı okur; `http` adresli bir resim bağlantı olarak kalır (güvendiğiniz bir metin için
  `remote_pictures=True`).
- Bir `JsonEditor` yalnız JSON verisi alır (metinler, sayılar, True / False, None, listeler ve sözlükler): bir tarih,
  `json` modülünde olduğu gibi reddedilir, çünkü metin olarak geri gelirdi.
- Bir `ChatView` cevabının parçaları bir arka plan işinden gelebilir (`run_in_background`): pencere çalışmaya devam eder,
  görünüm de okuyan yukarı kaydırana kadar sonu izler (`examples/chat.py`).
- Bir `WebView`'in sayfası internetten bir şey alıyorsa (bir betik, bir harita karosu, bir resim) bağlantı ister. Bu
  bilgisayardaki bir dosya (`view.load_file("rapor.html")`) metniyle gösterilir: yanındaki bir resim ya da stil yüklenmez.
- `examples/markdown_editor.py`, `examples/json_viewer.py`, `examples/json_editor.py` ve `examples/editor.py`
  (Python'unu çalıştıran küçük bir düzenleyici) bunları gösterir.

## Çizim: Canvas

```python
canvas = Canvas(height=400)
canvas.circle(100, 80, 30, fill="orange", draggable=True)
canvas.line(20, 20, 200, 120, color="tomato", line_width=4)
canvas.text(20, 180, "Daireyi sürükleyin", font_size=16)
```

- Şekiller: `line`, `rect`, `circle`, `ellipse`, `polyline`, `polygon`, `text`, `image`. Her biri anahtarını döndürür:
  `canvas.update_shape(key, fill="red")`, `canvas.move_shape(key, 10, 0)`, `canvas.remove_shape(key)`.
- Sayfa `draggable=True` olan bir şekli kendisi hareket ettirir; `on_shape_move(canvas, shape)` Python'a onun nerede
  durduğunu söyler.
- `drawing=True` fareye bir kalem verir; `canvas.save_image("cizim.png")` (`examples/paint.py`).

## Sonraki

[9. bölüm: Kendi bileşeniniz](09-your-own-component.md).
