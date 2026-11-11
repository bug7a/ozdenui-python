/* Bismillah */

/*

basic.js Website - Code Highlight - v26.09 (copy of index/code-highlight.js (repo root), plus CSS)
OzdenUI Website (2026-11-04): a copy of 03-webpages/webpage-basicjs/js/code-highlight.js, plus Python
("py": CodeHighlight.py) and plain text ("text": a terminal command, no colors).

- Kod panelinin küçük, bağımlılıksız sözdizimi renklendiricisi: JavaScript ve HTML.
  HTML içindeki <script> blokları JavaScript olarak renklenir.
- A small, dependency-free syntax highlighter for the code panel: JavaScript and HTML.
  <script> blocks inside HTML are highlighted as JavaScript.

USAGE:
CodeHighlight.injectCss();
elem.innerHTML = CodeHighlight.highlight(text, "js"); // "js", "html", "css", "py", "text"

NOTE: Tam bir ayrıştırıcı değildir; renklendirme amaçlıdır. Hatalı bir belirteç en fazla o satırı etkiler.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const CodeHighlight = {};

// *** TOKEN COLORS: (GitHub dark renkleri)
CodeHighlight.COLORS = {
    c: "#8B949E",   // comment
    k: "#FF7B72",   // keyword
    s: "#A5D6FF",   // string
    r: "#A5D6FF",   // regex
    n: "#79C0FF",   // number
    l: "#79C0FF",   // literal (true, null...), CONSTANT
    t: "#FFA657",   // Type / Component (PascalCase)
    f: "#D2A8FF",   // function call
    b: "#7EE787",   // basic.js name (page, that, Box, Label...)
    tag: "#7EE787", // html tag
    at: "#79C0FF",  // html attribute
    av: "#A5D6FF",  // html attribute value
    dt: "#8B949E",  // <!DOCTYPE>
    d: "#D2A8FF",   // a decorator of Python (@property)
};

CodeHighlight.JS_KEYWORDS = new Set(("break case catch class const continue debugger default delete do else export extends finally for "
    + "from function if import in instanceof let new of return static super switch this throw try typeof var void while with yield async await").split(" "));

CodeHighlight.JS_LITERALS = new Set("true false null undefined NaN Infinity".split(" "));

CodeHighlight.BASIC_NAMES = new Set(("page that prevThat basic Box Label Button Input Icon HGroup VGroup AutoLayout startBox endBox "
    + "startFlexBox endFlexBox endGroup startObject endObject startExtendedObject endExtendedObject mergeIntoIfMissing createIn "
    + "setDefaultContainerBox println Black White Alpha random waitAndRun setLoopTimer withPageZoom makeBasicObject").split(" "));

// WHY: Bu işaretlerden (veya bu kelimelerden) sonra gelen "/" bölme değil, düzenli ifadedir (regex).
CodeHighlight.REGEX_BEFORE = new Set("( , = : [ ! & | ? { } ; + - * % < > ~ ^".split(" "));
CodeHighlight.REGEX_AFTER_WORDS = new Set("return typeof case else in of new delete void throw yield await".split(" "));

CodeHighlight.RE = {
    blockComment: /\/\*[\s\S]*?(?:\*\/|$)/y,
    lineComment: /\/\/[^\n]*/y,
    string: /"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?|`(?:\\[\s\S]|[^`\\])*`?/y,
    regex: /\/(?![*\/])(?:\\.|\[(?:\\.|[^\]\\\n])*\]|[^\/\\\n\[])+\/[dgimsuy]*/y,
    number: /(?:0[xX][\da-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?![\w$])/y,
    ident: /[A-Za-z_$][\w$]*/y,
    space: /\s+/y,
};

CodeHighlight.escape = function (text) {
    return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
};

CodeHighlight.span = function (type, text) {
    return '<span class="bjs-' + type + '">' + CodeHighlight.escape(text) + '</span>';
};

CodeHighlight.highlight = function (text, language) {
    if (language == "html") return CodeHighlight.html(text);
    if (language == "css") return CodeHighlight.css(text);
    if (language == "py") return CodeHighlight.py(text);
    if (language == "text") return CodeHighlight.escape(text); // a terminal command: no colors
    return CodeHighlight.js(text);
};

