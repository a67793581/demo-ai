// 全局变量
let isInputValid = false;

// 输入类型改变时的处理
function onInputTypeChange() {
    const inputType = document.getElementById('input_type').value;
    const inputContent = document.getElementById('input_content');
    const inputHint = document.getElementById('input_hint');
    const inputContentLabel = document.getElementById('input_content_label');
    
    if (inputType === 'image') {
        inputContentLabel.textContent = '图片URL:';
        inputContent.placeholder = '请输入图片URL (支持 jpg, png, gif, bmp, webp, svg)';
        inputHint.textContent = '请输入有效的图片URL，支持HTTP/HTTPS协议，最大文件大小10MB';
        inputContent.value = 'https://example.com/image.jpg';
    } else {
        inputContentLabel.textContent = '输入内容:';
        inputContent.placeholder = '请输入文字内容或图片URL';
        inputHint.textContent = '请输入要生成动画的文字描述';
        inputContent.value = '请生成一个关于Python编程的教学动画';
    }
    
    // 重置验证状态
    isInputValid = false;
    updateValidationMessage('', '');
    updateSubmitButton();
}

// 验证输入内容
async function validateInput() {
    const inputType = document.getElementById('input_type').value;
    const inputContent = document.getElementById('input_content').value.trim();
    
    if (!inputContent) {
        updateValidationMessage('输入内容不能为空', 'error');
        isInputValid = false;
        updateSubmitButton();
        return;
    }
    
    if (inputType === 'image') {
        await validateImageUrl(inputContent);
    } else {
        // 文字类型的基本验证
        if (inputContent.length < 5) {
            updateValidationMessage('文字内容至少需要5个字符', 'error');
            isInputValid = false;
        } else {
            updateValidationMessage('✓ 文字内容格式正确', 'success');
            isInputValid = true;
        }
        updateSubmitButton();
    }
}

// 验证图片URL
async function validateImageUrl(url) {
    updateValidationMessage('⏳ 正在验证图片URL...', 'info');
    
    try {
        // 基本URL格式验证
        if (!isValidUrl(url)) {
            updateValidationMessage('❌ URL格式不正确，请检查协议和域名', 'error');
            isInputValid = false;
            updateSubmitButton();
            return;
        }
        
        // 检查文件扩展名
        const supportedFormats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'];
        const urlLower = url.toLowerCase();
        const hasValidExtension = supportedFormats.some(ext => urlLower.includes(ext));
        
        if (!hasValidExtension) {
            updateValidationMessage(`❌ 不支持的图片格式，支持的格式: ${supportedFormats.join(', ')}`, 'error');
            isInputValid = false;
            updateSubmitButton();
            return;
        }
        
        // 尝试访问图片URL
        const response = await fetch(url, { method: 'HEAD' });
        
        if (response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.startsWith('image/')) {
                const contentLength = response.headers.get('content-length');
                if (contentLength) {
                    const fileSize = parseInt(contentLength);
                    const maxSize = 10 * 1024 * 1024; // 10MB
                    if (fileSize > maxSize) {
                        updateValidationMessage(`❌ 图片文件过大，最大支持 ${maxSize / (1024*1024)}MB`, 'error');
                        isInputValid = false;
                    } else {
                        updateValidationMessage(`✓ 图片验证通过 (${(fileSize/1024/1024).toFixed(2)}MB)`, 'success');
                        isInputValid = true;
                    }
                } else {
                    updateValidationMessage('✓ 图片验证通过', 'success');
                    isInputValid = true;
                }
            } else {
                updateValidationMessage('❌ URL指向的不是图片文件', 'error');
                isInputValid = false;
            }
        } else {
            updateValidationMessage(`❌ 图片访问失败，HTTP状态码: ${response.status}`, 'error');
            isInputValid = false;
        }
    } catch (error) {
        updateValidationMessage(`❌ 图片验证失败: ${error.message}`, 'error');
        isInputValid = false;
    }
    
    updateSubmitButton();
}

// 验证URL格式
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

// 更新验证消息
function updateValidationMessage(message, type) {
    const validationDiv = document.getElementById('validation_message');
    validationDiv.textContent = message;
    validationDiv.className = `validation-${type}`;
}

