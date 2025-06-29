async function submitTask() {
    const user_id = document.getElementById('user_id').value;
    const input_type = document.getElementById('input_type').value;
    const input_content = document.getElementById('input_content').value;
    const payload = { user_id, input_type, input_content };
    showResult('⏳ 正在提交任务...');
    
    try {
        const resp = await fetch('/ai-animation/submit-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
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