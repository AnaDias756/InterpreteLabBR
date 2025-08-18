// Utilitário para detecção de dispositivos móveis e debugging

export interface DeviceInfo {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  userAgent: string;
  platform: string;
  screenWidth: number;
  screenHeight: number;
  devicePixelRatio: number;
  touchSupport: boolean;
  orientation: string;
  browser: string;
  os: string;
}

export interface NetworkInfo {
  isOnline: boolean;
  connectionType: string;
  effectiveType: string;
  downlink: number;
  rtt: number;
}

// Detecta se é um dispositivo móvel
export const isMobileDevice = (): boolean => {
  const userAgent = navigator.userAgent.toLowerCase();
  const mobileKeywords = [
    'android', 'webos', 'iphone', 'ipad', 'ipod', 'blackberry', 
    'windows phone', 'mobile', 'opera mini', 'iemobile'
  ];
  
  return mobileKeywords.some(keyword => userAgent.includes(keyword)) ||
         /Mobi|Android/i.test(navigator.userAgent) ||
         window.innerWidth <= 768;
};

// Detecta se é um tablet
export const isTabletDevice = (): boolean => {
  const userAgent = navigator.userAgent.toLowerCase();
  const tabletKeywords = ['ipad', 'tablet', 'kindle', 'playbook', 'silk'];
  
  return tabletKeywords.some(keyword => userAgent.includes(keyword)) ||
         (window.innerWidth > 768 && window.innerWidth <= 1024 && 'ontouchstart' in window);
};

// Detecta o navegador
export const detectBrowser = (): string => {
  const userAgent = navigator.userAgent;
  
  if (userAgent.includes('Chrome') && !userAgent.includes('Edg')) return 'Chrome';
  if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) return 'Safari';
  if (userAgent.includes('Firefox')) return 'Firefox';
  if (userAgent.includes('Edg')) return 'Edge';
  if (userAgent.includes('Opera') || userAgent.includes('OPR')) return 'Opera';
  if (userAgent.includes('Samsung')) return 'Samsung Internet';
  
  return 'Unknown';
};

// Detecta o sistema operacional
export const detectOS = (): string => {
  const userAgent = navigator.userAgent;
  
  if (/Android/i.test(userAgent)) return 'Android';
  if (/iPhone|iPad|iPod/i.test(userAgent)) return 'iOS';
  if (/Windows/i.test(userAgent)) return 'Windows';
  if (/Mac/i.test(userAgent)) return 'macOS';
  if (/Linux/i.test(userAgent)) return 'Linux';
  
  return 'Unknown';
};

// Obtém informações completas do dispositivo
export const getDeviceInfo = (): DeviceInfo => {
  const isMobile = isMobileDevice();
  const isTablet = isTabletDevice();
  
  return {
    isMobile,
    isTablet,
    isDesktop: !isMobile && !isTablet,
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    screenWidth: window.screen.width,
    screenHeight: window.screen.height,
    devicePixelRatio: window.devicePixelRatio || 1,
    touchSupport: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
    orientation: window.innerHeight > window.innerWidth ? 'portrait' : 'landscape',
    browser: detectBrowser(),
    os: detectOS()
  };
};

// Obtém informações de rede
export const getNetworkInfo = (): NetworkInfo => {
  const connection = (navigator as any).connection || 
                    (navigator as any).mozConnection || 
                    (navigator as any).webkitConnection;
  
  return {
    isOnline: navigator.onLine,
    connectionType: connection?.type || 'unknown',
    effectiveType: connection?.effectiveType || 'unknown',
    downlink: connection?.downlink || 0,
    rtt: connection?.rtt || 0
  };
};

// Logger específico para mobile debugging
export class MobileDebugger {
  private static logs: string[] = [];
  private static maxLogs = 100;
  
  static log(message: string, data?: any): void {
    const timestamp = new Date().toISOString();
    const deviceInfo = getDeviceInfo();
    const networkInfo = getNetworkInfo();
    
    const logEntry = {
      timestamp,
      message,
      data,
      device: {
        type: deviceInfo.isMobile ? 'mobile' : deviceInfo.isTablet ? 'tablet' : 'desktop',
        browser: deviceInfo.browser,
        os: deviceInfo.os,
        screen: `${deviceInfo.screenWidth}x${deviceInfo.screenHeight}`,
        orientation: deviceInfo.orientation
      },
      network: {
        online: networkInfo.isOnline,
        type: networkInfo.connectionType,
        speed: networkInfo.effectiveType
      }
    };
    
    const logString = JSON.stringify(logEntry, null, 2);
    
    // Adiciona ao array de logs
    this.logs.push(logString);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }
    
