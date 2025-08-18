// Polyfills para compatibilidade com navegadores móveis antigos

// Polyfill para Array.from (IE/Safari antigo)
if (!Array.from) {
  Array.from = function(arrayLike: any, mapFn?: any, thisArg?: any) {
    const C = this;
    const items = Object(arrayLike);
    if (arrayLike == null) {
      throw new TypeError('Array.from requires an array-like object - not null or undefined');
    }
    const mapFunction = mapFn === undefined ? undefined : mapFn;
    if (typeof mapFunction !== 'undefined' && typeof mapFunction !== 'function') {
      throw new TypeError('Array.from: when provided, the second argument must be a function');
    }
    const len = parseInt(items.length) || 0;
    const result = typeof C === 'function' ? Object(new C(len)) : new Array(len);
    let k = 0;
    while (k < len) {
      const kValue = items[k];
      if (mapFunction) {
        result[k] = typeof thisArg === 'undefined' ? mapFunction(kValue, k) : mapFunction.call(thisArg, kValue, k);
      } else {
        result[k] = kValue;
      }
      k++;
    }
    result.length = len;
    return result;
  };
}

// Polyfill para Object.assign (IE)
if (typeof Object.assign !== 'function') {
  Object.assign = function(target: any, ...sources: any[]) {
    if (target == null) {
      throw new TypeError('Cannot convert undefined or null to object');
    }
    const to = Object(target);
    for (let index = 0; index < sources.length; index++) {
      const nextSource = sources[index];
      if (nextSource != null) {
        for (const nextKey in nextSource) {
          if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
            to[nextKey] = nextSource[nextKey];
          }
        }
      }
    }
    return to;
  };
}

// Polyfill para Promise (IE/Android antigo)
if (typeof Promise === 'undefined') {
  (window as any).Promise = class Promise {
    private state: 'pending' | 'fulfilled' | 'rejected' = 'pending';
    private value: any;
    private handlers: Array<{ onFulfilled?: Function; onRejected?: Function; resolve: Function; reject: Function }> = [];

    constructor(executor: (resolve: Function, reject: Function) => void) {
      try {
        executor(this.resolve.bind(this), this.reject.bind(this));
      } catch (error) {
        this.reject(error);
      }
    }

    private resolve(value: any) {
      if (this.state === 'pending') {
        this.state = 'fulfilled';
        this.value = value;
        this.handlers.forEach(this.handle.bind(this));
        this.handlers = [];
      }
    }

    private reject(reason: any) {
      if (this.state === 'pending') {
        this.state = 'rejected';
        this.value = reason;
        this.handlers.forEach(this.handle.bind(this));
        this.handlers = [];
      }
    }

    private handle(handler: any) {
      if (this.state === 'pending') {
        this.handlers.push(handler);
      } else {
        if (this.state === 'fulfilled' && typeof handler.onFulfilled === 'function') {
          handler.onFulfilled(this.value);
        }
        if (this.state === 'rejected' && typeof handler.onRejected === 'function') {
          handler.onRejected(this.value);
        }
      }
    }

    then(onFulfilled?: Function, onRejected?: Function) {
      return new Promise((resolve, reject) => {
        this.handle({
          onFulfilled: (value: any) => {
            if (!onFulfilled) {
              resolve(value);
            } else {
              try {
                resolve(onFulfilled(value));
              } catch (error) {
                reject(error);
              }
            }
          },
          onRejected: (reason: any) => {
            if (!onRejected) {
              reject(reason);
            } else {
              try {
                resolve(onRejected(reason));
              } catch (error) {
                reject(error);
              }
            }
          },
          resolve,
          reject
        });
      });
    }

    catch(onRejected: Function) {
      return this.then(undefined, onRejected);
    }

    static resolve(value: any) {
      return new Promise(resolve => resolve(value));
    }

    static reject(reason: any) {
      return new Promise((_, reject) => reject(reason));
    }
  };
}