// 更新提交按钮状态
function updateSubmitButton() {
    const submitBtn = document.getElementById('submit_btn');
    submitBtn.disabled = !isInputValid;
}

async function submitTask() {
    const user_id = document.getElementById('user_id').value;
    const input_type = document.getElementById('input_type').value;
    const input_content = document.getElementById('input_content').value.trim();
    
    // 前端验证
    if (!user_id) {
        showResult('❌ 请填写用户ID');
        return;
    }
    
    if (!input_content) {
        showResult('❌ 请填写输入内容');
        return;
    }
    
    if (!isInputValid) {
        showResult('❌ 请先验证输入内容');
        return;
    }
    
    const payload = { user_id, input_type, input_content };
    showResult('⏳ 正在提交任务...');
    
    try {
        const resp = await fetch('/ai-animation/submit-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!resp.ok) {
            const errorData = await resp.json();
            throw new Error(errorData.detail || `HTTP ${resp.status}`);
        }
        
        const data = await resp.json();
        showResult('✅ 任务已提交:\n' + JSON.stringify(data, null, 2));
        if (data.task_id) {
            document.getElementById('query_task_id').value = data.task_id;
        }
    } catch (error) {
        showResult('❌ 提交任务失败: ' + error.message);
    }
}

async function queryStatus() {
    const task_id = document.getElementById('query_task_id').value;
    if (!task_id) return showResult('⚠️ 请填写任务ID');
    
    showResult('⏳ 查询中...');
    
    try {
        const resp = await fetch('/ai-animation/query-status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_id })
        });
        const data = await resp.json();
        
        let statusText = '';
        switch(data.status) {
            case 'queued':
                statusText = '📋 排队中';
                break;
            case 'processing':
                statusText = '⚙️ 处理中';
                break;
            case 'finished':
                statusText = '✅ 已完成';
                break;
            case 'failed':
                statusText = '❌ 失败';
                break;
            default:
                statusText = data.status;
        }
        
        let resultText = `📦 任务状态: ${statusText}\n`;
        resultText += `任务ID: ${data.task_id}\n`;
        resultText += `状态: ${data.status}\n`;
        
        if (data.result_url) {
            resultText += `结果URL: ${data.result_url}\n`;
        }
        
        if (data.error_message) {
            resultText += `错误信息: ${data.error_message}\n`;
        }
        
        showResult(resultText);
    } catch (error) {
        showResult('❌ 查询失败: ' + error.message);
    }
}

async function listTasks() {
    const user_id = document.getElementById('user_id').value;
    showResult('⏳ 查询中...');
    
    try {
        const resp = await fetch('/ai-animation/list-tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id, page: 1, page_size: 10 })
        });
        const data = await resp.json();
        
        let resultText = `📋 任务列表 (共 ${data.total} 个任务):\n\n`;
        
        if (data.tasks && data.tasks.length > 0) {
            data.tasks.forEach((task, index) => {
                let statusIcon = '';
                switch(task.status) {
                    case 'queued': statusIcon = '📋'; break;
                    case 'processing': statusIcon = '⚙️'; break;
                    case 'finished': statusIcon = '✅'; break;
                    case 'failed': statusIcon = '❌'; break;
                    default: statusIcon = '❓';
                }
                
                resultText += `${index + 1}. ${statusIcon} ${task.task_id}\n`;
                resultText += `   状态: ${task.status}\n`;
                resultText += `   创建时间: ${task.created_at}\n`;
                
                if (task.result_url) {
                    resultText += `   结果: ${task.result_url}\n`;
                }
                
                if (task.error_message) {
                    resultText += `   错误: ${task.error_message}\n`;
                }
                resultText += '\n';
            });
        } else {
            resultText += '暂无任务';
        }
        
        showResult(resultText);
    } catch (error) {
        showResult('❌ 获取任务列表失败: ' + error.message);
    }
}

function showResult(msg) {
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = msg;
    
    // 根据内容添加样式类
    resultDiv.className = 'result';
    if (msg.includes('✅')) {
        resultDiv.classList.add('status-finished');
    } else if (msg.includes('❌')) {
        resultDiv.classList.add('status-failed');
    } else if (msg.includes('⏳')) {
        resultDiv.classList.add('status-processing');
    } else if (msg.includes('📋')) {
        resultDiv.classList.add('status-queued');
    }
} 