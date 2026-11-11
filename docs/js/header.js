/* Bismillah */

/*

SiteHeader - v26.11 (OzdenUI Website, 2026-11-04; from the site of basic.js, v26.09)

- Sayfanın üstünde sabit duran koyu menü çubuğu. (Kaydırılan kutunun dışındadır.)
- Geniş ekranda bölüm bağlantıları görünür; dar ekranda menü düğmesi bir açılır liste açar.
- Kaydırınca altına ince bir çizgi gelir.
- The logo of OzdenUI (the paper boat, "OzdenUI", "FOR PYTHON"); the Handbook button (the handbook page of the site, in the language of
  the page); the GitHub button only when CONFIG.githubURL is given (on a phone they are items of the menu).
- 2026-11-05 (the user, as in the site of the Tauri template): with the GitHub button the bar was 375 px wide on a
  phone, so the menu button was cut even on a 390 px screen.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const LOGO_HEIGHT = 76;             // px: the logo in the bar (68 px high): the top of the juniper is out of the window
const LOGO_HEIGHT_MOBILE = 62;      // (a 60 px bar)
const LOGO_WORDS_MIDDLE = 70 / 130; // the middle of "OzdenUI" in the drawing, from its top (measured)

// Default values:
const SiteHeaderDefaults = {
    onNavClick: function (key) { },
    onLanguageClick: function () { },
};

const SiteHeader = function (params = {}) {

    mergeIntoIfMissing(params, SiteHeaderDefaults);

    const L = SITE.L;
    const T = SITE.T;
    const showNav = (L.w >= 1100) ? 1 : 0;
    const navKeys = CONFIG.navKeys;

    // BOX: Component container
    let box = startObject({
        left: 0,
        top: 0,
        width: "100%",
        height: L.headerH,
        color: SITE.HEADER,
    });
    box.elem.style.zIndex = "50";
    box.elem.style.backdropFilter = "blur(10px)";
    box.elem.style.borderBottom = "1px solid transparent";
    box.setMotion("border-color 0.25s");
    box.clipContent = 0;

    // *** PRIVATE VARIABLES:
    let menuBox = null;

    // *** PRIVATE FUNCTIONS:

    const openGithub = function () {
        window.open(CONFIG.githubURL, "_blank", "noopener");
    };

    const closeMenu = function () {
        if (menuBox) {
            menuBox.remove();
            menuBox = null;
        }
    };

    const openMenu = function () {

        closeMenu();

        // GROUP: Açılır menü (üst çubuğun altında)
        createIn(page, function () {

            menuBox = VGroup({
                left: 0,
                top: L.headerH,
                width: "100%",
                height: "auto",
                align: "left top",
                gap: 2,
                padding: [L.gutter - 12, 12],
                color: SITE.HEADER_MENU,
            });
            menuBox.position = "absolute";
            menuBox.elem.style.zIndex = "49";
            menuBox.elem.style.borderBottom = "1px solid " + SITE.ON_DARK_LINE;

                const addItem = function (text, onClick) {
                    const item = HGroup({ width: "100%", height: 48, align: "left center", padding: [12, 0], round: 8, color: "transparent" });
                    item.elem.style.cursor = "pointer";
                        SITE.label(text, { fontSize: 16, textColor: SITE.ON_DARK });
                    endGroup();
                    item.on("mouseenter", function () { item.color = "rgba(255, 255, 255, 0.06)"; });
                    item.on("mouseleave", function () { item.color = "transparent"; });
                    item.on("click", function () { closeMenu(); onClick(); });
                };

                navKeys.forEach(function (key) {
                    addItem(T.nav[key], function () { params.onNavClick(key); });
                });

                addItem(T.navBasicJs, function () { location.href = CONFIG.basicjsURL; });
                addItem(T.navHandbook, function () { location.href = SiteApp.handbookAddress(); });
                if (CONFIG.githubURL && L.mobile) addItem("GitHub", openGithub);

            endGroup();

        });

    };

    // *** PUBLIC FUNCTIONS:

    box.refreshScrollState = function (scrollTop) {
        box.elem.style.borderBottomColor = (scrollTop > 8) ? SITE.ON_DARK_LINE : "transparent";
    };

    box.closeMenu = closeMenu;

    // WHY: box.superRemove is overwritten by a component that extends this one, so the local copy is called below.
    const superRemove = box.remove;
    box.superRemove = superRemove;
    box.remove = function () {
        if (!box) return;
        closeMenu(); // NOTE: The menu is created on page, remove() of the header does not reach it.
        superRemove.call(box);
        box = null;
    };

    // *** OBJECT VIEW:

    // GROUP: Ortalanmış içerik
    HGroup({ width: "100%", height: "100%", align: "center center", padding: [L.gutter, 0] });
    that.clipContent = 0;

        HGroup({ width: L.content, height: "100%", align: "left center", gap: L.mobile ? 6 : 10 });
        that.clipContent = 0;

            // GROUP: Logo
            // WHY larger than the bar: the words of the logo were small; they stand beside the links (a little higher than
            //     the middle of the drawing), and the top of the juniper goes out of the window
            const logoHeight = L.mobile ? LOGO_HEIGHT_MOBILE : LOGO_HEIGHT;
            const brand = HGroup({ width: "auto", height: "auto", align: "left center", gap: 10 });
            brand.elem.style.cursor = "pointer";
            brand.elem.style.flexShrink = "0";
            brand.elem.style.transform = "translateY(-" + Math.round(logoHeight * (LOGO_WORDS_MIDDLE - 0.5)) + "px)";

                SITE.logo(logoHeight);

            endGroup();

            brand.on("click", function () { params.onNavClick("top"); });

            SITE.spacer();

            // Bölüm bağlantıları (geniş ekran)
            if (showNav) {

                navKeys.forEach(function (key) {
                    const link = SITE.label(T.nav[key], { fontSize: 14, textColor: SITE.ON_DARK_SOFT });
                    link.elem.style.cursor = "pointer";
                    link.elem.style.padding = "8px 10px";
                    link.setMotion("color 0.15s");
                    link.on("mouseenter", function () { link.textColor = "#FFFFFF"; });
                    link.on("mouseleave", function () { link.textColor = SITE.ON_DARK_SOFT; });
                    link.on("click", function () { params.onNavClick(key); });
                });

                SITE.spacer();

            }

            if (!L.mobile) {
                SITE.button({
                    text: T.navHandbook,
                    icon: "book",
                    kind: "plain-dark",
                    height: 38,
                    fontSize: 14,
                    onClick: function () { location.href = SiteApp.handbookAddress(); },
                });
                SITE.button({
                    text: T.navBasicJs,
                    icon: "code",
                    kind: "plain-dark",
                    height: 38,
                    fontSize: 14,
                    onClick: function () { location.href = CONFIG.basicjsURL; },
                });
            }

            // WHY !L.mobile: a phone has no room for it in the bar (the menu has it)
            if (CONFIG.githubURL && !L.mobile) {
                SITE.button({
                    icon: "github",
                    kind: "plain-dark",
                    height: 38,
                    fontSize: 15,
                    hint: "GitHub",
                    onClick: openGithub,
                });
            }

            SITE.button({
                text: T.languageButton,
                kind: "ghost-dark",
                height: 36,
                fontSize: 12,
                hint: T.languageHint,
                onClick: params.onLanguageClick,
            });

            if (!showNav) {
                SITE.button({
                    icon: "menu",
                    kind: "plain-dark",
                    height: 38,
                    fontSize: 16,
                    hint: T.menu,
                    onClick: function () { if (menuBox) closeMenu(); else openMenu(); },
                });
            }

        endGroup();

    endGroup();

    return endObject(box);

};
