// Otimizações específicas para dispositivos móveis

import { MobileDebugger } from './mobileDetection';

// Debounce function para evitar chamadas excessivas
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  immediate?: boolean
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null;
  
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };
    
    const callNow = immediate && !timeout;
    
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    
    if (callNow) func(...args);
  };
};

// Throttle function para limitar frequência de execução
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  
  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// Lazy loading para imagens
export const setupLazyLoading = (): void => {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          const src = img.dataset.src;
          if (src) {
            img.src = src;
            img.classList.remove('lazy');
            observer.unobserve(img);
            MobileDebugger.log('Imagem carregada via lazy loading', { src });
          }
        }
      });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  } else {
    // Fallback para navegadores sem IntersectionObserver
    document.querySelectorAll('img[data-src]').forEach(img => {
      const imgElement = img as HTMLImageElement;
      const src = imgElement.dataset.src;
      if (src) {
        imgElement.src = src;
      }
    });
  }
};

// Otimização de scroll para mobile
export const optimizeScrolling = (): void => {
  // Adiciona CSS para scroll suave em mobile
  const style = document.createElement('style');
  style.textContent = `
    * {
      -webkit-overflow-scrolling: touch;
    }
    
    body {
      overscroll-behavior: contain;
    }
    
    @media (max-width: 768px) {
      * {
        scroll-behavior: smooth;
      }
    }
  `;
  document.head.appendChild(style);
  
  MobileDebugger.log('Otimizações de scroll aplicadas');
};

// Preload de recursos críticos
export const preloadCriticalResources = (): void => {
  const criticalResources = [
    // Adicione aqui URLs de recursos críticos
  ];
  
  criticalResources.forEach(url => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = url;
    link.as = 'fetch';
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
  });
  
  if (criticalResources.length > 0) {
    MobileDebugger.log('Recursos críticos precarregados', { count: criticalResources.length });
  }
};

// Otimização de touch events
export const optimizeTouchEvents = (): void => {
  // Adiciona passive listeners para melhor performance
  const addPassiveListener = (element: Element, event: string, handler: EventListener) => {
    element.addEventListener(event, handler, { passive: true });
  };
  
  // Otimiza eventos de touch comuns
  document.addEventListener('touchstart', () => {}, { passive: true });
  document.addEventListener('touchmove', () => {}, { passive: true });
  document.addEventListener('touchend', () => {}, { passive: true });
  
  MobileDebugger.log('Touch events otimizados');
};

// Gerenciamento de memória para mobile
export class MobileMemoryManager {
  private static cache = new Map<string, any>();
  private static maxCacheSize = 50; // Limite menor para mobile
  
  static set(key: string, value: any): void {
    if (this.cache.size >= this.maxCacheSize) {
      // Remove o item mais antigo
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
      MobileDebugger.log('Cache limpo por limite de memória', { removedKey: firstKey });
    }
    
    this.cache.set(key, value);
  }
  
  static get(key: string): any {
    return this.cache.get(key);
  }
  
  static clear(): void {
    this.cache.clear();
    MobileDebugger.log('Cache completamente limpo');
  }
  
  static getSize(): number {
    return this.cache.size;
  }
  
  // Limpa cache automaticamente quando memória está baixa
  static setupMemoryPressureHandling(): void {
    if ('memory' in performance) {
      const checkMemory = () => {
        const memInfo = (performance as any).memory;
        const usedPercent = (memInfo.usedJSHeapSize / memInfo.jsHeapSizeLimit) * 100;
        
        if (usedPercent > 80) {
          this.clear();
          MobileDebugger.log('Cache limpo por pressão de memória', { usedPercent });
        }
      };
      
      setInterval(checkMemory, 30000); // Verifica a cada 30 segundos
    }
  }
}

