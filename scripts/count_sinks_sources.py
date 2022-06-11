# -*- coding: utf-8 -*-

"""
	Copyright (C) 2022  Soheil Khodayari, CISPA
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.
	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
	Description:
	------------
	Counts the number of sinks and sources in the collected data

"""

import json, os, sys
import hashlib


BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


sites = []
with open('./outputs/sitelist.out', 'r') as fd:
	lines = fd.readlines()
	for line in lines:
		sites.append(line.strip().rstrip('\n').strip())


sites_folder = []
with open('./outputs/sitelist_folder_names.out', 'r') as fd:
	lines = fd.readlines()
	for line in lines:
		sites_folder.append(line.strip().rstrip('\n').strip())


sites_folder = ["http-github.com"]
SINK_FILE_NAME = 'sinks.out.json'
SOURCE_FILE_NAME = 'sources.out.json'

# sources
window_methods = ["alert", "atob", "blur", "btoa", "cancelAnimationFrame", "cancelIdleCallback", "captureEvents", "clearImmediate", "clearInterval", "clearTimeout", "close", "confirm", "convertPointFromNodeToPage", "convertPointFromPageToNode", "createImageBitmap", "dump", "fetch", "find", "focus", "getComputedStyle", "getDefaultComputedStyle", "getSelection", "home", "matchMedia", "minimize", "moveBy", "moveTo", "open", "openDialog", "postMessage", "print", "prompt", "queueMicrotask", "releaseEvents", "requestAnimationFrame", "requestIdleCallback", "resizeBy", "resizeTo", "routeEvent", "scroll", "scrollBy", "scrollByLines", "scrollByPages", "scrollTo", "setCursor", "setImmediate", "setInterval", "setTimeout", "showDirectoryPicker", "showModalDialog", "showOpenFilePicker", "showSaveFilePicker", "sizeToContent", "stop", "updateCommands", "addEventListener"];
window_properties = ["caches", "closed", "console", "controllers", "crossOriginIsolated", "crypto", "customElements", "defaultStatus", "devicePixelRatio", "dialogArguments", "directories", "document", "event", "frameElement", "frames", "fullScreen", "history", "indexedDB", "innerHeight", "innerWidth", "isSecureContext", "isSecureContext", "length", "localStorage", "location", "locationbar", "menubar", "mozAnimationStartTime", "mozInnerScreenX", "mozInnerScreenY", "name", "navigator", "onabort", "onafterprint", "onanimationcancel", "onanimationend", "onanimationiteration", "onappinstalled", "onauxclick", "onbeforeinstallprompt", "onbeforeprint", "onbeforeunload", "onblur", "oncancel", "oncanplay", "oncanplaythrough", "onchange", "onclick", "onclose", "oncontextmenu", "oncuechange", "ondblclick", "ondevicemotion", "ondeviceorientation", "ondeviceorientationabsolute", "ondragdrop", "ondurationchange", "onended", "onerror", "onfocus", "onformdata", "ongamepadconnected", "ongamepaddisconnected", "ongotpointercapture", "onhashchange", "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onlanguagechange", "onload", "onloadeddata", "onloadedmetadata", "onloadend", "onloadstart", "onlostpointercapture", "onmessage", "onmessageerror", "onmousedown", "onmouseenter", "onmouseleave", "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onpaint", "onpause", "onplay", "onplaying", "onpointercancel", "onpointerdown", "onpointerenter", "onpointerleave", "onpointermove", "onpointerout", "onpointerover", "onpointerup", "onpopstate", "onrejectionhandled", "onreset", "onresize", "onscroll", "onselect", "onselectionchange", "onselectstart", "onstorage", "onsubmit", "ontouchcancel", "ontouchstart", "ontransitioncancel", "ontransitionend", "onunhandledrejection", "onunload", "onvrdisplayactivate", "onvrdisplayblur", "onvrdisplayconnect", "onvrdisplaydeactivate", "onvrdisplaydisconnect", "onvrdisplayfocus", "onvrdisplaypointerrestricted", "onvrdisplaypointerunrestricted", "onvrdisplaypresentchange", "onwheel", "opener", "origin", "outerHeight", "outerWidth", "pageXOffset", "pageYOffset", "parent", "performance", "personalbar", "pkcs11", "screen", "screenLeft", "screenTop", "screenX", "screenY", "scrollbars", "scrollMaxX", "scrollMaxY", "scrollX", "scrollY", "self", "sessionStorage", "sidebar", "speechSynthesis", "status", "statusbar", "toolbar", "top", "visualViewport"];

