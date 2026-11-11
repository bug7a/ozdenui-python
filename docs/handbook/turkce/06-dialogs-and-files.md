# 6. Diyaloglar, mesajlar ve dosyalar

## Diyaloglar cevaplarını döndürür

OzdenUI'da bir diyalog, `input()` gibi, cevabı döndüren bir fonksiyon çağrısıdır:

```python
from ozdenui import Dialog

if Dialog.confirm("Dosya silinecek.", title="Silinsin mi?", confirm_text="Sil", cancel_text="Vazgeç", danger=True):
    delete_the_file()

name = Dialog.prompt("Klasör için bir ad:", value="Fotoğraflar", confirm_text="Tamam", cancel_text="Vazgeç")
# name: yazılan metin ya da None (vazgeçildi)
choice = Dialog.ask("Değişiklikler kaydedilsin mi?", buttons=["Kaydet", "Kaydetme", "Vazgeç"])
# choice: tıklanan düğmenin metni ya da None
Dialog.alert("Kopyalama bitti.", title="Bitti", button_text="Tamam")
```

- **Kodunuz beklerken pencere çalışmaya devam eder**: öbür olaylar ve zamanlayıcılar çalışır, bir saat işlemeyi sürdürür.
  Cevabı yalnız soran fonksiyon bekler.
- `danger=True` onay düğmesini bir silme düğmesi olarak çizer. `Dialog.ask()` ilk düğmeyi ana düğme yapar.
- Escape ya da dışarıya bir tıklama "hayır"dır: `confirm()` için `False`, öbürleri için `None`.
- Düğmelerin metinleri verilmezse İngilizcedir (`Confirm`, `Cancel`, `OK`): yukarıdaki gibi Türkçelerini verin.
- Bir diyalog `start()` içinde de (önce pencere gösterilir) ve bir `run_in_background()` işinde de çalışır.

## Kısa mesajlar: Toast

```python
from ozdenui import Toast

Toast.success("Kaydedildi.")
Toast.error("Dosya kaydedilemedi.", title="Hata")
Toast.warning("Disk dolmak üzere.")
Toast.info("3 yeni mesaj", duration=0)      # ms; 0: kapatılana kadar kalır
```

Bir toast bir köşede belirir ve kendiliğinden gider. Hiç beklemez: kod hemen devam eder.

## Balonlar: Tooltip

```python
Tooltip(target=save_button, text="Dosyayı kaydeder (Ctrl+S)")      # fare üstündeyken
bubble = Tooltip.show(save_button, "Kaydedildi.", time=2000)        # şimdi, düğmenin yanında, 2 sn
```

Bir popover, açık kalan ve nesne tutan bir balondur; her açılışında nesnelerini sizin fonksiyonunuz yapar:

```python
def make_filters():
    CheckBox(text="Yalnız yeniler")
    CheckBox(text="Resmi olanlar")

filters = Tooltip.popover(filter_button, make_filters)   # düğmeye bir tıklama onu açar ve kapatır
filters.close()                                           # ayrıca: filters.open(), filters.is_open
```

## Sistemin dosya pencereleri

```python
from ozdenui import choose_folder, open_file, save_file

path = open_file(file_types=("Resimler (*.png;*.jpg)", "Tüm dosyalar (*.*)"))  # bir yol ya da None
paths = open_file(multiple=True)                                               # bir liste ya da None
target = save_file(file_name="rapor.csv", file_types=("CSV (*.csv)",))         # nereye kaydedilecek ya da None
folder = choose_folder()                                                       # bir klasör ya da None
```

Bunlar bilgisayarın kendi pencereleridir, bu yüzden yollar gerçektir: onları `open()` ya da `pathlib` ile açın.

### Küçük bir not defteri

```python
from pathlib import Path
from ozdenui import App, Dialog, HGroup, SmartButton, TextAreaField, Toast, VGroup, open_file, save_file

FILE_TYPES = ("Metin dosyaları (*.txt;*.md)", "Tüm dosyalar (*.*)")
view = {"path": None}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=12, padding=20, align="left top"):
        with HGroup(hug=True, gap=8):
            SmartButton(text="Aç", on_click=open_note)
            SmartButton(text="Kaydet", tone="cyan", on_click=save_note)
            SmartButton(text="Temizle", tone="orange", on_click=clear_note)
        view["note"] = TextAreaField(title_text="Not", width="100%", height=260)

def open_note():
    path = open_file(file_types=FILE_TYPES)
    if not path:
        return
    view["note"].text = Path(path).read_text(encoding="utf-8")
    view["path"] = path
    view["note"].title_text = Path(path).name

def save_note():
    path = view["path"] or save_file(file_name="not.txt", file_types=FILE_TYPES)
    if not path:
        return
    Path(path).write_text(view["note"].text, encoding="utf-8")
    view["path"] = path
    Toast.success("Kaydedildi.", title=Path(path).name)

def clear_note():
    if Dialog.confirm("Penceredeki metin silinecek.", title="Not temizlensin mi?", confirm_text="Temizle",
                      cancel_text="Vazgeç", danger=True):
        view["note"].text = ""

App(start, title="Not", size=(560, 420)).run()
```

## Pencereye bırakılan dosyalar: FilePicker

`FilePicker`, dosya bırakılan ya da tıklayınca dosya penceresini açan bir yerdir. Her dosya Python'a gerçek yoluyla
ulaşır:

```python
def show_files(picker):
    for file in picker.files:
        print(file["name"], file["size_text"], file["path"])

FilePicker(accept=".csv,.txt", multiple=True, title_text="Dosyaları buraya bırakın", on_change=show_files)
```

- Bir dosya bir sözlüktür: `name`, `path`, `size`, `size_text`, `type`, `extension`, `last_modified`.
  `picker.paths` yalnız yollardır.
- `accept=".pdf,.txt"` ya da `"image/*"`; `max_size` (bayt) ve `max_files`: geçemeyenler
  `on_error(picker, errors)`'a gider.
- `multiple=True` listeye ekler; bu olmadan yeni dosya eskisinin yerini alır. `directory=True` tıklamayla bir klasör
  seçtirir. `picker.add_paths([...])` koddan dosya ekler, `picker.clear()` listeyi boşaltır.
- `title_text`, `description_text`: metinleri; `icon_file`: simgesinin yerinde sizin bir resminiz.
- Üstüne bırakılan bir klasör okunmaz: bir klasörü `directory=True` ya da `choose_folder()` ile seçin.

`examples/files.py` bir klasörün ağacını, onun üstünde bir menüyü ve dosya bırakılacak bir yeri gösterir.

## Sonraki

[7. bölüm: Görünüm](07-looks.md): koyu pencereler, minimal görünüm ve sizin renkleriniz.
