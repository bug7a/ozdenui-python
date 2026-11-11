/* Bismillah */

/*

OzdenUI Website - Code - v26.11 (2026-11-04)

The code of examples/counter.py next to the picture of its window, and three things the code shows.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const CodeSection = function () {

    const L = SITE.L;
    const T = SITE.T;
    const columnWidth = L.stacked ? L.content : L.columns(2);

    SITE.startSection({ key: "code" });

        SITE.sectionIntro(T.codeEyebrow, T.codeTitle, T.codeLead);

        // GROUP: The code and its window (one under the other on a phone and a tablet)
        HGroup({ width: "100%", height: "auto", align: "center top", gap: L.gap, wrap: 1 });
        that.clipContent = 0;

            SITE.codePanel({ title: "examples/counter.py", code: SAMPLES.counter, language: "py", width: columnWidth });

            // GROUP: The window and the points
            VGroup({ width: columnWidth, height: "auto", align: "center top", gap: L.mobile ? 20 : 28 });
            that.clipContent = 0;

                SHOTS.window({ name: "counter", title: "Counter", alt: T.codeShotAlt, width: Math.min(400, columnWidth) });

                T.codePoints.forEach(function (point) {
                    CodeSection.point(point.title, TEXTS.fill(point.text), columnWidth);
                });

            endGroup();

        endGroup();

    SITE.endSection();

};

// GROUP: A point: a check, its title and its text
CodeSection.point = function (title, text, width, dark = 0) {

    HGroup({ width: width, height: "auto", align: "left top", gap: 12 });

        SITE.icon("check", SITE.RUN, 18, 2.6);

        VGroup({ width: width - 30, height: "auto", align: "left top", gap: 4 });
            SITE.h3(title, dark);
            that.fontSize = 17;
            SITE.text(text, "100%", dark, 15);
        endGroup();

    endGroup();

};
