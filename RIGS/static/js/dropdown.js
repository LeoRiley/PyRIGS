/*!
  * Bootstrap dropdown.js v4.4.1 (https://getbootstrap.com/)
  * Copyright 2011-2019 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t(require("jquery"),require("popper.js"),require("./util.js")):"function"==typeof define&&define.amd?define(["jquery","popper.js","./util.js"],t):(e=e||self).Dropdown=t(e.jQuery,e.Popper,e.Util)}(this,(function(e,t,n){"use strict";function r(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}e=e&&e.hasOwnProperty("default")?e.default:e,t=t&&t.hasOwnProperty("default")?t.default:t,n=n&&n.hasOwnProperty("default")?n.default:n;var a="dropdown",l="bs.dropdown",f="."+l,u=e.fn[a],c=new RegExp("38|40|27"),p={HIDE:"hide"+f,HIDDEN:"hidden"+f,SHOW:"show"+f,SHOWN:"shown"+f,CLICK:"click"+f,CLICK_DATA_API:"click.bs.dropdown.data-api",KEYDOWN_DATA_API:"keydown.bs.dropdown.data-api",KEYUP_DATA_API:"keyup.bs.dropdown.data-api"},h="disabled",d="show",g="dropup",_="dropright",m="dropleft",y="dropdown-menu-right",v="position-static",b='[data-toggle="dropdown"]',w=".dropdown form",P=".dropdown-menu",C=".navbar-nav",E=".dropdown-menu .dropdown-item:not(.disabled):not(:disabled)",D="top-start",A="top-end",O="bottom-start",j="bottom-end",I="right-start",N="left-start",k={offset:0,flip:!0,boundary:"scrollParent",reference:"toggle",display:"dynamic",popperConfig:null},T={offset:"(number|string|function)",flip:"boolean",boundary:"(string|element)",reference:"(string|element)",display:"string",popperConfig:"(null|object)"},K=function(){function i(e,t){this._element=e,this._popper=null,this._config=this._getConfig(t),this._menu=this._getMenuElement(),this._inNavbar=this._detectNavbar(),this._addEventListeners()}var o,u,w,K=i.prototype;return K.toggle=function(){if(!this._element.disabled&&!e(this._element).hasClass(h)){var t=e(this._menu).hasClass(d);i._clearMenus(),t||this.show(!0)}},K.show=function(r){if(void 0===r&&(r=!1),!(this._element.disabled||e(this._element).hasClass(h)||e(this._menu).hasClass(d))){var o={relatedTarget:this._element},s=e.Event(p.SHOW,o),a=i._getParentFromElement(this._element);if(e(a).trigger(s),!s.isDefaultPrevented()){if(!this._inNavbar&&r){if(void 0===t)throw new TypeError("Bootstrap's dropdowns require Popper.js (https://popper.js.org/)");var l=this._element;"parent"===this._config.reference?l=a:n.isElement(this._config.reference)&&(l=this._config.reference,void 0!==this._config.reference.jquery&&(l=this._config.reference[0])),"scrollParent"!==this._config.boundary&&e(a).addClass(v),this._popper=new t(l,this._menu,this._getPopperConfig())}"ontouchstart"in document.documentElement&&0===e(a).closest(C).length&&e(document.body).children().on("mouseover",null,e.noop),this._element.focus(),this._element.setAttribute("aria-expanded",!0),e(this._menu).toggleClass(d),e(a).toggleClass(d).trigger(e.Event(p.SHOWN,o))}}},K.hide=function(){if(!this._element.disabled&&!e(this._element).hasClass(h)&&e(this._menu).hasClass(d)){var t={relatedTarget:this._element},n=e.Event(p.HIDE,t),r=i._getParentFromElement(this._element);e(r).trigger(n),n.isDefaultPrevented()||(this._popper&&this._popper.destroy(),e(this._menu).toggleClass(d),e(r).toggleClass(d).trigger(e.Event(p.HIDDEN,t)))}},K.dispose=function(){e.removeData(this._element,l),e(this._element).off(f),this._element=null,this._menu=null,null!==this._popper&&(this._popper.destroy(),this._popper=null)},K.update=function(){this._inNavbar=this._detectNavbar(),null!==this._popper&&this._popper.scheduleUpdate()},K._addEventListeners=function(){var t=this;e(this._element).on(p.CLICK,(function(e){e.preventDefault(),e.stopPropagation(),t.toggle()}))},K._getConfig=function(t){return t=s({},this.constructor.Default,{},e(this._element).data(),{},t),n.typeCheckConfig(a,t,this.constructor.DefaultType),t},K._getMenuElement=function(){if(!this._menu){var e=i._getParentFromElement(this._element);e&&(this._menu=e.querySelector(P))}return this._menu},K._getPlacement=function(){var t=e(this._element.parentNode),n=O;return t.hasClass(g)?(n=D,e(this._menu).hasClass(y)&&(n=A)):t.hasClass(_)?n=I:t.hasClass(m)?n=N:e(this._menu).hasClass(y)&&(n=j),n},K._detectNavbar=function(){return e(this._element).closest(".navbar").length>0},K._getOffset=function(){var e=this,t={};return"function"==typeof this._config.offset?t.fn=function(t){return t.offsets=s({},t.offsets,{},e._config.offset(t.offsets,e._element)||{}),t}:t.offset=this._config.offset,t},K._getPopperConfig=function(){var e={placement:this._getPlacement(),modifiers:{offset:this._getOffset(),flip:{enabled:this._config.flip},preventOverflow:{boundariesElement:this._config.boundary}}};return"static"===this._config.display&&(e.modifiers.applyStyle={enabled:!1}),s({},e,{},this._config.popperConfig)},i._jQueryInterface=function(t){return this.each((function(){var n=e(this).data(l);if(n||(n=new i(this,"object"==typeof t?t:null),e(this).data(l,n)),"string"==typeof t){if(void 0===n[t])throw new TypeError('No method named "'+t+'"');n[t]()}}))},i._clearMenus=function(t){if(!t||3!==t.which&&("keyup"!==t.type||9===t.which))for(var n=[].slice.call(document.querySelectorAll(b)),r=0,o=n.length;r<o;r++){var s=i._getParentFromElement(n[r]),a=e(n[r]).data(l),f={relatedTarget:n[r]};if(t&&"click"===t.type&&(f.clickEvent=t),a){var u=a._menu;if(e(s).hasClass(d)&&!(t&&("click"===t.type&&/input|textarea/i.test(t.target.tagName)||"keyup"===t.type&&9===t.which)&&e.contains(s,t.target))){var c=e.Event(p.HIDE,f);e(s).trigger(c),c.isDefaultPrevented()||("ontouchstart"in document.documentElement&&e(document.body).children().off("mouseover",null,e.noop),n[r].setAttribute("aria-expanded","false"),a._popper&&a._popper.destroy(),e(u).removeClass(d),e(s).removeClass(d).trigger(e.Event(p.HIDDEN,f)))}}}},i._getParentFromElement=function(e){var t,r=n.getSelectorFromElement(e);return r&&(t=document.querySelector(r)),t||e.parentNode},i._dataApiKeydownHandler=function(t){if((/input|textarea/i.test(t.target.tagName)?!(32===t.which||27!==t.which&&(40!==t.which&&38!==t.which||e(t.target).closest(P).length)):c.test(t.which))&&(t.preventDefault(),t.stopPropagation(),!this.disabled&&!e(this).hasClass(h))){var n=i._getParentFromElement(this),r=e(n).hasClass(d);if(r||27!==t.which)if(r&&(!r||27!==t.which&&32!==t.which)){var o=[].slice.call(n.querySelectorAll(E)).filter((function(t){return e(t).is(":visible")}));if(0!==o.length){var s=o.indexOf(t.target);38===t.which&&s>0&&s--,40===t.which&&s<o.length-1&&s++,s<0&&(s=0),o[s].focus()}}else{if(27===t.which){var a=n.querySelector(b);e(a).trigger("focus")}e(this).trigger("click")}}},o=i,w=[{key:"VERSION",get:function(){return"4.4.1"}},{key:"Default",get:function(){return k}},{key:"DefaultType",get:function(){return T}}],(u=null)&&r(o.prototype,u),w&&r(o,w),i}();return e(document).on(p.KEYDOWN_DATA_API,b,K._dataApiKeydownHandler).on(p.KEYDOWN_DATA_API,P,K._dataApiKeydownHandler).on(p.CLICK_DATA_API+" "+p.KEYUP_DATA_API,K._clearMenus).on(p.CLICK_DATA_API,b,(function(t){t.preventDefault(),t.stopPropagation(),K._jQueryInterface.call(e(this),"toggle")})).on(p.CLICK_DATA_API,w,(function(e){e.stopPropagation()})),e.fn[a]=K._jQueryInterface,e.fn[a].Constructor=K,e.fn[a].noConflict=function(){return e.fn[a]=u,K._jQueryInterface},K}));