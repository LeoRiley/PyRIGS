/*!
  * Bootstrap alert.js v4.4.1 (https://getbootstrap.com/)
  * Copyright 2011-2019 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t(require("jquery"),require("./util.js")):"function"==typeof define&&define.amd?define(["jquery","./util.js"],t):(e=e||self).Alert=t(e.jQuery,e.Util)}(this,(function(e,t){"use strict";function n(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}e=e&&e.hasOwnProperty("default")?e.default:e,t=t&&t.hasOwnProperty("default")?t.default:t;var r=e.fn.alert,o={CLOSE:"close.bs.alert",CLOSED:"closed.bs.alert",CLICK_DATA_API:"click.bs.alert.data-api"},i="alert",l="fade",s="show",a=function(){function r(e){this._element=e}var a,u,f,c=r.prototype;return c.close=function(e){var t=this._element;e&&(t=this._getRootElement(e)),this._triggerCloseEvent(t).isDefaultPrevented()||this._removeElement(t)},c.dispose=function(){e.removeData(this._element,"bs.alert"),this._element=null},c._getRootElement=function(n){var r=t.getSelectorFromElement(n),o=!1;return r&&(o=document.querySelector(r)),o||(o=e(n).closest("."+i)[0]),o},c._triggerCloseEvent=function(t){var n=e.Event(o.CLOSE);return e(t).trigger(n),n},c._removeElement=function(n){var r=this;if(e(n).removeClass(s),e(n).hasClass(l)){var o=t.getTransitionDurationFromElement(n);e(n).one(t.TRANSITION_END,(function(e){return r._destroyElement(n,e)})).emulateTransitionEnd(o)}else this._destroyElement(n)},c._destroyElement=function(t){e(t).detach().trigger(o.CLOSED).remove()},r._jQueryInterface=function(t){return this.each((function(){var n=e(this),o=n.data("bs.alert");o||(o=new r(this),n.data("bs.alert",o)),"close"===t&&o[t](this)}))},r._handleDismiss=function(e){return function(t){t&&t.preventDefault(),e.close(this)}},a=r,f=[{key:"VERSION",get:function(){return"4.4.1"}}],(u=null)&&n(a.prototype,u),f&&n(a,f),r}();return e(document).on(o.CLICK_DATA_API,'[data-dismiss="alert"]',a._handleDismiss(new a)),e.fn.alert=a._jQueryInterface,e.fn.alert.Constructor=a,e.fn.alert.noConflict=function(){return e.fn.alert=r,a._jQueryInterface},a}));