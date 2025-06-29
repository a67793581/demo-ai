import re
import aiohttp
import asyncio
from typing import Tuple, Optional
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class ImageValidator:
    """Image validation utility class"""
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
    
    # File size limit (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Timeout settings
    REQUEST_TIMEOUT = 10
    
    @classmethod
    def validate_url_format(cls, url: str) -> Tuple[bool, str]:
        """
        Validate URL format
        
        Args:
            url: Image URL
            
        Returns:
            (is_valid, error_message)
        """
        if not url or not isinstance(url, str):
            return False, "URL不能为空"
        
        # Check URL format
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "URL格式不正确，需要包含协议和域名"
            
            if parsed.scheme not in ['http', 'https']:
                return False, "只支持HTTP和HTTPS协议"
                
        except Exception as e:
            return False, f"URL解析失败: {str(e)}"
        
        return True, ""
    
    @classmethod
    def validate_file_extension(cls, url: str) -> Tuple[bool, str]:
        """
        Validate file extension
        
        Args:
            url: Image URL
            
        Returns:
            (is_valid, error_message)
        """
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check file extension
        file_ext = None
        for ext in cls.SUPPORTED_FORMATS:
            if path.endswith(ext):
                file_ext = ext
                break
        
        if not file_ext:
            return False, f"不支持的图片格式，支持的格式: {', '.join(cls.SUPPORTED_FORMATS)}"
        
        return True, ""
    
    @classmethod
    async def validate_image_exists(cls, url: str) -> Tuple[bool, str]:
        """
        Asynchronously validate if image exists and is accessible
        
        Args:
            url: Image URL
            
        Returns:
            (is_valid, error_message)
        """
        try:
            timeout = aiohttp.ClientTimeout(total=cls.REQUEST_TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.head(url) as response:
                    if response.status == 200:
                        # Check Content-Type
                        content_type = response.headers.get('content-type', '').lower()
                        if not content_type.startswith('image/'):
                            return False, "URL指向的不是图片文件"
                        
                        # Check file size
                        content_length = response.headers.get('content-length')
                        if content_length:
                            file_size = int(content_length)
                            if file_size > cls.MAX_FILE_SIZE:
                                return False, f"图片文件过大，最大支持 {cls.MAX_FILE_SIZE // (1024*1024)}MB"
                        
                        return True, ""
                    elif response.status == 404:
                        return False, "图片文件不存在"
                    elif response.status == 403:
                        return False, "图片文件访问被拒绝"
                    else:
                        return False, f"图片访问失败，HTTP状态码: {response.status}"
                        
        except asyncio.TimeoutError:
            return False, "图片访问超时"
        except aiohttp.ClientError as e:
            return False, f"网络请求失败: {str(e)}"
        except Exception as e:
            logger.error(f"Error occurred while validating image: {str(e)}")
            return False, f"验证图片时发生未知错误"
    
    @classmethod
    async def validate_image_url(cls, url: str) -> Tuple[bool, str]:
        """
        Complete image URL validation
        
        Args:
            url: Image URL
            
        Returns:
            (is_valid, error_message)
        """
        # 1. Validate URL format
        is_valid, error = cls.validate_url_format(url)
        if not is_valid:
            return False, error
        
        # 2. Validate file extension
        is_valid, error = cls.validate_file_extension(url)
        if not is_valid:
            return False, error
        
        # 3. Validate image existence
        is_valid, error = await cls.validate_image_exists(url)
        if not is_valid:
            return False, error
        
        return True, "" 