    // Log no console
    console.log(`[Mobile Debug] ${message}`, logEntry);
    
    // Tenta enviar para localStorage para debug posterior
    try {
      localStorage.setItem('mobile_debug_logs', JSON.stringify(this.logs));
    } catch (e) {
      console.warn('Não foi possível salvar logs no localStorage:', e);
    }
  }
  
  static getLogs(): string[] {
    return [...this.logs];
  }
  
  static clearLogs(): void {
    this.logs = [];
    try {
      localStorage.removeItem('mobile_debug_logs');
    } catch (e) {
      console.warn('Não foi possível limpar logs do localStorage:', e);
    }
  }
  
  static exportLogs(): string {
    const deviceInfo = getDeviceInfo();
    const networkInfo = getNetworkInfo();
    
    const report = {
      exportDate: new Date().toISOString(),
      deviceInfo,
      networkInfo,
      logs: this.logs
    };
    
    return JSON.stringify(report, null, 2);
  }
}

// Hook para detectar mudanças de orientação
export const useOrientationChange = (callback: (orientation: string) => void): (() => void) => {
  const handleOrientationChange = () => {
    const newOrientation = window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
    callback(newOrientation);
    MobileDebugger.log('Orientação alterada', { orientation: newOrientation });
  };
  
  window.addEventListener('orientationchange', handleOrientationChange);
  window.addEventListener('resize', handleOrientationChange);
  
  // Cleanup function
  return () => {
    window.removeEventListener('orientationchange', handleOrientationChange);
    window.removeEventListener('resize', handleOrientationChange);
  };
};

// Detecta problemas específicos de mobile
export const detectMobileIssues = (): string[] => {
  const issues: string[] = [];
  const deviceInfo = getDeviceInfo();
  const networkInfo = getNetworkInfo();
  
  // Verifica se é um dispositivo móvel muito antigo
  if (deviceInfo.isMobile && deviceInfo.devicePixelRatio < 1.5) {
    issues.push('Dispositivo móvel com baixa densidade de pixels detectado');
  }
  
  // Verifica problemas de rede
  if (!networkInfo.isOnline) {
    issues.push('Dispositivo offline');
  }
  
  if (networkInfo.effectiveType === '2g' || networkInfo.effectiveType === 'slow-2g') {
    issues.push('Conexão muito lenta detectada (2G)');
  }
  
  // Verifica suporte a touch
  if (deviceInfo.isMobile && !deviceInfo.touchSupport) {
    issues.push('Dispositivo móvel sem suporte a touch detectado');
  }
  
  // Verifica tamanho de tela muito pequeno
  if (deviceInfo.screenWidth < 320) {
    issues.push('Tela muito pequena detectada (< 320px)');
  }
  
  // Verifica navegadores problemáticos
  if (deviceInfo.browser === 'Unknown') {
    issues.push('Navegador não identificado');
  }
  
  // Verifica se JavaScript está funcionando corretamente
  try {
    const testArray = [1, 2, 3];
    const testResult = testArray.map(x => x * 2);
    if (testResult.length !== 3) {
      issues.push('Problemas com JavaScript básico detectados');
    }
  } catch (e) {
    issues.push('Erro crítico de JavaScript detectado');
  }
  
  return issues;
};

// Inicializa o debugging mobile
export const initMobileDebugging = (): void => {
  const deviceInfo = getDeviceInfo();
  const networkInfo = getNetworkInfo();
  const issues = detectMobileIssues();
  
  MobileDebugger.log('Sistema inicializado', {
    deviceInfo,
    networkInfo,
    issues,
    url: window.location.href,
    timestamp: new Date().toISOString()
  });
  
  // Log de erros não capturados
  window.addEventListener('error', (event) => {
    MobileDebugger.log('Erro JavaScript não capturado', {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      error: event.error?.toString()
    });
  });
  
  // Log de promises rejeitadas
  window.addEventListener('unhandledrejection', (event) => {
    MobileDebugger.log('Promise rejeitada não tratada', {
      reason: event.reason?.toString(),
      promise: event.promise
    });
  });
  
  // Log de mudanças de conectividade
  window.addEventListener('online', () => {
    MobileDebugger.log('Dispositivo ficou online');
  });
  
  window.addEventListener('offline', () => {
    MobileDebugger.log('Dispositivo ficou offline');
  });
  
  // Log inicial de problemas detectados
  if (issues.length > 0) {
    MobileDebugger.log('Problemas detectados na inicialização', { issues });
  }
};