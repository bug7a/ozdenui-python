/* Bismillah */

/*

OzdenUI Website - Config - v26.11 (2026-11-04)

The values of the site in one place: the brand, the links, the facts and the state of the package.
The site is the sister of 03-webpages/webpage-basicjs (the same theme, header and build).

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
    logoFile: "assets/ozdenui-python-dark.svg", // the logo of OzdenUI FOR PYTHON (362 x 130), its version for the dark bar

    // *** PATHS: (relative to this page)
    rootPath: "./",
    imagesPath: "images/",

    // *** THE PACKAGE:
    packageName: "ozdenui",
    version: "0.1.0",
    // false until the package is on PyPI: the page says to install from the source (no "pip install" that fails)
    isOnPypi: true,
    pypiURL: "https://pypi.org/project/ozdenui/",
    githubURL: "https://github.com/bug7a/ozdenui-python", // the repository of the Python package ("": not opened yet, the GitHub button is hidden)
    pythonVersion: "3.9",

    // *** LINKS:
    basicjsURL: "https://bug7a.github.io/basic.js/", // the site of basic.js
    handbookURL: "handbook/", // the handbook of the package: a page of this site (handbook/index.htm); its language follows the page
    componentsURL: "https://bug7a.github.io/js-components/",
    pywebviewURL: "https://pywebview.flowrl.com/",
    authorURL: "https://bug7a.github.io/",

    // *** FACTS: (measured on a Mac, 2026-11-03; ozdenui-python/plan.md)
    // WHY \u00A0: a number and its unit stay on one line
    componentClasses: 53,
    componentCount: 88,
    installSize: "12\u00A0MB",
    clickTime: "3\u00A0ms",
    showTime: "0.5\u00A0s",
    license: "Apache 2.0",

    // *** THE SECTIONS OF THE HEADER:
    navKeys: ["code", "why", "components", "examples", "start"],

    // *** LANGUAGE:
    defaultLanguage: "en", // "tr", "en"
    languageStorageKey: "bjspy_lang",

    // *** SEO:
    // The published address of this page. "": not known yet (no canonical / hreflang / og:url until then).
    siteURL: "https://bug7a.github.io/ozdenui-python/",
    ogImage: "assets/og-image.jpg", // the link preview: the first screen of the page at 1200 x 630 (test/screenshot.js --og)

    // *** BEHAVIOR:
    rebuildOnResizeDelay: 180, // ms: the page is built again when the width changes

};
