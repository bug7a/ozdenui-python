/* Bismillah */

/*

OzdenUI Website - Footer - v26.11 (2026-11-04)

The dark end of the page: the logo, one line about the library, the links and the license.
GitHub and PyPI are shown only when they exist (CONFIG.githubURL, CONFIG.isOnPypi).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const FooterSection = function () {

    const L = SITE.L;
    const T = SITE.T;

    SITE.startSection({ key: "footer", dark: 1, gap: 0, padY: L.mobile ? 44 : 64 });

        // GROUP: The logo, the words and the links
        HGroup({ width: "100%", height: "auto", align: "left center", gap: 16, wrap: 1 });

            FooterSection.brand();

            SITE.text(TEXTS.fill(T.footerText) + " " + T.footerMade, "auto", 1, 13);
            that.elem.style.flex = "1 1 280px";

            // GROUP: The links
            HGroup({ width: "auto", height: "auto", align: "left center", gap: 18, wrap: 1 });
            that.elem.style.maxWidth = "100%"; // WHY: on a phone the links go on to a second line (they left the screen)
                FooterSection.links().forEach(function (item) {
                    FooterSection.link(item.text, item.url, 14, item.sameTab);
                });
            endGroup();

        endGroup();

        // GROUP: The copyright and the author
        HGroup({ width: "auto", height: "auto", align: "left center", gap: 4 });
        that.elem.style.marginTop = "18px";
            // WHY 2020: the years of basic.js and its components (the license of the package says 2020-2026 too)
            SITE.label("© 2020–" + new Date().getFullYear(), { fontSize: 12, textColor: SITE.ON_DARK_FAINT });
            const author = FooterSection.link("Buğra Özden", CONFIG.authorURL, 12);
            author.elem.style.textDecoration = "underline";
        endGroup();

    SITE.endSection();

};

// GROUP: The logo of OzdenUI
FooterSection.brand = function () {

    const brand = HGroup({ width: "auto", height: "auto", align: "left center", gap: 10 });

        SITE.logo(46);

    endGroup();

    return brand;

};

// The links: the ones that do not exist yet are left out
FooterSection.links = function () {

    const T = SITE.T;
    const links = [
        { text: T.navBasicJs, url: CONFIG.basicjsURL },
        { text: T.navHandbook, url: SiteApp.handbookAddress(), sameTab: 1 },
        { text: T.navComponents, url: CONFIG.componentsURL },
        { text: "pywebview", url: CONFIG.pywebviewURL },
    ];

    if (CONFIG.githubURL) links.push({ text: "GitHub", url: CONFIG.githubURL });
    if (CONFIG.isOnPypi) links.push({ text: "PyPI", url: CONFIG.pypiURL });

    return links;

};

// LABEL: A link on the dark ground (it opens in a new tab; sameTab: a page of this site)
FooterSection.link = function (text, url, fontSize, sameTab = 0) {

    const link = SITE.label(text, { fontSize: fontSize, textColor: SITE.ON_DARK_SOFT });
    link.role = "link";
    link.tabIndex = 0;
    link.elem.style.cursor = "pointer";

    const open = function () {
        if (sameTab) location.href = url;
        else window.open(url, "_blank", "noopener");
    };

    link.on("mouseenter", function () { link.textColor = "#FFFFFF"; });
    link.on("mouseleave", function () { link.textColor = SITE.ON_DARK_SOFT; });
    link.on("click", open);
    link.on("keydown", function (self, event) {
        if (event.key == "Enter") open();
    });

    return link;

};
