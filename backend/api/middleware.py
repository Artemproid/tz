import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger('api')


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware для логирования API запросов."""
    
    def process_request(self, request):          
        request.start_time = time.time()
        
        logger.info(
            f"Incoming request: {request.method} {request.path} "
            f"from {self.get_client_ip(request)}"
        )
        
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            logger.info(
                f"Response: {request.method} {request.path} "
                f"Status: {response.status_code} "
                f"Duration: {duration:.3f}s"
            )
            
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RateLimitMiddleware(MiddlewareMixin):
    """Middleware для ограничения количества запросов."""
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.rate_limit = getattr(settings, 'RATE_LIMIT', 100)  
        self.rate_limit_window = 60  
    
    def process_request(self, request):
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None
        
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit:{client_ip}"
        
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= self.rate_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'detail': f'Maximum {self.rate_limit} requests per minute allowed'
            }, status=429)
        
        cache.set(cache_key, current_requests + 1, self.rate_limit_window)
        
        return None
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class HealthCheckMiddleware(MiddlewareMixin):
    """Middleware для проверки здоровья приложения."""
    
    def process_request(self, request):
        if request.path == '/api/health/':
            from django.db import connection
            from django.core.cache import cache
            
            status = {
                'status': 'healthy',
                'timestamp': time.time(),
                'checks': {}
            }
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                status['checks']['database'] = 'healthy'
            except Exception as e:
                status['checks']['database'] = f'unhealthy: {str(e)}'
                status['status'] = 'unhealthy'
            
            try:
                cache.set('health_check', 'ok', 10)
                cache.get('health_check')
                status['checks']['cache'] = 'healthy'
            except Exception as e:
                status['checks']['cache'] = f'unhealthy: {str(e)}'
                status['status'] = 'unhealthy'
            
            import shutil
            try:
                disk_usage = shutil.disk_usage('/')
                free_space_gb = disk_usage.free / (1024**3)
                if free_space_gb < 1:  
                    status['checks']['disk_space'] = f'warning: {free_space_gb:.1f}GB free'
                    status['status'] = 'warning'
                else:
                    status['checks']['disk_space'] = f'healthy: {free_space_gb:.1f}GB free'
            except Exception as e:
                status['checks']['disk_space'] = f'error: {str(e)}'
            
            return JsonResponse(status)
        
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware для добавления заголовков безопасности."""
    
    def process_response(self, request, response):
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }
        
        if request.is_secure():
            security_headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        for header, value in security_headers.items():
            response[header] = value
        
        return response


class APIVersionMiddleware(MiddlewareMixin):
    """Middleware для версионирования API."""
    
    def process_request(self, request):
        api_version = getattr(settings, 'API_VERSION', '1.0')
        request.META['HTTP_API_VERSION'] = api_version
        
        return None
    
    def process_response(self, request, response):
        api_version = getattr(settings, 'API_VERSION', '1.0')
        response['X-API-Version'] = api_version
        
        return response


class CORSMiddleware(MiddlewareMixin):
    """Middleware для обработки CORS."""
    
    def process_response(self, request, response):
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', ['http://localhost:3000'])
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin in allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
        
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'  
        
        return response
    
    def process_request(self, request):
        if request.method == 'OPTIONS':
            response = JsonResponse({})
            return self.process_response(request, response)
        
        return None 