// Polyfill para fetch (IE/Android antigo)
if (!window.fetch) {
  (window as any).fetch = function(url: string, options: any = {}) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const method = options.method || 'GET';
      
      xhr.open(method, url);
      
      // Set headers
      if (options.headers) {
        Object.keys(options.headers).forEach(key => {
          xhr.setRequestHeader(key, options.headers[key]);
        });
      }
      
      xhr.onload = () => {
        const response = {
          ok: xhr.status >= 200 && xhr.status < 300,
          status: xhr.status,
          statusText: xhr.statusText,
          json: () => Promise.resolve(JSON.parse(xhr.responseText)),
          text: () => Promise.resolve(xhr.responseText),
          blob: () => Promise.resolve(new Blob([xhr.response])),
          headers: {
            get: (name: string) => xhr.getResponseHeader(name)
          }
        };
        resolve(response);
      };
      
      xhr.onerror = () => reject(new Error('Network error'));
      xhr.ontimeout = () => reject(new Error('Request timeout'));
      
      if (options.timeout) {
        xhr.timeout = options.timeout;
      }
      
      xhr.send(options.body || null);
    });
  };
}

// Polyfill para requestAnimationFrame
if (!window.requestAnimationFrame) {
  (window as any).requestAnimationFrame = function(callback: FrameRequestCallback) {
    return setTimeout(callback, 1000 / 60);
  };
}

if (!window.cancelAnimationFrame) {
  (window as any).cancelAnimationFrame = function(id: number) {
    clearTimeout(id);
  };
}

// Polyfill para classList (IE antigo)
if (!('classList' in document.createElement('_'))) {
  (function(view: any) {
    if (!('Element' in view)) return;
    
    const classListProp = 'classList';
    const protoProp = 'prototype';
    const elemCtrProto = view.Element[protoProp];
    const objCtr = Object;
    const strTrim = String[protoProp].trim || function() {
      return this.replace(/^\s+|\s+$/g, '');
    };
    
    const arrIndexOf = Array[protoProp].indexOf || function(item: any) {
      let i = 0;
      const len = this.length;
      for (; i < len; i++) {
        if (i in this && this[i] === item) {
          return i;
        }
      }
      return -1;
    };
    
    const DOMTokenList = function(el: Element) {
      this.el = el;
      const classes = el.className.replace(/^\s+|\s+$/g, '').split(/\s+/);
      for (let i = 0; i < classes.length; i++) {
        this.push(classes[i]);
      }
      this._updateClassName = function() {
        el.className = this.toString();
      };
    };
    
    const dtp = DOMTokenList[protoProp] = [];
    
    dtp.item = function(i: number) {
      return this[i] || null;
    };
    
    dtp.contains = function(token: string) {
      token += '';
      return arrIndexOf.call(this, token) !== -1;
    };
    
    dtp.add = function() {
      const tokens = arguments;
      let i = 0;
      const l = tokens.length;
      let token;
      let updated = false;
      do {
        token = tokens[i] + '';
        if (arrIndexOf.call(this, token) === -1) {
          this.push(token);
          updated = true;
        }
      } while (++i < l);
      
      if (updated) {
        this._updateClassName();
      }
    };
    
    dtp.remove = function() {
      const tokens = arguments;
      let i = 0;
      const l = tokens.length;
      let token;
      let updated = false;
      let index;
      do {
        token = tokens[i] + '';
        index = arrIndexOf.call(this, token);
        while (index !== -1) {
          this.splice(index, 1);
          updated = true;
          index = arrIndexOf.call(this, token);
        }
      } while (++i < l);
      
      if (updated) {
        this._updateClassName();
      }
    };
    
    dtp.toggle = function(token: string, force?: boolean) {
      token += '';
      const result = this.contains(token);
      const method = result ? force !== true && 'remove' : force !== false && 'add';
      
      if (method) {
        this[method](token);
      }
      
      if (force === true || force === false) {
        return force;
      } else {
        return !result;
      }
    };
    
    dtp.toString = function() {
      return this.join(' ');
    };
    
    if (objCtr.defineProperty) {
      const dtp2 = {
        get: function() {
          return new DOMTokenList(this);
        },
        enumerable: true,
        configurable: true
      };
      try {
        objCtr.defineProperty(elemCtrProto, classListProp, dtp2);
      } catch (ex) {
        if (ex.number === -0x7FF5EC54) {
          dtp2.enumerable = false;
          objCtr.defineProperty(elemCtrProto, classListProp, dtp2);
        }
      }
    } else if (objCtr[protoProp].__defineGetter__) {
      elemCtrProto.__defineGetter__(classListProp, dtp2.get);
    }
  })(window);
}

