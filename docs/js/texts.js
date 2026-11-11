/* Bismillah */

/*

OzdenUI Website - Texts - v26.11 (2026-11-04)

The texts of the page in English and Turkish (the same keys). TEXTS.fill(text) writes the facts of CONFIG into
{version}, {python}, {classes}, {components}, {size}, {click}, {show}, {license}.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const TEXTS = {

    en: {

        htmlLang: "en",
        pageTitle: "OzdenUI – Modern desktop windows, in plain Python",
        pageDescription: "OzdenUI opens a small, modern window of its own from Python: boxes, texts, buttons and the ready components of basic.js. Only Python: no JavaScript, no HTML, no browser tab, no server.",
        languageButton: "TR",
        languageHint: "Türkçe",
        nav: { code: "Code", why: "Why", components: "Components", examples: "Examples", start: "Start" },
        navBasicJs: "basic.js",
        navHandbook: "Handbook",
        navComponents: "Components of basic.js",
        menu: "Menu",
        copy: "Copy",
        copied: "The code is copied.",
        copyFailed: "The code could not be copied.",

        // HERO
        heroEyebrow: "v{version} · experimental · Python {python}+",
        heroTitle: "Modern desktop windows, in\u00A0plain Python", // WHY \u00A0: the line breaks before "in", not after it
        heroLead: "Write the window in Python: boxes, texts, buttons and ready components appear in a small window of its own. Only Python: no JavaScript, no HTML, no browser tab, no server.",
        heroPrimary: "Get started",
        heroSecondary: "See the examples",
        heroFacts: ["{classes} components with a Python class", "all {components} of basic.js by name", "{size} with its window", "{license}"],
        heroSlidesLabel: "The windows of the examples",
        heroShotAlts: {
            "hero-gallery-styled": "The window of examples/gallery-styled.py: buttons, a check box, a toggle, radio buttons, a drop-down list, a slider, a progress bar, a note field and lists, in the colors its code chose.",
            "minimal_theme": "The window of examples/minimal_theme.py: every component in the minimal look, small and made of lines.",
            "hero-charts": "The window of examples/charts.py: a live line, bars and a doughnut.",
            "hero-json_editor": "The window of examples/json_editor.py: the products of a shop in a JSON editor, as a table.",
            "hero-photos": "The window of examples/photos.py: small pictures in a grid and the chosen one large.",
            "hero-chat-dark": "The window of examples/chat.py in a dark window: a question and its answer, word by word.",
        },
        installSoon: "Not on PyPI yet: install it from its source (see Start).",

        // CODE
        codeEyebrow: "THE CODE IS THE WINDOW",
        codeTitle: "A counter in a few lines",
        codeLead: "Groups place the objects for you, and a function given to a button runs in Python when it is clicked.",
        codePoints: [
            { title: "with blocks", text: "The objects of a with block go into its group: the shape of the code is the shape of the window." },
            { title: "Values in Python", text: "count.text is read in Python, with no question to the window. Setting it changes the window." },
            { title: "One call for a function", text: "All the changes of a click go to the window together, so a click costs about {click}." },
        ],
        codeShotAlt: "The window of the counter: the number 0 and two buttons, − and +.",

        // WHY
        whyEyebrow: "WHY",
        whyTitle: "Small, fast enough, easy to read",
        why: [
            { icon: "feather", title: "Small and offline", text: "The package carries basic.js and its components. With its window it is about {size}; no internet, no server, no browser tab." },
            { icon: "bolt", title: "Fast enough to forget", text: "A click reaches your Python function and comes back on the screen in about {click}. The window shows in about {show}." },
            { icon: "code", title: "Code that reads like the window", text: "with blocks for groups, the names of basic.js, values read back without asking the window. An error points to your line." },
            { icon: "grid", title: "Components ready", text: "{classes} components have a Python class: buttons, fields, lists, a table, a chart, dialogs. All {components} of basic.js work with Component()." },
        ],

        // COMPONENTS
        componentsEyebrow: "COMPONENTS",
        componentsTitle: "Ready components, Python classes",
        componentsLead: "Each one takes its params in snake_case and a Python function for a callback. Its state is kept in Python: box.checked, select.value, table.rows.",
        componentsDarkTitle: "A dark window, in one word",
        componentsDarkText: "App(start, theme=\"dark\"): every component takes its dark look, the dialogs and the page too. \"auto\" follows the system. Fifteen components also change it while they are on the page: set_theme().",
        componentsDarkShotAlt: "The gallery in a dark window: buttons, check boxes, a list and a table on dark cards.",
        components: [
            { name: "SmartButton", text: "The default button: a text, an icon, a waiting clock." },
            { name: "TextField", text: "A text field with a title and warnings. EmailField, PasswordField and NumberField are made from it." },
            { name: "UrlField, PhoneField", text: "An address with its protocol, a phone number in its mask; CurrencyField writes an amount in groups of three." },
            { name: "TextAreaField", text: "A text of more lines." },
            { name: "SearchInput", text: "A search box with a clear button; a text at every change." },
            { name: "CheckBox", text: "A check with its label." },
            { name: "Toggle", text: "An on / off switch." },
            { name: "RadioButton", text: "One choice of a group." },
            { name: "SelectBox", text: "A drop-down list, with search." },
            { name: "Slider, RangeSlider", text: "A number on a thin bar with a round knob, or a range with two knobs. SliderField is a number in the shape of a field." },
            { name: "Stepper", text: "A number with - and + buttons. A typed number too." },
            { name: "DatePicker", text: "A date from a calendar. TimePicker and ColorPicker are the same kind of field." },
            { name: "FilePicker", text: "A place to drop files, or a click for the file dialog. The real paths reach Python." },
            { name: "ProgressBar, StepBar", text: "The progress of a job, from a background job too; and the steps of a job in a row." },
            { name: "ItemList", text: "A list to choose from, or a gallery of pictures." },
            { name: "SortableList", text: "A list whose order the user changes: drag a row, or Space and the arrows. Your items come back in the new order." },
            { name: "SmartTable", text: "A table of any size: 100000 rows stay fast. Sorting and a filter." },
            { name: "TreeView", text: "A tree of nodes: a folder is read when it opens." },
            { name: "Tabs", text: "Pages in one window." },
            { name: "Accordion", text: "Sections that fold, one or more open. A closed one keeps its objects." },
            { name: "GridGroup", text: "Objects in columns and rows: a form, the keys of a calculator. The grid() of Tk in a with block." },
            { name: "GraphBox", text: "Charts with no other library: line, bar, pie, radar, scatter. A tooltip, a legend, a table." },
            { name: "LogView", text: "The output of your program in colored lines; print() and logging go into it." },
            { name: "ImageView", text: "A picture or a matplotlib plot, with a zoom. A plot drawn again does not blink." },
            { name: "Canvas", text: "Lines, shapes, texts and pictures, each with a key: a click finds it, a drag moves it, a pen draws free lines." },
            { name: "MarkdownView, JsonView", text: "A text in Markdown: a report, or the answer of an AI as it comes. And a value as a tree: the path of a row, a list of a million items." },
            { name: "JsonEditor", text: "A list or a dict of JSON written in a table: rows, columns, switches, a JSON view, undo. The whole value comes to Python." },
            { name: "ChatView", text: "A conversation with an AI: bubbles, answers in Markdown that come piece by piece, three dots while one is waited for, Send and Stop." },
            { name: "WebView", text: "A web page or an HTML text with its scripts: a plotly chart, a folium map, a table of pandas." },
            { name: "MenuBar, ToolBar", text: "File, Edit, View with shortcuts and submenus, and the row of small buttons under them. What does not fit goes into a menu." },
            { name: "StatusBar, Splitter", text: "A short message at the bottom of the window; and two areas with a line between them: a drag changes their sizes." },
            { name: "CodeEditor", text: "Line numbers and colors for seven languages. A big file stays fast." },
            { name: "ContextMenu, Tooltip", text: "A menu on a right click. A hint under the mouse, a bubble at an object, a popover that holds objects." },
            { name: "Dialog, Toast", text: "Dialogs that return their answer, and a short message in a corner." },
        ],
        componentsOthersTitle: "And the others of basic.js",
        componentsOthersText: "All {components} components of basic.js come in the package. One without a Python class works by its name; App loads it with what it needs.",
        componentsShotAlt: "The window of gauge.py: a ring that shows 72%, with the word Disk under the number.",

        // YOUR OWN COMPONENT
        ownEyebrow: "YOUR OWN COMPONENTS",
        ownTitle: "A component of your own, in plain Python",
        ownLead: "A class that makes its objects in a with block is a component: use it again and again, change it with its methods, share it as a .py file. No JavaScript is needed.",
        ownPoints: [
            { title: "A class and a with block", text: "Its objects go into its group, and the class keeps them: <code>self.box</code>, <code>self.title</code>." },
            { title: "Methods change it", text: "<code>card.set_title()</code> changes its title, as the <code>setX()</code> methods of the components of basic.js do." },
            { title: "A file to share", text: "Put it in <code>card.py</code>, then <code>from card import Card</code> in every program that needs it." },
        ],
        ownShotAlt: "The window of card.py: three white cards, Sales, Stock and Orders, each with a text and an Open button. The first one was clicked: its title says Opened.",

        // DIALOGS
        dialogsEyebrow: "DIALOGS",
        dialogsTitle: "A dialog that returns its answer",
        dialogsLead: "Dialog.confirm() waits for the answer and returns it, like any function. The window keeps working meanwhile: timers run and the page is drawn.",
        dialogsPoints: [
            "alert, confirm, prompt, and ask with your own buttons",
            "from a click, a timer or a background job",
            "a dialog in start() works too: the window is shown first",
        ],
        dialogsShotAlt: "A dialog asks 'Replace it?' with the buttons Cancel and Replace.",

        // EXAMPLES
        examplesEyebrow: "EXAMPLES",
        examplesTitle: "Twenty-seven small programs",
        examplesLead: "In the examples folder of the source. Each one is checked in its real window: a test clicks, types and presses keys as a user would.",
        examples: [
            { key: "editor", image: "editor", title: "A small code editor", text: "Write Python, press F5 and read its output: a menu, a row of buttons, two areas, a dark theme." },
            { key: "markdown_editor", image: "markdown_editor", title: "A small Markdown editor", text: "Write on the left, read on the right: headings, a table, colored code, a file with its pictures." },
            { key: "json_viewer", image: "json_viewer", title: "A small JSON viewer", text: "Open a file, click a row to see its path, right click to copy its value." },
            { key: "json_editor", image: "json_editor", title: "A small JSON editor", text: "A table of products: write a cell, flip a switch, see the JSON; the settings in a window with Cancel and Apply." },
            { key: "chat", image: "chat", title: "A chat", text: "A conversation whose answer comes word by word from a background job; Stop ends it, New chat starts again." },
            { key: "photos", image: "photos", title: "Photos", text: "The pictures of a folder in a gallery; a click opens one large, the wheel zooms it." },
            { key: "paint", image: "paint", title: "Paint", text: "Draw with a pen, take a line back, drag a shape, save the drawing as a picture." },
            { key: "charts", image: "charts", title: "Charts", text: "A live line, bars with a format, a doughnut; a picture of a chart in a file." },
            { key: "files", image: "files", title: "A file tool", text: "A tree, a search in it, a menu, and files dropped with their real paths." },
            { key: "csv_viewer", image: "csv_viewer", title: "CSV viewer", text: "A CSV file in a table with a filter; 100000 rows stay fast." },
            { key: "form", image: "form", title: "A form", text: "Fields of text with warnings, a date, a time, a color, a number." },
            { key: "image_viewer", image: "image_viewer", title: "Image viewer", text: "Open a picture, or draw a plot again and again: the zoom stays." },
            { key: "job_log", image: "job_log", title: "A job and its log", text: "print() and logging in the window, while a job runs in the background." },
            { key: "file_tool", image: "file_tool", title: "Word counter", text: "A file dialog, a background job and a progress bar." },
            { key: "todo", image: "todo", title: "To do", text: "Add, tick and delete with a question. The program is a class." },
            { key: "settings", image: "settings", title: "Settings", text: "Tabs with a form; the values as a dict." },
            { key: "dialogs", image: "dialogs-open", title: "Dialogs", text: "alert, confirm, prompt, ask and a toast." },
            { key: "gallery", image: "gallery", title: "Gallery", text: "Every component with a class, on one page." },
            { key: "gallery-styled", image: "gallery-styled-dark", title: "The gallery in its own look", text: "The same page with looks and a color chosen by the code: style_name for some components, the cyan of the kit for every colored part." },
            { key: "minimal_theme", image: "minimal_theme", title: "The minimal look", text: "Every component in its minimal look, made of lines: App(style=\"minimal\"); a dark window too." },
            { key: "minimal_accent", image: "minimal_accent", title: "The minimal look in a color", text: "The same look in one color of yours: App(style=\"minimal\", accent=\"#2A78D6\")." },
            { key: "calculator", image: "calculator", title: "Calculator", text: "The keys in a GridGroup; the keys of the keyboard work too." },
            { key: "basics", image: "basics", title: "The basic objects", text: "A Box, an Icon, a Label, an Input and a Button, each in a place of its own." },
            { key: "counter", image: "counter", title: "Counter", text: "Two buttons change a number." },
            { key: "greeting", image: "greeting", title: "Greeting", text: "A TextField read in Python; Enter or a button." },
            { key: "clock", image: "clock", title: "Clock", text: "Timers: a clock and a stopwatch." },
            { key: "game", image: "game", title: "Catch the dots", text: "Places of their own, the keys and a timer." },
        ],

        // WHERE IT FITS
        fitEyebrow: "WHERE IT FITS",
        fitTitle: "Small tools, teaching, quick windows",
        fitGoodTitle: "A good choice for",
        fitGood: [
            "a small tool or a script that needs a window",
            "teaching Python with something to see",
            "a modern look without learning Qt, HTML or CSS",
            "people who already use basic.js",
        ],
        fitOtherTitle: "Something else is better for",
        fitOther: [
            "a large desktop application: Qt (PySide6) or Flet",
            "a web application for many users: NiceGUI or a web framework",
            "a data dashboard in the browser: Streamlit",
        ],
        fitNote: "OzdenUI is small on purpose. When it is not enough, these are good choices.",

        // START
        startEyebrow: "GET STARTED",
        startTitle: "Three steps",
        steps: [
            { title: "Install", textOnPypi: "One package; it brings pywebview, the window of the system.", textSoon: "Not on PyPI yet. Until then, install it from its source folder, in a virtual environment (on Windows: <code>.venv\\Scripts\\activate</code>). It brings pywebview, the window of the system." },
            { title: "Write start(page)", text: "Make the objects of the window in it. Groups place them; a function runs on a click." },
            { title: "Run it", text: "A window opens. Your program ends when it is closed." },
        ],
        startHandbook: "Then the handbook: ten short chapters, from the first window to a component of your own, in English and Turkish. Every program in it runs.",
        readHandbook: "Read the handbook", // the hero and the end of Start: a verb, as the other buttons
        startNote: "Python {python}+. Tested on macOS and Windows (WebView2); Linux (GTK or Qt) is not tested yet.",

        // FOOTER
        footerText: "OzdenUI is open source under the {license} license.",
        footerMade: "This page is built with basic.js.",

    },

    tr: {

        htmlLang: "tr",
        pageTitle: "OzdenUI – Düz Python ile modern masaüstü pencereleri",
        pageDescription: "OzdenUI, Python'dan kendi küçük, modern penceresini açar: basic.js'in kutuları, metinleri, düğmeleri ve hazır bileşenleri. Yalnız Python: JavaScript yok, HTML yok, tarayıcı sekmesi ve sunucu yok.",
        languageButton: "EN",
        languageHint: "English",
        nav: { code: "Kod", why: "Neden", components: "Bileşenler", examples: "Örnekler", start: "Başlangıç" },
        navBasicJs: "basic.js",
        navHandbook: "El kitabı",
        navComponents: "basic.js bileşenleri",
        menu: "Menü",
        copy: "Kopyala",
        copied: "Kod kopyalandı.",
        copyFailed: "Kod kopyalanamadı.",

        // HERO
        heroEyebrow: "v{version} · deneysel · Python {python}+",
        heroTitle: "Düz Python ile modern masaüstü pencereleri",
        heroLead: "Pencereyi Python ile yazın: kutular, metinler, düğmeler ve hazır bileşenler kendi küçük penceresinde görünür. Yalnız Python: JavaScript yok, HTML yok, tarayıcı sekmesi ve sunucu yok.",
        heroPrimary: "Başlayın",
        heroSecondary: "Örneklere bakın",
        heroFacts: ["Python sınıfı olan {classes} bileşen", "basic.js'in {components} bileşeninin hepsi adıyla", "penceresiyle birlikte {size}", "{license}"],
        heroSlidesLabel: "Örneklerin pencereleri",
        heroShotAlts: {
            "hero-gallery-styled": "examples/gallery-styled.py'nin penceresi: düğmeler, onay kutusu, açma-kapama düğmesi, seçenek düğmeleri, açılır liste, kaydırıcı, ilerleme çubuğu, not alanı ve listeler, kodunun seçtiği renklerde.",
            "minimal_theme": "examples/minimal_theme.py'nin penceresi: her bileşen minimal görünümünde, küçük ve çizgilerden.",
            "hero-charts": "examples/charts.py'nin penceresi: canlı bir çizgi, çubuklar ve bir halka grafik.",
            "hero-json_editor": "examples/json_editor.py'nin penceresi: bir dükkânın ürünleri bir JSON düzenleyicide, tablo olarak.",
            "hero-photos": "examples/photos.py'nin penceresi: ızgarada küçük resimler ve seçilen resim büyük.",
            "hero-chat-dark": "examples/chat.py koyu bir pencerede: bir soru ve kelime kelime gelen cevabı.",
        },
        installSoon: "Henüz PyPI'da değil: kaynağından kurun (Başlangıç bölümü).",

        // CODE
        codeEyebrow: "KOD PENCERENİN KENDİSİ",
        codeTitle: "Birkaç satırda bir sayaç",
        codeLead: "Gruplar nesneleri sizin için yerleştirir; bir düğmeye verilen fonksiyon, düğmeye tıklanınca Python'da çalışır.",
        codePoints: [
            { title: "with blokları", text: "Bir with bloğunun nesneleri grubuna girer: kodun şekli pencerenin şeklidir." },
            { title: "Değerler Python'da", text: "count.text pencereye sorulmadan Python'da okunur. Değiştirmek pencereyi değiştirir." },
            { title: "Bir fonksiyon için tek çağrı", text: "Bir tıklamanın bütün değişiklikleri pencereye birlikte gider; bir tıklama yaklaşık {click} sürer." },
        ],
        codeShotAlt: "Sayacın penceresi: 0 sayısı ve iki düğme, − ve +.",

        // WHY
        whyEyebrow: "NEDEN",
        whyTitle: "Küçük, yeterince hızlı, kolay okunan",
        why: [
            { icon: "feather", title: "Küçük ve internetsiz", text: "Paket basic.js'i ve bileşenlerini içinde taşır. Penceresiyle birlikte yaklaşık {size}; internet, sunucu ve tarayıcı sekmesi gerekmez." },
            { icon: "bolt", title: "Akla gelmeyecek kadar hızlı", text: "Bir tıklama Python fonksiyonunuza ulaşıp yaklaşık {click} içinde ekrana döner. Pencere yaklaşık yarım saniyede açılır." },
            { icon: "code", title: "Pencere gibi okunan kod", text: "Gruplar için with blokları, basic.js'in adları, pencereye sormadan okunan değerler. Bir hata sizin satırınızı gösterir." },
            { icon: "grid", title: "Hazır bileşenler", text: "{classes} bileşenin Python sınıfı var: düğmeler, alanlar, listeler, tablo, grafik, diyaloglar. basic.js'in {components} bileşeninin hepsi Component() ile çalışır." },
        ],

        // COMPONENTS
        componentsEyebrow: "BİLEŞENLER",
        componentsTitle: "Hazır bileşenler, Python sınıfları",
        componentsLead: "Her biri parametrelerini snake_case adlarıyla, geri çağrıları bir Python fonksiyonu olarak alır. Durumu Python'da tutulur: box.checked, select.value, table.rows.",
        componentsDarkTitle: "Tek kelimeyle koyu pencere",
        componentsDarkText: "App(start, theme=\"dark\"): her bileşen koyu görünüşünü alır, diyaloglar ve sayfa da. \"auto\" sistemi izler. On beş bileşen sayfadayken de değişir: set_theme().",
        componentsDarkShotAlt: "Koyu pencerede galeri: koyu kartlarda düğmeler, onay kutuları, bir liste ve bir tablo.",
        components: [
            { name: "SmartButton", text: "Varsayılan düğme: bir metin, bir ikon, bekleme saati." },
            { name: "TextField", text: "Başlıklı ve uyarılı metin alanı. EmailField, PasswordField ve NumberField ondan yapılır." },
            { name: "UrlField, PhoneField", text: "Protokolüyle bir adres, maskesinde bir telefon numarası; CurrencyField bir tutarı üçlü gruplarla yazar." },
            { name: "TextAreaField", text: "Birden çok satırlık metin." },
            { name: "SearchInput", text: "Temizleme düğmeli arama kutusu; her değişiklikte metni verir." },
            { name: "CheckBox", text: "Etiketiyle bir onay kutusu." },
            { name: "Toggle", text: "Açma-kapama düğmesi." },
            { name: "RadioButton", text: "Bir grubun seçeneklerinden biri." },
            { name: "SelectBox", text: "Aramalı açılır liste." },
            { name: "Slider, RangeSlider", text: "İnce çubukta yuvarlak düğmeli sayı ya da iki düğmeli aralık. SliderField, alan şeklinde bir sayıdır." },
            { name: "Stepper", text: "- ve + düğmeli sayı. Yazarak da girilir." },
            { name: "DatePicker", text: "Takvimden tarih. TimePicker ve ColorPicker aynı türden alanlar." },
            { name: "FilePicker", text: "Dosya bırakılan bir yer ya da tıklayınca dosya diyaloğu. Gerçek yollar Python'a gelir." },
            { name: "ProgressBar, StepBar", text: "Bir işin ilerleyişi, arka plandaki işten de; bir de işin adımları bir satırda." },
            { name: "ItemList", text: "Seçim yapılan bir liste ya da resim galerisi." },
            { name: "SortableList", text: "Sırasını kullanıcının değiştirdiği bir liste: bir satırı sürükleyin ya da Boşluk ve oklarla taşıyın. Öğeleriniz yeni sırasıyla geri gelir." },
            { name: "SmartTable", text: "Her boyutta tablo: 100000 satırda bile hızlı. Sıralama ve süzme." },
            { name: "TreeView", text: "Düğümlerden bir ağaç: klasör açılınca okunur." },
            { name: "Tabs", text: "Bir pencerede birkaç sayfa." },
            { name: "Accordion", text: "Katlanan bölümler, biri ya da birkaçı açık. Kapalı olan nesnelerini korur." },
            { name: "GridGroup", text: "Sütun ve satırlarda nesneler: bir form, hesap makinesinin tuşları. Tk'nın grid()'i, bir with bloğunda." },
            { name: "GraphBox", text: "Başka kütüphanesiz grafikler: çizgi, çubuk, pasta, radar, dağılım. İpucu, açıklama, tablo." },
            { name: "LogView", text: "Programınızın çıktısı renkli satırlarla; print() ve logging oraya gider." },
            { name: "ImageView", text: "Yakınlaştırmalı resim ya da matplotlib grafiği. Yeniden çizilen grafik yanıp sönmez." },
            { name: "Canvas", text: "Çizgi, şekil, yazı ve resim, her biri bir anahtarla: tıklama onu bulur, sürükleme taşır, kalem serbest çizer." },
            { name: "MarkdownView, JsonView", text: "Markdown metni: bir rapor ya da gelirken yapay zekâ cevabı. Bir de değeri ağaç olarak gösterir: satırın yolu, bir milyon öğelik liste." },
            { name: "JsonEditor", text: "Bir tabloda yazılan JSON listesi ya da sözlüğü: satırlar, sütunlar, anahtarlar, JSON görünümü, geri alma. Değerin bütünü Python'a gelir." },
            { name: "ChatView", text: "Bir yapay zekâyla konuşma: balonlar, parça parça gelen Markdown cevaplar, beklenirken üç nokta, Gönder ve Durdur." },
            { name: "WebView", text: "Bir web sayfası ya da betikleriyle bir HTML metni: bir plotly grafiği, bir folium haritası, bir pandas tablosu." },
            { name: "MenuBar, ToolBar", text: "Dosya, Düzenle, Görünüm, kısayollar ve alt menülerle; altında küçük düğmeler. Sığmayan menüye girer." },
            { name: "StatusBar, Splitter", text: "Pencerenin altında kısa mesaj ve küçük parçalar; bir de aralarında çizgi olan iki alan: sürükleyince boyutları değişir." },
            { name: "CodeEditor", text: "Yedi dil için satır numaraları ve renkler. Büyük dosyada bile hızlı." },
            { name: "ContextMenu, Tooltip", text: "Sağ tıkla menü. Fare altında ipucu, bir nesnenin yanında baloncuk, içinde nesne tutan açılır kutu." },
            { name: "Dialog, Toast", text: "Cevabını döndüren diyaloglar ve köşede kısa bir mesaj." },
        ],
        componentsOthersTitle: "Ve basic.js'in ötekileri",
        componentsOthersText: "basic.js'in {components} bileşeninin hepsi pakette. Python sınıfı olmayan bir bileşen adıyla çalışır; App onu gerekenleriyle birlikte yükler.",
        componentsShotAlt: "gauge.py'nin penceresi: %72 gösteren bir halka, sayının altında Disk yazıyor.",

        // YOUR OWN COMPONENT
        ownEyebrow: "KENDİ BİLEŞENİNİZ",
        ownTitle: "Düz Python ile kendi bileşeniniz",
        ownLead: "Nesnelerini bir with bloğunda yapan bir sınıf bir bileşendir: tekrar tekrar kullanılır, kendi yöntemleriyle değişir, bir .py dosyası olarak paylaşılır. JavaScript gerekmez.",
        ownPoints: [
            { title: "Bir sınıf ve bir with bloğu", text: "Nesneleri grubuna girer, sınıf da onları tutar: <code>self.box</code>, <code>self.title</code>." },
            { title: "Yöntemlerle değişir", text: "<code>card.set_title()</code> başlığını değiştirir; basic.js bileşenlerinin <code>setX()</code> yöntemleri gibi." },
            { title: "Paylaşılan bir dosya", text: "<code>card.py</code> dosyasına koyun, onu gereken her programda <code>from card import Card</code> yazın." },
        ],
        ownShotAlt: "card.py'nin penceresi: üç beyaz kart (Sales, Stock, Orders), her birinde bir metin ve bir Open düğmesi. İlkine tıklandı: başlığı Opened oldu.",

        // DIALOGS
        dialogsEyebrow: "DİYALOGLAR",
        dialogsTitle: "Cevabını döndüren bir diyalog",
        dialogsLead: "Dialog.confirm() cevabı bekler ve her fonksiyon gibi döndürür. Pencere bu sırada çalışmaya devam eder: zamanlayıcılar çalışır, sayfa çizilir.",
        dialogsPoints: [
            "alert, confirm, prompt ve kendi düğmelerinizle ask",
            "bir tıklamadan, bir zamanlayıcıdan ya da bir arka plan işinden",
            "start() içindeki bir diyalog da çalışır: pencere önce gösterilir",
        ],
        dialogsShotAlt: "Bir diyalog 'Replace it?' diye soruyor; Cancel ve Replace düğmeleri var.",

        // EXAMPLES
        examplesEyebrow: "ÖRNEKLER",
        examplesTitle: "Yirmi yedi küçük program",
        examplesLead: "Kaynağın examples klasöründe. Her biri gerçek penceresinde denenir: bir test, bir kullanıcı gibi tıklar, yazar ve tuşlara basar.",
        examples: [
            { key: "editor", image: "editor", title: "Küçük bir kod düzenleyici", text: "Python yazın, F5'e basın, çıktısını okuyun: menü, düğme satırı, iki alan, koyu tema." },
            { key: "markdown_editor", image: "markdown_editor", title: "Küçük bir Markdown düzenleyici", text: "Solda yazın, sağda okuyun: başlıklar, tablo, renkli kod, resimleriyle bir dosya." },
            { key: "json_viewer", image: "json_viewer", title: "Küçük bir JSON görüntüleyici", text: "Dosya açın, satıra tıklayıp yolunu görün, sağ tıkla değerini kopyalayın." },
            { key: "json_editor", image: "json_editor", title: "Küçük bir JSON düzenleyici", text: "Bir ürün tablosu: bir hücre yazın, bir anahtarı çevirin, JSON'u görün; ayarlar Cancel ve Apply düğmeli bir pencerede." },
            { key: "chat", image: "chat", title: "Bir sohbet", text: "Cevabı bir arka plan işinden kelime kelime gelen bir konuşma; Stop onu bitirir, New chat baştan başlar." },
            { key: "photos", image: "photos", title: "Fotoğraflar", text: "Bir klasörün resimleri bir galeride; tıklanan büyük açılır, tekerlek yakınlaştırır." },
            { key: "paint", image: "paint", title: "Çizim", text: "Kalemle çizin, bir çizgiyi geri alın, bir şekli sürükleyin, çizimi resim olarak kaydedin." },
            { key: "charts", image: "charts", title: "Grafikler", text: "Canlı bir çizgi, biçimli çubuklar, bir halka; grafiğin resmi bir dosyada." },
            { key: "files", image: "files", title: "Bir dosya aracı", text: "Bir ağaç, içinde arama, bir menü ve gerçek yollarıyla bırakılan dosyalar." },
            { key: "csv_viewer", image: "csv_viewer", title: "CSV görüntüleyici", text: "Süzmeli bir tabloda bir CSV dosyası; 100000 satırda bile hızlı." },
            { key: "form", image: "form", title: "Bir form", text: "Uyarılı metin alanları, bir tarih, bir saat, bir renk, bir sayı." },
            { key: "image_viewer", image: "image_viewer", title: "Resim görüntüleyici", text: "Bir resim açın ya da grafiği tekrar tekrar çizin: yakınlaştırma korunur." },
            { key: "job_log", image: "job_log", title: "Bir iş ve günlüğü", text: "Arka planda iş sürerken print() ve logging pencerede." },
            { key: "file_tool", image: "file_tool", title: "Kelime sayacı", text: "Dosya diyaloğu, arka plan işi ve ilerleme çubuğu." },
            { key: "todo", image: "todo", title: "Yapılacaklar", text: "Ekle, işaretle, sorarak sil. Program bir sınıftır." },
            { key: "settings", image: "settings", title: "Ayarlar", text: "Sekmelerde bir form; değerler bir sözlük olarak." },
            { key: "dialogs", image: "dialogs-open", title: "Diyaloglar", text: "alert, confirm, prompt, ask ve bir toast." },
            { key: "gallery", image: "gallery", title: "Galeri", text: "Sınıfı olan bütün bileşenler bir sayfada." },
            { key: "gallery-styled", image: "gallery-styled-dark", title: "Kendi görünümüyle galeri", text: "Aynı sayfa, görünümleri ve rengi kodla seçilmiş: bazı bileşenlerde style_name, renkli her parçada kitin camgöbeği rengi." },
            { key: "minimal_theme", image: "minimal_theme", title: "Minimal görünüm", text: "Çizgilerden yapılmış minimal görünümüyle her bileşen: App(style=\"minimal\"); koyu pencerede de." },
            { key: "minimal_accent", image: "minimal_accent", title: "Bir renkte minimal görünüm", text: "Aynı görünüm sizin bir renginizde: App(style=\"minimal\", accent=\"#2A78D6\")." },
            { key: "calculator", image: "calculator", title: "Hesap makinesi", text: "Tuşlar bir GridGroup'ta; klavyenin tuşları da çalışır." },
            { key: "basics", image: "basics", title: "Temel nesneler", text: "Bir Box, bir Icon, bir Label, bir Input ve bir Button, her biri kendi yerinde." },
            { key: "counter", image: "counter", title: "Sayaç", text: "İki düğme bir sayıyı değiştirir." },
            { key: "greeting", image: "greeting", title: "Selam", text: "Python'da okunan bir TextField; Enter ya da düğme." },
            { key: "clock", image: "clock", title: "Saat", text: "Zamanlayıcılar: bir saat ve bir kronometre." },
            { key: "game", image: "game", title: "Noktaları yakala", text: "Kendi yerindeki nesneler, tuşlar ve bir zamanlayıcı." },
        ],

        // WHERE IT FITS
        fitEyebrow: "NEREDE UYGUN",
        fitTitle: "Küçük araçlar, öğretim, hızlı pencereler",
        fitGoodTitle: "İyi bir seçim",
        fitGood: [
            "pencere gereken küçük bir araç ya da betik için",
            "görecek bir şeyle Python öğretmek için",
            "Qt, HTML ya da CSS öğrenmeden modern bir görünüş için",
            "zaten basic.js kullananlar için",
        ],
        fitOtherTitle: "Başka bir şey daha iyi",
        fitOther: [
            "büyük bir masaüstü uygulaması için: Qt (PySide6) ya da Flet",
            "çok kullanıcılı bir web uygulaması için: NiceGUI ya da bir web çatısı",
            "tarayıcıda bir veri panosu için: Streamlit",
        ],
        fitNote: "OzdenUI bilerek küçük. Yetmediğinde bunlar iyi seçimler.",

        // START
        startEyebrow: "BAŞLANGIÇ",
        startTitle: "Üç adım",
        steps: [
            { title: "Kurun", textOnPypi: "Tek paket; sistemin penceresi pywebview'i de getirir.", textSoon: "Henüz PyPI'da değil. O zamana kadar kaynak klasöründen, bir sanal ortama kurun (Windows'ta: <code>.venv\\Scripts\\activate</code>). Sistemin penceresi pywebview'i de getirir." },
            { title: "start(page) yazın", text: "Pencerenin nesnelerini içinde yapın. Gruplar onları yerleştirir; tıklanınca bir fonksiyon çalışır." },
            { title: "Çalıştırın", text: "Bir pencere açılır. Pencere kapanınca programınız biter." },
        ],
        startHandbook: "Sonra el kitabı: ilk pencereden kendi bileşeninize on kısa bölüm, İngilizce ve Türkçe. İçindeki her program çalışır.",
        readHandbook: "El kitabını okuyun",
        startNote: "Python {python}+. macOS'ta ve Windows'ta (WebView2) denendi; Linux (GTK ya da Qt) henüz denenmedi.",

        // FOOTER
        footerText: "OzdenUI, {license} lisansı ile açık kaynaktır.",
        footerMade: "Bu sayfa basic.js ile yapılmıştır.",

    },

};

TEXTS.fill = function (text) {
    return String(text)
        .replace(/\{version\}/g, CONFIG.version)
        .replace(/\{python\}/g, CONFIG.pythonVersion)
        .replace(/\{classes\}/g, CONFIG.componentClasses)
        .replace(/\{components\}/g, CONFIG.componentCount)
        .replace(/\{size\}/g, CONFIG.installSize)
        .replace(/\{click\}/g, CONFIG.clickTime)
        .replace(/\{show\}/g, CONFIG.showTime)
        .replace(/\{license\}/g, CONFIG.license);
};
