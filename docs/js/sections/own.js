/* Bismillah */

/*

OzdenUI Website - Your own component - v26.11 (2026-11-04)

A component of your own in plain Python: the code of a Card class next to its window (after a click on its button)
and three points. The code is the README's and tools/shot_card.py's (images/card.webp).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const OwnSection = function () {

    const L = SITE.L;
    const T = SITE.T;
    const columnWidth = L.stacked ? L.content : L.columns(2);

    SITE.startSection({ key: "own", color: SITE.BG_SOFT });

        SITE.sectionIntro(T.ownEyebrow, T.ownTitle, T.ownLead);

        // GROUP: The code and its window (one under the other on a phone and a tablet)
        HGroup({ width: "100%", height: "auto", align: "center top", gap: L.gap, wrap: 1 });
        that.clipContent = 0;

            SITE.codePanel({ title: "card.py", code: SAMPLES.own, language: "py", width: columnWidth });

            // GROUP: The window and the points
            VGroup({ width: columnWidth, height: "auto", align: "center top", gap: L.mobile ? 20 : 28 });
            that.clipContent = 0;

                SHOTS.window({ name: "card", title: "Cards", alt: T.ownShotAlt, width: columnWidth });

                T.ownPoints.forEach(function (point) {
                    CodeSection.point(point.title, point.text, columnWidth);
                });

            endGroup();

        endGroup();

    SITE.endSection();

};
