# OzdenUI — El Kitabı

Düz Python ile bir masaüstü penceresi kurun: nesneler, gruplar ve hazır bileşenler. Yalnız Python: JavaScript yok, HTML
yok, tarayıcı sekmesi ve sunucu yok. Bu kitap, Python bilen ama hiç web sayfası yazmamış kişiler için, konuyu adım adım anlatır.


```python
from ozdenui import App, Label, SmartButton, VGroup

def start(page):
    with VGroup(gap=12):
        Label(text="Python'dan merhaba", font_size=24, bold=True)
        SmartButton(text="Kapat", on_click=page.app.close)

App(start, title="Merhaba", size=(360, 200)).run()
```

## Bölümler

| | Bölüm | Öğrendikleriniz |
|---|---|---|
| 1 | [İlk pencere](01-first-window.md) | kurulum, `App`, `start(page)`, pencere ile kodunuz nasıl konuşur |
| 2 | [Nesneler](02-objects.md) | `Box`, `Label`, `Button`, `Input`, `Icon`; verdiğiniz ve okuduğunuz değerler; silmek |
| 3 | [Yerleşim](03-layout.md) | `VGroup`, `HGroup`, `GridGroup`, `fill=True`, `ScrollArea`, kendi yeri olan nesne |
| 4 | [Olaylar ve zaman](04-events-and-time.md) | tıklamalar ve tuşlar, olay sözlüğü, zamanlayıcılar, arka planda bir iş |
| 5 | [Bileşenler](05-components.md) | hazır parçalar: düğmeler, alanlar, seçimler, listeler, tablolar, sekmeler, çubuklar |
| 6 | [Diyaloglar, mesajlar ve dosyalar](06-dialogs-and-files.md) | `Dialog.confirm()`, `Toast`, balonlar, dosya pencereleri, bir `FilePicker`'a bırakılan dosyalar |
| 7 | [Görünüm](07-looks.md) | koyu pencereler, sizin renginizde minimal görünüm, tek bir bileşenin renkleri |
| 8 | [Veri ve resimler](08-data-and-pictures.md) | grafikler, büyük tablolar, çizimler, kayıtlar, Markdown, JSON, kod |
| 9 | [Kendi bileşeniniz](09-your-own-component.md) | nesnelerden yapılmış kendi sınıfınız, bir modül olarak paylaşmak |
| 10 | [Daha ileri](10-going-further.md) | Python'dan basic.js, hız, iş parçacıkları, sınırlar, hata bulmak |

1'den 4'e kadar sırayla okuyun: bütün fikir onlarda. Sonra gereken bölümleri seçin.

## Nasıl okunur

- `ozdenui`'i alan ve `App(...).run()` ile biten her program eksiksizdir: bir dosyaya kopyalayıp `python dosya.py` ile
  çalıştırın. Paketin testleri bunların hepsini çalıştırır, bu yüzden doğru kalırlar.
- Paketin örnekleri (kaynağındaki `examples/` klasörü) daha uzun programlardır: bir yapılacaklar listesi, bir dosya
  aracı, bir CSV görüntüleyici, bir çizim programı. Bölümler onları yeri geldikçe anar.
- `kod` biçimindeki bir ad, Python'daki bir addır. Penceredeki sayfa küçük bir JavaScript kütüphanesi olan
  [basic.js](https://bug7a.github.io/basic.js/) ile yapılır. Hiç JavaScript yazmanız gerekmez; 10. bölüm yine de ona
  nasıl ulaşacağınızı gösterir.
- Paketin adları (sınıflar, parametreler, metotlar) ve terminale yazdığı mesajlar İngilizcedir. Örneklerde
  ekranda görünen metinler Türkçedir.

## Bir dakikada

- `App(start).run()` bir pencere açar. `start(page)` nesnelerini yapar; `page` pencerenin zeminidir.
- Bir nesne yazıldığı yerde yapılır: bir `with` bloğunun içindeyse o kutuya ya da gruba girer.
- Bir grup nesnelerini yerleştirir: `VGroup` alt alta, `HGroup` yan yana.
- Bir değer, nesne yapılırken bir argümandır (`font_size=20`), sonra bir öznitelik (`label.text = "Merhaba"`).
- Bir olay bir fonksiyondur: `on_click=save`. Hiçbir şey almayabilir, nesneyi ya da nesneyle olayı alabilir.
- Bileşenler durumlarını Python'da tutar: `box.checked`, `select.value`, `table.rows`.
- Kodunuz tek bir iş parçacığında çalışır: bir olay, bir zamanlayıcı ve `start()` hiçbir zaman aynı anda çalışmaz.
