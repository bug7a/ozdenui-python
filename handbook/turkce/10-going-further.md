# 10. Daha ileri

## Bir hatayı bulmak

- **Python'un bir hatası** (yanlış bir ad, yanlış bir tür) her zamanki gibi kendi satırında durur: traceback
  terminaldedir.
- **Sayfanın bir hatası** (sayfanın kullanamadığı bir değer, başarısız olan bir bileşen) terminale, onu gönderen kod
  satırınızla yazılır:

  ```
  ozdenui: settings.py:24: create o17: <sayfanın söylediği>
  ```

- **Bir bileşenin uyarısı** da aynı yoldan gelir: `ozdenui (page warn): SmartButton: tone not found: cyann`.
- **Bir nesnenin sahip olmadığı bir ad** (bir yazım hatası) kendi satırında bir kez söylenir. Sayfa onu tek kelime
  etmeden saklardı:

  ```
  ozdenui: form.py:12: Label: "txet" is not a param of Label (did you mean "text"?)
  ```

  Bir sınıfa camelCase yazılan bir kit adı (`TextField(titleText=...)`) Python adıyla (`title_text`) söylenir: bir
  sınıf parametrelerini Python adlarıyla okur.
  Bir nesnede kendi değeriniz `_` ile başlayan bir ada konur: `row._price = 12` Python'da kalır.
  Bir editör (VS Code, PyCharm) her sınıfın parametrelerini önerir ve böyle bir adı program çalışmadan işaretler.
- Paketin mesajları İngilizcedir; dosya adı ve satır numarası, nereye bakacağınızı söyler.
- `App(..., debug=True)` pencereye web görünümünün geliştirici araçlarını verir: sağ tık > Inspect.
- Hiç verilmemiş bir değeri okumak, `measure()`'ı anan bir hata verir (2. bölüm).

## Python'dan basic.js

basic.js'in her şeyine ulaşılabilir; henüz Python adı olmayanlara da:

```python
gauge.call("setValue", 80)                 # sayfadaki nesnenin bir metodunu çağırır; beklemez
text = editor.ask("getSelectedText")       # bir metodu çağırır ve sonucunu döndürür
width = page.app.evaluate(f"{label.js}.elem.offsetWidth")   # herhangi bir JavaScript; label.js nesnenin kendisidir
```

- `call()` fonksiyonun öbür komutlarıyla birlikte gider; `ask()` ve `evaluate()` sayfayı bekler, bu yüzden onları
  döngülerin dışında tutun.
- Her bileşenin metotları ve parametreleri kaynağında ve [katalogda](https://bug7a.github.io/js-components/) yazılıdır.
  Python'da bir parametre snake_case yazılır; bir metot adını korur (`setValue`).

## Hız

Bir Mac'te ölçüldü:

| | |
|---|---|
| pencerenin görünmesi | yaklaşık 0.5 sn |
| 1000 nesne yapmak | yaklaşık 50 ms |
| bir tıklama → fonksiyonunuz → ekran | yaklaşık 3 ms |
| bir `SmartTable`'a 100000 satır | yaklaşık 2 sn, sonra hızlı kalır |
| 8 MB'lık bir resim | yaklaşık 150 ms |

Bir programı yavaşlatan çoğunlukla sayfaya soru soran bir döngüdür (`measure()`, `ask()`) ya da uygulamanın iş
parçacığındaki yavaş bir iştir. Bir fonksiyonun bütün komutları birlikte gider; bu yüzden bir döngüde 500 nesne yapmak
500 değil, tek bir çağrıdır.

Uygulamanın iş parçacığındaki uzun bir iş, ilerlemesini `page.app.flush()` ile gösterebilir: o ana kadar yapılan
komutlar sayfaya hemen gider. Uzun bir iş için `run_in_background()` daha iyidir (4. bölüm).

## İş parçacıkları, bir kez daha

| | nesneleri değiştirebilir | bir diyaloğu bekleyebilir | sayfaya sorabilir (`measure()`, `ask()`) |
|---|---|---|---|
| `start()`, olaylar, zamanlayıcılar (uygulamanın iş parçacığı) | evet | evet | evet |
| bir `run_in_background()` işi | evet | evet | hayır |
| sizin kendi iş parçacığınız | `call_soon(fn)` ile | | |

## v0.1'in sınırları

- Hemen cevap vermesi gereken bir callback bir Python fonksiyonu olamaz, çünkü cevap sonra gelir: bir `SmartButton`'ın
  `on_before_click`'i, `False` döndüren bir `Tabs` `on_close`'u, bir `TagInput`'un `validate`'i ve bir bileşenin içinde
  nesne kuran fonksiyonlar (`createItemView`, `createCellView`). Bir tablonun değerlerini Python'da biçimlendirin;
  bir `GraphBox`'ın ya da bir `Stepper`'ın sayıları bir biçim metni alır.
- On beş bileşen sayfadayken temasını değiştirebilir; öbürleri görünümlerini yapılırken alır (7. bölüm).
- macOS'ta yapıldı. Paketin testleri Windows'ta da çalışır (WebView2 çalışma ortamı gerekir); Linux için pywebview'in
  GTK ya da Qt web görünümü gerekir.
- Henüz tarayıcı ya da Jupyter kipi yok.
- PyInstaller ile tek dosya yapılan bir program, paketin dosyalarını ister (`--collect-data ozdenui`); bu henüz
  denenmedi.

## Bundan sonra

- Paket kaynağındaki **örnekler**, en küçüğünden başlayarak: `basics`, `counter`, `greeting`, `calculator`, `todo`,
  `settings`, `dialogs`, `clock`, `game`, `file_tool`, `csv_viewer`, `charts`, `files`, `photos`, `paint`, `editor`,
  `markdown_editor`, `json_viewer`, `json_editor`, `chat`, `image_viewer`, `job_log`, `form`, `gallery` (her bileşen),
  `minimal_theme`, `minimal_accent`. Örneklerin metinleri İngilizcedir.
- Paketin **README**'si: her bileşen tek bir tabloda.
- Python'da **`help(ClassName)`**: bir bileşenin parametreleri, callback'leri ve metotları.
- **[basic.js](https://bug7a.github.io/basic.js/)** ve **[bileşenler](https://bug7a.github.io/js-components/)**:
  altındaki kütüphane ve her bileşenin canlı bir örneği.

[Başa dön](README.md)
