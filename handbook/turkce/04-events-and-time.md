# 4. Olaylar ve zaman

## Bir olay bir fonksiyondur

```python
Button(text="Kaydet", on_click=save)        # yapılırken
button.on_click = save                      # sonra: öncekinin yerini alır
remove = button.on("click", log_click)      # bir işleyici daha; remove() onu kaldırır
```

Sayfanın her olayı çalışır: `on_click`, `on_dblclick`, `on_mouse_enter`, `on_mouse_leave`, `on_key_down`, `on_input`,
`on_focus`, `on_blur`... `on()` içinde sayfanın yazdığı gibi yazılır: `"click"`, `"mouseenter"`, `"keydown"`.

### İşleyici ne gerekiyorsa onu alır

```python
def save(): ...                     # hiçbir şey
def save(button): ...               # nesneyi
def save(button, event): ...        # nesneyi ve olayı: bir sözlük
```

Olayın değerleri yalnızca varsayılan değeri olmayan parametrelere gider. **Bir döngüde değeri varsayılan değer
saklar**, başka araçlarda olduğu gibi:

```python
for number in range(1, 6):
    SmartButton(text=str(number), on_click=lambda number=number: pick(number))
```

`functools.partial(pick, number)` da aynısını yapar.

Olay sözlüğünde olayın bildikleri vardır:

| Anahtar | Ne zaman |
|---|---|
| `key`, `code` | bir tuş: `"Enter"`, `"a"`, `"ArrowLeft"`; `code` tuşun klavyedeki yeridir (`"KeyA"`) |
| `shift`, `ctrl`, `alt`, `meta` | bir tuş: basılı tutulurken `True` (`meta`, Mac'te Cmd'dir) |
| `x`, `y` | fare, pencerenin köşesinden px olarak |
| `text` | bir `Input`: metni |

```python
from ozdenui import App, Box, Label, VGroup

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14):
        pressed = Label(text="Bir tuşa basın", font_size=28, bold=True)
        spot = Box(width=160, height=60, color="#5BBAC1", round=10)
        where = Label(text="", font_size=14, text_color="#5A6270")

    page.on("keydown", lambda page_, event: show_key(pressed, event))
    spot.on("mouseenter", lambda: spot.set(color="#E0A038"))
    spot.on("mouseleave", lambda: spot.set(color="#5BBAC1"))
    spot.on("click", lambda box, event: where.set(text=f"Tıklanan yer: {event['x']}, {event['y']}"))

def show_key(label, event):
    held = [name for name in ("ctrl", "alt", "shift", "meta") if event.get(name)]
    label.text = " + ".join(held + [event["key"]])

App(start, title="Olaylar", size=(420, 300)).run()
```

`page.on("keydown", ...)` penceredeki her tuşu duyar; odaktaki bir alan kendi tuşlarını da duyar.

## Tek iş parçacığı: kilit yok

`start()`, her olay ve her zamanlayıcı **sırayla, tek bir iş parçacığında** (uygulamanın iş parçacığında) çalışır. İki
tıklama hiçbir zaman aynı anda çalışmaz ve okuduğunuz bir değer şu anın değeridir. Kilide gerek yoktur.

Bunun öbür yüzü: bir fonksiyon çalışırken pencere bekler. 3 saniye süren bir fonksiyon pencereyi 3 saniye dondurur.
Yavaş bir iş arka plana gider (aşağıda).

## Zaman: every() ve after()

```python
import time
from ozdenui import App, Label, SmartButton, VGroup, after, every

view = {}

def start(page):
    with VGroup(gap=12):
        view["clock"] = Label(text=time.strftime("%H:%M:%S"), font_size=48, bold=True)
        SmartButton(text="Saati durdur", on_click=stop_clock)
    view["stop"] = every(1000, tick)          # tekrar tekrar, her 1000 ms'de
    after(5000, lambda: print("5 sn geçti"))  # bir kez

def tick():
    view["clock"].text = time.strftime("%H:%M:%S")

def stop_clock():
    view["stop"]()

App(start, title="Saat", size=(360, 220)).run()
```

- `every(ms, fn)` onu durduran bir fonksiyon döndürür; `after(ms, fn)` onu iptal eden bir fonksiyon.
- Bunlar ve pencerenin öbür fonksiyonları (aşağıdaki `run_in_background()`, 6. bölümdeki `open_file()`) `ozdenui`'ten
  gelir ve programın her fonksiyonunda çalışır. Uygulamada da vardırlar: `page.app.every(1000, tick)`.
- Bir zamanlayıcı da bir olaydır: uygulamanın iş parçacığında, tıklamaların arasında çalışır.
- `examples/clock.py` buna bir kronometre ekler.

## Yavaş bir iş: run_in_background()

```python
import time
from ozdenui import App, Label, ProgressBar, SmartButton, VGroup, run_in_background

view = {}

def start(page):
    page.color = "#F4F5F7"
    with VGroup(gap=14):
        view["bar"] = ProgressBar(title_text="Çalışıyor", value=0, width=320)
        view["button"] = SmartButton(text="Başlat", tone="cyan", on_click=begin)
        view["result"] = Label(text="", font_size=16)

def begin():
    view["button"].waiting = True        # düğmede bir saat: şimdi tıklama almaz
    run_in_background(work, 100)

def work(steps):
    for step in range(1, steps + 1):
        time.sleep(0.03)                   # yavaş kısım: büyük bir dosya, bir indirme, bir model
        view["bar"].value = step
    view["button"].waiting = False
    view["result"].text = "Bitti."

App(start, title="Yavaş bir iş", size=(420, 260)).run()
```

- `run_in_background(job, *args)`, `job(*args)`'ı kendi iş parçacığında çalıştırır; pencere çalışmaya devam eder.
- İş nesneleri değiştirebilir (yukarıdaki çubuk) ve bir diyaloğu bekleyebilir (6. bölümdeki `Dialog.confirm()`).
- Sayfaya soru soramaz (`measure()`, `ask()`): gerekenleri başlamadan önce ona verin.
- `examples/file_tool.py` büyük bir dosyanın kelimelerini böyle sayar.

### Kendi iş parçacığınız

Kendi başlattığınız bir iş parçacığı (bir sunucu, bir soket) değişikliklerini uygulamanın iş parçacığına `call_soon()`
ile verir:

```python
call_soon(lambda: status.set(text="Bir mesaj geldi"))
```

## Olayların sırası

Olaylar Python'a oldukları sırayla ulaşır; çoğu birden geldiğinde de (hızlı yazarken). Hızlı ve sürekli bir olay
(farenin hareketi, bir sürükleme) her hareketi Python'a gönderir: bunları sayfaya bırakın (9. bölüm nasıl olduğunu
gösterir), siz yalnız başını ve sonunu dinleyin.

## Sonraki

[5. bölüm: Bileşenler](05-components.md): bir pencerenin hazır parçaları.
