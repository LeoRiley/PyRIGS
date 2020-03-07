!function(h){"use strict";var r=function(t,i){this.options=h.extend({},r.DEFAULTS,i),this.$target=h(this.options.target).on("scroll.bs.affix.data-api",h.proxy(this.checkPosition,this)).on("click.bs.affix.data-api",h.proxy(this.checkPositionWithEventLoop,this)),this.$element=h(t),this.affixed=null,this.unpin=null,this.pinnedOffset=null,this.checkPosition()};function e(o){return this.each(function(){var t=h(this),i=t.data("bs.affix"),e="object"==typeof o&&o;i||t.data("bs.affix",i=new r(this,e)),"string"==typeof o&&i[o]()})}r.VERSION="3.3.7",r.RESET="affix affix-top affix-bottom",r.DEFAULTS={offset:0,target:window},r.prototype.getState=function(t,i,e,o){var f=this.$target.scrollTop(),n=this.$element.offset(),s=this.$target.height();if(null!=e&&"top"==this.affixed)return f<e&&"top";if("bottom"==this.affixed)return null!=e?!(f+this.unpin<=n.top)&&"bottom":!(f+s<=t-o)&&"bottom";var a=null==this.affixed,h=a?f:n.top;return null!=e&&f<=e?"top":null!=o&&t-o<=h+(a?s:i)&&"bottom"},r.prototype.getPinnedOffset=function(){if(this.pinnedOffset)return this.pinnedOffset;this.$element.removeClass(r.RESET).addClass("affix");var t=this.$target.scrollTop(),i=this.$element.offset();return this.pinnedOffset=i.top-t},r.prototype.checkPositionWithEventLoop=function(){setTimeout(h.proxy(this.checkPosition,this),1)},r.prototype.checkPosition=function(){if(this.$element.is(":visible")){var t=this.$element.height(),i=this.options.offset,e=i.top,o=i.bottom,f=Math.max(h(document).height(),h(document.body).height());"object"!=typeof i&&(o=e=i),"function"==typeof e&&(e=i.top(this.$element)),"function"==typeof o&&(o=i.bottom(this.$element));var n=this.getState(f,t,e,o);if(this.affixed!=n){null!=this.unpin&&this.$element.css("top","");var s="affix"+(n?"-"+n:""),a=h.Event(s+".bs.affix");if(this.$element.trigger(a),a.isDefaultPrevented())return;this.affixed=n,this.unpin="bottom"==n?this.getPinnedOffset():null,this.$element.removeClass(r.RESET).addClass(s).trigger(s.replace("affix","affixed")+".bs.affix")}"bottom"==n&&this.$element.offset({top:f-t-o})}};var t=h.fn.affix;h.fn.affix=e,h.fn.affix.Constructor=r,h.fn.affix.noConflict=function(){return h.fn.affix=t,this},h(window).on("load",function(){h('[data-spy="affix"]').each(function(){var t=h(this),i=t.data();i.offset=i.offset||{},null!=i.offsetBottom&&(i.offset.bottom=i.offsetBottom),null!=i.offsetTop&&(i.offset.top=i.offsetTop),e.call(t,i)})})}(jQuery);