tempt = window_methods + window_properties
window_props = []
for o in tempt:
	window_props.append("window."+ o)


document_properties = ["cookie", "activeElement", "alinkColor", "all", "anchors", "applets", "bgColor", "body", "characterSet", "childElementCount", "children", "compatMode", "contentType", "currentScript", "defaultView", "designMode", "dir", "doctype", "documentElement", "documentURI", "documentURIObject", "domain", "embeds", "fgColor", "firstElementChild", "forms", "fullscreen", "fullscreenElement", "fullscreenEnabled", "head", "height", "hidden", "images", "implementation", "lastElementChild", "lastModified", "lastStyleSheetSet", "linkColor", "links", "location", "mozSyntheticDocument", "onabort", "onafterscriptexecute", "onanimationcancel", "onanimationend", "onanimationiteration", "onauxclick", "onbeforescriptexecute", "onblur", "oncancel", "oncanplay", "oncanplaythrough", "onchange", "onclick", "onclose", "oncontextmenu", "oncuechange", "ondblclick", "ondurationchange", "onended", "onerror", "onfocus", "onformdata", "onfullscreenchange", "onfullscreenerror", "ongotpointercapture", "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload", "onloadeddata", "onloadedmetadata", "onloadend", "onloadstart", "onlostpointercapture", "onmousedown", "onmouseenter", "onmouseleave", "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onoffline", "ononline", "onpause", "onplay", "onplaying", "onpointercancel", "onpointerdown", "onpointerenter", "onpointerleave", "onpointermove", "onpointerout", "onpointerover", "onpointerup", "onreset", "onresize", "onscroll", "onselect", "onselectionchange", "onselectstart", "onsubmit", "ontouchcancel", "ontouchstart", "ontransitioncancel", "ontransitionend", "onvisibilitychange", "onwheel", "pictureInPictureElement", "pictureInPictureEnabled", "plugins", "pointerLockElement", "popupNode", "preferredStyleSheetSet", "readyState", "referrer", "rootElement", "scripts", "scrollingElement", "selectedStyleSheetSet", "styleSheets", "styleSheetSets", "timeline", "title", "tooltipNode", "URL", "visibilityState", "vlinkColor", "width", "xmlEncoding", "xmlVersion"];
document_methods = ["adoptNode", "append", "caretPositionFromPoint", "caretRangeFromPoint", "clear", "close", "createAttribute", "createCDATASection", "createComment", "createDocumentFragment", "createElement", "createElementNS", "createEntityReference", "createEvent", "createExpression", "createExpression", "createNodeIterator", "createNSResolver", "createNSResolver", "createProcessingInstruction", "createRange", "createTextNode", "createTouch", "createTouchList", "createTreeWalker", "elementFromPoint", "elementsFromPoint", "enableStyleSheetsForSet", "evaluate", "evaluate", "execCommand", "exitFullscreen", "exitPictureInPicture", "exitPointerLock", "getAnimations", "getBoxObjectFor", "getElementById", "getElementsByClassName", "getElementsByName", "getElementsByTagName", "getElementsByTagNameNS", "getSelection", "hasFocus", "hasStorageAccess", "importNode", "mozSetImageElement", "open", "prepend", "queryCommandEnabled", "queryCommandSupported", "querySelector", "querySelectorAll", "registerElement", "releaseCapture", "replaceChildren", "requestStorageAccess", "write", "writeln", "addEventListener"];

tempt = document_methods + document_properties
document_props = []
for o in tempt:
	document_props.append("document."+ o)

# sink semantic types
OPEN_REDIRECT_VULN = "open_redirect";
WEBSOCKET_URL_POISONING = "websocket_url_poisoning";
LINK_MANIPULATION = "link_manipulation";
COOKIE_MANIPULATION = "cookie_manipulation";
WEBSTORAGE_MANIPULATION = "web_storage_manipulation";
DOCUMENT_DOMAIN_MANIPULATION = "document_domain_manipulation";
CLIENT_SIDE_JSON_INJECTION = "client_side_json_injection";
REDOS_ATTACK = "regex_denial_of_service";
POST_MESSAGE_MANIPULATION = "post_message_manipulation";
FILE_READ_PATH_MANIPULATION = "file_read_path_manipulation";
REQUEST_FORGERY = "request_forgery";
CROSS_SITE_SCRIPTING = "cross_site_scripting";