// Otimização de renderização para mobile
export const optimizeRendering = (): void => {
  // Reduz a frequência de repaint/reflow
  const style = document.createElement('style');
  style.textContent = `
    @media (max-width: 768px) {
      * {
        will-change: auto;
        transform: translateZ(0);
      }
      
      .animate {
        will-change: transform, opacity;
      }
      
      .animate:not(:hover):not(:focus) {
        will-change: auto;
      }
    }
  `;
  document.head.appendChild(style);
  
  MobileDebugger.log('Otimizações de renderização aplicadas');
};

// Detecção e otimização para conexões lentas
export const optimizeForSlowConnections = (): void => {
  const connection = (navigator as any).connection || 
                    (navigator as any).mozConnection || 
                    (navigator as any).webkitConnection;
  
  if (connection) {
    const isSlowConnection = connection.effectiveType === '2g' || 
                           connection.effectiveType === 'slow-2g' ||
                           connection.downlink < 1;
    
    if (isSlowConnection) {
      // Reduz qualidade de imagens
      document.querySelectorAll('img').forEach(img => {
        if (img.src && !img.dataset.optimized) {
          // Adiciona parâmetros de otimização se a URL suportar
          const url = new URL(img.src, window.location.origin);
          url.searchParams.set('quality', '60');
          url.searchParams.set('format', 'webp');
          img.src = url.toString();
          img.dataset.optimized = 'true';
        }
      });
      
      // Desabilita animações desnecessárias
      const style = document.createElement('style');
      style.textContent = `
        @media (max-width: 768px) {
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
      `;
      document.head.appendChild(style);
      
      MobileDebugger.log('Otimizações para conexão lenta aplicadas', {
        effectiveType: connection.effectiveType,
        downlink: connection.downlink
      });
    }
  }
};

// Otimização de formulários para mobile
export const optimizeForms = (): void => {
  document.querySelectorAll('input, textarea, select').forEach(element => {
    const input = element as HTMLInputElement;
    
    // Adiciona atributos para melhor experiência mobile
    if (input.type === 'email') {
      input.setAttribute('inputmode', 'email');
    } else if (input.type === 'tel') {
      input.setAttribute('inputmode', 'tel');
    } else if (input.type === 'number') {
      input.setAttribute('inputmode', 'numeric');
    }
    
    // Adiciona autocomplete apropriado
    if (input.name.includes('email')) {
      input.setAttribute('autocomplete', 'email');
    } else if (input.name.includes('name')) {
      input.setAttribute('autocomplete', 'name');
    }
    
    // Previne zoom em iOS
    if (input.type === 'text' || input.type === 'email' || input.type === 'password') {
      const currentFontSize = window.getComputedStyle(input).fontSize;
      const fontSize = parseFloat(currentFontSize);
      if (fontSize < 16) {
        input.style.fontSize = '16px';
      }
    }
  });
  
  MobileDebugger.log('Formulários otimizados para mobile');
};

// Função principal para aplicar todas as otimizações
export const applyMobileOptimizations = (): void => {
  MobileDebugger.log('Iniciando otimizações mobile');
  
  // Aplica otimizações básicas
  optimizeScrolling();
  optimizeTouchEvents();
  optimizeRendering();
  optimizeForms();
  
  // Configura gerenciamento de memória
  MobileMemoryManager.setupMemoryPressureHandling();
  
  // Aplica otimizações baseadas na conexão
  optimizeForSlowConnections();
  
  // Configura lazy loading quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupLazyLoading);
  } else {
    setupLazyLoading();
  }
  
  // Precarrega recursos críticos
  preloadCriticalResources();
  
  MobileDebugger.log('Otimizações mobile aplicadas com sucesso');
};

// Hook React para otimizações
export const useMobileOptimizations = () => {
  React.useEffect(() => {
    applyMobileOptimizations();
    
    return () => {
      // Cleanup se necessário
      MobileMemoryManager.clear();
    };
  }, []);
};

// Exporta React para uso no hook
import React from 'react';

export default {
  debounce,
  throttle,
  setupLazyLoading,
  optimizeScrolling,
  optimizeTouchEvents,
  optimizeRendering,
  optimizeForSlowConnections,
  optimizeForms,
  applyMobileOptimizations,
  MobileMemoryManager
};