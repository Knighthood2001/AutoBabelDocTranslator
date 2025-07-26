// 获取DOM元素引用
const form = document.getElementById('translationForm');
const urlInput = document.getElementById('pdfUrl');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const resultMessage = document.getElementById('resultMessage');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');
const copyCmdBtn = document.getElementById('copyCmdBtn');

// 状态与进度映射
const statusConfig = {
    'initializing': { message: '初始化翻译引擎...', progress: 0 },
    'processing': { message: '开始处理...', progress: 20 },
    'downloading': { message: '上传至翻译服务...', progress: 50 },
    'translating': { message: '翻译文档内容...', progress: 70 },
    'completed': { message: '翻译完成，准备下载...', progress: 100 },
    'error': { message: '处理失败', progress: 0 }
};

// 表单提交逻辑
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const url = urlInput.value.trim();
    if (!url) return;

    resetUI();
    
    try {
        progressContainer.style.display = 'block';
        setTimeout(() => progressContainer.classList.add('show'), 10);
        updateProgress('initializing');

        const translateRes = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!translateRes.ok) {
            throw new Error(`请求失败 (${translateRes.status})`);
        }

        const translateData = await translateRes.json();
        if (translateData.error) {
            throw new Error(translateData.error);
        }
        
        setTimeout(() => updateProgress('initializing'), 1000);
        setTimeout(() => updateProgress('processing'), 2000);
        setTimeout(() => updateProgress('downloading'), 3000);
        setTimeout(() => updateProgress('translating'), 4000);
        setTimeout(() => updateProgress('completed'), 5000);
        setTimeout(() => showResult('请等待babel-doc的翻译过程'), 6000);
        
    } catch (err) {
        showError(`提交失败: ${err.message}`);
    }
});

// 其他函数保持不变...
function updateProgress(status, customMessage = '') {
    const config = statusConfig[status] || statusConfig['initializing'];
    progressBar.style.width = `${config.progress}%`;
    progressText.innerHTML = `<span class="spinner"></span> ${customMessage || config.message}`;
}

function showResult(message) {
    progressContainer.classList.remove('show');
    setTimeout(() => {
        progressContainer.style.display = 'none';
        resultMessage.textContent = message;
        resultContainer.style.display = 'block';
        setTimeout(() => resultContainer.classList.add('show'), 10);
    }, 500);
}

function showError(message) {
    progressContainer.classList.remove('show');
    setTimeout(() => {
        progressContainer.style.display = 'none';
        errorMessage.textContent = message;
        errorContainer.style.display = 'block';
        setTimeout(() => errorContainer.classList.add('show'), 10);
    }, 500);
}

function resetUI() {
    resultContainer.classList.remove('show');
    errorContainer.classList.remove('show');
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    downloadBtn.onclick = null;
}

copyCmdBtn.addEventListener('click', () => {
    navigator.clipboard.writeText('playwright install');
    const originalHtml = copyCmdBtn.innerHTML;
    copyCmdBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>已复制';
    setTimeout(() => {
        copyCmdBtn.innerHTML = originalHtml;
    }, 2000);
});
