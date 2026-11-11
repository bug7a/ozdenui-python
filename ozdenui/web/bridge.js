/* Bismillah */

/*

bridge.js - ozdenui v0.1 (OzdenUI: basic.js for Python)
The page side of ozdenui: it runs the commands of Python on basic.js.

Python sends a list of commands to __bp.apply(); every command makes, changes or removes a basic.js object.
The events of the objects and the callbacks of the components go back to Python with window.pywebview.api.emit().

Commands:
  { op: "create", id, type: "Box" | a component ("CheckBox"), args: [left, top, width, height], props: {...},
    parent: id or "page", state: ["value"], src: "app.py:12" }
  { op: "set", id, props: {...} }
  { op: "call", id, method, args: [...], refresh: 1 }   refresh: the state goes back to Python after the call
  { op: "static", target: "Toast", method: "show", args: [...], answer: callback id (for a Promise), keep: id (what it
    returned becomes an object of Python: a bubble) }
  { op: "part", id, of: id, path: ["panels", 0] }    a box inside a component, to put objects into
  { op: "placeBubble", id, target: id, side: "top" }  a popover is placed again when its objects are in it
  { op: "listen", id, event: "click" }
  { op: "remove", id }

Values from Python: { __bpCallback: id } becomes a function that tells Python (wholeArgs: [1]: the values at these places
are JSON data that goes whole, as { __bpJson: text }); { __bpObject: id } the object;
{ __bpNoop: 1 } an empty function; { __bpFormat: { prefix, suffix, thousands, decimals, percent } } a function that gives
the text of a number at once (the answer of a Python function comes too late for a page that draws).

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

*/

"use strict";

