/* Bismillah */

/*

OzdenUI Website - Where it fits - v26.11 (2026-11-04)

An honest place for the library: what it is good for, and what other tools are better for.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const FitSection = function () {

    const L = SITE.L;
    const T = SITE.T;

    SITE.startSection({ key: "fit" });

        SITE.sectionIntro(T.fitEyebrow, T.fitTitle);

        SITE.startGrid();
            FitSection.card(T.fitGoodTitle, T.fitGood, "check", SITE.RUN);
            FitSection.card(T.fitOtherTitle, T.fitOther, "arrow", SITE.TEXT_SOFT);
        SITE.endGrid();

        SITE.text(T.fitNote, Math.min(700, L.content), 0, 15);
        that.elem.style.textAlign = "center";
        that.elem.style.alignSelf = "center";
        that.elem.style.marginTop = (L.mobile ? 4 : 10) + "px";

    SITE.endSection();

};

// GROUP: A card with a title and a list (an icon before each line)
FitSection.card = function (title, lines, iconName, iconColor) {

    const L = SITE.L;
    const width = L.columns(2);
    const ICON_SIZE = 17;
    const ICON_TOP = 4; // (a line of 15 px text is about 25 px high)

    SITE.startCard({ width: width, gap: 14, hover: 0 });

        SITE.h3(title);

        lines.forEach(function (line) {
            HGroup({ width: "100%", height: "auto", align: "left top", gap: 10 });
                SITE.icon(iconName, iconColor, ICON_SIZE, 2.4);
                that.elem.style.marginTop = ICON_TOP + "px"; // WHY: in the middle of the first line of the text
                SITE.text(line, "auto", 0, 15);
                that.elem.style.flex = "1 1 0";
                that.elem.style.minWidth = "0";
            endGroup();
        });

    SITE.endCard();

};
