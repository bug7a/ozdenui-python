/* Bismillah */

/*

OzdenUI Website - Examples - v26.11 (2026-11-04)

The examples of the source: the picture of the window, its name, one line, its file.
On a wide screen the rows hold three cards each. What does not fill them goes in rows of two, at the top and at the end: no card is alone.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const ExamplesSection = function () {

    const T = SITE.T;

    SITE.startSection({ key: "examples", color: SITE.BG_SOFT });

        SITE.sectionIntro(T.examplesEyebrow, T.examplesTitle, T.examplesLead);

        SITE.startGrid();
            T.examples.forEach(function (example, index) {
                ExamplesSection.card(example, ExamplesSection.isWide(index, T.examples.length));
            });
        SITE.endGrid();

    SITE.endSection();

};

ExamplesSection.ROW_COUNT = 3; // the cards of a row
ExamplesSection.WIDE_ROW_COUNT = 2; // the cards of a wide row
ExamplesSection.WIDE_CARDS_BY_REST = [0, 4, 2]; // by what is left over rows of three: how many cards go in wide rows
ExamplesSection.PICTURE_RATIO = 0.62; // the height of the picture area to its width
ExamplesSection.PICTURE_PADDING = 18;
ExamplesSection.PICTURE_GROUND = "#E4E6EA"; // cool, as the pages of the windows

ExamplesSection.isWide = function (index, count) {
    const wideCards = ExamplesSection.WIDE_CARDS_BY_REST[count % ExamplesSection.ROW_COUNT];
    const wideAtTop = Math.min(wideCards, ExamplesSection.WIDE_ROW_COUNT);
    const wideAtEnd = wideCards - wideAtTop;
    return (index < wideAtTop || index >= count - wideAtEnd) ? 1 : 0;
};

// GROUP: The card of an example
ExamplesSection.card = function (example, wide) {

    const L = SITE.L;
    const width = wide ? L.columns(2) : L.columns(3);
    const innerWidth = width - 2; // WHY: the border of the card (1 px on each side)
    const pictureHeight = Math.round(innerWidth * ExamplesSection.PICTURE_RATIO);
    const pad = ExamplesSection.PICTURE_PADDING;

    SITE.startCard({ width: width, gap: 0, padding: 0 });

        // GROUP: The picture, whole, on a calm ground (the windows have other ratios)
        VGroup({ width: innerWidth, height: pictureHeight, align: "center center", color: ExamplesSection.PICTURE_GROUND });
        that.clipContent = 0;
        that.elem.style.flexShrink = "0";
            SHOTS.thumbnail(example.image, example.title, innerWidth - pad * 2, pictureHeight - pad * 2);
        endGroup();

        // GROUP: The words
        VGroup({ width: "100%", height: "auto", align: "left top", gap: 8, padding: L.mobile ? 18 : 22 });
            SITE.h3(example.title);
            SITE.text(example.text, "100%", 0, 14);
            const file = SITE.chip("examples/" + example.key + ".py", { mono: 1, fontSize: 12, color: "rgba(0, 0, 0, 0.05)", textColor: SITE.TEXT_SOFT });
            file.elem.style.marginTop = "4px";
        endGroup();

    SITE.endCard();

};
