/* Bismillah */

/*

OzdenUI Website - Why - v26.11 (2026-11-04)

Four reasons, in cards.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const WhySection = function () {

    const L = SITE.L;
    const T = SITE.T;

    SITE.startSection({ key: "why", color: SITE.BG_SOFT });

        SITE.sectionIntro(T.whyEyebrow, T.whyTitle);

        SITE.startGrid();

            T.why.forEach(function (item) {
                SITE.startCard({ width: L.columns(4), gap: 14 });
                    SITE.iconBadge(item.icon);
                    SITE.h3(item.title);
                    SITE.text(TEXTS.fill(item.text), "100%", 0, 15);
                SITE.endCard();
            });

        SITE.endGrid();

    SITE.endSection();

};
