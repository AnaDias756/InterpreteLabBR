// Polyfills para compatibilidade com navegadores móveis antigos
// Este arquivo garante que funcionalidades modernas funcionem em dispositivos mais antigos

// 1. IntersectionObserver Polyfill - Para lazy loading de imagens
if (!('IntersectionObserver' in window)) {
  // Polyfill simples do IntersectionObserver
  (window as any).IntersectionObserver = class {
    private callback: IntersectionObserverCallback;
    private elements: Set<Element> = new Set();
    public root: Document | Element | null = null;
    public rootMargin: string = '0px';
    public thresholds: ReadonlyArray<number> = [0];
    
    constructor(callback: IntersectionObserverCallback, options?: IntersectionObserverInit) {
      this.callback = callback;
      if (options) {
        this.root = options.root || null;
        this.rootMargin = options.rootMargin || '0px';
        this.thresholds = options.threshold ? 
          (Array.isArray(options.threshold) ? options.threshold : [options.threshold]) : [0];
      }
    }
    
    observe(element: Element): void {
      this.elements.add(element);
      // Simula intersecção imediata para fallback
      setTimeout(() => {
        const entry = {
          target: element,
          isIntersecting: true,
          intersectionRatio: 1,
          boundingClientRect: element.getBoundingClientRect(),
          intersectionRect: element.getBoundingClientRect(),
          rootBounds: null,
          time: Date.now()
        };
        this.callback([entry as IntersectionObserverEntry], this as any);
      }, 100);
    }
    
    unobserve(element: Element): void {
      this.elements.delete(element);
    }
    
    disconnect(): void {
      this.elements.clear();
    }
    
    takeRecords(): IntersectionObserverEntry[] {
      return [];
    }
  };
}

// 2. ResizeObserver Polyfill - Para detecção de mudanças de tamanho
if (!('ResizeObserver' in window)) {
  (window as any).ResizeObserver = class {
    private callback: ResizeObserverCallback;
    private elements: Set<Element> = new Set();
    private resizeHandler: () => void;
    
    constructor(callback: ResizeObserverCallback) {
      this.callback = callback;
      this.resizeHandler = () => {
        const entries: ResizeObserverEntry[] = [];
        this.elements.forEach(element => {
          const rect = element.getBoundingClientRect();
          entries.push({
            target: element,
            contentRect: rect,
            borderBoxSize: [{ inlineSize: rect.width, blockSize: rect.height }],
            contentBoxSize: [{ inlineSize: rect.width, blockSize: rect.height }],
            devicePixelContentBoxSize: [{ inlineSize: rect.width, blockSize: rect.height }]
          } as ResizeObserverEntry);
        });
        if (entries.length > 0) {
          this.callback(entries, this);
        }
      };
    }
    
    observe(element: Element): void {
      if (this.elements.size === 0) {
        window.addEventListener('resize', this.resizeHandler);
      }
      this.elements.add(element);
    }
    
    unobserve(element: Element): void {
      this.elements.delete(element);
      if (this.elements.size === 0) {
        window.removeEventListener('resize', this.resizeHandler);
      }
    }
    
    disconnect(): void {
      this.elements.clear();
      window.removeEventListener('resize', this.resizeHandler);
    }
  };
}

// 3. Array.from Polyfill - Para suporte a conversão de array-like objects
if (!Array.from) {
  Array.from = function<T>(arrayLike: ArrayLike<T>, mapFn?: (v: T, k: number) => any): any[] {
    const result: any[] = [];
    const length = arrayLike.length;
    
    for (let i = 0; i < length; i++) {
      const value = arrayLike[i];
      result[i] = mapFn ? mapFn(value, i) : value;
    }
    
    return result;
  };
}

