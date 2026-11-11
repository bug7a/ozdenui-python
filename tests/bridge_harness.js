/* Bismillah */

/*

bridge_harness.js - ozdenui v0.1 (OzdenUI: basic.js for Python)
bridge.js in Node, for tests/test_bridge.py: a small fake of basic.js and of pywebview around it. It runs the code of a
test (the body of a function, from stdin) on that page and prints what it returns as JSON.
Usage: echo 'return __bp.apply([]);' | node tests/bridge_harness.js ozdenui/web/bridge.js

The fake page: a maker (Box, Label..., and Thing, a component of the tests) keeps the props it was given in obj.given;
obj.remove() takes it off the page (obj.elem.isConnected is false); every call of window.pywebview.api.emit() is kept
in emitted, as [number, target id, event name, data].

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

const fs = require("fs");
const vm = require("vm");

const BRIDGE_FILE = process.argv[2];
const TEST_CODE = fs.readFileSync(0, "utf8");
const BASIC_MAKERS = ["Box", "Label", "Button", "Input", "Icon", "VGroup", "HGroup"];

class FakeElement {
    constructor() {
        this.isConnected = true;
    }
}

class FakeNode {}

class FakeEvent {}

// A maker of basic.js, Box(left, top, width, height, props), or of a component, Thing(props)
const fakeMaker = function (type) {
    return function (...args) {
        const obj = { type: type, args: args.slice(0, -1), given: Object.assign({}, args[args.length - 1]), handlers: {} };
        obj.elem = new FakeElement();
        obj.props = function (values) { Object.assign(obj.given, values); };
        obj.on = function (eventName, handler) { obj.handlers[eventName] = handler; };
        obj.remove = function () { obj.elem.isConnected = false; };
        return obj;
    };
};

const emitted = [];
const page = fakeMaker("MainBox")({});
page.width = 800;
page.height = 600;

const context = {
    console: { log: function () {}, error: function () {}, warn: function () {} },
    performance: { now: function () { return performance.now(); } },
    Element: FakeElement,
    Node: FakeNode,
    Event: FakeEvent,
    Thing: fakeMaker("Thing"),
    createIn: function (parent, make) { return make(); },
    endGroup: function () {},
    page: page,
    emitted: emitted,
    addEventListener: function () {},
    pywebview: { api: { emit: function (...args) { emitted.push(args); } } },
};
BASIC_MAKERS.forEach(function (name) { context[name] = fakeMaker(name); });
context.window = context; // WHY: on a page window is the global object; bridge.js uses both

vm.createContext(context);
vm.runInContext(fs.readFileSync(BRIDGE_FILE, "utf8"), context, { filename: BRIDGE_FILE });
const result = vm.runInContext("(function () {\n" + TEST_CODE + "\n})()", context, { filename: "test code" });
process.stdout.write(JSON.stringify(result === undefined ? null : result));
