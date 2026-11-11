/* Bismillah */

/*

OzdenUI Website - Start - v26.11 (2026-11-04)

Three steps: install it (from PyPI, or from its source while it is not there), write start(page), run it. Then the handbook.
On a wide screen the words of a step are on the left and its code on the right (as the site of basic.js).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const StartSection = function () {

    const L = SITE.L;
    const T = SITE.T;
    const stacked = L.stacked;
    const textWidth = stacked ? L.content : Math.round(L.content * 0.36);
    const codeWidth = stacked ? L.content : L.content - textWidth - 48;
    const codes = StartSection.codes();

    SITE.startSection({ key: "start", color: SITE.BG_SOFT, gap: stacked ? 36 : 44 });

        SITE.sectionIntro(T.startEyebrow, T.startTitle);

        T.steps.forEach(function (step, index) {

            // GROUP: A step
            HGroup({ width: "100%", height: "auto", align: "left top", gap: stacked ? 18 : 48, wrap: stacked ? 1 : 0 });
            that.clipContent = 0;

                // GROUP: The words
                VGroup({ width: textWidth, height: "auto", align: "left top", gap: 12 });
                    StartSection.number(index + 1);
                    SITE.h3(step.title);
                    SITE.text(StartSection.textOf(step), "100%", 0, 15);
                endGroup();

                const code = codes[index];
                const panel = SITE.codePanel({ title: code.title, code: code.code, language: code.language, width: codeWidth });
                panel.elem.style.alignSelf = "center";

            endGroup();

        });

        // GROUP: Then the handbook
        VGroup({ width: "100%", height: "auto", align: "center top", gap: 16 });
        that.clipContent = 0;
        that.elem.style.marginTop = (stacked ? 8 : 16) + "px";

            SITE.text(T.startHandbook, Math.min(640, L.content), 0, 15);
            that.elem.style.textAlign = "center";
            SITE.button({ text: T.readHandbook, icon: "book", kind: "dark", height: 44, fontSize: 15, onClick: function () { location.href = SiteApp.handbookAddress(); } });

        endGroup();

        SITE.text(TEXTS.fill(T.startNote), Math.min(760, L.content), 0, 14);
        that.elem.style.textAlign = "center";
        that.elem.style.alignSelf = "center";

    SITE.endSection();

};

// The code of each step: a terminal, the file, a terminal
StartSection.codes = function () {

    const install = CONFIG.isOnPypi ? SAMPLES.installPypi : SAMPLES.installSource;

    return [
        { title: "terminal", code: install, language: "text" },
        { title: "app.py", code: SAMPLES.hello, language: "py" },
        { title: "terminal", code: SAMPLES.run, language: "text" },
    ];

};

// The install step says where it comes from (PyPI, or the source until then)
StartSection.textOf = function (step) {
    if (step.text) return step.text;
    if (CONFIG.isOnPypi) return step.textOnPypi;
    return step.textSoon;
};

// LABEL: The number of a step in a circle
StartSection.number = function (number) {

    const SIZE = 38;

    Label({ text: String(number), width: SIZE, height: SIZE, fontSize: 17, textColor: SITE.ON_ACCENT, color: SITE.ACCENT, round: SIZE / 2 });
    that.elem.style.fontFamily = SITE.BOLD;
    that.elem.style.display = "flex";
    that.elem.style.alignItems = "center";
    that.elem.style.justifyContent = "center";

    return that;

};
