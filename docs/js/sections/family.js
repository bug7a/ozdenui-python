/* Bismillah */

/*

OzdenUI Website - Family - v26.11

The strip over the footer: the logos of the family of OzdenUI side by side (the components, Python, Go, Ruby), each a
link to its site. The logo of this site is shown too, as the page it is (not a link). CONFIG.familySelf names it.
WHY not in the footer: its links stood in one line there and left little room for its words.

Started Date: November 2026
Webpage: https://bug7a.github.io/js-components/

Copyright 2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const FamilySection = function () {

    const L = SITE.L;

    const strip = SITE.startSection({ key: "family", align: "center top", gap: 0, padY: L.mobile ? 28 : 40 });
    strip.elem.style.borderTop = "1px solid " + SITE.LINE;

        // GROUP: The logos (on a phone two in a line)
        HGroup({ width: "100%", height: "auto", align: "center center", gap: L.mobile ? [28, 22] : 56, wrap: 1 });
        that.clipContent = 0;
            FamilySection.MEMBERS.forEach(function (member) {
                FamilySection.logo(member, L.mobile ? FamilySection.PHONE_HEIGHT : FamilySection.HEIGHT);
            });
        endGroup();

    SITE.endSection();

};

FamilySection.HEIGHT = 46;
FamilySection.PHONE_HEIGHT = 38;
FamilySection.FADED = 0.72; // the other logos are a little softer until the mouse is on them

// The width and the height are the viewBox of each drawing, so the logos have their own shape at one height
FamilySection.MEMBERS = [
    { key: "components", name: "OzdenUI Components", file: "assets/family/ozdenui-components.svg", width: 360, height: 130, url: "https://bug7a.github.io/js-components/" },
    { key: "python", name: "OzdenUI for Python", file: "assets/family/ozdenui-python.svg", width: 380, height: 130, url: "https://bug7a.github.io/ozdenui-python/" },
    { key: "go", name: "OzdenUI for Go", file: "assets/family/ozdenui-go.svg", width: 342, height: 132, url: "https://bug7a.github.io/ozdenui-go/" },
    { key: "ruby", name: "OzdenUI for Ruby", file: "assets/family/ozdenui-ruby.svg", width: 364, height: 130, url: "https://bug7a.github.io/ozdenui-ruby/" },
];

// ICON: One logo; a link to its site in a new tab, but the logo of this site
FamilySection.logo = function (member, height) {

    const isSelf = (member.key == CONFIG.familySelf);
    const logo = Icon({ width: Math.round(height * member.width / member.height), height: height, color: "transparent" });
    logo.load(member.file);
    logo.elem.title = member.name;
    logo.elem.style.flexShrink = "0";

    if (isSelf) {
        logo.aria = { label: member.name, current: "page" };
        return logo;
    }

    logo.role = "link";
    logo.aria = { label: member.name };
    logo.tabIndex = 0;
    logo.elem.style.cursor = "pointer";
    logo.opacity = FamilySection.FADED;
    logo.setMotion("opacity 0.2s");

    const open = function () { window.open(member.url, "_blank", "noopener"); };

    logo.on("mouseenter", function () { logo.opacity = 1; });
    logo.on("mouseleave", function () { logo.opacity = FamilySection.FADED; });
    logo.on("click", open);
    logo.on("keydown", function (self, event) {
        if (event.key == "Enter") open();
    });
    logo.setFocusRing();

    return logo;

};