// *** JAVASCRIPT:
CodeHighlight.js = function (code) {

    const RE = CodeHighlight.RE;
    const span = CodeHighlight.span;
    const length = code.length;
    let out = "";
    let index = 0;
    let previous = ""; // Son anlamlı belirteç (boşluk ve yorum hariç)

    const readAt = function (regex) {
        regex.lastIndex = index;
        const match = regex.exec(code);
        return (match && match[0].length) ? match[0] : null;
    };

    // Kelimeden sonraki ilk boşluk olmayan karakter.
    const nextChar = function (from) {
        let i = from;
        while (i < length && (code[i] == " " || code[i] == "\t")) i++;
        return code[i] || "";
    };

    const regexAllowed = function () {
        return previous === "" || CodeHighlight.REGEX_BEFORE.has(previous) || CodeHighlight.REGEX_AFTER_WORDS.has(previous);
    };

    while (index < length) {

        let token = null;
        const char = code[index];

        if (char == "/" && (token = readAt(RE.blockComment))) {
            out += span("c", token);
        } else if (char == "/" && (token = readAt(RE.lineComment))) {
            out += span("c", token);
        } else if ((char == '"' || char == "'" || char == "`") && (token = readAt(RE.string))) {
            out += span("s", token);
            previous = "str";
        } else if (char == "/" && regexAllowed() && (token = readAt(RE.regex))) {
            out += span("r", token);
            previous = "regex";
        } else if (char >= "0" && char <= "9" && (token = readAt(RE.number))) {
            out += span("n", token);
            previous = "num";
        } else if ((token = readAt(RE.ident))) {
            const after = nextChar(index + token.length);
            let type = "";
            if (previous == ".") type = (after == "(") ? "f" : "";
            else if (CodeHighlight.JS_KEYWORDS.has(token)) type = "k";
            else if (CodeHighlight.JS_LITERALS.has(token)) type = "l";
            else if (CodeHighlight.BASIC_NAMES.has(token)) type = "b";
            else if (/^[A-Z][A-Z0-9_]+$/.test(token)) type = "l";
            else if (/^[A-Z]/.test(token)) type = "t";
            else if (after == "(") type = "f";
            out += (type) ? span(type, token) : token;
            previous = token;
        } else if ((token = readAt(RE.space))) {
            out += token;
        } else {
            token = char;
            out += CodeHighlight.escape(token);
            previous = token;
        }

        index += token.length;

    }

    return out;

};

// *** PYTHON (2026-11-04, the site of OzdenUI): the same scanner, the rules of Python.
// A comment is # (// is a division), strings may have a prefix (f, r, b...) and three quotes, no regex literals.
CodeHighlight.PY_KEYWORDS = new Set(("and as assert async await break class continue def del elif else except finally for from "
    + "global if import in is lambda nonlocal not or pass raise return try while with yield match case").split(" "));
CodeHighlight.PY_LITERALS = new Set("True False None self cls".split(" "));
// The names of the library (OzdenUI) are green, as the names of basic.js in the JS code
CodeHighlight.PY_NAMES = new Set(("App Box VGroup HGroup Label Button Input Icon Component SmartButton CheckBox Toggle "
    + "RadioButton SelectBox TextAreaField SliderField ProgressBar ItemList SmartTable Tabs Dialog Toast LogView ImageView Canvas MarkdownView JsonView JsonEditor MenuBar ToolBar StatusBar Splitter CodeEditor "
    + "TextField EmailField PasswordField NumberField Slider RangeSlider StepBar SearchInput GraphBox FilePicker TreeView ContextMenu Tooltip DatePicker TimePicker ColorPicker Stepper Accordion GridGroup page "
    + "UrlField PhoneField CurrencyField SortableList ChatView WebView ScrollArea SidePanel LoadingScreen TagInput DataTable").split(" "));