// 4. Object.assign Polyfill - Para merge de objetos
if (!Object.assign) {
  Object.assign = function(target: any, ...sources: any[]): any {
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

// 5. Promise Polyfill - Para suporte a promises em navegadores antigos
if (!window.Promise) {
  // Polyfill básico de Promise
  (window as any).Promise = class {
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
    
    private resolve(value: any): void {
      if (this.state === 'pending') {
        this.state = 'fulfilled';
        this.value = value;
        this.handlers.forEach(handler => this.handle(handler));
        this.handlers = [];
      }
    }
    
    private reject(reason: any): void {
      if (this.state === 'pending') {
        this.state = 'rejected';
        this.value = reason;
        this.handlers.forEach(handler => this.handle(handler));
        this.handlers = [];
      }
    }
    
    private handle(handler: any): void {
      if (this.state === 'pending') {
        this.handlers.push(handler);
      } else {
        setTimeout(() => {
          const callback = this.state === 'fulfilled' ? handler.onFulfilled : handler.onRejected;
          if (callback) {
            try {
              const result = callback(this.value);
              handler.resolve(result);
            } catch (error) {
              handler.reject(error);
            }
          } else {
            if (this.state === 'fulfilled') {
              handler.resolve(this.value);
            } else {
              handler.reject(this.value);
            }
          }
        }, 0);
      }
    }
    
    then(onFulfilled?: Function, onRejected?: Function): any {
      return new (window as any).Promise((resolve: Function, reject: Function) => {
        this.handle({ onFulfilled, onRejected, resolve, reject });
      });
    }
    
    catch(onRejected: Function): any {
      return this.then(undefined, onRejected);
    }
    
    static resolve(value: any): any {
      return new (window as any).Promise((resolve: Function) => resolve(value));
    }
    
    static reject(reason: any): any {
      return new (window as any).Promise((resolve: Function, reject: Function) => reject(reason));
    }
  };
}

// 6. Fetch Polyfill - Para requisições HTTP em navegadores antigos
if (!window.fetch) {
  (window as any).fetch = function(url: string, options: any = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const method = options.method || 'GET';
      
      xhr.open(method, url);
      
      // Headers
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
      
      // Timeout
      if (options.timeout) {
        xhr.timeout = options.timeout;
      }
      
      // Send request
      xhr.send(options.body || null);
    });
  };
}

// 7. Map Polyfill - Para suporte a Map em navegadores antigos
if (!window.Map) {
  (window as any).Map = class {
    private items: Array<[any, any]> = [];
    
    constructor(iterable?: Iterable<[any, any]>) {
      if (iterable) {
        Array.from(iterable).forEach((item: [any, any]) => {
          this.set(item[0], item[1]);
        });
      }
    }
    
    set(key: any, value: any): this {
      const index = this.items.findIndex(([k]) => k === key);
      if (index >= 0) {
        this.items[index][1] = value;
      } else {
        this.items.push([key, value]);
      }
      return this;
    }
    
    get(key: any): any {
      const item = this.items.find(([k]) => k === key);
      return item ? item[1] : undefined;
    }
    
    has(key: any): boolean {
      return this.items.some(([k]) => k === key);
    }
    
    delete(key: any): boolean {
      const index = this.items.findIndex(([k]) => k === key);
      if (index >= 0) {
        this.items.splice(index, 1);
        return true;
      }
      return false;
    }
    
    clear(): void {
      this.items = [];
    }
    
    get size(): number {
      return this.items.length;
    }
    
    keys(): IterableIterator<any> {
      let index = 0;
      const items = this.items;
      return {
        [Symbol.iterator]() { return this; },
        next() {
          if (index < items.length) {
            return { value: items[index++][0], done: false };
          }
          return { value: undefined, done: true };
        }
      } as IterableIterator<any>;
    }
    
    values(): IterableIterator<any> {
      let index = 0;
      const items = this.items;
      return {
        [Symbol.iterator]() { return this; },
        next() {
          if (index < items.length) {
            return { value: items[index++][1], done: false };
          }
          return { value: undefined, done: true };
        }
      } as IterableIterator<any>;
    }
    
    entries(): IterableIterator<[any, any]> {
      let index = 0;
      const items = this.items;
      return {
        [Symbol.iterator]() { return this; },
        next() {
          if (index < items.length) {
            return { value: items[index++], done: false };
          }
          return { value: undefined, done: true };
        }
      } as IterableIterator<[any, any]>;
    }
    
    forEach(callback: (value: any, key: any, map: this) => void): void {
      this.items.forEach(([key, value]) => callback(value, key, this));
    }
  };
}

