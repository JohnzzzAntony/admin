/**
 * AI Store Manager - Global Admin Widget
 * Injects a floating AI Agent into the Django Admin UI.
 */
document.addEventListener('DOMContentLoaded', function() {
    // 1. Create the Styles
    const style = document.createElement('style');
    style.innerHTML = `
        #ai-agent-widget { position: fixed; bottom: 30px; right: 30px; z-index: 9999; font-family: sans-serif; }
        #ai-agent-btn { 
            width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #a855f7, #6366f1);
            color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4); border: 2px solid rgba(255,255,255,0.2);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #ai-agent-btn:hover { transform: scale(1.1); }
        #ai-agent-panel {
            position: absolute; bottom: 80px; right: 0; width: 350px; height: 500px;
            background: #0f172a; border-radius: 20px; display: none; flex-direction: column;
            overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
        }
        #ai-agent-panel.active { display: flex; animation: slideUp 0.3s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        #ai-agent-header { padding: 15px 20px; background: rgba(30,41,59,0.5); border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; }
        #ai-agent-messages { flex: 1; padding: 15px; overflow-y: auto; color: #fff; font-size: 0.9rem; }
        #ai-agent-input-container { padding: 15px; background: rgba(15,23,42,0.8); display: flex; gap: 10px; }
        #ai-agent-input { 
            flex: 1; background: #1e293b; border: 1px solid rgba(255,255,255,0.1); color: #fff;
            border-radius: 10px; padding: 10px; outline: none; font-size: 0.85rem;
        }
        #ai-agent-send { background: #6366f1; color: #fff; border: none; padding: 10px 15px; border-radius: 10px; cursor: pointer; }
    `;
    document.head.appendChild(style);

    // 2. Create the Elements
    const widget = document.createElement('div');
    widget.id = 'ai-agent-widget';
    widget.innerHTML = `
        <div id="ai-agent-panel">
            <div id="ai-agent-header">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #22c55e; margin-right: 8px;"></div>
                <strong style="color: #fff;">AI Store Manager</strong>
            </div>
            <div id="ai-agent-messages">
                <div style="background: rgba(30,41,59,0.8); padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #6366f1;">
                    Hello admin! I can help you add categories or products right from here. Try saying "Add category Electronics".
                </div>
            </div>
            <div id="ai-agent-input-container">
                <input type="text" id="ai-agent-input" placeholder="Type a command...">
                <button id="ai-agent-send"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <div id="ai-agent-btn">
            <i class="fas fa-robot fa-2x"></i>
        </div>
    `;
    document.body.appendChild(widget);

    // 3. Logic
    const btn = document.getElementById('ai-agent-btn');
    const panel = document.getElementById('ai-agent-panel');
    const input = document.getElementById('ai-agent-input');
    const send = document.getElementById('ai-agent-send');
    const messages = document.getElementById('ai-agent-messages');

    btn.addEventListener('click', () => panel.classList.toggle('active'));

    async function handleCommand() {
        const prompt = input.value.trim();
        if (!prompt) return;

        // Add user message
        const userMsg = document.createElement('div');
        userMsg.style.cssText = "background: #6366f1; padding: 10px; border-radius: 10px; margin-bottom: 10px; align-self: flex-end; color: #fff;";
        userMsg.textContent = prompt;
        messages.appendChild(userMsg);
        input.value = '';
        messages.scrollTop = messages.scrollHeight;

        try {
            const response = await fetch('/ai-manager/api/process/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt })
            });
            const data = await response.json();
            
            const aiMsg = document.createElement('div');
            aiMsg.style.cssText = "background: rgba(30,41,59,0.8); padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #6366f1; color: #fff;";
            aiMsg.innerHTML = data.response || "I processed that request!";
            messages.appendChild(aiMsg);
            messages.scrollTop = messages.scrollHeight;
        } catch (e) {
            console.error(e);
        }
    }

    send.addEventListener('click', handleCommand);
    input.addEventListener('keypress', (e) => { if(e.key === 'Enter') handleCommand(); });
});