CodeHighlight.PY_RE = {
    comment: /#[^\n]*/y,
    string: /(?:[rRbBuUfF]{1,2})?(?:"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')/y,
    number: /(?:0[xX][0-9a-fA-F_]+|0[oO][0-7_]+|0[bB][01_]+|\d[\d_]*\.?[\d_]*(?:[eE][+-]?\d+)?[jJ]?|\.\d[\d_]*(?:[eE][+-]?\d+)?[jJ]?)/y,
    ident: /[A-Za-z_]\w*/y,
    decorator: /@[A-Za-z_][\w.]*/y,
    space: /[ \t\n\r]+/y,
};

CodeHighlight.py = function (code) {

    const RE = CodeHighlight.PY_RE;
    const span = CodeHighlight.span;
    const length = code.length;
    let out = "";
    let index = 0;
    let previous = ""; // the last token that means something (not a space or a comment)

    const readAt = function (regex) {
        regex.lastIndex = index;
        const match = regex.exec(code);
        return (match && match[0].length) ? match[0] : null;
    };

    const nextChar = function (from) {
        let i = from;
        while (i < length && (code[i] == " " || code[i] == "\t")) i++;
        return code[i] || "";
    };

    const isLineStart = function () {
        let i = index - 1;
        while (i >= 0 && (code[i] == " " || code[i] == "\t")) i--;
        return i < 0 || code[i] == "\n";
    };

    const identType = function (token, after) {
        if (previous == ".") return (after == "(") ? "f" : "";
        if (previous == "def") return "f";
        if (previous == "class") return "t";
        if (CodeHighlight.PY_KEYWORDS.has(token)) return "k";
        if (CodeHighlight.PY_LITERALS.has(token)) return "l";
        if (CodeHighlight.PY_NAMES.has(token)) return "b";
        if (/^[A-Z][A-Z0-9_]+$/.test(token)) return "l";
        if (/^[A-Z]/.test(token)) return "t";
        if (after == "(") return "f";
        return "";
    };

    while (index < length) {

        let token = null;
        const char = code[index];
        const isQuoteOrPrefix = /["'rRbBuUfF]/.test(char);
        const isNumberStart = /[0-9]/.test(char) || (char == "." && /[0-9]/.test(code[index + 1] || ""));

        if (char == "#" && (token = readAt(RE.comment))) {
            out += span("c", token);
        } else if (char == "@" && isLineStart() && (token = readAt(RE.decorator))) {
            out += span("d", token);
            previous = "decorator";
        } else if (isQuoteOrPrefix && (token = readAt(RE.string))) {
            const prefix = /^[a-zA-Z]*/.exec(token)[0];
            out += /[fF]/.test(prefix) ? CodeHighlight.pyFString(token) : span("s", token);
            previous = "str";
        } else if (isNumberStart && (token = readAt(RE.number))) {
            out += span("n", token);
            previous = "num";
        } else if ((token = readAt(RE.ident))) {
            const type = identType(token, nextChar(index + token.length));
            out += (type) ? span(type, token) : token;
            previous = token;
        } else if ((token = readAt(RE.space))) {
            out += token;
        } else {
            token = char;
            out += CodeHighlight.escape(token);
            previous = token;
        }

        index += token.length;

    }

    return out;

};

// An f-string: its text in the color of a string, its {expressions} as code. {{ and }} stay text.
// WHY flat spans (the string span is closed before an expression): SITE.codeHtml opens only one span again on a new
//     line, so a span inside a span broke a string of more lines.
CodeHighlight.pyFString = function (token) {

    const span = CodeHighlight.span;
    let out = "";
    let text = "";
    let i = 0;

    const flushText = function () {
        if (text) out += span("s", text);
        text = "";
    };

    // The } that closes the { at start (a {} inside it counts)
    const closingBrace = function (start) {
        let depth = 0;
        for (let j = start; j < token.length; j++) {
            if (token[j] == "{") depth++;
            if (token[j] == "}") depth--;
            if (depth === 0) return j;
        }
        return -1;
    };

    while (i < token.length) {
        const char = token[i];
        if ((char == "{" || char == "}") && token[i + 1] == char) {
            text += char + char;
            i += 2;
            continue;
        }
        const end = (char == "{") ? closingBrace(i) : -1;
        if (end < 0) {
            text += char;
            i++;
            continue;
        }
        flushText();
        out += CodeHighlight.escape("{") + CodeHighlight.py(token.slice(i + 1, end)) + CodeHighlight.escape("}");
        i = end + 1;
    }
    flushText();

    return out;

};

// *** HTML:
CodeHighlight.html = function (code) {

    const span = CodeHighlight.span;
    const escape = CodeHighlight.escape;
    const length = code.length;
    let out = "";
    let index = 0;

    while (index < length) {

        const open = code.indexOf("<", index);

        if (open == -1) {
            out += escape(code.slice(index));
            break;
        }

        // Metin
        out += escape(code.slice(index, open));
        index = open;

        // <!-- yorum -->
        if (code.startsWith("<!--", index)) {
            const end = code.indexOf("-->", index + 4);
            const stop = (end == -1) ? length : end + 3;
            out += span("c", code.slice(index, stop));
            index = stop;
            continue;
        }

        // <!DOCTYPE html>
        if (code.startsWith("<!", index)) {
            const end = code.indexOf(">", index);
            const stop = (end == -1) ? length : end + 1;
            out += span("dt", code.slice(index, stop));
            index = stop;
            continue;
        }

        // <tag ...> veya </tag>
        const tagMatch = /^<\/?([A-Za-z][\w-]*)/.exec(code.slice(index, index + 64));
        if (!tagMatch) {
            out += escape("<");
            index++;
            continue;
        }

        const tagEnd = CodeHighlight.findTagEnd(code, index);
        const tagText = code.slice(index, tagEnd);
        out += CodeHighlight.htmlTag(tagText);
        index = tagEnd;

        // <script> ve <style> içeriği
        const tagName = tagMatch[1].toLowerCase();
        const isClosing = (tagText[1] == "/");
        if (!isClosing && (tagName == "script" || tagName == "style")) {
            const closeAt = code.toLowerCase().indexOf("</" + tagName, index);
            const stop = (closeAt == -1) ? length : closeAt;
            const inner = code.slice(index, stop);
            out += (tagName == "script") ? CodeHighlight.js(inner) : escape(inner);
            index = stop;
        }

    }

    return out;

};

// Tırnak içindeki ">" işaretini atlayarak, etiketin bittiği yer.
CodeHighlight.findTagEnd = function (code, from) {

    let quote = "";

    for (let i = from + 1; i < code.length; i++) {
        const char = code[i];
        if (quote) {
            if (char == quote) quote = "";
        } else if (char == '"' || char == "'") {
            quote = char;
        } else if (char == ">") {
            return i + 1;
        }
    }

    return code.length;

};

// Tek bir etiketi renklendirir: <script src="x.js" type="text/javascript">
CodeHighlight.htmlTag = function (tagText) {

    const span = CodeHighlight.span;
    const escape = CodeHighlight.escape;
    const match = /^(<\/?)([A-Za-z][\w-]*)([\s\S]*?)(\/?>)?$/.exec(tagText);

    if (!match) return escape(tagText);

    let out = escape(match[1]) + span("tag", match[2]);

    const attrs = match[3] || "";
    const attrRegex = /([^\s=\/>]+)(\s*=\s*)?("[^"]*"?|'[^']*'?|[^\s>]+)?/g;
    let last = 0;
    let attr;

    while ((attr = attrRegex.exec(attrs))) {
        if (!attr[0].length) { attrRegex.lastIndex++; continue; }
        out += escape(attrs.slice(last, attr.index));
        out += span("at", attr[1]);
        if (attr[2]) out += escape(attr[2]);
        if (attr[3]) out += span("av", attr[3]);
        last = attr.index + attr[0].length;
    }

    out += escape(attrs.slice(last));
    out += escape(match[4] || "");

    return out;

};

// *** CSS LANGUAGE:
// Seçiciler, özellik adları, sayılar ve renkler. (Sadece renklendirme amaçlı.)
CodeHighlight.css = function (code) {

    const span = CodeHighlight.span;
    const escape = CodeHighlight.escape;
    let out = "";
    let depth = 0;
    let index = 0;

    // Bir değer: sayılar (px, %) ve #renkler
    const value = function (text) {
        let html = "";
        let last = 0;
        const regex = /#[0-9a-fA-F]{3,8}\b|-?\d+(?:\.\d+)?(?:px|%|em|rem|vh|vw|s|ms)?\b|"[^"]*"|'[^']*'/g;
        let match;
        while ((match = regex.exec(text))) {
            html += escape(text.slice(last, match.index));
            html += span(/^["']/.test(match[0]) ? "s" : "n", match[0]);
            last = match.index + match[0].length;
        }
        return html + escape(text.slice(last));
    };

    while (index < code.length) {

        if (code.startsWith("/*", index)) {
            const end = code.indexOf("*/", index + 2);
            const stop = (end == -1) ? code.length : end + 2;
            out += span("c", code.slice(index, stop));
            index = stop;
            continue;
        }

        const char = code[index];

        if (char == "{") { depth++; out += "{"; index++; continue; }
        if (char == "}") { depth = Math.max(0, depth - 1); out += "}"; index++; continue; }

        // Bir sonraki özel işarete kadar olan parça
        let next = index;
        while (next < code.length && "{};".indexOf(code[next]) == -1 && !code.startsWith("/*", next)) next++;
        if (next < code.length && code[next] == ";") next++;
        const part = code.slice(index, next);

        if (depth == 0) {
            // Seçici: .card h2
            out += part.replace(/^(\s*)([\s\S]*?)(\s*)$/, function (all, before, selector, after) {
                return before + (selector ? span("tag", selector) : "") + after;
            });
        } else {
            // Bildirim: display: flex;
            const colon = part.indexOf(":");
            if (colon > -1) {
                const name = part.slice(0, colon);
                const nameMatch = /^(\s*)(.*?)(\s*)$/.exec(name);
                out += nameMatch[1] + span("at", nameMatch[2]) + nameMatch[3] + ":" + value(part.slice(colon + 1));
            } else {
                out += escape(part);
            }
        }

        index = next;

    }

    return out;

};

// *** CSS:
// WHY: Belirteç renkleri satır içi stil ile de verilebilirdi, ama binlerce satırda sınıf adı çok daha kısa.
CodeHighlight.injectCss = function () {

    if (document.getElementById("bjs-code-css")) return;

    let css = "";
    for (let type in CodeHighlight.COLORS) {
        css += ".bjs-" + type + "{color:" + CodeHighlight.COLORS[type] + ";}";
    }
    css += ".bjs-c{font-style:italic;}";

    const style = document.createElement("style");
    style.id = "bjs-code-css";
    style.textContent = css;
    document.head.appendChild(style);

};