// 8. Set Polyfill - Para suporte a Set em navegadores antigos
if (!window.Set) {
  (window as any).Set = class {
    private items: any[] = [];
    
    constructor(iterable?: Iterable<any>) {
      if (iterable) {
        Array.from(iterable).forEach((value: any) => {
          this.add(value);
        });
      }
    }
    
    add(value: any): this {
      if (!this.has(value)) {
        this.items.push(value);
      }
      return this;
    }
    
    has(value: any): boolean {
      return this.items.includes(value);
    }
    
    delete(value: any): boolean {
      const index = this.items.indexOf(value);
      if (index >= 0) {
        this.items.splice(index, 1);
        return true;
      }
      return false;
    }
    
    clear(): void {
      this.items = [];
    }
    
    get size(): number {
      return this.items.length;
    }
    
    values(): IterableIterator<any> {
      let index = 0;
      const items = this.items;
      return {
        [Symbol.iterator]() { return this; },
        next() {
          if (index < items.length) {
            return { value: items[index++], done: false };
          }
          return { value: undefined, done: true };
        }
      } as IterableIterator<any>;
    }
    
    keys(): IterableIterator<any> {
      return this.values();
    }
    
    entries(): IterableIterator<[any, any]> {
      let index = 0;
      const items = this.items;
      return {
        [Symbol.iterator]() { return this; },
        next() {
          if (index < items.length) {
            const value = items[index++];
            return { value: [value, value], done: false };
          }
          return { value: undefined, done: true };
        }
      } as IterableIterator<[any, any]>;
    }
    
    forEach(callback: (value: any, value2: any, set: this) => void): void {
      this.items.forEach(value => callback(value, value, this));
    }
  };
}

// 9. requestAnimationFrame Polyfill - Para animações suaves
if (!window.requestAnimationFrame) {
  let lastTime = 0;
  (window as any).requestAnimationFrame = function(callback: FrameRequestCallback): number {
    const currTime = new Date().getTime();
    const timeToCall = Math.max(0, 16 - (currTime - lastTime));
    const id = window.setTimeout(() => {
      callback(currTime + timeToCall);
    }, timeToCall);
    lastTime = currTime + timeToCall;
    return id;
  };
}

if (!window.cancelAnimationFrame) {
  (window as any).cancelAnimationFrame = function(id: number): void {
    clearTimeout(id);
  };
}

// 10. CustomEvent Polyfill - Para eventos customizados
if (!window.CustomEvent) {
  (window as any).CustomEvent = function(event: string, params: CustomEventInit = {}): CustomEvent {
    const evt = document.createEvent('CustomEvent');
    evt.initCustomEvent(event, !!params.bubbles, !!params.cancelable, params.detail);
    return evt;
  };
}

// 11. Element.matches Polyfill - Para seletores CSS
if (!Element.prototype.matches) {
  Element.prototype.matches = 
    (Element.prototype as any).matchesSelector ||
    (Element.prototype as any).mozMatchesSelector ||
    (Element.prototype as any).msMatchesSelector ||
    (Element.prototype as any).oMatchesSelector ||
    (Element.prototype as any).webkitMatchesSelector ||
    function(this: Element, s: string): boolean {
      const matches = this.ownerDocument.querySelectorAll(s);
      let i = matches.length;
      while (--i >= 0 && matches.item(i) !== this) {}
      return i > -1;
    };
}

// 12. Element.closest Polyfill - Para navegação DOM
if (!Element.prototype.closest) {
  Element.prototype.closest = function(this: Element, s: string): Element | null {
    let el: Element | null = this;
    do {
      if (el.matches(s)) return el;
      el = el.parentElement || el.parentNode as Element;
    } while (el !== null && el.nodeType === 1);
    return null;
  };
}

