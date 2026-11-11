/* Bismillah */

/*

OzdenUI Website - Dialogs - v26.11 (2026-11-04)

A dialog returns its answer like a function: the text, the points and the code next to a window with an open dialog.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const DialogsSection = function () {

    const L = SITE.L;
    const T = SITE.T;
    const columnWidth = L.stacked ? L.content : L.columns(2);
    const SHOT_MAX_WIDTH = 640;

    SITE.startSection({ key: "dialogs", dark: 1 });

        HGroup({ width: "100%", height: "auto", align: "center center", gap: L.gap, wrap: 1 }); // WHY L.gap: two columns(2) and one L.gap fill the content
        that.clipContent = 0;

            // GROUP: The words and the code
            VGroup({ width: columnWidth, height: "auto", align: "left top", gap: 16 });
            that.clipContent = 0;

                SITE.eyebrow(T.dialogsEyebrow, 1);
                SITE.h2(T.dialogsTitle, 1, 0);
                SITE.lead(T.dialogsLead, "100%", 1, 0);

                T.dialogsPoints.forEach(function (point) {
                    HGroup({ width: "100%", height: "auto", align: "left center", gap: 10 });
                        SITE.icon("check", SITE.ACCENT_ON_DARK, 16, 2.6);
                        SITE.label(point, { fontSize: 15, textColor: SITE.ON_DARK_SOFT });
                        that.elem.style.whiteSpace = "normal";
                    endGroup();
                });

                SITE.codePanel({ title: "dialogs.py", code: SAMPLES.dialogs, language: "py", width: columnWidth });

            endGroup();

            SHOTS.window({ name: "dialogs-open", title: "examples/dialogs.py", alt: T.dialogsShotAlt, width: Math.min(SHOT_MAX_WIDTH, columnWidth) });

        endGroup();

    SITE.endSection();

};
