/* Bismillah */

/*

OzdenUI Website - Shots - v26.11 (2026-11-04)

A picture of a real window of the library, in a frame: the dark bar of a window (three dots and its title) over
the picture. The pictures are in CONFIG.imagesPath; js/image-sizes.js (IMAGE_SIZES) has their sizes.

USAGE:
SHOTS.window({ name: "counter", title: "examples/counter.py", alt: T.codeShotAlt, width: 480 });
SHOTS.thumbnail("todo", T.examples[5].title, 320, 220);

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const SHOTS = {};

SHOTS.SHADOW = "0px 24px 60px rgba(0, 0, 0, 0.28), 0px 0px 0px 1px rgba(0, 0, 0, 0.06)";
SHOTS.EXTENSION = ".webp"; // lossless, written by tools/make_images.py

// The height of a picture at a width (its own ratio)
SHOTS.heightAt = function (name, width) {
    const size = IMAGE_SIZES[name];
    return Math.round(width * size[1] / size[0]);
};

// ICON: The picture alone. fit: "contain" in an area of another ratio (height given), else its own height.
SHOTS.picture = function (name, alt, width, height = 0) {

    Icon({ width: width, height: height || SHOTS.heightAt(name, width), color: "transparent" });
    // WHY lazy (before the address): the page loaded all its pictures at once, and on a slow network even the first
    //     one waited; a picture far below comes when the reader comes near it
    that.elem.loading = "lazy";
    that.load(CONFIG.imagesPath + name + SHOTS.EXTENSION);
    that.alt = alt;
    that.imageFit = "contain";
    that.elem.style.flexShrink = "0";

    return that;

};

// The largest size of a picture inside an area, with its own ratio: { width, height }
SHOTS.fitSize = function (name, maxWidth, maxHeight) {
    const size = IMAGE_SIZES[name];
    const scale = Math.min(maxWidth / size[0], maxHeight / size[1]);
    return { width: Math.round(size[0] * scale), height: Math.round(size[1] * scale) };
};

// ICON: A small picture of a window (round corners and a soft shadow), as large as it fits in the area
SHOTS.thumbnail = function (name, alt, maxWidth, maxHeight) {

    const size = SHOTS.fitSize(name, maxWidth, maxHeight);

    SHOTS.picture(name, alt, size.width, size.height);
    that.round = 8;
    that.elem.style.boxShadow = "0px 8px 22px rgba(0, 0, 0, 0.14), 0px 0px 0px 1px rgba(0, 0, 0, 0.06)";

    return that;

};

// GROUP: The picture in the frame of a window. (1 group opened and closed)
SHOTS.window = function (params = {}) {

    mergeIntoIfMissing(params, {
        name: "",
        title: "",
        alt: "",
        width: 480,
        shadow: 1,
    });

    const frame = VGroup({ width: params.width, height: "auto", align: "left top", gap: 0, color: SITE.CODE_BG, round: 14 });
    frame.clipContent = 1;
    frame.elem.style.flexShrink = "0";
    if (params.shadow) frame.elem.style.boxShadow = SHOTS.SHADOW;

        SITE.codeBar(params.title, "", "");
        SHOTS.picture(params.name, params.alt, params.width);

    endGroup();

    return frame;

};