window.__bp = (function () {

    // *** PRIVATE VARIABLES:
    const MAKERS = { Box: Box, Label: Label, Button: Button, Input: Input, Icon: Icon, VGroup: VGroup, HGroup: HGroup };
    const GROUP_TYPES = ["VGroup", "HGroup", "GridGroup", "ScrollArea"]; // ScrollArea leaves its content started
    const PAGE_ID = "page";
    const MAX_VALUE_DEPTH = 64; // only a guard: a value that holds itself is cut by toJson() where it comes again
    const MAX_FRACTION_DIGITS = 20;
    const SWEEP_INTERVAL_MS = 1000; // at most this often apply() looks for the objects the page removed itself
    const GLOBAL_NAME = /^[A-Za-z_$][A-Za-z0-9_$]*$/;
    const objects = new Map(); // id -> basic.js object
    let eventNumber = 0;
    let lastSweepAt = 0;
    let isBasicReady = false;
    let isPythonTold = false;
    const earlyMessages = []; // the messages of the page before Python was ready

    // *** PRIVATE FUNCTIONS:

    const objectOf = function (id) {
        if (id === PAGE_ID) return page;
        const obj = objects.get(id);
        if (!obj) throw new Error("There is no object " + id + " (removed?)");
        return obj;
    };

    const isBasicObject = function (value) {
        return !!(value && value.elem instanceof Element);
    };

    // A function or object of the page by its name: a basic.js object maker or a component (CheckBox, Toast).
    // WHY Function(): the components are top-level "const" (const CheckBox = function...), so they are not on
    //      window; the name is checked first, so only a name can go in.
    const resolveGlobal = function (name) {
        if (MAKERS[name]) return MAKERS[name];
        if (!GLOBAL_NAME.test(name)) return undefined;
        return Function("return (typeof " + name + " !== \"undefined\") ? " + name + " : undefined;")();
    };

    // A value of the page as it goes to Python (JSON): an object of basic.js becomes its id. ancestors: the objects
    // the value is inside of; one of them again (an object of a component that holds another one that holds it) is null.
    // WHY not a small depth: it cut the data of the program too, without a word: data.owner.address of an item of an
    //      ItemList, a node of a TreeView or a row came to Python as None.
    const toJson = function (value, depth = 0, ancestors = []) {
        if (value === null || value === undefined) return null;
        if (typeof value === "function") return null;
        if (typeof value !== "object") return value;
        if (isBasicObject(value)) return objectToJson(value, depth, ancestors);
        if (value instanceof Date) return value.toISOString();
        if (value instanceof Node || value instanceof Event) return null;
        if (depth >= MAX_VALUE_DEPTH || ancestors.includes(value)) return null;
        const inside = ancestors.concat([value]);
        if (Array.isArray(value)) {
            return value.map(function (item) { return toJson(item, depth + 1, inside); });
        }
        const json = {};
        Object.keys(value).forEach(function (key) {
            json[key] = toJson(value[key], depth + 1, inside);
        });
        return json;
    };

    // A basic.js object: its id. WHY id and data: a part of a component (a row of a list) has no id of
    // Python, but its own id and data say which one it is.
    const objectToJson = function (obj, depth, ancestors) {
        if (obj.__bpId) return { __bpObject: obj.__bpId };
        const json = { __bpObject: null };
        if (obj.id !== undefined && obj.id !== "" && typeof obj.id !== "object") json.id = obj.id;
        if (obj.data !== undefined) json.data = toJson(obj.data, depth + 1, ancestors);
        return json;
    };

    // "checked" reads a property, "getSelectedKeys()" calls a method.
    const readAccessor = function (obj, accessor) {
        if (!accessor.endsWith("()")) return obj[accessor];
        const method = obj[accessor.slice(0, -2)];
        return (typeof method === "function") ? method.call(obj) : undefined;
    };

    // The values Python keeps: the state of a component ({ checked: "checked", selectedKeys: "getSelectedKeys()" })
    const stateOf = function (obj) {
        const spec = obj && obj.__bpState;
        if (!spec) return null;
        const keys = Object.keys(spec);
        if (!keys.length) return null;
        const state = {};
        keys.forEach(function (key) {
            state[key] = toJson(readAccessor(obj, spec[key]));
        });
        return state;
    };

    const send = function (targetId, eventName, data) {
        // WHY the number: pywebview runs every call from the page on a thread of its own, so the calls can reach
        //      Python in another order. Python puts them back in this order.
        eventNumber += 1;
        const sent = window.pywebview.api.emit(eventNumber, targetId, eventName, data);
        // WHY catch: a failed call must not become an "unhandledrejection" message that is sent again and again
        if (sent && sent.catch) sent.catch(function () {});
    };

    // The values of a callback as they go to Python. The places of wholeArgs are JSON data that goes whole, as a JSON text.
    // WHY: the value of a JsonEditor may be any JSON, also deeper than MAX_VALUE_DEPTH, and a big one: JSON.stringify
    //      writes it exactly, faster than toJson() walks it.
    const argsToJson = function (args, wholeArgs) {
        return args.map(function (arg, place) {
            const isWhole = (wholeArgs && wholeArgs.includes(place) && arg !== undefined);
            if (!isWhole) return toJson(arg, 1);
            try {
                return { __bpJson: JSON.stringify(arg) };
            } catch (error) {
                return toJson(arg, 1); // WHY: a value that holds itself has no JSON text
            }
        });
    };

    const makeCallback = function (callbackId, ownerId, wholeArgs) {
        return function (...args) {
            const owner = (ownerId) ? objects.get(ownerId) : null;
            send(callbackId, "callback", { args: argsToJson(args, wholeArgs), state: stateOf(owner) });
        };
    };

    // The text of a number, as the format of Python writes it ("{:,.1f} TL"). WHY en-US: Python writes 1,234.5.
    const makeNumberFormat = function (format) {
        const options = { useGrouping: (format.thousands === 1) };
        if (format.decimals === null) {
            options.maximumFractionDigits = MAX_FRACTION_DIGITS;
        } else {
            options.minimumFractionDigits = format.decimals;
            options.maximumFractionDigits = format.decimals;
        }
        const isPercent = (format.percent === 1);
        const percentSign = isPercent ? "%" : ""; // WHY: Python writes {:.1%} of 0.123 as 12.3%, with its sign
        return function (value) {
            if (typeof value !== "number") return String(value);
            const number = isPercent ? value * 100 : value;
            return format.prefix + number.toLocaleString("en-US", options) + percentSign + format.suffix;
        };
    };

    // A value from Python as the page takes it: the markers become functions and objects.
    const revive = function (value, ownerId) {
        if (value === null || typeof value !== "object") return value;
        if (Array.isArray(value)) {
            return value.map(function (item) { return revive(item, ownerId); });
        }
        if (value.__bpCallback) return makeCallback(value.__bpCallback, ownerId, value.wholeArgs);
        if (value.__bpObject) return objectOf(value.__bpObject);
        if (value.__bpNoop) return function () {};
        if (value.__bpFormat) return makeNumberFormat(value.__bpFormat);
        const revived = {};
        Object.keys(value).forEach(function (key) {
            revived[key] = revive(value[key], ownerId);
        });
        return revived;
    };

    const makeObject = function (command, props) {
        const make = resolveGlobal(command.type);
        if (typeof make !== "function") {
            throw new Error(command.type + " is not loaded (App(components=[\"" + command.type + "\"]) loads it)");
        }
        const obj = make(...command.args, props);
        // WHY: A group starts as the container of the next objects. Python gives the parent of every object
        //      itself, so a group is closed at once (a "with" block in Python only names the parent).
        if (GROUP_TYPES.includes(command.type)) endGroup();
        return obj;
    };

    const create = function (command) {
        const parent = objectOf(command.parent || PAGE_ID);
        const props = revive(command.props, command.id);
        const obj = createIn(parent, function () {
            return makeObject(command, props);
        });
        obj.__bpId = command.id;
        obj.__bpState = command.state || null;
        objects.set(command.id, obj);
    };

    const set = function (command) {
        const obj = objectOf(command.id);
        const props = revive(command.props, command.id);
        // WHY: page (a MainBox) has no props(): its values go one by one (Object.assign calls the setters).
        if (typeof obj.props !== "function") {
            Object.assign(obj, props);
            return;
        }
        obj.props(props);
    };

    const call = function (command) {
        const obj = objectOf(command.id);
        if (typeof obj[command.method] !== "function") throw new Error("There is no method " + command.method);
        obj[command.method](...revive(command.args, command.id));
        // WHY: a silent change (setValue(v, 1)) tells nobody, and the component may change the value (a slider keeps
        //      it inside min..max): Python gets the state as the page has it.
        if (command.refresh) send(command.id, "__state", { state: stateOf(obj) });
    };

    const keepObject = function (id, obj) {
        obj.__bpId = id;
        objects.set(id, obj);
    };

    const callStatic = function (command) {
        const target = resolveGlobal(command.target);
        if (!target || typeof target[command.method] !== "function") {
            throw new Error(command.target + "." + command.method + " is not loaded");
        }
        const result = target[command.method](...revive(command.args, null));
        if (command.keep) keepObject(command.keep, result);
        if (!command.answer) return;
        const tellAnswer = function (value) {
            send(command.answer, "callback", { args: [toJson(value)], state: null });
        };
        Promise.resolve(result).then(tellAnswer, function () { tellAnswer(null); });
    };

    const stepInto = function (obj, step, ownerId) {
        if (obj === undefined || obj === null) return obj;
        if (step && typeof step === "object" && step.call) {
            const method = obj[step.call];
            return (typeof method === "function") ? method.apply(obj, revive(step.args || [], ownerId)) : undefined;
        }
        return obj[step];
    };

    const part = function (command) {
        let obj = objectOf(command.of);
        command.path.forEach(function (step) {
            obj = stepInto(obj, step, command.of);
        });
        if (!isBasicObject(obj)) throw new Error("There is no box at " + JSON.stringify(command.path));
        obj.__bpId = obj.__bpId || command.id;
        objects.set(command.id, obj);
    };

    // WHY: the objects of a popover come after it was placed, and it grew from where it stood.
    const placeBubble = function (command) {
        const bubble = objectOf(command.id);
        Tooltip.place(bubble, Tooltip.toPageRect(objectOf(command.target)), command.side);
    };

    // What an event tells Python. An Input sends its text with every event: Python keeps it, so reading
    // inp.text in Python needs no question to the page.
    const dataOf = function (id, obj, event) {
        const data = {};
        if (obj.inputElement) data.text = obj.text;
        if (event && event.key !== undefined) {
            data.key = event.key;
            data.code = event.code;
            data.shift = event.shiftKey;
            data.ctrl = event.ctrlKey;
            data.alt = event.altKey;
            data.meta = event.metaKey;
        }
        if (event && event.clientX !== undefined) {
            data.x = event.clientX;
            data.y = event.clientY;
        }
        if (event && event.detail && typeof event.detail === "object") data.detail = toJson(event.detail); // a CustomEvent
        data.state = (id === PAGE_ID) ? { width: page.width, height: page.height } : stateOf(obj);
        return data;
    };

    const listen = function (command) {
        const obj = objectOf(command.id);
        obj.on(command.event, function (self, event) {
            send(command.id, command.event, dataOf(command.id, obj, event));
        });
    };

    // The objects that are not on the page any more leave the list, and Python is told (it forgets their callbacks).
    // WHY not only after remove: a component removes objects itself too (a closed Dialog, the panel of a removed tab).
    const sweepRemoved = function () {
        lastSweepAt = performance.now();
        const removedIds = [];
        objects.forEach(function (obj, id) {
            if (obj.elem.isConnected) return;
            removedIds.push(id);
            objects.delete(id);
        });
        return removedIds;
    };

    // basic.js removes the objects inside the removed one too.
    const remove = function (command) {
        objectOf(command.id).remove();
        return sweepRemoved();
    };

    const HANDLERS = { create: create, set: set, call: call, static: callStatic, part: part, placeBubble: placeBubble, listen: listen, remove: remove };

    // *** COMPONENTS THAT ARE NOT LOADED BY index.html (window.__bpComponents: name -> { file, needs })

    const loadScript = function (file) {
        return new Promise(function (resolve, reject) {
            const script = document.createElement("script");
            script.src = file;
            script.onload = resolve;
            script.onerror = function () { reject(new Error("could not load " + file)); };
            document.head.appendChild(script);
        });
    };

    // The files of the components and of what they need, each once, the needed ones first.
    const filesInOrder = function (names, errors) {
        const files = [];
        const seen = new Set(); // WHY: two components may need each other
        const addFile = function (name) {
            if (seen.has(name)) return;
            seen.add(name);
            const entry = (window.__bpComponents || {})[name];
            if (!entry) {
                errors.push("unknown component " + name);
                return;
            }
            (entry.needs || []).forEach(addFile);
            const isLoaded = (resolveGlobal(name) !== undefined);
            if (!isLoaded && !files.includes(entry.file)) files.push(entry.file);
        };
        names.forEach(addFile);
        return files;
    };

    // *** PUBLIC FUNCTIONS:

    // Applies the commands in order. A failed command does not stop the others: its error goes back to Python
    // with the line of the Python code that sent it.
    const apply = function (commands) {
        const startedAt = performance.now();
        const answer = { errors: [], removed: [] };
        commands.forEach(function (command) {
            try {
                const removedIds = HANDLERS[command.op](command);
                if (removedIds) answer.removed.push(...removedIds);
            } catch (error) {
                // WHY String(): a thrown text or object has no message; Python read error["message"] and failed
                const message = (error && error.message) ? error.message : String(error);
                answer.errors.push({ op: command.op, id: command.id || command.target, src: command.src || "", message: message });
                // WHY: Python waits for the answer of a dialog; a call that failed never gave one, so it waited for ever
                if (command.op === "static" && command.answer) send(command.answer, "callback", { args: [null], state: null });
            }
        });
        if (performance.now() - lastSweepAt > SWEEP_INTERVAL_MS) answer.removed.push(...sweepRemoved());
        // WHY: a component sends an event and then leaves the page (a Dialog: onClose, then remove()). Python forgets a
        //      removed object only after the events sent before this answer are handled.
        answer.lastEvent = eventNumber;
        answer.ms = performance.now() - startedAt;
        return answer;
    };

    // The value of a property as basic.js reads it (Python: obj.measure("width"))
    const read = function (id, key) {
        return toJson(objectOf(id)[key]);
    };

    // A method of an object and its result (Python: obj.ask("getValue"))
    const ask = function (id, method, args) {
        const obj = objectOf(id);
        if (typeof obj[method] !== "function") throw new Error("There is no method " + method);
        return toJson(obj[method](...revive(args, id)));
    };

    const loadComponents = async function (names) {
        const errors = [];
        for (const file of filesInOrder(names, errors)) {
            try {
                await loadScript(file);
            } catch (error) {
                errors.push(error.message);
            }
        }
        return { errors: errors };
    };

    // *** THE MESSAGES OF THE PAGE go to the terminal of Python (a warning of a component, an error).

    const tellPythonMessage = function (kind, text) {
        if (!isPythonTold) {
            earlyMessages.push([kind, text]);
            return;
        }
        send(PAGE_ID, "__message", { kind: kind, text: text });
    };

    ["error", "warn"].forEach(function (kind) {
        const original = console[kind].bind(console);
        console[kind] = function (...args) {
            original(...args);
            tellPythonMessage(kind, args.map(String).join(" "));
        };
    });
    window.addEventListener("error", function (event) {
        tellPythonMessage("error", event.message + " (" + event.filename + ":" + event.lineno + ")");
    });
    window.addEventListener("unhandledrejection", function (event) {
        tellPythonMessage("error", "Promise: " + String(event.reason));
    });

    // WHY: a file dropped on the window opened in it, in the place of the program. (A FilePicker takes its own drop;
    //      a text dragged into a field goes on as usual.)
    const keepFileOutOfThePage = function (event) {
        const isFile = event.dataTransfer && Array.from(event.dataTransfer.types).includes("Files");
        if (isFile) event.preventDefault();
    };
    window.addEventListener("dragover", keepFileOutOfThePage);
    window.addEventListener("drop", keepFileOutOfThePage);

    // A drop of files is told to Python first, in the order of the events (a FilePicker tells its new files after it).
    // WHY: the path of a dropped file comes from pywebview by another way. A path Python kept for a file of the same name
    //      and size belonged to an earlier drop, and a new drop got that old path when the FilePicker told first.
    const tellPythonOfADrop = function (event) {
        const files = (event.dataTransfer && event.dataTransfer.files) ? Array.from(event.dataTransfer.files) : [];
        if (!files.length || !isPythonTold) return;
        send(PAGE_ID, "__drop", {
            files: files.map(function (file) {
                return { name: file.name, size: file.size, lastModified: file.lastModified };
            }),
        });
    };
    window.addEventListener("drop", tellPythonOfADrop, true); // WHY capture: before the drop of the FilePicker

    // *** READY: Python starts when both basic.js (page) and the bridge of pywebview are ready.

    const hasPythonApi = function () {
        return !!(window.pywebview && window.pywebview.api && window.pywebview.api.ready);
    };

    const tellPythonWhenReady = function () {
        if (isPythonTold || !isBasicReady || !hasPythonApi()) return;
        isPythonTold = true;
        const prefersDark = !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
        window.pywebview.api.ready(basic.version, page.width, page.height, prefersDark);
        earlyMessages.forEach(function (message) { tellPythonMessage(message[0], message[1]); });
    };

    // The ground of a page loaded again for another theme (app.set_theme()): Python leaves it in window.name, which
    // stays over the load. WHY: the new page was light for a moment before Python drew it dark.
    const EARLY_PAGE_COLOR_PREFIX = "ozdenui-page-color:";
    const takeEarlyPageColor = function () {
        const name = String(window.name || "");
        if (name.indexOf(EARLY_PAGE_COLOR_PREFIX) !== 0) return;
        const color = name.slice(EARLY_PAGE_COLOR_PREFIX.length);
        if (color) page.color = color;
    };

    // basic.js calls start() when page is created.
    window.start = function () {
        takeEarlyPageColor();
        isBasicReady = true;
        tellPythonWhenReady();
    };
    window.addEventListener("pywebviewready", tellPythonWhenReady);

    return { apply: apply, read: read, ask: ask, objectOf: objectOf, loadComponents: loadComponents };

})();
