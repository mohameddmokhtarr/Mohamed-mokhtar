(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{"34Gh":function(e,t,n){"use strict";var o=n("dI71"),r=n("q1tI"),i=n.n(r),a=n("aJ3L"),l=n("00sx"),c=n("/MKj"),s=(n("Ux6t"),n("Wbzz")),u=n("Z3Vw"),p=n("vvFL"),f=n("aqT/"),m=n.n(f),h=function(e){function t(){for(var t,n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return(t=e.call.apply(e,[this].concat(o))||this).state={},t}return Object(o.a)(t,e),t.prototype.render=function(){var e=this,t=this.props.data,o=[{name:"Instagram",img:n("Zx6i"),img2x:n("NAo6"),svg:i.a.createElement(p.b,{theme:"white"}),link:t.instagramUrl},{name:"Facebook",img:n("AUhx"),img2x:n("5W7k"),svg:i.a.createElement(p.a,{theme:"white"}),link:t.facebookUrl},{name:"Twitter",img:n("U/Uh"),img2x:n("Lk4n"),svg:i.a.createElement(p.d,{theme:"white"}),link:t.twitterUrl},{name:"LinkedIn",img:n("MGm6"),img2x:n("cN5Q"),svg:i.a.createElement(p.c,{theme:"white"}),link:t.linkedInUrl}];return i.a.createElement(m.a,{minTopValue:"300",partialVisibility:!0},(function(n){return n.isVisible?e.props.hideMark():e.props.showMark(),i.a.createElement("footer",null,i.a.createElement("div",{className:"content-container footer-content"},i.a.createElement("div",{className:"footer-left column"},i.a.createElement("div",{className:"symbol-container"},i.a.createElement(l.a,{to:"/"},i.a.createElement(u.l,null))),i.a.createElement("div",{className:"catchphrase color-white"},t.catchphrase),i.a.createElement("ul",{className:"sns-links"},o.map((function(e){var t=e.svg,n=e.link,o=e.name;return i.a.createElement("li",{key:o},i.a.createElement(a.a,{href:n,target:"_blank",rel:"noopener noreferrer",className:"link"},i.a.createElement("div",{className:"link"},t)))})))),i.a.createElement("div",{className:"footer-right column"},i.a.createElement("div",{className:"title"},i.a.createElement("h3",{className:"type-comp1 color-white"},"Get in touch")),i.a.createElement("div",{className:"links contact"},i.a.createElement(a.a,{href:"mailto:"+t.generalEmail,className:"type-sub3 color-red link-underline email"},t.generalEmail),i.a.createElement(a.a,{href:"tel:"+t.phone,className:"type-sub3 color-red link-underline tel"},t.phone)),i.a.createElement("div",{className:"title last"},i.a.createElement("h3",{className:"type-comp1 color-white"},"Explore")),i.a.createElement("nav",{className:"links type-sub3 "},i.a.createElement("ul",{className:"footer-menu"},i.a.createElement("li",null,i.a.createElement(l.a,{to:"/work"},"Work")),i.a.createElement("li",null,i.a.createElement(l.a,{to:"/services"},"Services")),i.a.createElement("li",null,i.a.createElement(l.a,{to:"/about"},"About")),i.a.createElement("li",null,i.a.createElement(l.a,{to:"/careers"},"Careers")),i.a.createElement("li",null,i.a.createElement(l.a,{to:"/blog"},"Insights")),i.a.createElement("li",null,i.a.createElement(l.a,{to:"/lets-talk"},"Contact")))),i.a.createElement("div",{className:"info type-sub3 address"},t.address))))}))},t}(r.Component);t.a=function(e){return i.a.createElement(s.b,{query:"42194977",render:function(t){return i.a.createElement(b,Object.assign({data:t.contentfulDefaultSettings},e))}})};var b=Object(c.b)(null,(function(e){return{hideMark:function(){return e({type:"HIDE_MARK"})},showMark:function(){return e({type:"SHOW_MARK"})}}}))(h)},Ux6t:function(e,t,n){},"aqT/":function(e,t,n){var o;o=function(e,t){return function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}return n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=4)}([function(e,t,n){e.exports=n(5)()},function(t,n){t.exports=e},function(e,n){e.exports=t},function(e,t){e.exports=function(e,t,n){var o=e.direction,r=e.value;switch(o){case"top":return n.top+r<t.top&&n.bottom>t.bottom&&n.left<t.left&&n.right>t.right;case"left":return n.left+r<t.left&&n.bottom>t.bottom&&n.top<t.top&&n.right>t.right;case"bottom":return n.bottom-r>t.bottom&&n.left<t.left&&n.right>t.right&&n.top<t.top;case"right":return n.right-r>t.right&&n.left<t.left&&n.top<t.top&&n.bottom>t.bottom}}},function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return y}));var o=n(1),r=n.n(o),i=n(2),a=n.n(i),l=n(0),c=n.n(l),s=n(3),u=n.n(s);function p(e){return(p="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function f(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function m(e){return(m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function h(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function b(e,t){return(b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function d(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var y=function(e){function t(e){var n,o,r;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),o=this,r=m(t).call(this,e),n=!r||"object"!==p(r)&&"function"!=typeof r?h(o):r,d(h(n),"getContainer",(function(){return n.props.containment||window})),d(h(n),"addEventListener",(function(e,t,o,r){var i;n.debounceCheck||(n.debounceCheck={});var a=function(){i=null,n.check()},l={target:e,fn:r>-1?function(){i||(i=setTimeout(a,r||0))}:function(){clearTimeout(i),i=setTimeout(a,o||0)},getLastTimeout:function(){return i}};e.addEventListener(t,l.fn),n.debounceCheck[t]=l})),d(h(n),"startWatching",(function(){n.debounceCheck||n.interval||(n.props.intervalCheck&&(n.interval=setInterval(n.check,n.props.intervalDelay)),n.props.scrollCheck&&n.addEventListener(n.getContainer(),"scroll",n.props.scrollDelay,n.props.scrollThrottle),n.props.resizeCheck&&n.addEventListener(window,"resize",n.props.resizeDelay,n.props.resizeThrottle),!n.props.delayedCall&&n.check())})),d(h(n),"stopWatching",(function(){if(n.debounceCheck)for(var e in n.debounceCheck)if(n.debounceCheck.hasOwnProperty(e)){var t=n.debounceCheck[e];clearTimeout(t.getLastTimeout()),t.target.removeEventListener(e,t.fn),n.debounceCheck[e]=null}n.debounceCheck=null,n.interval&&(n.interval=clearInterval(n.interval))})),d(h(n),"check",(function(){var e,t,o=n.node;if(!o)return n.state;if(e=function(e){return void 0===e.width&&(e.width=e.right-e.left),void 0===e.height&&(e.height=e.bottom-e.top),e}(n.roundRectDown(o.getBoundingClientRect())),n.props.containment){var r=n.props.containment.getBoundingClientRect();t={top:r.top,left:r.left,bottom:r.bottom,right:r.right}}else t={top:0,left:0,bottom:window.innerHeight||document.documentElement.clientHeight,right:window.innerWidth||document.documentElement.clientWidth};var i=n.props.offset||{};"object"===p(i)&&(t.top+=i.top||0,t.left+=i.left||0,t.bottom-=i.bottom||0,t.right-=i.right||0);var a={top:e.top>=t.top,left:e.left>=t.left,bottom:e.bottom<=t.bottom,right:e.right<=t.right},l=e.height>0&&e.width>0,c=l&&a.top&&a.left&&a.bottom&&a.right;if(l&&n.props.partialVisibility){var s=e.top<=t.bottom&&e.bottom>=t.top&&e.left<=t.right&&e.right>=t.left;"string"==typeof n.props.partialVisibility&&(s=a[n.props.partialVisibility]),c=n.props.minTopValue?s&&e.top<=t.bottom-n.props.minTopValue:s}"string"==typeof i.direction&&"number"==typeof i.value&&(console.warn("[notice] offset.direction and offset.value have been deprecated. They still work for now, but will be removed in next major version. Please upgrade to the new syntax: { %s: %d }",i.direction,i.value),c=u()(i,e,t));var f=n.state;return n.state.isVisible!==c&&(f={isVisible:c,visibilityRect:a},n.setState(f),n.props.onChange&&n.props.onChange(c)),f})),n.state={isVisible:null,visibilityRect:{}},n}var n,o,i;return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(t,e),n=t,(o=[{key:"componentDidMount",value:function(){this.node=a.a.findDOMNode(this),this.props.active&&this.startWatching()}},{key:"componentWillUnmount",value:function(){this.stopWatching()}},{key:"componentDidUpdate",value:function(e){this.node=a.a.findDOMNode(this),this.props.active&&!e.active?(this.setState({isVisible:null,visibilityRect:{}}),this.startWatching()):this.props.active||this.stopWatching()}},{key:"roundRectDown",value:function(e){return{top:Math.floor(e.top),left:Math.floor(e.left),bottom:Math.floor(e.bottom),right:Math.floor(e.right)}}},{key:"render",value:function(){return this.props.children instanceof Function?this.props.children({isVisible:this.state.isVisible,visibilityRect:this.state.visibilityRect}):r.a.Children.only(this.props.children)}}])&&f(n.prototype,o),i&&f(n,i),t}(r.a.Component);d(y,"defaultProps",{active:!0,partialVisibility:!1,minTopValue:0,scrollCheck:!1,scrollDelay:250,scrollThrottle:-1,resizeCheck:!1,resizeDelay:250,resizeThrottle:-1,intervalCheck:!0,intervalDelay:100,delayedCall:!1,offset:{},containment:null,children:r.a.createElement("span",null)}),d(y,"propTypes",{onChange:c.a.func,active:c.a.bool,partialVisibility:c.a.oneOfType([c.a.bool,c.a.oneOf(["top","right","bottom","left"])]),delayedCall:c.a.bool,offset:c.a.oneOfType([c.a.shape({top:c.a.number,left:c.a.number,bottom:c.a.number,right:c.a.number}),c.a.shape({direction:c.a.oneOf(["top","right","bottom","left"]),value:c.a.number})]),scrollCheck:c.a.bool,scrollDelay:c.a.number,scrollThrottle:c.a.number,resizeCheck:c.a.bool,resizeDelay:c.a.number,resizeThrottle:c.a.number,intervalCheck:c.a.bool,intervalDelay:c.a.number,containment:"undefined"!=typeof window?c.a.instanceOf(window.Element):c.a.any,children:c.a.oneOfType([c.a.element,c.a.func]),minTopValue:c.a.number})},function(e,t,n){"use strict";var o=n(6);function r(){}function i(){}i.resetWarningCache=r,e.exports=function(){function e(e,t,n,r,i,a){if(a!==o){var l=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw l.name="Invariant Violation",l}}function t(){return e}e.isRequired=e;var n={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:i,resetWarningCache:r};return n.PropTypes=n,n}},function(e,t,n){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"}])},e.exports=o(n("q1tI"),n("i8i4"))}}]);
//# sourceMappingURL=d22ee007cf8220d7eff64837704a05445512d3f4-515725c96f70d5317ab1.js.map