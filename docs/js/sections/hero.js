/* Bismillah */

/*

OzdenUI Website - Hero - v26.11 (2026-11-04)

The title, three buttons (start, the examples, the handbook), the install line, short facts and the picture of the gallery window.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const HeroSection = function (params = {}) {

    mergeIntoIfMissing(params, { onNavClick: function (key) { } });

    const L = SITE.L;
    const T = SITE.T;
    const SHOT_WIDTH = Math.min(980, L.content);

    const strip = SITE.startSection({ key: "top", dark: 1, align: "center top", gap: L.mobile ? 18 : 24 });
    strip.elem.style.paddingTop = (L.headerH + (L.mobile ? 44 : 90)) + "px";
    strip.elem.style.paddingBottom = (L.mobile ? 60 : 100) + "px";
    // A light behind the title: the accent, faint
    strip.elem.style.backgroundImage = "radial-gradient(ellipse 42% 42% at 38% 0%, " + SITE.GLOW_GREEN + ", transparent 70%),"
        + " radial-gradient(ellipse 38% 36% at 64% 0%, " + SITE.GLOW_BLUE + ", transparent 70%)";

        // GROUP: The pill of the version
        HGroup({ width: "auto", height: "auto", align: "left center", gap: 8, padding: [14, 7], color: SITE.ACCENT_ON_DARK_SOFT, round: 100 });
        that.border = 1;
        that.borderColor = SITE.ACCENT_ON_DARK_LINE;

            Box({ width: 7, height: 7, round: 4, color: SITE.ACCENT_ON_DARK });
            SITE.label(TEXTS.fill(T.heroEyebrow), { fontSize: 13, textColor: SITE.ACCENT_ON_DARK });

        endGroup();

        // LABEL: The title
        SITE.h1(T.heroTitle, 1, Math.min(900, L.content));
        that.elem.style.textAlign = "center";

        // LABEL: The lead
        SITE.lead(T.heroLead, Math.min(700, L.content), 1, 1);

        // GROUP: The buttons
        HGroup({ width: "auto", height: "auto", align: "center center", gap: 12, wrap: 1 });
        that.elem.style.marginTop = "8px";

            SITE.button({ text: T.heroPrimary, icon: "arrow", iconRight: 1, kind: "primary", onClick: function () { params.onNavClick("start"); } });
            SITE.button({ text: T.heroSecondary, icon: "grid", kind: "ghost-dark", onClick: function () { params.onNavClick("examples"); } });
            SITE.button({ text: T.readHandbook, icon: "book", kind: "ghost-dark", onClick: function () { location.href = SiteApp.handbookAddress(); } });

        endGroup();

        HeroSection.createInstallLine();

        // GROUP: The facts
        HGroup({ width: "100%", height: "auto", align: "center center", gap: L.mobile ? 12 : 22, wrap: 1 });

            T.heroFacts.forEach(function (fact) {
                HGroup({ width: "auto", height: "auto", align: "left center", gap: 6 });
                    SITE.icon("check", SITE.ACCENT_ON_DARK, 15, 2.6);
                    SITE.label(TEXTS.fill(fact), { fontSize: 14, textColor: SITE.ON_DARK_SOFT });
                endGroup();
            });

        endGroup();

        // GROUP: The windows of six examples, one after the other
        const shot = HeroSection.createSlides(SHOT_WIDTH);
        shot.elem.style.marginTop = (L.mobile ? 20 : 36) + "px";

    SITE.endSection();

};

// The slides of the top: pictures of one size (tools/make_images.py: HERO_SHOTS), so the frame keeps its height
// (file: the key of its page, the name of its dot for a screen reader too)
HeroSection.SLIDES = [
    { file: "gallery-styled.py", picture: "hero-gallery-styled" },
    { file: "minimal_theme.py", picture: "minimal_theme" },
    { file: "charts.py", picture: "hero-charts" },
    { file: "json_editor.py", picture: "hero-json_editor" },
    { file: "photos.py", picture: "hero-photos" },
    { file: "chat.py", picture: "hero-chat-dark" },
];
HeroSection.SLIDE_SECONDS = 5;
HeroSection.MOTION_SECONDS = 0.25;
HeroSection.FRAME_SHADOW = "0px 30px 80px rgba(0, 0, 0, 0.5), 0px 0px 0px 1px rgba(255, 255, 255, 0.08)";
HeroSection.THUMB_SHADOW = "0px 6px 18px rgba(0, 0, 0, 0.45)";
HeroSection.THUMB_OPEN_SHADOW = "0px 0px 0px 4px rgba(66, 115, 173, 0.35), 0px 10px 24px rgba(0, 0, 0, 0.5)";
HeroSection.THUMB_WIDTH = 112;       // px: a small picture under the frame (smaller on a narrow screen)
HeroSection.THUMB_LINE = 3;          // px: its line (the line of the open one is the blue of the logo)
HeroSection.THUMB_ZOOM = 1.12;       // the picture is larger than its box, in its middle: WHY the edges of a window
                                     //     picture (its frame, its scroll bar, its status bar) made the line look uneven
HeroSection.THUMB_LIFT = 4;          // px: the open one stands a little higher
HeroSection.THUMB_OPACITY = 0.45;    // the picture of a small box that is not open (1 under the mouse)
HeroSection.TIME_BAR = 5;            // px: the line that fills in the open small box until the next picture
HeroSection.TIME_TRACK = "rgba(13, 19, 17, 0.62)"; // its ground: the part still to fill (WHY: alone the line was one with the cream border)

// GROUP: The frame of a window whose picture changes by itself, and a row of small pictures under it: a PageControl that
//     slides (a finger can swipe it), with arrows at the sides that go round (after the last, the first). The title of
//     the frame is the file of the picture. (1 group opened and closed)
// WHY arrows, small pictures and a slide: one picture that changes by itself was not seen as more than one.
// WHY the time is a line in the open small box: it shows when the next picture comes; it is the timer too (its end
//     opens the next picture), so it never runs apart from the change. It waits while the mouse is over the slides.
// WHY it stops for good after a choice of the visitor (an arrow, a small picture, a key, a swipe): the picture he chose
//     went away after 5 s (on a phone there is no mouse over it to make it wait).
HeroSection.createSlides = function (width) {

    const L = SITE.L;
    const T = SITE.T;
    const slides = HeroSection.SLIDES;
    const isReducedMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    const gap = L.mobile ? 6 : 10;
    const thumbWidth = Math.min(HeroSection.THUMB_WIDTH, Math.floor((width - gap * (slides.length - 1)) / slides.length * 0.92));
    const thumbHeight = SHOTS.heightAt(slides[0].picture, thumbWidth);
    let thumbs = [];
    let isPlaying = !isReducedMotion;   // WHY: a visitor who asked for less motion changes the pictures himself
    let isWaiting = false;              // the mouse is over the slides
    let isChangeByItself = false;

    HeroSection.addTimeCss();

    // Marks the small box of the open page, and runs its time line (the others have none)
    const paintThumbs = function () {
        thumbs.forEach(function (thumb) {
            const isOpen = (thumb.file === pages.value);
            thumb.borderColor = isOpen ? SITE.ACCENT : SITE.ON_DARK_LINE;
            thumb.elem.style.transform = isOpen ? "translateY(-" + HeroSection.THUMB_LIFT + "px)" : "translateY(0px)";
            thumb.elem.style.boxShadow = isOpen ? HeroSection.THUMB_OPEN_SHADOW : HeroSection.THUMB_SHADOW;
            // WHY the picture and not the box: a box that is not opaque showed what is behind it
            thumb.picture.opacity = (isOpen || thumb.isHover) ? 1 : HeroSection.THUMB_OPACITY;
            thumb.aria = { current: isOpen ? "true" : "false" };
            HeroSection.runTimeBar(thumb, isPlaying && isOpen, isWaiting);
        });
    };

    // The end of the time line: the next picture (after the last, the first)
    const openNextByItself = function () {
        if (!isPlaying) return;
        isChangeByItself = true;
        pages.next();
        isChangeByItself = false;
    };

    // GROUP: The frame and the row of its small pictures
    const box = VGroup({ width: width, height: "auto", align: "center top", gap: L.mobile ? 12 : 18 });
    box.clipContent = 0;
    box.elem.style.flexShrink = "0";

        const frame = VGroup({ width: width, height: "auto", align: "left top", gap: 0, color: SITE.CODE_BG, round: 14 });
        frame.clipContent = 1;
        frame.elem.style.flexShrink = "0";
        frame.elem.style.boxShadow = HeroSection.FRAME_SHADOW;

            const bar = SITE.codeBar("examples/" + slides[0].file, "", "");

            const pages = PageControl({
                width: width,
                height: SHOTS.heightAt(slides[0].picture, width),
                pages: slides.map(function (slide) { return slide.file; }),
                transition: "slide",
                motion: isReducedMotion ? 0 : HeroSection.MOTION_SECONDS,
                loop: 1,
                arrows: 1,
                ariaLabel: T.heroSlidesLabel,
                onChange: function (self) {
                    bar.lblTitle.text = basic.escapeHtml("examples/" + self.value);
                    if (!isChangeByItself) isPlaying = false; // the visitor chose a picture
                    paintThumbs();
                },
                style: {
                    arrows: {
                        size: L.mobile ? 32 : 40,
                        side: L.mobile ? 8 : 14,
                        color: SITE.SLIDE_ARROW,
                        hoverColor: SITE.SLIDE_ARROW_HOVER,
                        iconColor: "#FFFFFF",
                        iconSize: L.mobile ? 16 : 20,
                        shadow: "0 4px 14px rgba(0, 0, 0, 0.35)",
                    },
                },
            });

            slides.forEach(function (slide) {
                pages.startPage(slide.file);
                    SHOTS.picture(slide.picture, T.heroShotAlts[slide.picture], width);
                pages.endPage();
            });

        endGroup();

        // GROUP: The small pictures: every page at a look; a click (or Enter) opens its page
        const row = HGroup({ width: "auto", height: "auto", align: "center center", gap: gap });
        row.clipContent = 0;
        row.elem.style.paddingTop = HeroSection.THUMB_LIFT + "px"; // WHY: the open one stands higher, its line is not cut

            thumbs = slides.map(function (slide) {
                const thumb = HeroSection.createThumb(slide, thumbWidth, thumbHeight, function () { pages.open(slide.file); }, paintThumbs);
                thumb.timeBar.on("animationend", openNextByItself);
                return thumb;
            });

        endGroup();

    endGroup();

    box.on("mouseenter", function () { isWaiting = true; paintThumbs(); });
    box.on("mouseleave", function () { isWaiting = false; paintThumbs(); });

    paintThumbs();

    return box;

};

// The fill of the time line, once per picture (a CSS animation: it stops while the mouse is over the slides)
HeroSection.addTimeCss = function () {
    if (document.getElementById("hero-slide-time-css")) return;
    const style = document.createElement("style");
    style.id = "hero-slide-time-css";
    style.textContent = "@keyframes heroSlideTime { from { transform: scaleX(0); } to { transform: scaleX(1); } }";
    document.head.appendChild(style);
};

// The time line of a small box: it fills while its picture is open and the slides play, it waits under the mouse
HeroSection.runTimeBar = function (thumb, isRunning, isWaiting) {
    const style = thumb.timeBar.elem.style;
    const isRunningNow = (style.animationName === "heroSlideTime");
    thumb.timeTrack.visible = isRunning ? 1 : 0;
    thumb.timeBar.visible = isRunning ? 1 : 0;
    if (!isRunning) {
        style.animation = "none";
        return;
    }
    if (!isRunningNow) style.animation = "heroSlideTime " + HeroSection.SLIDE_SECONDS + "s linear forwards";
    style.animationPlayState = isWaiting ? "paused" : "running";
};

// BOX: A small picture of a page. open(): opens its page; paint(): marks the open one again (the mouse moved)
HeroSection.createThumb = function (slide, width, height, open, paint) {

    const line = HeroSection.THUMB_LINE;
    const thumb = Box({ width: width, height: height, color: SITE.CODE_BG, round: 8, border: line, borderColor: SITE.ON_DARK_LINE });
    thumb.file = slide.file;
    thumb.isHover = 0;
    thumb.clipContent = 1;
    thumb.role = "button";
    thumb.tabIndex = 0;
    thumb.aria = { label: "examples/" + slide.file };
    thumb.elem.style.flexShrink = "0";
    thumb.elem.style.cursor = "pointer";
    thumb.setMotion("border-color 0.15s, transform 0.2s, box-shadow 0.2s");
    thumb.setFocusRing(SITE.ACCENT_ON_DARK); // WHY: the ring of the browser stayed after a click; this one is for the keyboard

    createIn(thumb, function () {
        // WHY a place: in a Box (not a group) an object without a place was put out of the view
        const insideWidth = width - line * 2;
        const insideHeight = height - line * 2;
        const pictureWidth = Math.round(insideWidth * HeroSection.THUMB_ZOOM);
        const pictureHeight = Math.round(insideHeight * HeroSection.THUMB_ZOOM);
        thumb.picture = SHOTS.picture(slide.picture, "", pictureWidth, pictureHeight);
        thumb.picture.left = -Math.round((pictureWidth - insideWidth) / 2);
        thumb.picture.top = -Math.round((pictureHeight - insideHeight) / 2);
        thumb.picture.setMotion("opacity 0.15s");
        // BOX: The time line on its ground, at the bottom of the picture
        const timeTop = height - line * 2 - HeroSection.TIME_BAR;
        thumb.timeTrack = Box({ left: 0, top: timeTop, width: width - line * 2, height: HeroSection.TIME_BAR, color: HeroSection.TIME_TRACK });
        thumb.timeTrack.visible = 0;
        thumb.timeBar = Box({ left: 0, top: timeTop, width: width - line * 2, height: HeroSection.TIME_BAR, color: SITE.ACCENT });
        thumb.timeBar.elem.style.transformOrigin = "left center";
        thumb.timeBar.visible = 0;
    });

    thumb.on("click", open);
    thumb.on("keydown", function (self, event) {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        open();
    });
    thumb.on("mouseenter", function () { thumb.isHover = 1; paint(); });
    thumb.on("mouseleave", function () { thumb.isHover = 0; paint(); });

    return thumb;

};

// GROUP: "pip install ozdenui" with a copy button, or (not on PyPI yet) where to find how to install it
HeroSection.createInstallLine = function () {

    const T = SITE.T;

    const line = HGroup({ width: "auto", height: "auto", align: "left center", gap: 12, padding: [16, 8], color: "rgba(255, 255, 255, 0.06)", round: 10 });
    line.border = 1;
    line.borderColor = SITE.ON_DARK_LINE;

        if (CONFIG.isOnPypi) {
            SITE.label("$", { fontSize: 15, textColor: SITE.ON_DARK_FAINT });
            that.elem.style.fontFamily = SITE.MONO;
            SITE.label(SAMPLES.installPypi, { fontSize: 15, textColor: SITE.ON_DARK });
            that.elem.style.fontFamily = SITE.MONO;
            SITE.button({ icon: "copy", kind: "code", height: 30, fontSize: 13, hint: T.copy, onClick: function () { SITE.copy(SAMPLES.installPypi); } });
        } else {
            SITE.icon("download", SITE.ON_DARK_SOFT, 16);
            SITE.label(T.installSoon, { fontSize: 14, textColor: SITE.ON_DARK_SOFT });
            that.elem.style.whiteSpace = "normal";
        }

    endGroup();

    return line;

};