// 13. String.prototype.includes Polyfill
if (!String.prototype.includes) {
  // eslint-disable-next-line no-extend-native
  Object.defineProperty(String.prototype, 'includes', {
    value: function(search: string, start: number = 0): boolean {
      if (typeof start !== 'number') {
        start = 0;
      }
      
      if (start + search.length > this.length) {
        return false;
      } else {
        return this.indexOf(search, start) !== -1;
      }
    },
    configurable: true,
    writable: true
  });
}

// 14. String.prototype.startsWith Polyfill
if (!String.prototype.startsWith) {
  // eslint-disable-next-line no-extend-native
  Object.defineProperty(String.prototype, 'startsWith', {
    value: function(search: string, pos: number = 0): boolean {
      return this.substr(pos, search.length) === search;
    },
    configurable: true,
    writable: true
  });
}

// 15. String.prototype.endsWith Polyfill
if (!String.prototype.endsWith) {
  // eslint-disable-next-line no-extend-native
  Object.defineProperty(String.prototype, 'endsWith', {
    value: function(search: string, length?: number): boolean {
      const len = length === undefined || length > this.length ? this.length : length;
      return this.substring(len - search.length, len) === search;
    },
    configurable: true,
    writable: true
  });
}

// Função para verificar suporte a funcionalidades
export const checkFeatureSupport = (): { [key: string]: boolean } => {
  return {
    IntersectionObserver: 'IntersectionObserver' in window,
    ResizeObserver: 'ResizeObserver' in window,
    ArrayFrom: !!Array.from,
    ObjectAssign: !!Object.assign,
    Promise: !!window.Promise,
    fetch: !!window.fetch,
    Map: !!window.Map,
    Set: !!window.Set,
    requestAnimationFrame: !!window.requestAnimationFrame,
    CustomEvent: !!window.CustomEvent,
    ElementMatches: !!Element.prototype.matches,
    ElementClosest: !!Element.prototype.closest,
    StringIncludes: !!String.prototype.includes,
    StringStartsWith: !!String.prototype.startsWith,
    StringEndsWith: !!String.prototype.endsWith
  };
};

// Função para inicializar todos os polyfills
export const initPolyfills = (): void => {
  console.log('🔧 Polyfills carregados para compatibilidade mobile');
  
  // Log dos polyfills aplicados
  const appliedPolyfills: string[] = [];
  
  if (!('IntersectionObserver' in window)) appliedPolyfills.push('IntersectionObserver');
  if (!('ResizeObserver' in window)) appliedPolyfills.push('ResizeObserver');
  if (!Array.from) appliedPolyfills.push('Array.from');
  if (!Object.assign) appliedPolyfills.push('Object.assign');
  if (!window.Promise) appliedPolyfills.push('Promise');
  if (!window.fetch) appliedPolyfills.push('fetch');
  if (!window.Map) appliedPolyfills.push('Map');
  if (!window.Set) appliedPolyfills.push('Set');
  if (!window.requestAnimationFrame) appliedPolyfills.push('requestAnimationFrame');
  if (!window.CustomEvent) appliedPolyfills.push('CustomEvent');
  if (!Element.prototype.matches) appliedPolyfills.push('Element.matches');
  if (!Element.prototype.closest) appliedPolyfills.push('Element.closest');
  if (!String.prototype.includes) appliedPolyfills.push('String.includes');
  if (!String.prototype.startsWith) appliedPolyfills.push('String.startsWith');
  if (!String.prototype.endsWith) appliedPolyfills.push('String.endsWith');
  
  if (appliedPolyfills.length > 0) {
    console.log('📱 Polyfills aplicados:', appliedPolyfills.join(', '));
  } else {
    console.log('✅ Navegador moderno detectado - nenhum polyfill necessário');
  }
};

// Auto-inicialização
initPolyfills();

// Export default para compatibilidade
const polyfills = {
  initPolyfills
};

export default polyfills;