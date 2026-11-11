/* Bismillah */

/*

OzdenUI Handbook Website - Code Block - v26.11 (2026-11-09; from 03-webpages/webpage-handbook, v26.11)

The code blocks of the handbook: the language, a Copy button and the colored code. The code is Python (and a terminal
line or two): it is shown, not run. The site of basic.js runs its JavaScript examples in the page; a Python program
needs Python, so that part is not here.
The colors come from js/code-highlight.js of the page of the package ("py", "text", "js", "html", "css").

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const CodeBlock = {};

// The name of a language in the Markdown -> the language of js/code-highlight.js. Anything else: plain text (a terminal).
CodeBlock.LANGUAGES = { python: "py", py: "py", javascript: "js", js: "js", html: "html", htm: "html", css: "css" };

CodeBlock.highlightLanguage = function (language) {
    return CodeBlock.LANGUAGES[language] || "text";
};

// *** CREATE:
CodeBlock.create = function (block) {

    const T = SITE.T;
    const L = SITE.L;
    const language = CodeBlock.highlightLanguage(block.language);

    // GROUP: The card
    const card = VGroup({ width: "100%", height: "auto", align: "left top", gap: 0, color: SITE.CODE_BG, round: 12 });
    card.clipContent = 1;
    card.elem.style.alignItems = "stretch";
    card.elem.style.flexShrink = "0";

        // GROUP: The bar: the language and Copy
        HGroup({ width: "100%", height: 42, align: "left center", gap: 8, padding: [14, 0], color: SITE.CODE_BAR });
        that.elem.style.flexShrink = "0";

            // LABEL: The language ("python", or "terminal" for a block without one)
            Label({ text: basic.escapeHtml(block.language || "terminal"), fontSize: 12, textColor: SITE.CODE_SOFT });
            that.elem.style.fontFamily = SITE.MONO;
            that.elem.style.whiteSpace = "nowrap";
            that.elem.style.flexShrink = "0";

            SITE.spacer();

            SITE.button({ icon: "copy", kind: "code", height: 28, hint: T.copy, onClick: function () { CodeBlock.copy(block.code); } });

        endGroup();

        // BOX: The code (plain HTML: it can be selected)
        // NOTE: basic.css gives the boxes pointer-events: none and the page user-select: none; they are opened here.
        card.codeBox = Box({ width: "100%", height: "auto", color: "transparent" });
        card.codeBox.elem.style.position = "relative";

        const pre = document.createElement("pre");
        pre.style.cssText = "margin: 0px; padding: 16px 18px; white-space: pre-wrap; word-break: break-word; tab-size: 4;"
            + "font-family: " + SITE.MONO + "; font-size: " + (L.mobile ? 12 : 13) + "px; line-height: 21px;"
            + "color: " + SITE.CODE_TEXT + "; outline: none;"
            + "pointer-events: auto; user-select: text; -webkit-user-select: text; cursor: text;";
        pre.setAttribute("spellcheck", "false");
        pre.innerHTML = CodeHighlight.highlight(block.code, language);
        card.codeBox.elem.appendChild(pre);
        card.pre = pre;

    endGroup();

    return card;

};

// *** COPY:
CodeBlock.copy = function (text) {

    const T = SITE.T;

    const done = function () {
        if (typeof Toast === "function") Toast.show({ key: "copy", type: "success", messageText: T.copied });
    };

    const fail = function () {
        if (typeof Toast === "function") Toast.show({ key: "copy", type: "error", messageText: T.copyFailed });
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, fail);
        return;
    }

    const area = document.createElement("textarea");
    area.value = text;
    area.style.cssText = "position: fixed; left: -9999px; top: 0px;";
    document.body.appendChild(area);
    area.select();

    let ok = false;
    try {
        ok = document.execCommand("copy");
    } catch (error) {
        ok = false;
    }

    area.remove();
    if (ok) done(); else fail();

};
