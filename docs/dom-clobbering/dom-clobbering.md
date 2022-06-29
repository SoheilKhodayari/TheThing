# DOM Clobbering

[DOM Clobbering](https://wicg.github.io/sanitizer-api/#dom-clobbering) is a type of JavaScript-less injection attack where attackers confuse the client-side JavaScript code of web applications by inserting a piece of non-script HTML markup into webpages, and transforming it into executable code leveraging [named property accesses](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object).

DOM Clobbering vulnerabilities originate from a naming collision between JavaScript variables and named HTML markups, i.e., markups with an `id` or `name` attribute

## Named Properties in DOM

One of the ways JavaScript programs can manipulate the contents of webpages is through the [Document Object Model (DOM)](https://www.w3.org/TR/WD-DOM/introduction.html) a tree-structured representation of the rendered webpages.

Normally, DOM tree elements can be accessed in JavaScript via the object [selector methods](https://www.w3.org/TR/selectors-4/) of the [document](https://developer.mozilla.org/en-US/docs/Web/API/Document) object, e.g., `document.getElementById(x)` to locate the element with id `x`.

However, that is not the only way and the same can be acheived via a **property** of the `document` and global `window` objects, e.g., `document.x`, or `window.x`, known as `named property access`, as specified in [HTML](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object) and [DOM](https://html.spec.whatwg.org/multipage/dom.html#dom-tree-accessors) living standards. 

Accordingly, web browsers map HTML elements to JavaScript objects automatically based on the element `named` properties. Such named properties are, for example, `id` and `name` HTML tag attributes. 



## Attack Example

Consider the following code listing. 

```js
1 var s = document.createElement('script');
2 let config = window.globalConfig || {href: 'script.js'};
3 s.src = config.href;
4 document.body.appendChild(s);
```

When an [undefined variable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/undefined) and an HTML markup have the same name, the browser replaces the content of the variable with the DOM object mirroring the markup type. 

The snippet shows a vulnerable code, which loads a script whose URL is stored in a global configuration object, i.e., `window.globalConfig`. Specifically, the code first creates a `script` tag (line 1), and then, it retrieves the global configuration object and stores it in a local variable `config` (line 2). If the configuration object does not exist, it uses a minimal default configuration, i.e., `{href: script.js'}` (line 2). Then, the program sets the `src` attribute of the newly created script tag to the `href` property of the configuration object (line 3) and appends the new script to the DOM tree, resulting in the execution of the script (line 4). 

The vulnerability originates in the assignment in line 2 because
attackers can control the value of `window.globalConfig`, and ultimately, pick the script `src` value of their choosing by injecting an HTML tag with `id="globalConfig"`, e.g., `<a id="globalConfig" href="malicious.js">`. 

When parsing such a markup code, the browser maps the anchor tag element to the `window.globalConfig` property as mandated by the [named property accesses](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object). The escalation to arbitrary code execution happens in line 3, when the code reads the `href` property of the object `window.globalConfig`, which no longer contains the object with the global configuration but it contains the attacker-controlled anchor tag whose `href` property value is `malicious.js`. 


**Note.** Attackers can abuse named property accesses in other ways, where instead of overwriting variables by HTML nodes, they can overshadow [browser APIs](https://developer.mozilla.org/en-US/docs/Web/API). For example, if the attacker inserts a markup with `id=getElementbyId` in DOM, then the API `document.getElementbyId` no longer refers to the built-in API for finding an element in the DOM tree, but rather mirrors the DOM element with id `getElementbyId` in the DOM tree. This behaviour is due to the so-called [named property visibility algorithm](https://webidl.spec.whatwg.org/#legacy-platform-object-abstract-ops).




## Clobbering Techniques

### [T1: Named Access on Window (R1)](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object)

These group of markups leverage a single HTML element whose `id` or `name` is set to a target variable `x`, clobbering `window.x`.

### [T2: DOM Tree Accessors (R2)](https://html.spec.whatwg.org/multipage/dom.html#dom-tree-accessors)

The markups of this group can shadow `document` properties using a single named HTML element. Note that assignment to `document` is always shadowed by DOM Clobbering. 


### [T3: Form Parent-Child Elements (R3+R1, R3+R2)](https://html.spec.whatwg.org/multipage/forms.html#the-form-element)

These markups clobber properties `X.y` where `X` can be any of `x`, window.x, and document.x. First, they exploit either the rules R1 or R2 to clobber the base object `X`. 

Then, they use the Form Element rule (R3) to clobber property `y` of object `X`, i.e., the form elements' parent-child relationships where the browser creates a property of the second element for the first element's accessor variable. 

DOM Clobbering code that rely on this technique comprise a `form` tag and a child (e.g., an `input` whose named attributes are set to variables `x` and `y`, respectively. 


### [T4: Nested Window Proxies (R4+R1, R4+R2)](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#the-iframe-element)

These markups use the Iframe `srcdoc` rule (R4) to create nested window proxies that are named with `x` and `y`, respectively. 

Similarly to the previous group of markups, it uses the rule R1 or R2 to clobber the base object.
Then, the stacked iframes enable attackers to exploit frame navigation features to clobber object properties like `x.y`.


### [T5: HTML Collection (R5+R1, R5+R2)](https://dom.spec.whatwg.org/#interface-htmlcollection)

When two or more elements have the same `id` or `name` in the DOM tree, browsers create an array-like object called [HTMLCollection](https://portswigger.net/research/dom-clobbering-strikes-back), which contains all elements with the same id. 

Elements inside HTMLCollections can accessed by (i) their index in the collection and (ii) their `id` and `name`.
Attackers can exploit feature (i) to clobber arrays and loop elements (e.g., `x` and `x[i]`), where the length of the array can be controlled by the number of elements with the same id in the payload. Also, they can leverage feature (ii) to create payloads that clobber properties like `x.x` and `x.y`, where `x` references the collection, `x.x` points to the first element in the collection with id `x`, and finally `x.y` refers to the first element with id `x` and name `y` (see, e.g., [here](https://research.securitum.com/xss-in-amp4email-dom-clobbering/))




