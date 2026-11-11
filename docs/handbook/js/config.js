/* Bismillah */

/*

OzdenUI Handbook Website - Config - v26.11 (2026-11-09; from 03-webpages/webpage-handbook, v26.09)

The settings of the handbook page in one place. Texts: js/texts.js.
The chapters are the Markdown files of the handbook of the package (ozdenui-python/handbook), copied into english/ and
turkce/ by tools/update-handbook.sh of the site. The page reads them with fetch: open it with a web server.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const CONFIG = {

    // *** BRAND:
    brandName: "OzdenUI",
    version: "0.1.0", // the version of the package (js/config.js of the page of the package has it too)

    // *** PATHS:
    // The root of the site (the page of the package) from the address of this page: it is always <site>/handbook/.
    // WHY from the address and not a parent path written here: _make-standalone.sh lists a path that leaves the folder
    //     in the code; this one is read from the address, so nothing is listed and the logo comes from the site.
    siteRootURL: new URL(".", location.href).href.replace(/handbook\/$/, ""),
    logoFile: "", // written below: the logo of OzdenUI FOR PYTHON in assets/ of the site (362 x 130, its version for a light ground)
    // The chapters (Markdown), relative to this page; a folder for each language
    handbookPath: "./",
    languageFolders: {
        en: "english",
        tr: "turkce",
    },

    // *** CHAPTERS: (the order of the menu; group: js/texts.js -> groups; title: the name in the menu, else the title of the file)
    chapters: [
        { id: "start", file: "README.md", group: "start", title: { en: "Introduction", tr: "Giriş" } },
        { id: "first-window", file: "01-first-window.md", group: "basics" },
        { id: "objects", file: "02-objects.md", group: "basics" },
        { id: "layout", file: "03-layout.md", group: "basics" },
        { id: "events-and-time", file: "04-events-and-time.md", group: "basics" },
        { id: "components", file: "05-components.md", group: "components" },
        { id: "dialogs-and-files", file: "06-dialogs-and-files.md", group: "components" },
        { id: "looks", file: "07-looks.md", group: "components" },
        { id: "data-and-pictures", file: "08-data-and-pictures.md", group: "components" },
        { id: "your-own-component", file: "09-your-own-component.md", group: "more" },
        { id: "going-further", file: "10-going-further.md", group: "more" },
    ],

    // *** LINKS:
    githubURL: "https://github.com/bug7a/ozdenui-python", // the repository of the package ("": not opened yet, the button is hidden; _make-repo.sh writes it)
    basicjsURL: "https://bug7a.github.io/basic.js/",
    componentsURL: "https://bug7a.github.io/js-components/",

    // *** LOADING:
    loadConcurrency: 4, // chapters read at the same time

    // *** LAYOUT:
    sidebarWidth: 280,
    headerHeight: 60,
    articleMaxWidth: 780,
    tocWidth: 220,
    drawerBreakpoint: 960, // under it the chapter list is a drawer opened with the menu button
    tocBreakpoint: 1280, // over it the "On this page" list is shown on the right

    // *** LANGUAGE:
    defaultLanguage: "en", // "tr", "en"
    languageStorageKey: "bjspy_lang", // WHY the key of the page of the package: a language chosen on either page holds on both

    // *** SEO:
    // The published address of this page. "": not known yet (no canonical / hreflang / og:url until then).
    // _make-repo.sh --with-site writes it: the address of the site + "handbook/".
    siteURL: "https://bug7a.github.io/ozdenui-python/handbook/",
    ogImage: "assets/og-image.jpg", // the link preview picture: the one of the page of the package (the root of the site)

    // *** BEHAVIOR:
    resizeDelay: 120,

};

CONFIG.logoFile = CONFIG.siteRootURL + "assets/ozdenui-python.svg";