// Polyfill para addEventListener (IE8)
if (!Element.prototype.addEventListener) {
  (Element.prototype as any).addEventListener = function(type: string, listener: EventListener) {
    (this as any).attachEvent('on' + type, listener);
  };
}

if (!Element.prototype.removeEventListener) {
  (Element.prototype as any).removeEventListener = function(type: string, listener: EventListener) {
    (this as any).detachEvent('on' + type, listener);
  };
}

// Polyfill para console (IE antigo)
if (!window.console) {
  (window as any).console = {
    log: function() {},
    warn: function() {},
    error: function() {},
    info: function() {},
    debug: function() {},
    trace: function() {},
    group: function() {},
    groupEnd: function() {},
    time: function() {},
    timeEnd: function() {},
    clear: function() {}
  };
}

// Polyfill para String.prototype.includes
if (!String.prototype.includes) {
  String.prototype.includes = function(search: string, start?: number) {
    if (typeof start !== 'number') {
      start = 0;
    }
    
    if (start + search.length > this.length) {
      return false;
    } else {
      return this.indexOf(search, start) !== -1;
    }
  };
}

// Polyfill para Array.prototype.includes
if (!Array.prototype.includes) {
  Array.prototype.includes = function(searchElement: any, fromIndex?: number) {
    return this.indexOf(searchElement, fromIndex) !== -1;
  };
}

// Polyfill para Array.prototype.find
if (!Array.prototype.find) {
  Array.prototype.find = function(predicate: (value: any, index: number, obj: any[]) => boolean) {
    if (this == null) {
      throw new TypeError('Array.prototype.find called on null or undefined');
    }
    if (typeof predicate !== 'function') {
      throw new TypeError('predicate must be a function');
    }
    const list = Object(this);
    const length = parseInt(list.length) || 0;
    const thisArg = arguments[1];
    for (let i = 0; i < length; i++) {
      const element = list[i];
      if (predicate.call(thisArg, element, i, list)) {
        return element;
      }
    }
    return undefined;
  };
}

// Polyfill para Array.prototype.findIndex
if (!Array.prototype.findIndex) {
  Array.prototype.findIndex = function(predicate: (value: any, index: number, obj: any[]) => boolean) {
    if (this == null) {
      throw new TypeError('Array.prototype.findIndex called on null or undefined');
    }
    if (typeof predicate !== 'function') {
      throw new TypeError('predicate must be a function');
    }
    const list = Object(this);
    const length = parseInt(list.length) || 0;
    const thisArg = arguments[1];
    for (let i = 0; i < length; i++) {
      const element = list[i];
      if (predicate.call(thisArg, element, i, list)) {
        return i;
      }
    }
    return -1;
  };
}

// Polyfill para Number.isNaN
if (!Number.isNaN) {
  Number.isNaN = function(value: any) {
    return typeof value === 'number' && isNaN(value);
  };
}

// Polyfill para Number.isFinite
if (!Number.isFinite) {
  Number.isFinite = function(value: any) {
    return typeof value === 'number' && isFinite(value);
  };
}

// Função para inicializar todos os polyfills
export const initPolyfills = (): void => {
  // Os polyfills são executados automaticamente quando o módulo é importado
  console.log('Polyfills inicializados para compatibilidade mobile');
};

// Função para verificar suporte a funcionalidades
export const checkFeatureSupport = (): { [key: string]: boolean } => {
  return {
    fetch: typeof fetch !== 'undefined',
    promise: typeof Promise !== 'undefined',
    arrayFrom: typeof Array.from !== 'undefined',
    objectAssign: typeof Object.assign !== 'undefined',
    classList: 'classList' in document.createElement('div'),
    addEventListener: 'addEventListener' in document.createElement('div'),
    requestAnimationFrame: typeof requestAnimationFrame !== 'undefined',
    console: typeof console !== 'undefined',
    stringIncludes: typeof String.prototype.includes !== 'undefined',
    arrayIncludes: typeof Array.prototype.includes !== 'undefined',
    arrayFind: typeof Array.prototype.find !== 'undefined',
    numberIsNaN: typeof Number.isNaN !== 'undefined',
    touchEvents: 'ontouchstart' in window,
    geolocation: 'geolocation' in navigator,
    localStorage: (() => {
      try {
        return 'localStorage' in window && window.localStorage !== null;
      } catch (e) {
        return false;
      }
    })()
  };
};

export default initPolyfills;