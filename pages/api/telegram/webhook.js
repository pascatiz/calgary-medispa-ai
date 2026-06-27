export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const token = process.env.TELEGRAM_BOT_TOKEN;
  if (!token) return res.status(500).json({ error: 'Bot token not configured' });
  const { message } = req.body;
  if (!message) return res.status(200).json({ ok: true });
  const chatId = message.chat.id;
  const text = message.text || '';
  let reply = 'Hello from PeterOS Calgary MediSpa AI!';
  if (text === '/start') reply = 'Welcome to @PeterOSCalgaryMedispaBot! I am your clinic AI assistant.';
  else if (text === '/help') reply = 'Commands: /start /help /status';
  else if (text === '/status') reply = 'PeterOS is online and operational.';
  await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text: reply })
  });
  return res.status(200).json({ ok: true });
}
