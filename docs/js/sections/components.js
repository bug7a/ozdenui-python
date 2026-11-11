/* Bismillah */

/*

OzdenUI Website - Components - v26.11 (2026-11-04)

The components with a Python class (a card each: its name, what it is, one line of code), then the others of
basic.js: the code of Component() next to its window (gauge.py).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const ComponentsSection = function () {

    const L = SITE.L;
    const T = SITE.T;
    const columnWidth = L.stacked ? L.content : L.columns(2);
    const GAUGE_WIDTH = 240; // the picture is 440 px wide: sharp enough at 1.5x

    SITE.startSection({ key: "components" });

        SITE.sectionIntro(T.componentsEyebrow, T.componentsTitle, T.componentsLead);

        SITE.startGrid(L.mobile ? 10 : 14);

            T.components.forEach(function (item) {
                ComponentsSection.card(item.name, item.text, SAMPLES.componentLines[item.name]);
            });

        SITE.endGrid();

        // GROUP: The others of basic.js
        HGroup({ width: "100%", height: "auto", align: "center top", gap: L.gap, wrap: 1 });
        that.clipContent = 0;
        that.elem.style.marginTop = (L.mobile ? 28 : 48) + "px";

            VGroup({ width: columnWidth, height: "auto", align: "left top", gap: 14 });
            that.clipContent = 0;
                SITE.h3(T.componentsOthersTitle);
                that.fontSize = L.mobile ? 20 : 24;
                SITE.text(TEXTS.fill(T.componentsOthersText), "100%", 0, 16);
                SITE.codePanel({ title: "gauge.py", code: SAMPLES.others, language: "py", width: columnWidth });
            endGroup();

            // GROUP: The window of gauge.py, in the middle of its column
            VGroup({ width: columnWidth, height: "auto", align: "center center" });
            that.clipContent = 0;
            that.elem.style.alignSelf = "center";
                SHOTS.window({ name: "gauge", title: "gauge.py", alt: T.componentsShotAlt, width: Math.min(columnWidth, GAUGE_WIDTH) });
            endGroup();

        endGroup();

        // GROUP: A dark window
        HGroup({ width: "100%", height: "auto", align: "center top", gap: L.gap, wrap: 1 });
        that.clipContent = 0;
        that.elem.style.marginTop = (L.mobile ? 28 : 48) + "px";

            VGroup({ width: columnWidth, height: "auto", align: "left top", gap: 14 });
            that.clipContent = 0;
                SITE.h3(T.componentsDarkTitle);
                that.fontSize = L.mobile ? 20 : 24;
                SITE.text(T.componentsDarkText, "100%", 0, 16);
                SITE.codePanel({ title: "app.py", code: SAMPLES.dark, language: "py", width: columnWidth });
            endGroup();

            VGroup({ width: columnWidth, height: "auto", align: "center center" });
            that.clipContent = 0;
            that.elem.style.alignSelf = "center";
                SHOTS.window({ name: "gallery-dark", title: "gallery.py", alt: T.componentsDarkShotAlt, width: columnWidth });
            endGroup();

        endGroup();

    SITE.endSection();

};

// GROUP: The card of a component: its name, what it is, a line of code
ComponentsSection.card = function (name, text, codeLine) {

    const L = SITE.L;

    SITE.startCard({ width: L.columns(4), gap: 10, padding: L.mobile ? 18 : 22 });

        SITE.label(name, { fontSize: 16, bold: 1, textColor: SITE.INK });
        that.elem.style.fontFamily = SITE.MONO;

        SITE.text(text, "100%", 0, 14);

        // LABEL: The line of code (dark, as the code panels)
        Label({ width: "100%", text: SITE.codeHtml(codeLine, "py"), fontSize: 12, color: SITE.CODE_BG, round: 8 });
        that.css = { fontFamily: SITE.MONO, padding: "8px 10px", whiteSpace: "pre-wrap", wordBreak: "break-word", lineHeight: "18px", color: SITE.CODE_TEXT, marginTop: "auto" };

    SITE.endCard();

};