with open('./outputs/sinks-sources-github.out', 'w+') as main_fd:
	for idx in range(len(sites_folder)):

		if len(sites_folder) == 1:
			website = "github.com"
		else:
			website = sites[idx]
		folder_name = sites_folder[idx]

		count_webpages = 0
		count_sinks = 0
		min_sinks = -1
		max_sinks = -1

		count_sink_vulnerabilites = {
			"open_redirect"	 : 0,
			"websocket_url_poisoning"	 : 0,
			"link_manipulation"	 : 0,
			"cookie_manipulation"	 : 0,
			"web_storage_manipulation"	 : 0,
			"document_domain_manipulation"	 : 0,
			"client_side_json_injection"	 : 0,
			"regex_denial_of_service"	 : 0,
			"post_message_manipulation"	 : 0,
			"file_read_path_manipulation"	 : 0,
			"request_forgery"	 : 0,
			"cross_site_scripting"	 : 0,
		}


		count_sinks_types = {
			"window.location": 0,
			"script.textContent": 0,
			"element.innerHTML": 0,
			"element.outerHTML": 0,
			"eval": 0,
			"setTimeout": 0,
			"setInterval": 0,
			"new Function()": 0,
			"element.insertAdjacentHTML()": 0,
			"document.write": 0,
			"document.writeln": 0,
			"$.parseHTML()": 0,
			"$(element).html"		: 0,
			"$(element).append"		: 0,
			"$(element).prepend"		: 0,
			"$(element).add"			: 0,
			"$(element).insertAfter"	: 0,
			"$(element).insertBefore" : 0,
			"$(element).after"		: 0,
			"$(element).before"		: 0,
			"$(element).wrap"			: 0,
			"$(element).wrapInner"	: 0,
			"$(element).wrapAll"		: 0,
			"$(element).has"			: 0,
			"$(element).index"		: 0,
			"$(element).replaceAll"	: 0,
			"$(element).replaceWith"	: 0,
			"element.src": 0,
			"document.cookie": 0,
			"document.domain": 0,
			"fetch": 0,
			"asyncrequest": 0,
			"$.ajax": 0,
			"XMLHttpRequest.open()": 0,
			"XMLHttpRequest.setRequestHeader()": 0,
			"new FileReader().readAsText()": 0,
			"window.postMessage()": 0,
			"localStorage.setItem()": 0,
			"sessionStorage.setItem()": 0,
			"JSON.parse()": 0,
			"new WebSocket()": 0,
			"new RegExp()": 0,
		}

		count_sink_vulnerabilites_taintable = {
			"open_redirect"	 : 0,
			"websocket_url_poisoning"	 : 0,
			"link_manipulation"	 : 0,
			"cookie_manipulation"	 : 0,
			"web_storage_manipulation"	 : 0,
			"document_domain_manipulation"	 : 0,
			"client_side_json_injection"	 : 0,
			"regex_denial_of_service"	 : 0,
			"post_message_manipulation"	 : 0,
			"file_read_path_manipulation"	 : 0,
			"request_forgery"	 : 0,
			"cross_site_scripting"	 : 0,
		}


		count_sinks_types_taintable = {
			"window.location": 0,
			"script.textContent": 0,
			"element.innerHTML": 0,
			"element.outerHTML": 0,
			"eval": 0,
			"setTimeout": 0,
			"setInterval": 0,
			"new Function()": 0,
			"element.insertAdjacentHTML()": 0,
			"document.write": 0,
			"document.writeln": 0,
			"$.parseHTML()": 0,
			"$(element).html"		: 0,
			"$(element).append"		: 0,
			"$(element).prepend"		: 0,
			"$(element).add"			: 0,
			"$(element).insertAfter"	: 0,
			"$(element).insertBefore" : 0,
			"$(element).after"		: 0,
			"$(element).before"		: 0,
			"$(element).wrap"			: 0,
			"$(element).wrapInner"	: 0,
			"$(element).wrapAll"		: 0,
			"$(element).has"			: 0,
			"$(element).index"		: 0,
			"$(element).replaceAll"	: 0,
			"$(element).replaceWith"	: 0,
			"element.src": 0,
			"document.cookie": 0,
			"document.domain": 0,
			"fetch": 0,
			"asyncrequest": 0,
			"$.ajax": 0,
			"XMLHttpRequest.open()": 0,
			"XMLHttpRequest.setRequestHeader()": 0,
			"new FileReader().readAsText()": 0,
			"window.postMessage()": 0,
			"localStorage.setItem()": 0,
			"sessionStorage.setItem()": 0,
			"JSON.parse()": 0,
			"new WebSocket()": 0,
			"new RegExp()": 0,
		}


		count_sources = 0
		min_sources = -1
		max_sources = -1

		count__window_native_property = 0
		count__native_property = 0
		count__document_native_property = 0
		count__window_custom_property = 0
		count__custom_property = 0
		count__document_custom_property = 0


		website_folder = os.path.join(DATA_DIR, folder_name)
		webpages = os.listdir(website_folder)
		for webpage_hash in webpages:
			webpage_folder = os.path.join(website_folder, webpage_hash)
			if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):

				source_file = os.path.join(webpage_folder, SOURCE_FILE_NAME)
				sink_file = os.path.join(webpage_folder, SINK_FILE_NAME)
				if not os.path.exists(source_file) or not os.path.exists(sink_file):
					continue
				count_webpages+=1

				# ---------------------------------------------
				#	Sources
				# ---------------------------------------------
				source_fd = open(source_file, 'r')
				source_data = json.load(source_fd)
				source_fd.close()
				sources = source_data["sources"].keys()

				current_count_sources = len(sources)
				count_sources+= current_count_sources

				if current_count_sources < min_sources or min_sources == -1:
					min_sources = current_count_sources
				if current_count_sources > max_sources or max_sources == -1:
					max_sources = current_count_sources


				for s in sources:
					if s.startswith('window.'):
						if s in window_props:
							count__window_native_property+=1
						else:
							count__window_custom_property+=1
					elif s.startswith('document.'):
						if s in document_props:
							count__document_native_property+=1
						else:
							count__document_custom_property+=1
					else:
						if s in window_methods or s in window_properties or s in document_methods or s in document_properties:
							count__native_property+=1
						else:
							count__custom_property+=1


				# ---------------------------------------------
				#	Sinks
				# ---------------------------------------------

				sink_fd = open(sink_file, 'r')
				sink_data = json.load(sink_fd)
				sink_fd.close()
				sinks = sink_data["sinks"]

				current_count_sinks = len(sinks)
				count_sinks+= current_count_sinks

				if current_count_sinks < min_sinks or min_sinks == -1:
					min_sinks = current_count_sinks
				if current_count_sinks > max_sinks or max_sinks == -1:
					max_sinks = current_count_sinks

				for sink_object in sinks:
					count_sink_vulnerabilites[sink_object["vuln"]]+=1
					count_sinks_types[sink_object["sink_type"]]+=1
					if str(sink_object["taint_possibility"]).lower() == 'true':
						count_sink_vulnerabilites_taintable[sink_object["vuln"]]+=1
						count_sinks_types_taintable[sink_object["sink_type"]]+=1

		avg_sinks = count_sinks / count_webpages
		avg_sources = count_sources / count_webpages

		writeme="{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
			website,
			count_webpages,
			min_sources,
			avg_sources,
			max_sources,
			count_sources,
			count__window_native_property,
			count__native_property,
			count__document_native_property,
			count__window_custom_property,
			count__custom_property,
			count__document_custom_property,
			min_sinks,
			avg_sinks,
			max_sinks,
			count_sinks,
			##
			count_sink_vulnerabilites["open_redirect"], 
			count_sink_vulnerabilites["websocket_url_poisoning"],	
			count_sink_vulnerabilites["link_manipulation"],	
			count_sink_vulnerabilites["cookie_manipulation"],	
			count_sink_vulnerabilites["web_storage_manipulation"],	
			count_sink_vulnerabilites["document_domain_manipulation"],	
			count_sink_vulnerabilites["client_side_json_injection"],	
			count_sink_vulnerabilites["regex_denial_of_service"],	
			count_sink_vulnerabilites["post_message_manipulation"],	
			count_sink_vulnerabilites["file_read_path_manipulation"],	
			count_sink_vulnerabilites["request_forgery"],	
			count_sink_vulnerabilites["cross_site_scripting"],
			####
			count_sink_vulnerabilites_taintable["open_redirect"], 
			count_sink_vulnerabilites_taintable["websocket_url_poisoning"],	
			count_sink_vulnerabilites_taintable["link_manipulation"],	
			count_sink_vulnerabilites_taintable["cookie_manipulation"],	
			count_sink_vulnerabilites_taintable["web_storage_manipulation"],	
			count_sink_vulnerabilites_taintable["document_domain_manipulation"],	
			count_sink_vulnerabilites_taintable["client_side_json_injection"],	
			count_sink_vulnerabilites_taintable["regex_denial_of_service"],	
			count_sink_vulnerabilites_taintable["post_message_manipulation"],	
			count_sink_vulnerabilites_taintable["file_read_path_manipulation"],	
			count_sink_vulnerabilites_taintable["request_forgery"],	
			count_sink_vulnerabilites_taintable["cross_site_scripting"],
			####
			count_sinks_types["window.location"],
			count_sinks_types["script.textContent"],
			count_sinks_types["element.innerHTML"],
			count_sinks_types["element.outerHTML"],
			count_sinks_types["eval"],
			count_sinks_types["setTimeout"],
			count_sinks_types["setInterval"],
			count_sinks_types["new Function()"],
			count_sinks_types["element.insertAdjacentHTML()"],
			count_sinks_types["document.write"],
			count_sinks_types["document.writeln"],
			count_sinks_types["$.parseHTML()"],
			count_sinks_types["$(element).html"],
			count_sinks_types["$(element).append"],
			count_sinks_types["$(element).prepend"],
			count_sinks_types["$(element).add"],
			count_sinks_types["$(element).insertAfter"],
			count_sinks_types["$(element).insertBefore"],
			count_sinks_types["$(element).after"],
			count_sinks_types["$(element).before"],
			count_sinks_types["$(element).wrap"],
			count_sinks_types["$(element).wrapInner"],
			count_sinks_types["$(element).wrapAll"],
			count_sinks_types["$(element).has"],
			count_sinks_types["$(element).index"],
			count_sinks_types["$(element).replaceAll"],
			count_sinks_types["$(element).replaceWith"],
			count_sinks_types["element.src"],
			count_sinks_types["document.cookie"],
			count_sinks_types["document.domain"],
			count_sinks_types["fetch"],
			count_sinks_types["asyncrequest"],
			count_sinks_types["$.ajax"],
			count_sinks_types["XMLHttpRequest.open()"],
			count_sinks_types["XMLHttpRequest.setRequestHeader()"],
			count_sinks_types["new FileReader().readAsText()"],
			count_sinks_types["window.postMessage()"],
			count_sinks_types["localStorage.setItem()"],
			count_sinks_types["sessionStorage.setItem()"],
			count_sinks_types["JSON.parse()"],
			count_sinks_types["new WebSocket()"],
			count_sinks_types["new RegExp()"],
			####
			count_sinks_types_taintable["window.location"],
			count_sinks_types_taintable["script.textContent"],
			count_sinks_types_taintable["element.innerHTML"],
			count_sinks_types_taintable["element.outerHTML"],
			count_sinks_types_taintable["eval"],
			count_sinks_types_taintable["setTimeout"],
			count_sinks_types_taintable["setInterval"],
			count_sinks_types_taintable["new Function()"],
			count_sinks_types_taintable["element.insertAdjacentHTML()"],
			count_sinks_types_taintable["document.write"],
			count_sinks_types_taintable["document.writeln"],
			count_sinks_types_taintable["$.parseHTML()"],
			count_sinks_types_taintable["$(element).html"],
			count_sinks_types_taintable["$(element).append"],
			count_sinks_types_taintable["$(element).prepend"],
			count_sinks_types_taintable["$(element).add"],
			count_sinks_types_taintable["$(element).insertAfter"],
			count_sinks_types_taintable["$(element).insertBefore"],
			count_sinks_types_taintable["$(element).after"],
			count_sinks_types_taintable["$(element).before"],
			count_sinks_types_taintable["$(element).wrap"],
			count_sinks_types_taintable["$(element).wrapInner"],
			count_sinks_types_taintable["$(element).wrapAll"],
			count_sinks_types_taintable["$(element).has"],
			count_sinks_types_taintable["$(element).index"],
			count_sinks_types_taintable["$(element).replaceAll"],
			count_sinks_types_taintable["$(element).replaceWith"],
			count_sinks_types_taintable["element.src"],
			count_sinks_types_taintable["document.cookie"],
			count_sinks_types_taintable["document.domain"],
			count_sinks_types_taintable["fetch"],
			count_sinks_types_taintable["asyncrequest"],
			count_sinks_types_taintable["$.ajax"],
			count_sinks_types_taintable["XMLHttpRequest.open()"],
			count_sinks_types_taintable["XMLHttpRequest.setRequestHeader()"],
			count_sinks_types_taintable["new FileReader().readAsText()"],
			count_sinks_types_taintable["window.postMessage()"],
			count_sinks_types_taintable["localStorage.setItem()"],
			count_sinks_types_taintable["sessionStorage.setItem()"],
			count_sinks_types_taintable["JSON.parse()"],
			count_sinks_types_taintable["new WebSocket()"],
			count_sinks_types_taintable["new RegExp()"]
		)
		main_fd.write(writeme)

